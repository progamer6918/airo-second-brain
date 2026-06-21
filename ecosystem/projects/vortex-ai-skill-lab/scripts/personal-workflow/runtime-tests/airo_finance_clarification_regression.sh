#!/usr/bin/env bash
set -euo pipefail
DEPLOYMENT_ID="${1:-AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA}"
URL="https://script.google.com/macros/s/${DEPLOYMENT_ID}/exec"
STAMP="$(date +%Y%m%d_%H%M%S)"
post_msg() {
  local chat_id="$1"
  local text="$2"
  curl -sS -L -H 'Content-Type: application/json' -d "{\"message\":{\"chat\":{\"id\":${chat_id},\"type\":\"private\"},\"text\":\"${text}\"}}" "$URL"
}
echo "TASK=airo_finance_clarification_regression_all"
echo "DEPLOYMENT_ID=$DEPLOYMENT_ID"
CC_CHAT="-181$(date +%s)1"
CC_R1="$(post_msg "$CC_CHAT" "cc 50001 regression_cc_${STAMP}")"
sleep 2
CC_R2="$(post_msg "$CC_CHAT" "D")"
echo "CC_R1=$CC_R1"
echo "CC_R2=$CC_R2"
DEBT_CHAT="-181$(date +%s)2"
DEBT_R1="$(post_msg "$DEBT_CHAT" "hutang 50001 regression_debt_${STAMP}")"
sleep 2
DEBT_R2="$(post_msg "$DEBT_CHAT" "D")"
echo "DEBT_R1=$DEBT_R1"
echo "DEBT_R2=$DEBT_R2"
GOLD_CHAT="-181$(date +%s)3"
GOLD_R1="$(post_msg "$GOLD_CHAT" "emas 50001 regression_gold_${STAMP}")"
sleep 2
GOLD_R2="$(post_msg "$GOLD_CHAT" "D")"
echo "GOLD_R1=$GOLD_R1"
echo "GOLD_R2=$GOLD_R2"
echo "$CC_R1" | grep -q '"clarification_type":"cc_ambiguous"'
echo "$CC_R2" | grep -Eq '"cancelled":true|"status":"ignored"|"skipped":true'
echo "$DEBT_R1" | grep -q '"clarification_type":"debt_ambiguous"'
echo "$DEBT_R2" | grep -Eq '"cancelled":true|"status":"ignored"|"skipped":true'
echo "$GOLD_R1" | grep -q '"clarification_type":"asset_gold_ambiguous"'
echo "$GOLD_R2" | grep -q '"status":"ignored"'
echo "RESULT_CC=PASS"
echo "RESULT_DEBT=PASS"
echo "RESULT_ASSET_GOLD=PASS"

MISSING_CHAT="-180$(date +%s)4"
SPRINT0A_MISSING_R1="$(post_msg "$MISSING_CHAT" "beli bensin sprint0a_missing_${STAMP}")"
echo "SPRINT0A_MISSING_R1=$SPRINT0A_MISSING_R1"
echo "$SPRINT0A_MISSING_R1" | grep -Eq '"clarification_requested":true' && echo "RESULT_SPRINT0A_MISSING=PASS" || { echo "RESULT_SPRINT0A_MISSING=FAIL"; exit 1; }

CATEGORY_CHAT="-180$(date +%s)5"
SPRINT0A_CATEGORY_R1="$(post_msg "$CATEGORY_CHAT" "50001 sprint0a_category_${STAMP}")"
sleep 2
SPRINT0A_CATEGORY_R2="$(post_msg "$CATEGORY_CHAT" "makan")"
echo "SPRINT0A_CATEGORY_R1=$SPRINT0A_CATEGORY_R1"
echo "SPRINT0A_CATEGORY_R2=$SPRINT0A_CATEGORY_R2"
echo "$SPRINT0A_CATEGORY_R1" | grep -Eq '"clarification_requested":true|"skipped":true|"reason":"non_finance_or_too_unclear"' && echo "RESULT_SPRINT0A_CATEGORY_GUARD=PASS" || { echo "RESULT_SPRINT0A_CATEGORY_GUARD=FAIL"; exit 1; }

NONFIN_CHAT="-180$(date +%s)6"
SPRINT0A_NONFIN_R1="$(post_msg "$NONFIN_CHAT" "halo apa kabar sprint0a_nonfinance_${STAMP}")"
echo "SPRINT0A_NONFIN_R1=$SPRINT0A_NONFIN_R1"
echo "$SPRINT0A_NONFIN_R1" | grep -Eq '"skipped":true|"reason":"non_finance_or_too_unclear"' && echo "RESULT_SPRINT0A_NONFINANCE=PASS" || { echo "RESULT_SPRINT0A_NONFINANCE=FAIL"; exit 1; }


