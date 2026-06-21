# AIRO Full Auto Asset Sync v1.2D Dedupe Key Fix

Status: patched.

## Bug

The v1.2B/v1.2C planner emitted asset duplicate keys with prefixes:

- `savings:sav_...`
- `gold:gold_...`

But the actual `🥇 Aset` ledger stores and exports the key header values directly:

- `savings_event_id`: `sav_...`
- `gold_event_id`: `gold_...`

This caused fresh snapshot verification to still classify the applied asset row as `insert_candidate`.

## Fix

Asset planner duplicate keys now match the actual sheet key columns exactly:

- savings duplicate key = `savings_event_id`
- gold duplicate key = `gold_event_id`

## Verified live row

The live row from `nabung 5000 ke blu` is:

- target tab: `🥇 Aset`
- section: `savings_transfer_ledger`
- savings_event_id: `sav_d78b1a231bb6`
- amount: `5000`
- row: 7
- key column: O
