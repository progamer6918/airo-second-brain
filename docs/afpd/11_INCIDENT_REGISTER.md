# 11_INCIDENT_REGISTER.md

## Incidents Register

### Incident 1 — Old A/B/C/D/E Email Prompt at 08:51
- **incident_id**: INC_001
- **detected_at**: 2026-07-12 08:51 UTC
- **symptom**: Email expense prompts still displayed A/B/C/D/E letters instead of numeric options.
- **impact**: Confused users expecting the numeric Arfin prompt interface.
- **root_cause**: Legacy webhook endpoint connected to an unpatched development environment.
- **repair**: Forensic isolation of the webhook, routing to active multitab handler.
- **verification**: Check transaction triggers.
- **status**: RESOLVED
- **related_versions**: v370
- **related_evidence**: 08:51 runtime log capture
- **remaining_risk**: Inactive legacy endpoints.

### Incident 2 — Account Reply "2" Not Routed
- **incident_id**: INC_002
- **detected_at**: 2026-07-10 12:50 UTC
- **symptom**: Replying with numeric option "2" failed to resolve.
- **impact**: Blocked account resolution for selected option.
- **root_cause**: Parser checked string arrays instead of normal category strings.
- **repair**: Convert replies to strings before registry array parsing.
- **verification**: Selftest check cases.
- **status**: RESOLVED
- **related_versions**: v371
- **related_evidence**: test case `numeric_account_ux`
- **remaining_risk**: Array bounds check issues.

### Incident 3 — Typed "Blu Pocket" Resolving as "Blu"
- **incident_id**: INC_003
- **detected_at**: 2026-07-10 13:12 UTC
- **symptom**: User input "Blu Pocket" matched substring "Blu" instead of full name.
- **impact**: Routed transaction funding from wrong account.
- **root_cause**: Substring regex checked before exact match registry parser.
- **repair**: Shift exact match checks to higher priority level.
- **verification**: Selftest validation.
- **status**: RESOLVED
- **related_versions**: v374
- **related_evidence**: v374 diff
- **remaining_risk**: Regex greedy matching.

### Incident 4 — Expense Category "0" Fall-Through
- **incident_id**: INC_004
- **detected_at**: 2026-07-10 13:20 UTC
- **symptom**: Expense category "0" falling through parser before v375 and posting to ledger.
- **impact**: Data mapping pollution in Account Ledger.
- **root_cause**: Category parser missing strict validation block for "0" review route.
- **repair**: Direct category "0" explicitly to Review Queue fallback.
- **verification**: Staging selftest validation.
- **status**: RESOLVED
- **related_versions**: v375
- **related_evidence**: v375 test logs
- **remaining_risk**: Other fall-through keys.

### Incident 5 — Split Authority (Final Kitab vs ARFIN.md)
- **incident_id**: INC_005
- **detected_at**: 2026-07-12 09:40 UTC
- **symptom**: Split claims of canonical guidance between the two docs.
- **impact**: Ambiguity for developers updating codebase.
- **root_cause**: Reconciliations not unified in previous sessions.
- **repair**: Create unified AFPD modules (docs/afpd/).
- **status**: IN_PROGRESS
- **related_versions**: Phase 2/3
- **related_evidence**: Contradiction Matrix
- **remaining_risk**: Inactive activation stubs.

### Incident 6 — Missing Durable v371-v375 Documentation
- **incident_id**: INC_006
- **detected_at**: 2026-07-12 09:45 UTC
- **symptom**: Version changes absent from main documentation files.
- **impact**: Lack of traceability for past patches.
- **root_cause**: Rapid hotfixing bypass of documentation updates.
- **repair**: Backfill progress log entries in Phase 3.
- **status**: RESOLVED
- **related_versions**: Phase 3
- **related_evidence**: Progress log backfill plan
- **remaining_risk**: None.

### Incident 7 — Manifest Timezone vs Business Timezone
- **incident_id**: INC_007
- **detected_at**: 2026-07-12 09:48 UTC
- **symptom**: appsscript.json manifest timezone discrepancy.
- **impact**: Deployed times in GCP mismatched with local Jakarta times.
- **root_cause**: Manifest left at default Asia/Bangkok while code uses Asia/Jakarta.
- **repair**: Documented unresolved discrepancy in trigger topology. Normalization deferred.
- **status**: UNRESOLVED
- **related_versions**: Phase 3
- **related_evidence**: appsscript.json manifest
- **remaining_risk**: Date conversion offsets in logs.

