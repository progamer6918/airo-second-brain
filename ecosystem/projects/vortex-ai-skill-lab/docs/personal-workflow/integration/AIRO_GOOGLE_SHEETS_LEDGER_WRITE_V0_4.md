# AIRO Google Sheets Ledger Write Skeleton v0.4

Status: IMPLEMENTED / SKELETON / NO WRITE
Date: 2026-05-10
Script: `scripts/personal-workflow/airo_sheets_ledger_write_v0_4.py`

## Purpose

This artifact establishes the write-mode structure before any real finance ledger write is implemented.

It is intentionally a skeleton:

- no Google API client
- no credential read
- no Google write
- no DB mutation
- no hard delete

## Why this exists

The project is now in batch-forward mode. Instead of waiting until the last minute to design write behavior, v0.4 creates the command structure and gate checks now.

This reduces future mistakes when real ledger write is added.

## Modes

### preview

Default.

Runs `airo_sheets_sync_write_preview.py` and returns a skeleton report.

### write

Requires exact approval phrase:

`I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE`

In v0.4, even write mode performs no Google write. It validates the gate and returns:

`NO_WRITE_IMPLEMENTED_IN_V0_4`

## Write scopes

Supported scope names for validation:

- `sync_log_only`
- `transactions_review_cc`

Real implementation is deferred.

## Current expected result

Because current SQLite contains only a validation marker row, v0.4 should report:

- source preview action: skip_validation_marker
- google_write_performed: false
- credentials_read: false
- real_write_implemented: false

## Next official item

Wait for real finance rows from Telegram/local parser, then rerun:

1. dry-run mapper
2. sheet key exporter
3. write_preview
4. ledger write skeleton preview

If real rows appear clean, implement real Google API client write mode in the next batch.
