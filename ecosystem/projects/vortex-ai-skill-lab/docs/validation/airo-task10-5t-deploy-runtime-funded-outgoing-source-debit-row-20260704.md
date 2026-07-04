# AIRO Finance Validation Report — Task 10.5T

**Date/time:** 2026-07-04 19:16 Asia/Jakarta  
**Status:** PASS  
**Scope:** DEPLOY_AND_RUNTIME_SELF_TEST_ONLY  
**Baseline commit:** 5605673067b5e3005359fc90f3df1c4860c68484  
**Local source SHA256:** ec013f2fb7999caf585427983d6b6e8ef887e437fc5c9e9bec4ab851cc7f1c55  

## 1. Clasp Target Verification
- Script ID: `1JVKcn7cR8K3VNDCP2vxKoJl45aS2u2O9I_TU_hWuNRRbFsuz_e6y3Uf0`
- Target configuration: `apps-script-live/.clasp.json` (prod-v2 target)
- Credentials verified: Yes (`~/.clasprc.json`)

## 2. Clasp Push Output Summary
- Status: Success
- Local changes pushed to Apps Script target.

## 3. Remote Readback & Parity
- Pulled code location: `/tmp/clasp_readback_10_5t`
- Remote SHA256 matches Local SHA256: Yes
- Deployed code contains 10.5S patches (preservation of "Blu Pocket", 3-row write plan, separate account/funding source display).

## 4. Runtime Self-Test Matrix
- Test function: `runTask105OutgoingConfirmationGateSelfTestFromEditor`
- Execution: `npx clasp run` (HEAD)
- Results:
  - `funded_payment_account_outgoing_3_rows`: PASS
  - `funding source OUT row account Blu Pocket`: PASS
  - `payment account IN row Cash Umum`: PASS
  - `payment account OUT expense row Cash Umum`: PASS
  - `same-source SINGLE_OUTGOING 1 row`: PASS
  - `funded prompt display Akun transaksi / Sumber dana`: PASS
  - `normalize validation preserves Blu Pocket`: PASS
  - `numeric account options`: PASS
  - `numeric subcategory options`: PASS
  - `receipt Category > Subcategory`: PASS
  - `outgoing Income / Transfer / CC Payment block`: PASS
  - `forbidden API scan`: PASS

## 5. Web App Deployment Update
- Previous version: unknown  
- New version: 334  
- Deployment ID: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`  
- Deployment update status: SUCCESS  

## 6. Post-Deploy Production Self-Test
- Probe Endpoint: `https://script.google.com/macros/s/AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA/exec?airo_probe=task9_access_gate`
- Probe Result: PASS (successfully returned probe confirmation from deployed web app)

## 7. Webhook / Worker Parity
- Webhook status: YES (Pointed to active web app deployment)

## 8. Governance & Safety Audits
- WORKBOOK_MUTATION: NO
- LEDGER_WRITE: NO
- ACCOUNT_LEDGER_WRITE: NO
- FINANCE_EVENTS_WRITE: NO
- REVIEW_QUEUE_WRITE: NO
- CATEGORY_REGISTRY_MUTATION: NO
- DASHBOARD_MUTATION: NO
- GMAIL_READ: NO
- TELEGRAM_SEND: NO
- TRIGGER_CREATION: NO
- SCHEDULED_TRIGGER: NO
- REAL_TRANSACTION_APPROVAL: NO

## 9. Next Steps
- Owner may run one real Telegram acceptance test manually after reviewing this evidence (e.g. `cash bayar makan rp 1`).
