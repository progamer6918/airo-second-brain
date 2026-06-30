#!/usr/bin/env python3
"""
AIRO Telegram Gateway ? Single getUpdates Consumer + Multi-App Router
Solves 409 Conflict when multiple bots share the same bot token.

This gateway:
1. Owns the single long-poll getUpdates session for the shared bot token.
2. Routes callback_query ? AIRO Earesmes listener (via action staging)
3. Routes text messages with earnsai commands ? earnsai via local IPC (socket/file)
4. Routes ordinary natural-language text ? durable NL queue (nonblocking)
5. Photo/document/unsupported ? silently ignored

Architecture:
  [Telegram API] ? [Gateway long-poll] ? [AIRO callback handler]
                                       ? [EarnSAI text command handler]
                                       ? [NL queue ? airo-hermes-worker]

Lock: state/runtime/telegram-gateway.lock
Offset: state/runtime/telegram-gateway-offset
Log: logs/telegram-gateway.log

The old telegram-action-listener.py should be STOPPED when gateway is running.
EarnSAI paper control bot must be STOPPED and replaced by gateway's earnsai router.

Usage:
  python3 ops/telegram/telegram-gateway.py
"""


# AIRO_C3M3_WEBHOOK_ACTIVE_POLLING_GUARD_BEGIN
def _airo_c3m3_exit_if_webhook_active_():
    """
    Local polling guard.
    Telegram Bot API forbids getUpdates while webhook is active.
    Production AIRO Arfin uses Cloudflare Worker webhook, so this local gateway
    must fail closed unless AIRO_ALLOW_TELEGRAM_POLLING=1 is explicitly set.
    """
    import os as _os
    import sys as _sys
    import json as _json
    import urllib.request as _urllib_request
    from pathlib import Path as _Path

    if _os.environ.get("AIRO_ALLOW_TELEGRAM_POLLING") == "1":
        return

    env_path = _Path(_os.environ.get("AIRO_TELEGRAM_ENV", "/home/egitaristorandas/.airo/telegram.env"))
    if not env_path.exists():
        return

    token = ""
    try:
        for _line in env_path.read_text(encoding="utf-8").splitlines():
            if _line.startswith("AIRO_TELEGRAM_BOT_TOKEN="):
                token = _line.split("=", 1)[1].strip()
                break
    except Exception:
        return

    if not token:
        return

    try:
        _raw = _urllib_request.urlopen(
            "https://api.telegram.org/bot" + token + "/getWebhookInfo",
            timeout=15
        ).read().decode("utf-8")
        _data = _json.loads(_raw)
        _url = ((_data.get("result") or {}).get("url") or "").strip()
        if _url:
            _sys.stderr.write("[AIRO_C3M3] WEBHOOK_ACTIVE=YES; local getUpdates gateway disabled. Set AIRO_ALLOW_TELEGRAM_POLLING=1 only after deleting webhook.\n")
            _sys.exit(0)
    except Exception as _err:
        _sys.stderr.write("[AIRO_C3M3] webhook guard check failed; refusing local polling fail-closed: " + str(_err) + "\n")
        _sys.exit(0)

_airo_c3m3_exit_if_webhook_active_()
# AIRO_C3M3_WEBHOOK_ACTIVE_POLLING_GUARD_END

import sys
import os
import json
import time
import signal
import fcntl
import urllib.request
import urllib.parse
import urllib.error
import subprocess
import uuid
from datetime import datetime

# ??? Paths ????????????????????????????????????????????????????????????????????
REPO_DIR        = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
ENV_FILE        = "/home/egitaristorandas/.airo/telegram.env"
ACTIONS_DIR     = os.path.join(REPO_DIR, "inbox/telegram-actions")
STATE_RUNTIME   = os.path.join(REPO_DIR, "state/runtime")
LOCK_FILE       = os.path.join(STATE_RUNTIME, "telegram-gateway.lock")
OFFSET_FILE     = os.path.join(STATE_RUNTIME, "telegram-gateway-offset")
LASTUPDATE_FILE = os.path.join(STATE_RUNTIME, "telegram-gateway-last-update")
LOG_FILE        = os.path.join(REPO_DIR, "logs/telegram-gateway.log")
SHORTID_SCRIPT  = os.path.join(REPO_DIR, "scripts/airo-manual-queue-shortid")

