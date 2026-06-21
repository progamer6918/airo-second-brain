#!/usr/bin/env bash
set -euo pipefail

WORKER_URL="${WORKER_URL:-https://airo-finance-telegram-proxy.progamer6918.workers.dev}"
CHAT_ID="${CHAT_ID:-8482041086}"

post_case() {
  local id="$1"
  local text="$2"
  local expected="$3"

  echo
  echo "===== $id :: $text ====="

  response="$(
    curl -sS -X POST "$WORKER_URL" \
      -H "Content-Type: application/json" \
      --data "{\"update_id\":$id,\"message\":{\"message_id\":$id,\"from\":{\"id\":$CHAT_ID,\"is_bot\":false,\"first_name\":\"QA\"},\"chat\":{\"id\":$CHAT_ID,\"first_name\":\"QA\",\"type\":\"private\"},\"date\":1778690004,\"text\":\"$text QA_TEST\"}}"
  )"

  echo "$response"

  python3 - "$response" "$expected" <<'PY'
import json, sys

raw = sys.argv[1]
expected = sys.argv[2]

try:
    data = json.loads(raw)
except Exception:
    print("ASSERT_FAIL: response is not JSON")
    sys.exit(1)

written = data.get("written_tab") or data.get("planned_tab") or ""
status = data.get("routed_status", "")

if expected not in written:
    print(f"ASSERT_FAIL: expected tab contains {expected!r}, got {written!r}")
    sys.exit(1)

if status not in ("written", "fallback", ""):
    print(f"ASSERT_WARN: unusual routed_status={status!r}")

print("ASSERT_OK")
PY
}

BASE="$(date +%s)"

post_case "$((BASE+1))"  "bca beli makan 11000 hari ini"                         "Transactions"
post_case "$((BASE+2))"  "bca gaji masuk 2500000 hari ini"                       "Transactions"

post_case "$((BASE+3))"  "cash masuk 11000 hari ini"                             "Cash Ledger"
post_case "$((BASE+4))"  "cash beli kopi 5000 hari ini"                          "Cash Ledger"
post_case "$((BASE+5))"  "cash bensin masuk 30000 hari ini"                      "Cash Ledger"
post_case "$((BASE+6))"  "cash beli bensin 15000 hari ini"                       "Cash Ledger"

post_case "$((BASE+7))"  "tokopedia cc beli mouse 123000 hari ini"                "Credit Card"
post_case "$((BASE+8))"  "bayar tagihan tokopedia cc 123000 dari blu hari ini"    "Credit Card"

post_case "$((BASE+9))"  "bca bayar cicilan rumah 1543000 hari ini"              "Cicilan Rumah"

post_case "$((BASE+10))" "bca bayar hutang ke mamak 100000 hari ini"              "Hutang"
post_case "$((BASE+11))" "pinjam uang dari mamak 100000 hari ini"                 "Hutang"

post_case "$((BASE+12))" "aset emas 24k berat 0,5 gram"                          "Aset"
post_case "$((BASE+13))" "aset emas jual 0,25 gram hari ini"                     "Aset"
post_case "$((BASE+14))" "bca nabung aset 50000 hari ini"                        "Aset"

post_case "$((BASE+15))" "kayaknya kemarin bayar sesuatu"                        "Review Queue"

echo
echo "REGRESSION_SMOKE_DONE"
echo "Filter/delete QA rows later by raw_text contains: QA_TEST"
