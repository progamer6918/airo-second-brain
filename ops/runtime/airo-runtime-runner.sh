#!/usr/bin/env bash

set -e

SHOW_HELP=false
DRY_RUN=false
JSON_MODE=false
NO_NOTIFY=false
FORCE_NOTIFY=false

for arg in "$@"; do
  case $arg in
    --help)
      SHOW_HELP=true
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    --json)
      JSON_MODE=true
      ;;
    --no-notify)
      NO_NOTIFY=true
      ;;
    --force-notify)
      FORCE_NOTIFY=true
      ;;
  esac
done

if [ "$SHOW_HELP" = true ]; then
  if [ "$JSON_MODE" = true ]; then
    echo '{"help": "Usage: airo-runtime-runner.sh [--help] [--dry-run] [--json] [--no-notify] [--force-notify]"}'
  else
    echo "Usage: airo-runtime-runner.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help          Show this help message"
    echo "  --dry-run       Run in dry-run mode (no actual git push or queue move)"
    echo "  --json          Output results in JSON format"
    echo "  --no-notify     Suppress Telegram notifications"
    echo "  --force-notify  Force Telegram notification regardless of state changes"
  fi
  exit 0
fi

LOCK_FILE="/tmp/airo-second-brain-runtime.lock"
RUNTIME_LOG="logs/runtime.log"

mkdir -p locks logs

log() {
  local msg="$1"
  local timestamp=$(date -Iseconds)
  echo "[$timestamp] $msg" >> "$RUNTIME_LOG"
  if [ "$JSON_MODE" = false ]; then
    echo "[$timestamp] $msg"
  fi
}

# 1. Acquire Lock
if [ -f "$LOCK_FILE" ]; then
  # check age
  file_time=$(stat -c %Y "$LOCK_FILE" 2>/dev/null || stat -f %m "$LOCK_FILE" 2>/dev/null)
  now=$(date +%s)
  age=$((now - file_time))
  if [ "$age" -gt 600 ]; then
    log "Stale lock found (age: ${age}s). Removing..."
    rm -f "$LOCK_FILE"
  else
    if [ "$JSON_MODE" = true ]; then
      echo '{"status": "already_running", "success": false, "message": "Another runtime is already running."}'
    else
      log "Another runtime is already running. status=already_running"
    fi
    exit 0
  fi
fi

touch "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

STATUS_BEFORE=$(./ops/runtime/airo-runtime-status.sh --json)
READY_BEFORE=$(echo "$STATUS_BEFORE" | grep -o '"ready": "[^"]*"' | cut -d'"' -f4)
SB_STATUS_BEFORE=$(echo "$STATUS_BEFORE" | grep -o '"second_brain_status": "[^"]*"' | cut -d'"' -f4)

log "Starting runtime runner..."

if [ "$NO_NOTIFY" = false ]; then
  ./ops/notifications/telegram-notify.sh --type runtime_online --message "🚀 **AIRO Second Brain Runtime Started**"$'\n'"Status: Checking system health..."$'\n'"Time: $(date -Iseconds)"
fi

RUNTIME_SYNC_MODE="real_sync_enabled" # Proven safe

# 2. Run Health
log "Running health check (read-only)..."
if [ "$JSON_MODE" = true ]; then
  ./scripts/airo-health --no-write --json > /dev/null 2>&1 || true
else
  ./scripts/airo-health --no-write > /dev/null 2>&1 || true
fi

# 3. Run Remote Queue Processor
log "Running remote queue processor..."
Q_ARGS=""
if [ "$DRY_RUN" = true ]; then
  Q_ARGS="--dry-run"
fi
Q_OUT=$(./ops/remote-queue/process-remote-queue.sh $Q_ARGS --json 2>&1)
Q_RES=$?
if [ $Q_RES -eq 0 ]; then
  Q_COUNT=$(echo "$Q_OUT" | grep -o '"processed_count": [0-9]*' | cut -d' ' -f2)
  if [ -n "$Q_COUNT" ] && [ "$Q_COUNT" -gt 0 ]; then
    log "Processed $Q_COUNT remote queue items."
    if [ "$NO_NOTIFY" = false ]; then
      ./ops/notifications/telegram-notify.sh --type remote_queue_processed --message "📥 **Remote Queue Processed**"$'\n'"Items processed: $Q_COUNT"$'\n'"Time: $(date -Iseconds)"
    fi
  fi
fi

# 4. Run Sync Dry-Run (Always safe)
log "Running sync dry-run..."
./scripts/airo-sync --dry-run > /dev/null 2>&1 || true

