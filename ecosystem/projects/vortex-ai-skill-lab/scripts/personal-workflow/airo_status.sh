#!/usr/bin/env bash
set -Eeuo pipefail

cd "${AIRO_REPO_DIR:-$HOME/vortex-ai-skill-lab}"

echo "== git =="
git log --oneline -n 5
git status --short

echo
echo "== services =="
systemctl --user is-active openclaw-gateway.service
systemctl --user is-active airo-full-auto-sheets-sync.timer
systemctl --user list-timers "*airo*" --no-pager || true

echo
echo "== finance regression =="
scripts/personal-workflow/airo_finance_prod_regression.sh

echo
echo "PASS: AIRO status check passed."
