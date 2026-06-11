---
last_updated: 2026-06-11
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
---

# Report Automation VBA

This project file is the canonical context for Excel/VBA-based report automation work inside the AIRO ecosystem.

The first active implementation is the Honda Report Automation Command Center pilot, but the project name intentionally remains generic because the pattern is reusable for other departments, templates, and recurring reports.

## Current Objective

Build a Command Center workbook that automates recurring Excel report creation by importing daily raw data files, refreshing template staging sheets and pivots, generating final report outputs, and logging process results.

The long-term objective is to reduce repetitive manual report preparation time across multiple report templates that share overlapping raw data sources.

## Active Implementation

Active pilot:

- Command Center workbook: `Command_Center.xlsm`
- Main report family: `SALES_5PIVOT`
- Active reports:
  - `RPT001` Monitoring Dealer
  - `RPT002` Report Per Type
- Registered but not processed:
  - `RPT003` Result VE

## Project Folder Structure

```text
Honda_Report_Automation_Pilot_Package
├── 00_Command_Center
│   └── Command_Center.xlsm
├── 01_Raw_Data
│   ├── Today
│   └── Archive
├── 02_Reference Data
│   └── SSU.2026.xlsx
├── 03_Report_Templates
│   ├── MONITORING DEALER.xlsx
│   ├── Report Per Type.xlsx
│   └── Result VE.xlsm
├── 04_Working_Output
├── 05_Log
└── 06_VBA_Modules
```

## Report Registry

| Report ID | Report Name | Template | Family | Final Output Sheet | Status |
|---|---|---|---|---|---|
| RPT001 | Monitoring Dealer | MONITORING DEALER.xlsx | SALES_5PIVOT | Sales Comparison Dealer | Active |
| RPT002 | Report Per Type | Report Per Type.xlsx | SALES_5PIVOT | Comparison by Type | Active |
| RPT003 | Result VE | Result VE.xlsm | Mapping Required | TBD | Do not process yet |

## SALES_5PIVOT Family

Reports in this family share the same core staging and pivot structure:

```text
Raw Data SSU M
Data SSU YTD
Raw Data Stock D
Raw Data Stock MD
Inden
Pivot SSU M
Pivot SSU M-1
Pivot Stock D
Pivot Stock MD
Pivot Inden
```

Required source files:

```text
Monitoring Penjualan Dealer Daily
SSU
Stok_per_no_mesin_dealer
StokMD
Inden-FIPS
```

Not used yet in `SALES_5PIVOT`:

```text
export_leads
Picking_list_unit
```

## Last Confirmed Working Baseline

The confirmed working baseline is the R4/R5-style Monitoring Dealer engine.

Known confirmed result:

- `RPT001 Monitoring Dealer` successfully generates the final report.
- Final output sheet is `Sales Comparison Dealer`.
- Template can be processed even when the user removed the `Ach. Outlook` column.
- The macro must not force-create or repair `Ach. Outlook` when the template intentionally does not contain that column.

## Current RPT002 Status

`RPT002 Report Per Type` belongs to the same `SALES_5PIVOT` family.

Known latest run status:

- Source imports succeeded.
- Five pivots refreshed.
- Failure happened during helper copy into `Comparison by Type`.
- Detected area `Comparison by Type!II5:IJ124` contained formulas.
- The macro correctly avoided overwriting formulas, but the process should not fail only because formula-protected helper or output cells exist.

Required behavior:

- Preserve formula areas.
- Skip unsafe helper copy when formula cells are detected.
- Log a warning.
- Continue saving the report when the rest of the process succeeds.

## Result VE Rule

`Result VE.xlsm` must not be processed yet.

Reason:

- Uses Data Model.
- Uses workbook connections.
- Uses external Master Data.
- Uses large formula staging.
- Requires separate mapping analysis.

Registry status:

```text
MAPPING_REQUIRED
```

Do not create dummy mappings such as:

```text
SalesData_
VEData_
Raw_VEData
```

## VBA Development Rules

For this project, the assistant must behave as a production repair engineer.

Rules:

- Do not repeat trial-and-error loops.
- Do not provide scattered small patches unless explicitly requested.
- Prefer one complete module, one complete replacement block, or one safe manual edit path.
- Preserve the last confirmed working baseline.
- Do not replace a working R4/R5 engine with a speculative generic engine.
- Do not modify original templates.
- Always work from a copied working file in `04_Working_Output`.
- Do not modify `MULAI DI SINI!B2`.
- Public macros should use the `CC_` prefix.
- Do not damage workbook UI buttons or overlay layout.
- Do not claim compile success unless actually compiled or clearly label it as static validation only.
- If download links fail, provide pasteable text or a manual edit path immediately.

## Output Contract

Batch output should create:

```text
MONITORING_DEALER_yyyymmdd.xlsx
REPORT_PER_TYPE_yyyymmdd.xlsx
PROCESS_SUMMARY_yyyymmdd.xlsx
```

Output folder:

```text
04_Working_Output
```

## Recovery Rules

When a new module breaks compile:

1. Stop adding new changes.
2. Identify the exact highlighted compile line.
3. Restore or preserve the last working module.
4. Apply the minimum safe correction.
5. Compile before running.
6. Run only after compile passes.

When a report fails after successful imports and pivot refresh:

1. Check the run log.
2. Identify the exact failing stage.
3. Do not assume source data is wrong.
4. Protect formulas and template layout first.
5. Patch only the failing stage.

## Current Next Step

Continue from the R5-confirmed engine and apply formula-safe handling for `RPT002 Report Per Type`.

Do not process `Result VE` until mapping is explicitly completed.

## Session Closeout Requirement

At the end of meaningful work on this project, produce a session closeout containing:

- what changed
- what was confirmed
- what failed or remains uncertain
- next safest step
- files or modules touched
- evidence from logs, compile results, generated outputs, or owner confirmation