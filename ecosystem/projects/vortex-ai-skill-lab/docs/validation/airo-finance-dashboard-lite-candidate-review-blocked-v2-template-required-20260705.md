# AIRO Finance Dashboard Lite — Candidate Review Blocked & V2 Template Requirement Report

**Date/time:** 2026-07-05 09:19 Asia/Jakarta  
**Status:** OWNER_CANDIDATE_REVIEW_BLOCKED / OWNER_REVIEW_BLOCKED  
**Scope:** DOCS_ONLY_RECORD_REVIEW  
**Baseline commit:** 5b2556d573d6a3cc61d14f127e4da3982ad8ccba  

## 1. Owner Candidate Review Findings & Block
The Owner reviewed the first render output of the `🧪 Dashboard Lite Candidate` sheet and BLOCKED it. 

### Why the Candidate Was Rejected:
- The candidate layout still retains old/noisy panels and layout logic:
  - `SECONDARY` section.
  - `LEVEL` and `STATUS` columns in the wallet section.
  - `DATA QUALITY CENTER` table.
  - Generic `DOMAIN / METRIC` technical summary tables.
  - Cramped, overlapping, or vertically oriented text elements.
  - Raw technical domain labels (e.g. `TOKPED_CC...`).
- Merely adopting the dark color palette is insufficient. The layout must feel like a premium, spaced, and structured Dashboard V2 dashboard, not just a colored legacy grid.

## 2. Corrected Approach: Dashboard V2 Template
The layout strategy must be completely reversed:
1. **Source visual structure**: Adopt the layout structure of **Dashboard V2** first (spacing, section feel, header blocks, card boxes).
2. **Inject Lite content**: Overwrite the Dashboard V2 layout regions with simplified Dashboard Lite data:
   - **Topbar sync**: formatted sync timestamp + month/year filters (G2/I2).
   - **Categories**: Top 5 categories + "Lainnya" summary row.
   - **Subcategories**: Top 10 subcategories + "Lainnya" summary row.
   - **Wallets**: Active wallet names, balances, and total balance.
   - **Credit Card**: Tokopedia Credit Card billing summary (due/unbilled).
   - **Emas**: Gram count and total value.
   - **Cicilan Rumah**: PROGRESS count (e.g., month x/120).
3. **Strictly Remove/Exclude**:
   - Executive Command Center
   - Smart Insight complex
   - Data Quality Center
   - Wallet LEVEL and STATUS columns
   - Secondary action blocks
   - Raw technical tables and domain headers

## 3. Staging and Safety Rules
- Active `🏠 Dashboard` sheet remains frozen.
- All development and test runs are restricted to `🧪 Dashboard Lite Candidate`.
- Scheduler remains **OFF/parked**.
