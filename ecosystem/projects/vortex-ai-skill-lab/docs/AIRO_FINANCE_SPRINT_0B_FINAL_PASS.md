# AIRO Finance — Sprint 0B Final PASS

Status: CLOSED / PASS  
Sprint: Sprint 0B — Email Ambiguity Research & Bridge Design  
Track: Canonical Kitab roadmap  
Runtime scope: Research/design only

## Result

Sprint 0B is CLOSED / PASS.

This sprint produced research/design artifacts only. It did not implement Gmail OAuth, Gmail triggers, runtime email fetching, full email body storage, automatic ledger writes from email, or full Email Ingestion v1.

## Evidence

Sprint 0B documents:

- `docs/AIRO_FINANCE_SPRINT_0B_SCOPE_MATRIX.md`
- `docs/AIRO_FINANCE_SPRINT_0B_EMAIL_POLICY_DESIGN.md`

Sprint 0B commits:

- `1b6e622 docs(airo-finance): start Sprint 0B email ambiguity design`
- `4b25a27 docs(airo-finance): finalize Sprint 0B email policy design`

## Definition of Done Mapping

| Definition of Done | Status | Evidence |
|---|---:|---|
| Email ambiguity list is defined | PASS | Scope matrix and policy design |
| OTP/security hard-block policy is clear | PASS | Email policy design |
| Email ambiguous flow asks Telegram first | PASS | Email-to-Telegram bridge design |
| Review Queue remains fallback | PASS | Scope matrix and policy design |
| No full Email Ingestion implementation yet | PASS | Runtime guard / docs-only Sprint 0B changes |

## Final Sprint 0B Decisions

### Email ambiguity taxonomy

Email-derived finance candidates are ambiguous when they have:

- missing amount
- multiple amounts
- missing account/source
- missing destination
- missing category
- unclear direction
- unclear success/failed/pending status
- unclear Credit Card type
- duplicate candidate against Telegram/manual input
- low parser confidence

### OTP/security hard-block

OTP/security email must be stopped before finance parsing.

Hard-blocked content must not:

- enter finance parser
- be sent to Telegram
- enter Review Queue
- enter Finance Events
- be stored as full body text
- generate ledger/domain writes

### Email-to-Telegram bridge

Ambiguous email must ask Telegram first.

If Telegram answer resolves the ambiguity, the future normalized candidate may continue to the existing router in a later sprint. If Telegram answer is missing, invalid, timed out, or still ambiguous, Review Queue remains the fallback.

### Missing category from email

Missing category is ambiguity. It must not enter clean category metrics until resolved.

### Duplicate email vs Telegram

Amount alone is not enough to mark duplicate.

Future dedupe must consider:

- amount
- date/time window
- merchant/counterparty
- account/card/e-wallet
- direction
- category candidate
- source channel
- message ID hash
- Telegram message reference

## Explicit Non-Implementation Confirmation

Sprint 0B did not add:

- Gmail OAuth
- Gmail trigger
- Gmail runtime fetcher
- Apps Script email parser
- full email body storage
- email-to-ledger automatic write
- dashboard Email Ingestion Status activation
- Sprint 1 Account Ledger implementation

## Next Sprint

Next official sprint after Sprint 0B closeout:

Sprint 1 — Account Ledger Hardening

Sprint 1 must start with repo audit and current Account Ledger behavior verification before any runtime patch.
