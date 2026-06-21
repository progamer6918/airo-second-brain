#!/bin/bash
set -euo pipefail
TS="$(date +%Y%m%d_%H%M%S)"
OUT="/mnt/c/Ubuntu/home/egitaristorandas/vortex-ai-skill-lab/airo_finance_task9_readonly_preflight_${TS}.txt"

{
  echo "===== AIRO FINANCE TASK 9 READONLY PREFLIGHT ====="
  date -Is
  echo "MODE=READ_ONLY_NO_PATCH_NO_DEPLOY_NO_WORKBOOK_NO_GMAIL"
  echo

  ASB="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
  FIN="/home/egitaristorandas/vortex-ai-skill-lab"

  echo "===== REPO EXISTENCE ====="
  for D in "$ASB" "$FIN"; do
    if [ -d "$D/.git" ]; then
      echo "FOUND_GIT_REPO=$D"
    else
      echo "MISSING_OR_NOT_GIT=$D"
    fi
  done
  echo

  echo "===== ASB GIT STATE ====="
  if [ -d "$ASB/.git" ]; then
    cd "$ASB"
    git fetch origin main --prune
    git status --short --branch
    echo "HEAD=$(git rev-parse HEAD)"
    echo "ORIGIN_MAIN=$(git rev-parse origin/main 2>/dev/null || true)"
    git log -8 --oneline
  fi
  echo

  echo "===== AIRO FINANCE GIT STATE ====="
  if [ -d "$FIN/.git" ]; then
    cd "$FIN"
    git fetch origin main --prune
    git status --short --branch
    echo "HEAD=$(git rev-parse HEAD)"
    echo "ORIGIN_MAIN=$(git rev-parse origin/main 2>/dev/null || true)"
    git log -12 --oneline
  fi
  echo

  echo "===== ASB SYSTEM HEALTH ====="
  cd "$ASB"
  cat state/system-health.md 2>/dev/null || echo "MISSING state/system-health.md"
  echo

  echo "===== ASB AIRO FINANCE CURRENT STATE ====="
  cat projects/airo-finance/current-state.md 2>/dev/null || echo "MISSING projects/airo-finance/current-state.md"
  echo

  echo "===== ASB REVIEW FILES ====="
  for F in reviews/owner-review-queue-20260612.md reviews/owner-decision-batch-20260612.md; do
    echo "--- $F ---"
    cat "$F" 2>/dev/null || echo "MISSING $F"
    echo
  done

  echo "===== ASB LATEST VALIDATION FILES ====="
  find docs/validation -maxdepth 1 -type f 2>/dev/null | sort | tail -n 30
  echo

  echo "===== FINANCE CANONICAL DOCS ====="
  cd "$FIN"
  for F in \
    AIRO_MANIFEST.md \
    docs/AIRO_FINANCE_CURRENT_STATE.md \
    docs/AIRO_FINANCE_PRD_LIVING.md \
    docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
  do
    echo "--- $F ---"
    if [ -f "$F" ]; then
      sed -n "1,220p" "$F"
    else
      echo "MISSING $F"
    fi
    echo
  done

  echo "===== LATEST FINANCE RECORDS ====="
  find docs/airo-finance/records -type f 2>/dev/null | sort | tail -n 40 || true
  echo

  echo "===== TASK 9 / CC SETTLEMENT SEARCH ====="
  grep -RIn \
    --exclude-dir=.git \
    --exclude="*.zip" \
    --exclude="*.json" \
    --exclude="*.token" \
    --exclude="credentials*.json" \
    --exclude="token*.json" \
    -E "Task 9|cc sudah|cek tagihan pending cc|ledger-first|CC pending|Credit Card|Dashboard migration|Asset Ledger|Aset" \
    docs/AIRO_FINANCE_CURRENT_STATE.md docs/airo-finance/records 2>/dev/null | tail -n 240 || true
  echo

  echo "===== SOURCE FILE MARKERS ====="
  for F in \
    apps-script-live/AIRO_Finance_Multitab_Final_v1.js \
    apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js \
    scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs
  do
    echo "--- $F ---"
    if [ -f "$F" ]; then
      sha256sum "$F"
      grep -nE "cc sudah|cek tagihan pending cc|pending cc|markCreditCardPocket|appendCreditCardPurchase|CreditCard|writeAsset|Aset|ledger-first" "$F" | head -n 120 || true
    else
      echo "MISSING $F"
    fi
  done

  echo "===== CLASP DEPLOYMENTS IF AVAILABLE ====="
  if command -v clasp >/dev/null 2>&1; then
    clasp deployments 2>&1 || true
  else
    echo "CLASP_NOT_FOUND"
  fi

  echo
  echo "===== PREFLIGHT END ====="
} 2>&1 | tee "$OUT"

if command -v clip.exe >/dev/null 2>&1; then
  clip.exe < "$OUT"
  echo "COPIED_TO_CLIPBOARD=$OUT"
else
  echo "CLIPBOARD_COPY=SKIPPED"
  echo "OUTPUT_PATH=$OUT"
fi
