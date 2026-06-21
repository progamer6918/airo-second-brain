# AIRO Finance — Sprint 0B Scope Matrix

Status: DESIGN SKELETON  
Sprint: Sprint 0B — Email Ambiguity Research & Bridge Design  
Track: Canonical Kitab roadmap  
Source of truth: `docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md`

## Boundary

Sprint 0B is research/design only.

This sprint must not implement full Gmail ingestion, full Email Ingestion v1, dashboard work, ledger hardening, or domain tab maturation.

## Definition of Done

- Email ambiguity list is defined.
- OTP/security hard-block policy is clear.
- Email ambiguous flow asks Telegram first.
- Review Queue remains fallback.
- No full Email Ingestion implementation yet.

## Scope Matrix

| Area | Sprint 0B Requirement | Design Decision Needed | Runtime Implementation Now? | Fallback |
|---|---|---|---:|---|
| Email ambiguity taxonomy | Define ambiguous email transaction cases | Classify which email signals are safe, ambiguous, duplicate, or blocked | No | Review Queue |
| Email-to-Telegram Clarification Bridge | Design Telegram-first clarification flow for ambiguous email | Define prompt shape, correlation key, and timeout/failure behavior | No | Review Queue |
| OTP/security hard-block policy | Prevent OTP/security emails from becoming finance records | Define hard-block keywords and sender patterns | No | Skip / hard-block |
| Source allowlist / negative keywords | Define trusted senders and exclusion terms | Separate allowlist, denylist, and suspicious-but-reviewable cases | No | Review Queue |
| Missing category from email | Decide how category gaps are handled | Telegram clarification first; do not infer aggressively | No | Review Queue |
| Duplicate email vs Telegram | Prevent double-recording same transaction | Define dedupe keys and collision handling | No | Review Queue / skip duplicate |

## Email Ambiguity Taxonomy Draft

### A. Safe candidate emails

Emails that may become finance events later, but are not implemented in Sprint 0B:

- Bank debit/credit notifications.
- Credit card transaction notifications.
- E-wallet payment notifications.
- Marketplace payment notifications.
- Transfer success notifications.
- Bill payment confirmations.

### B. Ambiguous emails requiring Telegram clarification

- Transaction amount exists but account/source is missing.
- Merchant exists but category is unclear.
- Bank/card notification does not clearly indicate debit vs credit.
- Transfer notification does not clearly identify source/destination.
- Email contains multiple amounts.
- Email looks financial but transaction date/time is unclear.
- Email may duplicate a Telegram/manual entry.

### C. Hard-block emails

These must never create finance records directly:

- OTP.
- Login code.
- Verification code.
- Password reset.
- Security alert.
- Device login.
- Account recovery.
- Fraud warning without confirmed transaction.
- Promotional offer without confirmed payment.
- Marketing newsletter.

### D. Review Queue fallback cases

- Email parse confidence is low.
- Telegram clarification fails or times out.
- Duplicate detection is uncertain.
- Sender is not allowlisted but contains possible finance signal.
- Required fields remain missing after clarification.

## Email-to-Telegram Clarification Bridge Draft

Future email ingestion should follow this order:

1. Receive candidate email.
2. Apply OTP/security hard-block.
3. Apply source allowlist and negative keyword policy.
4. Extract possible transaction fields.
5. Detect ambiguity.
6. If ambiguous, ask user through Telegram first.
7. If user answers clearly, convert to normalized finance intent.
8. If user does not answer or answer remains unclear, write to Review Queue.
9. Never bypass Telegram clarification for ambiguous email-derived finance events.

## Duplicate Email vs Telegram Design Draft

Potential dedupe keys:

- normalized amount
- normalized transaction date/time window
- normalized merchant/counterparty
- normalized account/card/e-wallet source
- email message ID
- Telegram message timestamp
- transaction direction
- category candidate

Collision policy:

- Exact duplicate: skip future duplicate write.
- Probable duplicate: ask Telegram.
- Uncertain duplicate: Review Queue.
- Different account/category/direction: not duplicate until clarified.

## Explicit Non-Goals

- No Gmail OAuth implementation.
- No Apps Script Gmail trigger implementation.
- No full Email Ingestion v1.
- No dashboard work.
- No ledger schema migration.
- No domain tab maturation.
- No cash ledger removal.
- No proactive alert engine.

## Closeout Checklist

- [x] Scope matrix reviewed against Kitab.
- [x] OTP/security hard-block policy finalized.
- [x] Email ambiguity taxonomy finalized.
- [x] Telegram clarification bridge design finalized.
- [x] Review Queue fallback confirmed.
- [x] No full Email Ingestion implementation added.
