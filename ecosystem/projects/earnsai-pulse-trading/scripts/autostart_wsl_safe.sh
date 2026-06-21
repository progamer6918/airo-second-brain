#!/usr/bin/env bash
set -euo pipefail
LOCK_DIR="/tmp/earnsai-pulse-autostart.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT
REPO="$HOME/earnsai-pulse-trading"
cd "$REPO"
bash scripts/start_paper_runtime_safe.sh || true
bash scripts/start_paper_control_bot_safe.sh || true
