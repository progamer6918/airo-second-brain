#!/usr/bin/env bash
set -euo pipefail
REPO="$HOME/earnsai-pulse-trading"
ENV_FILE="$HOME/.config/earnsai-pulse/paper_runtime.env"
cd "$REPO"
if [ -f "$ENV_FILE" ]; then
  set -a
  . "$ENV_FILE"
  set +a
fi
if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] || [ -z "${TELEGRAM_CHAT_ID:-}" ]; then
  echo "TELEGRAM_ENV_MISSING"
  exit 1
fi
if tmux has-session -t earnsai-paper-control 2>/dev/null; then
  echo "PAPER_CONTROL_ALREADY_RUNNING"
else
  tmux new-session -d -s earnsai-paper-control 'cd ~/earnsai-pulse-trading && set -a && . ~/.config/earnsai-pulse/paper_runtime.env && set +a && python3 scripts/telegram_paper_control_bot.py'
  echo "PAPER_CONTROL_TMUX_STARTED"
fi
