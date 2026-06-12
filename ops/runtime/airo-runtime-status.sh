#!/usr/bin/env bash

SHOW_HELP=false
JSON_MODE=false

for arg in "$@"; do
  case $arg in
    --help)
      SHOW_HELP=true
      ;;
    --json)
      JSON_MODE=true
      ;;
  esac
done

if [ "$SHOW_HELP" = true ]; then
  if [ "$JSON_MODE" = true ]; then
    echo '{"help": "Usage: airo-runtime-status.sh [--help] [--json]"}'
  else
    echo "Usage: airo-runtime-status.sh [--help] [--json]"
  fi
  exit 0
fi

# Fetch states
SB_STATUS="unknown"
if [ -f state/system-health.md ]; then
  if grep -q "system_status: healthy" state/system-health.md; then SB_STATUS="healthy"; fi
  if grep -q "system_status: degraded" state/system-health.md; then SB_STATUS="degraded"; fi
  if grep -q "system_status: blocked" state/system-health.md; then SB_STATUS="blocked"; fi
fi

SCHEDULER_STATUS="unknown"
if command -v powershell.exe >/dev/null 2>&1; then
  # Simple check if task exists via powershell - requires windows environment access
  # To avoid hanging or errors in pure WSL, we assume active if the powershell command works or 'unknown'
  SCHEDULER_STATUS="active_or_unverified"
fi

LAST_RUN="never"
if [ -f state/last-runtime-run.txt ]; then
  LAST_RUN=$(cat state/last-runtime-run.txt)
fi

LAST_SYNC="never"
if grep -q "Git push completed successfully" logs/sync/sync.log 2>/dev/null; then
  LAST_SYNC=$(grep "Git push completed successfully" logs/sync/sync.log | tail -n 1 | awk '{print $1}' | tr -d '[]')
fi

LAST_Q="never"
if grep -q "Processed " logs/runtime.log 2>/dev/null; then
  LAST_Q=$(grep "Running remote queue processor" logs/runtime.log | tail -n 1 | awk '{print $1}' | tr -d '[]')
fi

TELEGRAM_STATUS="log_only_unconfigured"

AIRO_FINANCE="dirty_from_known_pre_existing_work"

READY="yes"
if [ "$SB_STATUS" = "degraded" ]; then READY="degraded"; fi
if [ "$SB_STATUS" = "blocked" ]; then READY="blocked"; fi

if [ "$JSON_MODE" = true ]; then
  cat <<EOF
{
  "second_brain_status": "$SB_STATUS",
  "scheduler_status": "$SCHEDULER_STATUS",
  "last_runtime_run": "$LAST_RUN",
  "last_successful_sync": "$LAST_SYNC",
  "last_queue_process": "$LAST_Q",
  "telegram_status": "$TELEGRAM_STATUS",
  "airo_finance_known_dirty_exception": true,
  "ready": "$READY"
}
EOF
else
  echo "Second Brain status: $SB_STATUS"
  echo "Scheduler status: $SCHEDULER_STATUS"
  echo "Last runtime run: $LAST_RUN"
  echo "Last successful sync: $LAST_SYNC"
  echo "Last queue process: $LAST_Q"
  echo "Telegram status: $TELEGRAM_STATUS"
  echo "AIRO Finance known dirty exception: $AIRO_FINANCE"
  echo "Ready: $READY"
fi
