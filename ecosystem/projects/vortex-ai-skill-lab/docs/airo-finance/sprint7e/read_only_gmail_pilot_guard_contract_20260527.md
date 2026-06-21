# AIRO Finance — Sprint 7E Read-Only Gmail Pilot Guard Contract

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7E Read-Only Gmail Pilot
Mode: guard contract only
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
Sprint 7E: Read-Only Gmail Pilot guard contract active

## Result

RESULT=PASS_SPRINT7E_READ_ONLY_GMAIL_PILOT_GUARD_CONTRACT_RECORDED
NEXT=sprint7e_read_only_gmail_pilot_static_implementation_default_off

## Purpose

This guard contract defines the hard safety boundary for any future read-only Gmail pilot implementation.

This step does not deploy code.
This step does not read Gmail.
This step does not create triggers.
This step does not modify email state.
This step does not write finance data.

## Required default state

Email ingestion enabled: false
Email default OFF: true
Dry-run only: true
Pilot enabled default: false
Manual approval required: true

## Allowed source scope

Gmail label required:

Info Terbaru

Allowed senders:

- receipts@blubybcadigital.id
- noreply@tokopedia.com

Source mappings:

- Blu via receipts@blubybcadigital.id -> Blu
- Tokopedia Card via noreply@tokopedia.com -> Tokopedia Card

Tokopedia sender risk:

noreply@tokopedia.com is broad and may include non-finance, promo, login, and security emails. Future pilot must enforce label, sender, subject classification, and sensitive hard-block before candidate parsing.

## Future pilot limits

Max messages per run: 5
Max threads per run: 5
Allowed sender count: 2
Required label: Info Terbaru
Metadata-only: true
Full body storage: false
Raw body storage: false
Finance write: false

## Allowed metadata fields for future pilot

- message_id
- thread_id
- sender
- subject
- date
- label_presence
- provider
- source_id
- account_mapping
- candidate_status
- parse_status
- block_reason

## Forbidden content storage

Never store:

- full email body
- raw email body
- OTP
- auth code
- login link
- password reset link
- full card number
- full account number
- private security content

## Sensitive hard-block terms

Any future pilot must skip and must not forward to Telegram if subject or allowed safe metadata contains:

- OTP
- kode verifikasi
- verification code
- auth code
- password
- reset password
- login
- perangkat baru
- security
- keamanan
- suspicious
- card number
- account number

## Forbidden Gmail mutation operations

Future pilot must not call or perform:

- createLabel
- addLabel
- removeLabel
- markRead
- markUnread
- moveToArchive
- moveToInbox
- moveToTrash
- delete
- star
- unstar

## Forbidden finance write operations

Future pilot must not perform:

- Account Ledger write
- Finance Events write
- Review Queue write
- domain tab write
- dashboard mutation
- reconciliation write

## Required future output fields

Any future read-only pilot result must expose:

- run_id
- run_mode
- gmail_label
- allowed_sender_count
- scanned_message_count
- candidate_count
- skipped_sensitive_count
- skipped_sender_not_allowed_count
- skipped_missing_label_count
- parse_candidate_count
- clarification_needed_count
- dry_run_route_count
- finance_write_performed
- account_ledger_write_performed
- finance_events_write_performed
- review_queue_write_performed
- domain_tab_write_performed
- gmail_modified
- full_email_body_stored
- raw_email_forwarded_to_telegram

## Acceptance criteria

Guard contract passes if:

- default OFF is true
- manual approval required is true
- Gmail label is Info Terbaru
- allowed sender count is 2
- max messages per run is 5
- all Gmail mutation operations are forbidden
- all finance writes are forbidden
- all sensitive content storage is forbidden
- current step performs no Gmail read
- current step performs no deploy
- current step performs no finance write

## Next fixed phase

sprint7e_read_only_gmail_pilot_static_implementation_default_off

The future implementation must stay default OFF and must not perform live Gmail read until explicitly approved.
