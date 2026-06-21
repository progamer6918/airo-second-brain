#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Research Lab Status v0.1 =="
echo "Mode: read-only local analysis"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - <<'PY'
from pathlib import Path
import json
import csv
from datetime import datetime

ROOT = Path(".")

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
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    text = str(value)
    if len(text) > 80:
        return text[:77] + "..."
    return text

def load_json(path):
    if not path.exists():
        return None, "missing"
    if path.stat().st_size > 10 * 1024 * 1024:
        return None, "skipped: file larger than 10MB"
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), "ok"
    except Exception as e:
        return None, f"invalid: {e}"

def describe_json(path):
    data, status = load_json(path)
    print(f"- {path}: {status}")

    if status != "ok":
        return

    if isinstance(data, dict):
        print(f"  type: dict")
        print(f"  top-level keys: {', '.join(map(str, list(data.keys())[:15])) or '(empty)'}")

        interesting = [
            "balance", "cash", "equity", "portfolio", "positions",
            "symbol", "price", "last_price", "signal", "status",
            "updated_at", "timestamp"
        ]

        for key in interesting:
            if key in data:
                print(f"  {key}: {safe_value(key, data[key])}")

        if "positions" in data:
            positions = data.get("positions")
            if isinstance(positions, dict):
                print(f"  positions_count: {len(positions)}")
            elif isinstance(positions, list):
                print(f"  positions_count: {len(positions)}")

    elif isinstance(data, list):
        print(f"  type: list")
        print(f"  rows: {len(data)}")

        if data:
            last = data[-1]
            if isinstance(last, dict):
                allowed = [
                    "time", "timestamp", "datetime", "symbol", "side",
                    "action", "qty", "quantity", "price", "pnl", "profit",
                    "status", "reason"
                ]
                summary = {
                    k: safe_value(k, last.get(k))
                    for k in allowed
                    if k in last
                }
                print(f"  last_row_summary: {summary if summary else '(no standard trade fields)'}")
            else:
                print(f"  last_row_type: {type(last).__name__}")
    else:
        print(f"  type: {type(data).__name__}")

def describe_csv(path):
    if not path.exists():
        print(f"- {path}: missing")
        return

    if path.stat().st_size > 10 * 1024 * 1024:
        print(f"- {path}: skipped, file larger than 10MB")
        return

    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"- {path}: invalid CSV: {e}")
        return

    print(f"- {path}: ok")
    print(f"  rows: {len(rows)}")
    print(f"  columns: {', '.join(reader.fieldnames or [])}")

    if rows:
        last = rows[-1]
        allowed = [
            "time", "timestamp", "datetime", "symbol", "side",
            "action", "qty", "quantity", "price", "pnl", "profit",
            "status", "reason"
        ]
        summary = {
            k: safe_value(k, last.get(k))
            for k in allowed
            if k in last
        }
        print(f"  last_row_summary: {summary if summary else '(no standard trade fields)'}")

print("Research data files:")
for file_name in [
    "trading_data.json",
    "portfolio_snapshot.json",
    "trade_log.json",
]:
    describe_json(ROOT / file_name)

print("")
print("Paper trading CSV:")
describe_csv(ROOT / "paper_trades.csv")

print("")
print("Research folders:")
for folder_name in ["data", "backtest", "paper-trading", "docs", "checkpoints"]:
    path = ROOT / folder_name
    if path.exists() and path.is_dir():
        files = [p for p in path.rglob("*") if p.is_file()]
        print(f"- {folder_name}/: exists, files={len(files)}")
    else:
        print(f"- {folder_name}/: missing")

print("")
print("Research status result: PASSED")
print("Generated at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
PY
