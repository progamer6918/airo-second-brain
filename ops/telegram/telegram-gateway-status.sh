#!/usr/bin/env bash
# ops/telegram/telegram-gateway-status.sh
# Read-only status report for AIRO Telegram Gateway

LOCK_FILE="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain/state/runtime/telegram-gateway.lock"
OFFSET_FILE="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain/state/runtime/telegram-gateway-offset"
LAST_UPDATE_FILE="/home/egitaristorandas/AI_WORKSPACES/airo-second-brain/state/runtime/telegram-gateway-last-update"

GATEWAY_RUNNING="no"
GATEWAY_PID="none"

if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE" 2>/dev/null | tr -d '[:space:]')
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        # Verify process cmdline contains telegram-gateway
        CMD=$(ps -fp "$PID" -o cmd= 2>/dev/null)
        if echo "$CMD" | grep -q "telegram-gateway"; then
            GATEWAY_RUNNING="yes"
            GATEWAY_PID="$PID"
        else
            GATEWAY_RUNNING="no (stale/recycled PID)"
        fi
    fi
fi

OFFSET="none"
if [ -f "$OFFSET_FILE" ]; then
    OFFSET=$(cat "$OFFSET_FILE" 2>/dev/null)
fi

LAST_TICK="none"
if [ -f "$LAST_UPDATE_FILE" ]; then
    LAST_TICK=$(cat "$LAST_UPDATE_FILE" 2>/dev/null)
fi

echo "=== AIRO Telegram Gateway Status ==="
echo "gateway_running: $GATEWAY_RUNNING"
echo "pid: $GATEWAY_PID"
echo "offset: $OFFSET"
echo "last_callback: $LAST_TICK"
