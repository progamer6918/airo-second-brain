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

<!-- AIRO:RAVBA_R811:BEGIN -->
## Final Platform Vision

Build a reusable, scalable, safe, auditable, and operator-friendly Excel/VBA Command Center platform for recurring report automation across multiple raw-data sources, templates, report families, operators, and eventually departments. Honda Report Automation is the first pilot, not the final scope.

## Permanent Product Criteria

- Daily operation is button-first from `MULAI DI SINI`; normal operators do not use Alt+F8.
- `CC_SOURCE_REGISTRY` and `CC_REPORT_REGISTRY` are the configuration sources of truth.
- Langkah 3 and Langkah 4 remain dynamic.
- Preserve the original UI, buttons, merged layout, and `MULAI DI SINI!B2`.
- Never modify original templates; process copied working files under `04_Working_Output`.
- Preserve formulas, pivots, helper areas, layout, connections, and report-specific date logic.
- Unknown templates follow `scan -> audit -> classify -> map -> approve -> activate`.
- Allowed classifications: `AUTO_READY`, `MAPPING_REQUIRED`, `BLOCKED`.
- Do not create speculative mappings.
- PASS, DONE, STABLE, compile success, and runtime success require evidence.
- Prefer one complete implementation package and preserve frozen baselines.

## Target Architecture

1. Operator layer: `MULAI DI SINI` and its daily buttons.
2. Configuration layer: source/report registries and dependency rules.
3. Audit/onboarding layer: headers, formulas, connections, external dependencies, family fit, mapping, approval.
4. Execution layer: resolver, sanitizer, staging import, adaptive writes, pivots, helpers, date logic, output generation.
5. Evidence layer: process/error logs, matched paths, runtime status, output paths, timestamps, Process Summary.
6. Governance layer: versioning, frozen baseline, rollback, approval gates, regression evidence, release notes.

## Roadmap

### Track 1 — Core Report Engine
- RPT001 Monitoring Dealer: complete and PASS.
- RPT002 Report Per Type: complete and business-output PASS.
- `SALES_5PIVOT`: working reusable family baseline.
- Additional report families: not started.

### Track 2 — Dynamic Platform
- Dynamic source/report registries: complete.
- BBN live sync and button-first UI: complete.
- Runtime status/output persistence and Process Summary truth: complete.

### Track 3 — Audit and Onboarding
- Active milestone: Automated Template Onboarding and Mapping Engine (Result VE is only the first proof case, not the product goal).
- Guided onboarding, template health center, and automated family-fit assessment: not started.

### Track 4 — Governance and Scale
- R8.11 frozen stable baseline and reopen persistence: complete.
- Rollback/release package: partially complete.
- Cross-department reuse: future milestone.

## Frozen Stable Baseline

- Version: R8.11.
- Module: `modHondaCommandCenter_R8_11_RUNTIME_EVIDENCE_PERSISTENCE.bas`.
- Status: `FROZEN STABLE BASELINE`.
- Close/reopen persistence: PASS.
- Confirmed outputs: `MONITORING_DEALER_20260611.xlsx`, `REPORT_PER_TYPE_20260611.xlsx`, `PROCESS_SUMMARY_20260611_01.xlsx`.

Do not modify frozen R8.11 directly. New development must use a copied candidate.

Confirmed PASS includes dynamic registries, BBN sync, original UI preservation, six main buttons and three toggles, button-first workflow, HTML-XLS sanitizer, adaptive import recovery, RPT001, RPT002, formula-safe Stock MD helper, visible report date, RPT003 safety block, Process Summary, runtime recovery, output-path recovery, and persistence after reopen.

## Automated Template Onboarding Spec

### Product Status

Current truthful status of the platform:
```text
Existing report operation = PASS
Admin readiness checker = PASS
Automated template discovery = NOT COMPLETE
Automated mapping draft = NOT COMPLETE
Generic new-report onboarding = NOT PROVEN
Reusable product platform = NOT COMPLETE
```
The platform is not production-complete until a previously unsupported template is onboarded successfully through the automated workflow.

### Proof-of-Product Requirement
The platform must demonstrate this flow:
```text
new unsupported template
→ automatic read-only discovery
→ draft mapping generated
→ minimal business confirmation
→ validated mapping stored
→ report classified READY
→ report executed through Command Center
→ output validated
→ status and evidence persisted
```

### Owner Input Boundary
- **Owner Role**: Supplies business intent and resolves choices that cannot be inferred safely.
- **Product Role**: Discovers technical workbook structure and generates mapping evidence.

#### Valid Owner Questions
- Which candidate sheet is the intended final report?
- Which visible date should appear on the report?
- Which business source is authoritative when two candidates exist?
- Should this report be active for daily production?

#### Invalid Owner Requests (Must be automated by scanner)
- List all hidden sheets.
- Screenshot all workbook connections.
- Map formula dependencies manually.
- Identify staging ranges manually.
- Inspect Power Pivot tables manually.
- Explain the internal workbook structure.

### Config Structures
The onboarding layer maintains these config structures:
- `CC_TEMPLATE_DISCOVERY`
- `CC_MAPPING_DRAFT`
- `CC_REPORT_SOURCE_MAP`
- `CC_REPORT_TARGET_MAP`
- `CC_REPORT_EXEC_RULES`
- `CC_REPORT_VALIDATION`
- `CC_REPORT_FAMILY`

### Status Lifecycle
A newly registered report moves through this lifecycle:
```text
DISCOVERED
→ NEEDS REVIEW
→ MAPPING REQUIRED
→ MAPPING VALIDATED
→ READY
→ ACTIVE
```
Unsafe templates become `BLOCKED`.

## Import Root Cause and Countermeasure

Some `.xls` source exports are HTML disguised as Excel and contain formula-like numeric artifacts such as `=32.600.000`. The sanitizer normalizes these values in working memory without changing the original source file. Verified normalization counts: Sales 44 cells; SSU 302 cells.

## Known Technical Debt

- Excel may temporarily raise `Out of memory`; adaptive splitting currently recovers.
- RPT002 has 3,382 legacy `#REF!` formulas in technical areas outside active range `A1:Q73`; this is not resolved.
- RPT003 remains `MAPPING_REQUIRED`.

## Current Next Step

Implement the Automated Template Onboarding and Mapping Engine. This is an onboarding milestone. Do not modify the frozen R8.11 baseline directly. Final classification must be `AUTO_READY`, `MAPPING_REQUIRED` with complete gaps, or `BLOCKED` with explicit reasons.
<!-- AIRO:RAVBA_R811:END -->
