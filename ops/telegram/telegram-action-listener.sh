#!/usr/bin/env bash
# AIRO Earesmes — Telegram Live Action Listener (Redirected to Gateway)
# Runs persistent long-poll loop. Lock-guarded. Never prints token/chat_id.
# Usage: bash ops/telegram/telegram-action-listener.sh [--daemon]
exec bash /home/egitaristorandas/AI_WORKSPACES/airo-second-brain/ops/telegram/telegram-gateway.sh "$@"

