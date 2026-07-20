# AIRO Finance Gate P2 Email Expense Direction False Inflow v384 Live Email Expense Alpha Prompt Regression Remediation Plan Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_EMAIL_EXPENSE_ALPHA_PROMPT_REGRESSION_REMEDIATION_PLAN_NO_DEPLOY`
- **Timestamp**: `20260720_193337`
- **Base Commit SHA**: `d1895ef5863e386ebfad91df5e94905bc35b52ef`
- **Source SHA256 Deployed**: `c16ae1addcc99fc583e436f7449dde4b6c834ae333ee361ecb02c8ca1c3576d5`
- **Apps Script Version**: `v384`
- **Rollback Version**: `v383`
- **Target Deployment Suffix**: `ZYjuOA`
- **Deployment Readback**: PASS (v384)
- **Local Unit Self-Test**: PASS (46/46)
- **Runtime Proof Status**: `PASS_46_OF_46_ACCEPTED_WITH_APPS_SCRIPT_LOG_TRUNCATION_LIMITATION`
- **Live Retest Status**: `FAIL_LEGACY_ALPHA_PROMPT_REGRESSION`
- **Remediation Plan Status**: `READY`
- **Repair Scope**: `V384_EMAIL_LIVE_DIRECTION_AMBIGUITY_AND_SUBCATEGORY_PROMPT_NUMERIC_RENDERING`
- **Source Target**: `AIRO_Finance_Multitab_Final_v1.js`
- **Harness Target**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745_HARNESS.js`
- **Direction Prompt Target Function**: `airoSprint7FBuildFriendlyClarificationMessage_`
- **Subcategory Prompt Target Function**: `airoSprint7CategoryContractBuildSubcategoryPrompt_`
- **Alpha Display Allowed**: NO
- **Internal Alpha Parser Compatibility Allowed**: YES (stale/in-flight replies only)
- **Numeric Display Required**: YES
- **Numeric Reply Required**: YES
- **Current Test Count**: 46
- **Planned Alpha Prompt Tests**: 11
- **Expected Test Count After Repair**: 57

## Remediation Strategy Overview
The remediation plan addresses the root causes identified in RCA commit `d1895ef5863e386ebfad91df5e94905bc35b52ef`.
1. `airoSprint7FBuildFriendlyClarificationMessage_` will be updated to format direction ambiguity options as numeric digits (`1. Pengeluaran`, `2. Pemasukan`, `3. Transfer...`, `0. Abaikan / Batalkan`).
2. `airoSprint7CategoryContractBuildSubcategoryPrompt_` will be updated to format subcategory choices as numeric digits (`1. Jajan`, `2. Makan di Luar`, `3. Kopi`... `5. Tulis manual / lainnya`).
3. Prompts will strictly display numeric options only.
4. Internal parsers will retain backward-compatible letter parsing (`a`, `b`, `c`...) so that any in-flight prompt replies from earlier cycles do not break.
5. 11 new pure local unit tests will be added to verify numeric direction ambiguity rendering, numeric subcategory rendering, and numeric choice mappings, expanding the self-test suite from 46 to 57 test cases.

## Governance Flags
- **Source Patch Performed**: NO
- **Harness Patch Performed**: NO
- **Deployment Performed**: NO
- **`clasp run` Performed**: NO
- **Apps Script Runtime Executed by Agent**: NO
- **Gmail Accessed / Read by Agent**: NO
- **Poller / Trigger Executed by Agent**: NO
- **Telegram Sent / Replied by Agent**: NO
- **Workbook / Review Queue Mutation**: NO
- **Approval Performed**: NO
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_RETEST_BLOCKED_BY_LEGACY_ALPHA_PROMPT_REGRESSION_REMEDIATION_PLAN_READY_AWAITING_REPAIR_PREFLIGHT`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_EMAIL_EXPENSE_ALPHA_PROMPT_REGRESSION_REPAIR_PREFLIGHT_NO_DEPLOY`
