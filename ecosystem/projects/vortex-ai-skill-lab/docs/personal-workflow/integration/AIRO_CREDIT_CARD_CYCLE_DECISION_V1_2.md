# AIRO Credit Card Cycle Decision v1.2

Date: 2026-05-20
Project: AIRO Finance Sheet Workflow v1.2
Scope: Credit Card billing cycle, Pocket Blu allocation, Dashboard display logic

## Status

Credit Card cycle validation: PASS

The Tokopedia CC billing cycle uses a 16-to-15 cycle, not a calendar-month cycle.

## Final Rule

Statement cycle:

- Cycle starts on day 16.
- Cycle ends on day 15 of the following month.
- Example:
  - 16 Apr 2026 – 15 May 2026 = TOKPED_CC_2026-05
  - 16 May 2026 – 15 Jun 2026 = TOKPED_CC_2026-06

Due date:

- The 16 Apr – 15 May cycle has due date 30 May.
- Transactions after 15 May must not be mixed into the 16 Apr – 15 May payable bill.

## User Decisions

### Dashboard display

Dashboard should show two separate Credit Card contexts:

1. Tagihan Jatuh Tempo
   - Closed statement cycle.
   - Example: 16 Apr – 15 May.
   - Due date: 30 May.
   - Status can be unpaid, partial, paid, or overdue.

2. Periode Berjalan / Unbilled
   - Current running cycle.
   - Example: 16 May – 15 Jun.
   - Not yet a final bill.
   - Should not be mixed with the previous payable cycle.

### Dashboard vs Credit Card tab

Dashboard:

- Show summary only.
- Do not show all transaction details.
- Keep it readable as a personal finance snapshot.

Credit Card tab:

- Show detailed transactions.
- Especially show unpaid / not-yet-funded-to-Blu items.

### Overdue behavior

If a closed statement passes due date and is not safe/paid/funded:

- Show warning in Dashboard and Credit Card tab.
- Future ideal behavior: Telegram reminder.
- Do not implement reminder until cycle/status logic is reliable.

### Meaning of “Belum ke Blu”

“Belum ke Blu” means:

- The money for paying the CC bill has not yet been prepared in the dedicated Pocket Blu for CC payment.
- It does not merely mean “not paid to bank yet”.
- The Pocket Blu CC allocation status is important for personal cash control.

## Runtime Proof

After running:

admin fix cc tanggal

Telegram returned:

- Rows updated: 9

Then after running:

admin audit cc cycles

Telegram returned:

- Rows counted: 9

Cycle totals:

- TOKPED_CC_2026-04: Rp15000
- TOKPED_CC_2026-05: Rp351000
- TOKPED_CC_2026-06: Rp24500

Important row proof:

- Row #11:
  - Date: 15/05/2026
  - Amount: Rp40.000
  - Cycle: TOKPED_CC_2026-05
  - Period: 2026-04-16 – 2026-05-15

- Row #12:
  - Date: 20/05/2026
  - Amount: Rp24.500
  - Cycle: TOKPED_CC_2026-06
  - Period: 2026-05-16 – 2026-06-15

Conclusion:

- 15 May is correctly included in TOKPED_CC_2026-05.
- 20 May is correctly included in TOKPED_CC_2026-06.
- The 16-to-15 cycle rule is working.

## Implemented / Relevant Commands

Available Telegram commands:

- admin fix cc tanggal
- admin audit cc cycles

`admin fix cc tanggal` recomputes:

- date
- merchant_app
- billing_cycle_id
- billing_start
- billing_end
- statement_month

`admin audit cc cycles` displays:

- Credit Card row count
- cycle totals
- recent rows
- date
- amount
- Pocket Blu status
- billing cycle id
- billing start/end

## Relevant Commits

- cf77ef3 test(airo-finance): add credit card cycle audit command
- 9ffd147 test(airo-finance): harden credit card cycle audit command
- 264fbbc test(airo-finance): harden credit card cycle audit command
- 0ff71bb test(airo-finance): fix credit card cycle audit amount parsing
- c14d24b test(airo-finance): cap account rows audit output

## Dashboard Implication

For the future Google Sheet Dashboard:

Credit Card section should include:

1. Tagihan Jatuh Tempo
   - Current closed statement
   - Due date
   - Total bill
   - Amount not yet prepared in Pocket Blu
   - Paid/funded/overdue status

2. Periode Berjalan / Unbilled
   - Running cycle
   - Temporary total
   - Not yet final
   - Should not be counted as due bill yet

Do not mix unbilled transactions into the previous payable statement.
