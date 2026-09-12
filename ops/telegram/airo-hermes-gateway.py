#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ops/telegram/airo-hermes-gateway.py
AIRO Hermes Dedicated Telegram Gateway — Live getUpdates ingress for AIRO Hermes Alpha.

Reads credentials from ~/.config/airo/airo-hermes-telegram.env.
Enqueues incoming messages to ~/.local/state/airo-second-brain/airo-hermes-bridge/queue/
Strictly isolated from Earesmes gateway and queues.
"""

import os
import sys
import json
import time
import fcntl
import signal
import logging
import urllib.request
import urllib.parse
import urllib.error
import uuid
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List

# ─── Canonical Paths ──────────────────────────────────────────────────────────
REPO_DIR = os.environ.get("AIRO_REPO_DIR", os.path.expanduser("~/AI_WORKSPACES/airo-second-brain"))
ENV_FILE = os.path.expanduser("~/.config/airo/airo-hermes-telegram.env")

LOCAL_STATE_DIR = os.path.expanduser("~/.local/state/airo-second-brain/airo-hermes-bridge")
NL_QUEUE_DIR = os.path.join(LOCAL_STATE_DIR, "queue")
DEAD_DIR = os.path.join(LOCAL_STATE_DIR, "dead")

RUNTIME_STATE_DIR = os.path.join(REPO_DIR, "state/runtime")
LOCK_FILE = os.path.join(RUNTIME_STATE_DIR, "airo-hermes-gateway.lock")
OFFSET_FILE = os.path.join(RUNTIME_STATE_DIR, "airo-hermes-gateway-offset")
LAST_UPDATE_FILE = os.path.join(RUNTIME_STATE_DIR, "airo-hermes-gateway-last-update")
LOG_FILE = os.path.join(REPO_DIR, "logs/airo-hermes-gateway.log")

LONG_POLL_TIMEOUT = 30
_lock_fd = None

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("airo-hermes-gateway")

def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
    logger.info(msg)


# ─── 1. Credentials & Allowlist Loading ──────────────────────────────────────
def load_credentials() -> Tuple[str, str]:
    token = os.environ.get("AIRO_HERMES_TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("OWNER_TELEGRAM_ID") or os.environ.get("AIRO_TELEGRAM_CHAT_ID", "").strip()

    if (not token or not chat_id) and os.path.exists(ENV_FILE):
        try:
            with open(ENV_FILE, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("export "):
                        line = line[7:]
                    if "=" in line and not line.startswith("#"):
                        k, v = line.split("=", 1)
                        v = v.strip('"' + "'")
                        if k == "AIRO_HERMES_TELEGRAM_BOT_TOKEN" and not token:
                            token = v
                        elif k in ("OWNER_TELEGRAM_ID", "AIRO_TELEGRAM_CHAT_ID") and not chat_id:
                            chat_id = v
        except Exception as e:
            log(f"Failed reading env file {ENV_FILE}: {e}")

    # Fallback to canonical owner chat id if unspecified
    if not chat_id:
        chat_id = "8482041086"

    return token, str(chat_id)


# ─── 2. Lock Management (flock + PID verification) ───────────────────────────
def acquire_lock() -> bool:
    global _lock_fd
    os.makedirs(RUNTIME_STATE_DIR, exist_ok=True)
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
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except Exception:
        pass


# ─── 3. Offset Persistence ───────────────────────────────────────────────────
def read_offset() -> int:
    if os.path.exists(OFFSET_FILE):
        try:
            with open(OFFSET_FILE, encoding="utf-8") as f:
                txt = f.read().strip()
                if txt.isdigit():
                    return int(txt)
        except Exception:
            pass
    return 0


def write_offset(offset: int):
    os.makedirs(RUNTIME_STATE_DIR, exist_ok=True)
    tmp = OFFSET_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(str(offset))
        os.replace(tmp, OFFSET_FILE)
    except Exception as e:
        log(f"Failed to write offset {offset}: {e}")


def update_last_tick():
    os.makedirs(RUNTIME_STATE_DIR, exist_ok=True)
    tmp = LAST_UPDATE_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
        os.replace(tmp, LAST_UPDATE_FILE)
    except Exception:
        pass


# ─── 4. Telegram API getUpdates ──────────────────────────────────────────────
def tg_get_updates(token: str, offset: int, timeout: int = 30) -> Tuple[Optional[List[dict]], Optional[int]]:
    url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout={timeout}"
    req = urllib.request.Request(url, headers={"User-Agent": "AIRO-Hermes-Gateway/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=timeout + 10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return data.get("result", []), None
            return None, None
    except urllib.error.HTTPError as e:
        if e.code == 409:
            log("FATAL: Telegram API returned HTTP 409 Conflict (competing getUpdates consumer). Failing closed.")
            return None, 409
        log(f"Telegram getUpdates HTTP Error: {e.code}")
        return None, e.code
    except Exception as e:
        log(f"Telegram getUpdates error: {e}")
        return None, None


# ─── 5. Atomic Hermes Queue Enqueue ──────────────────────────────────────────
def enqueue_nl_message(update_id: int, sender_chat_id: str, owner_chat_id: str, message_id: int, text: str) -> bool:
    if str(sender_chat_id) != str(owner_chat_id):
        log(f"SECURITY: Ignore message from unauthorized chat_id {sender_chat_id} (not matching owner allowlist)")
        return False

    if not text or not text.strip():
        return False

    os.makedirs(NL_QUEUE_DIR, exist_ok=True)
    request_id = f"req-{update_id}-{message_id}"
    dest_file = os.path.join(NL_QUEUE_DIR, f"{update_id}_{message_id}.json")

    if os.path.exists(dest_file):
        log(f"NL Queue: duplicate message {request_id} — skipping")
        return False

    item = {
        "request_id": request_id,
        "telegram_update_id": update_id,
        "chat_id": str(owner_chat_id),
        "message_id": message_id,
        "received_at": datetime.now().isoformat(),
        "text": text.strip(),
        "status": "pending",
        "attempt_count": 0,
        "last_attempt_at": None,
        "reply_sent": False
    }

    tmp_file = dest_file + "." + uuid.uuid4().hex + ".tmp"
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(item, f, indent=2, ensure_ascii=False)
        os.replace(tmp_file, dest_file)
        log(f"Enqueued NL message {request_id} to AIRO Hermes bridge queue.")
        update_last_tick()
        return True
    except Exception as e:
        log(f"Failed to enqueue message {request_id}: {e}")
        try:
            os.remove(tmp_file)
        except Exception:
            pass
        return False


def route_update(owner_chat_id: str, update: dict):
    if "message" in update:
        msg = update["message"]
        sender_cid = str(msg.get("chat", {}).get("id", ""))
        text = msg.get("text", "")
        update_id = update.get("update_id", 0)
        message_id = msg.get("message_id", 0)

        if text and text.strip():
            enqueue_nl_message(update_id, sender_cid, owner_chat_id, message_id, text)


# ─── 6. Live Main Loop & Entry Point ─────────────────────────────────────────
def run_live_gateway():
    log("Starting AIRO Hermes Telegram Gateway live polling loop...")
    token, owner_chat_id = load_credentials()

    if not token or not owner_chat_id:
        log(f"ERROR: Bot token or Owner chat_id not configured in {ENV_FILE}. Exiting.")
        sys.exit(1)

    if not acquire_lock():
        log("Another AIRO Hermes gateway instance holds the lock. Exiting safely.")
        sys.exit(0)

    log(f"AIRO Hermes Gateway lock acquired. PID={os.getpid()}")

    def shutdown(signum, frame):
        log(f"Signal {signum} received. Stopping live gateway.")
        release_lock()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    offset = read_offset()
    log(f"Live polling started with offset={offset}")

    consecutive_errors = 0
    max_errors = 20

    try:
        while True:
            updates, err_code = tg_get_updates(token, offset, LONG_POLL_TIMEOUT)

            if err_code == 409:
                log("FATAL: Telegram HTTP 409 Conflict. Exiting to prevent competing polling loop.")
                break

            if updates is None:
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    log("Exceeded max consecutive network errors. Exiting.")
                    break
                time.sleep(min(5 * consecutive_errors, 60))
                continue

            consecutive_errors = 0
            for update in updates:
                try:
                    route_update(owner_chat_id, update)
                except Exception as e:
                    log(f"Error routing update: {e}")
                offset = update.get("update_id", offset) + 1
                write_offset(offset)

    finally:
        release_lock()
        log("AIRO Hermes live gateway stopped cleanly.")

if __name__ == "__main__":
    run_live_gateway()
