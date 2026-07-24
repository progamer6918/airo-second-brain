# 09_DECISION_REGISTER.md

## Durable Decision Records
- **AFPD Proposed Authority Hierarchy**: Initiated Phase 3 skeleton creation to replace split authority between Final Kitab and ARFIN.md once canonical activation is granted.
- **Final Kitab Preservation**: Final Kitab is preserved unchanged during documentation migrations to maintain historical stability.
- **ARFIN Runtime Contract Integration**: Merged ARFIN.md behavior and Final Kitab rules in module 03.
- **Review Queue Dual Semantics**: Separate status mappings for Manual-Review Fallback and Approval Staging.
- **Numeric UX Prompts**: Prompts upgraded to numeric indexes (`1..N`, `0`). Alpha A-E remains legacy/unresolved.
- **Timezone Normalization Deferred**: Jakarta business timezone is active in script; Bangkok manifest timezone normalization is deferred.
## AIRO Finance Web App V2 Direction & Architecture Decisions (2026-07-23)
- **Web App V2 Product Model:** Read-only finance cockpit. Source of truth remains Google Sheets. Backend remains Google Apps Script. Web App must not approve, edit, delete, save, post, or mutate financial data. No external DB or SaaS migration.
- **Information Architecture:** 7 core domains (Ringkasan, Pengeluaran, Akun & Saldo, Kewajiban [Credit Card, Hutang, Cicilan Rumah], Aset [Emas, future assets], Aktivitas, Data Quality).
- **Global UI Contract:** Month and Year selectors must remain separate (combined month-year selector is forbidden). Responsive navigation (sidebar on Desktop, compact/bottom nav on Mobile). Visible read-only indicator. Safe DOM insertion.
- **Spending Contract:** Top Category & Top Subcategory available with previous-period comparison (`new`, `increase`, `decrease`, `disappeared`, `no_comparison`). Backend adapters supply canonical values; browser does not calculate domain truth.
- **Account Contract:** `CASH_ACCOUNT_MODEL=SEPARATE`, `CASH=NOT_USED`, `CASH_UMUM=ACTIVE`, `CASH_BENSIN=ACTIVE`, `CASH_MAKAN=ACTIVE`, `CASH_AND_CASH_UMUM_ARE_SAME_ACCOUNT=NO`, `CASH_GROUP_AGGREGATION=DISABLED`, `CASH_REGEX_COLLAPSE=FORBIDDEN`, `WALLET_MATCHING=EXACT_CANONICAL_ACCOUNT`.
- **Deployment-Before-Registry Sequence:** Deployment of separate cash matching and Top Subcategory rendering occurs BEFORE Account Registry mutation. Cash Makan registry insertion is deferred until post-deploy. No inactive `Cash` tombstone row insertion.
- **Domain Execution Order:** Cicilan Rumah is established as the first complex domain vertical slice following Phase 3 foundation.
- **Anti-Freeze Rules:** Enforced 12 anti-freeze execution rules including 1-gate-1-deliverable, max 1-2 days without visible artifact, and mandatory bounded forensic gates for >2hr investigations.

<!-- AIRO_PHASE_1_CLOSEOUT_PHASE_2_ENTRY_BEGIN -->
## Decision — Close Phase 1 and open Phase 2

Recorded at: 2026-07-23T13:53:12+00:00
Decision: Phase 1 is closed as PASS.
Production remains version 390.
Cash Makan already exists exactly once, is active, aligned, and rendered.
No Cash Makan insertion, activation, or registry remediation is required.
Phase 2 begins with a separate local shell candidate and no deployment.
The prior audit is functionally PASS with process limitations recorded.
<!-- AIRO_PHASE_1_CLOSEOUT_PHASE_2_ENTRY_END -->

<!-- AIRO_FINANCE_WEB_APP_V2_PHASE_2_SHELL_OWNER_VISUAL_ACCEPTANCE_RECORD_NO_DEPLOY_BEGIN -->
## Decision — Accept Web App V2 Phase 2 Shell

- Recorded: `2026-07-23T15:20:46+00:00`
- Owner acceptance: `PASS ALL`
- The responsive shell direction is accepted.
- Ringkasan, Pengeluaran, Akun & Saldo and Data Quality render correctly.
- Desktop and mobile navigation are accepted.
- Month and Year controls are accepted.
- Loading, Empty, Warning and Error states are accepted.
- Cash account separation and read-only presentation are accepted.
- The candidate remains local and uses public-safe sample data.
- No production deployment is authorized by this decision.
- Next work begins with a local read-only snapshot adapter candidate.
<!-- AIRO_FINANCE_WEB_APP_V2_PHASE_2_SHELL_OWNER_VISUAL_ACCEPTANCE_RECORD_NO_DEPLOY_END -->


<!-- AIRO_FINANCE_WEB_APP_V2_PHASE_2_LOCAL_SNAPSHOT_ADAPTER_OWNER_ACCEPTANCE_RECORD_NO_DEPLOY_20260724_194916_BEGIN -->
## Decision — Accept Web App V2 Phase 2 Local Read-Only Snapshot Adapter Candidate

- Recorded: `2026-07-24 Asia/Jakarta`
- Owner acceptance: `PASS ALL`
- Integration commit: `f79be1e6fc6f1aa5aef1a8e9f0518e1d13ca23c6`
- Technical contract: `61/61 PASS`
- Provider runtime harness: `PASS`
- Active snapshot data flow: `PASS`
- Stale-request guards: `PASS`
- Separate Cash accounts: `PASS` (`Cash Umum`, `Cash Bensin`, `Cash Makan`)
- Candidate remains local and uses public-safe sample data.
- Production version remains `390`. No production deployment is authorized by this decision.
- Next gate: `AIRO_FINANCE_WEB_APP_V2_PHASE_2_LIVE_READ_ONLY_SNAPSHOT_CONTRACT_ATTRIBUTION_AND_PLAN_NO_DEPLOY`
<!-- AIRO_FINANCE_WEB_APP_V2_PHASE_2_LOCAL_SNAPSHOT_ADAPTER_OWNER_ACCEPTANCE_RECORD_NO_DEPLOY_20260724_194916_END -->
