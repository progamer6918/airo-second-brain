# AIRO Finance Web Dashboard Read-Only MVP Proposal Summary

- **Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_MVP_PROPOSAL_NO_DEPLOY`
- **Timestamp**: `20260721_201006`
- **Baseline Commit**: `84050f9d2cd2e76f6bdf66bc17779e6325e89e0b`
- **Baseline Apps Script Version**: `v385`
- **Mode**: `DOCS_ONLY_NO_DEPLOY_NO_PATCH`
- **Web Dashboard Mode**: `READ_ONLY`
- **Approval Enabled**: `NO`
- **Edit Enabled**: `NO`
- **Workbook Mutation**: `NO`
- **Old Sheet Dashboard Status**: `FROZEN_REFERENCE_ONLY`
- **Owner Decision**: `GO_FOR_DISCOVERY_ONLY`
- **Next Safe Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_DISCOVERY_NO_DEPLOY`

## Executive Summary & Background
AFPD-INC-009 was resolved on Apps Script v385. Following resolution, Owner approved exploring a browser-based read-only AIRO Finance dashboard web application (candidate: Apps Script `HtmlService`). This web app replaces/re-attempts the old Google Sheets dashboard concept purely as a read-only web dashboard MVP. The old Sheet Dashboard is frozen as reference only.

## Proposal Scope
- Read-only web dashboard UI (Apps Script `HtmlService` candidate)
- Month/year filter
- Financial KPIs: Total income, Total expense, Net cashflow
- Category & Subcategory Insights: Top spending category, Top spending subcategory, Contribution %
- Comparison & Growth: Growth vs previous month basic
- Transaction Activity: Recent Account Ledger view
- Data Quality & Operations: Data quality warnings, Last synced / data status display

## Explicit Non-Goals
1. No approval functionality in MVP.
2. No transaction editing or deletion.
3. No ledger write or Review Queue mutation.
4. No Telegram messaging or bot commands.
5. No Gmail mutation or auto-fix operations.
6. No full Dashboard Final parity requirement for initial MVP.
7. No production deployment during proposal/discovery.

## Recommended Data Source Architecture
- **Primary**: Account Ledger approved/final rows first.
- **Secondary / Evaluation**: Finance Events evaluated later during discovery only if data hygiene proves clean enough.

## Hard Stop Rules
1. No coding before dashboard freeze forensic discovery.
2. No UI implementation before data contract definition.
3. No Spending Intelligence if total expense for selected month cannot be reconciled to ledger.
4. No approval/edit/write in MVP.
5. No workbook mutation by dashboard MVP.
6. Pause if discovery cannot produce freeze reason and MVP data contract within two focused sessions.
7. If scope expands to full Dashboard Final, return to Owner Decision Gate.
