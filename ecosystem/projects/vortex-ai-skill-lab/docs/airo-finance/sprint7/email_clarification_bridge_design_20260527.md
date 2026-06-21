# AIRO Finance — Sprint 7 Email Clarification Bridge Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7 Email Ingestion
Mode: design-only
Deploy performed: false

## Purpose

Email Clarification Bridge defines how future safe email candidates ask the user for clarification through Telegram before any Review Queue write, Finance Events write, Account Ledger write, or domain tab write.

This bridge connects metadata-only email candidates to the existing Telegram clarification-first policy.

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
- auto-post raw email to Telegram
- Account Ledger write from email
- Finance Events write from email
- Review Queue write from email
- domain tab write from email
- finance write of any kind

Allowed in this phase:

- clarification bridge design documentation
- Telegram prompt template planning
- safe metadata field definition
- pending clarification lifecycle planning
- dry-run readback planning

## Bridge principle

Email ambiguity must not go directly to Review Queue if Telegram clarification can resolve it.

Expected future flow:

Email metadata candidate
-> sensitive hard-block
-> source and label contract
-> candidate lifecycle
-> if clear and safe: future dry-run router only
-> if ambiguous: Telegram clarification bridge
-> user answer
-> candidate merge
-> future router gate
-> future write only after explicitly approved phase

## Safe Telegram prompt fields

Allowed fields in Telegram clarification:

- provider or source name
- detected amount
- detected date
- merchant or counterparty if available
- card last4 if available
- detected direction if available
- detected transaction status if available
- candidate reference id
- short action options

Forbidden fields in Telegram clarification:

- full email body
- OTP code
- auth code
- password reset link
- login link
- security link
- full card number
- full account number
- unredacted sensitive email content
- raw email headers
- raw email body

## Clarification types

Supported future clarification types:

- email_missing_category
- email_direction_ambiguous
- email_source_account_missing
- email_destination_account_missing
- email_status_unclear
- email_cc_purchase_vs_payment
- email_refund_vs_income
- email_failed_vs_success
- email_transfer_internal_vs_expense
- email_merchant_unclear
- email_duplicate_possible
- email_low_confidence_parse

## Prompt template: credit card

AIRO menemukan kandidat email Credit Card.

Nominal: Rp{amount}
Tanggal: {date}
Merchant: {merchant}
Kartu: {last4}

Ini transaksi apa?

A. Belanja pakai Credit Card
B. Bayar tagihan Credit Card
C. Refund / reversal
D. Fee / bunga
E. Review manual

## Prompt template: bank or wallet

AIRO menemukan kandidat email transaksi.

Sumber: {source}
Nominal: Rp{amount}
Tanggal: {date}
Merchant/Tujuan: {merchant_or_counterparty}

Ini mau dicatat sebagai apa?

A. Pengeluaran dari rekening
B. Transfer internal
C. Pembayaran Credit Card
D. Uang masuk / refund
E. Review manual

## Prompt template: unclear status

AIRO menemukan kandidat email transaksi, tapi statusnya belum jelas.

Nominal: Rp{amount}
Tanggal: {date}
Merchant/Tujuan: {merchant_or_counterparty}

Status transaksi ini apa?

A. Berhasil
B. Gagal
C. Pending
D. Refund / reversal
E. Review manual

## Prompt template: missing category

AIRO menemukan kandidat email pengeluaran.

Nominal: Rp{amount}
Tanggal: {date}
Merchant: {merchant}

Kategori apa?

A. Makan
B. Transport
C. Belanja
D. Tagihan
E. Tulis manual

## Pending clarification object

Required fields:

- clarification_id
- candidate_id
- email_log_id
- source_channel
- question_type
- safe_prompt_text
- allowed_options
- status
- created_at
- expires_at
- answered_at
- answer_raw
- answer_normalized
- merged_candidate_ref
- notes

Forbidden fields:

- full_email_body
- OTP/security content
- full card number
- full account number
- raw sensitive headers

## Pending clarification status

Allowed status values:

- pending
- answered
- expired
- canceled
- escalated_to_review_future
- blocked_sensitive
- failed

## Merge rules

User answer may merge into candidate only if:

- candidate_id matches pending clarification
- pending status is pending
- answer matches allowed option or safe manual field
- sensitive state remains false
- candidate still has metadata-only policy
- no duplicate conflict appears
- no finance write occurs in current phase

## Review Queue policy

Review Queue is fallback, not first destination.

In current phase:

- Review Queue write is forbidden
- Review Queue planning is allowed
- Escalation target may be designed only

Future Review Queue escalation is allowed only when:

- clarification expires
- user chooses Review manual
- answer remains ambiguous
- parser confidence is low
- duplicate risk remains high
- critical field remains missing

## Data quality impact

Unresolved email clarification must create future Warning status, not Trusted.

Sensitive-blocked email must not create Review Queue or user prompt.

OTP/security accidentally reaching prompt would be Dirty critical.

## Duplicate and idempotency

Clarification idempotency key should consider:

- candidate_id
- email_log_id
- message_id
- question_type
- created_at bucket

Duplicate prompts must be suppressed.

Repeated user answer must not create duplicate routing.

## Current phase acceptance

This phase is complete when design is recorded and guardrails are explicit.

No Apps Script deploy is required for design-only record.

## Future readback target

Future Telegram command:

admin email sprint7 clarification bridge

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
- OTP/security forwarded false
- finance write performed false
- Account Ledger write performed false
- Finance Events write performed false
- Review Queue write performed false
- safe prompt fields present
- forbidden prompt fields present
- clarification types present
- status email_clarification_bridge_design_ready

## Acceptance result

RESULT=PASS_SPRINT7_EMAIL_CLARIFICATION_BRIDGE_DESIGN_RECORDED
NEXT=email_clarification_bridge_readback_design_only
