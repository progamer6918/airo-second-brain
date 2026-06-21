#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT="reports/research_report_$TS.md"
LATEST="reports/RESEARCH_REPORT_LATEST.md"

echo "== EarnsAI Research Report v0.1 =="
echo "Mode: local report generation"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT" "$LATEST" <<'PY'
from pathlib import Path
import json
import csv
import sys
from datetime import datetime
from statistics import mean

out = Path(sys.argv[1])
latest = Path(sys.argv[2])

SENSITIVE_HINTS = {
    "token", "secret", "password", "passwd", "api_key", "apikey",
    "private_key", "authorization", "credential", "bearer"
}

def is_sensitive_key(key):
    k = str(key).lower()
    return any(h in k for h in SENSITIVE_HINTS)

def safe_value(key, value):
    if is_sensitive_key(key):
        return "***REDACTED***"
    if isinstance(value, dict):
        return f"dict(keys={len(value)})"
    if isinstance(value, list):
        return f"list(rows={len(value)})"
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    text = str(value)
    return text if len(text) <= 100 else text[:97] + "..."

def load_json(name):
    path = Path(name)
    if not path.exists():
        return None, "missing"
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), "ok"
    except Exception as e:
        return None, f"invalid: {e}"

def load_csv(name):
    path = Path(name)
    if not path.exists():
        return [], [], "missing"
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fields = reader.fieldnames or []
        return rows, fields, "ok"
    except Exception as e:
        return [], [], f"invalid: {e}"

def get_case(row, *names):
    lower = {str(k).lower(): v for k, v in row.items()}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return None

def as_float(v):
    try:
        if v is None or str(v).strip() == "":
            return None
        return float(str(v).replace(",", ""))
    except Exception:
        return None

trading_data, trading_status = load_json("trading_data.json")
portfolio, portfolio_status = load_json("portfolio_snapshot.json")
trade_log, trade_log_status = load_json("trade_log.json")
paper_rows, paper_fields, paper_status = load_csv("paper_trades.csv")

