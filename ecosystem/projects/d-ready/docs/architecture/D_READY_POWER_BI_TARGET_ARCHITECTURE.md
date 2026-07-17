---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
architecture_status: TARGET_NOT_YET_PROVEN

# D-READY Power BI Target Architecture

## 1. Target Data Flow

```text
Approved Source Location
    ↓
Power Query
    ├── Sales ingestion
    ├── Stock ingestion
    ├── Target ingestion
    ├── Dealer master
    ├── Product and color master
    ├── Contribution profile
    └── Calendar
    ↓
Data Quality Gate
    ↓
Star Schema
    ↓
DAX Measures
    ↓
Report and Validation Pages
```

## 2. Proposed Model

### Dimensions

- `DimDate`
- `DimDealer`
- `DimProduct`
- `DimColor`
- `DimContributionProfile`
- `DimReadinessParameter`

### Facts

- `FactSales`
- `FactStockSnapshot`
- `FactMonthlyTarget`
- `FactHistoricalColorSales`
- `FactColorContribution`
- future `FactFollowUp`

## 3. Relationship Principles

- one-to-many from dimensions to facts;
- single-direction filters by default;
- type code and base-color code use surrogate or governed composite keys;
- All Dealer is represented by absence of dealer filtering, not a fake dealer row;
- stock uses snapshot date, not transaction date.

## 4. Semantic Measures

Measures, not duplicated calculated columns, should implement:

- Target;
- Sales;
- Achievement;
- Target Daily Sales;
- Daily Sales;
- Outlook;
- Demand Rate;
- Stock;
- Actual Stock Days;
- Operational Stock Days;
- Status;
- Estimated Needs.

## 5. Report Pages

### Main Readiness Page

Unified hierarchy matrix, KPI cards, slicers, status formatting, refresh timestamp, reporting cut-off.

### Validation Page

Source totals, mapped totals, Excel parity sample, exception trace.

### Data Quality Page

Unmapped dealer, type, color, missing target, duplicate grain, invalid contribution, stale snapshot.

### Follow-up Page

Future state after workflow and ownership are approved.

## 6. Refresh Model

Target operating direction: one Data Analyst maintains the daily update process. Refresh frequency, gateway, source folder, and credential model remain pending implementation decisions.

## 7. Security

Dealer-facing access requires approved row-level security or separately governed export. The architecture must prevent unauthorized cross-dealer visibility.

## 8. Promotion Gate

The target architecture is not production-ready until:

- source contracts are proven;
- critical formulas are locked;
- Excel parity passes;
- data-quality gates pass;
- refresh and access controls are validated;
- owner acceptance is recorded.
