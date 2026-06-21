#!/usr/bin/env python3
from pathlib import Path
import sys

required_files = [
    "docs/OPERATOR_GUIDE.md",
    "docs/SAFETY_GUIDE.md",
    "docs/COMMAND_REFERENCE.md",
    "docs/PHASE9_STATUS.md",
    "CHECKPOINT_PHASE9E.md",
]

required_terms = [
    "PAPER_ONLY",
    "LIVE_TRADING_LOCKED=true",
    "private_exchange_api=disabled",
    "HOLD",
    "BLOCKED",
]

unsafe_terms = [
    "LIVE_TRADING_LOCKED=false",
    "live_trading=true",
    "real_money_execution=enabled",
    "dry_run=false",
]

combined = ""

for file in required_files:
    path = Path(file)
    if not path.exists():
        print(f"PHASE9E_SMOKE FAIL missing {file}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 80:
        print(f"PHASE9E_SMOKE FAIL short {file}")
        sys.exit(1)

    combined += text + "\n"

lower = combined.lower()

for term in required_terms:
    if term.lower() not in lower:
        print(f"PHASE9E_SMOKE FAIL missing {term}")
        sys.exit(1)

for term in unsafe_terms:
    if term.lower() in lower:
        print(f"PHASE9E_SMOKE FAIL unsafe {term}")
        sys.exit(1)

makefile = Path("Makefile").read_text(encoding="utf-8")

for target in ["phase9e-smoke:", "phase9e-gate:"]:
    if target not in makefile:
        print(f"PHASE9E_SMOKE FAIL missing {target}")
        sys.exit(1)

print("PHASE9E_SMOKE PASS")
