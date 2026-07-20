# AIRO Finance Gate P2 Email Expense Direction False Inflow v384 Live Email Expense Alpha Prompt Regression RCA Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_EMAIL_EXPENSE_ALPHA_PROMPT_REGRESSION_RCA_NO_DEPLOY`
- **Timestamp**: `20260720_191847`
- **Base Commit SHA**: `f9339cc13f6124768cdacf4b945dc446b8b85c6b`
- **Source SHA256 Deployed**: `c16ae1addcc99fc583e436f7449dde4b6c834ae333ee361ecb02c8ca1c3576d5`
- **Apps Script Version**: `v384`
- **Rollback Version**: `v383`
- **Target Deployment Suffix**: `ZYjuOA`
- **Deployment Readback**: PASS (v384)
- **Local Unit Self-Test**: PASS (46/46)
- **Runtime Proof Status**: `PASS_46_OF_46_ACCEPTED_WITH_APPS_SCRIPT_LOG_TRUNCATION_LIMITATION`
- **Live Retest Status**: `FAIL_LEGACY_ALPHA_PROMPT_REGRESSION`
- **RCA Classification**: `LIVE_EMAIL_AMBIGUOUS_DIRECTION_AND_SUBCATEGORY_PROMPT_PATHS_STILL_USE_LEGACY_ALPHA_RENDERERS_NOT_COVERED_BY_V384_SELFTEST`
- **RCA Confidence**: `HIGH`

## Root Cause Analysis Details

### 1. Direction Ambiguity Prompt Path
- **Function**: `airoSprint7FBuildFriendlyClarificationMessage_(candidateId, candidate)` (Lines 22746 - 22809)
- **Exact Cause**: Lines 22793 - 22802 explicitly hardcode:
  ```javascript
  lines.push("Ini maksudnya apa?");
  lines.push("A. Pengeluaran");
  lines.push("B. Pemasukan");
  lines.push("C. Transfer antar akun sendiri");
  lines.push("D. Abaikan");
  lines.push("Balas A/B/C/D.");
  ```
- **Impact**: When direction is `ambigu`, the prompt instructs the user to reply `A/B/C/D` instead of numeric `1/2/3/0`.

### 2. Subcategory Prompt Path
- **Function**: `airoSprint7CategoryContractBuildSubcategoryPrompt_(category)` (Lines 26346 - 26364)
- **Exact Cause**: Lines 26353 - 26361 loop using `alphabet = "abcdefghijklmnopqrstuvwxyz"` and format options as `A. Jajan`, `B. Makan di Luar`, `C. Kopi`... and `E. Tulis manual / lainnya`.
- **Impact**: After direction resolution, subcategory selection prompts render alpha options `A. B. C. D. E.` instead of numeric `1. 2. 3. 4. 5.`.

### 3. Unit Test Coverage Gap
- The existing 46 unit test cases verified direction inference, numeric expense category prompt for direct expense routes, and numeric parser logic, but did NOT contain test cases validating that `airoSprint7FBuildFriendlyClarificationMessage_` and `airoSprint7CategoryContractBuildSubcategoryPrompt_` output numeric choices only without alpha options.

### 4. Remediation Plan Recommendation
- Update `airoSprint7FBuildFriendlyClarificationMessage_` (direction `ambigu` branch) to render numeric options:
  - `1. Pengeluaran`
  - `2. Pemasukan`
  - `3. Transfer antar akun sendiri`
  - `0. Abaikan / Batalkan`
  - `Balas angka pilihan.`
- Update `airoSprint7CategoryContractBuildSubcategoryPrompt_` to render numeric options `1..N` and `0. Batalkan / Tulis manual`.
- Retain internal parser compatibility for legacy alpha choices if in-flight replies exist, but remove alpha display from all prompt texts.
- Add dedicated unit tests for numeric direction ambiguity prompt and numeric subcategory prompt formatting.

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
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_RETEST_BLOCKED_BY_LEGACY_ALPHA_PROMPT_REGRESSION_RCA_COMPLETED_AWAITING_REMEDIATION_PLAN`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V384_LIVE_EMAIL_EXPENSE_ALPHA_PROMPT_REGRESSION_REMEDIATION_PLAN_NO_DEPLOY`
