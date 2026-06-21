# AIRO Finance — Sprint 7 Email Candidate Lifecycle Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7 Email Ingestion
Mode: design-only
Deploy performed: false

## Purpose

This document defines the lifecycle states for future email transaction candidates before any live Gmail read, mailbox trigger, email modification, or email-to-ledger write is allowed.

Email Candidate Lifecycle is the safety boundary between raw email metadata and future routing to Telegram clarification, Review Queue, Finance Events, or Account Ledger.

## Current status

Email ingestion remains default OFF.

This phase is design-only.

## Hard guardrails

Blocked in this phase:

- Gmail live read
- Mailbox read
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
- auto-post email to Telegram
- Account Ledger write from email
- Finance Events write from email
- Review Queue write from email
- finance write of any kind

Allowed in this phase:

- lifecycle design documentation
- state machine definition
- dry-run transition planning
- metadata-only contract planning
- safety and failure mode definition

## Candidate definition

An email candidate is a metadata-only normalized object derived from a future allowed email source.

It is not a ledger event yet.

It is not a Finance Event yet.

It is not a Review Queue item yet.

It must remain blocked until source contract, label contract, sensitive hard-block, metadata-only policy, and parser confidence are all proven.

## Candidate fields

Required candidate fields:

- candidate_id
- email_log_id
- message_id
- thread_id
- source_id
- source_channel
- from_email
- subject_hash
- received_at
- detected_amount
- detected_date
- detected_merchant
- detected_last4
- detected_direction
- detected_status
- parser_profile_id
- parse_status
- parse_confidence
- sensitivity_status
- lifecycle_state
- lifecycle_reason
- clarification_ref
- event_ref
- review_queue_ref
- created_at
- updated_at
- notes

Forbidden candidate fields:

- full_email_body
- raw_otp_code
- raw_auth_code
- raw_login_link
- full_card_number
- full_account_number
- password_reset_link
- unredacted_security_content

## Lifecycle states

### disabled_default_off

Email ingestion is disabled by configuration.

No Gmail read is allowed.

### source_contract_blocked

Candidate cannot exist because source contract is not satisfied.

Examples:

- no allowed sender profile
- missing required Gmail label
- live allowlist disabled
- unknown provider

### skipped_sensitive

Candidate is blocked because sensitive/security content is detected.

Examples:

- OTP
- verification code
- login notification
- password reset
- device security
- auth code

Rules:

- must not enter finance parser
- must not enter Telegram clarification
- must not enter Review Queue
- must not enter Finance Events
- full body must not be stored
- only skip count/hash/status may be recorded

### metadata_logged

Metadata-only record exists in _AIRO_Email_Ingestion_Log.

No finance routing has happened.

### parse_candidate

Parser produced a possible finance candidate.

Still not committed.

### needs_clarification

Candidate has enough metadata to ask user in Telegram, but lacks safe final routing fields.

Examples:

- ambiguous direction
- unknown category
- unclear merchant
- CC purchase vs payment
- success vs failed status unclear

### awaiting_telegram_answer

Telegram clarification has been sent and AIRO is waiting for user answer.

No ledger write.

### clarification_resolved

User answer resolved missing/ambiguous fields.

Candidate is eligible for next routing gate.

### needs_review

Candidate cannot be safely resolved automatically.

Review Queue may be considered only after clarification fails or risk is high.

In current phase, no Review Queue write is allowed.

### ready_for_router

Candidate is normalized and safe enough for future router handoff.

Current phase must not route.

### routed_dry_run

Dry-run planner proves where candidate would go, without write.

### committed_future

Reserved future state.

Actual write is not allowed in this phase.

### failed

Parser or lifecycle handler failed.

Failure must be visible in metadata-only log.

## State transition rules

Allowed design transitions:

disabled_default_off -> source_contract_blocked
source_contract_blocked -> metadata_logged
metadata_logged -> skipped_sensitive
metadata_logged -> parse_candidate
parse_candidate -> needs_clarification
parse_candidate -> needs_review
parse_candidate -> ready_for_router
needs_clarification -> awaiting_telegram_answer
awaiting_telegram_answer -> clarification_resolved
clarification_resolved -> ready_for_router
ready_for_router -> routed_dry_run
any non-committed state -> failed

Forbidden transitions in current phase:

routed_dry_run -> committed_future
parse_candidate -> Account Ledger write
parse_candidate -> Finance Events write
parse_candidate -> Review Queue write
skipped_sensitive -> Telegram clarification
skipped_sensitive -> finance parser
skipped_sensitive -> Review Queue
skipped_sensitive -> Finance Events

## Quality gate

Candidate can reach ready_for_router only if:

- email_ingestion_enabled is explicitly true in a future approved phase
- Gmail label requirement is satisfied
- source allowlist passes
- sensitive hard-block passes
- no full email body is stored
- amount is detected
- source/direction is known
- success/failed status is known when relevant
- parser confidence is above threshold
- category handling follows missing category policy
- duplicate guard passes

## Telegram clarification bridge

If lifecycle_state is needs_clarification, future Telegram prompt must show only safe metadata:

- provider/source
- nominal
- date
- merchant if available
- card last4 if available
- detected direction/status if available

Telegram prompt must not include:

- full email body
- OTP/security text
- full card number
- full account number
- login/security links

## Duplicate guard

Candidate duplicate key should consider:

- message_id
- thread_id
- source_id
- detected_amount
- detected_date
- detected_merchant
- detected_last4

Duplicate candidate should become duplicate_candidate or needs_review.

No duplicate may auto-write.

## Failure visibility

Every failed lifecycle step must produce metadata-only error visibility:

- parse_status
- lifecycle_state
- lifecycle_reason
- error_message
- processed_at
- notes

No failure may silently disappear.

## Readback target for future command

Future Telegram command:

admin email sprint7 candidate lifecycle

Expected readback must prove:

- design only true
- write performed false
- email ingestion enabled false
- default off true
- Gmail read performed false
- mailbox read performed false
- Gmail modified false
- trigger created false
- full email body stored false
- sensitive content stored false
- finance write performed false
- Account Ledger write performed false
- Finance Events write performed false
- Review Queue write performed false
- lifecycle states present
- forbidden transitions present
- status email_candidate_lifecycle_design_ready

## Acceptance result

RESULT=PASS_SPRINT7_EMAIL_CANDIDATE_LIFECYCLE_DESIGN_RECORDED
NEXT=email_candidate_lifecycle_readback_design_only
