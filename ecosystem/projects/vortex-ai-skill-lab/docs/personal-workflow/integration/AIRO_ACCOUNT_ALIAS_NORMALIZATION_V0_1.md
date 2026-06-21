# AIRO Account Alias Normalization v0.1

Status: IMPLEMENTED AS NORMALIZATION MODULE
Date: 2026-05-10

## Trigger

User sent:

`catat beli makan siang 12000 pakai blubca`

Airo replied:

`Sudah tercatat transaksi makanan sebesar Rp12.000 via akun belum ditentukan.`

This means the parser recognized the transaction category/amount but failed to map `blubca` to the canonical account `BLU BCA`.

## Canonical decision

Canonical account name:

`BLU BCA`

Accepted aliases:

- `blu`
- `blubca`
- `blu bca`
- `blu-bca`
- `blu_bca`
- `bank blu`
- `bank blu bca`

## Artifact

Module:

`scripts/personal-workflow/airo_account_aliases.py`

Tests:

`tests/personal-workflow/test_airo_account_aliases.py`

## Expected behavior

Input:

`catat beli makan siang 12000 pakai blubca`

Expected account:

`BLU BCA`

Input:

`catat beli makan siang 12000 pakai blu`

Expected account:

`BLU BCA`

## Integration note

This module is implemented as a parser-support artifact.

Next parser integration should import/use:

- `normalize_account_alias`
- `extract_account_from_text`

in the Telegram finance parser path before persisting the transaction account/payment_method to SQLite.

## Safety

This change does not perform Google write, DB mutation, credential read, or service restart.
