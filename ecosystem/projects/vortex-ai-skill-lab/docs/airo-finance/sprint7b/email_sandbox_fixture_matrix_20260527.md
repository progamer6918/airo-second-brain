# AIRO Finance — Sprint 7B Email Sandbox Fixture Matrix

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7B Email Sandbox Fixtures
Mode: synthetic-only fixture matrix
Deploy performed: false

## Result

RESULT=PASS_SPRINT7B_EMAIL_SANDBOX_FIXTURE_MATRIX_BUILT
NEXT=sprint7b_fixture_matrix_readback_or_phase_closeout

## Guardrails

- Gmail live read performed: false
- Mailbox read performed: false
- Mail trigger created: false
- Email modified: false
- Full email body stored: false
- Raw email forwarded to Telegram: false
- Finance write performed: false
- Write allowed for all fixtures: false
- Write performed for all fixtures: false

## Fixture coverage

Fixture count: 20

| # | fixture_id | group | expected_parse_status | lifecycle | router_destination | block_reason |
|---:|---|---|---|---|---|---|
| 1 | s7b_fx_001 | safe_expense_bank | parsed | ready_for_router | account_ledger_expense |  |
| 2 | s7b_fx_002 | safe_income_bank | parsed | ready_for_router | account_ledger_income |  |
| 3 | s7b_fx_003 | safe_credit_card_purchase | parsed | ready_for_router | credit_card_purchase |  |
| 4 | s7b_fx_004 | safe_credit_card_payment | parsed | ready_for_router | credit_card_payment |  |
| 5 | s7b_fx_005 | safe_refund_reversal | parsed | ready_for_router | refund_or_reversal |  |
| 6 | s7b_fx_006 | safe_internal_transfer | parsed | ready_for_router | internal_transfer |  |
| 7 | s7b_fx_007 | ambiguous_direction | needs_clarification | needs_clarification | no_route | direction_unclear |
| 8 | s7b_fx_008 | ambiguous_status | needs_clarification | needs_clarification | no_route | status_unclear |
| 9 | s7b_fx_009 | missing_category | needs_clarification | needs_clarification | blocked_missing_field | category_required_but_missing |
| 10 | s7b_fx_010 | missing_account_mapping | needs_clarification | needs_clarification | blocked_missing_field | account_mapping_missing |
| 11 | s7b_fx_011 | duplicate_candidate | duplicate_candidate | needs_review | blocked_duplicate | duplicate_risk_exists |
| 12 | s7b_fx_012 | low_confidence_parse | low_confidence | needs_review | blocked_low_confidence | parser_confidence_too_low |
| 13 | s7b_fx_013 | sensitive_otp_block | skipped_sensitive | skipped_sensitive | blocked_sensitive | sensitive_content_detected |
| 14 | s7b_fx_014 | sensitive_login_block | skipped_sensitive | skipped_sensitive | blocked_sensitive | sensitive_content_detected |
| 15 | s7b_fx_015 | sensitive_password_reset_block | skipped_sensitive | skipped_sensitive | blocked_sensitive | sensitive_content_detected |
| 16 | s7b_fx_016 | unknown_sender_block | sender_not_allowed | source_contract_blocked | no_route | source_contract_failed |
| 17 | s7b_fx_017 | missing_required_label_block | missing_required_label | source_contract_blocked | blocked_missing_field | required_label_missing |
| 18 | s7b_fx_018 | failed_transaction_no_write | parsed_failed_no_write | needs_review | no_route | status_failed_no_write |
| 19 | s7b_fx_019 | pending_transaction_no_write | parsed_pending_no_write | needs_review | no_route | status_pending_no_write |
| 20 | s7b_fx_020 | malformed_metadata | malformed_metadata | failed | no_route | malformed_metadata |

## Machine-readable artifact

docs/airo-finance/sprint7b/email_sandbox_fixture_matrix_20260527.json

## Acceptance

All fixtures are synthetic and assert no write behavior.