lines = []
lines.append("# EarnsAI Research Report v0.1")
lines.append("")
lines.append(f"- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append("- Phase: Phase 4 — Trading Research Lab")
lines.append("- Baseline: EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED")
lines.append("- Mode: local/offline analysis only")
lines.append("- Network/API/live trading: disabled")
lines.append("- `.env` / credentials: not read")
lines.append("")

lines.append("## 1. Data Health")
lines.append("")
lines.append("| File | Status | Summary |")
lines.append("|---|---:|---|")

def json_summary(data):
    if isinstance(data, dict):
        return f"dict, keys={len(data)}"
    if isinstance(data, list):
        return f"list, rows={len(data)}"
    if data is None:
        return "-"
    return type(data).__name__

lines.append(f"| `trading_data.json` | {trading_status} | {json_summary(trading_data)} |")
lines.append(f"| `portfolio_snapshot.json` | {portfolio_status} | {json_summary(portfolio)} |")
lines.append(f"| `trade_log.json` | {trade_log_status} | {json_summary(trade_log)} |")
lines.append(f"| `paper_trades.csv` | {paper_status} | rows={len(paper_rows)}, columns={len(paper_fields)} |")
lines.append("")

lines.append("## 2. Trading State Snapshot")
lines.append("")
if isinstance(trading_data, dict):
    for key in [
        "balance_usdt", "balance_btc", "entry_price", "last_price",
        "last_price_source", "last_price_updated", "last_feed_error"
    ]:
        if key in trading_data:
            lines.append(f"- `{key}`: `{safe_value(key, trading_data.get(key))}`")
else:
    lines.append("- Trading state unavailable.")
lines.append("")

lines.append("## 3. Portfolio Snapshot")
lines.append("")
if isinstance(portfolio, dict):
    for key in ["timestamp", "bot_version", "created_by"]:
        if key in portfolio:
            lines.append(f"- `{key}`: `{safe_value(key, portfolio.get(key))}`")
    if "trading_data" in portfolio:
        lines.append("- `trading_data`: embedded snapshot detected")
    if "trade_log" in portfolio:
        val = portfolio.get("trade_log")
        if isinstance(val, list):
            lines.append(f"- `trade_log`: embedded rows={len(val)}")
        else:
            lines.append(f"- `trade_log`: {safe_value('trade_log', val)}")
else:
    lines.append("- Portfolio snapshot unavailable.")
lines.append("")

lines.append("## 4. Trade Log Summary")
lines.append("")
if isinstance(trade_log, list):
    lines.append(f"- Root `trade_log.json` rows: `{len(trade_log)}`")
    if trade_log:
        last = trade_log[-1]
        if isinstance(last, dict):
            lines.append("- Last trade summary:")
            for key in ["timestamp", "time", "symbol", "side", "action", "qty", "quantity", "price", "pnl", "status", "reason"]:
                if key in last:
                    lines.append(f"  - `{key}`: `{safe_value(key, last.get(key))}`")
    else:
        lines.append("- No active trade rows found in root trade log.")
else:
    lines.append("- Trade log unavailable or not a list.")
lines.append("")

lines.append("## 5. Paper Trading CSV Summary")
lines.append("")
if paper_status == "ok":
    lines.append(f"- Rows: `{len(paper_rows)}`")
    lines.append(f"- Columns: `{', '.join(paper_fields) if paper_fields else '-'}`")

    symbols = []
    actions = []
    prices = []

    for row in paper_rows:
        symbol = get_case(row, "symbol")
        action = get_case(row, "action", "side")
        price = as_float(get_case(row, "price"))

        if symbol:
            symbols.append(symbol)
        if action:
            actions.append(action)
        if price is not None:
            prices.append(price)

    if symbols:
        lines.append(f"- Symbols: `{', '.join(sorted(set(symbols)))}`")
    if actions:
        lines.append(f"- Actions: `{', '.join(sorted(set(actions)))}`")
    if prices:
        lines.append(f"- Price min: `{min(prices)}`")
        lines.append(f"- Price max: `{max(prices)}`")
        lines.append(f"- Price average: `{round(mean(prices), 6)}`")
        lines.append(f"- Last price in CSV: `{prices[-1]}`")

    if paper_rows:
        last = paper_rows[-1]
        lines.append("- Last paper trade row:")
        for key in paper_fields:
            if str(key).lower() in {"timestamp", "time", "datetime", "symbol", "action", "side", "price", "qty", "quantity", "status"}:
                lines.append(f"  - `{key}`: `{safe_value(key, last.get(key))}`")
else:
    lines.append(f"- Paper trading CSV status: `{paper_status}`")
lines.append("")

lines.append("## 6. Research Notes")
lines.append("")
notes = []

if isinstance(trading_data, dict):
    last_price = trading_data.get("last_price")
    if last_price in (0, 0.0, "0", "0.0", None):
        notes.append("`last_price` is zero or empty, so price feed/state should be treated as inactive or stale until verified.")

if isinstance(trade_log, list) and len(trade_log) == 0:
    notes.append("Root `trade_log.json` has zero rows; current evidence of activity is mainly from `paper_trades.csv`.")

if paper_status == "ok" and len(paper_rows) > 0:
    notes.append("Paper trading data exists and can be used for early Research Lab reporting.")

if not notes:
    notes.append("No major local data warning detected.")

for note in notes:
    lines.append(f"- {note}")

lines.append("")
lines.append("## 7. Next Safe Step")
lines.append("")
lines.append("Recommended next step: create a read-only paper-trade analyzer that summarizes action frequency and basic price movement without touching exchange APIs or credentials.")
lines.append("")

report = "\n".join(lines)
out.write_text(report, encoding="utf-8")
latest.write_text(report, encoding="utf-8")

print(f"Report created: {out}")
print(f"Latest report updated: {latest}")
print("")
print("Research report result: PASSED")
PY