# NL queue ? ordinary natural-language text messages for airo-hermes-worker
LOCAL_STATE_DIR = os.path.expanduser(
    "~/.local/state/airo-second-brain/hermes-bridge"
)
NL_QUEUE_DIR    = os.path.join(LOCAL_STATE_DIR, "queue")

# EarnSAI routing (file-based IPC ? earnsai bot reads from this dir)
EARNSAI_ROUTE_DIR = os.path.join(os.path.expanduser("~"), ".config/earnsai-pulse/gateway-inbox")

LONG_POLL_TIMEOUT = 25

def ensure_runtime_dirs():
    """Create runtime directories only when the gateway actually starts."""
    os.makedirs(STATE_RUNTIME, exist_ok=True)
    os.makedirs(ACTIONS_DIR, exist_ok=True)
    os.makedirs(LOCAL_STATE_DIR, exist_ok=True)
    os.makedirs(NL_QUEUE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


# ??? Logging ??????????????????????????????????????????????????????????????????
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"[{ts}] [GATEWAY] {msg}"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, file=sys.stderr, flush=True)


# ??? Credentials ??????????????????????????????????????????????????????????????
def load_credentials():
    token, chat_id = "", ""
    if not os.path.exists(ENV_FILE):
        return None, None
    try:
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "AIRO_TELEGRAM_BOT_TOKEN":
                        token = v
                    elif k == "AIRO_TELEGRAM_CHAT_ID":
                        chat_id = v
    except Exception as e:
        log(f"Error reading credentials: {e}")
    if not token or not chat_id:
        return None, None
    if token.startswith("YOUR_BOT_TOKEN") or chat_id.startswith("YOUR_CHAT_ID"):
        return None, None
    return token, chat_id


# ??? Telegram API helpers ??????????????????????????????????????????????????????
def tg_post(token: str, method: str, payload: dict, timeout: int = 10):
    url = f"https://api.telegram.org/bot{token}/{method}"
    params = urllib.parse.urlencode(payload).encode("utf-8")
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, data=params, method="POST"), timeout=timeout
        ) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"tg_post {method} HTTP error {e.code}: {e.read()[:200]}")
    except Exception as e:
        log(f"tg_post {method} error: {e}")
    return None


def tg_get_updates(token: str, offset: int, poll_timeout: int):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = urllib.parse.urlencode({"offset": offset, "timeout": poll_timeout}).encode("utf-8")
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, data=params, method="POST"), timeout=poll_timeout + 15
        ) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return data.get("result", [])
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:200]
        except Exception:
            pass
        log(f"getUpdates HTTP {e.code}: {body}")
    except Exception as e:
        log(f"getUpdates error: {e}")
    return None


def answer_callback(token: str, callback_id: str, text: str = "?? Diterima."):
    tg_post(token, "answerCallbackQuery", {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": False,
    })


