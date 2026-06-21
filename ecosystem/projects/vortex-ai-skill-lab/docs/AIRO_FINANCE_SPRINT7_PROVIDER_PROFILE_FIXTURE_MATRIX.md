# AIRO Finance Sprint 7 - Provider Profile and Fixture Matrix Design

Status: DESIGN ONLY.

This document defines the next Sprint 7 phase after manual sample preview closeout.

No Gmail live read is allowed in this phase.

No mailbox read is allowed in this phase.

No Gmail or mail trigger is allowed in this phase.

No finance write is allowed in this phase.

No Account Ledger, Finance Events, or Review Queue write is allowed in this phase.

Email ingestion remains default OFF.

## Purpose

The goal is to define provider profiles and expected parser outputs before any live mailbox integration.

This phase prepares:

- provider pattern catalog
- sender allowlist design
- Gmail label/filter design
- fixture matrix
- _AIRO_Email_Ingestion_Log field refinement
- dry-run-only parser confidence rules

This phase does not enable live email ingestion.

## Global Safety Contract

Required invariant:

- email_ingestion_enabled: false
- dry_run_only: true
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

## Provider Profile Contract

Each provider profile must define:

- provider_id
- provider_name
- source_channel
- allowed_sender_patterns
- required_label
- subject_positive_patterns
- subject_negative_patterns
- body_or_snippet_positive_patterns
- body_or_snippet_negative_patterns
- sensitive_hard_block_keywords
- amount_patterns
- date_patterns
- merchant_patterns
- payment_method_patterns
- status_patterns
- direction_patterns
- category_hint_patterns
- confidence_rules
- duplicate_key_parts
- required_preview_fields
- parse_status_map
- next_action_rules

## Required Preview Fields

Every preview object must keep these fields:

- source_message_id
- sender
- subject
- received_at
- merchant
- amount
- currency
- transaction_date
- payment_method
- category_guess
- confidence
- duplicate_key
- needs_review_reason
- parse_status
- sensitive_skip_reason

## Parse Status Values

Allowed values:

- skipped_sensitive
- blocked_source_contract
- not_finance_candidate
- candidate_low_confidence
- candidate_needs_clarification
- candidate_duplicate_dry_run
- candidate_ready_preview_only

No parse status may imply finance write in this phase.

## Provider Profiles v1

### Provider: BCA Transaction Notification

provider_id: bca_transaction_notification

source_channel: email_bca

allowed_sender_patterns:

- design-only placeholder, must be filled from real trusted sender later
- no wildcard live allowlist yet

required_label:

- Finance/ToProcess design placeholder

positive patterns:

- BCA
- transaksi
- Rp
- transfer
- debit
- pembayaran

negative hard-block patterns:

- otp
- kode
- verifikasi
- login
- security
- password
- reset
- perangkat
- device
- one time password
- 2fa
- authentication
- auth code
- kode keamanan

expected behavior:

- If sensitive keyword appears, return skipped_sensitive before finance parsing.
- If amount and payment method exist but category is missing, return candidate_needs_clarification.
- Do not write to any sheet.

### Provider: Blu Transaction Notification

provider_id: blu_transaction_notification

source_channel: email_blu

allowed_sender_patterns:

- design-only placeholder, must be filled from real trusted sender later
- no wildcard live allowlist yet

required_label:

- Finance/ToProcess design placeholder

positive patterns:

- blu
- debit
- transaksi
- Rp
- merchant
- pembayaran

negative hard-block patterns:

- same global sensitive hard-block list

expected behavior:

- Known food/cafe merchant or keyword can guess Makan.
- Missing merchant or category must lower confidence or need clarification.
- Do not write to any sheet.

### Provider: Credit Card Purchase Notification

provider_id: credit_card_purchase_notification

source_channel: email_cc

allowed_sender_patterns:

- design-only placeholder, must be filled from real trusted sender later
- no wildcard live allowlist yet

required_label:

- Finance/ToProcess design placeholder

positive patterns:

- credit card
- kartu kredit
- cc
- purchase
- transaksi
- merchant
- Rp

negative hard-block patterns:

- same global sensitive hard-block list

expected behavior:

- Credit card purchase should not directly create Account Ledger outflow.
- Preview only can show payment_method Credit Card.
- Routing remains forbidden in this phase.
- Do not write to Credit Card tab yet.

### Provider: Refund or Reversal Notification

provider_id: refund_reversal_notification

source_channel: email_cc or email_bca or email_blu

allowed_sender_patterns:

- design-only placeholder, must be filled from real trusted sender later

positive patterns:

- refund
- reversal
- pengembalian
- reversed
- dikembalikan

expected behavior:

- category_guess should be Refund.
- status should remain preview-only.
- Ambiguous destination account must require clarification later.
- Do not write to any sheet.

### Provider: Failed Transaction Notification

provider_id: failed_transaction_notification

source_channel: email_bca or email_blu or email_cc

positive patterns:

- failed
- gagal
- declined
- ditolak
- tidak berhasil

expected behavior:

- Failed transactions must not be written as expense.
- Preview should set parse_status candidate_needs_clarification or not_finance_candidate depending on fields.
- Do not write to Account Ledger.
- Do not write to Finance Events.

### Provider: OTP or Security Notification

