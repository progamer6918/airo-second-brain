# AIRO Finance Sprint 7 - Source Allowlist Design

Status: DESIGN ONLY.

This document defines the source allowlist contract before any live Gmail read.

No Gmail live read is allowed in this phase.

No mailbox read is allowed in this phase.

No Gmail or mail trigger is allowed in this phase.

No finance write is allowed in this phase.

No Account Ledger, Finance Events, or Review Queue write is allowed in this phase.

Email ingestion remains default OFF.

## Purpose

The source allowlist prevents unknown email senders from entering the email ingestion parser.

This phase designs the allowlist contract only.

It does not activate any sender.

It does not read Gmail.

It does not install triggers.

It does not write to finance sheets.

## Global Safety Contract

Required invariant:

- email_ingestion_enabled: false
- email_default_off: true
- dry_run_only: true
- design_only: true
- live_email_scan_allowed: false
- auto_write_allowed: false
- Gmail live read: forbidden
- mailbox read: forbidden
- Gmail trigger install: forbidden
- mail trigger install: forbidden
- full email body storage: forbidden
- OTP/security forwarding to Telegram: forbidden
- finance write from email: forbidden
- Account Ledger write from email: forbidden
- Finance Events write from email: forbidden
- Review Queue write from email: forbidden

## Allowlist Philosophy

Default behavior:

- block unknown sender
- block missing label
- block missing provider profile
- block sensitive OTP/security content before finance parsing
- return preview status only
- never write finance rows

No sender may be treated as trusted unless explicitly approved later.

## Source Allowlist Contract

Each allowlist entry must define:

- allowlist_id
- provider_id
- provider_name
- source_channel
- sender_match_type
- sender_value
- sender_display_hint
- required_gmail_label
- allowed_subject_patterns
- blocked_subject_patterns
- sensitive_hard_block_keywords
- body_scan_scope
- storage_scope
- enabled
- dry_run_only
- created_by
- created_at
- updated_at
- audit_reason
- review_status

## Allowed Sender Match Types

Allowed:

- exact_email
- exact_subdomain_email
- exact_domain_when_official_verified_later

Forbidden for live ingestion:

- wildcard_all
- wildcard_domain_without_verification
- contains_text
- display_name_only
- fuzzy_sender_match
- unknown_sender
- any_sender

## Required Label Contract

Every allowed sender must still require Gmail label:

Finance/ToProcess

Rules:

- label is required even if sender is allowlisted
- missing label returns blocked_source_contract
- label design does not install Gmail filter yet
- label design does not read Gmail yet
- label design does not modify email state

## Provider-Specific Allowlist Placeholders

Important:

All values below are placeholders.

No live sender is approved yet.

### BCA Transaction Notification

allowlist_id: allow_bca_transaction_notification_design

provider_id: bca_transaction_notification

source_channel: email_bca

sender_match_type: exact_email required later

sender_value: placeholder_not_live

required_gmail_label: Finance/ToProcess

enabled: false

dry_run_only: true

review_status: design_only_pending_real_sender

### Blu Transaction Notification

allowlist_id: allow_blu_transaction_notification_design

provider_id: blu_transaction_notification

source_channel: email_blu

sender_match_type: exact_email required later

sender_value: placeholder_not_live

required_gmail_label: Finance/ToProcess

enabled: false

dry_run_only: true

review_status: design_only_pending_real_sender

### Credit Card Purchase Notification

allowlist_id: allow_credit_card_purchase_notification_design

provider_id: credit_card_purchase_notification

source_channel: email_cc

sender_match_type: exact_email required later

sender_value: placeholder_not_live

required_gmail_label: Finance/ToProcess

enabled: false

dry_run_only: true

review_status: design_only_pending_real_sender

### Refund or Reversal Notification

allowlist_id: allow_refund_reversal_notification_design

provider_id: refund_reversal_notification

source_channel: email_cc_or_email_bca_or_email_blu

sender_match_type: exact_email required later

sender_value: placeholder_not_live

required_gmail_label: Finance/ToProcess

enabled: false

dry_run_only: true

review_status: design_only_pending_real_sender

### Failed Transaction Notification

allowlist_id: allow_failed_transaction_notification_design

provider_id: failed_transaction_notification

source_channel: email_bca_or_email_blu_or_email_cc

sender_match_type: exact_email required later

sender_value: placeholder_not_live

required_gmail_label: Finance/ToProcess

enabled: false

dry_run_only: true

review_status: design_only_pending_real_sender

### OTP or Security Notification

allowlist_id: block_otp_security_notification_design

provider_id: otp_security_notification

source_channel: email_security

sender_match_type: blocked_before_finance_parse

sender_value: any_sender_with_sensitive_keyword

required_gmail_label: not_required_for_hard_block

enabled: false

dry_run_only: true

review_status: always_block_before_finance_parse

## Unknown Sender Rules

Unknown sender must return:

parse_status: blocked_source_contract

Expected preview fields:

- source_message_id: hash only when available
- sender: redacted or sender hash later
- subject: subject hash only later
- merchant: blank
- amount: 0
- currency: blank
- transaction_date: blank
- payment_method: blank
- category_guess: blank
- confidence: 0
- duplicate_key: source contract block key
- needs_review_reason: sender_not_allowlisted
- parse_status: blocked_source_contract
- sensitive_skip_reason: blank unless sensitive keyword exists

If sensitive keyword exists, skipped_sensitive takes priority before blocked_source_contract.

## Sensitive Priority Rule

Priority order:

1. skipped_sensitive
2. blocked_source_contract
3. not_finance_candidate
4. candidate_low_confidence
5. candidate_needs_clarification
6. candidate_duplicate_dry_run
7. candidate_ready_preview_only

Sensitive content always wins.

OTP/security content must never be finance-parsed.

## Sender Review Workflow Design

A future sender approval flow must require:

- user-provided sender email
- provider mapping
- Gmail label confirmation
- reason for approval
- manual dry-run preview
- no OTP/security conflict
- audit record

Approval must not automatically enable live ingestion.

Approval must only change allowlist design or dry-run allowlist state in a later phase.

## _AIRO_Email_Ingestion_Log Allowlist Fields

Potential log fields for future dry-run log:

- email_log_id
- provider_id
- allowlist_id
- sender_match_type
- sender_value_hash
- sender_allowed
- label_required
- label_present
- source_contract_status
- parse_status
- sensitive_skip_reason
- review_status
- audit_reason
- created_at
- processed_at

Forbidden log content:

- full email body
- OTP code
- password reset code
- full card number
- full account number
- raw sensitive subject/body
- unredacted unknown sender until policy approved

## Telegram Readback Command Plan

Next safe command:

admin email sprint7 source allowlist

Expected behavior:

- returns allowlist design summary
- returns provider placeholder count
- returns unknown sender block rule
- returns sensitive priority rule
- dry-run only
- no Gmail read
- no trigger
- no finance write
- no sheet write

## Still Forbidden

Still forbidden after this design:

- Gmail live read
- Gmail trigger install
- Email-to-ledger write
- Email-to-Finance Events write
- Review Queue write from email
- Full body storage
- Auto-post from email
- Live sender activation without explicit trusted sender values
- Wildcard allowlist
- Unknown sender parsing as finance

## Result

RESULT=PASS_SPRINT7_SOURCE_ALLOWLIST_DESIGN_READY
