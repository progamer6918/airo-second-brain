#!/usr/bin/env bash
# AIRO Earesmes — Telegram Gateway
# Single getUpdates consumer + multi-app router.
# Replaces both telegram-action-listener.sh and resolves 409 conflict.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/telegram-gateway.py" "$@"
