#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

has_npm_script() {
  local script="$1"
  node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$script'] ? 0 : 1)" 2>/dev/null
}

if [ -f package.json ] && command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1; then
  if has_npm_script dev; then
    npm run dev
  elif has_npm_script start; then
    npm start
  else
    echo "No dev/start script found."
    exit 1
  fi
else
  echo "No runnable npm project detected."
  exit 1
fi
