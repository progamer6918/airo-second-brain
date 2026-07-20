# AIRO Finance Gate P2 Email Expense Direction False Inflow v384 Live Email Expense Alpha Prompt Regression State Machine Remediation Plan Amendment Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_EMAIL_EXPENSE_ALPHA_PROMPT_REGRESSION_STATE_MACHINE_REMEDIATION_PLAN_AMENDMENT_NO_DEPLOY`
- **Timestamp**: `20260720_195918`
- **Base Commit SHA**: `b1a98efc075d369d5d6045bfa6967a569cf3a4f4`
- **Source SHA256**: `c16ae1addcc99fc583e436f7449dde4b6c834ae333ee361ecb02c8ca1c3576d5`
- **Apps Script Version**: `v384`
- **Rollback Version**: `v383`
- **Target Deployment Suffix**: `ZYjuOA`
- **Deployment Readback**: PASS (v384)
- **Local Unit Self-Test**: PASS (46/46)
- **RCA Addendum Classification**: `LIVE_EMAIL_DIRECTION_PROMPT_RENDERER_AND_PENDING_STATE_MACHINE_ARE_INCONSISTENT_AMBIGUOUS_REPLY_IS_HANDLED_AS_EXPENSE_CATEGORY_SELECTION`
- **RCA Addendum Confidence**: `HIGH`
- **Live Behavior Explained by Source**: YES
- **Amended Repair Scope**: `V384_EMAIL_LIVE_DIRECTION_AMBIGUITY_PENDING_STATE_MACHINE_AND_NUMERIC_PROMPT_RENDERING`
- **Renderer-Only Repair Contract Status**: `SUPERSEDED_INCOMPLETE`
- **State Machine Repair Required**: YES
- **Amended Remediation Plan Status**: `READY`
- **Current Test Count**: 46
- **Planned Alpha Prompt Tests**: 11
- **Planned State Machine Tests**: 8
- **Total Planned New Tests**: 19
- **Expected Test Count After Repair**: 65

## Root Cause Addendum & State Machine Proof
Static source analysis confirms that the live v384 alpha prompt regression is NOT merely a prompt renderer display issue.
1. In `airoSprint7FSavePendingPointer_`, candidate payloads are saved with:
   ```javascript
   clarification_state: String(candidate.inferred_direction).toLowerCase() === "pengeluaran" ? "account_pending" : "category_pending"
   ```
   Because `candidate.inferred_direction` is `"ambigu"`, it evaluates to `false`, saving the pending candidate into `"category_pending"` state.
2. Candidate fields `inferred_direction` and `clarification_question_type` are NOT persisted in the script properties payload.
3. In `"category_pending"`, choice `1` or choice `A` maps directly to `Food & Drink` category.
4. Consequently, when the Owner replied `a` to the direction prompt (`A. Pengeluaran`), the handler in `"category_pending"` processed `a` as selecting `Food & Drink`, immediately outputting: `Pilih subkategori untuk Food & Drink:`.
5. Replacing display labels `A/B/C/D` with `1/2/3/4` without fixing the state machine would cause replying `1` to ALSO be processed as selecting `Food & Drink`.
6. Therefore, the state machine MUST be amended to introduce explicit `direction_pending` handling for candidates with ambiguous direction before category resolution.

## Amended Repair Plan Scope
1. **Pending Pointer Repair**: Update `airoSprint7FSavePendingPointer_` to persist `inferred_direction` and set `clarification_state: "direction_pending"` for ambiguous candidates.
2. **State Machine Handler**: Introduce explicit `direction_pending` route in `airoSprint7FEmailAnswerMaybeHandleRoute_` to transition `1` (`pengeluaran`) -> `account_pending`, `2` (`pemasukan`) -> income clarification, `3` (`transfer`) -> transfer clarification, and `0` -> safe cancel.
3. **Numeric Prompt Renderers**: Render numeric choices only (`1..N`, `0`) for direction and subcategory prompts.
4. **Internal Parser Compatibility**: Retain internal alpha reply parsing (`a`, `b`, `c`...) for stale/in-flight replies.
5. **Test Suite Expansion**: Add 11 prompt renderer tests + 8 state machine tests (total 19 new tests), expanding the suite from 46 to 65 test cases.

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
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_RETEST_BLOCKED_BY_ALPHA_PROMPT_STATE_MACHINE_MISALIGNMENT_AMENDED_PLAN_READY`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_EMAIL_EXPENSE_ALPHA_PROMPT_REGRESSION_REVISED_REPAIR_PREFLIGHT_NO_DEPLOY`
