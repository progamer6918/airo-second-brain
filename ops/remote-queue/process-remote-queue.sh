#!/usr/bin/env bash

set -e

SHOW_HELP=false
DRY_RUN=false
JSON_MODE=false

for arg in "$@"; do
  case $arg in
    --help)
      SHOW_HELP=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --json)
      JSON_MODE=true
      shift
      ;;
  esac
done

if [ "$SHOW_HELP" = true ]; then
  if [ "$JSON_MODE" = true ]; then
    echo '{"help": "Usage: process-remote-queue.sh [--help] [--dry-run] [--json]"}'
  else
    echo "Usage: process-remote-queue.sh [--help] [--dry-run] [--json]"
    echo ""
    echo "Options:"
    echo "  --help     Show this help message"
    echo "  --dry-run  Simulate queue processing without moving files"
    echo "  --json     Output results in JSON format"
  fi
  exit 0
fi

QUEUE_DIR="inbox/remote"
PROPOSAL_DIR="distill/proposals"
EVENT_DIR="events/raw"

mkdir -p "$PROPOSAL_DIR" "$EVENT_DIR"

PROCESSED_COUNT=0
FILES_PROCESSED=()

shopt -s nullglob
for file in "$QUEUE_DIR"/*.md; do
  [ -e "$file" ] || continue
  filename=$(basename "$file")
  
  # Basic logic: simple moving to proposals to await owner review.
  dest="$PROPOSAL_DIR/$filename"
  
  if [ "$DRY_RUN" = false ]; then
    mv "$file" "$dest"
  fi
  
  FILES_PROCESSED+=("$filename")
  PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
done
shopt -u nullglob

if [ "$JSON_MODE" = true ]; then
  # Build JSON array for files
  FILES_JSON="["
  for i in "${!FILES_PROCESSED[@]}"; do
    FILES_JSON+="\"${FILES_PROCESSED[$i]}\""
    if [ $i -lt $((${#FILES_PROCESSED[@]}-1)) ]; then
      FILES_JSON+=", "
    fi
  done
  FILES_JSON+="]"

  cat <<EOF
{
  "success": true,
  "dry_run": $DRY_RUN,
  "processed_count": $PROCESSED_COUNT,
  "files_processed": $FILES_JSON,
  "message": "Processed $PROCESSED_COUNT remote queue items."
}
EOF
else
  if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN: Would have processed $PROCESSED_COUNT remote queue items."
  else
    echo "SUCCESS: Processed $PROCESSED_COUNT remote queue items."
  fi
  for f in "${FILES_PROCESSED[@]}"; do
    echo " - $f -> $PROPOSAL_DIR"
  done
fi
