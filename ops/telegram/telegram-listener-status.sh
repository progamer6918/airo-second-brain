#!/usr/bin/env bash
# AIRO Earesmes — Telegram Listener Status
# Shows listener running state, PID, last update. Never prints token/chat_id.

REPO_DIR="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
STATE_RUNTIME="$REPO_DIR/state/runtime"
LOCK_FILE="$STATE_RUNTIME/telegram-listener.lock"
OFFSET_FILE="$STATE_RUNTIME/telegram-update-offset"
LASTUPDATE_FILE="$STATE_RUNTIME/telegram-listener-last-update"
LOG_FILE="$REPO_DIR/logs/telegram-listener.log"
ACTIONS_DIR="$REPO_DIR/inbox/telegram-actions"

echo "=== AIRO Earesmes Telegram Listener Status ==="

# Check lock file
if [ -f "$LOCK_FILE" ]; then
  PID=$(cat "$LOCK_FILE" 2>/dev/null | tr -d '[:space:]')
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    echo "listener_running: yes"
    echo "pid: $PID"
    ELAPSED=$(ps -o etime= -p "$PID" 2>/dev/null | tr -d ' ' || echo "unknown")
    echo "uptime: $ELAPSED"
  else
    echo "listener_running: no (stale lock file, pid=$PID not alive)"
    echo "pid: none"
  fi
else
  echo "listener_running: no"
  echo "pid: none"
fi

# Offset
if [ -f "$OFFSET_FILE" ]; then
  OFFSET=$(cat "$OFFSET_FILE")
  echo "update_offset: $OFFSET"
else
  echo "update_offset: 0 (not set)"
fi

# Last update handled
if [ -f "$LASTUPDATE_FILE" ]; then
  echo "last_callback_handled: $(cat "$LASTUPDATE_FILE")"
else
  echo "last_callback_handled: never"
fi

# Callback count
CB_COUNT=$(ls -1 "$ACTIONS_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')
echo "total_action_files: $CB_COUNT"

# Recent log (last 5 lines, no token)
if [ -f "$LOG_FILE" ]; then
  echo ""
  echo "=== Recent log (last 5 lines) ==="
  tail -n 5 "$LOG_FILE"
else
  echo "log_file: not found"
fi

echo ""
echo "token: [HIDDEN]"
echo "chat_id: [HIDDEN]"
