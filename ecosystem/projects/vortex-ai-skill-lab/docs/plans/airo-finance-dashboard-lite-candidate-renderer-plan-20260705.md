# AIRO Finance Dashboard Lite — Candidate Renderer Implementation Plan

**Date/time:** 2026-07-05 09:04 Asia/Jakarta  
**Status:** PLAN_LOCKED / OWNER_REVIEW_BLOCKED  
**Scope:** DOCS_ONLY_PLAN  
**Baseline commit:** 3fb99c10ce1eaba9826141cdf34e4623140f4617  

## 1. Candidate Tab Target
- Target tab name: `🧪 Dashboard Lite Candidate`
- Staging mode: The rendering functions will write formatting, styling, values, and calculations exclusively to the candidate tab.

## 2. Active Tab Freeze
- **No active mutations**: The active `🏠 Dashboard` sheet will be completely untouched. 
- **Read-only source logic**: The active dashboard can only be accessed as a read-only template/source if required by copying logic. All visual changes, calculations, and updates are locked out of the live dashboard.

## 3. Source Patch Strategy
To support isolated candidate rendering without regression risks, the source patch will introduce:
1. **Candidate-Targeted Rendering**: Modify or parameterize the dashboard lite renderer function (`airoDashboardLiteRender_`) to accept a custom target sheet object instead of default active dashboard.
2. **Dedicated Candidate Helper**: Add the helper function:
   `runDashboardLiteCandidateJuni2026RefreshReadbackFromEditor`
   This helper will apply G2/I2 filter parameters, trigger candidate-targeted render, flush the spreadsheet, and perform readbacks on the candidate tab.

## 4. Required Readback Ranges (Candidate)
The candidate refresh helper must read back the following ranges from `🧪 Dashboard Lite Candidate`:
- Z3 (Metadata verdict): must return `DASHBOARD_LITE_REFRESH_PASS`
- B2 (Topbar): synced text info
- B5:E15: category spending rows
- G5:J15: subcategory spending rows
- B18:C30: active wallet and balance rows
- B31:C31: total wallet balance
- G18:J20: domain metrics rows

## 5. Visual Acceptance Checklist (Based on Owner Blocker)
The styling logic must be modified to satisfy the following constraints:
- **No legacy labels**: The columns `LEVEL` and `STATUS` in wallet rows, `DATA QUALITY CENTER` table, `SECONDARY` indicators, and generic raw `DOMAIN/METRIC` tables must be completely removed.
- **Header cleanups**: Section headers must be neat and formatted correctly.
- **Friendly Domain Summary Labels**: Replace technical labels with friendly titles (e.g. "Kartu Kredit", "Nilai Emas", "Cicilan Rumah").
- **Spacing and Alignment**: Proper row heights, column widths, and cell padding to avoid cramped or overlapping text.
- **Ledger Rows Count**: Ensure `Ledger rows` count displays correctly instead of blank.

## 6. Promote-to-Active Criteria
Promotion to the live `🏠 Dashboard` requires:
1. Both the candidate refresh readback and the visual sanity readback pass with 100% success on the `🧪 Dashboard Lite Candidate` tab.
2. The Owner manually reviews and approves the candidate tab visual layout.

## 7. Rollback & Scheduler Status
- **Rollback**: To rollback, delete the candidate tab and revert source patch changes. The active `🏠 Dashboard` is never affected.
- **Scheduler**: The periodic refresh scheduler remains **OFF/parked**.
