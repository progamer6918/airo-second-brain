---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY System Architecture

## 1. Architecture Objective

Separate business knowledge, operational artifacts, calculation logic, and reporting so the project can evolve from an Excel prototype to a governed Power BI solution without losing traceability.

## 2. Two-Plane Model

### Knowledge and Governance Plane

Stored in ASB:

- product requirements;
- architecture;
- data contracts;
- formula definitions;
- decisions;
- validation plans;
- sanitized evidence.

### Artifact and Runtime Plane

Stored local-only or in an approved private workspace:

- raw sales, stock, target, and dealer data;
- operational workbook;
- original presentation;
- PBIX;
- screenshots with business data;
- private follow-up records;
- refresh credentials and gateway configuration.

## 3. Current State

```text
Source Exports
    ↓
Excel Paste Zones and Master Mapping
    ↓
Excel Calculation Table
    ↓
Hierarchy Report and Status Review
    ↓
Manual Business Validation
```

The workbook is a logic and interaction prototype. It is not the target automation platform.

## 4. Target State

```text
Governed Source Files
    ↓
Power Query Ingestion
    ↓
Standardization and Data Quality
    ↓
Star Schema
    ↓
DAX Semantic Measures
    ↓
Unified Power BI Report
    ↓
Exception Review and Follow-up
```

## 5. System Boundaries

D-READY consumes target, sales, stock, dealer master, product master, base-color mapping, calendar, and contribution information.

D-READY produces monitoring metrics and coordination indicators.

D-READY does not create a final logistics allocation or distribution transaction.

## 6. Core Layers

### Source Layer

Monthly target, sales to date, stock snapshot, historical color sales, dealer master, product master, color map, selling-day calendar.

### Preparation Layer

File validation, schema normalization, key standardization, raw-to-base color mapping, duplicate detection, unmapped detection, snapshot-date validation.

### Model Layer

Dealer, date, product, color, parameter dimensions and target, sales, stock, contribution facts.

### Calculation Layer

Achievement, sales pace, outlook, stock coverage, operational coverage, status, and estimated need.

### Presentation Layer

One primary report, validation view, data-quality view, and future follow-up view.

## 7. Control Principles

- authoritative totals remain authoritative;
- detail mapping must reconcile to totals;
- parent metrics use metric-specific aggregation;
- no silent data loss;
- no production claim without runtime evidence;
- no confidential operational artifact in public ASB.
