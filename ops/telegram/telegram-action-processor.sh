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

def send_telegram(text, reply_markup=None):
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

def get_safe_callback_target(full_id, action_prefix):
    SHORTID_SCRIPT = "./scripts/airo-manual-queue-shortid"
    if os.path.exists(SHORTID_SCRIPT):
        try:
            res = subprocess.run(
                ["python3", SHORTID_SCRIPT, "--effective", full_id, action_prefix],
                capture_output=True, text=True, timeout=5
            )
            val = res.stdout.strip()
            if val:
                return val
        except Exception as e:
            sys.stderr.write(f"Failed to get safe callback target: {e}\n")
    return full_id

def is_capture_archived(capture_id):
    import glob
    match = re.match(r"^(\d{4})(\d{2})(\d{2})-", capture_id)
    if match:
        date_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        guess_path = f"archive/manual-sync-queue/{date_str}/{capture_id}.md"
        if os.path.exists(guess_path):
            return True
            
    search_pattern = f"archive/manual-sync-queue/*/{capture_id}.md"
    matches = glob.glob(search_pattern)
    if matches:
        return True
    return False

def get_capture_details(full_id):
    filepath = "inbox/manual-sync-queue.md"
    if not os.path.exists(filepath):
        return None
        
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return None
        
    import re
    def title_to_id(title):
        title = title.strip()
        title = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\1\2\3", title)
        title = title.lower()
        title = title.replace("—", " ").replace(":", " ")
        title = re.sub(r"[^a-z0-9\s-]", "", title)
        title = re.sub(r"[\s-]+", "-", title)
        return title.strip("-")

    sections = re.split(r"\n(## \d{4}-\d{2}-\d{2}.*)", content)
    if len(sections) < 2:
        return None
        
    for i in range(1, len(sections), 2):
        title_line = sections[i]
        body = sections[i+1]
        title = title_line[3:].strip()
        cap_id = title_to_id(title)
        
        if cap_id == full_id:
            status = "pending"
            for line in body.splitlines():
                if line.lower().strip().startswith("status:"):
                    status = line.split(":", 1)[1].strip().lower()
                    break
            
            canonical_files = []
            in_target_files = False
            for line in body.splitlines():
                line_strip = line.strip()
                if "target canonical files:" in line_strip.lower():
                    in_target_files = True
                    continue
                if in_target_files:
                    if line_strip.startswith("*") or line_strip.startswith("-"):
                        match = re.search(r"`([^`]+)`", line_strip)
                        if match:
                            canonical_files.append(match.group(1))
                    elif line_strip == "" or line_strip.startswith("##"):
                        if not (line_strip.startswith("*") or line_strip.startswith("-")):
                            in_target_files = False
                            
            return {
                "id": cap_id,
                "status": status,
                "canonical_files": canonical_files
            }
    return None

