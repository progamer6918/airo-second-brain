# AIRO Finance Gate P2 Telegram Semantics & Email Numeric Prompt Remediation Plan

- **Marker**: `AIRO_ARFIN_GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_REMEDIATION_PLAN_NO_DEPLOY`
- **Timestamp**: `20260719_165921`
- **Base Commit SHA**: `e2a7058d379e1a6d65245a3a52ff4a3fa6f9fb14`
- **Source SHA256**: `1853e4a8c8ff8b4a1d3b49e163cc62e10983b801ed62af9d5cdb4eb3f930be6a`
- **Active Deployment Version**: `379`
- **Deployment Readback**: PASS
- **Inherited RCA Classification**: `TELEGRAM_ACCOUNT_FUNDING_PARSER_GREEDY_MATCH_AND_DISPLAY_REVERSAL_PLUS_EMAIL_INCOME_LEGACY_ALPHA_PROMPT`
- **Source Symbols Inspected**: `parseAccount_,parseTransaction_,airoBuildOutgoingAccountPromptMessage_,airoBuildSubcategoryGroupedPromptMessage_,airoSprint7FBuildEmailIncomePrompt_`
- **Remediation Plan Status**: READY

## Remediation Plan Core Components
1. **Explicit Contextual Account Parser**: Regex for `akun transaksi <account>` and `sumber dana <account>`.
2. **Greedy Fallback Guard**: Keep `parseAccount_` greedy match only as fallback.
3. **Pending Data Model Invariant**: Keep `pending.account` (execution) distinct from `pending.funding_source_account` (funding source).
4. **Prompt Display Repair**: Render `Akun transaksi: Cash Umum` and `Sumber dana: Blu Pocket` correctly.
5. **Amount Marker Regression Guard**: Ensure numeric timestamp markers do not contaminate nominal amount.
6. **Email Income Numeric Prompt Repair**: Replace `A/B/C/D/E` legacy alpha options with `1. Gaji / income ... 5. Lainnya`.
7. **Local Harness Coverage Extension**: Extend test harness cases to 21/21 PASS.
8. **Execution & Deployment Sequence Plan**: Guarded repair -> local test -> preflight -> deploy -> manual proof -> live Telegram retest -> workbook readback.

## Gate Safety Record
- **Source Patch Performed**: NO
- **Deployment Performed**: NO
- **Clasp Push / Deploy / Run Performed**: NO
- **Apps Script Runtime Executed**: NO
- **Workbook Mutation**: NO
- **Telegram Mutation**: NO
- **Gmail Mutation**: NO
- **Approval Performed**: NO
- **Incident Status**: `AFPD-INC-009=LIVE_TELEGRAM_SEMANTICS_AND_EMAIL_PROMPT_REMEDIATION_PLAN_READY`
- **Recommended Next Gate**: `GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_REPAIR_PREFLIGHT_NO_DEPLOY`
