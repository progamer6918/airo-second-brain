# AIRO Credit Card Mirror Planner v0.9

Status: IMPLEMENTED / NO GOOGLE WRITE
Date: 2026-05-10

## Purpose

Generate a 💳 Credit Card mirror operation for Tokopedia Card transactions.

The normal transaction remains in:

- 💸 Transactions

A mirror row is planned for:

- 💳 Credit Card

## Why this is needed

Tokopedia Card billing cycles do not follow calendar months.

Cycle rule:

- start day: 16
- end day: 15
- statement_month is the month containing billing_end

Examples:

- 2026-04-15 -> TOKPED_CC_2026-04
- 2026-04-16 -> TOKPED_CC_2026-05
- 2026-05-15 -> TOKPED_CC_2026-05
- 2026-05-16 -> TOKPED_CC_2026-06

## Artifacts

Mirror planner:

- scripts/personal-workflow/airo_credit_card_mirror_planner.py

Tests:

- tests/personal-workflow/test_airo_credit_card_mirror_planner.py

Integrated into write_preview:

- scripts/personal-workflow/airo_sheets_sync_write_preview.py

## Mirror row fields

The planner outputs:

- cc_entry_id
- date
- merchant_app
- amount
- description
- status_pocket_blu
- transferred_at
- linked_txn_id
- notes
- billing_cycle_id
- billing_start
- billing_end
- statement_month
- due_date
- is_statement_locked

## Idempotency

The mirror operation uses:

- duplicate_key = transaction_id

This matches the sheet key exporter behavior for 💳 Credit Card, which reads `linked_txn_id`.

## Safety

- no Google write
- no credential read
- no DB mutation
- validation marker rows are skipped
- NO_WRITE operations are skipped

## Next official item

Create or ingest a Tokopedia Card transaction through Telegram/Airo, rerun write_preview, and verify that it produces:

- 💸 Transactions insert/update candidate
- 💳 Credit Card mirror insert candidate with correct billing_cycle_id
