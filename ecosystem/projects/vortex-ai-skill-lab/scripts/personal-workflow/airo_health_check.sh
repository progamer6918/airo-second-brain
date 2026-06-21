#!/usr/bin/env bash
set -Eeuo pipefail

cd "${AIRO_REPO_DIR:-$HOME/vortex-ai-skill-lab}"

echo "== git =="
git log --oneline -n 5
git status --short

echo
echo "== services =="
systemctl --user is-active --quiet openclaw-gateway.service
echo "OPENCLAW_ACTIVE_PASS"

systemctl --user is-active --quiet airo-full-auto-sheets-sync.timer
echo "SHEETS_TIMER_ACTIVE_PASS"

systemctl --user list-timers "*airo*" --no-pager || true

echo
echo "== OpenClaw env =="
systemctl --user cat openclaw-gateway.service \
  | grep -E 'AIRO_REPO_DIR|PYTHONPATH|ExecStart|PATH=' || true

echo
echo "== finance production regression =="
scripts/personal-workflow/airo_finance_prod_regression.sh

echo
echo "== recent sync service status =="
systemctl --user status airo-full-auto-sheets-sync.service --no-pager 2>/dev/null \
  | sed -n '1,80p' || true

echo
echo "PASS: AIRO health check passed."
