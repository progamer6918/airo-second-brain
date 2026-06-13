#!/usr/bin/env bash
exec python3 - "$@" << 'EOF'
import sys
import os
import json
import time
import hashlib
from datetime import datetime
import urllib.request
import urllib.parse
import fcntl

# Process locking to prevent concurrent notification spam
lock_file_path = "/tmp/airo-second-brain-telegram-notify.lock"
try:
    lock_file = open(lock_file_path, "w")
    fcntl.flock(lock_file, fcntl.LOCK_EX)
except Exception as e:
    sys.stderr.write(f"Warning: Notification lock failed: {e}\n")

# 1. Parse arguments manually
is_test = False
event_type = None
message = None
capture_id = None
extra = None

args = sys.argv[1:]
i = 0
while i < len(args):
    arg = args[i]
    if arg == "--test":
        is_test = True
    elif arg == "--type":
        if i + 1 < len(args):
            event_type = args[i+1]
            i += 1
    elif arg == "--message":
        if i + 1 < len(args):
            message = args[i+1]
            i += 1
    elif arg == "--capture-id":
        if i + 1 < len(args):
            capture_id = args[i+1]
            i += 1
    elif arg == "--extra":
        if i + 1 < len(args):
            extra = args[i+1]
            i += 1
    i += 1

# 2. Path configuration
STATE_FILE = "ops/notifications/notification-state.json"
ENV_FILE = "/home/egitaristorandas/.airo/telegram.env"

# 3. Read telegram.env safely (do not expose or print values)
token = ""
chat_id = ""
if os.path.exists(ENV_FILE):
    try:
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "AIRO_TELEGRAM_BOT_TOKEN":
                        token = v.strip()
                    elif k.strip() == "AIRO_TELEGRAM_CHAT_ID":
                        chat_id = v.strip()
    except Exception as e:
        sys.stderr.write(f"Error reading env file: {e}\n")

# Check if actually configured
is_configured = False
if token and chat_id:
    if not (token.startswith("YOUR_BOT_TOKEN") or chat_id.startswith("YOUR_CHAT_ID") or token.startswith("<secret>")):
        is_configured = True

telegram_status = "active" if is_configured else "log_only_unconfigured"

# 4. Load state
state = {
    "last_notification_time": None,
    "last_status": "healthy",
    "last_error_time": 0,
    "last_error_msg": "",
    "last_startup_time": 0,
    "last_review_time": 0,
    "last_review_count": 0,
    "last_latest_capture_id": "",
    "last_review_items_hash": "",
    "telegram_status": "log_only_unconfigured",
    "last_event_times": {}
}

if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            loaded = json.load(f)
            for k, v in loaded.items():
                state[k] = v
    except Exception:
        pass

state["telegram_status"] = telegram_status

def save_state():
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        sys.stderr.write(f"Error saving state: {e}\n")

def log_event(msg):
    timestamp = datetime.now().isoformat()
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/runtime.log", "a") as f:
            f.write(f"[{timestamp}] [NOTIFY] {msg}\n")
    except Exception:
        pass
    print(msg)

def send_telegram(text, reply_markup=None):
    if not is_configured:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
        
    data = urllib.parse.urlencode(payload).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            return res_json.get("ok", False)
    except Exception as e:
        sys.stderr.write(f"Telegram API Request failed: {e}\n")
        return False

# 5. Handle --test
if is_test:
    if not is_configured:
        print("TELEGRAM_TEST=SKIP_UNCONFIGURED")
        save_state()
        sys.exit(0)
    
    success = send_telegram("🔔 **AIRO Second Brain Telegram Test Message**\nStatus: Testing connection\nTime: " + datetime.now().isoformat())
    if success:
        print("TELEGRAM_TEST=PASS")
        save_state()
        sys.exit(0)
    else:
        print("TELEGRAM_TEST=FAIL")
        save_state()
        sys.exit(1)

# 6. Handle standard events
if not event_type:
    sys.stderr.write("Error: --type <type> is required when not running --test\n")
    sys.exit(1)

current_time = time.time()
should_send = False
custom_msg = ""
reply_markup = None

# Initialize last_event_times safely
state.setdefault("last_event_times", {})
for k in ["sync_failed", "runtime_blocked", "secret_guard_hit", "owner_review_needed", "runtime_online", "manual_queue_card", "owner_review_card"]:
    state["last_event_times"].setdefault(k, 0.0)

if event_type == "runtime_online":
    # Startup online cooldown: 6 hours (21600 seconds)
    time_elapsed = current_time - state["last_event_times"].get("runtime_online", 0.0)
    if time_elapsed >= 21600:
        should_send = True
        custom_msg = "🚀 **Earesmes nyala.**\n\nSecond Brain hidup, sync aman.\nAku bakal diam kalau gak ada yang penting."
        state["last_event_times"]["runtime_online"] = current_time
    else:
        log_event(f"Suppressed duplicate runtime_online event (cooldown active: {int(21600 - time_elapsed)}s left)")

elif event_type == "sync_pushed":
    log_event(f"Log-only sync_pushed (normal sync silent): {message}")

elif event_type == "sync_failed":
    # Cooldown: 60 minutes (3600 seconds)
    time_elapsed = current_time - state["last_event_times"].get("sync_failed", 0.0)
    status_changed = (state.get("last_status", "healthy") != "degraded")
    if status_changed or time_elapsed >= 3600:
        should_send = True
        state["last_event_times"]["sync_failed"] = current_time
        state["last_status"] = "degraded"
        state["last_error_time"] = current_time
        state["last_error_msg"] = message
        custom_msg = "⚠️ **Sync lagi nyangkut.**\n\nData lokal aman, aku gak maksa push.\nAku bakal diam dulu biar gak spam. Nanti kabarin kalau sudah pulih."
    else:
        log_event(f"Suppressed duplicate sync_failed event (cooldown active: {int(3600 - time_elapsed)}s left)")

