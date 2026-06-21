#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Safe Smoke Test v0.1.1 =="
echo "Mode: offline/local only"
echo "Network/API/live trading: disabled"
echo ""

python3 - <<'PY'
import json
import py_compile
from pathlib import Path

root = Path(".")
python_candidates = [
    "simple_pulse_bot.py",
    "integrated_paper_bot.py",
    "paper_bot.py",
    "paper_bot_lazy.py",
    "analytics.py",
    "report.py",
    "check_balance.py",
    "test_langsung.py",
]

json_candidates = [
    "trading_data.json",
    "portfolio_snapshot.json",
    "trade_log.json",
]

print("Python syntax smoke:")
found_py = 0
for name in python_candidates:
    path = root / name
    if path.exists():
        found_py += 1
        py_compile.compile(str(path), doraise=True)
        print(f"  OK: {name}")

if found_py == 0:
    print("  No known Python entry files found")

print("")
print("JSON integrity smoke:")
found_json = 0
for name in json_candidates:
    path = root / name
    if path.exists():
        found_json += 1
        with path.open("r", encoding="utf-8") as f:
            json.load(f)
        print(f"  OK: {name}")

if found_json == 0:
    print("  No root JSON state files found")

print("")
print("Smoke result: PASSED")
PY
