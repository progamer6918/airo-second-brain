#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI v3.1.9 Safe Diff Guard =="
echo "Mode: offline/local only"
echo "Purpose: compare active bot with verified v3.1.9 checkpoint"
echo ""

ACTIVE_BOT="simple_pulse_bot.py"
V319_BOT="checkpoints/simple_pulse_bot_v3_1_9_sequential_handler_verified.py"

[ -f "$ACTIVE_BOT" ] || { echo "FAILED: $ACTIVE_BOT missing"; exit 1; }
[ -f "$V319_BOT" ] || { echo "FAILED: $V319_BOT missing"; exit 1; }

python3 - <<'PY'
from pathlib import Path
import hashlib
import difflib
import re

active = Path("simple_pulse_bot.py")
verified = Path("checkpoints/simple_pulse_bot_v3_1_9_sequential_handler_verified.py")

def sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]

def redact(line: str) -> str:
    patterns = [
        r'(?i)(token\s*=\s*)["\'][^"\']+["\']',
        r'(?i)(api[_-]?key\s*=\s*)["\'][^"\']+["\']',
        r'(?i)(secret\s*=\s*)["\'][^"\']+["\']',
        r'(?i)(password\s*=\s*)["\'][^"\']+["\']',
        r'(?i)(private[_-]?key\s*=\s*)["\'][^"\']+["\']',
    ]
    out = line
    for pattern in patterns:
        out = re.sub(pattern, r'\1"***REDACTED***"', out)
    return out

active_sha = sha16(active)
verified_sha = sha16(verified)

print(f"active sha16:   {active_sha}")
print(f"verified sha16: {verified_sha}")
print("")

if active_sha == verified_sha:
    print("OK: active bot matches verified v3.1.9 checkpoint")
    print("Diff result: clean")
    raise SystemExit(0)

print("WARNING: active bot differs from verified v3.1.9 checkpoint")
print("Showing safe redacted unified diff, max 220 lines.")
print("")

active_lines = active.read_text(encoding="utf-8", errors="ignore").splitlines()
verified_lines = verified.read_text(encoding="utf-8", errors="ignore").splitlines()

diff = difflib.unified_diff(
    verified_lines,
    active_lines,
    fromfile="checkpoint_v3_1_9_verified",
    tofile="active_simple_pulse_bot",
    lineterm="",
)

count = 0
for line in diff:
    print(redact(line))
    count += 1
    if count >= 220:
        print("")
        print("[TRUNCATED] Diff is longer than 220 lines.")
        break

print("")
print("Diff guard completed with differences detected.")
PY
