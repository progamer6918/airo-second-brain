# AIRO Finance — Sprint 7E Read-Only Gmail Pilot Controlled Enable Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7E Read-Only Gmail Pilot Controlled Enable
Mode: design-only
Deploy performed: false
Gmail live read performed: false
Finance write performed: false

## Roadmap position

Sprint 0A: closed
Sprint 0B: done
Sprint 1: closed
Sprint 2: closed
Sprint 3: closed
Sprint 4: closed / live pass
Sprint 5: core live pass
Sprint 6: dashboard live pass recorded
Sprint 6B: closed
Sprint 7: Email Ingestion active / default OFF
Sprint 7B: Email Sandbox Fixture Matrix closed
Sprint 7C: Synthetic Candidate Simulation closed
Sprint 7D: Real Email Source Setup Manual Config verified
Sprint 7E: Read-Only Gmail Pilot controlled enable design active

## Result

RESULT=PASS_SPRINT7E_READ_ONLY_GMAIL_PILOT_CONTROLLED_ENABLE_DESIGN_RECORDED
NEXT=sprint7e_read_only_gmail_pilot_controlled_enable_contract_or_manual_approval

## Purpose

This phase defines how the read-only Gmail pilot may be enabled later without accidentally reading Gmail, modifying mailbox state, storing full email body, or writing finance data.

This step does not enable the pilot.

This step does not read Gmail.

This step does not deploy Apps Script.

This step does not create triggers.

This step does not write finance data.

## Current proven status

Status command:

admin email sprint7e read only pilot status

Verified status:

read_only_gmail_pilot_static_default_off_ready

Verified properties:

- Gmail pilot enabled: false
- Manual approval required: true
- Email ingestion enabled: false
- Email default OFF: true
- Dry-run only: true
- Gmail label required: Info Terbaru
- Max messages per run: 5
- Max threads per run: 5
- Source count: 2
- Allowed sender count: 2
- Gmail read performed: false
- Mailbox read performed: false
- Gmail modified: false
- Mail trigger created: false
- Full email body stored: false
- Finance write performed: false

## Controlled enable requirements

A future Gmail read-only pilot may only run if all of these are true:

1. User explicitly approves a one-run read-only pilot.
2. Approval text contains the exact requested label: Info Terbaru.
3. Approval text contains max message limit: 5.
4. Approval text confirms no finance write.
5. Approval text confirms no email modification.
6. Approval text confirms no full body storage.
7. Approval text confirms no OTP/security forwarding.
8. Source allowlist remains exactly:
   - receipts@blubybcadigital.id
   - noreply@tokopedia.com
9. Gmail label remains exactly:
   - Info Terbaru
10. Pilot remains one-shot, not recurring.
11. No trigger is created.
12. Pilot output is dry-run summary only.

## Required future approval phrase

The future live read-only pilot must not run unless the user explicitly sends a command or approval equivalent to:

APPROVE SPRINT 7E ONE-SHOT READ-ONLY GMAIL PILOT
LABEL=Info Terbaru
MAX_MESSAGES=5
NO_FINANCE_WRITE=true
NO_EMAIL_MODIFICATION=true
NO_FULL_BODY_STORAGE=true

## Future pilot runtime boundaries

Allowed:

- Read up to 5 messages only.
- Only messages under Gmail label Info Terbaru.
- Only allowed senders:
  - receipts@blubybcadigital.id
  - noreply@tokopedia.com
- Metadata-only extraction.
- Dry-run candidate summary.
- Sensitive hard-block.
- No-write proof.

Forbidden:

- Reading arbitrary mailbox.
- Reading more than 5 messages.
- Creating triggers.
- Modifying Gmail labels.
- Marking read or unread.
- Moving, archiving, deleting, starring, or mutating messages.
- Storing full email body.
- Forwarding raw email to Telegram.
- Forwarding OTP or security content.
- Account Ledger write.
- Finance Events write.
- Review Queue write.
- Domain tab write.
- Dashboard mutation.
- Reconciliation mutation.

## Future output requirements

Any future one-shot pilot must output:

- RESULT
- run_id
- label
- max_messages
- allowed_sender_count
- scanned_message_count
- candidate_count
- skipped_sensitive_count
- skipped_sender_not_allowed_count
- skipped_missing_label_count
- clarification_needed_count
- dry_run_route_count
- gmail_pilot_enabled
- gmail_live_read_performed
- mailbox_read_performed
- mail_trigger_created
- email_modified
- full_email_body_stored
- finance_write_performed

## Success criteria for future one-shot pilot

The future pilot passes only if:

- scanned_message_count <= 5
- every scanned message has label Info Terbaru
- every candidate sender is allowlisted
- sensitive/security messages are blocked
- full_email_body_stored is false
- email_modified is false
- mail_trigger_created is false
- finance_write_performed is false
- output includes enough metadata for user review
- no automatic finance write occurs

## Failure criteria for future one-shot pilot

The future pilot fails if:

- Gmail read happens without explicit approval
- more than 5 messages are scanned
- non-allowlisted sender is parsed as a candidate
- missing-label message is parsed as a candidate
- security/OTP message is sent to Telegram
- full body is stored
- email state is modified
- finance write happens
- trigger is created
- recurring scan is enabled

## Next fixed choice

After this design, there are only two valid paths:

A. Record a controlled-enable contract/readback command while still default OFF.

B. User explicitly approves the one-shot read-only Gmail pilot.

Recommended next: controlled-enable contract/readback command, still default OFF.
