# AIRO Full Auto Asset Sync v1.2B Integration

Status: patched and smoke-tested.

## Scope

Extends the full-auto Google Sheets pipeline to include `🥇 Aset`.

Integration path:

1. `airo_sheets_sync_dry_run.py`
   - loads `airo_asset_event_planner.py`
   - emits planned operations for `🥇 Aset`

2. `airo_sheets_sync_write_preview.py`
   - preserves `section`
   - checks section snapshot keys:
     - `🥇 Aset::savings_transfer_ledger`
     - `🥇 Aset::gold_ledger`

3. `airo_full_auto_sheets_sync.py`
   - allows `🥇 Aset` insert candidates
   - writes savings ledger rows to `🥇 Aset!O3:Z`
   - writes gold ledger rows to `🥇 Aset!A24:M`
   - keeps asset ledgers append-only in v1.2B

4. `airo_google_sheets_client.py`
   - exports asset section keys
   - supports append to explicit A1 range

## Safety

- No approval phrase is required.
- No Apps Script is required.
- No credential is stored in repo.
- Asset ledger update candidates are not auto-applied; only new insert candidates are written.

## Product rule

Gold/emas quantity is canonical in grams. Rupiah remains cost/modal.