elif event_type == "runtime_blocked":
    # Cooldown: 60 minutes (3600 seconds)
    time_elapsed = current_time - state["last_event_times"].get("runtime_blocked", 0.0)
    status_changed = (state.get("last_status", "healthy") != "blocked")
    if status_changed or time_elapsed >= 3600:
        should_send = True
        state["last_event_times"]["runtime_blocked"] = current_time
        state["last_status"] = "blocked"
        state["last_error_time"] = current_time
        state["last_error_msg"] = message
        custom_msg = "🚫 **Runtime terblokir.**\n\nAda conflict atau error sistem kritis."
    else:
        log_event(f"Suppressed duplicate runtime_blocked event (cooldown active: {int(3600 - time_elapsed)}s left)")

elif event_type == "secret_guard_hit":
    # Cooldown: 60 minutes (3600 seconds)
    time_elapsed = current_time - state["last_event_times"].get("secret_guard_hit", 0.0)
    status_changed = (state.get("last_status", "healthy") != "blocked")
    if status_changed or time_elapsed >= 3600:
        should_send = True
        state["last_event_times"]["secret_guard_hit"] = current_time
        state["last_status"] = "blocked"
        state["last_error_time"] = current_time
        state["last_error_msg"] = message
        custom_msg = "🚫 **Aku blokir sync.**\n\nAda yang kelihatan seperti secret. Token gak akan kupush."
    else:
        log_event(f"Suppressed duplicate secret_guard_hit event (cooldown active: {int(3600 - time_elapsed)}s left)")

elif event_type == "runtime_recovered":
    if state.get("last_status", "healthy") != "healthy":
        should_send = True
        custom_msg = "✅ **Sync pulih.**\n\nBrain sudah aman lagi di GitHub.\nAku balik mode diem."
        state["last_status"] = "healthy"
        state["last_event_times"]["sync_failed"] = 0.0
        state["last_event_times"]["runtime_blocked"] = 0.0
        state["last_event_times"]["secret_guard_hit"] = 0.0
    else:
        log_event("Suppressed runtime_recovered (already healthy)")

elif event_type == "owner_review_needed":
    # Legacy event mapping, let's keep it but suppress if review_card is used
    log_event("Suppressing legacy owner_review_needed in favor of owner_review_card")

elif event_type == "remote_queue_processed":
    count = 1
    if message and "processed" in message.lower():
        try:
            count = int([s for s in message.split() if s.isdigit()][0])
        except Exception:
            pass
    should_send = True
    custom_msg = f"📥 **Remote queue selesai diproses.**\nAda {count} proposal baru siap ditinjau."

elif event_type == "manual_queue_card":
    is_new_or_changed = (capture_id != state.get("last_latest_capture_id"))
    time_elapsed = current_time - state["last_event_times"].get("manual_queue_card", 0.0)
    
    if is_new_or_changed or time_elapsed >= 21600:
        should_send = True
        state["last_event_times"]["manual_queue_card"] = current_time
        state["last_latest_capture_id"] = capture_id
        
        custom_msg = f"🟡 **Ada capture baru di Manual Sync Queue.**\n\n**Judul:**\n{message}\n\n**Intinya:**\n{extra}\n\nMau diapain?"
        
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "Proses ke canonical", "callback_data": f"manualqueue:canonicalize:{capture_id}"},
                    {"text": "Lihat detail", "callback_data": f"manualqueue:detail:{capture_id}"}
                ],
                [
                    {"text": "Tunda", "callback_data": f"manualqueue:defer:{capture_id}"},
                    {"text": "Arsipkan", "callback_data": f"manualqueue:archive:{capture_id}"}
                ]
            ]
        }
    else:
        log_event(f"Suppressed duplicate manual_queue_card (cooldown active: {int(21600 - time_elapsed)}s left)")

elif event_type == "owner_review_card":
    items_hash = hashlib.sha256((message or "").encode("utf-8")).hexdigest()
    time_elapsed = current_time - state["last_event_times"].get("owner_review_card", 0.0)
    is_new_or_changed = (items_hash != state.get("last_review_items_hash"))
    
    if is_new_or_changed or time_elapsed >= 43200:
        should_send = True
        state["last_event_times"]["owner_review_card"] = current_time
        state["last_review_items_hash"] = items_hash
        
        custom_msg = f"🟡 **Ada review pending.**\n\n{message}\n\nPilih mode aman:"
        
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "Lihat detail", "callback_data": "ownerreview:summary"},
                    {"text": "Defer verify-first", "callback_data": "ownerreview:defer_verify_first"}
                ],
                [
                    {"text": "Proses aman", "callback_data": "ownerreview:process_safe"},
                    {"text": "Tunda 12 jam", "callback_data": "ownerreview:snooze12h"}
                ]
            ]
        }
    else:
        log_event(f"Suppressed duplicate owner_review_card (cooldown active: {int(43200 - time_elapsed)}s left)")

else:
    sys.stderr.write(f"Unknown event type: {event_type}\n")
    sys.exit(1)

if should_send and custom_msg:
    if is_configured:
        log_event(f"Sending Telegram notification for type '{event_type}'")
        success = send_telegram(custom_msg, reply_markup)
        if success:
            log_event(f"Notification sent successfully: {event_type}")
            state["last_notification_time"] = current_time
        else:
            log_event(f"Failed to send Telegram notification: {event_type}")
    else:
        log_event(f"Log-only notification (Telegram unconfigured) for type '{event_type}': {custom_msg}")
else:
    log_event(f"Notification suppressed/logged for type '{event_type}'")

save_state()
sys.exit(0)
EOF
