---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Excel–Power BI Parity Plan

## 1. Objective

Prove that approved Power BI measures reproduce the approved Excel business logic at controlled test grains.

## 2. Baseline Requirements

- owner-approved Excel workbook version;
- workbook hash;
- approved formula specification;
- fixed report date;
- fixed source snapshot;
- sanitized test-case identifiers.

## 3. Required Sample Classes

- at least one dealer from each lead-time classification;
- All Dealer;
- one product from each governed segment;
- one no-stock case;
- one zero-sales case;
- one no-activity case;
- one overstock case;
- one raw-to-base color consolidation case;
- one zero-history contribution case;
- one parent aggregation case.

## 4. Comparison Fields

- Target;
- Sales;
- Stock;
- daily metrics;
- outlook;
- stock coverage;
- operational coverage;
- status;
- Estimated Needs.

## 5. Tolerance

Exact tolerance for decimal metrics must be documented before execution. Integer source totals require exact equality.

## 6. Failure Classification

- source mismatch;
- mapping mismatch;
- filter-context mismatch;
- formula mismatch;
- rounding mismatch;
- stale snapshot;
- expected business-rule change.

## 7. Exit Gate

Parity is `PASS` only when all critical cases pass or each approved variance has a signed decision record.