def get_capture_summary_and_title(full_id):
    filepath = "inbox/manual-sync-queue.md"
    title = None
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            import re
            def title_to_id(title):
                title = title.strip()
                title = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\1\2\3", title)
                title = title.lower()
                title = title.replace("—", " ").replace(":", " ")
                title = re.sub(r"[^a-z0-9\s-]", "", title)
                title = re.sub(r"[\s-]+", "-", title)
                return title.strip("-")
            sections = re.split(r"\n(## \d{4}-\d{2}-\d{2}.*)", content)
            for i in range(1, len(sections), 2):
                title_line = sections[i]
                t = title_line[3:].strip()
                if title_to_id(t) == full_id:
                    title = t
                    break
        except Exception:
            pass
            
    # Fallback to archive search if title not found
    if not title:
        import glob
        match = re.match(r"^(\d{4})(\d{2})(\d{2})-", full_id)
        archive_path = None
        if match:
            date_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
            guess_path = f"archive/manual-sync-queue/{date_str}/{full_id}.md"
            if os.path.exists(guess_path):
                archive_path = guess_path
        if not archive_path:
            matches = glob.glob(f"archive/manual-sync-queue/*/{full_id}.md")
            if matches:
                archive_path = matches[0]
                
        if archive_path:
            try:
                with open(archive_path, "r", encoding="utf-8", errors="ignore") as f:
                    first_line = f.readline()
                    if first_line.startswith("## "):
                        title = first_line[3:].strip()
            except Exception:
                pass
            
    summary = ""
    try:
        res = subprocess.run(
            ["python3", "./scripts/airo-manual-queue-summarize", full_id],
            capture_output=True, text=True, timeout=5
        )
        summary = res.stdout.strip()
    except Exception:
        pass
    if not summary:
        summary = f"Capture ID: {full_id}"
    return title, summary

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
    original_target_id = action_data.get("target_id", "none")
    target_id = original_target_id
    callback_id = action_data.get("callback_id", "none")

    # Resolve short ID → full capture ID if needed
    SHORTID_SCRIPT = "./scripts/airo-manual-queue-shortid"
    if target_id and target_id.startswith("mq-") and os.path.exists(SHORTID_SCRIPT):
        try:
            res_resolve = subprocess.run(
                ["python3", SHORTID_SCRIPT, "--resolve", target_id],
                capture_output=True, text=True, timeout=5
            )
            resolved = res_resolve.stdout.strip()
            if resolved and resolved != target_id:
                print(f"Short ID resolved: {target_id} → {resolved}")
                target_id = resolved
        except Exception as e:
            sys.stderr.write(f"Short ID resolution failed: {e}\n")
    print(f"Processing action '{action}' for target '{target_id}'...")
    success = False
    msg_to_send = ""
    reply_markup_to_send = None

    # Resolve target check
    is_unresolved_mq = target_id and target_id.startswith("mq-")

    # manualqueue actions
    if is_unresolved_mq and action.startswith("manualqueue:"):
        success = True
        msg_to_send = "⚠️ Tombol ini sudah kedaluwarsa. Kirim/ambil card terbaru."
    elif action == "manualqueue:canonicalize":
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
            if "kedaluwarsa" in detail_content.lower():
                send_telegram(detail_content)
                msg_to_send = ""
            else:
                if len(detail_content) > 3000:
                    detail_content = detail_content[:3000] + "\n...(truncated)..."
                
                # 1. Send the detail message first
                detail_msg = f"📄 *Detail untuk Capture `{target_id}`:*\n\n```markdown\n{detail_content}\n```"
                send_telegram(detail_msg)
            
            # 2. Prepare follow-up keyboard
            is_archived = is_capture_archived(target_id)
            is_smoke_test = ("smoke" in target_id.lower()) or ("test" in target_id.lower())
            
            buttons = []
            if is_archived:
                if is_smoke_test:
                    target_archive = get_safe_callback_target(target_id, "manualqueue:archive:")
                    target_back = get_safe_callback_target(target_id, "manualqueue:back:")
                    buttons.append([
                        {"text": "Arsipkan smoke test", "callback_data": f"manualqueue:archive:{target_archive}"},
                        {"text": "Kembali", "callback_data": f"manualqueue:back:{target_back}"}
                    ])
                else:
                    target_back = get_safe_callback_target(target_id, "manualqueue:back:")
                    buttons.append([
                        {"text": "Kembali", "callback_data": f"manualqueue:back:{target_back}"}
                    ])
            else:
                target_canonicalize = get_safe_callback_target(target_id, "manualqueue:canonicalize:")
                target_defer = get_safe_callback_target(target_id, "manualqueue:defer:")
                target_archive = get_safe_callback_target(target_id, "manualqueue:archive:")
                target_back = get_safe_callback_target(target_id, "manualqueue:back:")
                
                info = get_capture_details(target_id)
                show_canonicalize = False
                if info:
                    status_pending = (info.get("status") == "pending")
                    files_exist = False
                    if info.get("canonical_files"):
                        files_exist = all(os.path.exists(f) for f in info["canonical_files"])
                    show_canonicalize = (status_pending and files_exist)
                
                row1 = []
                if show_canonicalize:
                    row1.append({"text": "Proses ke canonical", "callback_data": f"manualqueue:canonicalize:{target_canonicalize}"})
                row1.append({"text": "Tunda", "callback_data": f"manualqueue:defer:{target_defer}"})
                buttons.append(row1)
                
                row2 = [
                    {"text": "Arsipkan", "callback_data": f"manualqueue:archive:{target_archive}"},
                    {"text": "Kembali", "callback_data": f"manualqueue:back:{target_back}"}
                ]
                buttons.append(row2)
                
            reply_markup = {"inline_keyboard": buttons}
            # Send follow-up decision card
            send_telegram("Mau diapain dengan capture ini?", reply_markup=reply_markup)
            msg_to_send = "" # Bypass bottom send_telegram
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
            proc_stdout = res.stdout.strip()
            if "already archived" in proc_stdout.lower():
                msg_to_send = f"📥 *Capture `{target_id}` sudah diarsipkan sebelumnya (already archived).*"
            elif "kedaluwarsa" in proc_stdout.lower():
                msg_to_send = proc_stdout
            else:
                msg_to_send = f"📥 *Capture `{target_id}` diarsipkan sebagai obsolete.*"
        else:
            msg_to_send = f"❌ *Gagal mengarsipkan Capture:* `{target_id}`.\nDetail: {res.stderr.strip()}"
            
    elif action == "manualqueue:back":
        title, summary = get_capture_summary_and_title(target_id)
        if title:
            success = True
            is_archived = is_capture_archived(target_id)
            is_smoke_test = ("smoke" in target_id.lower()) or ("test" in target_id.lower())
            
            if is_archived:
                msg_to_send = f"📦 *Capture ini sudah diarsipkan.*\n\n**Judul:**\n{title}\n\n**Intinya:**\n{summary}"
                
                buttons = []
                if is_smoke_test:
                    target_archive = get_safe_callback_target(target_id, "manualqueue:archive:")
                    target_back = get_safe_callback_target(target_id, "manualqueue:back:")
                    buttons.append([
                        {"text": "Arsipkan smoke test", "callback_data": f"manualqueue:archive:{target_archive}"},
                        {"text": "Kembali", "callback_data": f"manualqueue:back:{target_back}"}
                    ])
                else:
                    target_back = get_safe_callback_target(target_id, "manualqueue:back:")
                    buttons.append([
                        {"text": "Kembali", "callback_data": f"manualqueue:back:{target_back}"}
                    ])
                reply_markup_to_send = {"inline_keyboard": buttons}
            else:
                msg_to_send = f"🟡 **Ada capture baru di Manual Sync Queue.**\n\n**Judul:**\n{title}\n\n**Intinya:**\n{summary}\n\nMau diapain?"
                
                target_canonicalize = get_safe_callback_target(target_id, "manualqueue:canonicalize:")
                target_detail = get_safe_callback_target(target_id, "manualqueue:detail:")
                target_defer = get_safe_callback_target(target_id, "manualqueue:defer:")
                target_archive = get_safe_callback_target(target_id, "manualqueue:archive:")
                
                reply_markup_to_send = {
                    "inline_keyboard": [
                        [
                            {"text": "Proses ke canonical", "callback_data": f"manualqueue:canonicalize:{target_canonicalize}"},
                            {"text": "Lihat detail", "callback_data": f"manualqueue:detail:{target_detail}"}
                        ],
                        [
                            {"text": "Tunda", "callback_data": f"manualqueue:defer:{target_defer}"},
                            {"text": "Arsipkan", "callback_data": f"manualqueue:archive:{target_archive}"}
                        ]
                    ]
                }
        else:
            msg_to_send = f"❌ *Gagal mengambil ringkasan untuk Capture:* `{target_id}`."
            
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
    if msg_to_send:
        send_telegram(msg_to_send, reply_markup=reply_markup_to_send)


sys.exit(0)
EOF
