#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${AIRO_REPO_DIR:-$HOME/vortex-ai-skill-lab}"
cd "$REPO_DIR"

echo "== AIRO v1.3 next-chat bootstrap =="
pwd
git branch --show-current
git fetch origin main --tags
git pull --ff-only origin main

echo
echo "== recent commits =="
git log --oneline -n 15

echo
echo "== git status =="
git status --short

echo
echo "== core local route: ambiguous finance must go to Review Queue =="
python3 scripts/personal-workflow/airo_intent_router.py "kayaknya bayar sesuatu kemarin"

echo
echo "== mapper expected output =="
python3 scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py "kayaknya bayar sesuatu kemarin" --confidence 0.30 --json

echo
echo "== cash route expected output =="
python3 scripts/personal-workflow/airo_intent_router.py "hari ini cash kepake beli makan 20rb"

echo
echo "== status CLI =="
python3 scripts/personal-workflow/airo_finance_sheet_v12_status.py --text

echo
echo "== v1.2/v1.3 regression =="
python3 scripts/personal-workflow/airo_finance_sheet_v12_regression.py

echo
echo "== AIRO health =="
scripts/personal-workflow/airo_status.sh

echo
echo "== OpenClaw recent logs =="
journalctl --user -u openclaw-gateway.service --since "30 minutes ago" --no-pager -n 220 || true

echo
echo "== next action =="
cat <<'TXT'
Read docs/personal-workflow/handoff/AIRO_V13_TELEGRAM_TO_SHEETS_CARRYOVER_PROMPT.md first.

Current target:
Telegram chat -> AIRO finance route -> local persistence/queue -> full-auto Google Sheet sync -> correct tab in 💰 Airo Personal Finance.

Already proven:
- local intent router routes ambiguous finance to 🧾 Review Queue
- local mapper routes ambiguous finance to 🧾 Review Queue
- Telegram no longer answers generic chat for "kayaknya bayar sesuatu kemarin"
- v1.3 write path exists

Not yet proven:
- actual Review Queue row persisted from Telegram
- actual Google Sheet row write after Telegram smoke

Do not send repeated Telegram smoke. Patch persistence/write-candidate generation first if TOTAL_WRITE_CANDIDATES remains 0.
TXT
