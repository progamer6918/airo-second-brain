#!/usr/bin/env python3
"""
AIRO Telegram Gateway — Single getUpdates Consumer + Multi-App Router
Solves 409 Conflict when multiple bots share the same bot token.

This gateway:
1. Owns the single long-poll getUpdates session for the shared bot token.
2. Routes callback_query → AIRO Earesmes listener (via action staging)
3. Routes text messages with earnsai commands → earnsai via local IPC (socket/file)
4. All other events are routed to the appropriate handler.

Architecture:
  [Telegram API] → [Gateway long-poll] → [AIRO callback handler]
                                       → [EarnSAI text command handler]

Lock: state/runtime/telegram-gateway.lock
Offset: state/runtime/telegram-gateway-offset
Log: logs/telegram-gateway.log

The old telegram-action-listener.py should be STOPPED when gateway is running.
EarnSAI paper control bot must be STOPPED and replaced by gateway's earnsai router.

Usage:
  python3 ops/telegram/telegram-gateway.py
"""

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
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_DIR        = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
ENV_FILE        = "/home/egitaristorandas/.airo/telegram.env"
ACTIONS_DIR     = os.path.join(REPO_DIR, "inbox/telegram-actions")
STATE_RUNTIME   = os.path.join(REPO_DIR, "state/runtime")
LOCK_FILE       = os.path.join(STATE_RUNTIME, "telegram-gateway.lock")
OFFSET_FILE     = os.path.join(STATE_RUNTIME, "telegram-gateway-offset")
LASTUPDATE_FILE = os.path.join(STATE_RUNTIME, "telegram-gateway-last-update")
LOG_FILE        = os.path.join(REPO_DIR, "logs/telegram-gateway.log")
SHORTID_SCRIPT  = os.path.join(REPO_DIR, "scripts/airo-manual-queue-shortid")

# EarnSAI routing (file-based IPC — earnsai bot reads from this dir)
EARNSAI_ROUTE_DIR = os.path.join(os.path.expanduser("~"), ".config/earnsai-pulse/gateway-inbox")

LONG_POLL_TIMEOUT = 25

os.makedirs(STATE_RUNTIME, exist_ok=True)
os.makedirs(ACTIONS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


# ─── Logging ──────────────────────────────────────────────────────────────────
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"[{ts}] [GATEWAY] {msg}"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, file=sys.stderr, flush=True)


# ─── Credentials ──────────────────────────────────────────────────────────────
def load_credentials():
    token, chat_id = "", ""
    if not os.path.exists(ENV_FILE):
        return None, None
    try:
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                if k == "AIRO_TELEGRAM_BOT_TOKEN":
                    token = v
                elif k == "AIRO_TELEGRAM_CHAT_ID":
                    chat_id = v
    except Exception as e:
        log(f"ERROR reading credentials: {e}")
    return (token or None), (chat_id or None)


# ─── Telegram API ─────────────────────────────────────────────────────────────
def tg_post(token: str, method: str, params: dict, timeout: int = 10) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, data=data, method="POST"), timeout=timeout
        ) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"API {method} error: {e}")
        return {"ok": False}


def tg_get_updates(token: str, offset: int, poll_timeout: int) -> list:
    url = (
        f"https://api.telegram.org/bot{token}/getUpdates"
        f"?offset={offset}&timeout={poll_timeout}"
    )
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url), timeout=poll_timeout + 15
        ) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return data.get("result", [])
    except urllib.error.HTTPError as e:
        if e.code == 409:
            log("409 Conflict — another getUpdates session still active. Retrying after backoff.")
        else:
            log(f"getUpdates HTTP {e.code}: {e}")
    except Exception as e:
        log(f"getUpdates error: {e}")
    return []


def answer_callback(token: str, callback_id: str, text: str = "🫡 Diterima."):
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


# ─── Offset + Lock ────────────────────────────────────────────────────────────
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


# ─── Short ID resolution ──────────────────────────────────────────────────────
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
            log(f"Short ID resolved: {id_str} → {resolved}")
            return resolved
    except Exception as e:
        log(f"Short ID resolution error: {e}")
    return id_str


# ─── AIRO Earesmes callback handler ──────────────────────────────────────────
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
        log(f"Duplicate callback {callback_id} — skipping")
        answer_callback(token, callback_id, "⚡ Sudah diproses.")
        return

    # 1. Answer immediately
    answer_callback(token, callback_id, "🫡 Diterima.")

    # 2. Visible ack
    send_message(token, chat_id,
        f"🫡 *Diterima. Aku proses sebentar.*\n\nAksi: {action}\nTarget: {target_id}"
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
    log(f"Staged: inbox/telegram-actions/{callback_id}.json → {action} / {target_id}")

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


# ─── EarnSAI text command router ─────────────────────────────────────────────
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


# ─── Main update router ───────────────────────────────────────────────────────
def route_update(token: str, chat_id: str, update: dict):
    if "callback_query" in update:
        cb = update["callback_query"]
        sender_cid = str(cb.get("message", {}).get("chat", {}).get("id", ""))
        if sender_cid != chat_id:
            log(f"SECURITY: callback from unauthorized chat_id — ignored")
            return
        data = cb.get("data", "")
        if is_airo_callback(data):
            handle_airo_callback(token, chat_id, cb)
        else:
            log(f"Unrecognized callback data: {data[:50]}")

    elif "message" in update:
        msg = update["message"]
        text = msg.get("text", "")
        if is_earnsai_command(text):
            route_to_earnsai(update)
        # Other messages: silently ignore or log
        else:
            log(f"Ignored non-command message")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
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
                # Likely a recoverable error — backoff
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
