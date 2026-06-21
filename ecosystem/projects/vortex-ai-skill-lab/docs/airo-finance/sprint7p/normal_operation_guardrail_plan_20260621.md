# Sprint 7P — AIRO Finance Normal Operation Guardrail Plan

This document outlines the operational guardrails, plan, and checklist for the stable normal operation phase of the AIRO Finance Credit Card numbered settlement system.

## 1. Current Stable Baseline
* **Active Deployment Version:** `@306`
* **Active Deployment ID:** `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
* **Active git commit (ASB):** `f2747ca` (or later f2747ca-derived build)
* **Code Parity status:** 100% parity across `apps-script-live`, `apps-script-prod-v2`, and the local mirror `.gs` script.

## 2. Daily Commands Currently Safe for Owner
These commands have been verified via end-to-end smoke testing and are fully safe for production use:
1. `cek tagihan pending cc`
   * Displays unbilled pending credit card transactions mapped to their relative index numbers.
   * Safe, read-only.
2. `cc sudah <nomor>`
   * Settles the pending credit card transaction matching the list index `<nomor>`.
   * Automatically performs ledger-first transfer write (`Blu Pocket` -> `Blu Pocket CC`) and marks row status as `✅ Sudah` with cross-referencing.
   * Fully protected against duplicate settlement writes (idempotency guard).

## 3. Commands Not Yet Guaranteed
These commands are experimental or require further configuration/authorization and should **not** be used in daily operations:
1. `admin task9 repair`
   * Cleans up unvalidated entries or manually repairs registry and ledger rows. Use only during recovery.
2. Direct spreadsheet mutations on `status_pocket_blu` column
   * Manual edits to `Sudah` directly on the Google Sheet without ledger linkage will trigger audit alerts.

## 4. Read-Only Regression Checklist
Before any future updates, the operator must verify:
* [ ] No differences exist between production, live, and mirror script versions.
* [ ] Static regression test suite (`scripts/airo_finance_sprint7o_cc_sudah_static_test.js`) runs and passes completely.
* [ ] Target spreadsheet configuration mapping matches active workbook IDs in script properties.

## 5. Rollback Baseline
If any regression or anomaly is detected in the spreadsheet or Telegram updates:
* Rollback deployment in-place to version `@306` using clasp.
* Command to rollback:
  ```bash
  cd /home/egitaristorandas/vortex-ai-skill-lab/apps-script-live
  npx clasp deploy AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA 306 "Rollback to stable Task 9 CC Sudah baseline"
  ```

## 6. Definition of Done for Sprint 7P
* [x] Verification of stable baseline `@306` deployment.
* [x] Creation of the Normal Operation Guardrail Plan.
* [x] Creation of the Owner Telegram Command Cheat Sheet.
* [x] Documentation committed and pushed to git repo.
* [x] Skip clasp push and deployment since no code changes are introduced.

## 7. Risks and Mitigation
* **Risk: Accidental Live Mutation**
  * *Mitigation:* Only run static tests locally. Do not invoke smoke scripts or mutate production data without explicit instructions.
* **Risk: Duplicate Ledger Write**
  * *Mitigation:* Ensure the `cc_already_settled` block in the webhook handler is active and matches existing ledger row IDs.
* **Risk: Stale Deployment**
  * *Mitigation:* Always verify that target webhook URL matches the deployed version ID.
* **Risk: Dirty Repository**
  * *Mitigation:* Keep `core.filemode false` to ignore file mode changes and stage only explicitly required files.

## 8. Hard Operator Rule
* **DO NOT** rerun destructive live smoke scripts (`smoke_run.py`) unless the Owner explicitly approves or request-gates it.
* All CLI commands must capture outputs to `/tmp/` logs and copy them to the Windows clipboard via `clip.exe`.
