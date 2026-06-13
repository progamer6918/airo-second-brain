#!/usr/bin/env bash
# AIRO Earesmes — Telegram Gateway Status
# Shows gateway state, PID, offset, last callback. Never prints token.

REPO_DIR="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
STATE_RUNTIME="$REPO_DIR/state/runtime"
LOCK_FILE="$STATE_RUNTIME/telegram-gateway.lock"
OFFSET_FILE="$STATE_RUNTIME/telegram-gateway-offset"
LASTUPDATE_FILE="$STATE_RUNTIME/telegram-gateway-last-update"
LOG_FILE="$REPO_DIR/logs/telegram-gateway.log"

echo "=== AIRO Telegram Gateway Status ==="

if [ -f "$LOCK_FILE" ]; then
  PID=$(cat "$LOCK_FILE" 2>/dev/null | tr -d '[:space:]')
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    echo "gateway_running: yes"
    echo "pid: $PID"
    ELAPSED=$(ps -o etime= -p "$PID" 2>/dev/null | tr -d ' ' || echo "unknown")
    echo "uptime: $ELAPSED"
  else
    echo "gateway_running: no (stale lock)"
    echo "pid: none"
  fi
else
  echo "gateway_running: no"
  echo "pid: none"
fi

echo "offset: $(cat "$OFFSET_FILE" 2>/dev/null || echo '0 (not set)')"
echo "last_callback: $(cat "$LASTUPDATE_FILE" 2>/dev/null || echo 'never')"
echo ""
echo "=== Recent log (last 5) ==="
tail -n 5 "$LOG_FILE" 2>/dev/null || echo 'no log'
echo ""
echo "token: [HIDDEN]"
