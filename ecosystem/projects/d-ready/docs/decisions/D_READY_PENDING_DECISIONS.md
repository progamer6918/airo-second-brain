---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---

# D-READY Pending Decisions

## DREADY-PENDING-001 — Operational Stock Days

- Issue: Earlier design and later workbook behavior use different lead-time treatments.
- Required decision: business meaning, formula operator, blank handling, parent behavior.
- Stop condition: do not lock Power BI measure before owner approval.

## DREADY-PENDING-002 — Estimated Needs

- Issue: Candidate formulas produce materially different results in stock-zero, fractional-target, and parent cases.
- Required decision: formula, demand basis, rounding, stock-zero fallback, aggregation.
- Stop condition: do not declare the metric canonical.

## DREADY-PENDING-003 — Contribution Fallback

- Issue: Dealer-specific contribution is not available for every dealer.
- Candidate: dealer profile, else all-dealer profile, else equal split across active colors.
- Required decision: approve order and validation.

## DREADY-PENDING-004 — Active Product-Color Governance

- Issue: unexpected or obsolete colors can receive target and status if the active master is incorrect.
- Required decision: authoritative active list, approver, effective date, review flow.

## DREADY-PENDING-005 — Product Lifecycle

- Issue: runout or discontinued types require treatment separate from color activity.
- Required decision: lifecycle states and report inclusion.

## DREADY-PENDING-006 — Potential Loss Sales KPI Unit

- Options: case count, dealer count, type count, color count, or estimated units.
- Required decision: one business definition for KPI cards and presentation.

## DREADY-PENDING-007 — Power BI Refresh

- Required decision: source location, manual or scheduled refresh, gateway, owner, frequency, failure notification.

## DREADY-PENDING-008 — Access Model

- Required decision: internal-only, row-level security, governed export, or another approved model.

## DREADY-PENDING-009 — Follow-Up Record

- Required decision: storage platform, fields, owner, closure criteria, and privacy treatment.

## DREADY-PENDING-010 — Pilot Scope

- Required decision: official pilot dealer scope and acceptance sample.
- Public rule: dealer identities remain outside public ASB.
