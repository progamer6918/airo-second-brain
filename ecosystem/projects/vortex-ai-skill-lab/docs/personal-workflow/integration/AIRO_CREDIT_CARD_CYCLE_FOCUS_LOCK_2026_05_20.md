# AIRO Credit Card Cycle Focus Lock

Date: 2026-05-20
Project: AIRO Finance Sheet Workflow v1.2
Active focus: Credit Card cycle only

## Current Active Focus

The current working focus is strictly:

Credit Card cycle validation / checkpoint.

Do not continue unrelated roadmap items unless the user explicitly approves a scope change.

## Confirmed PASS

Credit Card cycle rule has been validated as PASS:

- 15/05/2026 enters TOKPED_CC_2026-05.
- TOKPED_CC_2026-05 period is 2026-04-16 to 2026-05-15.
- 20/05/2026 enters TOKPED_CC_2026-06.
- TOKPED_CC_2026-06 period is 2026-05-16 to 2026-06-15.
- The 16-to-15 Credit Card cycle rule is working.

Related decision doc:

- docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_DECISION_V1_2.md

## User Decisions

Dashboard / Credit Card display must separate:

1. Tagihan Jatuh Tempo
   - Closed statement period.
   - Due date for 16 Apr – 15 May is 30 May.
   - This remains visible until paid/funded/closed.

2. Periode Berjalan / Unbilled
   - Running statement period.
   - Example: transactions from 16 May onward.
   - Must not be mixed into the previous payable statement.

Meaning of “Belum ke Blu”:

- The money for paying the CC bill has not yet been prepared in the dedicated Pocket Blu for CC payment.
- It does not simply mean “not paid to bank yet”.

## Relevant Scope

Allowed within current focus:

- Tab: 💳 Credit Card
- billing_cycle_id
- billing_start
- billing_end
- statement_month
- due date 30
- Tagihan Jatuh Tempo
- Periode Berjalan / Unbilled
- status_pocket_blu
- Belum ke Blu / Pocket Blu CC allocation
- admin fix cc tanggal
- admin audit cc cycles
- Dashboard section only if directly related to Credit Card cycle

Skip unless user explicitly approves:

- Review Queue
- Cash Ledger
- Account Ledger transfer matrix
- Cicilan Rumah
- Hutang
- Aset
- Monthly Review general formulas
- Dashboard general redesign
- Any non-CC-cycle roadmap item

## Paste-output Rule

If the user pastes output that does not appear relevant to the current Credit Card cycle focus, do not continue automatically.

Ask first:

“Ini output yang benar untuk step Credit Card cycle, atau salah paste / mau ganti scope?”

## Out-of-focus Patch Note

A Review Queue patch was accidentally continued before this focus lock:

- df7d20d fix(airo-finance): route ambiguous parser output to review queue
- Deployed in Apps Script version 136

Decision:

- Keep the commit.
- Do not revert it now.
- Treat it as OUT-OF-FOCUS / NOT VALIDATED.
- Do not claim Review Queue PASS.
- Do not continue Review Queue work unless the user explicitly approves.

## Latest Desired Next Step

Stay on Credit Card cycle checkpoint.

Recommended next action:

- Verify repo status.
- Keep Credit Card cycle decision and focus lock in carryover.
- Do not start new feature work until user explicitly approves.
