#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Safe Status =="
echo "Path: $ROOT"
echo ""

if [ -d .git ]; then
  echo "Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  echo "Last commit: $(git log -1 --oneline 2>/dev/null || echo unknown)"
  echo ""
  echo "Git changes:"
  git status --short || true
else
  echo "Git: not detected"
fi

echo ""
echo "Important files:"
for f in package.json pyproject.toml requirements.txt Makefile README.md .env; do
  if [ -e "$f" ]; then
    if [ "$f" = ".env" ]; then
      echo "  .env: exists, redacted"
    else
      echo "  $f: exists"
    fi
  else
    echo "  $f: missing"
  fi
done

echo ""
echo "Runtime:"
command -v node >/dev/null 2>&1 && echo "  node: $(node -v)" || echo "  node: not found"
command -v npm >/dev/null 2>&1 && echo "  npm: $(npm -v)" || echo "  npm: not found"
command -v python3 >/dev/null 2>&1 && echo "  python3: $(python3 --version)" || echo "  python3: not found"
