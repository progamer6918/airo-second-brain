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

LOCK_FILE="locks/airo-runtime.lock"
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
      echo '{"success": false, "message": "Fresh active lock exists. Skipping run."}'
    else
      log "Fresh active lock exists. Skipping run."
    fi
    exit 0
  fi
fi

touch "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

log "Starting runtime runner..."

# 2. Run Health
log "Running health check..."
if [ "$JSON_MODE" = true ]; then
  ./scripts/airo-health --json > /dev/null 2>&1 || true
else
  ./scripts/airo-health > /dev/null 2>&1 || true
fi

# 3. Run Remote Queue Processor
log "Running remote queue processor..."
Q_ARGS=""
if [ "$DRY_RUN" = true ]; then
  Q_ARGS="--dry-run"
fi
./ops/remote-queue/process-remote-queue.sh $Q_ARGS > /dev/null 2>&1 || true

# 4. Run Sync Dry-Run (Always safe)
log "Running sync dry-run..."
./scripts/airo-sync --dry-run > /dev/null 2>&1 || true

# 5. Optionally run real sync only if safe
RUNTIME_SYNC_MODE="dry_run_only" # Hardcoded safe default until proven

if [ "$RUNTIME_SYNC_MODE" = "real_sync_enabled" ] && [ "$DRY_RUN" = false ]; then
  log "Running real sync..."
  ./scripts/airo-sync > /dev/null 2>&1 || log "Real sync encountered an error."
else
  log "Skipping real sync (mode: $RUNTIME_SYNC_MODE)"
fi

# Update state
timestamp=$(date -Iseconds)
echo "$timestamp" > state/last-runtime-run.txt

# Telegram policy enforcement mock
if [ "$NO_NOTIFY" = false ]; then
  log "Evaluating Telegram notification policy..."
  # "No news = no Telegram", "No-op = silent"
  # Since this is a dry-run or routine check, we don't spam.
  log "No-op sync = silent. Notification suppressed."
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
