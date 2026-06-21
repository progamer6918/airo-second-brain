#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Check =="

has_npm_script() {
  local script="$1"
  node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$script'] ? 0 : 1)" 2>/dev/null
}

if [ -f package.json ] && command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1; then
  echo "Detected package.json"

  if has_npm_script typecheck; then
    echo "Running: npm run typecheck"
    npm run -s typecheck
  else
    echo "Skip typecheck: script not found"
  fi

  if has_npm_script lint; then
    echo "Running: npm run lint"
    npm run -s lint
  else
    echo "Skip lint: script not found"
  fi

  if has_npm_script build; then
    echo "Running: npm run build"
    npm run -s build
  else
    echo "Skip build: script not found"
  fi
else
  echo "Node/npm check skipped"
fi

if command -v python3 >/dev/null 2>&1; then
  PY_FILES="$(git ls-files '*.py' 2>/dev/null || true)"
  if [ -n "$PY_FILES" ]; then
    echo "Running Python compile check"
    python3 - <<'PY'
import py_compile, subprocess, sys

files = subprocess.check_output(["git", "ls-files", "*.py"], text=True).splitlines()
failed = []
for f in files:
    try:
        py_compile.compile(f, doraise=True)
    except Exception as e:
        failed.append((f, str(e)))

if failed:
    for f, e in failed:
        print(f"[PY_COMPILE_FAIL] {f}: {e}")
    sys.exit(1)

print("Python compile check passed")
PY
  else
    echo "No tracked Python files detected"
  fi
fi

echo "Check completed."
