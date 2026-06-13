#!/usr/bin/env python3
"""
AIRO Second Brain — Earesmes Telegram Action Listener
Persistent long-poll listener for real-time button responsiveness.
Runs continuously in background. Lock-guarded to prevent duplicates.
Never prints token or chat_id.
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
LOCK_FILE       = os.path.join(STATE_RUNTIME, "telegram-listener.lock")
OFFSET_FILE     = os.path.join(STATE_RUNTIME, "telegram-update-offset")
LASTUPDATE_FILE = os.path.join(STATE_RUNTIME, "telegram-listener-last-update")
LOG_FILE        = os.path.join(REPO_DIR, "logs/telegram-listener.log")

LONG_POLL_TIMEOUT = 25    # seconds per getUpdates long-poll request
CONFLICT_409_BACKOFF_BASE = 30   # seconds to wait on 409 before retry
CONFLICT_409_MAX_BACKOFF = 300   # max backoff 5 minutes

os.makedirs(STATE_RUNTIME, exist_ok=True)
os.makedirs(ACTIONS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


# ─── Logging (file only — no stdout to prevent double-logging when nohup'd) ───
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass
    # Also print to stderr for real-time debugging when run interactively
    print(line, file=sys.stderr, flush=True)


# ─── Credentials — never printed ──────────────────────────────────────────────
def load_credentials():
    token = ""
    chat_id = ""
    if not os.path.exists(ENV_FILE):
        return None, None
    try:
        with open(ENV_FILE, "r") as f:
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
        log(f"ERROR reading credentials: {e}")
    return (token or None), (chat_id or None)


# ─── Telegram API helpers ─────────────────────────────────────────────────────
def tg_post(token: str, method: str, params: dict, timeout: int = 10) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"API {method} error: {e}")
        return {"ok": False}


class ConflictError(Exception):
    """Raised when Telegram returns 409 Conflict (another long-poll session active)"""
    pass


def tg_get_updates(token: str, offset: int, poll_timeout: int) -> list:
    url = (
        f"https://api.telegram.org/bot{token}/getUpdates"
        f"?offset={offset}&timeout={poll_timeout}&allowed_updates=callback_query"
    )
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=poll_timeout + 15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return data.get("result", [])
    except urllib.error.HTTPError as e:
        if e.code == 409:
            raise ConflictError("409 Conflict: another getUpdates session is active")
        log(f"getUpdates HTTP error {e.code}: {e}")
    except Exception as e:
        log(f"getUpdates error: {e}")
    return []


def answer_callback(token: str, callback_id: str, text: str = "🫡 Diterima."):
    tg_post(token, "answerCallbackQuery", {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": False
    })


def send_message(token: str, chat_id: str, text: str):
    tg_post(token, "sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })


# ─── Offset management ────────────────────────────────────────────────────────
def read_offset() -> int:
    if os.path.exists(OFFSET_FILE):
        try:
            return int(open(OFFSET_FILE).read().strip())
        except Exception:
            pass
    return 0


def write_offset(offset: int):
    try:
        with open(OFFSET_FILE, "w") as f:
            f.write(str(offset))
    except Exception as e:
        log(f"Failed to write offset: {e}")


# ─── Lock management ──────────────────────────────────────────────────────────
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
    if _lock_fd:
        try:
            fcntl.flock(_lock_fd, fcntl.LOCK_UN)
            _lock_fd.close()
        except Exception:
            pass
    if os.path.exists(LOCK_FILE):
        try:
            os.remove(LOCK_FILE)
        except Exception:
            pass


# ─── Action helpers ───────────────────────────────────────────────────────────
def is_already_staged(callback_id: str) -> bool:
    return os.path.exists(os.path.join(ACTIONS_DIR, f"{callback_id}.json"))


def stage_action(callback_id: str, action: str, target_id: str) -> str:
    action_file = os.path.join(ACTIONS_DIR, f"{callback_id}.json")
    payload = {
        "source": "telegram_callback_live",
        "chat_id_verified": True,
        "callback_id": callback_id,
        "action": action,
        "target_id": target_id,
        "received_at": datetime.now().isoformat(),
        "status": "pending"
    }
    with open(action_file, "w") as f:
        json.dump(payload, f, indent=2)
    log(f"Staged: inbox/telegram-actions/{callback_id}.json")
    return action_file


def run_processor():
    processor = os.path.join(REPO_DIR, "ops/telegram/telegram-action-processor.sh")
    if not os.path.exists(processor):
        log("WARNING: processor script not found")
        return
    try:
        result = subprocess.run(
            ["bash", processor],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        for line in (result.stdout or "").strip().splitlines():
            log(f"PROCESSOR: {line}")
        if result.returncode != 0 and result.stderr:
            log(f"PROCESSOR ERR: {result.stderr[:500]}")
    except subprocess.TimeoutExpired:
        log("PROCESSOR timed out after 60s")
    except Exception as e:
        log(f"PROCESSOR run failed: {e}")


# ─── Callback handler ─────────────────────────────────────────────────────────
def handle_callback(token: str, chat_id: str, update: dict):
    cb = update.get("callback_query", {})
    callback_id = cb.get("id", "")
    data        = cb.get("data", "")
    sender_cid  = str(cb.get("message", {}).get("chat", {}).get("id", ""))

    # Security: verify sender chat_id
    if sender_cid != chat_id:
        log("SECURITY: callback from unauthorized chat_id — ignored")
        return

    # Parse  action:target_id
    parts = data.split(":")
    if len(parts) >= 2:
        action    = f"{parts[0]}:{parts[1]}"
        target_id = parts[2] if len(parts) >= 3 else "none"
    else:
        action    = data
        target_id = "none"

    log(f"CALLBACK: action={action} target={target_id}")

    # Idempotency
    if is_already_staged(callback_id):
        log(f"Duplicate callback_id {callback_id} — already staged, skipping")
        answer_callback(token, callback_id, "⚡ Sudah diproses.")
        return

    # 1. Answer callback → stops spinner immediately
    answer_callback(token, callback_id, "🫡 Diterima.")

    # 2. Send visible acknowledgement message to owner
    send_message(
        token, chat_id,
        f"🫡 *Diterima. Aku proses sebentar.*\n\nAksi: {action}\nTarget: {target_id}"
    )

    # 3. Stage action JSON
    stage_action(callback_id, action, target_id)

    # 4. Run processor inline → sends readback
    run_processor()

    # 5. Update last-update timestamp
    try:
        with open(LASTUPDATE_FILE, "w") as f:
            f.write(datetime.now().isoformat())
    except Exception:
        pass


# ─── Main loop ────────────────────────────────────────────────────────────────
def main():
    token, chat_id = load_credentials()
    if not token or not chat_id:
        log("ERROR: Telegram credentials not configured. Exiting.")
        sys.exit(1)

    if not acquire_lock():
        log("Another listener instance is already running. Exiting safely.")
        sys.exit(0)

    log(f"Earesmes Telegram listener started. PID={os.getpid()}")

    def shutdown(signum, frame):
        log(f"Received signal {signum}. Shutting down.")
        release_lock()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    offset = read_offset()
    log(f"Starting from update offset={offset}")

    consecutive_errors = 0
    conflict_backoff = CONFLICT_409_BACKOFF_BASE
    conflict_notified = False
    max_errors = 10

    try:
        while True:
            try:
                updates = tg_get_updates(token, offset, LONG_POLL_TIMEOUT)
                consecutive_errors = 0
                # Reset conflict state on success
                if conflict_backoff > CONFLICT_409_BACKOFF_BASE:
                    conflict_backoff = CONFLICT_409_BACKOFF_BASE
                    conflict_notified = False
                    log("Conflict resolved. Listener active again.")
                    send_message(token, chat_id, "✅ Earesmes listener aktif kembali. Tombol Telegram responsif.")

            except ConflictError:
                log(f"409 Conflict: another getUpdates active. Backing off {conflict_backoff}s.")
                if not conflict_notified:
                    send_message(
                        token, chat_id,
                        f"⚠️ *Earesmes listener conflict.*\n\n"
                        f"Ada proses lain yang menggunakan bot token yang sama untuk getUpdates. "
                        f"Tombol Telegram tidak akan responsif live selama konflik ini.\n\n"
                        f"Kemungkinan penyebab: EarnSAI paper control bot (pid 657) aktif.\n"
                        f"Retry dalam {conflict_backoff}s."
                    )
                    conflict_notified = True
                time.sleep(conflict_backoff)
                conflict_backoff = min(conflict_backoff * 2, CONFLICT_409_MAX_BACKOFF)
                continue

            except Exception as e:
                consecutive_errors += 1
                log(f"getUpdates exception ({consecutive_errors}/{max_errors}): {e}")
                if consecutive_errors >= max_errors:
                    log("Too many consecutive errors. Exiting.")
                    break
                time.sleep(5)
                continue

            if updates:
                for update in updates:
                    if "callback_query" in update:
                        try:
                            handle_callback(token, chat_id, update)
                        except Exception as e:
                            log(f"handle_callback error: {e}")
                    offset = update["update_id"] + 1
                write_offset(offset)

    finally:
        release_lock()
        log("Listener stopped cleanly.")


if __name__ == "__main__":
    main()
