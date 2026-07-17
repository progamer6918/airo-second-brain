---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
document_status: ACTIVE_REFERENCE_CANDIDATE
estimated_needs_status: OPEN

# D-READY Status and Estimated Needs Rules

## 1. Status Vocabulary

- `POTENTIAL_LOSS_SALES`
- `LOW_STOCK`
- `HEALTHY`
- `OVER_STOCK`
- `NEED_SALES_REVIEW`
- `NO_ACTIVITY`

Display labels may differ from semantic codes. For example, the report may display a neutral symbol for `NO_ACTIVITY`.

## 2. Status Intent

### Potential Loss Sales

Demand exists or is expected, while stock is unavailable or operational coverage is critically low.

### Low Stock

Operational coverage is below the governed target but above the critical-risk threshold.

### Healthy

Operational coverage is within the governed healthy band.

### Over Stock

Operational coverage exceeds the governed upper band.

### Need Sales Review

Stock exists but sales movement is zero or the demand basis is not sufficient for a reliable coverage interpretation.

### No Activity

Target, sales, and stock are all effectively zero.

## 3. Decision Order

The rule order is important:

```text
1. No Activity
2. Stock zero with demand
3. Stock exists with zero sales
4. Missing coverage basis
5. Critical coverage
6. Low Stock
7. Healthy
8. Over Stock
```

Exact thresholds are governed internal parameters and are intentionally not stored in this public-safe specification.

## 4. Effective Target

A governed effective-unit rule may be used to prevent immaterial fractional color targets from creating misleading alerts. The rounding method requires explicit documentation and parity testing.

## 5. Operational Stock Days Conflict

Two interpretations have existed:

### Interpretation A

```text
Operational Stock Days = MAX(0, Actual Stock Days - Lead Time)
```

This treats lead time as coverage consumed before replenishment can arrive.

### Interpretation B

```text
Operational Stock Days = Actual Stock Days + Lead Time
```

This has appeared in later workbook behavior but requires an explicit business explanation because it changes the risk direction.

No Power BI implementation may lock this measure until the owner ratifies the intended meaning.

## 6. Estimated Needs Business Meaning

Estimated Needs estimates a stock gap for coordination. It is not a final allocation instruction, purchase order, or logistics commitment.

## 7. Formula Candidates

### Required-Stock Candidate

```text
Required Stock = Approved Demand Rate × Required Coverage
Estimated Needs = MAX(0, Required Stock - Current Stock)
```

### Coverage-Gap Candidate

```text
Estimated Needs =
MAX(0, Coverage Gap × Approved Demand Rate)
```

### Hybrid Candidate

Uses a separate fallback when stock is zero or the coverage metric is blank.

## 8. Mandatory Edge Cases

The selected formula must pass:

- target zero, sales zero, stock zero;
- target positive, sales zero, stock zero;
- target zero, sales positive, stock zero;
- sales zero, stock positive;
- fractional color target;
- missing operational coverage;
- overstock;
- parent aggregation;
- All Dealer context;
- zero historical color sales.

## 9. Promotion Rule

`Estimated Needs` remains `OPEN`. Any document or dashboard treating one candidate as final without owner approval is noncanonical.
