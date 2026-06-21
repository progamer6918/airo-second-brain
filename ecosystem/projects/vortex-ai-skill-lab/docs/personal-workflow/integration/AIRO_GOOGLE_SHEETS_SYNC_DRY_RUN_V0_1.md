# AIRO Google Sheets Sync Dry-run Mapper v0.1

Status: IMPLEMENTED / DRY-RUN ONLY
Date: 2026-05-10
Script: `scripts/personal-workflow/airo_sheets_sync_dry_run.py`

## Purpose

This script reads the Airo Personal Workflow SQLite finance DB and builds planned Google Sheet operations in memory.

It performs:

- SQLite read-only mapping
- redacted JSON dry-run report
- duplicate key preview
- sync hash preview
- validation marker skip
- Review Queue routing preview
- Credit Card mirror row preview

It does not perform:

- Google Sheets write
- credential read
- OAuth read
- `.env` read
- DB mutation
- git staging of runtime/private files

## Default DB

`~/.local/share/airo-personal-workflow/airo.sqlite3`

## Current observed dry-run result

Latest successful run showed:

- `google_write_performed: false`
- `credentials_read: false`
- tables discovered: 9
- row counts:
  - `accounts`: 1
  - `transactions`: 1
  - `audit_log`: 2
  - all other finance sync target tables: 0
- planned operations:
  - `NO_WRITE`: 1
  - `skip_validation_marker`: 1

The current only transaction is a validation marker containing `validasi-persistent-db`, so it is intentionally skipped from Google Sheet finance sync.

## Mapping v0.1

### transactions

Primary target: `💸 Transactions`

Conditional mirror target: `💳 Credit Card` when one of the following contains Tokopedia Credit Card:

- merchant
- payment_method
- resolved account name

Review target: `🧾 Review Queue` for suspicious amount, missing category, unresolved account, or ambiguity.

Skip target: `NO_WRITE` for deleted rows and validation marker rows.

### approval_queue

Target: `🧾 Review Queue`

Rows from approval_queue are mapped into Review Queue with `sqlite_approval_queue` source.

### installment_payments

Target: `🏠 Cicilan Rumah`

Rows map into payment history.

### accounts

Used as lookup only in v0.1.

### audit_log

Counted for discovery only in v0.1.

### unsupported in v0.1

The current SQLite schema does not yet provide enough structured fields for these Google Sheet domains:

- Cash Ledger sessions and cash entries
- Hutang payments by person
- Aset Gold Ledger with grams and price
- Savings / Transfer Ledger with from/to account
- CC pocket allocation events

Those require parser/DB enrichment before production sync.

## Dedup strategy

Primary duplicate keys:

- Transactions: `transactions:<transaction_id>`
- Credit Card mirror: `credit_card:<transaction_id>`
- Review Queue from transaction: `review:transactions:<rowid>`
- Review Queue from approval queue: `review:approval_queue:<rowid>`
- Installment payment: `installment_payment:<payment_id>`

Sync hash uses stable business fields from source rows.

## Guardrails

- No Google write in v0.1.
- No credentials are read.
- Validation markers are skipped.
- Deleted rows are skipped.
- Suspicious amounts route to Review Queue.
- Restricted local paths are not touched.
- Runtime outputs are not committed.

## How to run

From repo root:

    python3 scripts/personal-workflow/airo_sheets_sync_dry_run.py

Optional DB override:

    python3 scripts/personal-workflow/airo_sheets_sync_dry_run.py --db "$HOME/.local/share/airo-personal-workflow/airo.sqlite3"

## Next official item

Sheet header read-only validation design.

This future phase may read Google Sheet headers only, but still must not write. Real write mode requires explicit approval gate:

`I APPROVE GOOGLE SHEETS WRITE FOR AIRO FINANCE`
