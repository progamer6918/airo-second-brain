#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_MD="reports/state_doctor_$TS.md"
OUT_JSON="reports/state_doctor_$TS.json"
LATEST_MD="reports/STATE_DOCTOR_LATEST.md"
LATEST_JSON="reports/STATE_DOCTOR_LATEST.json"

echo "== EarnsAI State Doctor v0.1 =="
echo "Mode: read-only local state diagnosis"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$OUT_MD" "$OUT_JSON" "$LATEST_MD" "$LATEST_JSON" <<'PY'
from pathlib import Path
import json, sys
from datetime import datetime

out_md = Path(sys.argv[1])
out_json = Path(sys.argv[2])
latest_md = Path(sys.argv[3])
latest_json = Path(sys.argv[4])

def load_json(name):
    p = Path(name)
    if not p.exists():
        return None, "missing"
    try:
        return json.loads(p.read_text(encoding="utf-8")), "ok"
    except Exception as e:
        return None, f"invalid: {e}"

def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)

trading, trading_status = load_json("trading_data.json")
snapshot, snapshot_status = load_json("portfolio_snapshot.json")
trade_log, trade_log_status = load_json("trade_log.json")

oks, warnings, issues = [], [], []

if trading_status != "ok" or not isinstance(trading, dict):
    issues.append(f"trading_data.json status: {trading_status}")
else:
    oks.append("trading_data.json valid dict")
    for k in ["balance_usdt", "balance_btc", "entry_price", "last_price"]:
        if k not in trading:
            issues.append(f"missing trading_data key: {k}")
        elif not is_num(trading[k]):
            warnings.append(f"trading_data `{k}` is not numeric")
    if trading.get("last_price") in [0, 0.0, None, "0", "0.0"]:
        warnings.append("last_price is zero/empty; price feed/state may be inactive or stale")
    if trading.get("last_feed_error"):
        warnings.append(f"last_feed_error present: {trading.get('last_feed_error')}")

if snapshot_status != "ok" or not isinstance(snapshot, dict):
    warnings.append(f"portfolio_snapshot.json status: {snapshot_status}")
else:
    oks.append("portfolio_snapshot.json valid dict")
    if "trading_data" not in snapshot:
        warnings.append("snapshot missing embedded trading_data")
    if "trade_log" not in snapshot:
        warnings.append("snapshot missing embedded trade_log")

if trade_log_status != "ok" or not isinstance(trade_log, list):
    warnings.append(f"trade_log.json status: {trade_log_status}")
else:
    oks.append(f"trade_log.json valid list rows={len(trade_log)}")
    if len(trade_log) == 0:
        warnings.append("trade_log.json has zero rows; current activity evidence may be from paper_trades.csv only")

health = "FAIL" if issues else ("WARN" if warnings else "PASS")

result = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "phase": "Phase 4 — Trading Research Lab",
    "baseline": "EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED",
    "mode": "read-only local state diagnosis",
    "health": health,
    "oks": oks,
    "warnings": warnings,
    "issues": issues,
}

lines = [
    "# EarnsAI State Doctor v0.1",
    "",
    f"- Generated at: {result['generated_at']}",
    f"- Health: `{health}`",
    "- Mode: read-only local state diagnosis",
    "- Network/API/live trading: disabled",
    "- `.env` / credentials: not read",
    "",
    "## OK",
    "",
]
lines += [f"- {x}" for x in oks] or ["- No OK checks recorded."]
lines += ["", "## Warnings", ""]
lines += [f"- {x}" for x in warnings] or ["- No warnings."]
lines += ["", "## Issues", ""]
lines += [f"- {x}" for x in issues] or ["- No blocking issues."]
lines += ["", "## Result", ""]
lines.append("State doctor passed with warnings." if health == "WARN" else f"State doctor result: {health}")

report = "\n".join(lines) + "\n"

out_md.write_text(report, encoding="utf-8")
latest_md.write_text(report, encoding="utf-8")
out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
latest_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"State doctor markdown created: {out_md}")
print(f"State doctor json created: {out_json}")
print(f"Latest markdown updated: {latest_md}")
print(f"Latest json updated: {latest_json}")
print("")
print(f"State doctor result: {health}")

if health == "FAIL":
    raise SystemExit(1)
PY
