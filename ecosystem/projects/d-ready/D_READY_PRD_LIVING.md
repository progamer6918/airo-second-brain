---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
document_status: ACTIVE_REFERENCE_CANDIDATE
version: 0.1.0

# D-READY Living Product Requirements Document

## 1. Executive Summary

D-READY converts fragmented dealer stock monitoring into a structured early-alert workflow. It combines monthly target, sales velocity, dealer stock, selling-day calendar, replenishment lead time, product hierarchy, and base-color contribution to identify readiness conditions and support coordinated follow-up.

The current Excel workbook is a calculation and report prototype. The target operational platform is Power BI.

## 2. Product Vision

Create one governed monitoring experience that allows an authorized user to move from data refresh to prioritized exception review without rebuilding manual analysis for every dealer, type, or color.

The intended reading sequence is:

```text
Target → Sales → Demand Rate → Stock → Coverage → Status → Estimated Need
```

## 3. Problem Statement

Target, sales, stock, product, calendar, dealer, and historical color data are maintained in different structures and grains. Without a governed model, users must reconcile these inputs manually before they can judge whether a dealer is adequately stocked.

## 4. Goals

D-READY shall:

1. Monitor readiness from aggregate hierarchy to type and base-color detail.
2. Support an all-dealer context and an authorized single-dealer context.
3. Preserve authoritative type targets while allocating color targets through controlled contribution rules.
4. Calculate sales pace, outlook, stock coverage, operational coverage, status, and estimated need consistently.
5. Identify no-stock risk, low coverage, healthy coverage, excess coverage, and stock-without-sales conditions.
6. Remain auditable from report output back to source and master mapping.
7. Be operable through a simple daily workflow.
8. provide a validated calculation contract for Power BI implementation.

## 5. Non-Goals

D-READY shall not:

- determine final unit allocation;
- replace logistics planning;
- infer supply availability from unrelated internal stock;
- publish confidential dealer data to unauthorized users;
- depend on Macro/VBA as its target architecture;
- treat a visual prototype as production evidence;
- claim a time-saving KPI before actual measurement.

## 6. Primary Users

### Data Analyst

Updates source data, refreshes the model, reviews data-quality exceptions, and confirms the reporting cut-off.

### Sales or Supervisor

Reviews readiness exceptions, validates business context, prioritizes coordination, and records follow-up.

### Management

Reviews aggregated readiness, material exceptions, and follow-up effectiveness.

### Dealer Stakeholder

Provides local context and executes agreed actions. Dealer access requires an approved security model.

## 7. Functional Scope

### Included

- dealer filter context;
- segment, subsegment, series, type, and base-color hierarchy;
- monthly target;
- sales to date;
- achievement;
- target daily sales;
- actual daily sales;
- month-end outlook;
- dealer stock;
- actual stock coverage days;
- replenishment lead time;
- operational stock days;
- readiness status;
- estimated needs;
- data-quality exceptions;
- Excel-to-Power BI parity validation.

### Excluded

- final allocation;
- automated transfer order;
- logistics replacement;
- confidential cross-dealer comparison without authorization;
- raw operational artifact storage in public ASB.

## 8. Product Hierarchy

```text
Grand Total
  └── Segment
       └── Subsegment
            └── Series
                 └── Type
                      └── Base Color
```

Parents aggregate only direct children. A parent must not sum both type totals and their color children because that creates double counting.

## 9. Key Requirements

### DREADY-REQ-001 — Product Identity

Type code is the stable product key. Type description is a display label, not the primary key.

### DREADY-REQ-002 — Color Standardization

Raw source colors must map to a governed base-color code before reporting.

### DREADY-REQ-003 — Type Target Authority

Type target comes directly from the target source at month, dealer, and type grain.

### DREADY-REQ-004 — Color Target Allocation

Color target equals authoritative type target multiplied by governed color contribution. Full-precision color allocations must reconcile to the type target within the approved tolerance.

### DREADY-REQ-005 — Sales and Stock Source Totals

Type-level sales and stock come from authoritative source totals. Color-level values come from mapped raw-color details.

### DREADY-REQ-006 — Calendar

Daily metrics use governed selling days. Sundays and approved holidays are excluded according to the calendar specification.

### DREADY-REQ-007 — Readiness Status

Status must be deterministic, parameter-driven, and recalculated at the current reporting grain.

### DREADY-REQ-008 — Estimated Need

Estimated Need is a coordination indicator, not an allocation instruction. Its final formula remains blocked until owner ratification and edge-case validation.

### DREADY-REQ-009 — Unified Report

Power BI shall provide one primary report experience with governed filters and access control rather than unrelated internal and dealer dashboards.

### DREADY-REQ-010 — Evidence

No implementation, parity, refresh, deployment, or business-impact claim may be marked complete without direct evidence.

## 10. Non-Functional Requirements

### Accuracy

No double counting, silent mapping loss, or unhandled calculation error.

### Auditability

Every reported value must trace to source, key, mapping, formula, report date, and validation result.

### Maintainability

Rules should live in tables or measures, not scattered hard-coded formulas.

### Usability

The main workflow must be understandable by a nontechnical operator.

### Security

Public ASB stores only sanitized knowledge. Operational artifacts remain local-only or private.

### Performance

The final Power BI report must remain responsive at normal filter and drill depth.

## 11. Success Criteria

The pilot is successful when:

- authoritative source totals reconcile;
- type and color target logic reconcile;
- selected dealer-type-color cases match the approved Excel logic;
- status edge cases pass;
- no unmapped material record is silently discarded;
- one operator can complete the documented refresh and validation workflow;
- Power BI and Excel produce approved parity results.

## 12. Current Constraints

- final Estimated Needs formula is open;
- Operational Stock Days semantics require explicit ratification;
- nonpilot contribution fallback requires approval;
- active and inactive product-color governance requires approval;
- Power BI runtime and refresh are not yet proven;
- production access model is not yet approved.

## 13. Acceptance Boundary

This PRD is an `ACTIVE_REFERENCE_CANDIDATE`. It may guide documentation and validation design. It must not be treated as an execution-complete production contract until the pending decisions are closed and owner approval promotes it.
