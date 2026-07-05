# AIRO Finance Dashboard Lite — V2 Template Mapping Audit Report

**Date/time:** 2026-07-05 09:23 Asia/Jakarta  
**Status:** OWNER_CANDIDATE_REVIEW_BLOCKED / OWNER_REVIEW_BLOCKED  
**Scope:** READ_ONLY_AUDIT_ONLY  
**Baseline commit:** 5b2556d573d6a3cc61d14f127e4da3982ad8ccba  

## 1. Sheet/Tab Identification
- **V2 Visual Template Tab**: `🏠 Dashboard v2` (resolved in Apps Script via `airoTask102GetV2Template_(ss)`).
- **Candidate Tab**: `🧪 Dashboard Lite Candidate` (created in workbook).
- **Current Candidate Creation Helper**: `runDashboardLiteCreateCandidateTabFromActiveDashboard` currently copies the active `🏠 Dashboard` instead of `🏠 Dashboard v2`. This is incorrect because the active dashboard layout has already deviated from the V2 standard. It must be updated to duplicate `🏠 Dashboard v2`.

## 2. Reusable V2 Visual Sections & Ranges
Based on the layout of `🏠 Dashboard v2`, the following styling, spacing, card boxes, and ranges are reusable:
- **Title Block & Sync Info**: Cells `B1:E2` (Header theme colors, title styling).
- **Category Spending Card**: Columns `B:E` starting at row 5.
- **Subcategory Spending Card**: Columns `G:J` starting at row 5.
- **Wallet & Cashflow Card**: Columns `B:C` starting at row 18.
- **Domain Metrics Card**: Columns `G:J` starting at row 18.

## 3. Excluded Legacy & Noisy Sections
The candidate renderer must clear or exclude these areas from the template layout:
- **Executive Command Center & Smart Insight**: Typically at the top right or bottom; must be removed to keep Lite simple.
- **Data Quality Center**: Must be omitted/cleared.
- **Wallet LEVEL / STATUS Bars**: Column D and E next to wallets must be cleared of formulas and bars.
- **Secondary Action Blocks**: Must be completely removed.
- **Raw DOMAIN / METRIC Table**: Technical metrics and domain labels (e.g., `TOKPED_CC...` raw strings) must be removed.

## 4. Proposed Dashboard Lite Content Zones
The candidate renderer will populate simplified, clean values into these V2 card zones:
1. **Topbar Sync & Filters** (`B2` / `G2:I2`): Displays synced timestamp, source (`Account Ledger`), and G2/I2 filter selections (e.g. `Juni 2026`).
2. **Top 5 Categories + Lainnya** (`B5:E15`): Displays Food & Drink, Utilities, etc., plus sum of other spending as "Lainnya" with percentages.
3. **Top 10 Subcategories + Lainnya** (`G5:J15`): Displays Makan Siang, Bensin, etc., plus "Lainnya" subcategory spending.
4. **Active Wallets & Balances** (`B18:C30`): Lists active wallets (BCA, Cash, Blu, etc.) and current balances.
5. **Total Saldo** (`B31:C31`): Renders combined wallet balance.
6. **Domain Summaries** (`G18:J20`): Populates human-friendly summary text and metrics:
   - **Credit Card**: Billing summary (due date/amount).
   - **Emas**: Gram count and current value.
   - **Cicilan Rumah**: PROGRESS status (e.g., month x/120).

## 5. Next Steps Source Patch
In the next gate, we will:
1. Update `runDashboardLiteCreateCandidateTabFromActiveDashboard` to clone `🏠 Dashboard v2` (via `airoTask102GetV2Template_(ss)`) instead of `🏠 Dashboard`.
2. Implement visual cleansing logic in the candidate renderer to clear the legacy cards/columns while keeping the V2 card borders and colors.
3. Run the candidate renderer helper and verify the visual layout matches V2 styling.

## 6. Governance & Safety Check
- Apps Script Source Mutation: NO
- Workbook Cell Mutation: NO
- Scheduler / Gate 12 triggers status: PARKED (not connected)
