# AIRO Finance Project Documentation (AFPD)

> [!IMPORTANT]
STATUS=PROPOSED_NOT_CANONICAL
PHASE=CONTENT_MIGRATION
CANONICAL_ACTIVATION=PENDING_OWNER_APPROVAL

## Phase 4.2 Status Note
- **NORMATIVE_REMEDIATION**: PASS
- **EVIDENCE_DURABILITY**: PARTIAL
- **NEXT_GATE**: INDEPENDENT_REAUDIT

## Phase 4.2 Status Note
- **NORMATIVE_REMEDIATION**: PASS
- **EVIDENCE_DURABILITY**: PARTIAL
- **NEXT_GATE**: INDEPENDENT_REAUDIT
>
> WARNING: Old project documentation files (including Final Kitab, ARFIN.md, Living PRD, and CURRENT.md) remain authoritative until activation is approved by the Owner. This document acts only as a proposed navigation entrypoint.

## Proposed Authority Hierarchy
The future authority hierarchy for AIRO Finance project documentation and configuration is proposed as follows:
1. [AFPD.md](AFPD.md) — Sole project documentation entrypoint
2. [00_CURRENT_HANDOFF.md](docs/afpd/00_CURRENT_HANDOFF.md) — Current verified snapshot
3. [03_ARFIN_RUNTIME_CONTRACT.md](docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md) — Active Arfin runtime behavior rules
4. [02_ARCHITECTURE_AND_GOVERNANCE.md](docs/afpd/02_ARCHITECTURE_AND_GOVERNANCE.md) — Durable architecture and developer governance rules
5. [08_ROADMAP.md](docs/afpd/08_ROADMAP.md) — Current Task/Gate execution roadmap
6. Source code + immutable Apps Script version (e.g., `AIRO_Finance_Multitab_Final_v1.js`)
7. Live runtime evidence (e.g., deployment info, triggers, workbook metadata)
8. Decision, progress, incident, validation, and historical records

## Required Reading Order
For all future sessions, developers/AI must bootstrap using this order:
1. Read [AFPD.md](AFPD.md)
2. Read [00_CURRENT_HANDOFF.md](docs/afpd/00_CURRENT_HANDOFF.md)
3. Verify current Apps Script source SHA and deployment version
4. Verify workbook trigger/runtime state
5. Read relevant [10_PROGRESS_LOG.md](docs/afpd/10_PROGRESS_LOG.md) and [11_INCIDENT_REGISTER.md](docs/afpd/11_INCIDENT_REGISTER.md)
6. Check for contradiction resolutions in [03_ARFIN_RUNTIME_CONTRACT.md](docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md)

## Navigation Modules
- [00_CURRENT_HANDOFF.md](docs/afpd/00_CURRENT_HANDOFF.md) — Handoff snapshot
- [01_PROJECT_CHARTER.md](docs/afpd/01_PROJECT_CHARTER.md) — Project charter and operating principles
- [02_ARCHITECTURE_AND_GOVERNANCE.md](docs/afpd/02_ARCHITECTURE_AND_GOVERNANCE.md) — Governance rules and durability
- [03_ARFIN_RUNTIME_CONTRACT.md](docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md) — Active Arfin runtime behavior rules
- [04_RUNTIME_TOPOLOGY.md](docs/afpd/04_RUNTIME_TOPOLOGY.md) — Deployment/Webhook runtime map
- [05_STATE_MACHINES.md](docs/afpd/05_STATE_MACHINES.md) — Intake flow state machines
- [06_DATA_AND_WORKBOOK_CONTRACTS.md](docs/afpd/06_DATA_AND_WORKBOOK_CONTRACTS.md) — Sheet schema contracts
- [07_OPERATIONS_DEPLOYMENT_TRIGGERS.md](docs/afpd/07_OPERATIONS_DEPLOYMENT_TRIGGERS.md) — Clasp operations & triggers
- [08_ROADMAP.md](docs/afpd/08_ROADMAP.md) — Active roadmaps and gates
- [09_DECISION_REGISTER.md](docs/afpd/09_DECISION_REGISTER.md) — Log of durable decisions
- [10_PROGRESS_LOG.md](docs/afpd/10_PROGRESS_LOG.md) — Backfilled v371-v375 logs
- [11_INCIDENT_REGISTER.md](docs/afpd/11_INCIDENT_REGISTER.md) — Active incident logs
- [12_EVIDENCE_INDEX.md](docs/afpd/12_EVIDENCE_INDEX.md) — Index of validation proofs
- [99_HISTORICAL_AND_SUPERSEDED.md](docs/afpd/99_HISTORICAL_AND_SUPERSEDED.md) — Superseded materials

<!-- BEGIN AFPD_BOOT_ENFORCEMENT -->
## Boot Enforcement

BOOT_ENTRYPOINT=AFPD_BOOT_BUNDLE.md
BOOT_MANIFEST=docs/afpd/AFPD_BOOT_MANIFEST.tsv
BOOT_ENTRYPOINT_STATUS=ACTIVE
AFPD_BOOT_BUNDLE_SHA256=648d78dc3d0284ff74e135fac3e1c097fa2712139e8febfbede069291ab20c18
LATEST_PROGRESS_READ_LAST=YES
CURRENT_HANDOFF_READ_LAST=YES
AFPD_STATUS=PROPOSED_NOT_CANONICAL
CANONICAL_ACTIVATION=PENDING_OWNER_APPROVAL
EVIDENCE_DURABILITY=PARTIAL
<!-- END AFPD_BOOT_ENFORCEMENT -->
