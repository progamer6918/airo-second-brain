# AIRO Finance Web App V2 PRD Addendum

- **Status:** OWNER_APPROVED_ACTIVE_PROJECT_ADDENDUM
- **Date:** 2026-07-23
- **Owner:** Approved Direction
- **AFPD Status Note:** AFPD remains PROPOSED_NOT_CANONICAL pending explicit activation.

---

## 1. Purpose
This document serves as the canonical product addendum recording the Owner-approved direction, prototype structure, global UI contracts, domain architecture, and acceptance criteria for AIRO Finance Web App V2.

## 2. Relationship to Living PRD and ARFIN Contracts
- This addendum complements `ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_PRD_LIVING.md` for Web App V2 read-only cockpit execution.
- It does **NOT** supersede or replace `ARFIN.md` or AFPD Module 03 (`03_ARFIN_RUNTIME_CONTRACT.md`) regarding intake, state machines, Telegram approval workflows, Review Queue semantics, or Account Ledger posting rules.
- AFPD documentation remains `PROPOSED_NOT_CANONICAL`.

## 3. Product Boundary: Scope and Non-Scope
### In-Scope:
- Read-only Web App finance cockpit served via Google Apps Script `HtmlService`.
- 7 core information architecture domains:
  1. Ringkasan (Overview)
  2. Pengeluaran (Spending Intelligence)
  3. Akun & Saldo (Accounts & Balances)
  4. Kewajiban (Liabilities: Credit Card, Hutang, Cicilan Rumah)
  5. Aset (Assets: Emas, future supported assets)
  6. Aktivitas (Activity)
  7. Data Quality (Data Quality & System Health)
- Separate Month and Year selectors.
- Category and Subcategory previous-period growth comparison.
- Exact-account wallet matching for cash accounts (`CASH_UMUM`, `CASH_BENSIN`, `CASH_MAKAN`).
- Lazy-loaded domain detail RPC boundary.

### Non-Scope:
- Any web-based data mutation, transaction editing, approval, posting, or deletion.
- Migration to external database engines (PostgreSQL, Supabase) or SaaS platforms.
- External build pipelines, Node.js bundling, or external CDN frameworks.
- Insertion of inactive `Cash` tombstone rows into Account Registry.
- Immediate Cash Makan registry mutation (deferred until exact-account wallet matching is live post-deployment).

## 4. Global UI Contract
- **Filters:** Month (1–12) and Year (YYYY) selectors must remain separate. Combined Month-Year dropdown is strictly forbidden.
- **Navigation:** Desktop uses structured sidebar navigation; Mobile uses compact/bottom navigation.
- **Read-Only Visibility:** A clear "Read-Only Cockpit" indicator badge must be visible at all times.
- **State Handling:** Interface must handle Loading, Empty, Warning, Failure, and Stale-response states gracefully.
- **DOM Safety:** Dynamic values must be safely inserted into the DOM using `textContent` or sanitized text escaping (no direct `innerHTML` injection of raw strings).

## 5. Spending Contract
- **Top Categories & Subcategories:** Display top spending categories and top subcategories for the selected period.
- **Previous-Period Comparison:** Compute and display period-over-period growth/delta for both Category and Subcategory levels.
- **Comparison States:**
  1. `new` (category/subcategory present in current period, absent in previous period)
  2. `increase` (spending increased)
  3. `decrease` (spending decreased)
  4. `disappeared` (present in previous period, absent in current period)
  5. `no_comparison` (insufficient historical baseline)
- **Domain Truth:** The browser/frontend MUST NOT perform domain calculations or infer financial truth. All canonical values and comparison statuses are supplied by Google Apps Script backend adapters.

## 6. Account Contract & Cash Wallets
- `CASH_ACCOUNT_MODEL` = `SEPARATE`
- `CASH` = `NOT_USED`
- `CASH_UMUM` = `ACTIVE`
- `CASH_BENSIN` = `ACTIVE`
- `CASH_MAKAN` = `ACTIVE`
- `CASH_AND_CASH_UMUM_ARE_SAME_ACCOUNT` = `NO`
- `CASH_GROUP_AGGREGATION` = `DISABLED`
- `CASH_REGEX_COLLAPSE` = `FORBIDDEN`
- `WALLET_MATCHING` = `EXACT_CANONICAL_ACCOUNT`
- Cash must not be inserted merely as an inactive tombstone unless a mandatory schema contract is proved.
- Cash Makan registry insertion is deferred until exact-account wallet matching is deployed.

## 7. Domain Architecture & Lazy Loading Strategy
- **Overview Snapshot RPC:** `getDashboardOverviewSnapshot({year, month})` returns lightweight snapshot for fast initial view.
- **Domain Detail RPC:** `getDashboardDomainSnapshot({domain, year, month})` lazy-loads detail data per tab upon user navigation.
- Conceptual RPC design only; implementation proceeds in vertical slices.

## 8. Private / Public Data Boundary
- ASB repository remains PUBLIC.
- NO real financial amounts, transaction descriptions, merchant names, personal/institution names, account numbers, email bodies, or local token credentials shall be committed to git.
- Real-data prototype HTML/JSON remains `LOCAL_ONLY_OWNER_REFERENCE`.

## 9. Acceptance Criteria
1. Web App interface operates in 100% read-only mode without write methods or POST mutation endpoints.
2. Month and Year filter controls are separate and function across all domain views.
3. Subcategory previous-period comparison works alongside Category comparison.
4. Accounts view displays exact separate cash wallets (`CASH_UMUM`, `CASH_BENSIN`) without collapsing into generic `Cash`.
5. Mobile and Desktop layouts adapt responsively.
6. All dynamic financial data is passed via Apps Script RPC and rendered safely.
