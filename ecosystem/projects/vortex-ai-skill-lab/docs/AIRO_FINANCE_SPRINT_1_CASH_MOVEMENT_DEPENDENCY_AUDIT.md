# AIRO Finance — Sprint 1 Cash Movement Dependency Audit

Status: AUDIT + REGRESSION  
Sprint: Sprint 1 — Account Ledger Hardening  
Scope: cash movement into Account Ledger  
Runtime change in this micro-step: No production logic change; regression corrected to match actual orchestration surface

## Result Target

This micro-step verifies the Sprint 1 rule:

- cash movement must be visible in Account Ledger
- Account Ledger is wallet movement source-of-truth
- Cash Ledger compatibility must not be deleted in Sprint 1
- Cash Ledger deletion remains Sprint 3

## Active Runtime Surface

Primary source:

- `scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs`

Relevant functions:

- `writeCashLedger_`
- `writeAccountLedgerMirror_`
- `ensureAccountLedgerSheet_`

## Contract Locked by Regression

Regression file:

- `tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py`

Locked expectations:

- Cash route orchestration calls `writeCashLedger_` and then mirrors the movement with `writeAccountLedgerMirror_`.
- Cash movement uses `AIRO_CONFIG.tabs.cash` as `source_tab` evidence.
- `writeAccountLedgerMirror_` writes directly to Account Ledger through `ensureAccountLedgerSheet_` and `appendByHeader_`.
- Account Ledger mirror preserves `amount_in` / `amount_out` direction.
- Account Ledger mirror preserves `source_tab`.
- Account Ledger mirror preserves `linked_txn_id`, falling back to `entryId`.
- Sprint 1 does not delete Cash Ledger.

## Boundary

This is not Sprint 3.

No Cash Ledger deletion, historical migration, dashboard migration, or Finance Events implementation belongs in this micro-step.

## Next Action

If this regression passes, the next smallest Sprint 1 gap is either:

1. Audit CC payment wallet outflow into Account Ledger, or
2. Audit asset/debt payment wallet outflow into Account Ledger.

Pick the smaller gap based on source evidence.


## Regression Correction

Initial regression incorrectly assumed `writeCashLedger_` directly calls `writeAccountLedgerMirror_`.

Actual runtime architecture:

1. Cash route writes the Cash Ledger compatibility row through `writeCashLedger_`.
2. The route orchestration then calls `writeAccountLedgerMirror_` with `AIRO_CONFIG.tabs.cash` as `source_tab`.
3. `writeAccountLedgerMirror_` writes the Account Ledger row using `appendByHeader_`.

This keeps Cash Ledger as compatibility evidence while Account Ledger receives the wallet movement mirror.