def send_message(token: str, chat_id: str, text: str):
    tg_post(token, "sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    })


# ??? Offset + Lock ????????????????????????????????????????????????????????????
def read_offset() -> int:
    try:
        return int(open(OFFSET_FILE).read().strip())
    except Exception:
        return 0


def write_offset(offset: int):
    try:
        with open(OFFSET_FILE, "w") as f:
            f.write(str(offset))
    except Exception as e:
        log(f"Failed to write offset: {e}")


_lock_fd = None


def acquire_lock() -> bool:
    global _lock_fd
    try:
        _lock_fd = open(LOCK_FILE, "w")
        fcntl.flock(_lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _lock_fd.write(str(os.getpid()))
        _lock_fd.flush()
        return True
    except (IOError, OSError):
        return False


def release_lock():
    global _lock_fd
    try:
        if _lock_fd:
            fcntl.flock(_lock_fd, fcntl.LOCK_UN)
            _lock_fd.close()
    except Exception:
        pass
    try:
        os.remove(LOCK_FILE)
    except Exception:
        pass


# ??? Short ID resolution ??????????????????????????????????????????????????????
def resolve_short_id(id_str: str) -> str:
    if not id_str.startswith("mq-"):
        return id_str
    try:
        res = subprocess.run(
            ["python3", SHORTID_SCRIPT, "--resolve", id_str],
            capture_output=True, text=True, timeout=5, cwd=REPO_DIR,
        )
        resolved = res.stdout.strip()
        if resolved and resolved != id_str:
            log(f"Short ID resolved: {id_str} ? {resolved}")
            return resolved
    except Exception as e:
        log(f"Short ID resolution error: {e}")
    return id_str


# ??? AIRO Earesmes callback handler ??????????????????????????????????????????
def is_airo_callback(data: str) -> bool:
    return data.startswith("manualqueue:") or data.startswith("ownerreview:")


def handle_airo_callback(token: str, chat_id: str, cb: dict):
    callback_id = cb.get("id", "")
    data = cb.get("data", "")

    parts = data.split(":")
    if len(parts) >= 2:
        action = f"{parts[0]}:{parts[1]}"
        target_raw = parts[2] if len(parts) >= 3 else "none"
    else:
        action = data
        target_raw = "none"

    # Resolve short ID
    target_id = resolve_short_id(target_raw)

    action_file = os.path.join(ACTIONS_DIR, f"{callback_id}.json")
    if os.path.exists(action_file):
        log(f"Duplicate callback {callback_id} ? skipping")
        answer_callback(token, callback_id, "? Sudah diproses.")
        return

    # 1. Answer immediately
    answer_callback(token, callback_id, "?? Diterima.")

    # 2. Visible ack
    send_message(token, chat_id,
        f"?? *Diterima. Aku proses sebentar.*\n\nAksi: {action}\nTarget: {target_id}"
    )

    # 3. Stage action JSON with resolved ID
    payload = {
        "source": "telegram_gateway",
        "chat_id_verified": True,
        "callback_id": callback_id,
        "action": action,
        "target_id": target_id,
        "received_at": datetime.now().isoformat(),
        "status": "pending",
    }
    with open(action_file, "w") as f:
        json.dump(payload, f, indent=2)
    log(f"Staged: inbox/telegram-actions/{callback_id}.json ? {action} / {target_id}")

    # 4. Run processor
    processor = os.path.join(REPO_DIR, "ops/telegram/telegram-action-processor.sh")
    try:
        result = subprocess.run(
            ["bash", processor], cwd=REPO_DIR, capture_output=True, text=True, timeout=60
        )
        for line in (result.stdout or "").strip().splitlines():
            log(f"PROCESSOR: {line}")
    except Exception as e:
        log(f"PROCESSOR error: {e}")

    # Update last-update
    try:
        with open(LASTUPDATE_FILE, "w") as f:
            f.write(datetime.now().isoformat())
    except Exception:
        pass


# ??? EarnSAI text command router ?????????????????????????????????????????????
EARNSAI_COMMANDS = {"/help", "/status", "/start", "/stop", "/tail"}


def is_earnsai_command(text: str) -> bool:
    if not text:
        return False
    return any(text.strip().startswith(cmd) for cmd in EARNSAI_COMMANDS)


def route_to_earnsai(update: dict):
    """Write update to earnsai gateway inbox for earnsai to pick up."""
    os.makedirs(EARNSAI_ROUTE_DIR, exist_ok=True)
    update_id = update.get("update_id", int(time.time()))
    fpath = os.path.join(EARNSAI_ROUTE_DIR, f"{update_id}.json")
    try:
        with open(fpath, "w") as f:
            json.dump(update, f, indent=2)
        log(f"Routed update {update_id} to earnsai gateway inbox")
    except Exception as e:
        log(f"EarnSAI routing failed: {e}")


# ??? NL queue ? nonblocking enqueue for airo-hermes-worker ???????????????????
def enqueue_nl_message(
    update_id: int,
    sender_chat_id: str,
    owner_chat_id: str,
    message_id: int,
    text: str,
) -> bool:
    """
    Atomically enqueue an ordinary NL message for the Hermes worker.

    Uses tmp-file + os.replace() for atomic write on Linux ext4.
    Idempotency key: "{update_id}-{message_id}" ? existing items are never
    overwritten so duplicate Telegram delivery cannot trigger duplicate
    model calls.

    The bot token is NEVER written to the queue file.
    The chat_id stored is the verified owner chat_id from credentials.

    Returns True if enqueued, False if skipped (duplicate or unauthorized).
    """
    if sender_chat_id != owner_chat_id:
        log(f"NL SECURITY: message from unauthorized chat_id ? ignored")
        return False

    if not text or not text.strip():
        log(f"NL: empty text skipped")
        return False

    request_id = f"{update_id}-{message_id}"
    dest = os.path.join(NL_QUEUE_DIR, f"{request_id}.json")

    # Idempotency: never overwrite an existing item
    if os.path.exists(dest):
        log(f"NL queue: duplicate {request_id} ? skipping")
        return False

    item = {
        "request_id": request_id,
        "telegram_update_id": update_id,
        "chat_id": owner_chat_id,
        "message_id": message_id,
        "received_at": datetime.now().isoformat(),
        "text": text.strip(),
        "status": "pending",
        "attempt_count": 0,
        "last_attempt_at": None,
        "reply_sent": False,
    }

    tmp = dest + "." + uuid.uuid4().hex + ".tmp"
    try:
        os.makedirs(NL_QUEUE_DIR, exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(item, f, indent=2, ensure_ascii=False)
        os.replace(tmp, dest)  # atomic on Linux ext4
        log(f"NL queued: {request_id} ({len(text)} chars)")
        return True
    except Exception as e:
        log(f"NL enqueue failed for {request_id}: {e}")
        try:
            os.remove(tmp)
        except Exception:
            pass
        return False


# ??? Main update router ???????????????????????????????????????????????????????
def route_update(token: str, chat_id: str, update: dict):
    # Priority 1: callback_query (AIRO deterministic actions)
    if "callback_query" in update:
        cb = update["callback_query"]
        sender_cid = str(cb.get("message", {}).get("chat", {}).get("id", ""))
        if sender_cid != chat_id:
            log(f"SECURITY: callback from unauthorized chat_id ? ignored")
            return
        data = cb.get("data", "")
        if is_airo_callback(data):
            handle_airo_callback(token, chat_id, cb)
        else:
            log(f"Unrecognized callback data: {data[:50]}")

    elif "message" in update:
        msg = update["message"]
        text = msg.get("text", "")
        sender_cid = str(msg.get("chat", {}).get("id", ""))

        # Priority 2: EarnSAI slash commands
        if is_earnsai_command(text):
            route_to_earnsai(update)

        # Priority 3: ordinary NL text ? nonblocking enqueue
        elif text and text.strip():
            update_id = update.get("update_id", int(time.time()))
            message_id = msg.get("message_id", 0)
            enqueue_nl_message(
                update_id=update_id,
                sender_chat_id=sender_cid,
                owner_chat_id=chat_id,
                message_id=message_id,
                text=text.strip(),
            )

        # Priority 4: photo/document/unsupported ? silently ignore
        else:
            log(f"Ignored non-text message (photo/document/sticker/etc)")


# ??? Main ?????????????????????????????????????????????????????????????????????
def main():
    ensure_runtime_dirs()
    token, chat_id = load_credentials()
    if not token or not chat_id:
        log("ERROR: Telegram credentials not configured. Exiting.")
        sys.exit(1)

    if not acquire_lock():
        log("Another gateway instance is already running. Exiting safely.")
        sys.exit(0)

    log(f"Telegram Gateway started. PID={os.getpid()}")

    def shutdown(signum, frame):
        log(f"Signal {signum} received. Shutting down.")
        release_lock()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    offset = read_offset()
    log(f"Starting from offset={offset}")

    consecutive_errors = 0
    max_errors = 20
    backoff = 5

    try:
        while True:
            updates = tg_get_updates(token, offset, LONG_POLL_TIMEOUT)

            if updates is None or (isinstance(updates, list) and len(updates) == 0 and consecutive_errors > 0):
                # Likely a recoverable error ? backoff
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    log("Too many consecutive errors. Exiting.")
                    break
                wait = min(backoff * consecutive_errors, 120)
                log(f"Backing off {wait}s (error #{consecutive_errors})")
                time.sleep(wait)
                continue

            if updates:
                consecutive_errors = 0
                backoff = 5
                for update in updates:
                    try:
                        route_update(token, chat_id, update)
                    except Exception as e:
                        log(f"route_update error: {e}")
                    offset = update["update_id"] + 1
                write_offset(offset)

    finally:
        release_lock()
        log("Gateway stopped cleanly.")


if __name__ == "__main__":
    main()
