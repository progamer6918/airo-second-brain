# AIRO Full Auto Sheets Sync v1.1

Status: IMPLEMENTED / CORE AUTO-SYNC READY
Date: 2026-05-10

## Goal

Replace one-off Apps Script writers with a Python full-auto core sync pipeline.

Final flow:

Telegram -> SQLite -> write_preview -> Google Sheets

No per-write approval phrase.

## Scope v1.1

Auto-sync write targets:

- 💸 Transactions
- 💳 Credit Card
- 🔄 Sync Log

Supported behavior:

- live Google key export
- write_preview decisioning
- insert candidates
- update candidates
- idempotent skip decisions
- Sync Log audit rows
- systemd timer template

## Not yet generalized in v1.1

The following are not yet full-auto write targets:

- 🧾 Review Queue
- 💵 Cash Ledger
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🥇 Aset
- 📅 Monthly Review

## Scripts

Google client:

- scripts/personal-workflow/airo_google_sheets_client.py

Full auto sync:

- scripts/personal-workflow/airo_full_auto_sheets_sync.py

Systemd templates:

- ops/personal-workflow/systemd/airo-full-auto-sheets-sync.service
- ops/personal-workflow/systemd/airo-full-auto-sheets-sync.timer
- ops/personal-workflow/systemd/sheets-sync.env.example

## One-time setup

Required environment:

- AIRO_SPREADSHEET_ID
- AIRO_GOOGLE_SERVICE_ACCOUNT_JSON_PATH or AIRO_GOOGLE_SERVICE_ACCOUNT_JSON

Required Python dependencies for live Google access:

python3 -m pip install --user google-api-python-client google-auth

## Usage

Dry-run with live Google key export:

python3 scripts/personal-workflow/airo_full_auto_sheets_sync.py --mode dry-run

Apply/write mode:

python3 scripts/personal-workflow/airo_full_auto_sheets_sync.py --mode apply

## Safety by design

No approval phrase is required.

Idempotency is still enforced by:

- duplicate_key for 💸 Transactions
- linked_txn_id for 💳 Credit Card
- Sync Log audit rows

## Next official item

Connect Google credentials once, run dry-run live, then run apply once manually. After PASS, install the systemd timer.

## v1.1.1 smoke hardening

Status: IMPLEMENTED / VERIFIED

Added `--report-out` and validated final report fields directly:

- mode=dry-run
- google_write_performed=false
- approval_phrase_required=false
- write_candidate_count=0

## v1.1.2 OAuth support

Status: IMPLEMENTED / READY FOR LIVE OAUTH LOGIN

Service account key creation was blocked by `iam.disableServiceAccountKeyCreation`, so AIRO now supports OAuth Desktop Client auth.

Env vars:

- AIRO_GOOGLE_OAUTH_CLIENT_SECRET_PATH
- AIRO_GOOGLE_OAUTH_TOKEN_PATH

First live run opens a one-time OAuth browser flow. Future full-auto runs reuse the local token.

## v1.1.3 live dry-run PASS

Status: PASS

OAuth token was created successfully and live dry-run read the real Google Sheet.

Verified:

- google_read_performed=true
- google_write_performed=false
- approval_phrase_required=false
- write_candidate_count=0

The systemd service was patched to use `AIRO_SYNC_PYTHON` from the local venv.

## v1.1.4 timer PASS

Status: PASS

Full-auto core sync is confirmed working.

Verified:

- Telegram transaction captured to SQLite.
- systemd timer runs apply mode automatically.
- new BLU BCA transaction `trx_f2884e451cd1` became `skip_duplicate` in live verification.
- write_candidate_count=0 after timer.
- approval_phrase_required=false.

Core full-auto scope confirmed:

- 💸 Transactions
- 💳 Credit Card
- 🔄 Sync Log
