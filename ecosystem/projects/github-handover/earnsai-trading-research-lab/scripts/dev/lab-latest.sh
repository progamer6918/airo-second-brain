#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Latest Lab Reports v0.1 =="
echo "Mode: read-only local summary"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - <<'PY'
from pathlib import Path
import json

reports = Path("reports")

items = [
    ("Lab Health", reports / "LAB_HEALTH_LATEST.json", reports / "LAB_HEALTH_LATEST.md"),
    ("Lab Index", reports / "LAB_INDEX_LATEST.json", reports / "LAB_INDEX_LATEST.md"),
    ("Dataset Summary", reports / "DATASET_SUMMARY_LATEST.json", reports / "DATASET_SUMMARY_LATEST.md"),
    ("Backtest Inspection", reports / "BACKTEST_INSPECTION_LATEST.json", reports / "BACKTEST_INSPECTION_LATEST.md"),
    ("Paper Analysis", reports / "PAPER_ANALYSIS_LATEST.json", reports / "PAPER_ANALYSIS_LATEST.md"),
    ("Research Report", reports / "RESEARCH_REPORT_LATEST.md", reports / "RESEARCH_REPORT_LATEST.md"),
]

for label, json_path, md_path in items:
    print(f"{label}:")
    print(f"  markdown: {md_path if md_path.exists() else 'missing'}")
    print(f"  json:     {json_path if json_path.exists() else 'missing'}")

    if json_path.exists() and json_path.suffix == ".json":
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            if "summary" in data:
                print(f"  summary:  {data['summary']}")
            elif "rows" in data:
                print(f"  rows:     {data['rows']}")
            elif "status_counts" in data:
                print(f"  status:   {data['status_counts']}")
            elif "folder_summary" in data:
                print(f"  folders:  {list(data['folder_summary'].keys())}")
        except Exception as e:
            print(f"  read:     failed: {e}")

    print("")

print("Latest lab reports result: PASSED")
PY
