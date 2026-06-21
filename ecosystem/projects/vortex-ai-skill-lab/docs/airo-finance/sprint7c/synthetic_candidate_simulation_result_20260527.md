# AIRO Finance — Sprint 7C Synthetic Candidate Simulation Result

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7C Synthetic Candidate Simulation
Mode: synthetic-only
Deploy performed: false

## Result

RESULT=PASS_SPRINT7C_SYNTHETIC_CANDIDATE_SIMULATION_BUILT
NEXT=sprint7c_synthetic_candidate_simulation_readback_or_closeout

## Summary

Simulation count: 20
Pass count: 20
Fail count: 0
Safe fixtures: 6
Clarification fixtures: 4
Blocked fixtures: 10
Sensitive blocked fixtures: 3
All writes disabled: true

## Guardrails

- Gmail live read performed: false
- Mailbox read performed: false
- Mail trigger created: false
- Email modified: false
- Full email body stored: false
- Raw email forwarded to Telegram: false
- Finance write performed: false

## Fixture results

| # | fixture_id | group | expected_parse | actual_parse | expected_lifecycle | actual_lifecycle | expected_router | actual_router | result |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | s7b_fx_001 | safe_expense_bank | parsed | parsed | ready_for_router | ready_for_router | account_ledger_expense | account_ledger_expense | PASS |
| 2 | s7b_fx_002 | safe_income_bank | parsed | parsed | ready_for_router | ready_for_router | account_ledger_income | account_ledger_income | PASS |
| 3 | s7b_fx_003 | safe_credit_card_purchase | parsed | parsed | ready_for_router | ready_for_router | credit_card_purchase | credit_card_purchase | PASS |
| 4 | s7b_fx_004 | safe_credit_card_payment | parsed | parsed | ready_for_router | ready_for_router | credit_card_payment | credit_card_payment | PASS |
| 5 | s7b_fx_005 | safe_refund_reversal | parsed | parsed | ready_for_router | ready_for_router | refund_or_reversal | refund_or_reversal | PASS |
| 6 | s7b_fx_006 | safe_internal_transfer | parsed | parsed | ready_for_router | ready_for_router | internal_transfer | internal_transfer | PASS |
| 7 | s7b_fx_007 | ambiguous_direction | needs_clarification | needs_clarification | needs_clarification | needs_clarification | no_route | no_route | PASS |
| 8 | s7b_fx_008 | ambiguous_status | needs_clarification | needs_clarification | needs_clarification | needs_clarification | no_route | no_route | PASS |
| 9 | s7b_fx_009 | missing_category | needs_clarification | needs_clarification | needs_clarification | needs_clarification | blocked_missing_field | blocked_missing_field | PASS |
| 10 | s7b_fx_010 | missing_account_mapping | needs_clarification | needs_clarification | needs_clarification | needs_clarification | blocked_missing_field | blocked_missing_field | PASS |
| 11 | s7b_fx_011 | duplicate_candidate | duplicate_candidate | duplicate_candidate | needs_review | needs_review | blocked_duplicate | blocked_duplicate | PASS |
| 12 | s7b_fx_012 | low_confidence_parse | low_confidence | low_confidence | needs_review | needs_review | blocked_low_confidence | blocked_low_confidence | PASS |
| 13 | s7b_fx_013 | sensitive_otp_block | skipped_sensitive | skipped_sensitive | skipped_sensitive | skipped_sensitive | blocked_sensitive | blocked_sensitive | PASS |
| 14 | s7b_fx_014 | sensitive_login_block | skipped_sensitive | skipped_sensitive | skipped_sensitive | skipped_sensitive | blocked_sensitive | blocked_sensitive | PASS |
| 15 | s7b_fx_015 | sensitive_password_reset_block | skipped_sensitive | skipped_sensitive | skipped_sensitive | skipped_sensitive | blocked_sensitive | blocked_sensitive | PASS |
| 16 | s7b_fx_016 | unknown_sender_block | sender_not_allowed | sender_not_allowed | source_contract_blocked | source_contract_blocked | no_route | no_route | PASS |
| 17 | s7b_fx_017 | missing_required_label_block | missing_required_label | missing_required_label | source_contract_blocked | source_contract_blocked | blocked_missing_field | blocked_missing_field | PASS |
| 18 | s7b_fx_018 | failed_transaction_no_write | parsed_failed_no_write | parsed_failed_no_write | needs_review | needs_review | no_route | no_route | PASS |
| 19 | s7b_fx_019 | pending_transaction_no_write | parsed_pending_no_write | parsed_pending_no_write | needs_review | needs_review | no_route | no_route | PASS |
| 20 | s7b_fx_020 | malformed_metadata | malformed_metadata | malformed_metadata | failed | failed | no_route | no_route | PASS |

## Machine-readable artifact

docs/airo-finance/sprint7c/synthetic_candidate_simulation_result_20260527.json

