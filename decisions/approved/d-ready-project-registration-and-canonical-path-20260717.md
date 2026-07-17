---
decision_id: ASB-DREADY-REG-20260717
status: OWNER_APPROVED_FOR_REGISTRATION
scope: ASB_PROJECT_REGISTRATION
last_updated: 2026-07-17
---

# D-READY Project Registration and Canonical Path

## Decision

Register D-READY as an active ASB project node.

```text
PROJECT_ID=DREADY
DISPLAY_NAME=D-READY
FULL_NAME=Dealer Stock Readiness Early Alert Dashboard
CANONICAL_PATH=ecosystem/projects/d-ready/
PROJECT_STATUS=ACTIVE
PROJECT_STAGE=PILOT_LOGIC_VALIDATION
PRD_STATUS=ACTIVE_REFERENCE_CANDIDATE
```

## Architecture Boundary

- Excel is the current logic/report prototype.
- Power BI is the target operational platform.
- Macro/VBA is not the final architecture.
- D-READY supports monitoring and early alert, not final logistics allocation.

## Repository Safety

ASB is public. Only sanitized public-safe documentation may be committed. Operational workbooks, original presentations, PBIX files, dealer identities, actual commercial data, and private evidence remain outside public ASB.

## Global Pointers

Registration should update:

- `PRD_INDEX.md`
- `ROADMAP_INDEX.md`
- `CURRENT.md`

## Completion Evidence

This decision authorizes registration. It does not prove that files were committed, pushed, or remotely synchronized.
