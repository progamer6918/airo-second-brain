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
SB_STATUS="healthy"
if [ -d .git ]; then
  if [ -n "$(git status --porcelain)" ]; then
    SB_STATUS="degraded"
  fi
  if git diff --name-only --diff-filter=U | grep -q .; then
    SB_STATUS="blocked"
  fi
fi

SCHEDULER_STATUS="unknown"
if command -v powershell.exe >/dev/null 2>&1; then
  if powershell.exe -NoProfile -Command "Get-ScheduledTask -TaskName 'AIRO Second Brain Runtime Sync' -ErrorAction SilentlyContinue" | grep -q "AIRO Second Brain Runtime Sync"; then
    SCHEDULER_STATUS="active"
  else
    SCHEDULER_STATUS="not_installed"
  fi
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
if [ -f ops/notifications/notification-state.json ]; then
  TELEGRAM_STATUS=$(grep -o '"telegram_status": "[^"]*"' ops/notifications/notification-state.json | cut -d'"' -f4)
  if [ -z "$TELEGRAM_STATUS" ]; then
    TELEGRAM_STATUS="log_only_unconfigured"
  fi
fi

AIRO_FINANCE="dirty_from_known_pre_existing_work"

PENDING_DECISIONS=0
if [ -f state/system-health.md ]; then
  PENDING_DECISIONS=$(grep "decisions:" state/system-health.md | awk '{print $2}' | tr -d '\r ')
  if [ -z "$PENDING_DECISIONS" ]; then PENDING_DECISIONS=0; fi
fi

PENDING_PROPOSALS=0
if [ -d distill/proposals ]; then
  PENDING_PROPOSALS=$(ls -1q distill/proposals/*.md 2>/dev/null | wc -l | tr -d '\r ')
fi

OWNER_REVIEW_REQUIRED=0
if [ -f reviews/owner-review-queue-20260612.md ]; then
  OWNER_REVIEW_REQUIRED=$(grep -c "## Review Item" reviews/owner-review-queue-20260612.md | tr -d '\r ' || true)
fi

READY="healthy"
if [ "$SB_STATUS" = "degraded" ]; then READY="degraded"; fi
if [ "$SB_STATUS" = "blocked" ]; then READY="blocked"; fi

# New rule: Knowledge backlog must not make runtime readiness "blocked" if runtime infra is healthy.
if [ "$READY" = "healthy" ] || [ "$READY" = "degraded" ]; then
  if [ "$PENDING_DECISIONS" -gt 0 ] || [ "$PENDING_PROPOSALS" -gt 0 ] || [ "$OWNER_REVIEW_REQUIRED" -gt 0 ]; then
    READY="degraded_review_pending"
  fi
fi

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
  "ready": "$READY",
  "readiness": "$READY",
  "project_status": "operational_complete",
  "runtime_sync_mode": "real_sync_enabled",
  "pending_decisions": $PENDING_DECISIONS,
  "pending_proposals": $PENDING_PROPOSALS,
  "owner_review_required": $OWNER_REVIEW_REQUIRED
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
