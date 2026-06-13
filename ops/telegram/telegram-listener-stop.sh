#!/usr/bin/env bash
# AIRO Earesmes — Telegram Listener Stop
# Safely stops running listener. Removes lock file.

REPO_DIR="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
STATE_RUNTIME="$REPO_DIR/state/runtime"
LOCK_FILE="$STATE_RUNTIME/telegram-listener.lock"

echo "=== AIRO Earesmes Telegram Listener Stop ==="

if [ ! -f "$LOCK_FILE" ]; then
  echo "No lock file found. Listener is not running."
  exit 0
fi

PID=$(cat "$LOCK_FILE" 2>/dev/null | tr -d '[:space:]')

if [ -z "$PID" ]; then
  echo "Lock file empty. Removing stale lock."
  rm -f "$LOCK_FILE"
  exit 0
fi

if kill -0 "$PID" 2>/dev/null; then
  echo "Sending SIGTERM to listener PID=$PID"
  kill -TERM "$PID"
  sleep 2
  if kill -0 "$PID" 2>/dev/null; then
    echo "Process still alive — sending SIGKILL"
    kill -KILL "$PID" 2>/dev/null || true
    sleep 1
  fi
  echo "Listener stopped."
else
  echo "PID=$PID not alive. Removing stale lock file."
fi

rm -f "$LOCK_FILE"
echo "Lock file removed."
echo "LISTENER_STOPPED=OK"
