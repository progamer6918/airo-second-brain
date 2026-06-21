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
if tmux has-session -t earnsai-paper-runtime 2>/dev/null; then
  echo "PAPER_RUNTIME_ALREADY_RUNNING"
else
  make paper-runtime-tmux-start
fi