### Incident 8 — Undercounted Phase 4 Normative Extractor
- **incident_id**: AFPD-INC-008
- **detected_at**: 2026-07-12 10:12 WIB
- **symptom**: Phase 4 declared readiness using an undercounted normative extractor.
- **impact**: Canonical activation could have occurred with missing rules.
- **root_cause**: Audit implementation used selected or hardcoded rules instead of the full dynamic baseline.
- **repair**: Independent extraction and full normative remediation mapping 377 rules.
- **verification**: Phase 4.2 post-remediation audit.
- **status**: OPEN until Phase 4.3 PASS
- **related_versions**: Phase 4/4.1/4.2
- **related_evidence**: /tmp/airo_afpd_phase4_1_20260712_101527
- **remaining_risk**: Gaps in newly appended sections.

### Incident 8 Update — Undercounted Phase 4 Normative Extractor
- **incident_id**: AFPD-INC-008
- **detected_at**: 2026-07-12 10:12 WIB
- **status**: OPEN (Pending Phase 4.5 independent semantic re-audit)

### Incident 9 — Manual Telegram Resolution Bypassed Review Queue

- **incident_id**: AFPD-INC-009
- **detected_at**: 2026-07-12, Owner-reported Telegram transaction flow
- **symptom**: After manual account and subcategory selection, Arfin reported success and changed ledger state without Review Queue approval.
- **impact**: Premature ledger mutation, false-success messaging, and possible loss of execution-account versus funding-account semantics.
- **root_cause**: `airoHandleOutgoingConfirmationReply_` called `writeRouted_` directly in the resolved-subcategory branch and cleared pending state before governed staging/readback.
- **repair**: Replace direct ledger write with `telegram_manual` approval staging, source-scoped approval guards, deterministic dedupe identity, category-scoped prompts, and posting-plan metadata restoration.
- **repository_source_commit**: `22caa64774977fdedcd5ae8555e3c805b20feac8`
- **source_sha256**: `aca69b3750ce63ce2015ce416880d9b225e704166f8b030a9783623056a93b52`
- **stable_patch_id**: `1d3c4a7f0a88efc4ccce2bb22fa3d0351e3baea5`
- **verification**: Independent semantic review, content-equivalence audit, syntax validation, same-account 1-row test, funded-payment 3-row test, and repeat-approval zero-extra-row test.
- **status**: REPAIR_INTEGRATED_NOT_DEPLOYED
- **production_resolution**: PENDING
- **related_evidence**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642.md`
- **remaining_risk**: Apps Script deployment parity and live Telegram/workbook behavior remain unproven.
- **next_gate**: Owner-authorized Gate P2 deployment and production runtime/readback proof.

#### `AFPD-INC-009` Gate P1.1 update — self-test contract aligned

- **Timestamp**: 2026-07-13 19:17:45 WIB
- **Marker**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1`
- **Source repair commit**: `36bb37c228999efedaeb3ee305e03354f54cbf1a`
- **Change**: Added `plannedPostingRowCount` to the resolved dry-run and replaced stale pre-approval `rowCount === 3/1` assertions.
- **Runtime implementation changed**: NO
- **Built-in self-test result**: PASS
- **Deployment performed**: NO
- **Incident status**: REPAIR_INTEGRATED_NOT_DEPLOYED
- **Evidence**: `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745.md`

- 2026-07-19: Repaired Gate P1.2 self-test harness dependency alignment (`AIRO_ARFIN_SELFTEST_HARNESS_REPAIR_P1_2`). Self-test pass rate: 17/17.

- 2026-07-19: Documented Gate P2 rollback status and runtime failure evidence (`AIRO_ARFIN_GATE_P2_ROLLBACK_STATUS_AND_FAILURE_EVIDENCE`). Rollback confirmed to version 377.

- 2026-07-19: Documented Gate P2 runtime failure RCA (`AIRO_ARFIN_GATE_P2_RUNTIME_FAILURE_RCA_NO_DEPLOY`). Classification: `CLASP_RUN_CONTEXT_NOT_AUTHORIZED_FOR_SCRIPT_FUNCTION`.

- 2026-07-19: Formulated Gate P2 clasp runtime permission remediation plan (`AIRO_ARFIN_GATE_P2_CLASP_RUNTIME_PERMISSION_REMEDIATION_NO_DEPLOY`). Route: `OWNER_ENABLE_APPS_SCRIPT_API_AND_EXECUTION_API_CONTEXT`.

