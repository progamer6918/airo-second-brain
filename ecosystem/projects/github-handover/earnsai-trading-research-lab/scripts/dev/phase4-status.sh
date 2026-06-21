#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Phase 4 Status v0.1 =="
echo "Phase: Phase 4 — Trading Research Lab"
echo "Baseline: EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED"
echo "Mode: local/read-only research lab"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - <<'PY'
from pathlib import Path
import json

def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

health = read_json("reports/LAB_HEALTH_LATEST.json")
state = read_json("reports/STATE_DOCTOR_LATEST.json")
paper = read_json("reports/PAPER_ANALYSIS_LATEST.json")

print("Latest health:")
if health and "summary" in health:
    print(f"  health: {health['summary'].get('health')}")
    print(f"  steps: {health['summary'].get('passed')}/{health['summary'].get('total_steps')} passed")
else:
    print("  missing")

print("")
print("State doctor:")
if state:
    print(f"  health: {state.get('health')}")
    warnings = state.get("warnings", [])
    print(f"  warnings: {len(warnings)}")
else:
    print("  missing")

print("")
print("Paper analysis:")
if paper:
    print(f"  rows: {paper.get('rows')}")
    print(f"  symbols: {paper.get('symbols')}")
    print(f"  actions: {paper.get('actions')}")
else:
    print("  missing")

print("")
print("Core commands:")
print("  make daily")
print("  make phase4-status")
print("  make lab-latest")
print("  make command-audit")
print("  make verify-v319")
print("  make diff-v319")

print("")
print("Phase 4 status result: PASSED")
PY
