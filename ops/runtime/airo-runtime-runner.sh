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

notify() {
  if [ "$NO_NOTIFY" = false ]; then
    log "[NOTIFY] Sending Telegram notification: $*"
    if ! ./ops/notifications/telegram-notify.sh "$@"; then
      log "Warning: Telegram notification failed for args: $*"
    fi
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

STATUS_BEFORE=$(./ops/runtime/airo-runtime-status.sh --json || echo "{}")
READY_BEFORE=$(echo "$STATUS_BEFORE" | grep -o '"ready": "[^"]*"' | cut -d'"' -f4 || echo "unknown")
SB_STATUS_BEFORE=$(echo "$STATUS_BEFORE" | grep -o '"second_brain_status": "[^"]*"' | cut -d'"' -f4 || echo "unknown")

log "Starting runtime runner..."

notify --type runtime_online --message "🚀 **AIRO Second Brain Runtime Started**"$'\n'"Status: Checking system health..."$'\n'"Time: $(date -Iseconds)"

# 2. git fetch/pull/rebase safe
log "Step 2: Performing git fetch and safe rebase..."

WORKTREE_CLEAN=true
if [ -n "$(git status --porcelain)" ]; then
  WORKTREE_CLEAN=false
fi

LOCAL_HEAD=$(git rev-parse HEAD)
ORIGIN_MAIN=$(git rev-parse origin/main 2>/dev/null || echo "")

if [ -z "$ORIGIN_MAIN" ]; then
  REMOTE_RELATION="EQUAL"
elif [ "$LOCAL_HEAD" = "$ORIGIN_MAIN" ]; then
  REMOTE_RELATION="EQUAL"
elif git merge-base --is-ancestor "$ORIGIN_MAIN" "$LOCAL_HEAD" 2>/dev/null; then
  REMOTE_RELATION="LOCAL_AHEAD"
elif git merge-base --is-ancestor "$LOCAL_HEAD" "$ORIGIN_MAIN" 2>/dev/null; then
  REMOTE_RELATION="REMOTE_AHEAD"
else
  REMOTE_RELATION="DIVERGED"
fi

RUN_DEGRADED=false
DEGRADED_REASON=""

if [ "$WORKTREE_CLEAN" = true ]; then
  log "Worktree is clean (Relation: $REMOTE_RELATION)."
  if [ "$DRY_RUN" = false ]; then
    git fetch origin main >/dev/null 2>&1 || log "Warning: Git fetch failed."
    
    # Re-evaluate relation after fetch
    LOCAL_HEAD=$(git rev-parse HEAD)
    ORIGIN_MAIN=$(git rev-parse origin/main 2>/dev/null || echo "")
    if [ "$LOCAL_HEAD" = "$ORIGIN_MAIN" ]; then
      REMOTE_RELATION="EQUAL"
    elif git merge-base --is-ancestor "$ORIGIN_MAIN" "$LOCAL_HEAD" 2>/dev/null; then
      REMOTE_RELATION="LOCAL_AHEAD"
    elif git merge-base --is-ancestor "$LOCAL_HEAD" "$ORIGIN_MAIN" 2>/dev/null; then
      REMOTE_RELATION="REMOTE_AHEAD"
    else
      REMOTE_RELATION="DIVERGED"
    fi

    if [ "$REMOTE_RELATION" = "REMOTE_AHEAD" ] || [ "$REMOTE_RELATION" = "DIVERGED" ]; then
      log "Remote is ahead or diverged. Rebasing..."
      if ! git rebase origin/main >/dev/null 2>&1; then
        log "Warning: Git rebase failed, aborting..."
        git rebase --abort >/dev/null 2>&1 || true
      fi
    fi
  fi
else
  log "Worktree is dirty."
  if [ "$DRY_RUN" = false ]; then
    git fetch origin main >/dev/null 2>&1 || log "Warning: Git fetch failed."
    
    # Re-evaluate relation after fetch
    LOCAL_HEAD=$(git rev-parse HEAD)
    ORIGIN_MAIN=$(git rev-parse origin/main 2>/dev/null || echo "")
    if [ "$LOCAL_HEAD" = "$ORIGIN_MAIN" ]; then
      REMOTE_RELATION="EQUAL"
    elif git merge-base --is-ancestor "$ORIGIN_MAIN" "$LOCAL_HEAD" 2>/dev/null; then
      REMOTE_RELATION="LOCAL_AHEAD"
    elif git merge-base --is-ancestor "$LOCAL_HEAD" "$ORIGIN_MAIN" 2>/dev/null; then
      REMOTE_RELATION="REMOTE_AHEAD"
    else
      REMOTE_RELATION="DIVERGED"
    fi
  fi

  if [ "$REMOTE_RELATION" = "EQUAL" ] || [ "$REMOTE_RELATION" = "LOCAL_AHEAD" ]; then
    log "SAFE_REBASE_SKIPPED_DIRTY_WORKTREE (Relation: $REMOTE_RELATION). Continuing..."
  else
    log "DEGRADED_REMOTE_SYNC_BLOCKED (Relation: $REMOTE_RELATION). Cannot rebase/push."
    RUN_DEGRADED=true
    DEGRADED_REASON="DEGRADED_REMOTE_SYNC_BLOCKED"
    RUNTIME_SYNC_MODE="degraded_sync_disabled"
  fi
fi

# 3. poll Telegram actions
log "Step 3: Polling Telegram actions..."
if [ "$DRY_RUN" = false ]; then
  ./ops/telegram/telegram-action-poller.sh >/dev/null 2>&1 || log "Warning: Telegram action poller failed."
fi

# 4. process Telegram actions
log "Step 4: Processing Telegram actions..."
if [ "$DRY_RUN" = false ]; then
  ./ops/telegram/telegram-action-processor.sh >/dev/null 2>&1 || log "Warning: Telegram action processor failed."
fi

# 5. detect manual queue pending
log "Step 5: Detecting manual queue pending..."
MQ_STATUS=$(./scripts/airo-manual-queue-status || echo "")
MQ_PENDING_COUNT=$(echo "$MQ_STATUS" | grep "^pending_count:" | cut -d' ' -f2 || echo "")
MQ_LATEST_ID=$(echo "$MQ_STATUS" | grep "^latest_capture_id:" | cut -d' ' -f2 || echo "")
MQ_LATEST_TITLE=$(echo "$MQ_STATUS" | grep "^latest_capture_title:" | cut -d' ' -f2- || echo "")

# 6. send Earesmes manual queue action card only if new/changed and cooldown allows
if [ -n "$MQ_PENDING_COUNT" ] && [ "$MQ_PENDING_COUNT" -gt 0 ]; then
  log "Step 6: Sending Earesmes manual queue action card..."
  MQ_SUMMARY=$(./scripts/airo-manual-queue-summarize "$MQ_LATEST_ID" || echo "")
  notify --type manual_queue_card --capture-id "$MQ_LATEST_ID" --message "$MQ_LATEST_TITLE" --extra "$MQ_SUMMARY"
else
  log "Step 6: No pending manual queue items."
fi

# 7. detect owner review pending
log "Step 7: Detecting owner review pending..."
STATUS_NOW=$(./ops/runtime/airo-runtime-status.sh --json || echo "{}")
REVIEW_COUNT=$(echo "$STATUS_NOW" | grep -o '"owner_review_required": [0-9]*' | cut -d' ' -f2 || echo "0")

# 8. send Earesmes owner review card only if new/changed and cooldown allows
if [ -n "$REVIEW_COUNT" ] && [ "$REVIEW_COUNT" -gt 0 ]; then
  log "Step 8: Sending Earesmes owner review card..."
  REVIEW_ITEMS=$(python3 -c "
import re, os
r_file = 'reviews/owner-review-queue-20260612.md'
if os.path.exists(r_file):
    with open(r_file, 'r') as f:
        content = f.read()
    sections = re.split(r'\n(## Review Item \d+:.*)', content)
    summary_text = ''
    item_num = 1
    for i in range(1, len(sections), 2):
        title = sections[i].replace('## Review Item', '').strip()
        title = re.sub(r'^\d+:\s*', '', title)
        body = sections[i+1]
        rec_match = re.search(r'Recommended owner action:\s*\n-\s*(\w+)', body)
        rec_action = rec_match.group(1) if rec_match else 'unknown'
        summary_text += f'{item_num}. {title} — {rec_action.lower()}\n'
        item_num += 1
    print(summary_text.strip())
" || echo "")
  if [ -n "$REVIEW_ITEMS" ]; then
    notify --type owner_review_card --message "$REVIEW_ITEMS"
  fi
else
  log "Step 8: No pending owner review items."
fi

# 9. process remote queue
log "Step 9: Running remote queue processor..."
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
    notify --type remote_queue_processed --message "📥 **Remote Queue Processed**"$'\n'"Items processed: $Q_COUNT"$'\n'"Time: $(date -Iseconds)"
  fi
fi

# 10. run health
log "Step 10: Running health check..."
if [ "$JSON_MODE" = true ]; then
  ./scripts/airo-health --no-write --json > /dev/null 2>&1 || true
else
  ./scripts/airo-health --no-write > /dev/null 2>&1 || true
fi

# 11. sync safe changes
log "Step 11: Running real sync..."
RUNTIME_SYNC_MODE="real_sync_enabled"
SYNC_PUSHED_NOTIFIED=false
if [ "$RUNTIME_SYNC_MODE" = "real_sync_enabled" ] && [ "$DRY_RUN" = false ]; then
  SYNC_OUT=$(./scripts/airo-sync --json 2>&1)
  SYNC_RES=$?
  if [ $SYNC_RES -eq 0 ]; then
    PUSHED=$(echo "$SYNC_OUT" | grep -o '"push_successful": [a-z]*' | cut -d' ' -f2)
    if [ "$PUSHED" = "true" ]; then
      log "Real sync pushed changes successfully."
      COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')
      COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null | head -n 1 || echo 'auto-sync')
      notify --type sync_pushed --message "🔄 **State Synced**"$'\n'"Commit: $COMMIT_HASH"$'\n'"Message: $COMMIT_MSG"$'\n'"Time: $(date -Iseconds)"
      SYNC_PUSHED_NOTIFIED=true
    else
      log "Real sync completed (no changes to push)."
    fi
  else
    log "Real sync failed or blocked (exit code $SYNC_RES)."
    notify --type sync_failed --message "⚠️ **AIRO Second Brain State Change**"$'\n'"Current State: degraded"$'\n'"Reason: Real sync failed or blocked (exit code $SYNC_RES)."$'\n'"Time: $(date -Iseconds)"
  fi
else
  log "Skipping real sync (mode: $RUNTIME_SYNC_MODE)"
fi

# 12. release lock
log "Step 12: Releasing lock."

# Update state
timestamp=$(date -Iseconds)
echo "$timestamp" > state/last-runtime-run.txt

STATUS_AFTER=$(./ops/runtime/airo-runtime-status.sh --json || echo "{}")
SB_STATUS_AFTER=$(echo "$STATUS_AFTER" | grep -o '"second_brain_status": "[^"]*"' | cut -d'"' -f4 || echo "unknown")

# Persist health changes only on transition to minimize commit noise
if [ "$SB_STATUS_BEFORE" != "$SB_STATUS_AFTER" ]; then
  log "Health status changed from $SB_STATUS_BEFORE to $SB_STATUS_AFTER. Persisting updated health file..."
  ./scripts/airo-health > /dev/null 2>&1 || true
fi

# Telegram policy enforcement
# Handle transitions between states
if [ "$SB_STATUS_AFTER" = "degraded" ] && [ "$SB_STATUS_BEFORE" != "degraded" ]; then
  notify --type sync_failed --message "⚠️ **AIRO Second Brain State Change**"$'\n'"Previous State: $SB_STATUS_BEFORE"$'\n'"Current State: $SB_STATUS_AFTER"$'\n'"Time: $(date -Iseconds)"
elif [ "$SB_STATUS_AFTER" = "blocked" ] && [ "$SB_STATUS_BEFORE" != "blocked" ]; then
  notify --type runtime_blocked --message "⚠️ **AIRO Second Brain State Change**"$'\n'"Previous State: $SB_STATUS_BEFORE"$'\n'"Current State: $SB_STATUS_AFTER"$'\n'"Time: $(date -Iseconds)"
elif [ "$SB_STATUS_BEFORE" = "degraded" ] || [ "$SB_STATUS_BEFORE" = "blocked" ]; then
  if [ "$SB_STATUS_AFTER" = "healthy" ]; then
    notify --type runtime_recovered --message "✅ **AIRO Second Brain Recovered**"$'\n'"State restored to Healthy."$'\n'"Time: $(date -Iseconds)"
  fi
fi

if [ "$RUN_DEGRADED" = true ]; then
  if [ "$JSON_MODE" = true ]; then
    cat <<EOF
{
  "success": false,
  "dry_run": $DRY_RUN,
  "runtime_sync_mode": "$RUNTIME_SYNC_MODE",
  "message": "Runtime run completed with degraded status: $DEGRADED_REASON."
}
EOF
  else
    log "Runtime run completed with degraded status: $DEGRADED_REASON."
  fi
  exit 1
else
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
  exit 0
fi