- 2026-07-19: Documented Gate P2 runtime proof method decision (`AIRO_ARFIN_GATE_P2_RUNTIME_PROOF_METHOD_DECISION_NO_DEPLOY`). Decision: `MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS`.

- 2026-07-19: Executed Gate P2 guarded deployment retry to version `379` (`AIRO_ARFIN_GATE_P2_GUARDED_DEPLOYMENT_RETRY_EXECUTION_MANUAL_RUNTIME_PROOF_METHOD`). Awaiting post-deploy manual editor runtime proof.

- 2026-07-19: Documented post-deploy manual editor runtime proof for version 379 (`AIRO_ARFIN_GATE_P2_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`). Status: PASS 17/17.

- 2026-07-19: Documented partial Telegram live proof and formulated retest plan (`AIRO_ARFIN_GATE_P2_TELEGRAM_FUNDING_FIRST_LIVE_PROOF_RECORD_PARTIAL_AND_RETEST_PLAN`). Status: `PARTIAL_PASS_WITH_BLOCKERS`.

- 2026-07-19: Documented root cause analysis for live Telegram semantics reversal and email legacy alpha prompt (`AIRO_ARFIN_GATE_P2_LIVE_TELEGRAM_SEMANTICS_AND_EMAIL_PROMPT_RCA_NO_DEPLOY`).

- 2026-07-19: Formulated Telegram semantics and email numeric prompt remediation plan (`AIRO_ARFIN_GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_REMEDIATION_PLAN_NO_DEPLOY`).

- 2026-07-19: Integrated source repair for Telegram semantics and email numeric prompt (`AIRO_ARFIN_GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_REPAIR_EXECUTION_NO_DEPLOY`). Local self-test PASS 21/21.

- 2026-07-19: Deployed Telegram semantics repair (version 380) via `AIRO_ARFIN_GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_GUARDED_DEPLOYMENT_EXECUTION`. Readback PASS.

- 2026-07-19: Recorded post-deploy manual Apps Script editor runtime proof PASS 21/21 for version 380 (`AIRO_ARFIN_GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF_RECORD`).

- 2026-07-19: Recorded live Telegram retest PASS for version 380 (`AIRO_ARFIN_GATE_P2_TELEGRAM_SEMANTICS_AND_EMAIL_NUMERIC_PROMPT_LIVE_TELEGRAM_RETEST_RECORD`). Staged to Review Queue.

- 2026-07-19: Recorded email expense category prompt legacy alpha blocker for version 380 (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_LEGACY_ALPHA_PROMPT_RECORD_BLOCKER_NO_DEPLOY`).

- 2026-07-19: Completed RCA for email expense category prompt legacy alpha display (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_RCA_NO_DEPLOY`).

- 2026-07-19: Formulated remediation plan for email expense category numeric prompt repair (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REMEDIATION_PLAN_NO_DEPLOY`).

- 2026-07-19: Integrated source repair for email expense category numeric prompt (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_REPAIR_EXECUTION_NO_DEPLOY`).

- 2026-07-19: Deployed email expense category numeric prompt repair to Apps Script version 381 (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_GUARDED_DEPLOYMENT_EXECUTION`).

- 2026-07-19: Recorded manual Apps Script editor runtime proof for v381 (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_CATEGORY_NUMERIC_PROMPT_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF_RECORD`).

- 2026-07-19: Recorded email expense false inflow blocker (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_RECORD_BLOCKER_NO_DEPLOY`).

- 2026-07-19: Recorded email expense false inflow RCA (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_RCA_NO_DEPLOY`).

- 2026-07-19: Recorded email expense false inflow remediation plan (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REMEDIATION_PLAN_NO_DEPLOY`).

- 2026-07-19: Executed local repair for email direction false inflow defect (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_REPAIR_EXECUTION_NO_DEPLOY`).

- 2026-07-19: Executed guarded deployment for email direction false inflow repair to Apps Script version v383 (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_GUARDED_DEPLOYMENT_EXECUTION`).

- 2026-07-19: Recorded Owner manual Apps Script editor runtime proof for v383 false inflow direction repair (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF_RECORD`).

- 2026-07-20: Recorded live retest blocker: fresh Blu expense email not picked up by Arfin after several minutes on v383 (`AIRO_ARFIN_GATE_P2_EMAIL_EXPENSE_DIRECTION_FALSE_INFLOW_V383_EMAIL_INGESTION_LAG_OR_MISSED_CANDIDATE_RECORD_NO_DEPLOY`).
