# AIRO Finance Dashboard Lite — Recovery & Candidate Tab Plan

**Date/time:** 2026-07-05 08:52 Asia/Jakarta  
**Status:** PLAN_LOCKED / OWNER_REVIEW_BLOCKED  
**Scope:** DOCS_ONLY_PLAN  
**Baseline commit:** 59c127a0174bcc227880db3399eda427eb26af28  

## 1. Active Dashboard Freeze Policy
- The active `🏠 Dashboard` sheet will be frozen in its current state.
- No direct styling or cell mutations may be performed on the `🏠 Dashboard` sheet during candidate development and iteration.

## 2. Candidate Tab Configuration
- **Candidate Tab Name**: `🧪 Dashboard Lite Candidate`
- **Development isolation**: Every layout iteration, formatting update, color adjustments, and test render must be performed strictly within the `🧪 Dashboard Lite Candidate` tab.
- **Renderer Target configuration**: The Apps Script renderer must dynamically read options from and render outputs to this specific candidate sheet when executing tests, leaving the `🏠 Dashboard` untouched.

## 3. Candidate Readback Requirements
The candidate tab must satisfy the following data contracts before review:
1. G2 month and I2 year filter filters must read back exactly as set (e.g. Juni 2026).
2. Category spending table must populate correctly without empty rows.
3. Subcategory spending table must populate correctly without empty rows.
4. Active wallets and balances must read back correctly.
5. All legacy panels and raw technical indicators (LEVEL, STATUS, DATA QUALITY, SECONDARY) must be completely omitted or cleared.

## 4. Candidate Visual Acceptance Checklist
To prevent rejection, the candidate tab must visually mirror the high quality of active Dashboard V2:
- **Clean layouts**: Empty padding rows/columns around content cards.
- **Typography & size**: Consistent Arial font family, size 10 for normal cells, size 12-14 for headers/titles.
- **Card Styling**: Consistent dark gray/blue container backgrounds (`#182235`), dark titles (`#0b1220`), and correct cell alignments (names left, values right).
- **No overlapping text**: Proper row heights and column widths to prevent overlapping text.
- **Clean domain summary labels**: Friendly, owner-oriented labels instead of raw technical metric outputs.

## 5. Promotion-to-Active Criteria
The candidate layout may only be copied/promoted to the live `🏠 Dashboard` tab when:
1. The `🧪 Dashboard Lite Candidate` tab is fully built and populated.
2. The Owner manually reviews and signs off on the candidate tab layout.
3. A validation document recording the Owner's explicit approval is committed to ASB.

## 6. Rollback Strategy & Scheduler Status
- **Rollback**: If a candidate iteration fails, the candidate tab is simply deleted or reset; the live `🏠 Dashboard` remains untouched.
- **Scheduler**: The periodic refresh scheduler remains **OFF/parked**.
