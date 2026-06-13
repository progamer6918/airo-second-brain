#!/usr/bin/env bash
exec python3 - "$@" << 'EOF'
import sys
import os
import json
import time
import re
import subprocess
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
    sys.stderr.write("Telegram credentials not configured. Skipping processor.\n")
    sys.exit(0)

def send_telegram(text):
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
        sys.stderr.write(f"Telegram API sendMessage failed: {e}\n")
        return False

def defer_verify_first_items():
    review_file = "reviews/owner-review-queue-20260612.md"
    if not os.path.exists(review_file):
        return "Tidak ada review file."
    
    with open(review_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "status: processed" in content:
        return "Review queue sudah diproses."
        
    sections = re.split(r"\n(## Review Item \d+:.*)", content)
    header = sections[0]
    changed = False
    updated_sections = []
    
    for i in range(1, len(sections), 2):
        title_line = sections[i]
        body = sections[i+1]
        
        if "Recommended owner action:\n- VERIFY_FIRST" in body or "Recommended owner action: VERIFY_FIRST" in body:
            new_title = title_line.replace("## Review Item", "## Processed Review Item")
            new_body = body.replace("- [ ] DEFER", "- [x] DEFER")
            new_body += "\nDecision: DEFER (auto-deferred via Earesmes action)\n"
            updated_sections.append(new_title)
            updated_sections.append(new_body)
            changed = True
        else:
            updated_sections.append(title_line)
            updated_sections.append(body)
            
    if changed:
        new_content = header
        for i in range(0, len(updated_sections), 2):
            new_content += "\n" + updated_sections[i] + updated_sections[i+1]
            
        if "## Review Item" not in new_content:
            new_content = new_content.replace("status: pending", "status: processed")
            new_content = new_content.replace("(PENDING)", "(PROCESSED)")
            
        with open(review_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        return "Item dengan rekomendasi VERIFY_FIRST telah ditangguhkan (DEFER)."
    else:
        return "Tidak ada item pending dengan rekomendasi VERIFY_FIRST."

def process_safe_items():
    review_file = "reviews/owner-review-queue-20260612.md"
    if not os.path.exists(review_file):
        return "Tidak ada review file."
        
    with open(review_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "status: processed" in content:
        return "Review queue sudah diproses."
        
    sections = re.split(r"\n(## Review Item \d+:.*)", content)
    header = sections[0]
    changed = False
    updated_sections = []
    
    for i in range(1, len(sections), 2):
        title_line = sections[i]
        body = sections[i+1]
        
        safe_default = "DEFER"
        new_title = title_line.replace("## Review Item", "## Processed Review Item")
        new_body = body.replace(f"- [ ] {safe_default}", f"- [x] {safe_default}")
        new_body += f"\nDecision: {safe_default} (resolved via Earesmes safe processing)\n"
        updated_sections.append(new_title)
        updated_sections.append(new_body)
        changed = True
        
    if changed:
        new_content = header
        for i in range(0, len(updated_sections), 2):
            new_content += "\n" + updated_sections[i] + updated_sections[i+1]
            
        new_content = new_content.replace("status: pending", "status: processed")
        new_content = new_content.replace("(PENDING)", "(PROCESSED)")
        
        with open(review_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        return "Semua pending review item telah diproses secara aman menggunakan safe default (DEFER)."
    else:
        return "Tidak ada pending review item yang ditemukan."

def get_ownerreview_summary():
    review_file = "reviews/owner-review-queue-20260612.md"
    if not os.path.exists(review_file):
        return "Tidak ada review file."
        
    with open(review_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    sections = re.split(r"\n(## Review Item \d+:.*)", content)
    if len(sections) < 2:
        return "Tidak ada review item pending."
        
    summary_text = ""
    item_num = 1
    for i in range(1, len(sections), 2):
        title_line = sections[i]
        body = sections[i+1]
        
        title = title_line.replace("## Review Item", "").strip()
        title = re.sub(r"^\d+:\s*", "", title)
        
        rec_match = re.search(r"Recommended owner action:\s*\n-\s*(\w+)", body)
        rec_action = rec_match.group(1) if rec_match else "unknown"
        
        summary_text += f"{item_num}. {title} — {rec_action.lower()}\n"
        item_num += 1
        
    if not summary_text:
        return "Tidak ada review item pending."
    return summary_text

def snooze_review_notifications():
    state_file = "ops/notifications/notification-state.json"
    if not os.path.exists(state_file):
        return "File status notifikasi tidak ditemukan."
    try:
        with open(state_file, "r") as f:
            state = json.load(f)
    except Exception:
        state = {}
        
    state.setdefault("last_event_times", {})
    state["last_event_times"]["owner_review_needed"] = time.time()
    
    try:
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
        return "Notifikasi owner review ditunda (snooze) selama 12 jam."
    except Exception as e:
        return f"Gagal menyimpan status snooze: {e}"

# 2. Process all pending action files
if not os.path.exists(ACTIONS_DIR):
    sys.exit(0)

action_files = [f for f in os.listdir(ACTIONS_DIR) if f.endswith(".json")]
if not action_files:
    sys.exit(0)

print(f"Found {len(action_files)} action files in {ACTIONS_DIR}.")

for fname in action_files:
    fpath = os.path.join(ACTIONS_DIR, fname)
    try:
        with open(fpath, "r") as f:
            action_data = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Failed to read action file {fpath}: {e}\n")
        continue
        
    if action_data.get("status") != "pending":
        continue
        
    action_data["status"] = "processing"
    with open(fpath, "w") as f:
        json.dump(action_data, f, indent=2)
        
    action = action_data.get("action", "")
    target_id = action_data.get("target_id", "none")
    callback_id = action_data.get("callback_id", "none")
    
    print(f"Processing action '{action}' for target '{target_id}'...")
    success = False
    msg_to_send = ""
    
    # manualqueue actions
    if action == "manualqueue:canonicalize":
        res = subprocess.run(
            ["python3", "./scripts/airo-manual-queue-process", "--capture-id", target_id, "--action", "canonicalize"],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            # Compact the queue
            subprocess.run(["python3", "./scripts/airo-manual-queue-compact"])
            success = True
            msg_to_send = f"✅ *Manual Queue Canonicalized:*\nCapture ID: `{target_id}` berhasil dipromosikan ke dokumen kanonikal, diarsipkan, dan antrean telah di-compact."
        else:
            msg_to_send = f"❌ *Canonicalization Gagal:*\nCapture ID: `{target_id}` tidak dapat dipromosikan.\nDetail: {res.stderr.strip()}"
            
    elif action == "manualqueue:detail":
        res = subprocess.run(
            ["python3", "./scripts/airo-manual-queue-process", "--capture-id", target_id, "--action", "detail"],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            success = True
            detail_content = res.stdout.strip()
            if len(detail_content) > 3000:
                detail_content = detail_content[:3000] + "\n...(truncated)..."
            msg_to_send = f"📄 *Detail untuk Capture `{target_id}`:*\n\n```markdown\n{detail_content}\n```"
        else:
            msg_to_send = f"❌ *Gagal mengambil detail Capture:* `{target_id}`.\nDetail: {res.stderr.strip()}"
            
    elif action == "manualqueue:defer":
        res = subprocess.run(
            ["python3", "./scripts/airo-manual-queue-process", "--capture-id", target_id, "--action", "defer"],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            subprocess.run(["python3", "./scripts/airo-manual-queue-compact"])
            success = True
            msg_to_send = f"📥 *Capture `{target_id}` ditangguhkan (DEFER).* Block dipindahkan ke `inbox/deferred/`."
        else:
            msg_to_send = f"❌ *Gagal menangguhkan Capture:* `{target_id}`.\nDetail: {res.stderr.strip()}"
            
    elif action == "manualqueue:archive":
        res = subprocess.run(
            ["python3", "./scripts/airo-manual-queue-process", "--capture-id", target_id, "--action", "archive-obsolete"],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            subprocess.run(["python3", "./scripts/airo-manual-queue-compact"])
            success = True
            msg_to_send = f"📥 *Capture `{target_id}` diarsipkan sebagai obsolete.*"
        else:
            msg_to_send = f"❌ *Gagal mengarsipkan Capture:* `{target_id}`.\nDetail: {res.stderr.strip()}"
            
    # ownerreview actions
    elif action == "ownerreview:summary":
        summary_list = get_ownerreview_summary()
        success = True
        msg_to_send = f"🟡 *Daftar review pending:*\n\n{summary_list}"
        
    elif action == "ownerreview:defer_verify_first":
        result_msg = defer_verify_first_items()
        success = True
        msg_to_send = f"✅ *Owner Review Action:*\n{result_msg}"
        
    elif action == "ownerreview:process_safe":
        result_msg = process_safe_items()
        success = True
        msg_to_send = f"✅ *Owner Review Action:*\n{result_msg}"
        
    elif action == "ownerreview:snooze12h":
        result_msg = snooze_review_notifications()
        success = True
        msg_to_send = f"💤 *Owner Review Action:*\n{result_msg}"
        
    else:
        msg_to_send = f"⚠️ *Aksi tidak dikenal:* `{action}`."
        
    # Update action file status
    action_data["status"] = "processed" if success else "failed"
    action_data["processed_at"] = datetime.now().isoformat()
    action_data["result"] = msg_to_send
    
    with open(fpath, "w") as f:
        json.dump(action_data, f, indent=2)
        
    # Send feedback telegram
    send_telegram(msg_to_send)

sys.exit(0)
EOF
