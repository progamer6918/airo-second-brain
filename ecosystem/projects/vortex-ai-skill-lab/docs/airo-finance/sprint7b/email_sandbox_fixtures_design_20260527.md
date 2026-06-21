# AIRO Finance — Sprint 7B Email Sandbox Fixtures Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7B Email Sandbox Fixtures
Mode: design-only
Deploy performed: false

## Purpose

Sprint 7B Email Sandbox Fixtures defines safe synthetic email-like test cases for parser, candidate lifecycle, clarification bridge, and dry-run router validation.

This phase must prove behavior without reading Gmail, touching mailbox state, or writing finance data.

## Current state

Sprint 7 Email Ingestion dry-run design chain is closed through Email Dry Run Router.

Latest carry-over commit:

784037f docs(airo-finance): record Sprint 7 carry over

Recommended next phase:

Sprint 7B Email Sandbox Fixtures

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

- synthetic fixture design
- fixture matrix documentation
- fake email metadata payloads
- fake parser inputs
- expected dry-run outcomes
- expected block reasons
- static tests
- direct Web App dry-run readback if command is later implemented

## Fixture principle

Fixtures must be synthetic.

Fixtures must not contain real email bodies.

Fixtures must not contain real OTP, auth code, login link, full card number, full account number, or private security content.

Fixtures may contain fake metadata such as:

- fake provider
- fake merchant
- fake amount
- fake date
- fake card last4
- fake subject hash
- fake message id
- fake thread id

## Fixture categories

Required fixture categories:

1. safe_expense_bank
2. safe_income_bank
3. safe_credit_card_purchase
4. safe_credit_card_payment
5. safe_refund_reversal
6. safe_internal_transfer
7. ambiguous_direction
8. ambiguous_status
9. missing_category
10. missing_account_mapping
11. duplicate_candidate
12. low_confidence_parse
13. sensitive_otp_block
14. sensitive_login_block
15. sensitive_password_reset_block
16. unknown_sender_block
17. missing_required_label_block
18. failed_transaction_no_write
19. pending_transaction_no_write
20. malformed_metadata

## Fixture required fields

Each fixture must define:

- fixture_id
- fixture_group
- source_id
- sender_profile
- required_label_present
- fake_message_id
- fake_thread_id
- fake_subject_hash
- received_at
- detected_amount
- detected_date
- detected_merchant
- detected_last4
- detected_direction
- detected_status
- parser_confidence
- sensitivity_status
- expected_parse_status
- expected_lifecycle_state
- expected_clarification_type
- expected_router_destination
- expected_block_reason
- expected_write_allowed
- expected_write_performed
- notes

## Required constants

Every fixture must assert:

- Gmail read performed: false
- mailbox read performed: false
- mail trigger created: false
- email modified: false
- full email body stored: false
- raw email forwarded to Telegram: false
- finance write performed: false
- write allowed: false
- write performed: false

## Expected safe fixture examples

### safe_expense_bank

Input:

BCA transaksi Rp240000 di Tokopedia berhasil

Expected:

- sensitivity_status: safe
- lifecycle_state: ready_for_router
- expected_router_destination: account_ledger_expense
- expected_write_allowed: false
- expected_write_performed: false

### safe_credit_card_purchase

Input:

Credit card purchase Starbucks Rp58000 approved

Expected:

- sensitivity_status: safe
- lifecycle_state: ready_for_router
- expected_router_destination: credit_card_purchase
- expected_write_allowed: false
- expected_write_performed: false

### safe_refund_reversal

Input:

Refund reversal Rp75000 merchant Tokopedia kartu kredit

Expected:

- sensitivity_status: safe
- lifecycle_state: ready_for_router
- expected_router_destination: refund_or_reversal
- expected_write_allowed: false
- expected_write_performed: false

## Expected block fixture examples

### sensitive_otp_block

Input:

Kode OTP Anda 123456 untuk transaksi

Expected:

- sensitivity_status: sensitive
- expected_parse_status: skipped_sensitive
- expected_lifecycle_state: skipped_sensitive
- expected_router_destination: blocked_sensitive
- expected_write_allowed: false
- expected_write_performed: false

### missing_required_label_block

Input:

Valid-looking bank transaction without Finance/ToProcess label

Expected:

- expected_parse_status: missing_required_label
- expected_lifecycle_state: source_contract_blocked
- expected_router_destination: blocked_missing_field
- expected_write_allowed: false
- expected_write_performed: false

### unknown_sender_block

Input:

Valid-looking payment email from unknown sender

Expected:

- expected_parse_status: sender_not_allowed
- expected_lifecycle_state: source_contract_blocked
- expected_router_destination: no_route
- expected_write_allowed: false
- expected_write_performed: false

## Quality gate

Sprint 7B fixtures are acceptable only if they cover:

- at least 20 synthetic fixtures
- positive safe candidates
- clarification-needed candidates
- blocked sensitive candidates
- blocked source-contract candidates
- blocked duplicate candidates
- no-write policy for every fixture
- no real email body
- no real OTP/security data
- no real full card number
- no real full account number

## Future readback target

Future Telegram command:

admin email sprint7b sandbox fixtures

Expected readback must prove:

- design only true
- synthetic fixtures only true
- write performed false
- write allowed false
- email ingestion enabled false
- default off true
- dry-run only true
- Gmail read performed false
- mailbox read performed false
- mail trigger created false
- email modified false
- full email body stored false
- sensitive content stored false
- raw email forwarded false
- finance write performed false
- fixture categories present
- required fixture fields present
- fixture minimum count target present
- status email_sandbox_fixtures_design_ready

## Acceptance result

RESULT=PASS_SPRINT7B_EMAIL_SANDBOX_FIXTURES_DESIGN_RECORDED
NEXT=sprint7b_email_sandbox_fixtures_readback_design_only
