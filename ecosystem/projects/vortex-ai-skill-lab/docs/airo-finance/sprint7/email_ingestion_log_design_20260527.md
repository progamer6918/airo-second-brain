# AIRO Finance — Sprint 7 Email Ingestion Log Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7 Email Ingestion
Mode: design-only
Deploy performed: false

## Purpose

_AIRO_Email_Ingestion_Log is a backend audit and trace log for future email ingestion.

It exists to prove what would happen to an email candidate without allowing Gmail live read, Gmail trigger, mailbox modification, or finance write during default-off Sprint 7 dry-run phases.

## Guardrails

Email ingestion remains default OFF.

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
- OTP or security content forwarding
- Account Ledger write from email
- Finance Events write from email
- Review Queue write from email
- auto-post email to Telegram
- finance write of any kind

Allowed in this phase:

- design documentation
- schema planning
- static contract definition
- dry-run readback planning
- metadata-only candidate model
- sensitive skip status definition

## Sheet name

_AIRO_Email_Ingestion_Log

This is a backend sheet, not a user-facing dashboard tab.

## Schema v1

Required columns:

1. email_log_id
2. message_id
3. thread_id
4. source_id
5. from_email
6. subject_hash
7. received_at
8. processed_at
9. parse_status
10. parse_confidence
11. detected_amount
12. detected_date
13. detected_merchant
14. detected_last4
15. sensitive_skip_reason
16. clarification_ref
17. event_ref
18. review_queue_ref
19. error_message
20. notes

## Metadata-only policy

Allowed metadata:

- message_id
- thread_id
- source_id
- from_email
- subject_hash
- received_at
- processed_at
- detected amount
- detected date
- detected merchant
- detected card last4
- parse status
- confidence
- skip reason
- refs
- error summary
- notes

Forbidden storage:

- full email body
- OTP code
- auth code
- password reset content
- login link
- full card number
- full account number
- full raw security email content
- unredacted sensitive message

## parse_status values

- dry_run_ready
- blocked_source_contract
- skipped_sensitive
- missing_required_label
- sender_not_allowed
- parse_candidate
- needs_clarification
- needs_review
- duplicate_candidate
- parse_failed
- disabled_default_off

## sensitive_skip_reason values

- otp_keyword
- verification_keyword
- login_keyword
- password_reset_keyword
- security_keyword
- device_keyword
- auth_code_keyword
- sensitive_sender
- sensitive_unknown

## source_id values

Initial planned source ids:

- email_blu
- email_cc
- email_bca
- email_unknown_allowed
- email_unknown_blocked

## Readback target

Future Telegram readback command should prove:

- design only true
- write performed false
- email ingestion enabled false
- default off true
- dry-run only true
- Gmail read performed false
- mailbox read performed false
- Gmail modified false
- mail trigger created false
- full body stored false
- sensitive content stored false
- finance write performed false
- Account Ledger write performed false
- Finance Events write performed false
- Review Queue write performed false
- required schema columns present in contract
- parse_status values present in contract
- metadata-only policy active
- status email_ingestion_log_design_ready

## Acceptance result

RESULT=PASS_SPRINT7_EMAIL_INGESTION_LOG_DESIGN_RECORDED
NEXT=email_ingestion_log_readback_design_only
