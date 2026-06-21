# AIRO Finance Sprint 7 - Email Ingestion Decision Gate

Status: decision gate recorded.

## Current Position

Sprint 6B Telegram Alert Engine is closed.

Sprint 7 Email Ingestion is the next roadmap item, but it remains:

    NOT STARTED
    default OFF

## Decision

Do not enable Email Ingestion yet.

Sprint 7 must start with a dry-run design gate before any live ingestion path is enabled.

## Why Default OFF

Email ingestion can introduce higher risk than Telegram input because it may parse external content, forwarded messages, receipts, notifications, bank emails, or subscription emails.

The system must not ingest email automatically until the following are designed and validated:

- source allowlist
- sender allowlist
- subject/body parser boundary
- attachment handling policy
- duplicate detection
- review queue fallback
- no auto-posting without confidence gate
- audit log coverage
- dry-run preview command
- kill-switch
- default OFF property

## Required Guardrails

Sprint 7 must preserve these rules:

- email_ingestion_enabled = false by default
- no trigger install at first step
- no email read/write side effect at first step
- no automatic Finance Event creation at first step
- dry-run only until approved
- all parsed email candidates must go to Review Queue or preview only
- Telegram manual input remains primary source of truth
- Dashboard Email Ingestion Status remains hidden unless enabled

## Planned Sprint 7 Step Order

1. Email ingestion decision gate
2. Source contract and property guard
3. Dry-run email parser plan
4. Dry-run preview command
5. Review Queue routing only
6. Duplicate detection
7. Audit log coverage
8. Controlled test with one sample email
9. Optional trigger lifecycle after all dry-run tests pass

## Explicit Non-Goals For First Sprint 7 Step

Do not:
- read Gmail live
- install Gmail trigger
- create finance transaction from email
- write to Account Ledger from email
- write to Finance Events from email
- expose Email Ingestion Status on dashboard by default

## Next

Implement Sprint 7 dry-run source contract and property guard.
