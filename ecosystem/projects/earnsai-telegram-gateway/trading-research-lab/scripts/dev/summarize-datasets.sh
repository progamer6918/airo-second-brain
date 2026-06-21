#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_MD="reports/dataset_summary_$TS.md"
OUT_JSON="reports/dataset_summary_$TS.json"
LATEST_MD="reports/DATASET_SUMMARY_LATEST.md"
LATEST_JSON="reports/DATASET_SUMMARY_LATEST.json"

echo "== EarnsAI Dataset Summarizer v0.1 =="
echo "Mode: read-only local dataset profiling"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT_MD" "$OUT_JSON" "$LATEST_MD" "$LATEST_JSON" <<'PY'
from pathlib import Path
import csv
import json
import sys
from datetime import datetime
from statistics import mean
from collections import Counter

out_md = Path(sys.argv[1])
out_json = Path(sys.argv[2])
latest_md = Path(sys.argv[3])
latest_json = Path(sys.argv[4])

TARGETS = [
    Path("paper_trades.csv"),
    Path("trading_data.json"),
    Path("portfolio_snapshot.json"),
    Path("trade_log.json"),
]

for folder in ["data", "backtest", "paper-trading"]:
    p = Path(folder)
    if p.exists():
        TARGETS.extend(sorted([x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in [".csv", ".json"]]))

MAX_SIZE = 10 * 1024 * 1024
MAX_ROWS_PROFILE = 5000

def as_float(v):
    try:
        if v is None or str(v).strip() == "":
            return None
        return float(str(v).replace(",", ""))
    except Exception:
        return None

def profile_csv(path):
    result = {
        "path": str(path),
        "type": "csv",
        "size_bytes": path.stat().st_size,
        "status": "ok",
        "rows_profiled": 0,
        "columns": [],
        "numeric_columns": {},
        "top_values": {},
    }

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        result["columns"] = reader.fieldnames or []
        numeric_values = {c: [] for c in result["columns"]}
        value_counts = {c: Counter() for c in result["columns"]}
        total_rows = 0

        for row in reader:
            total_rows += 1
            if total_rows <= MAX_ROWS_PROFILE:
                for c in result["columns"]:
                    val = row.get(c)
                    if val not in (None, ""):
                        value_counts[c][str(val)[:80]] += 1
                    num = as_float(val)
                    if num is not None:
                        numeric_values[c].append(num)

        result["rows_total"] = total_rows
        result["rows_profiled"] = min(total_rows, MAX_ROWS_PROFILE)

    for c, values in numeric_values.items():
        if values:
            result["numeric_columns"][c] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "average": round(mean(values), 8),
            }

    for c, counter in value_counts.items():
        if counter:
            result["top_values"][c] = counter.most_common(5)

    return result

def profile_json(path):
    result = {
        "path": str(path),
        "type": "json",
        "size_bytes": path.stat().st_size,
        "status": "ok",
    }

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        result["json_type"] = "dict"
        result["top_level_keys"] = list(data.keys())[:30]
        result["key_count"] = len(data)
    elif isinstance(data, list):
        result["json_type"] = "list"
        result["rows"] = len(data)
        if data and isinstance(data[0], dict):
            keys = sorted({k for row in data[:MAX_ROWS_PROFILE] if isinstance(row, dict) for k in row.keys()})
            result["detected_keys"] = keys[:50]
    else:
        result["json_type"] = type(data).__name__

    return result

seen = set()
profiles = []

for path in TARGETS:
    if not path.exists() or not path.is_file():
        continue
    if str(path) in seen:
        continue
    seen.add(str(path))

    if path.stat().st_size > MAX_SIZE:
        profiles.append({
            "path": str(path),
            "type": path.suffix.lower(),
            "size_bytes": path.stat().st_size,
            "status": "skipped_large_file",
        })
        continue

    try:
        if path.suffix.lower() == ".csv":
            profiles.append(profile_csv(path))
        elif path.suffix.lower() == ".json":
            profiles.append(profile_json(path))
    except Exception as e:
        profiles.append({
            "path": str(path),
            "type": path.suffix.lower(),
            "size_bytes": path.stat().st_size,
            "status": f"invalid: {e}",
        })

