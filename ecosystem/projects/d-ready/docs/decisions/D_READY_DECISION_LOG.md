---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Decision Log

## DREADY-DEC-001 — Monitoring and Early-Alert Role

- Status: `LOCKED`
- Decision: D-READY is a Sales monitoring and early-alert tool.
- Boundary: It does not determine final logistics allocation.

## DREADY-DEC-002 — Platform Direction

- Status: `LOCKED`
- Decision: Excel is the current logic/report prototype; Power BI is the target operational platform.

## DREADY-DEC-003 — Macro/VBA

- Status: `LOCKED`
- Decision: Macro/VBA is not the final solution architecture.

## DREADY-DEC-004 — Product Key

- Status: `LOCKED`
- Decision: Type code is the stable product key. Description is a display attribute.

## DREADY-DEC-005 — Hierarchy

- Status: `LOCKED`
- Decision: Reporting hierarchy extends from aggregate segment to type and base color.

## DREADY-DEC-006 — Target Source

- Status: `LOCKED`
- Decision: Type target comes directly from the authoritative target source.

## DREADY-DEC-007 — Color Target

- Status: `LOCKED`
- Decision: Color target equals type target multiplied by governed color contribution.

## DREADY-DEC-008 — Sales and Stock

- Status: `LOCKED`
- Decision: Type values use authoritative source totals; color values use raw-to-base color mapping.

## DREADY-DEC-009 — No Historical Color Sales

- Status: `LOCKED_DIRECTION`
- Decision: When a type has no usable historical color sales, contribution is distributed equally across approved active colors.
- Constraint: The active-color master must be approved.

## DREADY-DEC-010 — Segment-Specific Coverage Targets

- Status: `LOCKED`
- Decision: Target Stock Days differ by product segment and are governed parameters.

## DREADY-DEC-011 — Status Terminology

- Status: `LOCKED`
- Decision: Use `Potential Loss Sales` rather than the older `Runout Risk` label.

## DREADY-DEC-012 — Evidence

- Status: `LOCKED`
- Decision: Dummy impact data is prohibited. Use actual evidence or a clearly marked placeholder.

## DREADY-DEC-013 — Time-Saving Claim

- Status: `LOCKED`
- Decision: Do not use an operating-time claim as a headline KPI until measured under the stabilized method.

## DREADY-DEC-014 — Presentation Alignment

- Status: `LOCKED`
- Decision: All improvement steps must use the same current architecture, vocabulary, scope, and status rules.

## DREADY-DEC-015 — Unified Report Direction

- Status: `CURRENT_DIRECTION`
- Decision: Prefer one unified Power BI reporting experience with governed filters and access control.
- Constraint: Dealer access model remains pending.
