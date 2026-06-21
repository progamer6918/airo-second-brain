# AIRO Google Sheets write_preview v0.3

Status: IMPLEMENTED / NO WRITE
Date: 2026-05-10

## Artifacts

Python:

- scripts/personal-workflow/airo_sheets_sync_write_preview.py

Apps Script read-only exporter:

- scripts/personal-workflow/apps-script/airo_finance_sheet_key_exporter_v0_3.gs

## Purpose

write_preview compares SQLite dry-run planned operations against existing Google Sheet keys.

It determines:

- insert_candidate
- update_candidate
- skip_duplicate
- insert_review_candidate
- update_review_candidate
- dry-run skip actions such as skip_validation_marker

It performs no Google write.

## Current behavior

If no sheet snapshot is provided:

- existing keys are treated as empty
- this is valid for smoke testing
- no Google credentials are read

If a sheet snapshot JSON is provided:

- duplicate_key and sync_hash are compared against planned operations
- output shows insert/update/skip plan

## Sheet key exporter

The Apps Script exporter is read-only.

Function:

exportAiroFinanceSheetKeysV03

It reads keys from:

- 💸 Transactions
- 💳 Credit Card
- 🧾 Review Queue
- 🏠 Cicilan Rumah
- 🔄 Sync Log

It logs:

SHEET_KEYS_JSON={...}

The JSON can be copied to a local file and passed to Python with:

python3 scripts/personal-workflow/airo_sheets_sync_write_preview.py --sheet-snapshot /path/to/sheet_keys.json

## Safety

- no Google write
- no credential read
- no DB mutation
- no hard delete
- no restricted path touch
- no finance ledger write

## Next official item

Run Apps Script sheet key exporter, then run Python write_preview with that snapshot.