provider_id: otp_security_notification

source_channel: email_security

positive patterns:

- otp
- kode
- verifikasi
- login
- security
- password
- reset
- perangkat
- device
- one time password
- 2fa
- authentication
- auth code
- kode keamanan

expected behavior:

- Always skipped_sensitive.
- amount must be 0.
- merchant must be blank.
- payment_method must be blank.
- category_guess must be blank.
- confidence must be 0.
- no finance parsing after sensitive detection.
- do not send OTP/security content to Telegram beyond safe skipped_sensitive metadata.
- do not write to any sheet.

## Fixture Matrix v1

### Fixture 1 - Blu food merchant

Input:

admin email sprint7 sample preview Blu debit notification sample Rp125000 merchant Kopi Kenangan

Expected:

- provider_id: blu_transaction_notification
- merchant: Kopi Kenangan
- amount: 125000
- currency: IDR
- payment_method: Blu
- category_guess: Makan
- confidence: 100
- parse_status: candidate_ready_preview_only
- write_performed: false

### Fixture 2 - BCA transfer or generic transaction missing category

Input:

admin email sprint7 sample preview BCA transaksi Rp240000 di Tokopedia

Expected:

- provider_id: bca_transaction_notification
- merchant: Tokopedia
- amount: 240000
- currency: IDR
- payment_method: BCA
- category_guess: blank
- confidence: 85
- needs_review_reason: missing_category_guess
- parse_status: candidate_needs_clarification
- write_performed: false

### Fixture 3 - Credit Card cafe purchase

Input:

admin email sprint7 sample preview credit card purchase at Starbucks Rp58000

Expected:

- provider_id: credit_card_purchase_notification
- merchant: Starbucks
- amount: 58000
- currency: IDR
- payment_method: Credit Card
- category_guess: Makan
- confidence: 100
- parse_status: candidate_ready_preview_only
- write_performed: false

### Fixture 4 - Refund or reversal

Input:

admin email sprint7 sample preview refund reversal Rp75000 merchant Tokopedia kartu kredit

Expected:

- provider_id: refund_reversal_notification
- merchant: Tokopedia
- amount: 75000
- currency: IDR
- payment_method: Credit Card
- category_guess: Refund
- confidence: 100
- parse_status: candidate_ready_preview_only
- write_performed: false

### Fixture 5 - OTP or security hard-block

Input:

admin email sprint7 sample preview OTP kode verifikasi login 123456 dari BCA jangan bagikan kode ini

Expected:

- provider_id: otp_security_notification
- merchant: blank
- amount: 0
- currency: blank
- payment_method: blank
- category_guess: blank
- confidence: 0
- parse_status: skipped_sensitive
- sensitive_skip_reason: blocked_keyword_otp
- write_performed: false

## _AIRO_Email_Ingestion_Log Design Refinement

The hidden/backend log may be introduced later, but not written yet in this phase.

Design fields:

- email_log_id
- message_id_hash
- thread_id_hash
- source_id
- provider_id
- from_email
- subject_hash
- received_at
- processed_at
- parse_status
- parse_confidence
- detected_amount
- detected_currency
- detected_date
- detected_merchant
- detected_payment_method
- detected_category_guess
- detected_last4
- sensitive_skip_reason
- duplicate_key
- clarification_ref
- event_ref
- review_queue_ref
- error_message
- notes

Forbidden log content:

- full email body
- OTP code
- password reset code
- full card number
- full account number
- raw sensitive subject/body

## Sender Allowlist Design

Allowed sender list must remain empty until user provides trusted real sender values.

Rules:

- no wildcard domain allowlist for live ingestion
- no live scan until allowlist exists
- sender must be exact or tightly scoped
- sender changes must be audit logged later
- unknown sender must return blocked_source_contract

## Gmail Label and Filter Design

Required label placeholder:

- Finance/ToProcess

Rules:

- no trigger install yet
- no markRead
- no delete
- no archive
- no modify email
- no live read until explicit later phase
- manual Gmail filter setup must be user-approved later

## Duplicate Key Design

Duplicate key should include:

- provider_id
- message_id_hash if available
- sender
- subject_hash
- amount
- merchant
- transaction_date
- payment_method

If message_id_hash is missing in manual sample mode, duplicate key can use sample subject hash.

## Confidence Rules v1

Suggested confidence scoring:

- amount detected: +30
- merchant detected: +20
- payment method detected: +20
- category detected: +15
- safe non-sensitive sample: +15

Sensitive email:

- confidence must be 0
- parse_status must be skipped_sensitive

Missing category:

- parse_status candidate_needs_clarification
- not clean write

High confidence preview:

- parse_status candidate_ready_preview_only
- still no write in this phase

## Next Valid Step

Implement Telegram command for provider fixture matrix readback only:

admin email sprint7 fixture matrix

Expected behavior:

- returns this design summary
- dry-run only
- no Gmail read
- no trigger
- no finance write
- no sheet write

Still forbidden:

- Gmail live read
- Gmail trigger install
- Email-to-ledger write
- Email-to-Finance Events write
- Review Queue write from email
- Full body storage
- Auto-post from email

## Result

RESULT=PASS_SPRINT7_PROVIDER_FIXTURE_MATRIX_DESIGN_READY
