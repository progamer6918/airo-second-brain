#!/usr/bin/env bash
# AIRO Earesmes — Telegram Gateway
# Single getUpdates consumer + multi-app router.
# Replaces both telegram-action-listener.sh and resolves 409 conflict.
# Usage: bash ops/telegram/telegram-gateway.sh
exec python3 /home/egitaristorandas/AI_WORKSPACES/airo-second-brain/ops/telegram/telegram-gateway.py "$@"
