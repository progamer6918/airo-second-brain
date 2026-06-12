#!/usr/bin/env bash
exec python3 - "$@" << 'EOF'
import sys
import os
import json
import time
from datetime import datetime
import urllib.request
import urllib.parse

# 1. Parse arguments manually
is_test = False
event_type = None
message = None

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

# Check if actually configured (not empty, placeholder, or token/chat_id literal placeholder)
is_configured = False
if token and chat_id:
    # check for placeholder values
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
    "telegram_status": "log_only_unconfigured"
}

if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            loaded = json.load(f)
            for k, v in loaded.items():
                state[k] = v
    except Exception:
        pass

# Update state status dynamically
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

def send_telegram(text):
    if not is_configured:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            return res_json.get("ok", False)
    except Exception as e:
        sys.stderr.write("Telegram API Request failed (connection or credential error).\n")
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

if not message:
    message = f"Event: {event_type}"

current_time = time.time()
should_send = False

if event_type == "runtime_online":
    # Startup online cooldown: 30 minutes (1800 seconds)
    time_elapsed = current_time - state.get("last_startup_time", 0)
    if time_elapsed >= 1800:
        should_send = True
        state["last_startup_time"] = current_time
    else:
        log_event(f"Suppressed duplicate runtime_online event (cooldown active: {int(1800 - time_elapsed)}s left)")

elif event_type == "sync_pushed":
    # Always notify when changes are pushed
    should_send = True

elif event_type == "runtime_degraded":
    # Same warning cooldown: 60 minutes (3600 seconds)
    is_same = (message == state.get("last_error_msg", "") and state.get("last_status", "") in ("degraded", "blocked"))
    time_elapsed = current_time - state.get("last_error_time", 0)
    if not is_same or time_elapsed >= 3600:
        should_send = True
        state["last_error_time"] = current_time
        state["last_error_msg"] = message
        state["last_status"] = "degraded"
    else:
        log_event(f"Suppressed duplicate runtime_degraded event (cooldown active: {int(3600 - time_elapsed)}s left)")

elif event_type == "runtime_recovered":
    # Notify on recovery immediately if we were degraded or blocked before
    should_send = True
    state["last_status"] = "healthy"

elif event_type == "owner_review_needed":
    # Cooldown: 360 minutes (21600 seconds)
    # Check queue count from file
    review_count = 0
    review_file = "reviews/owner-review-queue-20260612.md"
    if os.path.exists(review_file):
        try:
            with open(review_file, "r") as f:
                review_count = sum(1 for line in f if "## Review Item" in line)
        except Exception:
            pass
            
    if review_count > 0:
        time_elapsed = current_time - state.get("last_review_time", 0)
        if review_count != state.get("last_review_count", 0) or time_elapsed >= 21600:
            should_send = True
            state["last_review_time"] = current_time
            state["last_review_count"] = review_count
        else:
            log_event(f"Suppressed owner_review_needed event (count unchanged or cooldown active: {int(21600 - time_elapsed)}s left)")
    else:
        log_event("Suppressed owner_review_needed (no review items pending)")

elif event_type == "remote_queue_processed":
    # Send immediately
    should_send = True

else:
    sys.stderr.write(f"Unknown event type: {event_type}\n")
    sys.exit(1)

if should_send:
    if is_configured:
        log_event(f"Sending Telegram notification for type '{event_type}'")
        success = send_telegram(message)
        if success:
            log_event(f"Notification sent successfully: {event_type}")
            state["last_notification_time"] = current_time
        else:
            log_event(f"Failed to send Telegram notification: {event_type}")
    else:
        log_event(f"Log-only notification (Telegram unconfigured) for type '{event_type}': {message}")
else:
    log_event(f"Notification suppressed for type '{event_type}'")

save_state()
sys.exit(0)
EOF
