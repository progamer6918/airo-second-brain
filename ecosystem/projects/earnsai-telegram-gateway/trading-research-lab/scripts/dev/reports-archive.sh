#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
ARCHIVE_DIR=".dev-archives/reports-archive-$TS"
MANIFEST="$ARCHIVE_DIR/MANIFEST.txt"

echo "== EarnsAI Reports Archive v0.1 =="
echo "Mode: local housekeeping"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$ARCHIVE_DIR" "$MANIFEST" <<'PY'
from pathlib import Path
import sys
import shutil
from datetime import datetime

reports = Path("reports")
archive = Path(sys.argv[1])
manifest = Path(sys.argv[2])

archive_reports = archive / "reports"
archive_reports.mkdir(parents=True, exist_ok=True)

if not reports.exists():
    print("reports/ missing, nothing to archive.")
    manifest.write_text("reports/ missing, nothing archived.\n", encoding="utf-8")
    print("Reports archive result: PASSED")
    raise SystemExit(0)

candidates = []
for path in reports.iterdir():
    if not path.is_file():
        continue
    name = path.name

    # Keep current pointers in place.
    if "LATEST" in name:
        continue

    # Archive generated reports/logs only.
    if path.suffix.lower() not in {".md", ".json", ".log"}:
        continue

    candidates.append(path)

lines = []
lines.append("EarnsAI Reports Archive Manifest")
lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append(f"Archive dir: {archive}")
lines.append("")
lines.append(f"Files archived: {len(candidates)}")
lines.append("")

for src in sorted(candidates):
    dst = archive_reports / src.name
    shutil.move(str(src), str(dst))
    lines.append(f"- {src} -> {dst}")

manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Archive dir: {archive}")
print(f"Manifest: {manifest}")
print(f"Files archived: {len(candidates)}")
print("")
print("Reports archive result: PASSED")
PY
