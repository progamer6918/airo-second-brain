#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date '+%Y-%m-%d %H:%M:%S')"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"

cat >> CHECKPOINT.md <<EOF2

## Checkpoint — $TS

- Phase: Phase 4 — Trading Research Lab
- Stable version: EarnsAI Pulse v3.1.9 — Sequential Handler Mode VERIFIED
- Progress project: 53/100
- Branch: $BRANCH
- Commit: $COMMIT
- Note: Dev Command Layer v0.1 available.

EOF2

echo "Checkpoint appended to CHECKPOINT.md"
