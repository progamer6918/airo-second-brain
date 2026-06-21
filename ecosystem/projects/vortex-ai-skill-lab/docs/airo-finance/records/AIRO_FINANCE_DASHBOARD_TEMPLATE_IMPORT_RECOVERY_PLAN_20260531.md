# AIRO Finance — Dashboard Template Import Recovery Plan

**Date**: 2026-05-31  
**Task**: Dashboard Excel Template Import Recovery Pass  
**Status**: PLAN — awaiting user manual import step

---

## Context

The Apps Script cell-by-cell generated `🏠 Dashboard v2` layout was visually rejected.
See: `docs/airo-finance/records/AIRO_FINANCE_DASHBOARD_V2_GENERATED_LAYOUT_REJECTION_20260531.md`

The new canonical approach imports the Excel reference as a Google Sheets template tab first, then uses Apps Script to copy it into `🏠 Dashboard v2`.

---

## Phase 1: Import Excel Template into Google Sheets

### Method A — Manual Import (RECOMMENDED — safest, no API re-auth needed)

**Step-by-step instructions for the user:**

1. Open the AIRO Finance Google Spreadsheet in your browser
2. Click **File → Import**
3. Select **Upload** tab
4. Upload the file: `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.xlsx`
5. In the "Import file" dialog, set:
   - **Import location**: `Insert new sheet(s)` ← IMPORTANT
   - **Separator type**: Detect automatically
   - **Convert numbers, dates, and formulas**: Yes
6. Click **Import data**
7. A new sheet will be created — Google Sheets will name it `Dashboard` (from the Excel tab name)
8. Rename that sheet to exactly: `_AIRO_Dashboard_Template_Claude`
9. Verify the visual layout matches the Excel reference screenshot

**After import, tell the agent:** "Template imported as `_AIRO_Dashboard_Template_Claude`" and send a screenshot.

---

### Method B — Drive API Upload (automated, but requires re-auth with Drive scope)

The existing OAuth token only has `spreadsheets` scope (not `drive` scope).  
A Drive API upload would require the user to re-authorize the OAuth client with `drive.file` scope added.

**This method is NOT recommended** unless Method A fails, because:
- It requires adding a new OAuth scope
- It requires re-running the browser-based OAuth flow
- It is slower and introduces more failure modes

If the user wants to use Method B anyway, a helper script `scripts/personal-workflow/airo_import_excel_to_sheets.py` can be prepared (see Phase 1B below).

---

## Phase 1B: Drive API Import Script (Optional — only if Method A fails)

A helper script would:
1. Re-authenticate with `drive.file` + `spreadsheets` scopes
2. Use `drive.files().create()` with `mimeType=application/vnd.google-apps.spreadsheet` to convert the xlsx
3. Use `drive.files().export()` or `sheets.spreadsheets.sheets.copyTo()` to copy the Dashboard sheet from the converted file into the live spreadsheet
4. Rename the copied sheet to `_AIRO_Dashboard_Template_Claude`
5. Delete the temporary converted spreadsheet

---

## Phase 2: Visual Verification (User action)

After import:
- Open `_AIRO_Dashboard_Template_Claude` in Google Sheets
- Compare visually with `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.png`
- Send screenshot to agent for confirmation

**Accept criteria:**
- Dark background visible
- Section headers visible (ACTION REQUIRED, EXECUTIVE COMMAND CENTER, etc.)
- Column widths approximately match the reference
- No formula errors visible
- Static sample values are OK at this stage

---

## Phase 3: Apps Script — Copy Template to Dashboard v2

After Phase 2 is confirmed, the Apps Script `airoSprint6DashboardV2Build_` function will be patched to:

1. Find `_AIRO_Dashboard_Template_Claude` sheet
2. Copy it using `sheet.copyTo(ss)` (the same mechanism used for Dashboard backups)
3. Rename the copy to `🏠 Dashboard v2` (replacing or removing the old broken tab)
4. Set the sheet position (move it to the correct tab order)

This means Apps Script will no longer rebuild the layout from scratch — it will always copy the template.

```javascript
// Phase 3 pseudocode (not yet patched)
function airoSprint6DashboardV2Build_(ss, options) {
  const template = ss.getSheetByName('_AIRO_Dashboard_Template_Claude');
  if (!template) throw new Error('Template not found: _AIRO_Dashboard_Template_Claude');
  
  // Remove old v2 if exists
  const oldV2 = ss.getSheetByName('🏠 Dashboard v2');
  if (oldV2) ss.deleteSheet(oldV2);
  
  // Copy template
  const v2 = template.copyTo(ss);
  v2.setName('🏠 Dashboard v2');
  
  // Move to correct position (after main Dashboard tab)
  // ... position logic ...
  
  return { ok: true, dashboard_tab: '🏠 Dashboard v2', dashboard_gid: v2.getSheetId() };
}
```

---

## Phase 4: Dynamic Formula Wiring (SEPARATE TASK — after visual approval)

Only after Phase 3 visual is approved:
- Wire G2 period selector dropdown
- Wire M2:M6 helper cells
- Wire SUMIFS formulas for wallet balances, inflow/outflow, spending, data quality
- Wire Smart Insight narratives

Formula wiring is a **separate task** — do NOT start until template visual is approved.

---

## Constraints Carried Forward

- ✅ Do NOT promote `🏠 Dashboard v2` until screenshot approved
- ✅ Do NOT overwrite `🏠 Dashboard`
- ✅ No Phase 6 / Gmail / email
- ✅ No Alert Engine core patch
- ✅ No transaction routing patch
- ✅ No live alert enable / trigger install

---

## File Inventory

| File | Role |
|---|---|
| `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.xlsx` | Canonical visual template source |
| `docs/airo-finance/references/AIRO_Finance_Dashboard_reference_20260531.png` | Reference screenshot |
| `docs/airo-finance/records/AIRO_FINANCE_DASHBOARD_EXCEL_REFERENCE_SPEC_20260531.md` | Layout geometry spec |
| `docs/airo-finance/records/AIRO_FINANCE_DASHBOARD_V2_GENERATED_LAYOUT_REJECTION_20260531.md` | Rejection record |
| `docs/airo-finance/records/AIRO_FINANCE_DASHBOARD_TEMPLATE_IMPORT_RECOVERY_PLAN_20260531.md` | This file |
