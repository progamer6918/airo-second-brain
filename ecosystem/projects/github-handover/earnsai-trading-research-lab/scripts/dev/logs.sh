#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== Recent Logs, Redacted =="

LOG_FILES="$(find . -maxdepth 3 -type f \( -name '*.log' -o -path './logs/*' \) 2>/dev/null | head -5 || true)"

if [ -z "$LOG_FILES" ]; then
  echo "No log files found."
  exit 0
fi

for f in $LOG_FILES; do
  echo ""
  echo "--- $f ---"
  tail -80 "$f" | sed -E 's/((token|secret|password|passwd|api[_-]?key|private[_-]?key)[=: ]+)[^ ]+/\1***REDACTED***/Ig'
done
