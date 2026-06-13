#!/usr/bin/env bash
# AIRO Earesmes — Telegram Live Action Listener
# Runs persistent long-poll loop. Lock-guarded. Never prints token/chat_id.
# Usage: bash ops/telegram/telegram-action-listener.sh [--daemon]
exec python3 /home/egitaristorandas/AI_WORKSPACES/airo-second-brain/ops/telegram/telegram-action-listener.py "$@"
