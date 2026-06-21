#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "== EarnsAI Command Layer Audit v0.1 =="
echo "Mode: local command integrity audit"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - <<'PY'
from pathlib import Path
import re
import sys
from collections import Counter

makefile = Path("Makefile")
scripts_dir = Path("scripts/dev")

expected_targets = [
    "status", "diagnose", "backup", "check", "smoke", "run", "logs", "checkpoint",
    "verify-v319", "diff-v319",
    "research-status", "research-report", "analyze-paper",
    "inspect-backtest", "summarize-datasets", "lab-index",
    "lab-health", "lab-refresh", "daily", "verify", "commands",
    "lab-latest", "reports-archive", "state-doctor", "command-audit",
]

expected_scripts = [
    "status.sh", "backup.sh", "check.sh", "smoke.sh", "run.sh", "logs.sh", "checkpoint.sh",
    "verify-v319.sh", "diff-v319.sh",
    "research-status.sh", "research-report.sh", "analyze-paper.sh",
    "inspect-backtest.sh", "summarize-datasets.sh", "lab-index.sh",
    "lab-health.sh", "lab-latest.sh", "reports-archive.sh", "state-doctor.sh",
    "command-audit.sh",
]

issues = []
warnings = []

if not makefile.exists():
    issues.append("Makefile missing")
else:
    text = makefile.read_text(encoding="utf-8", errors="ignore")
    raw_targets = re.findall(r"^([A-Za-z0-9_.-]+):", text, flags=re.MULTILINE)

    # Exclude Make special targets such as .PHONY from duplicate target audit.
    targets = [t for t in raw_targets if not t.startswith(".")]

    for target in expected_targets:
        if target not in targets:
            warnings.append(f"missing Makefile target: {target}")

    counts = Counter(targets)
    duplicates = sorted([t for t, c in counts.items() if c > 1])
    for target in duplicates:
        warnings.append(f"duplicate Makefile target detected: {target}")

if not scripts_dir.exists():
    issues.append("scripts/dev directory missing")
else:
    unsafe_patterns = [
        "cat" + " .env",
        "source" + " .env",
        ". " + ".env",
    ]

    for script in expected_scripts:
        path = scripts_dir / script
        if not path.exists():
            warnings.append(f"missing script: {path}")
        elif not path.stat().st_mode & 0o111:
            warnings.append(f"script not executable: {path}")

    for path in scripts_dir.glob("*.sh"):
        script_text = path.read_text(encoding="utf-8", errors="ignore")

        for pattern in unsafe_patterns:
            if pattern in script_text:
                issues.append(f"unsafe .env access pattern `{pattern}` in {path}")

health = "FAIL" if issues else ("WARN" if warnings else "PASS")

print(f"Health: {health}")
print("")
print("Issues:")
if issues:
    for x in issues:
        print(f"  - {x}")
else:
    print("  - none")

print("")
print("Warnings:")
if warnings:
    for x in warnings:
        print(f"  - {x}")
else:
    print("  - none")

print("")
print(f"Command audit result: {health}")

if health == "FAIL":
    sys.exit(1)

PY
