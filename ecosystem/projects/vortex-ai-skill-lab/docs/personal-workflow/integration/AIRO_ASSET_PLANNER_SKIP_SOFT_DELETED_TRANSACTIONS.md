# AIRO Asset Planner Skip Soft-Deleted Transactions

Status: patched.

## Bug

Duplicate Telegram smoke rows for `nabung 5000 ke blu` were soft-deleted in SQLite, but the asset planner still generated `🥇 Aset` rows for them.

The previous dry-run guard only skipped deleted rows in `plan_transaction()`. Asset ledger planning uses `airo_asset_event_planner.py`, so it needed its own deleted-row guard.

## Fix

- `airo_sheets_sync_dry_run.py` skips deleted rows in `plan_transaction()`.
- `airo_asset_event_planner.py` skips deleted rows in `_plan_row()`.
- Duplicate smoke rows were reconciled, keeping original linked transaction `trx_a8ad5c2eec99`.

## Validation

Expected after fix:

- exactly one `nabung 5000 ke blu` asset candidate from current DB
- amount remains `5000`
- linked transaction remains `trx_a8ad5c2eec99`
- live dry-run should return `skip_duplicate`

## Live Sheet sync hash update pending

After normalizing the kept transaction from `uncategorized` to `tabungan`, the live Sheet row for `sav_d78b1a231bb6` may show `update_candidate` because its stored `sync_hash` differs from the newly planned hash.

This is expected and should be inspected before apply. Do not re-enable the timer until the candidate list is reviewed.
