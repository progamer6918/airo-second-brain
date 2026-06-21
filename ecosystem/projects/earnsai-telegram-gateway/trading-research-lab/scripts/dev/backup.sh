#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT=".dev-backups/source-snapshot-$TS.tar.gz"
mkdir -p .dev-backups

tar \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.*' \
  --exclude='node_modules' \
  --exclude='dist' \
  --exclude='build' \
  --exclude='__pycache__' \
  --exclude='.dev-backups' \
  -czf "$OUT" .

echo "Backup created: $OUT"
echo "Note: .env and credential-like files were excluded."
