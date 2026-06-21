# AIRO Transaction Amount Parser Bare Number Fix

Status: patched.

## Bug

`nabung 5000 ke blu` was persisted as `5000000`.

Correct value is `5000`.

## Rule

- `5000` -> `5000`
- `5 rb` / `5 ribu` / `5k` -> `5000`
- `5 juta` / `5 jt` -> `5000000`

No implicit multiplier is applied to bare numbers.

## Guardrail

If upstream returns `raw_amount * 1000` while raw text contains a bare amount, persistence corrects it to the literal raw amount.

## Safety

The wrong live row `trx_a8ad5c2eec99` was backed up and corrected in SQLite before Sheets apply.