TRANSFER_CHAT="-182$(date +%s)7"
SPRINT0A_TRANSFER_R1="$(post_msg "$TRANSFER_CHAT" "transfer 50001 sprint0a_transfer_${STAMP}")"
echo "SPRINT0A_TRANSFER_R1=$SPRINT0A_TRANSFER_R1"
echo "$SPRINT0A_TRANSFER_R1" | grep -Eq '"clarification_requested":true' && echo "RESULT_SPRINT0A_TRANSFER=PASS" || { echo "RESULT_SPRINT0A_TRANSFER=FAIL"; exit 1; }

DIRECTION_CHAT="-182$(date +%s)8"
SPRINT0A_DIRECTION_R1="$(post_msg "$DIRECTION_CHAT" "bca blu 50001 sprint0a_direction_${STAMP}")"
echo "SPRINT0A_DIRECTION_R1=$SPRINT0A_DIRECTION_R1"
echo "$SPRINT0A_DIRECTION_R1" | grep -Eq '"clarification_requested":true' && echo "RESULT_SPRINT0A_DIRECTION=PASS" || { echo "RESULT_SPRINT0A_DIRECTION=FAIL"; exit 1; }

CASH_CHAT="-182$(date +%s)9"
SPRINT0A_CASH_R1="$(post_msg "$CASH_CHAT" "cash 50001 sprint0a_cash_${STAMP}")"
echo "SPRINT0A_CASH_R1=$SPRINT0A_CASH_R1"
echo "$SPRINT0A_CASH_R1" | grep -Eq '"clarification_requested":true' && echo "RESULT_SPRINT0A_CASH=PASS" || { echo "RESULT_SPRINT0A_CASH=FAIL"; exit 1; }

ACCOUNT_CHAT="-182$(date +%s)10"
SPRINT0A_ACCOUNT_R1="$(post_msg "$ACCOUNT_CHAT" "makan 50001 sprint0a_account_${STAMP}")"
echo "SPRINT0A_ACCOUNT_R1=$SPRINT0A_ACCOUNT_R1"
echo "$SPRINT0A_ACCOUNT_R1" | grep -Eq '"clarification_requested":true' && echo "RESULT_SPRINT0A_ACCOUNT=PASS" || { echo "RESULT_SPRINT0A_ACCOUNT=FAIL"; exit 1; }


AMOUNTBUG_CHAT="-183$(date +%s)11"
SPRINT0A_AMOUNT_BUG_R1="$(post_msg "$AMOUNTBUG_CHAT" "https://docs.google.com/spreadsheets/d/abc/edit#gid=791296096 chat transcript sprint0a_amountbug_${STAMP}")"
echo "SPRINT0A_AMOUNT_BUG_R1=$SPRINT0A_AMOUNT_BUG_R1"
echo "$SPRINT0A_AMOUNT_BUG_R1" | grep -Eq '"skipped":true|"reason":"non_finance_or_too_unclear"' && echo "RESULT_SPRINT0A_AMOUNT_BUG=PASS" || { echo "RESULT_SPRINT0A_AMOUNT_BUG=FAIL"; exit 1; }


FALLBACK_CHAT="-184$(date +%s)12"
SPRINT0A_FALLBACK_R1="$(post_msg "$FALLBACK_CHAT" "beli bensin sprint0a_fallback_${STAMP}")"
sleep 1
SPRINT0A_FALLBACK_R2="$(post_msg "$FALLBACK_CHAT" "salah")"
sleep 1
SPRINT0A_FALLBACK_R3="$(post_msg "$FALLBACK_CHAT" "tetap salah")"
echo "SPRINT0A_FALLBACK_R1=$SPRINT0A_FALLBACK_R1"
echo "SPRINT0A_FALLBACK_R2=$SPRINT0A_FALLBACK_R2"
echo "SPRINT0A_FALLBACK_R3=$SPRINT0A_FALLBACK_R3"
echo "$SPRINT0A_FALLBACK_R3" | grep -Eq '"fallback_to_review":true|"status":"review_queue_fallback_after_clarification_failed"' && echo "RESULT_SPRINT0A_FALLBACK_REVIEW=PASS" || { echo "RESULT_SPRINT0A_FALLBACK_REVIEW=FAIL"; exit 1; }

echo "FINAL_RESULT=PASS"
