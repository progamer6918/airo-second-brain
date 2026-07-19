# AIRO Finance Gate P2 Email Expense Category Numeric Prompt Remediation Plan Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REMEDIATION_PLAN_NO_DEPLOY`
- **Timestamp**: `20260719_191211`
- **Base Commit SHA**: `5459779c9efc19e91966068d256192553a07fd68`
- **Source SHA256**: `13aee22cc75cfa5c2d01c821bd048481adf63393e0c88caa204eefcd94074e4c`
- **Apps Script Deployed Version**: `380`
- **Deployment Readback**: PASS
- **Telegram Live Retest Status**: `PASS_WORKBOOK_READBACK_PENDING`
- **Email Income Numeric Prompt**: PASS
- **Email Expense Category Numeric Prompt**: `FAIL_LEGACY_A_B_C_D_E_DISPLAYED`
- **RCA Classification**: `EMAIL_EXPENSE_CATEGORY_PROMPT_LEGACY_ALPHA_DISPLAY_PATH_NOT_INCLUDED_IN_PREVIOUS_EMAIL_INCOME_NUMERIC_REPAIR`
- **RCA Confidence**: `HIGH`
- **Remediation Plan Status**: `READY`

## Detailed Remediation Plan

### 1. Source Repair Scope
Target symbols in `AIRO_Finance_Multitab_Final_v1.js`:
- `airoSprint7FDAnswerChoice_` (line 23094): Update `category_expense` map keys to numeric `"1".."5"` (`1: Food & Drink`, `2: Transport`, `3: Groceries`, `4: Utilities`, `5: Cari kategori / lihat bantuan`). Silently preserve backward-compatible `A..E` keys for input parsing.
- `airoSprint7H` (line 23727): Update `categoryMap` in email clarification reply handler to accept numeric keys `"1".."4"` mapping to category strings (`1: Food & Drink`, etc.), while silently preserving `A..D`.
- `airoSprint7FDInferAction_` (line 23313): Update choice check for `category_expense` to accept choices `"1".."5"` (and `"A".."E"`).
- Instruction line text: Update rendered instruction to `Balas angka pilihan.`.

### 2. Required New Harness Test Cases
Extend `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745_HARNESS.js`:
1. `email_expense_category_prompt_numeric_not_alpha`: Assert rendered prompt includes `1. Food & Drink` .. `5. Cari...` and `Balas angka pilihan.`, and does NOT contain `A. Food & Drink` or `Balas A/B/C/D/E.`.
2. `email_expense_category_numeric_choice_maps_food_drink`: Assert choice `"1"` maps to `Food & Drink` (and silent `"A"` remains compatible).
3. `email_expense_category_numeric_choice_help_option`: Assert choice `"5"` maps to help/search (and silent `"E"` remains compatible).

Total self-test cases after repair will increase from 21/21 to 24/24 PASS.

### 3. Execution & Deployment Pipeline
1. `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REPAIR_PREFLIGHT_NO_DEPLOY`
2. `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REPAIR_EXECUTION_NO_DEPLOY`
3. `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_POST_REPAIR_PREFLIGHT_NO_DEPLOY`
4. `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_GUARDED_DEPLOYMENT_PREFLIGHT`
5. `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_GUARDED_DEPLOYMENT_EXECUTION`
6. `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`
7. Live Email Retest & Workbook Readback.

## Gate Safety Record
- **Source Patch Performed**: NO
- **Deployment Performed**: NO
- **Clasp Push / Deploy / Run Performed**: NO
- **Apps Script Runtime Executed by Agent**: NO
- **Telegram Message Sent by Agent**: NO
- **Email Prompt Replied by Agent**: NO
- **Workbook Mutation**: NO
- **Gmail Mutation**: NO
- **Approval Performed**: NO
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REMEDIATION_PLAN_READY_NO_DEPLOY`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REPAIR_PREFLIGHT_NO_DEPLOY`
