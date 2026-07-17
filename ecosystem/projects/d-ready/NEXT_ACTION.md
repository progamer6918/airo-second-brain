---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Next Action

```text
NEXT_ACTION_ID=DREADY-GATE-001
OBJECTIVE=Ratify the remaining business rules before Power BI data-model implementation.
MUTATION_ALLOWED=DOCUMENTATION_AND_OWNER_DECISION_ONLY
PRODUCTION_MUTATION_ALLOWED=NO
```

## Required Owner Decisions

1. Define the business meaning and operator for Operational Stock Days.
2. Approve the final Estimated Needs formula and aggregation behavior.
3. Approve the color-contribution fallback for dealers without a specific profile.
4. Approve product and color active/inactive lifecycle governance.
5. Define the Potential Loss Sales KPI unit.

## Expected Evidence

- approved decision records;
- worked examples for critical edge cases;
- no unresolved contradiction between PRD, formula specification, and workbook behavior.

## Stop Condition

Stop before Power BI implementation if any critical formula or grain remains ambiguous.
