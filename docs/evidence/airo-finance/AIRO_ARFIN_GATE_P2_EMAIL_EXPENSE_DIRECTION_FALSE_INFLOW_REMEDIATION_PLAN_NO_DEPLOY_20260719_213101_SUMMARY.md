# AIRO Finance Gate P2 Email Expense Direction False Inflow Remediation Plan Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REMEDIATION_PLAN_NO_DEPLOY`
- **Timestamp**: `20260719_213101`
- **Base Commit SHA**: `d45ee9278ebf91b3471bc64b7b25cb49d93ee446`
- **Source SHA256**: `3070c37f412ced711ebdfe88688a46dd6315af34eb8f94a1cddde1fbf38e2b9a`
- **Apps Script Deployed Version**: `381`
- **Deployment Readback**: PASS
- **Remediation Plan Status**: `READY`
- **Repair Scope**: `EMAIL_DIRECTION_EVIDENCE_COLLECTION_CONTEXTUAL_MATCHING_AND_CONFLICT_RESOLUTION`
- **Proposed Direction Policy**: `STRONG_EVIDENCE_ONLY_GENERIC_UI_TOKENS_NEUTRAL_CONFLICTS_AMBIGUOUS`
- **Current Test Count**: `24`
- **Planned Direction Tests**: `11`
- **Expected Test Count After Repair**: `35`

## Remediation Strategy & Policy
1. **Neutralize Non-Transactional UI Phrases**: Exclude generic UI/footer phrases (e.g. *"masuk ke aplikasi"*, *"login ke aplikasi"*, *"silakan masuk"*) before direction scoring.
2. **Contextual Evidence Collection**: Re-implement `airoSprint7FInferDirection_` to collect explicit inflow and outflow signals rather than returning on first substring match.
3. **Conflict & Ambiguity Policy**:
   - Only strong inflow signals -> `"pemasukan"`
   - Only strong outflow signals -> `"pengeluaran"`
   - Both inflow and outflow signals -> `"ambigu"`
   - Neither -> `"ambigu"`
4. **Candidate Type Rules**: Candidate type `transfer_masuk` serves as strong inflow evidence, but if subject/body contains strong outflow signals, the result maps to `"ambigu"` instead of forcing `"pemasukan"`.
5. **Regression Coverage**: Expand built-in self-test suite from 24 to 35 PASS test cases to validate pure expense, generic login token neutrality, mixed expense/login text, explicit transfer masuk, generic Blu notifications, and conflict resolution.

## Planned Deployment & Proof Sequence
1. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REPAIR_PREFLIGHT_NO_DEPLOY`
2. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REPAIR_EXECUTION_NO_DEPLOY`
3. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_POST_REPAIR_PREFLIGHT_NO_DEPLOY`
4. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_GUARDED_DEPLOYMENT_PREFLIGHT`
5. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_GUARDED_DEPLOYMENT_EXECUTION` (Deploy to v382)
6. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`
7. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_LIVE_EMAIL_EXPENSE_RETEST_PREFLIGHT`
8. `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_LIVE_EMAIL_EXPENSE_RETEST_RECORD`

## Gate Safety Record
- **Source Patch Performed**: NO
- **Harness Patch Performed**: NO
- **Deployment Performed**: NO
- **Clasp Push / Deploy / Run Performed**: NO
- **Apps Script Runtime Executed by Agent**: NO
- **Gmail Accessed / Read by Agent**: NO
- **Telegram Sent by Agent**: NO
- **Workbook / Review Queue Mutation**: NO
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REMEDIATION_PLAN_READY_NO_DEPLOY`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REPAIR_PREFLIGHT_NO_DEPLOY`
