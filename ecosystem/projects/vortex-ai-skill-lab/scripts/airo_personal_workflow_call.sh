#!/usr/bin/env bash
set -euo pipefail

# AIRO_STATUS_COMMAND_V1
_RAW_TEXT_FOR_STATUS="${*:-}"
_RAW_TEXT_STATUS_LC="$(printf '%s' "$_RAW_TEXT_FOR_STATUS" | tr '[:upper:]' '[:lower:]' | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
case "$_RAW_TEXT_STATUS_LC" in
  "status airo"|"airo status"|"cek status airo"|"status airos"|"cek airosync"|"airosync status"|"cek sync airo")
    exec python3 scripts/personal-workflow/airo_status_workflow.py
    ;;
esac


MODE="${AIRO_WORKFLOW_MODE:-real}"
TEXT="${*:-}"

if [ -z "$TEXT" ]; then
  echo '{"ok":false,"error":"empty_input","message":"No text provided"}'
  exit 1
fi

export AIRO_DB_QUIET=1

if [ "$MODE" = "dry-run" ] && [ -z "${AIRO_DB_PATH:-}" ]; then
  TMP_DIR="$(mktemp -d)"
  export AIRO_DB_PATH="$TMP_DIR/test_gateway.sqlite3"
fi

python3 -m airo_personal_workflow.gateway "$TEXT"
