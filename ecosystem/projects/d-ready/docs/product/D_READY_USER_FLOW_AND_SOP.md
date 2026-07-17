---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY User Flow and SOP

## 1. Current Excel Pilot Flow

```text
Prepare source
→ Update calendar
→ Update target, sales, and stock
→ Validate totals and mappings
→ Select dealer
→ Review hierarchy
→ Validate critical status
→ Coordinate
```

## 2. Target Power BI Daily Flow

```text
Place approved source files
→ Validate file names and schema
→ Refresh dataset
→ Verify refresh result
→ Review data-quality page
→ Review Potential Loss Sales and Low Stock
→ Validate material cases
→ Coordinate
→ Record follow-up
```

## 3. Operator Roles

### Data Analyst

Owns data update, refresh, schema check, cut-off check, and data-quality triage.

### Sales or Supervisor

Owns exception review, business validation, priority, and follow-up.

### Management

Owns aggregated monitoring and policy decisions.

### Logistics Stakeholder

Validates feasibility and executes decisions through the logistics process. D-READY does not replace this authority.

## 4. Daily Control Checklist

- correct report month;
- correct sales cut-off;
- current stock snapshot;
- selling-day calendar current;
- no material unmapped record;
- target total reconciled;
- sales total reconciled;
- stock total reconciled;
- contribution valid;
- critical cases reviewed.

## 5. Incident Handling

Stop normal use when:

- source schema changes;
- totals fail reconciliation;
- snapshot date is stale;
- contribution is invalid;
- formula errors appear;
- refresh fails;
- unauthorized data becomes visible.

## 6. Time Measurement

Operating time may be measured after the process is stable. Until then, do not use an unverified duration as a primary project benefit.
