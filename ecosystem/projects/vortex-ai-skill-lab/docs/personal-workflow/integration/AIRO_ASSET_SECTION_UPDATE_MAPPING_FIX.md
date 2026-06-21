# AIRO Asset Section Update Mapping Fix

Status: patched.

## Bug

The live snapshot stores asset section keys under section-specific snapshot keys, for example:

- `🥇 Aset::savings_transfer_ledger`

But `find_existing_row()` looked only under:

- `🥇 Aset`

As a result, asset update candidates could not find existing rows and fell back to append behavior.

## Fix

- `find_existing_row()` now accepts `section` and maps asset sections to snapshot keys.
- Savings ledger updates write to `O{row}:Z{row}`.
- Gold ledger updates write to `A{row}:M{row}`.
- Asset `update_candidate` is included in the apply write decision filter.
- Asset update refuses `insert_fallback` if an existing row cannot be found.

## Validation

The expected target row is:

- `sav_d78b1a231bb6`
- `🥇 Aset::savings_transfer_ledger`
- range `O{row}:Z{row}`

After apply, the targeted transaction and asset rows should both return `skip_duplicate`.
