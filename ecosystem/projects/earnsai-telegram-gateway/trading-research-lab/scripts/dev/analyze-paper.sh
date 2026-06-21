#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_MD="reports/paper_analysis_$TS.md"
OUT_JSON="reports/paper_analysis_$TS.json"
LATEST_MD="reports/PAPER_ANALYSIS_LATEST.md"
LATEST_JSON="reports/PAPER_ANALYSIS_LATEST.json"

echo "== EarnsAI Paper Trade Analyzer v0.1 =="
echo "Mode: read-only local analysis"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT_MD" "$OUT_JSON" "$LATEST_MD" "$LATEST_JSON" <<'PY'
from pathlib import Path
import csv
import json
import sys
from collections import Counter
from statistics import mean
from datetime import datetime

out_md = Path(sys.argv[1])
out_json = Path(sys.argv[2])
latest_md = Path(sys.argv[3])
latest_json = Path(sys.argv[4])

csv_path = Path("paper_trades.csv")

def norm(row):
    return {str(k).strip().lower(): v for k, v in row.items()}

def get(row, *keys):
    r = norm(row)
    for key in keys:
        if key.lower() in r:
            return r[key.lower()]
    return None

def as_float(v):
    try:
        if v is None or str(v).strip() == "":
            return None
        return float(str(v).replace(",", ""))
    except Exception:
        return None

if not csv_path.exists():
    raise SystemExit("FAILED: paper_trades.csv missing")

with csv_path.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames or []

symbols = []
actions = []
prices = []
timeline = []

for_row_count = 0
for row in rows:
    symbol = get(row, "symbol")
    action = get(row, "action", "side")
    price = as_float(get(row, "price"))
    timestamp = get(row, "timestamp", "time", "datetime")

    if symbol:
        symbols.append(symbol)
    if action:
        actions.append(action)
    if price is not None:
        prices.append(price)

    timeline.append({
        "timestamp": timestamp,
        "symbol": symbol,
        "action": action,
        "price": price,
    })

price_delta = None
price_delta_pct = None
if len(prices) >= 2 and prices[0] != 0:
    price_delta = prices[-1] - prices[0]
    price_delta_pct = (price_delta / prices[0]) * 100

analysis = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "mode": "read-only local analysis",
    "source": "paper_trades.csv",
    "rows": len(rows),
    "columns": fields,
    "symbols": dict(Counter(symbols)),
    "actions": dict(Counter(actions)),
    "price": {
        "count": len(prices),
        "min": min(prices) if prices else None,
        "max": max(prices) if prices else None,
        "average": round(mean(prices), 8) if prices else None,
        "first": prices[0] if prices else None,
        "last": prices[-1] if prices else None,
        "delta": round(price_delta, 8) if price_delta is not None else None,
        "delta_pct": round(price_delta_pct, 4) if price_delta_pct is not None else None,
    },
    "last_trade": timeline[-1] if timeline else None,
}

notes = []
if len(rows) == 0:
    notes.append("No paper trade rows found.")
if len(set(symbols)) == 1 and symbols:
    notes.append(f"Single-symbol paper trading detected: {symbols[0]}.")
if actions:
    action_counts = Counter(actions)
    notes.append("Action distribution: " + ", ".join(f"{k}={v}" for k, v in action_counts.items()))
if price_delta_pct is not None:
    direction = "up" if price_delta_pct > 0 else "down" if price_delta_pct < 0 else "flat"
    notes.append(f"Observed paper price movement from first to last row: {direction} {round(price_delta_pct, 4)}%.")
if not notes:
    notes.append("No notable paper-trading pattern detected yet.")

analysis["notes"] = notes

lines = []
lines.append("# EarnsAI Paper Trade Analysis v0.1")
lines.append("")
lines.append(f"- Generated at: {analysis['generated_at']}")
lines.append("- Phase: Phase 4 — Trading Research Lab")
lines.append("- Mode: read-only local analysis")
lines.append("- Network/API/live trading: disabled")
lines.append("- `.env` / credentials: not read")
lines.append("")
lines.append("## Summary")
lines.append("")
lines.append(f"- Source: `paper_trades.csv`")
lines.append(f"- Rows: `{analysis['rows']}`")
lines.append(f"- Columns: `{', '.join(fields) if fields else '-'}`")
lines.append("")
lines.append("## Symbol Frequency")
lines.append("")
if analysis["symbols"]:
    for k, v in analysis["symbols"].items():
        lines.append(f"- `{k}`: `{v}`")
else:
    lines.append("- No symbol data.")
lines.append("")
lines.append("## Action Frequency")
lines.append("")
if analysis["actions"]:
    for k, v in analysis["actions"].items():
        lines.append(f"- `{k}`: `{v}`")
else:
    lines.append("- No action data.")
lines.append("")
lines.append("## Price Summary")
lines.append("")
for k, v in analysis["price"].items():
    lines.append(f"- `{k}`: `{v}`")
lines.append("")
lines.append("## Last Trade")
lines.append("")
if analysis["last_trade"]:
    for k, v in analysis["last_trade"].items():
        lines.append(f"- `{k}`: `{v}`")
else:
    lines.append("- No last trade.")
lines.append("")
lines.append("## Research Notes")
lines.append("")
for note in notes:
    lines.append(f"- {note}")
lines.append("")
lines.append("## Next Safe Step")
lines.append("")
lines.append("Create a read-only backtest data inspector to summarize available local datasets before adding any strategy logic.")
lines.append("")

report = "\n".join(lines)

out_md.write_text(report, encoding="utf-8")
latest_md.write_text(report, encoding="utf-8")
out_json.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
latest_json.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Analysis markdown created: {out_md}")
print(f"Analysis json created: {out_json}")
print(f"Latest markdown updated: {latest_md}")
print(f"Latest json updated: {latest_json}")
print("")
print("Paper trade analysis result: PASSED")
PY
