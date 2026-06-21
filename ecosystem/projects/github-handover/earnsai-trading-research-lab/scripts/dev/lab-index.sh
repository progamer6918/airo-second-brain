#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_MD="reports/lab_index_$TS.md"
OUT_JSON="reports/lab_index_$TS.json"
LATEST_MD="reports/LAB_INDEX_LATEST.md"
LATEST_JSON="reports/LAB_INDEX_LATEST.json"

echo "== EarnsAI Research Lab Index v0.1 =="
echo "Mode: read-only report indexing"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT_MD" "$OUT_JSON" "$LATEST_MD" "$LATEST_JSON" <<'PY'
from pathlib import Path
import json
import sys
from datetime import datetime

out_md = Path(sys.argv[1])
out_json = Path(sys.argv[2])
latest_md = Path(sys.argv[3])
latest_json = Path(sys.argv[4])

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

latest_reports = [
    "RESEARCH_REPORT_LATEST.md",
    "PAPER_ANALYSIS_LATEST.md",
    "BACKTEST_INSPECTION_LATEST.md",
    "DATASET_SUMMARY_LATEST.md",
]

all_reports = sorted(
    [p for p in reports_dir.glob("*.md") if p.name != "LAB_INDEX_LATEST.md"],
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

index = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "phase": "Phase 4 — Trading Research Lab",
    "baseline": "EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED",
    "mode": "read-only report indexing",
    "latest_reports": [],
    "recent_reports": [],
}

for name in latest_reports:
    path = reports_dir / name
    index["latest_reports"].append({
        "file": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
    })

for path in all_reports[:20]:
    index["recent_reports"].append({
        "file": str(path),
        "size_bytes": path.stat().st_size,
        "modified_epoch": int(path.stat().st_mtime),
    })

lines = []
lines.append("# EarnsAI Research Lab Index v0.1")
lines.append("")
lines.append(f"- Generated at: {index['generated_at']}")
lines.append("- Phase: Phase 4 — Trading Research Lab")
lines.append("- Baseline: EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED")
lines.append("- Mode: read-only report indexing")
lines.append("- Network/API/live trading: disabled")
lines.append("- `.env` / credentials: not read")
lines.append("")

lines.append("## Latest Reports")
lines.append("")
lines.append("| Report | Exists | Size |")
lines.append("|---|---:|---:|")
for item in index["latest_reports"]:
    lines.append(f"| `{item['file']}` | {item['exists']} | {item['size_bytes']} |")
lines.append("")

lines.append("## Recent Report Files")
lines.append("")
if index["recent_reports"]:
    lines.append("| File | Size |")
    lines.append("|---|---:|")
    for item in index["recent_reports"]:
        lines.append(f"| `{item['file']}` | {item['size_bytes']} |")
else:
    lines.append("- No report files detected.")
lines.append("")

lines.append("## Research Lab Status")
lines.append("")
missing = [x["file"] for x in index["latest_reports"] if not x["exists"]]
if missing:
    lines.append("- Status: partial")
    lines.append("- Missing latest reports:")
    for item in missing:
        lines.append(f"  - `{item}`")
else:
    lines.append("- Status: complete")
    lines.append("- All expected latest report files are available.")
lines.append("")

lines.append("## Next Safe Step")
lines.append("")
lines.append("Create `make lab-health` to run the full read-only Research Lab verification bundle in one command.")
lines.append("")

report = "\n".join(lines)

out_md.write_text(report, encoding="utf-8")
latest_md.write_text(report, encoding="utf-8")
out_json.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
latest_json.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Lab index markdown created: {out_md}")
print(f"Lab index json created: {out_json}")
print(f"Latest markdown updated: {latest_md}")
print(f"Latest json updated: {latest_json}")
print("")
print("Research Lab index result: PASSED")
PY
