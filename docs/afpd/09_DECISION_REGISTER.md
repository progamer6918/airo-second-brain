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
