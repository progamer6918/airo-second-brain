# Live Pass: Dashboard v2 Promotion to Main Dashboard

## 1. Metadata
* **Verification Date**: 2026-05-31
* **Apps Script Deployment**: `@227`
* **Apps Script Deployment ID**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`

---

## 2. Implementation Overview
This task promotes the approved `🏠 Dashboard v2` layout, metric formatting, and dynamic period logic to become the official main `🏠 Dashboard` tab.

The promotion is executed via the `admin promote dashboard` admin webhook command which performs the following operations:
1. **Backup Existing Dashboard**: Renames the existing `🏠 Dashboard` sheet to `_AIRO_Dashboard_Pre_Promote_Backup_YYYYMMDD_HHMMSS` to ensure historical backups are preserved and name conflicts are avoided.
2. **Archive Approved V2 Sheet**: Renames the approved `🏠 Dashboard v2` sheet to `_AIRO_Dashboard_v2_Approved_YYYYMMDD_HHMMSS` as an archive of the approved preview.
3. **Copy to Main Dashboard**: Copies the archived approved v2 sheet to create the new official `🏠 Dashboard` sheet.
4. **Position Main Tab**: Moves the new `🏠 Dashboard` sheet to the first position in the spreadsheet.

Additionally:
* The spreadsheet `onEdit(e)` trigger was updated to monitor G2 edits on both `🏠 Dashboard` and `🏠 Dashboard v2` sheets, dynamically rebuilding the layout for the active sheet.
* Rebuild and readback routes were generalized and exposed via webhook to support targeted validation of the main `🏠 Dashboard` tab.

---

## 3. Live Webhook Output
The promotion was run and validated via webhook using `trigger_promoted_build.sh`.

### Webhook 1: admin promote dashboard
```json
{
    "ok": true,
    "handled": true,
    "command": "dashboard_promote",
    "write_performed": true,
    "google_write_performed": true,
    "result": {
        "ok": true,
        "sheetNames": [
            "🏠 Dashboard",
            "_AIRO_Dashboard_Pre_Promote_Backup_20260601_075204",
            "_AIRO_Ops_Center",
            "_AIRO_Email_Ingestion_Log",
            "_AIRO_Audit_Log",
            "📌 Finance Events",
            "📒 Account Ledger",
            "💵 Cash Ledger",
            "💸 Transactions",
            "_AIRO_Dedupe_Log",
            "💳 Credit Card",
            "🏠 Cicilan Rumah",
            "🤝 Hutang",
            "🥇 Aset",
            "📅 Monthly Review",
            "🧾 Review Queue",
            "⚙️ Settings",
            "🔄 Sync Log",
            "_AIRO_Dashboard_Backup_20260526_221845",
            "_AIRO_Dashboard_Template_Claude",
            "_AIRO_Dashboard_v2_Approved_20260601_075204"
        ],
        "message": "Existing 🏠 Dashboard renamed to backup _AIRO_Dashboard_Pre_Promote_Backup_20260601_075204. Approved 🏠 Dashboard v2 renamed to _AIRO_Dashboard_v2_Approved_20260601_075204 and copied to official 🏠 Dashboard."
    }
}
```

### Webhook 2: admin dashboard build
```json
{
    "ok": true,
    "handled": true,
    "command": "dashboard_build",
    "write_performed": true,
    "google_write_performed": true,
    "result": {
        "ok": true,
        "command": "sprint6_dashboard_v2_build",
        "dashboard_tab": "🏠 Dashboard",
        "dashboard_gid": 1271746299
    }
}
```

### Webhook 3: admin dashboard readback
```json
{
    "ok": true,
    "handled": true,
    "command": "dashboard_readback",
    "write_performed": false,
    "google_write_performed": false,
    "result": {
        "ok": true,
        "command": "sprint6_dashboard_v2_readback",
        "spreadsheet_id": "1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU",
        "dashboard_found": true,
        "template_found": true,
        "dashboard_rows": 36,
        "dashboard_cols": 13,
        "marker_status": {
            "ACTION REQUIRED": true,
            "EXECUTIVE COMMAND CENTER": true,
            "WALLET & CASHFLOW": true,
            "DOMAIN HEALTH": true,
            "SPENDING INTELLIGENCE": true,
            "DATA QUALITY CENTER": true,
            "SMART INSIGHT PANEL": true
        },
        "required_marker_pass_count": 7,
        "required_marker_total": 7,
        "required_marker_pass": true,
        "has_technical_ops": false,
        "column_width_mismatch_count": 0,
        "row_height_mismatch_count": 0,
        "error_cells": [],
        "raw_formula_cells": []
    }
}
```

---

## 4. Verification & Analysis
* **Successful Promotion**: The promotion webhook completed successfully, placing the new official `🏠 Dashboard` in the first position and renaming the old sheets to their respective timestamped backups.
* **Layout and formatting preserved**: Column width and row height mismatch counts both equal `0`.
* **Zero Formula Errors**: Readback successfully validated that there are no visible `#NAME?`, `#REF!`, `#N/A`, or `#VALUE!` cells in the cockpit `A1:K41` range.
* **Zero Raw Formulas**: Confirmed no visible raw `=SUMIF(...)` or debug/logical cells exist.
* **Technical Ops Hidden**: No operational metadata (deployment ID, Apps Script runtimes) is present in the cockpit area.
* **Active Selector Dropdown**: Period selector is configured on `G2` and functions with data validation lists.
* **Minor Accepted Visual Debt**:
  - Wallet no-data helper text may be clipped in narrow columns.
  - 0% spending progress bars remain as neutral empty tracks (`░░░░░░░░░░`).
  - Critical alerts card color polish is deferred.
