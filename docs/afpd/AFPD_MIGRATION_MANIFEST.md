# AFPD Migration Manifest

## Proposed AFPD Structure
The proposed skeleton design for the unified AIRO Finance Project Documentation (AFPD) is structured as follows:
- `AFPD.md` — Sole project documentation entrypoint
- `docs/afpd/00_CURRENT_HANDOFF.md` — Current verified snapshot and handoff instructions
- `docs/afpd/01_PROJECT_CHARTER.md` — Project mission, scope, and core decisions
- `docs/afpd/02_ARCHITECTURE_AND_GOVERNANCE.md` — Durable architecture and developer governance rules
- `docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md` — Reconciled active Arfin runtime behavior rules
- `docs/afpd/04_RUNTIME_TOPOLOGY.md` — Runtime configuration, functions, properties, and system boundaries
- `docs/afpd/05_STATE_MACHINES.md` — Diagrammed flow states for intake, pending, and approval
- `docs/afpd/06_DATA_AND_WORKBOOK_CONTRACTS.md` — Detailed sheet schema contracts and status policies
- `docs/afpd/07_OPERATIONS_DEPLOYMENT_TRIGGERS.md` — Deployment mechanisms, versions, triggers, and operations
- `docs/afpd/08_ROADMAP.md` — Historical and current Task/Gate execution roadmap
- `docs/afpd/09_DECISION_REGISTER.md` — Durable register of project decisions
- `docs/afpd/10_PROGRESS_LOG.md` — History of session progress logs
- `docs/afpd/11_INCIDENT_REGISTER.md` — Log of production incidents and resolutions
- `docs/afpd/12_EVIDENCE_INDEX.md` — Index of validation logs and check proofs
- `docs/afpd/99_HISTORICAL_AND_SUPERSEDED.md` — Deprecated systems (e.g., Cash Ledger, old roadmaps)

## Scope and Phase 2 Limits
- **Final Kitab & ARFIN.md**: The original files `AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md` and `ARFIN.md` remain completely untouched, undeleted, and unnamed in this phase.
- **AFPD.md Canonical Declaration**: AFPD.md is not declared canonical in this phase. It remains PROPOSED until all migration gates are successfully verified.
- **Mutations Allowed**: Only documentation files under `docs/afpd/` and `docs/progress/` are created, and `meta/changelog.md` is updated.
- **Verifications**: Node.js syntax checks are performed on Apps Script files, confirming zero syntax errors and that the source SHA remains unchanged.

## Phase 2 Completeness Check
- All 69 Final Kitab headings have been mapped to exactly one target destination in the section map.
- All 12 ARFIN headings have been mapped to `03_ARFIN_RUNTIME_CONTRACT.md`.
- Apparent orphan authority files have been classified.
- The 5 contradictions have been resolved in plan form.
- The v371-v375 progress/incident logs have been backfilled in plan form.
- The 9 file:/// links have been verified and resolved.
