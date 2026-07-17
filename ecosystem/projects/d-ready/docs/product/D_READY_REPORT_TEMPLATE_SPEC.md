---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
artifact_role: EXCEL_LOGIC_AND_REPORT_PROTOTYPE

# D-READY Excel Report Template Specification

## 1. Workbook Role

The Excel workbook is the current logic and report prototype. It validates business rules, hierarchy behavior, source mapping, formulas, and user interaction before Power BI implementation.

It is not the target production automation platform.

## 2. Logical Sheets

### Report Template

Contains the user-facing report, filter controls, hierarchy, calculations, and governed source paste zones.

### Master Data

Contains dealer, product, color, parameter, and contribution mappings.

### Calendar Control

Contains report date, selling days, Sundays, holidays, elapsed days, and remaining days.

## 3. Report Column Contract

| Column | Metric |
|---|---|
| A | Hierarchy label |
| B | Type code |
| C | Base color code |
| D | Target |
| E | Sales |
| F | Achievement |
| G | Target Daily Sales |
| H | Daily Sales |
| I | Outlook |
| J | Stock |
| K | Actual Stock Days |
| L | Lead Time |
| M | Operational Stock Days |
| N | Status |
| O | Estimated Needs |
| P | Color Contribution |

Exact cell addresses are maintained in the private artifact specification because the public repository must not expose operational workbook details unnecessarily.

## 4. Hierarchy Behavior

```text
Grand Total → Segment → Subsegment → Series → Type → Base Color
```

Use native outline or drill behavior. Parent rows aggregate direct children only.

## 5. Source Behavior

- type target: direct lookup by dealer and type code;
- color target: type target multiplied by contribution;
- type sales: authoritative source type total;
- color sales: raw colors mapped and summed to base color;
- type stock: authoritative source type total;
- color stock: raw colors mapped and summed to base color.

## 6. User Workflow

1. update report period and calendar;
2. paste or refresh approved sources;
3. validate source totals;
4. review data-quality exceptions;
5. select dealer context;
6. expand the hierarchy;
7. review status;
8. validate material Estimated Needs;
9. coordinate follow-up.

## 7. Usability Rules

- formula cells are protected;
- paste zones are visually distinct;
- no unexplained helper tables in the user area;
- blanks and zeros have defined meanings;
- formulas must be traceable;
- normal operation does not require formula editing.

## 8. Prototype Acceptance

The workbook is accepted as a logic baseline only after formula errors, source reconciliation, hierarchy aggregation, edge cases, and reopen persistence are verified on the owner workbook.
