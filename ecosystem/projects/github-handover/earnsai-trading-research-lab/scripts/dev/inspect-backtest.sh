#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_MD="reports/backtest_inspection_$TS.md"
OUT_JSON="reports/backtest_inspection_$TS.json"
LATEST_MD="reports/BACKTEST_INSPECTION_LATEST.md"
LATEST_JSON="reports/BACKTEST_INSPECTION_LATEST.json"

echo "== EarnsAI Backtest/Data Inspector v0.1 =="
echo "Mode: read-only local inspection"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT_MD" "$OUT_JSON" "$LATEST_MD" "$LATEST_JSON" <<'PY'
from pathlib import Path
import csv
import json
import sys
from datetime import datetime
from collections import Counter

out_md = Path(sys.argv[1])
out_json = Path(sys.argv[2])
latest_md = Path(sys.argv[3])
latest_json = Path(sys.argv[4])

TARGET_DIRS = ["backtest", "data", "paper-trading"]
MAX_READ_BYTES = 10 * 1024 * 1024

def file_info(path: Path):
    info = {
        "path": str(path),
        "suffix": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "status": "ok",
    }

    if path.stat().st_size > MAX_READ_BYTES:
        info["status"] = "skipped_large_file"
        return info

    if path.suffix.lower() == ".csv":
        try:
            with path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                info["rows"] = len(rows)
                info["columns"] = reader.fieldnames or []
        except Exception as e:
            info["status"] = f"invalid_csv: {e}"

    elif path.suffix.lower() == ".json":
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                info["json_type"] = "dict"
                info["top_level_keys"] = list(data.keys())[:20]
            elif isinstance(data, list):
                info["json_type"] = "list"
                info["rows"] = len(data)
            else:
                info["json_type"] = type(data).__name__
        except Exception as e:
            info["status"] = f"invalid_json: {e}"

    elif path.suffix.lower() == ".py":
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            info["lines"] = len(text.splitlines())
            info["contains_backtest_signal"] = any(
                token in text.lower()
                for token in ["backtest", "strategy", "signal", "paper", "portfolio", "pnl"]
            )
        except Exception as e:
            info["status"] = f"read_error: {e}"

    elif path.suffix.lower() in [".md", ".txt"]:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            info["lines"] = len(text.splitlines())
        except Exception as e:
            info["status"] = f"read_error: {e}"

    return info

all_files = []
folders = {}

for folder in TARGET_DIRS:
    path = Path(folder)
    if not path.exists() or not path.is_dir():
        folders[folder] = {
            "exists": False,
            "files": 0,
            "by_extension": {},
            "items": [],
        }
        continue

    files = sorted([p for p in path.rglob("*") if p.is_file()])
    items = [file_info(p) for p in files]
    by_ext = Counter((p.suffix.lower() or "[no_ext]") for p in files)

    folders[folder] = {
        "exists": True,
        "files": len(files),
        "by_extension": dict(by_ext),
        "items": items,
    }
    all_files.extend(items)

status_counts = Counter(item["status"] for item in all_files)
ext_counts = Counter(item["suffix"] or "[no_ext]" for item in all_files)

analysis = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "mode": "read-only local inspection",
    "target_dirs": TARGET_DIRS,
    "folder_summary": {
        folder: {
            "exists": data["exists"],
            "files": data["files"],
            "by_extension": data["by_extension"],
        }
        for folder, data in folders.items()
    },
    "status_counts": dict(status_counts),
    "extension_counts": dict(ext_counts),
    "files": all_files,
}

lines = []
lines.append("# EarnsAI Backtest/Data Inspection v0.1")
lines.append("")
lines.append(f"- Generated at: {analysis['generated_at']}")
lines.append("- Phase: Phase 4 — Trading Research Lab")
lines.append("- Mode: read-only local inspection")
lines.append("- Network/API/live trading: disabled")
lines.append("- `.env` / credentials: not read")
lines.append("")

lines.append("## Folder Summary")
lines.append("")
lines.append("| Folder | Exists | Files | Extensions |")
lines.append("|---|---:|---:|---|")
for folder, data in analysis["folder_summary"].items():
    ext_text = ", ".join(f"{k}:{v}" for k, v in data["by_extension"].items()) or "-"
    lines.append(f"| `{folder}/` | {data['exists']} | {data['files']} | {ext_text} |")
lines.append("")

lines.append("## File Health")
lines.append("")
lines.append("| Status | Count |")
lines.append("|---|---:|")
for status, count in analysis["status_counts"].items():
    lines.append(f"| `{status}` | {count} |")
lines.append("")

lines.append("## Dataset Candidates")
lines.append("")
dataset_candidates = [
    item for item in all_files
    if item["suffix"] in [".csv", ".json"] and item["status"] == "ok"
]

if dataset_candidates:
    lines.append("| File | Type | Rows/Keys | Size |")
    lines.append("|---|---|---:|---:|")
    for item in dataset_candidates:
        if item["suffix"] == ".csv":
            detail = f"rows={item.get('rows', '-')}, cols={len(item.get('columns', []))}"
        elif item["suffix"] == ".json":
            if item.get("json_type") == "dict":
                detail = f"keys={len(item.get('top_level_keys', []))}"
            elif item.get("json_type") == "list":
                detail = f"rows={item.get('rows', '-')}"
            else:
                detail = item.get("json_type", "-")
        else:
            detail = "-"
        lines.append(f"| `{item['path']}` | `{item['suffix']}` | {detail} | {item['size_bytes']} |")
else:
    lines.append("- No valid CSV/JSON dataset candidates detected.")
lines.append("")

lines.append("## Python Research Scripts")
lines.append("")
py_items = [item for item in all_files if item["suffix"] == ".py"]
if py_items:
    lines.append("| File | Lines | Backtest Signals |")
    lines.append("|---|---:|---:|")
    for item in py_items:
        lines.append(f"| `{item['path']}` | {item.get('lines', '-')} | {item.get('contains_backtest_signal', False)} |")
else:
    lines.append("- No Python scripts detected in inspected folders.")
lines.append("")

lines.append("## Research Notes")
lines.append("")
if dataset_candidates:
    lines.append("- Local dataset candidates are available for the next read-only analysis step.")
else:
    lines.append("- Dataset candidates are limited; inspect data sources before strategy logic.")
if py_items:
    lines.append("- Existing Python research/backtest scripts were detected and should be inspected before adding new logic.")
else:
    lines.append("- No existing Python backtest scripts detected in target folders.")
lines.append("- Next safe step: create `make summarize-datasets` to profile CSV/JSON dataset contents before strategy development.")
lines.append("")

report = "\n".join(lines)

out_md.write_text(report, encoding="utf-8")
latest_md.write_text(report, encoding="utf-8")
out_json.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
latest_json.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Inspection markdown created: {out_md}")
print(f"Inspection json created: {out_json}")
print(f"Latest markdown updated: {latest_md}")
print(f"Latest json updated: {latest_json}")
print("")
print("Backtest/data inspection result: PASSED")
PY
