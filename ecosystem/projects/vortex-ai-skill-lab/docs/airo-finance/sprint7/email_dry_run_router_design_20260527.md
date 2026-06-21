# AIRO Finance — Sprint 7 Email Dry Run Router Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7 Email Ingestion
Mode: design-only
Deploy performed: false

## Purpose

Email Dry Run Router defines how future resolved email candidates would be routed without performing any actual finance write.

This router is a planning and proof layer only.

It must never write to Account Ledger, Finance Events, Review Queue, or domain tabs during Sprint 7 default-off dry-run phases.

## Current status

Email ingestion remains default OFF.

This phase is design-only.

No Gmail read, mailbox trigger, email modification, or finance write is allowed.

## Hard guardrails

Blocked in this phase:

- Gmail live read
- mailbox read
- Gmail trigger creation
- Gmail label creation by script
- Gmail filter creation by script
- markRead
- archive
- delete
- move
- email modification
- full email body storage
- OTP/security content storage
- OTP/security forwarding to Telegram
- raw email forwarding to Telegram
- Account Ledger write from email
- Finance Events write from email
- Review Queue write from email
- domain tab write from email
- finance write of any kind

Allowed in this phase:

- dry-run router design documentation
- routing decision table planning
- safe destination prediction
- failure and review fallback planning
- dry-run readback planning

## Router input

Router input must be a resolved metadata-only candidate.

Required preconditions:

- lifecycle_state is ready_for_router or clarification_resolved
- sensitive hard-block passed
- source contract passed
- required label contract passed
- metadata-only policy passed
- duplicate guard passed
- parser confidence above threshold or user clarification resolved
- no full email body stored
- no raw security content stored
- no OTP/security content forwarded

## Router output

Router output is a dry-run plan object only.

Required fields:

- route_plan_id
- candidate_id
- email_log_id
- source_id
- proposed_destination
- proposed_tab
- proposed_account
- proposed_category
- proposed_amount
- proposed_date
- proposed_merchant
- proposed_direction
- proposed_status
- confidence
- risk_level
- write_allowed
- write_performed
- reason
- blockers
- next_action
- created_at
- notes

Required constants in current phase:

- write_allowed: false
- write_performed: false
- email_ingestion_enabled: false
- dry_run_only: true

## Proposed destinations

Allowed dry-run destination predictions:

- account_ledger_expense
- account_ledger_income
- account_ledger_transfer
- credit_card_purchase
- credit_card_payment
- refund_or_reversal
- internal_transfer
- review_queue_future
- blocked_sensitive
- blocked_duplicate
- blocked_low_confidence
- blocked_missing_field
- no_route

## Destination rules

### account_ledger_expense

Use when candidate is confirmed successful expense from a known account or wallet.

Required:

- amount
- date
- source account
- merchant or counterparty
- category
- direction: outflow
- status: success

Current phase result:

- proposed_destination: account_ledger_expense
- write_allowed: false
- write_performed: false

### account_ledger_income

Use when candidate is confirmed successful income or refund into a known account.

Required:

- amount
- date
- destination account
- source or merchant if available
- direction: inflow
- status: success

Current phase result:

- proposed_destination: account_ledger_income
- write_allowed: false
- write_performed: false

### account_ledger_transfer

Use when candidate is confirmed internal transfer.

Required:

- amount
- date
- source account
- destination account
- direction: internal_transfer
- status: success

Current phase result:

- proposed_destination: account_ledger_transfer
- write_allowed: false
- write_performed: false

### credit_card_purchase

Use when candidate is confirmed credit card purchase.

Required:

- amount
- date
- card last4 or mapped card account
- merchant
- category
- direction: outflow
- status: success

Current phase result:

- proposed_destination: credit_card_purchase
- write_allowed: false
- write_performed: false

### credit_card_payment

Use when candidate is confirmed credit card bill payment.

Required:

- amount
- date
- source account
- credit card account or last4
- status: success

Current phase result:

- proposed_destination: credit_card_payment
- write_allowed: false
- write_performed: false

### refund_or_reversal

Use when candidate is confirmed refund or reversal.

Required:

- amount
- date
- merchant or original reference if available
- destination account or card
- status: success or reversal

Current phase result:

- proposed_destination: refund_or_reversal
- write_allowed: false
- write_performed: false

### review_queue_future

Use only as fallback when clarification cannot resolve the candidate or risk remains high.

Current phase result:

- proposed_destination: review_queue_future
- write_allowed: false
- write_performed: false

## Blocked outcomes

Dry-run router must block when:

- sensitive content detected
- duplicate risk exists
- amount missing
- date missing
- account mapping missing
- source contract failed
- required label missing
- parser confidence too low
- status unclear
- category required but missing
- merchant required but missing
- direction unclear

## Risk levels

Allowed risk levels:

- low
- medium
- high
- critical

Critical examples:

- OTP/security content
- full card number
- password reset
- raw login link
- raw email body exposure
- duplicate with possible write risk

## Write policy

Current phase must always produce:

write_allowed: false
write_performed: false

No exception allowed.

## Dry-run readback target

Future Telegram command:

admin email sprint7 dry run router

Expected readback must prove:

- design only true
- write performed false
- write allowed false
- email ingestion enabled false
- default off true
- dry-run only true
- Gmail read performed false
- mailbox read performed false
- Gmail modified false
- trigger created false
- full email body stored false
- sensitive content stored false
- raw email forwarded false
- finance write performed false
- Account Ledger write performed false
- Finance Events write performed false
- Review Queue write performed false
- domain tab write performed false
- proposed destinations present
- blocked outcomes present
- risk levels present
- status email_dry_run_router_design_ready

## Acceptance result

RESULT=PASS_SPRINT7_EMAIL_DRY_RUN_ROUTER_DESIGN_RECORDED
NEXT=email_dry_run_router_readback_design_only
