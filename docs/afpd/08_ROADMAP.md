# 08_ROADMAP.md

<!-- AIRO_FINANCE_WEB_APP_V2_PHASE_2_SHELL_LOCAL_CANDIDATE_BUILD_NO_DEPLOY_BEGIN -->
## Phase 2 Shell Candidate — 2026-07-23T14:09:56+00:00

- Phase 0 canonicalization: `PASS`
- Phase 1 MVP stabilization: `PASS`
- Phase 2 Web App V2 Shell: `LOCAL_CANDIDATE_BUILT`
- Primary visible artifact: `ecosystem/projects/vortex-ai-skill-lab/webapp-v2-candidate/AIRO_Finance_WebApp_V2_Shell_Candidate.html`
- Backend integration: `NOT_STARTED`
- Production deployment: `NO`
- Next gate: `AIRO_FINANCE_WEB_APP_V2_PHASE_2_SHELL_OWNER_VISUAL_REVIEW_NO_DEPLOY`
<!-- AIRO_FINANCE_WEB_APP_V2_PHASE_2_SHELL_LOCAL_CANDIDATE_BUILD_NO_DEPLOY_END -->


<!-- AIRO_PHASE_1_CLOSEOUT_PHASE_2_ENTRY_BEGIN -->
## Phase Entry — 2026-07-23T13:53:12+00:00

Phase 0 canonicalization: PASS
Phase 1 MVP stabilization: PASS
Phase 2 Web App V2 Shell: READY_TO_START
Phase 3-8: PLANNED
Immediate next gate: AIRO_FINANCE_WEB_APP_V2_PHASE_2_SHELL_LOCAL_CANDIDATE_BUILD_NO_DEPLOY
<!-- AIRO_PHASE_1_CLOSEOUT_PHASE_2_ENTRY_END -->


<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1320-1321
source_heading: 18. Final Roadmap
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1322-1355
source_heading: Sprint 0A - Telegram Clarification Closure
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1356-1382
source_heading: Sprint 0B - Email Ambiguity Research & Bridge Design
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1383-1410
source_heading: Sprint 1 - Account Ledger Hardening
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1411-1434
source_heading: Sprint 2 - Domain Tabs Maturation
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1435-1459
source_heading: Sprint 3 - Cash Ledger Removal
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1460-1491
source_heading: Sprint 4 - Finance Events v1
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1492-1517
source_heading: Sprint 5 - Audit, Reconciliation, Partial Recovery
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1518-1554
source_heading: Sprint 6 - Dashboard Final
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1555-1580
source_heading: Sprint 6B - Proactive Telegram Alert Engine v1
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1581-1610
source_heading: Sprint 7 - Email Ingestion v1, Outline Only
migration_status: HISTORICAL
conflict_id: none
-->

## Active Roadmap: AIRO Finance Web App V2 Track (2026-07-23)
- **Status:** OWNER_APPROVED
- **Execution Plan Pointer:** `ecosystem/projects/vortex-ai-skill-lab/docs/plans/AIRO_FINANCE_WEB_APP_V2_EXECUTION_SLICE_PLAN.md`
- **Phase 0 (Canonicalization):** PASS (this docs-only gate)
- **Phase 1 (Stabilize MVP):** Separate Cash matching, Top Subcategory, split filters, Cash Makan post-deploy.
- **Phase 2 (V2 Shell):** Responsive 4-domain shell, loading/empty/stale states, Category/Subcategory comparisons.
- **Phase 3 (Adapter Foundation):** Lazy-loading RPC boundary (`getDashboardOverviewSnapshot`, `getDashboardDomainSnapshot`).
- **Phase 4 (Cicilan Rumah):** First complex domain vertical slice.
- **Phase 5 (Credit Card):** Credit card vertical slice.
- **Phase 6 (Hutang):** Hutang vertical slice.
- **Phase 7 (Aset / Emas):** Assets vertical slice.
- **Phase 8 (Unified Activity & Hardening):** Cross-domain activity log and final production hardening.
- **Immediate Next Gate:** `AIRO_FINANCE_WEB_DASHBOARD_SEPARATE_CASH_ACCOUNTS_AND_TOP_SUBCATEGORY_GUARDED_DEPLOYMENT_PREFLIGHT_NO_DEPLOY`

## Historical Sprints
- Sprint 0A through Sprint 7 are legacy records of completed features and MUST NOT be used for active task sequences.

## Proposed Track: AIRO Finance Web Dashboard Read-Only MVP (2026-07-21)
- Status: PROPOSED (Owner Decision: GO_FOR_DISCOVERY_ONLY)
- Gate: AIRO_FINANCE_WEB_DASHBOARD_READONLY_MVP_PROPOSAL_NO_DEPLOY
- Scope: Read-Only HtmlService Web App Candidate, Account Ledger approved rows data source

- **2026-07-23 (Phase 1 Local Repair)**: Repaired live client RPC wrapper `airoWebDashboardGetClientSnapshot` to supply Account Registry-derived wallet boundaries. Added read-only helper `airoWebDashboardGetAccountEligibilityReadOnly_`, removed generic `"Cash"` fallback from default list, and added 7 new selftests (124/124 PASS). Next safe gate: `AIRO_FINANCE_WEB_DASHBOARD_V389_GENERIC_CASH_LIVE_WRAPPER_REGISTRY_HANDOFF_GUARDED_DEPLOYMENT_PREFLIGHT_NO_DEPLOY`.

- **2026-07-23 (Phase 1 Deployment Preflight)**: Validated preflight readiness for generic Cash live wrapper registry handoff fix. Selftest 124/124 PASS, remote HEAD baseline matched v389 source SHA (7ee00e69c790de00d9489c9a10624d650454b2944d9db3b8ce4331c65b91afe8), candidate diff isolated to 1 source file. DEPLOYMENT_READINESS=GO. Target version expected: 390. Rollback version: 389. Next safe gate: `AIRO_FINANCE_WEB_DASHBOARD_V389_GENERIC_CASH_LIVE_WRAPPER_REGISTRY_HANDOFF_GUARDED_DEPLOYMENT_EXECUTION_V390`.

- **2026-07-23 (Phase 1 Guarded Deployment v390)**: Deployed version 390 to target deployment `ZYjuOA`. Real browser proof PASS (Cash Umum distinct, Cash Bensin distinct, generic Cash absent, Cash Makan not invented, Top Subcategory PASS). Active version: 390. Immediate rollback version: 389. Next safe gate: `AIRO_FINANCE_WEB_DASHBOARD_V390_POST_DEPLOY_OWNER_LIVE_ACCEPTANCE_RECORD_NO_MUTATION`.

- **2026-07-23 (Owner Live Acceptance v390)**: Recorded Owner live production acceptance PASS for dashboard version 390. Generic Cash incident AFPD-INC-010 is RESOLVED. Active production version: 390. Rollback target: 389. Next safe gate: `AIRO_FINANCE_CASH_MAKAN_ACCOUNT_REGISTRY_READ_ONLY_AUDIT_NO_MUTATION`.

- **2026-07-23 (Cash Makan Audit)**: Completed read-only Account Registry schema audit for `Cash Makan`. Classification: `EXACT_ONE_ACTIVE_ALIGNED`. Live dashboard renders Cash Makan as active registry-driven wallet. Mutation required: NO. Phase 1 full closeout ready: YES. Next safe gate: `AIRO_FINANCE_PHASE_1_MVP_STABILIZATION_CLOSEOUT_AND_PHASE_2_ENTRY_RECORD_NO_RUNTIME_MUTATION`.
