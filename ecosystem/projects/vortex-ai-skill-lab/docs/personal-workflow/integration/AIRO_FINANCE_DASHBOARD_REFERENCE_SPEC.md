# AIRO Finance Dashboard Reference Spec

Date: 2026-05-20
Project: AIRO Finance Sheet Workflow v1.2
Scope: Dashboard/status UX summary
Reference: User-provided Airo_Finance_Dashboard.pdf

## Purpose

This document preserves the user's Dashboard reference so future chats do not need to re-discuss the PDF.

The Dashboard target is a Google Sheet Dashboard page, not a PDF export and not a web dashboard.

The desired result is a clean, formal, premium one-page personal finance snapshot inside Google Sheets.

## Target Similarity

Realistic target for Google Sheet implementation:

- Information structure similarity: 85-90%
- Financial content similarity: 80-90%, depending on tab readiness
- Visual/layout similarity: 65-75%
- Total practical similarity: 75-82%

Do not promise pixel-perfect PDF reproduction inside Google Sheets.

## Reference Structure

The PDF reference contains these main sections:

1. Header
   - AIRO PERSONAL FINANCE
   - Snapshot date
   - User name
   - System active indicator

2. Net Worth Hero
   - Net Worth Total
   - Liquid assets
   - Home equity

3. Summary Cards
   - Home value
   - Remaining KPR
   - Gold asset
   - Total non-KPR debt

4. Account Balances
   - BCA
   - Blu BCA
   - Mandiri
   - GoPay
   - ShopeePay
   - Cash

5. Monthly Cashflow
   - Transactions income
   - Cash in
   - Transactions expense
   - Cash out
   - Net month
   - Short note about data status

6. Cicilan Rumah
   - KPR installment number
   - Due date
   - Monthly installment
   - Progress percentage
   - Remaining principal
   - Home equity
   - Estimated payoff date

7. Hutang Aktif
   - Active debt list by person
   - Remaining amount
   - Paid amount and percentage
   - Total non-KPR debt

8. Credit Card
   - Tokopedia CC
   - Billing cycle
   - Amount not yet transferred to Blu
   - Item list with paid/unpaid status
   - Cycle total

9. Gold Asset
   - Total gram equivalent
   - Current estimated value
   - Market price per gram
   - Purchase capital
   - Unrealized gain
   - Return percentage
   - Ownership description

10. Footer
   - AIRO Personal Finance
   - Generated from Google Sheets/n8n
   - Date
   - Confidential marker

## Design Direction

Style:

- Clean
- Formal
- Premium
- Personal finance report feel
- Not a dark NOC/monitoring dashboard
- Not a technical-only system dashboard

Dashboard should feel like the PDF reference but remain editable and formula-driven inside Google Sheets.

## Implementation Target

The final Dashboard should be implemented as a Google Sheet Dashboard page.

Do not export to PDF as the main deliverable.

Do not create a web dashboard unless explicitly approved later.

Recommended implementation order:

1. Build Sheet Dashboard layout like the PDF snapshot.
2. Keep it compatible with existing Google Sheet formulas.
3. Add daily/monthly summary potential later.
4. Web dashboard is future-only.

## Dashboard Content Priority

Use this hierarchy:

1. Net Worth total
2. Liquid assets and home equity
3. Account balances
4. Monthly cashflow
5. Cicilan Rumah
6. Hutang Aktif
7. Credit Card
8. Gold Asset
9. Small AIRO Finance status

## Small System Status Area

System status should be small, not dominant.

Recommended status items:

- AIRO Finance status: PASS/CHECK
- Cash parity: PASS/CHECK
- Last refresh date/time
- Review Queue pending count
- Formula health: PASS/CHECK

Do not turn the Dashboard into a large technical audit panel.

## Data Source Mapping

Dashboard block to source tabs:

- Net Worth Total: Aset, Hutang, Cicilan Rumah, Account Ledger/account balances
- Liquid assets: Account Ledger and account balance formulas
- Home equity: Cicilan Rumah
- Home value: Cicilan Rumah or Settings/config
- Remaining KPR: Cicilan Rumah
- Gold asset: Aset gold ledger
- Total non-KPR debt: Hutang
- Account balances: Account Ledger and Cash Ledger compatibility where needed
- Cashflow month: Account Ledger and Monthly Review
- Cicilan Rumah block: Cicilan Rumah
- Hutang Aktif block: Hutang
- Credit Card block: Credit Card
- AIRO Finance status: audit commands/formula health/review queue status

## Data Readiness Notes

Current readiness:

- Cash/Account Ledger: increasingly stable.
- Cicilan Rumah: must be audited in Priority 3.
- Hutang: must be audited in Priority 3.
- Credit Card: roadmap says core-ready/Tokopedia CC PASS, but needs final regression before Dashboard final.
- Aset: asset sync patched, but needs regression before Dashboard final.
- Monthly Review: cash reporting formulas have passed; final formula health still needed.

Therefore, do not build final Dashboard until Priority 2 and key Priority 3 audits are complete.

## Before / After

Before:

- Data is scattered across tabs.
- Dashboard is not yet a polished one-page finance snapshot.
- User must manually inspect tabs and run audit commands to trust the numbers.

After:

- Dashboard Sheet becomes a one-page personal finance snapshot.
- User can see net worth, cashflow, debts, KPR, credit card, gold assets, and small system status at a glance.
- Dashboard remains formula-driven and editable inside Google Sheets.
- No PDF export required.

## Explicit User Decision

The user does not want the final deliverable to be a PDF export.

The user wants the Google Sheet Dashboard page to look and feel like the provided PDF reference.

## Constraints

- Do not commit the original PDF unless user explicitly approves.
- Do not expose personal financial values unnecessarily.
- Do not redesign the entire sheet.
- Do not create new tabs unless explicitly approved.
- Do not make Dashboard work before data sources are stable.
