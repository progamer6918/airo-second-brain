# AIRO Finance Sprint 7 - Gmail Label and Filter Design

Status: DESIGN ONLY.

This document defines the Gmail label/filter contract before any live Gmail read.

No Gmail live read is allowed in this phase.

No mailbox read is allowed in this phase.

No Gmail filter is created in this phase.

No Gmail or mail trigger is allowed in this phase.

No email modification is allowed in this phase.

No finance write is allowed in this phase.

No Account Ledger, Finance Events, or Review Queue write is allowed in this phase.

Email ingestion remains default OFF.

## Purpose

The Gmail label/filter design provides a safe staging boundary for future email ingestion.

The label is used as an explicit user-controlled gate.

Even if a sender is allowlisted later, an email must also have the required label before it can enter any future dry-run scan.

This phase only designs the rules.

It does not create labels.

It does not create filters.

It does not read Gmail.

It does not modify email.

It does not install triggers.

It does not write finance rows.

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
- Gmail label creation: forbidden in this phase
- Gmail filter creation: forbidden in this phase
- Gmail trigger install: forbidden
- mail trigger install: forbidden
- markRead: forbidden
- archive: forbidden
- delete: forbidden
- moveToTrash: forbidden
- label modification by script: forbidden
- full email body storage: forbidden
- OTP/security forwarding to Telegram: forbidden
- finance write from email: forbidden
- Account Ledger write from email: forbidden
- Finance Events write from email: forbidden
- Review Queue write from email: forbidden

## Required Label

Design label:

Finance/ToProcess

Rules:

- Label is required for future email ingestion dry-run.
- Label must be manually created or manually approved later.
- Label must not be created automatically in this phase.
- Missing label must return parse_status blocked_source_contract.
- Missing label must not trigger finance parser.
- Missing label must not write to any sheet.
- Missing label must not send full email content to Telegram.

## Optional Labels for Later Phases

These are design placeholders only:

- Finance/ToProcess
- Finance/Processed
- Finance/NeedsReview
- Finance/SkippedSensitive
- Finance/BlockedSource
- Finance/DuplicateCandidate
- Finance/Error

Current phase status:

- none are created by script
- none are required to exist yet
- none are used for live Gmail scan
- none are modified by script

## Filter Design Philosophy

Gmail filters must be user-owned, user-approved, and explicit.

No script-created filter in this phase.

No script-created forwarding.

No automatic archive/delete.

No automatic mark read.

No automatic move to trash.

No label modification by Apps Script until a later explicit phase.

## Future Manual Filter Criteria

A future Gmail filter may be manually configured by the user only after allowlist approval.

Recommended future criteria:

- From: exact trusted sender email only
- Subject includes: provider-specific finance notification hint
- Subject excludes: OTP, login, verification, password, reset, security
- Has attachment: no requirement by default
- Apply label: Finance/ToProcess
- Never send to spam: not decided
- Mark as read: false
- Archive: false
- Delete: false
- Forward: false

## Filter Creation Guardrails

Forbidden:

- wildcard sender filters
- broad domain filters without official verification
- display-name-only matching
- contains-text sender matching
- any filter that catches OTP/security emails as finance candidates
- any filter that marks email as read
- any filter that archives or deletes email
- any filter that forwards email
- any filter that modifies email state without user approval

Required later before any filter activation:

- exact sender value provided by user
- provider profile selected
- source allowlist design updated
- test fixture available
- dry-run preview command exists
- no sensitive keyword conflict
- user confirms filter manually

## Label Gate Rule

Future live or dry-run source contract must require:

1. sensitive hard-block check
2. sender allowlist check
3. required label check
4. provider profile check
5. duplicate key check
6. preview output only

Current phase does not implement Gmail scan.

## Missing Label Rule

If required label is missing:

Expected parse result:

- parse_status: blocked_source_contract
- needs_review_reason: missing_required_label
- amount: 0
- merchant: blank
- payment_method: blank
- category_guess: blank
- confidence: 0
- write_performed: false

## Unknown Sender + Missing Label Rule

If both unknown sender and missing label:

Expected parse result:

- parse_status: blocked_source_contract
- needs_review_reason: sender_not_allowlisted, missing_required_label
- amount: 0
- merchant: blank
- payment_method: blank
- category_guess: blank
- confidence: 0
- write_performed: false

## Sensitive Priority Rule

Sensitive content always wins before sender and label checks.

If OTP/security keyword exists:

Expected parse result:

- parse_status: skipped_sensitive
- sensitive_skip_reason: blocked_keyword_*
- amount: 0
- merchant: blank
- payment_method: blank
- category_guess: blank
- confidence: 0
- write_performed: false

No finance parsing is allowed after sensitive detection.

## Provider Label Mapping

### BCA Transaction Notification

provider_id: bca_transaction_notification

required_label: Finance/ToProcess

filter_status: design_only_not_created

sender_status: placeholder_not_live

### Blu Transaction Notification

provider_id: blu_transaction_notification

required_label: Finance/ToProcess

filter_status: design_only_not_created

sender_status: placeholder_not_live

### Credit Card Purchase Notification

provider_id: credit_card_purchase_notification

required_label: Finance/ToProcess

filter_status: design_only_not_created

sender_status: placeholder_not_live

### Refund or Reversal Notification

provider_id: refund_reversal_notification

required_label: Finance/ToProcess

filter_status: design_only_not_created

sender_status: placeholder_not_live

### Failed Transaction Notification

provider_id: failed_transaction_notification

required_label: Finance/ToProcess

filter_status: design_only_not_created

sender_status: placeholder_not_live

### OTP or Security Notification

provider_id: otp_security_notification

required_label: not_required_for_hard_block

filter_status: never_finance_filter

sender_status: any_sender_with_sensitive_keyword

behavior: skipped_sensitive before sender and label checks

## _AIRO_Email_Ingestion_Log Label Fields

Potential future fields:

- email_log_id
- provider_id
- allowlist_id
- required_label
- label_present
- label_gate_status
- filter_design_id
- filter_status
- source_contract_status
- parse_status
- sensitive_skip_reason
- needs_review_reason
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

admin email sprint7 gmail label filter

Expected behavior:

- returns Gmail label/filter design summary
- returns required label
- returns optional labels
- returns filter guardrails
- returns missing label rule
- returns sensitive priority rule
- dry-run only
- design only
- no Gmail read
- no Gmail filter creation
- no Gmail trigger
- no email modification
- no finance write
- no sheet write

## Still Forbidden

Still forbidden after this design:

- Gmail live read
- Gmail trigger install
- Gmail filter creation by script
- Gmail label creation by script
- markRead
- archive
- delete
- moveToTrash
- Email-to-ledger write
- Email-to-Finance Events write
- Review Queue write from email
- Full body storage
- Auto-post from email
- Live sender activation
- Wildcard allowlist
- Unknown sender parsing as finance

## Result

RESULT=PASS_SPRINT7_GMAIL_LABEL_FILTER_DESIGN_READY