# 5. Optionally run real sync only if safe
SYNC_PUSHED_NOTIFIED=false
if [ "$RUNTIME_SYNC_MODE" = "real_sync_enabled" ] && [ "$DRY_RUN" = false ]; then
  log "Running real sync..."
  SYNC_OUT=$(./scripts/airo-sync --json 2>&1)
  SYNC_RES=$?
  if [ $SYNC_RES -eq 0 ]; then
    PUSHED=$(echo "$SYNC_OUT" | grep -o '"push_successful": [a-z]*' | cut -d' ' -f2)
    if [ "$PUSHED" = "true" ]; then
      log "Real sync pushed changes successfully."
      if [ "$NO_NOTIFY" = false ]; then
        COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null | head -n 1 || echo "auto-sync")
        ./ops/notifications/telegram-notify.sh --type sync_pushed --message "🔄 **State Synced**"$'\n'"Commit: $COMMIT_HASH"$'\n'"Message: $COMMIT_MSG"$'\n'"Time: $(date -Iseconds)"
        SYNC_PUSHED_NOTIFIED=true
      fi
    else
      log "Real sync completed (no changes to push)."
    fi
  else
    log "Real sync failed or blocked (exit code $SYNC_RES)."
    if [ "$NO_NOTIFY" = false ]; then
      ./ops/notifications/telegram-notify.sh --type sync_failed --message "⚠️ **AIRO Second Brain State Change**"$'\n'"Current State: degraded"$'\n'"Reason: Real sync failed or blocked (exit code $SYNC_RES)."$'\n'"Time: $(date -Iseconds)"
    fi
  fi
else
  log "Skipping real sync (mode: $RUNTIME_SYNC_MODE)"
fi

# Update state
timestamp=$(date -Iseconds)
echo "$timestamp" > state/last-runtime-run.txt

STATUS_AFTER=$(./ops/runtime/airo-runtime-status.sh --json)
READY_AFTER=$(echo "$STATUS_AFTER" | grep -o '"ready": "[^"]*"' | cut -d'"' -f4)
SB_STATUS_AFTER=$(echo "$STATUS_AFTER" | grep -o '"second_brain_status": "[^"]*"' | cut -d'"' -f4)
REVIEW_COUNT=$(echo "$STATUS_AFTER" | grep -o '"owner_review_required": [0-9]*' | cut -d' ' -f2)

# Persist health changes only on transition to minimize commit noise
if [ "$SB_STATUS_BEFORE" != "$SB_STATUS_AFTER" ]; then
  log "Health status changed from $SB_STATUS_BEFORE to $SB_STATUS_AFTER. Persisting updated health file..."
  ./scripts/airo-health > /dev/null 2>&1 || true
fi

# Telegram policy enforcement
if [ "$NO_NOTIFY" = false ]; then
  # Handle transitions between states
  if [ "$SB_STATUS_AFTER" = "degraded" ]; then
    ./ops/notifications/telegram-notify.sh --type sync_failed --message "⚠️ **AIRO Second Brain State Change**"$'\n'"Previous State: $SB_STATUS_BEFORE"$'\n'"Current State: $SB_STATUS_AFTER"$'\n'"Time: $(date -Iseconds)"
  elif [ "$SB_STATUS_AFTER" = "blocked" ]; then
    ./ops/notifications/telegram-notify.sh --type runtime_blocked --message "⚠️ **AIRO Second Brain State Change**"$'\n'"Previous State: $SB_STATUS_BEFORE"$'\n'"Current State: $SB_STATUS_AFTER"$'\n'"Time: $(date -Iseconds)"
  elif [ "$SB_STATUS_BEFORE" = "degraded" ] || [ "$SB_STATUS_BEFORE" = "blocked" ]; then
    if [ "$SB_STATUS_AFTER" = "healthy" ]; then
      ./ops/notifications/telegram-notify.sh --type runtime_recovered --message "✅ **AIRO Second Brain Recovered**"$'\n'"State restored to Healthy."$'\n'"Time: $(date -Iseconds)"
    fi
  fi

  # Handle owner review needed
  if [ -n "$REVIEW_COUNT" ] && [ "$REVIEW_COUNT" -gt 0 ]; then
    ./ops/notifications/telegram-notify.sh --type owner_review_needed --message "⚠️ **AIRO Second Brain Owner Review Needed**"$'\n'"Pending items: $REVIEW_COUNT"$'\n'"Time: $(date -Iseconds)"
  fi
fi

if [ "$JSON_MODE" = true ]; then
  cat <<EOF
{
  "success": true,
  "dry_run": $DRY_RUN,
  "runtime_sync_mode": "$RUNTIME_SYNC_MODE",
  "message": "Runtime run completed successfully."
}
EOF
else
  log "Runtime run completed successfully."
fi
