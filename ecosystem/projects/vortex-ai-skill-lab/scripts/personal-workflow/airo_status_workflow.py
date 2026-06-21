#!/usr/bin/env python3
import json
import subprocess

cmd = ["bash", "scripts/personal-workflow/airo_status.sh"]
p = subprocess.run(cmd, text=True, capture_output=True)

ok = p.returncode == 0
text = (p.stdout + p.stderr).strip()

if ok:
    message = "AIRO status PASS: OpenClaw aktif, timer aktif, DB canonical valid, Sheets dry-run idempotent."
else:
    message = "AIRO status CHECK: ada komponen yang perlu dicek. Jalankan scripts/personal-workflow/airo_status.sh."

print(json.dumps({
    "ok": ok,
    "intent": "airo_status",
    "action": "status_checked",
    "message": message,
    "status_output_tail": "\n".join([line for line in text.splitlines() if "PASS" in line or "CHECK" in line][-12:]),
}, ensure_ascii=False))
