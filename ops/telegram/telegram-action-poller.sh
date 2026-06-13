#!/usr/bin/env bash
exec python3 - "$@" << 'EOF'
import sys
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

ENV_FILE = "/home/egitaristorandas/.airo/telegram.env"
ACTIONS_DIR = "inbox/telegram-actions"

# 1. Read credentials safely
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

if not token or not chat_id:
    sys.stderr.write("Telegram credentials not configured. Skipping poller.\n")
    sys.exit(0)

# 2. Get updates
url = f"https://api.telegram.org/bot{token}/getUpdates"
try:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=10) as response:
        res_data = response.read().decode("utf-8")
        res_json = json.loads(res_data)
except Exception as e:
    sys.stderr.write(f"Telegram getUpdates failed: {e}\n")
    sys.exit(1)

if not res_json.get("ok", False):
    sys.stderr.write("Telegram API returned error.\n")
    sys.exit(1)

updates = res_json.get("result", [])
os.makedirs(ACTIONS_DIR, exist_ok=True)

# 3. Process callback queries
for update in updates:
    callback_query = update.get("callback_query")
    if not callback_query:
        continue
        
    sender_chat_id = str(callback_query.get("message", {}).get("chat", {}).get("id", ""))
    if sender_chat_id != chat_id:
        sys.stderr.write(f"Verification FAILED: Callback from unauthorized chat_id: {sender_chat_id}\n")
        continue
        
    callback_id = callback_query.get("id")
    data = callback_query.get("data", "")
    
    # Parse action data
    # Format e.g., manualqueue:canonicalize:20260613-correct-product-direction...
    parts = data.split(":")
    action = ""
    target_id = "none"
    if len(parts) >= 2:
        action = f"{parts[0]}:{parts[1]}"
        if len(parts) >= 3:
            target_id = parts[2]
    else:
        action = data
        
    action_file = f"{ACTIONS_DIR}/{callback_id}.json"
    if not os.path.exists(action_file):
        action_data = {
            "source": "telegram_callback",
            "chat_id_verified": True,
            "callback_id": callback_id,
            "action": action,
            "target_id": target_id,
            "received_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        try:
            with open(action_file, "w") as f:
                json.dump(action_data, f, indent=2)
            print(f"Staged Telegram action: {action_file}")
            
            # Answer callback query to stop loading spinner
            answer_url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
            answer_data = urllib.parse.urlencode({
                "callback_query_id": callback_id,
                "text": "Aksi disimpan di antrean Second Brain."
            }).encode("utf-8")
            urllib.request.urlopen(urllib.request.Request(answer_url, data=answer_data, method="POST"), timeout=10)
        except Exception as e:
            sys.stderr.write(f"Failed to stage action: {e}\n")

# Offset updates so we don't get them again
if updates:
    last_update_id = updates[-1]["update_id"]
    try:
        urllib.request.urlopen(f"{url}?offset={last_update_id + 1}", timeout=10)
    except Exception:
        pass

sys.exit(0)
EOF
