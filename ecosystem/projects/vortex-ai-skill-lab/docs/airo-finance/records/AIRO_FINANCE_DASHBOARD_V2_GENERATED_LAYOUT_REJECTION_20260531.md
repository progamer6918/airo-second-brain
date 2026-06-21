# AIRO Finance — Dashboard v2 Generated Layout Rejection Record

**Date**: 2026-05-31  
**Sprint**: Dashboard Pixel-Reference Template Clone Implementation  
**Decision**: REJECT current `🏠 Dashboard v2` generated layout  
**Status**: PENDING RECOVERY via Template Import approach

---

## Why the Generated Layout Was Rejected

The Apps Script cell-by-cell rebuild of `🏠 Dashboard v2` was rejected by the user after live visual inspection. The following problems were observed:

| Issue | Description |
|---|---|
| Text wrapping | Labels and values wrap vertically due to row height / column width mismatch |
| Section misalignment | Sections do not align with the Excel reference A1:K41 compact canvas |
| Broken topbar | Row 2 topbar does not match the reference topbar layout |
| Action cards mismatch | Action Required cards do not visually match the reference 2x2 layout |
| `#N/A` visible | Formula errors appear in the visible cockpit area |
| Overall | Layout is **not** a visual clone of the Excel reference |

### Root Cause

Google Sheets Apps Script cannot reliably reproduce the visual fidelity of an Excel-designed dashboard because:
- Column width, row height, and font rendering differ between Excel and Google Sheets
- Cell-by-cell `setBackground`, `setFontSize`, `setFontFamily`, `setColumnWidth` calls stack visual rounding errors
- Merged cell layout, formula semicolon/comma separators, and conditional format rules all behave differently
- Unicode progress bars render at different glyph widths per platform
- Apps Script `setFormula` vs `setFormulaR1C1` vs `setFormulaLocal` and locale-dependent separator (`,` vs `;`) cause `#N/A` errors

---

## What Was Tried (and Failed)

| Attempt | Version | Error |
|---|---|---|
| Initial pixel-reference layout push | v205 | `Anda harus memilih semua sel dalam rentang penggabungan` (merge conflict) |
| Moved breakApart before clear | v206 | `Data yang dimasukkan ke sel G2 melanggar aturan validasi` (G2 validation error) |
| Added G2 normalization | v207 | BUILD OK, READBACK PASS 10/10 markers — but **visual inspection REJECTED** |

All three versions passed unit tests and readback marker checks, but the visual output did not match the Excel reference.

---

## New Canonical Approach: Template Import

### Decision
**Do NOT continue patching the Apps Script generated layout.**

Instead:
1. Import the Excel reference file as a real Google Sheets tab: `_AIRO_Dashboard_Template_Claude`
2. Apps Script `🏠 Dashboard v2` build copies this template sheet (not redraws it)
3. Dynamic formulas are wired **only after** visual template clone is confirmed by user

### Reference Files
- **Excel template**: `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.xlsx`
- **Reference screenshot**: `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.png`
- **Excel spec**: `docs/airo-finance/records/AIRO_FINANCE_DASHBOARD_EXCEL_REFERENCE_SPEC_20260531.md`

### Target sheet name
`_AIRO_Dashboard_Template_Claude`

### Why this approach is correct
- The Excel file contains the exact visual layout, column widths, row heights, fonts, colors, and merged cells already rendered correctly
- Google Sheets can import an Excel file and preserve most styling faithfully
- Apps Script `copyTo()` and `setValues()` from a real template sheet is far more reliable than cell-by-cell reconstruction
- Dynamic formula wiring is separated from visual layout (two-phase approach)

---

## Current State of Protected Tabs

| Tab | Status |
|---|---|
| `🏠 Dashboard` | ✅ Untouched — main dashboard preserved |
| `🏠 Dashboard v2` | ⚠️ Contains broken generated layout — do not promote |
| `_AIRO_Dashboard_Template_Claude` | ❌ Does not yet exist — needs import |

---

## Recovery Plan (see `AIRO_FINANCE_DASHBOARD_TEMPLATE_IMPORT_RECOVERY_PLAN_20260531.md`)
