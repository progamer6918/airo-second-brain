---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
document_status: ACTIVE_REFERENCE_CANDIDATE

# D-READY Metric and Formula Specification

## 1. General Rules

- Calculations operate at the current filter grain.
- Parent rows aggregate only direct children.
- Ratios and coverage measures are recalculated from parent numerators and denominators.
- Blank, zero, and no-activity states are semantically distinct.
- Parameter values are stored in governed master data and are not exposed in this public document.

## 2. Target

### Type Target

Authoritative monthly target at month, dealer, and type grain.

### Color Target

```text
Color Target = Type Target × Color Contribution
```

Full-precision color targets must reconcile to the authoritative type target within the approved tolerance.

## 3. Sales

### Type Sales

Authoritative source total for the selected dealer and type.

### Color Sales

Sum of source color values after mapping raw source color codes to the governed base color.

## 4. Achievement

```text
Achievement = Sales ÷ Target
```

When Target is zero, return blank rather than a division error.

## 5. Target Daily Sales

```text
Target Daily Sales = Target ÷ Total Selling Days
```

## 6. Daily Sales

```text
Daily Sales = Sales to Date ÷ Selling Days Elapsed
```

## 7. Outlook

```text
Outlook = Sales to Date + Daily Sales × Remaining Selling Days
```

## 8. Demand Rate

Current design candidate:

```text
Demand Rate = MAX(Target Daily Sales, Daily Sales)
```

Purpose: retain a demand basis when actual sales are temporarily zero but an approved target exists.

## 9. Stock

### Type Stock

Authoritative stock total for the selected dealer and type.

### Color Stock

Sum of source color values after raw-to-base color mapping.

## 10. Actual Stock Days

```text
Actual Stock Days = Stock ÷ Demand Rate
```

When Demand Rate is zero, return blank.

## 11. Lead Time

Lead time is governed by dealer or area classification. Exact internal parameter values remain outside the public repository.

## 12. Operational Stock Days

The operator and business interpretation remain pending owner ratification. Current implementations and prior designs have used different treatments.

See `D_READY_STATUS_AND_EST_NEEDS_RULES.md`.

## 13. Status

Status is a deterministic decision tree based on effective demand, stock, operational coverage, target coverage, and no-activity conditions.

## 14. Estimated Needs

Estimated Needs is a coordination indicator. The final formula and parent aggregation are not yet canonical.

## 15. Parent Aggregation

| Metric | Parent Rule |
|---|---|
| Target | Sum direct children |
| Sales | Sum direct children |
| Stock | Sum direct children |
| Achievement | Parent Sales ÷ Parent Target |
| Daily metrics | Recalculate from parent inputs |
| Coverage | Parent Stock ÷ Parent Demand |
| Status | Recalculate at parent grain |
| Estimated Needs | Pending explicit rule |
| Contribution | Leaf color only |

## 16. Error Contract

The calculation layer must not return:

```text
#REF!
#DIV/0!
#VALUE!
#N/A
#NAME?
```
