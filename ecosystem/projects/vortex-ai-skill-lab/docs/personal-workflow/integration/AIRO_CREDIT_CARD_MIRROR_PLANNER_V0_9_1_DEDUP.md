# AIRO Credit Card Mirror Planner v0.9.1 De-dup Fix

Status: IMPLEMENTED / NO GOOGLE WRITE
Date: 2026-05-10

## Trigger

After Tokopedia Card capture, write_preview generated too many Credit Card candidates:

- expected: 1 💳 Credit Card candidate
- observed: 3 💳 Credit Card candidates

The correct billing-cycle candidate existed, but duplicate legacy/mirror rows also appeared.

## Fix

v0.9.1 applies two safeguards:

1. Mirror planner only mirrors canonical 💸 Transactions operations.
2. write_preview normalizes/deduplicates Credit Card operations:
   - final Credit Card duplicate_key is linked_txn_id
   - billing-cycle mirror row is preferred
   - legacy duplicate_key prefix credit_card:<txn_id> is dropped when a billing mirror exists

## Expected final preview

For the current sheet snapshot and SQLite state:

- BLU BCA transaction `transactions:trx_29f527902571`: skip_duplicate
- Tokopedia CC transaction `transactions:trx_41a84be31c7e`: 💸 Transactions insert_candidate
- Tokopedia CC mirror `trx_41a84be31c7e`: 💳 Credit Card insert_candidate

Expected candidate counts:

- REAL_WRITE_CANDIDATE_COUNT=2
- TRANSACTIONS_CANDIDATE_COUNT=1
- CREDIT_CARD_CANDIDATE_COUNT=1

Expected Credit Card billing fields:

- billing_cycle_id: TOKPED_CC_2026-05
- billing_start: 2026-04-16
- billing_end: 2026-05-15
- statement_month: 2026-05

## Safety

- no Google write
- no credential read
- no DB mutation
- no restricted path touch

## Next official item

Prepare approval-gated Tokopedia CC write artifact after v0.9.1 preview PASS.