status_counts = Counter(p["status"] for p in profiles)
type_counts = Counter(p["type"] for p in profiles)

analysis = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "mode": "read-only local dataset profiling",
    "profiles": profiles,
    "status_counts": dict(status_counts),
    "type_counts": dict(type_counts),
}

lines = []
lines.append("# EarnsAI Dataset Summary v0.1")
lines.append("")
lines.append(f"- Generated at: {analysis['generated_at']}")
lines.append("- Phase: Phase 4 — Trading Research Lab")
lines.append("- Mode: read-only local dataset profiling")
lines.append("- Network/API/live trading: disabled")
lines.append("- `.env` / credentials: not read")
lines.append("")

lines.append("## Overview")
lines.append("")
lines.append(f"- Dataset files detected: `{len(profiles)}`")
lines.append(f"- Status counts: `{dict(status_counts)}`")
lines.append(f"- Type counts: `{dict(type_counts)}`")
lines.append("")

lines.append("## Dataset Files")
lines.append("")
lines.append("| File | Type | Status | Size | Rows/Keys |")
lines.append("|---|---|---|---:|---|")
for p in profiles:
    if p["type"] == "csv":
        detail = f"rows={p.get('rows_total', '-')}, cols={len(p.get('columns', []))}"
    elif p["type"] == "json":
        if p.get("json_type") == "dict":
            detail = f"keys={p.get('key_count', '-')}"
        elif p.get("json_type") == "list":
            detail = f"rows={p.get('rows', '-')}"
        else:
            detail = p.get("json_type", "-")
    else:
        detail = "-"
    lines.append(f"| `{p['path']}` | `{p['type']}` | `{p['status']}` | {p['size_bytes']} | {detail} |")
lines.append("")

lines.append("## Numeric CSV Columns")
lines.append("")
found_numeric = False
for p in profiles:
    if p.get("type") == "csv" and p.get("numeric_columns"):
        found_numeric = True
        lines.append(f"### `{p['path']}`")
        lines.append("")
        lines.append("| Column | Count | Min | Max | Average |")
        lines.append("|---|---:|---:|---:|---:|")
        for col, stats in p["numeric_columns"].items():
            lines.append(f"| `{col}` | {stats['count']} | {stats['min']} | {stats['max']} | {stats['average']} |")
        lines.append("")
if not found_numeric:
    lines.append("- No numeric CSV columns detected.")
    lines.append("")

lines.append("## JSON Structures")
lines.append("")
for p in profiles:
    if p.get("type") == "json" and p.get("status") == "ok":
        lines.append(f"### `{p['path']}`")
        lines.append(f"- JSON type: `{p.get('json_type')}`")
        if p.get("top_level_keys"):
            lines.append(f"- Top-level keys: `{', '.join(map(str, p['top_level_keys']))}`")
        if p.get("detected_keys"):
            lines.append(f"- Detected row keys: `{', '.join(map(str, p['detected_keys']))}`")
        lines.append("")

lines.append("## Research Notes")
lines.append("")
valid = [p for p in profiles if p.get("status") == "ok"]
csv_valid = [p for p in valid if p.get("type") == "csv"]
json_valid = [p for p in valid if p.get("type") == "json"]

lines.append(f"- Valid CSV datasets: `{len(csv_valid)}`")
lines.append(f"- Valid JSON datasets: `{len(json_valid)}`")

if csv_valid:
    lines.append("- CSV datasets are ready for simple research metrics and backtest preparation.")
if json_valid:
    lines.append("- JSON state/snapshot files are available for bot-state consistency checks.")

lines.append("- Next safe step: create `make lab-index` to combine latest reports into one Research Lab index.")
lines.append("")

report = "\n".join(lines)

out_md.write_text(report, encoding="utf-8")
latest_md.write_text(report, encoding="utf-8")
out_json.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
latest_json.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Dataset summary markdown created: {out_md}")
print(f"Dataset summary json created: {out_json}")
print(f"Latest markdown updated: {latest_md}")
print(f"Latest json updated: {latest_json}")
print("")
print("Dataset summary result: PASSED")
PY
