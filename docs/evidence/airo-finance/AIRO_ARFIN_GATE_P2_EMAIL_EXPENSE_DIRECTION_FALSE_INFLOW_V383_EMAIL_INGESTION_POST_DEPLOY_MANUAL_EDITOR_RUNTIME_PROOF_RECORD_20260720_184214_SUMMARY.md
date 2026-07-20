# AIRO Finance Gate P2 Email Expense Direction False Inflow v383 Email Ingestion Post-Deploy Manual Editor Runtime Proof Record Summary

- **Marker**: `AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF_RECORD`
- **Timestamp**: `20260720_184214`
- **Base Commit SHA**: `9b8f1a0675711826bdafa8af8b19f7c21e9242e3`
- **Source SHA256 Deployed**: `c16ae1addcc99fc583e436f7449dde4b6c834ae333ee361ecb02c8ca1c3576d5`
- **Apps Script Version**: `v384`
- **Rollback Version**: `v383`
- **Target Deployment Suffix**: `ZYjuOA`
- **Deployment Readback**: PASS (v384)
- **Local Unit Self-Test**: PASS (46/46)
- **Owner Runtime Proof Function**: `runTask105OutgoingConfirmationGateSelfTestFromEditor`
- **Owner Execution Start**: `2026-07-20 18:35:15 WIB`
- **Owner Execution Finish**: `2026-07-20 18:35:24 WIB`
- **Top-Level Status in Log**: `PASS`
- **Mutation Scope**: `OUTGOING_CONFIRMATION_GATE_SELFTEST`
- **Apps Script Log Truncation Warning**: `2026-07-20 18:35:24 WIB: Logging output too large. Truncating output.`
- **Runtime Log Truncated**: YES
- **Full Raw JSON Captured**: NO
- **Full 46-Case List Visible in Log**: NO
- **Owner Manual Editor Runtime Proof Status**: `PASS_46_OF_46_ACCEPTED_WITH_APPS_SCRIPT_LOG_TRUNCATION_LIMITATION`
- **Accepted with Limitation**: `YES_WITH_LIMITATION`

## Runtime Proof Assessment
The Owner manually executed `runTask105OutgoingConfirmationGateSelfTestFromEditor` on deployed version `v384` in the Apps Script editor. The execution completed successfully in 9 seconds with status `PASS` under mutation scope `OUTGOING_CONFIRMATION_GATE_SELFTEST`. Due to Apps Script's built-in log size limit, the JSON output was truncated by the editor console after printing initial test cases. The runtime proof is accepted with the explicit limitation that top-level execution succeeded (`PASS`), but full raw 46-case JSON was not captured due to platform log truncation.

## Governance Flags
- **Source Patch Performed**: NO
- **Harness Patch Performed**: NO
- **Deployment Performed by this Gate**: NO
- **`clasp run` Performed**: NO
- **Apps Script Runtime Executed by Owner**: YES
- **Apps Script Runtime Executed by Agent**: NO
- **Gmail Accessed / Read by Agent**: NO
- **Poller / Trigger Executed by Agent**: NO
- **Telegram Sent / Replied by Agent**: NO
- **Workbook / Review Queue Mutation**: NO
- **Live Email Expense Retest Status**: `NOT_YET_PERFORMED_AFTER_INGESTION_REPAIR_RUNTIME_PROOF`
- **Incident Status**: `AFPD-INC-009=EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_REPAIR_DEPLOYED_RUNTIME_PROOF_RECORDED_AWAITING_LIVE_EMAIL_EXPENSE_RETEST`
- **Recommended Next Gate**: `GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_LIVE_EMAIL_EXPENSE_RETEST_PREFLIGHT`
