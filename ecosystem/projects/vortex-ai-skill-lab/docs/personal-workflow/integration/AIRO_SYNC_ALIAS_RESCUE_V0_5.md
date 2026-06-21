# AIRO Sync Alias Rescue v0.5

Status: IMPLEMENTED / NO GOOGLE WRITE
Date: 2026-05-10

## Trigger

Runtime Telegram/Airo still responded:

`Sudah tercatat transaksi makanan sebesar Rp12.000 via akun belum ditentukan.`

for:

`catat beli makan siang 12000 pakai blubca`

even after the repo-level parser alias integration.

## Decision

Add alias rescue at the sync mapper layer too.

This allows sync/dry-run/write_preview to recover canonical account names from:

- payment_method
- account lookup name
- note/raw_text

even if the active Telegram runtime persisted the transaction with unresolved account.

## Canonical mapping

`blubca`, `blu`, `blu bca`, `blu-bca`, `blu_bca`, `bank blu`, and `bank blu bca` normalize to:

`BLU BCA`

## Artifact patched

- scripts/personal-workflow/airo_sheets_sync_dry_run.py

## Safety

- no Google write
- no credential read
- no DB mutation
- no service restart
- no restricted path touch

## Next official item

If alias rescue creates real write candidates, proceed to first ledger-write implementation design.

If candidate count remains zero, inspect whether the new Telegram captures are being persisted to SQLite at all.
