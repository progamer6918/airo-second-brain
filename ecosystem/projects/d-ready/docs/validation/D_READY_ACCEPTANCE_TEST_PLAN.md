---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Acceptance Test Plan

## 1. Data Tests

- dealer key completeness;
- type key completeness;
- raw-to-base color mapping;
- no unexpected duplicate grain;
- no material unmapped record;
- current report and snapshot dates.

## 2. Target Tests

- dealer-type target equals authoritative source;
- All Dealer target equals approved control total;
- color target reconciles to type target;
- active contribution reconciles to 100%;
- zero-history fallback uses approved active colors.

## 3. Sales Tests

- dealer filter changes results correctly;
- type sales equals source type total;
- mapped color sales equals source detail;
- mapped color sum reconciles to type total.

## 4. Stock Tests

- type stock equals source type total;
- mapped color stock equals source detail;
- mapped color sum reconciles to type total;
- snapshot date is visible and current.

## 5. Calendar Tests

- Sundays excluded;
- approved holidays excluded;
- total, elapsed, and remaining selling days correct;
- report-date changes propagate.

## 6. Metric Tests

- Achievement;
- Target Daily Sales;
- Daily Sales;
- Outlook;
- Demand Rate;
- Actual Stock Days;
- Operational Stock Days after ratification;
- Status;
- Estimated Needs after ratification.

## 7. Edge-Case Tests

- no activity;
- demand with no stock;
- stock with no sales;
- fractional color target;
- zero historical color sales;
- overstock;
- missing mapping;
- discontinued type;
- All Dealer;
- parent aggregation.

## 8. Error Scan

No visible or calculated:

```text
#REF!
#DIV/0!
#VALUE!
#N/A
#NAME?
```

## 9. Completion Evidence

A test is complete only with:

- test identifier;
- input;
- expected output;
- actual output;
- result;
- timestamp;
- artifact version or hash;
- validator.
