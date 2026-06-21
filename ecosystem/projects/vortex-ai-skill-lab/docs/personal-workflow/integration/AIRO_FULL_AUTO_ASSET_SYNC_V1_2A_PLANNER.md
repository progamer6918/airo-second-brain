# AIRO Full Auto Asset Sync v1.2A Planner

Status: PASS-ready planner patch.

## Scope

Adds pure planner support for the Google Sheet tab `🥇 Aset`.

Covered sections:

- `savings_transfer_ledger`
- `gold_ledger`

No Google write is performed by this patch.

## Product rules

Savings/tabungan is event-ledger based, not direct balance overwrite.

Gold/emas uses gram as canonical asset quantity. Rupiah is cost/modal when purchase happens. Current value may fluctuate, but owned gram must stay stable.

## Supported examples

Savings:

- `nabung 5 juta ke blu`
- `transfer 1 juta dari bca ke blu`
- `tarik 500rb dari blu ke cash`

Gold:

- `beli emas 1 gram ...`

## Output contract

Every planned event returns:

- `target_tab`: `🥇 Aset`
- `section`: `savings_transfer_ledger` or `gold_ledger`
- `duplicate_key`
- `sync_hash`
- `row`

Savings row headers:

`savings_event_id, date, type, from_account, to_account, purpose, amount, source, raw_text, linked_transaction_id, sync_hash, notes`

Gold row headers:

`gold_event_id, date, action, grams_in, grams_out, price_per_gram, fee, total_amount, source_account, source, raw_text, sync_hash, notes`

## Safety

This planner performs:

- no SQLite reads
- no Google reads
- no Google writes
- no credential/env/token reads
- no Apps Script dependency

## Next

Patch v1.2B should integrate the planner into `airo_full_auto_sheets_sync.py` after inspecting the current operation/write-candidate shape.

Expected integration:

1. Existing SQLite transaction rows are loaded by current full-auto code.
2. Rows are passed to `plan_asset_events_from_transactions`.
3. Savings rows append to `🥇 Aset` savings ledger section.
4. Gold rows append to `🥇 Aset` gold ledger section after live header confirmation for row 24.
5. Duplicate checks use `duplicate_key` and/or `sync_hash`.
6. Approval phrase remains unused.
