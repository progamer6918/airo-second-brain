#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI v3.1.9 Milestone Verification =="
echo "Mode: offline/local only"
echo "Network/API/live trading: disabled"
echo ""

ACTIVE_BOT="simple_pulse_bot.py"
V319_BOT="checkpoints/simple_pulse_bot_v3_1_9_sequential_handler_verified.py"
V319_CHECKPOINT="checkpoints/CHECKPOINT_v3_1_9_VERIFIED.md"

fail() {
  echo "FAILED: $1"
  exit 1
}

warn() {
  echo "WARNING: $1"
}

ok() {
  echo "OK: $1"
}

echo "1) Required milestone files"
[ -f "$ACTIVE_BOT" ] || fail "$ACTIVE_BOT missing"
[ -f "$V319_BOT" ] || fail "$V319_BOT missing"
[ -f "$V319_CHECKPOINT" ] || fail "$V319_CHECKPOINT missing"

ok "$ACTIVE_BOT exists"
ok "$V319_BOT exists"
ok "$V319_CHECKPOINT exists"

echo ""
echo "2) Python syntax verification"
python3 - <<PY
import py_compile

files = [
    "$ACTIVE_BOT",
    "$V319_BOT",
]

for f in files:
    py_compile.compile(f, doraise=True)
    print(f"OK: {f} compiles")
PY

echo ""
echo "3) State JSON integrity"
python3 - <<'PY'
import json
from pathlib import Path

files = [
    "trading_data.json",
    "portfolio_snapshot.json",
    "trade_log.json",
]

for name in files:
    path = Path(name)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            json.load(f)
        print(f"OK: {name} valid JSON")
    else:
        print(f"WARNING: {name} missing")
PY

echo ""
echo "4) Sequential handler signal scan"
python3 - <<'PY'
from pathlib import Path

targets = {
    "active": Path("simple_pulse_bot.py"),
    "checkpoint_v319": Path("checkpoints/simple_pulse_bot_v3_1_9_sequential_handler_verified.py"),
}

signals = [
    "sequential",
    "handler",
    "lock",
    "queue",
    "asyncio",
    "await",
]

for label, path in targets.items():
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    found = [s for s in signals if s in text]
    print(f"{label}: {path}")
    print(f"  signals: {', '.join(found) if found else 'none'}")
    if label == "checkpoint_v319" and not {"sequential", "handler"}.intersection(found):
        raise SystemExit("FAILED: v3.1.9 checkpoint lacks sequential/handler signal")
PY

echo ""
echo "5) Active file vs verified checkpoint fingerprint"
python3 - <<'PY'
from pathlib import Path
import hashlib

active = Path("simple_pulse_bot.py")
verified = Path("checkpoints/simple_pulse_bot_v3_1_9_sequential_handler_verified.py")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]

active_sha = sha(active)
verified_sha = sha(verified)

print(f"active sha16:   {active_sha}")
print(f"verified sha16: {verified_sha}")

if active_sha == verified_sha:
    print("OK: active bot matches verified v3.1.9 checkpoint")
else:
    print("WARNING: active bot differs from verified v3.1.9 checkpoint")
    print("This is not automatically fatal, but next patch must inspect the diff first.")
PY

echo ""
echo "v3.1.9 verification completed."
