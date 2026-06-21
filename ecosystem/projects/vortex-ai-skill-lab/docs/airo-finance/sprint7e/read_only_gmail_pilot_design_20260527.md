# AIRO Finance — Sprint 7E Read-Only Gmail Pilot Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7E Read-Only Gmail Pilot
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
Sprint 7E: Read-Only Gmail Pilot design active

## Result

RESULT=PASS_SPRINT7E_READ_ONLY_GMAIL_PILOT_DESIGN_RECORDED
NEXT=sprint7e_read_only_gmail_pilot_guard_contract

## Purpose

Sprint 7E defines the first controlled Gmail read-only pilot.

This design does not read Gmail yet.

The future pilot may only inspect metadata from a very small, explicitly limited set of Gmail messages matching:

- Gmail label: Info Terbaru
- Allowed sender: receipts@blubybcadigital.id
- Allowed sender: noreply@tokopedia.com

The pilot must remain default OFF until explicitly approved.

## Sprint 7D source input

Config source:

docs/airo-finance/sprint7d/real_email_source_setup_config_20260527.json

Configured sources:

1. Blu
   - Sender: receipts@blubybcadigital.id
   - Account mapping: Blu -> Blu
   - Gmail label: Info Terbaru

2. Tokopedia Card
   - Sender: noreply@tokopedia.com
   - Account mapping: Tokopedia Card last4 2003 -> Tokopedia Card
   - Gmail label: Info Terbaru

## Allowed future read-only scope

Read-only pilot may later inspect:

- message id
- thread id
- sender
- subject
- date
- label presence
- small safe snippet only if explicitly allowed by guard contract
- detected provider
- detected source mapping
- detected transaction candidate metadata

Read-only pilot must not store:

- full email body
- raw email body
- OTP
- auth code
- login link
- password reset link
- full card number
- full account number
- private security content

## Pilot limits

Initial future read-only pilot must enforce:

- max messages per run: 5
- max threads per run: 5
- sender allowlist required: true
- Gmail label required: Info Terbaru
- metadata-only mode: true
- finance write allowed: false
- email modification allowed: false
- trigger creation allowed: false
- mailbox mutation allowed: false

## Hard blocks

Any future pilot must skip and never forward to Telegram if subject/snippet contains:

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

## Expected read-only output

Future pilot result object must include:

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

## Write policy

Current and future 7E read-only pilot must always keep:

- finance_write_performed: false
- account_ledger_write_performed: false
- finance_events_write_performed: false
- review_queue_write_performed: false
- domain_tab_write_performed: false

No exception.

## Gmail state policy

Current and future 7E read-only pilot must keep:

- Gmail label creation by script: false
- Gmail label modification by script: false
- markRead: false
- archive: false
- delete: false
- move: false
- addLabel: false
- removeLabel: false

## Acceptance criteria

Sprint 7E design passes if it records:

- default OFF
- read-only only
- label required: Info Terbaru
- allowed senders: 2
- max future messages: 5
- metadata-only
- no full body
- no security forwarding
- no email modification
- no trigger
- no finance write
- next fixed step: guard contract

## Next fixed phase

sprint7e_read_only_gmail_pilot_guard_contract

The guard contract must be implemented before any Gmail live read occurs.
