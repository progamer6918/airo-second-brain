# AIRO Credit Card Billing Cycle v0.8

Status: ARTIFACT READY / SHEET PATCH NOT YET RUN
Date: 2026-05-10

## Trigger

Tokopedia Card billing periods do not follow calendar month boundaries.

User clarified:

- billing cycle runs from the 16th to the 15th
- example: 16 April through 15 May belongs to the May statement period
- usage on 16 May already belongs to the next billing period

## Decision

Add explicit billing cycle fields to 💳 Credit Card.

Existing header row:

- A3:I3

New billing fields:

- J: billing_cycle_id
- K: billing_start
- L: billing_end
- M: statement_month
- N: due_date
- O: is_statement_locked

## Billing rule

For Tokopedia Card:

- cycle start day: 16
- cycle end day: 15
- statement_month is the month of billing_end

If transaction day >= 16:

- billing_start = current month 16
- billing_end = next month 15
- statement_month = next month

If transaction day <= 15:

- billing_start = previous month 16
- billing_end = current month 15
- statement_month = current month

## Examples

| Transaction date | Billing start | Billing end | Statement month | Cycle ID |
|---|---|---|---|---|
| 2026-04-15 | 2026-03-16 | 2026-04-15 | 2026-04 | TOKPED_CC_2026-04 |
| 2026-04-16 | 2026-04-16 | 2026-05-15 | 2026-05 | TOKPED_CC_2026-05 |
| 2026-05-15 | 2026-04-16 | 2026-05-15 | 2026-05 | TOKPED_CC_2026-05 |
| 2026-05-16 | 2026-05-16 | 2026-06-15 | 2026-06 | TOKPED_CC_2026-06 |

## Artifacts

Python utility:

- scripts/personal-workflow/airo_credit_card_billing_cycle.py

Test:

- tests/personal-workflow/test_airo_credit_card_billing_cycle.py

Apps Script:

- scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs

Main Apps Script functions:

- smokeTestTokpedCardBillingCycleV08
- patchCreditCardBillingCycleHeaderV08
- validateCreditCardBillingCycleHeaderV08

## Safety

The Apps Script patch only writes Credit Card header/formatting cells.

It does not write transaction rows.

## Next official item

Paste Apps Script v0.8 to Google Sheet Apps Script and run:

1. smokeTestTokpedCardBillingCycleV08
2. patchCreditCardBillingCycleHeaderV08
3. validateCreditCardBillingCycleHeaderV08

## Sheet validation result

Status: PASS
Date: 2026-05-10

Observed Apps Script log:

- AIRO_CC_BILLING_CYCLE_HEADER_VALIDATE_V08=PASS
- google_write_performed=false
- checked_range=💳 Credit Card!A3:O3
- mismatches=[]

Interpretation: the Credit Card header now supports billing cycle fields through column O.
