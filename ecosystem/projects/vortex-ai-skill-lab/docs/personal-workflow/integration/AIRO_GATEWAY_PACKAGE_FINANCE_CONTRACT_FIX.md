# AIRO Gateway Package Finance Contract Fix

Status: patched.

## Root cause

OpenClaw/Telegram calls:

`scripts/airo_personal_workflow_call.sh`
-> `python3 -m airo_personal_workflow.gateway`

The gateway package parser still used the older amount/category parser, so:

`nabung 5000 ke blu`

was parsed as:

- amount: `5000000`
- category: `uncategorized`

even though `scripts/personal-workflow/airo_transaction_persistence.py` had already been fixed.

## Fix

`airo_personal_workflow/intents/parser.py` now implements AIRO Finance Language Contract v1.0:

- `5000` -> `5000`
- `5` -> `5000`
- `5rb` -> `5000`
- `5 juta` -> `5000000`
- `1.250.000` -> `1250000`
- `nabung ...` category -> `tabungan`
- `blu` -> `BLU BCA`

## Required validation

Before re-enabling Sheets timer:

1. wrapper smoke must parse `nabung 5000 ke blu` as `5000` and `tabungan`
2. Telegram smoke must insert a new SQLite row with amount `5000`
3. full-auto dry-run must show asset row idempotency
