# AFPD Authority Matrix

## Proposed Authority Hierarchy
The future authority hierarchy for AIRO Finance project documentation and configuration is proposed as follows (prioritized highest to lowest):
1. `AFPD.md` — Sole project documentation entrypoint
2. `docs/afpd/00_CURRENT_HANDOFF.md` — Current verified snapshot
3. `docs/afpd/03_ARFIN_RUNTIME_CONTRACT.md` — Active Arfin runtime behavior rules
4. `docs/afpd/02_ARCHITECTURE_AND_GOVERNANCE.md` — Durable architecture and developer governance rules
5. `docs/afpd/08_ROADMAP.md` — Current Task/Gate execution roadmap
6. Source code + immutable Apps Script version (e.g., `AIRO_Finance_Multitab_Final_v1.js`)
7. Live runtime evidence (e.g., deployment info, triggers, workbook metadata)
8. decision, progress, incident, validation, and historical records

*Note: This hierarchy is currently PROPOSED and will only be activated upon the completion of the final migration.*

## Classification of Apparent Orphan Authority Files
The following files containing canonical/source-of-truth claims outside the core authority files are classified as follows:

1. `ecosystem/projects/vortex-ai-skill-lab/airo_finance_task9_readonly_preflight_20260620_214904.txt`
   - **Classification**: `EVIDENCE_SNAPSHOT_WITH_EMBEDDED_DOCUMENTS`
   - **Authority Status**: Not an independent authority. It represents a read-only validation check of the live workbook at a specific timestamp.
   - **Action**: Reference in `docs/afpd/12_EVIDENCE_INDEX.md`.

2. `ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_CANONICAL_ROADMAP_LOCK.md`
   - **Classification**: `LEGACY_POINTER_TO_FINAL_KITAB`
   - **Authority Status**: Superseded. This was a temporary pointer file locking Sprint 6/7 roadmap scopes.
   - **Action**: Deprecate and map to `docs/afpd/99_HISTORICAL_AND_SUPERSEDED.md`.

3. `ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_SPRINT_7_EMAIL_INGESTION_DECISION_GATE.md`
   - **Classification**: `HISTORICAL_DECISION_RECORD`
   - **Authority Status**: Historical. The phrase "primary source" inside this file refers to the raw Telegram/Email input structure, not documentation authority.
   - **Action**: Map to `docs/afpd/09_DECISION_REGISTER.md`.

4. `ecosystem/projects/vortex-ai-skill-lab/docs/personal-workflow/handoff/AIRO_FINANCE_V1_2_YOLO_CARRYOVER_2026_05_20.md`
   - **Classification**: `HISTORICAL_HANDOFF`
   - **Authority Status**: Historical. The terminal output statements contained within represent evidence-precedence context for legacy migrations.
   - **Action**: Map to `docs/afpd/99_HISTORICAL_AND_SUPERSEDED.md`.

5. `ecosystem/projects/vortex-ai-skill-lab/docs/personal-workflow/phase-3/AIRO_PHASE_3_ROADMAP.md`
   - **Classification**: `DIFFERENT_PROJECT_SCOPE`
   - **Authority Status**: Out of Scope. This file relates to general ASB Phase 3 roadmap planning, not AIRO Finance documentation authority.
   - **Action**: File remains outside the AIRO Finance AFPD scope.

## Kode.js Classification
- **File**: `ecosystem/projects/vortex-ai-skill-lab/apps-script-live/Kode.js`
- **Classification**: Legacy neutralized compatibility source code.
- **Active doPost Count**: 0.
- **Active Handler**: `AIRO_Finance_Multitab_Final_v1.js` is the sole active doPost handler.
- **Governance Rule**: Do not delete this file during AFPD migration to maintain project structure compatibility.
- **Documentation Location**: `docs/afpd/04_RUNTIME_TOPOLOGY.md` under legacy source inventory.
