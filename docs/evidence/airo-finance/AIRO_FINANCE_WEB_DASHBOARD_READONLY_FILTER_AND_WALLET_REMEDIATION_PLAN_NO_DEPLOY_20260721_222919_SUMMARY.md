# AIRO Finance Web Dashboard Read-Only Filter & Wallet Remediation Plan Summary

- **Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_FILTER_AND_WALLET_REMEDIATION_PLAN_NO_DEPLOY`
- **Timestamp**: `20260721_222919`
- **Active Apps Script Version**: `v386`
- **Mode**: `DOCS_ONLY_REMEDIATION_PLAN_NO_DEPLOY_NO_PATCH`
- **Source Patch Performed**: `NO`
- **Deployment Performed**: `NO`
- **Owner Browser Proof Result**: `PASS_WITH_PRODUCT_GAPS`
- **Existing Filter Contract**: `YES (Dashboard Lite V2 G2 Month + I2 Year cells)`
- **Filter Expected Shape**: `SEPARATE_MONTH_YEAR`
- **Filter UI Gap**: `v386 combined dropdown ("Juli 2026") does not match contract`
- **Filter Remediation Scope**: `SMALL_FIX (split into separate Month and Year dropdowns)`
- **Existing Wallet Contract**: `YES (Account Ledger cumulative net inflow Col D - Col E per account + Account Registry active list)`
- **Wallet UI Gap**: `v386 omitted Saldo per Akun Aktif table`
- **Wallet Remediation Scope**: `SMALL_FIX (add wallet_snapshot array to server JSON + render Saldo Akun card)`
- **Workbook Mutation**: `NO`
- **Next Safe Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_FILTER_AND_WALLET_LOCAL_REPAIR_NO_DEPLOY`

## Executive Summary & Detailed Plan

### 1. Context & Owner Observations
Owner browser proof for `v386` passed technical checks (URL opened, read-only banner visible, period change works, zero errors, zero write buttons). However, owner observed two key product/contract gaps:
1. **Filter Selector**: Combined month/year dropdown (`"Juli 2026"`) was rendered in `v386` UI instead of separate Month and Year dropdown controls established in AFPD Task 10.2 / Gate 11B (`G2` Month, `I2` Year).
2. **Wallet / Account Balances**: Active account balances ("Saldo per Akun Aktif") were missing from the dashboard UI, despite existing in the legacy workbook `Dashboard Lite V2` contract (rows 17..21).

---

### 2. Remediation Plan Architecture

#### A. Filter Remediation Plan
- **UI Changes in `AIRO_Finance_WebDashboard.html`**:
  - Remove combined `<select id="period-select">`.
  - Introduce two separate dropdown controls side-by-side:
    - `<select id="month-select">`: Options 1..12 / Jan..Des (defaults to current month, e.g. `7` for Juli).
    - `<select id="year-select">`: Options 2020..2030 (defaults to current year, e.g. `2026`).
  - Trigger `fetchSnapshot()` on change of either dropdown.
- **Server Contract Alignment**:
  - `airoWebDashboardGetClientSnapshot({ year, month })` remains 100% unchanged in interface contract.
  - `airoWebDashboardSanitizeInput_({ year, month })` handles separate year and month parameters smoothly.
  - Zero workbook mutation.

#### B. Wallet / Saldo Remediation Plan
- **Server Snapshot Calculator (`airoWebDashboardGetSnapshot_`)**:
  - Query active accounts from `🏦 Account Registry` (or default active account names: `BCA`, `Blu`, `Cash`, `Blu Pocket`, `Mandiri`).
  - For each active account, calculate cumulative balance up to the end date of the selected period:
    24608\text{Account Balance} = \sum \text{Income (Col D up to period end)} - \sum \text{Expense (Col E up to period end)}24608
  - Add `wallet_snapshot` array to JSON output:
    ```json
    "wallet_snapshot": [
      { "account": "BCA", "balance": 15500000, "status": "ACTIVE" },
      { "account": "Blu", "balance": 4200000, "status": "ACTIVE" },
      { "account": "Cash", "balance": 850000, "status": "ACTIVE" }
    ]
    ```
- **UI Rendering in `AIRO_Finance_WebDashboard.html`**:
  - Add "Saldo Akun / Wallet Snapshot" card in dashboard layout.
  - Render active account balances with formatted currency (`Rp ...`).
  - Exclude inactive accounts.
  - Read-only only (zero write/edit/transfer buttons).

---

### 3. Required Tests for Local Repair Gate (`AIRO_FINANCE_WEB_DASHBOARD_READONLY_FILTER_AND_WALLET_LOCAL_REPAIR_NO_DEPLOY`)
1. Separate month and year selector HTML static validation PASS.
2. Combined selector removal HTML static validation PASS.
3. `wallet_snapshot` array present in JSON snapshot contract PASS.
4. Active account balance cumulative calculation PASS (income - expense up to period end).
5. Account registry active account filter PASS (exclude inactive).
6. Read-only static guard PASS (0 write methods).
7. HTML static validation PASS (no approval/edit/write buttons, no external CDN).
8. Existing selftests remain PASS 85/85 or higher.
