#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

OUT="docs/CARRY_OVER_PHASE4_LATEST.md"

echo "== EarnsAI Carry-Over Snapshot v0.1 =="
echo "Mode: local project summary"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT" <<'PY'
from pathlib import Path
from datetime import datetime
import json

out = Path(__import__("sys").argv[1])

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

lines = []
lines.append("# PROJECT CARRY-OVER — EarnsAI Phase 4")
lines.append("")
lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append("")
lines.append("## Active Source of Truth")
lines.append("")
lines.append("- Project: EarnsAI")
lines.append("- Current phase: Phase 4 — Trading Research Lab")
lines.append("- Active baseline: EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED")
lines.append("- Progress project: 74/100")
lines.append("- Workflow mode: Senior AI Systems Architect & Production Debugging Engineer")
lines.append("- Safety: no live trading, no private exchange API, no credential exposure")
lines.append("")
lines.append("## Required Response Header")
lines.append("")
lines.append("Every EarnsAI response must start with:")
lines.append("")
lines.append("```text")
lines.append("Status konteks: X/100")
lines.append("Progress project: X/100")
lines.append("Current phase: Phase 4 — Trading Research Lab")
lines.append("Milestone sekarang: ...")
lines.append("Target micro-step: ...")
lines.append("```")
lines.append("")
lines.append("## Current Verified Commands")
lines.append("")
for cmd in [
    "make phase4",
    "make daily",
    "make phase4-status",
    "make lab-refresh",
    "make lab-health",
    "make lab-latest",
    "make command-audit",
    "make verify-v319",
    "make diff-v319",
    "make state-doctor",
    "make research-status",
    "make research-report",
    "make analyze-paper",
    "make inspect-backtest",
    "make summarize-datasets",
    "make lab-index",
]:
    lines.append(f"- `{cmd}`")
lines.append("")
lines.append("## Latest Health")
lines.append("")
if health and "summary" in health:
    s = health["summary"]
    lines.append(f"- Lab health: `{s.get('health')}`")
    lines.append(f"- Passed steps: `{s.get('passed')}/{s.get('total_steps')}`")
else:
    lines.append("- Lab health: missing")
lines.append("")
lines.append("## State Doctor")
lines.append("")
if state:
    lines.append(f"- State health: `{state.get('health')}`")
    lines.append(f"- Warnings: `{len(state.get('warnings', []))}`")
else:
    lines.append("- State doctor: missing")
lines.append("")
lines.append("## Paper Analysis")
lines.append("")
if paper:
    lines.append(f"- Rows: `{paper.get('rows')}`")
    lines.append(f"- Symbols: `{paper.get('symbols')}`")
    lines.append(f"- Actions: `{paper.get('actions')}`")
else:
    lines.append("- Paper analysis: missing")
lines.append("")
lines.append("## Operating Workflow")
lines.append("")
lines.append("Use this principle:")
lines.append("")
lines.append("```text")
lines.append("diagnose → backup → patch kecil → compile check → smoke test → checkpoint → continue unless error/checkpoint besar")
lines.append("```")
lines.append("")
lines.append("## Next Recommended Micro-Step")
lines.append("")
lines.append("Add `make phase4-freeze` to create a stable local release snapshot of the command layer and reports before starting deeper strategy research.")
lines.append("")

out.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Carry-over snapshot created: {out}")
print("Carry-over result: PASSED")
PY
