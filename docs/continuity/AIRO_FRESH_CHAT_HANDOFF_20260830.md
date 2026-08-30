# AIRO Fresh Chat Continuity Handoff (2026-08-30)

This document is the canonical entry point index for fresh AI sessions continuing AIRO ecosystem work.

## 1. Active Architecture State (ASB)
- **Status**: `A2WG_PRODUCTION_STATUS=ACTIVE` (Attempt #2 Accepted)
- **Physical Repository Truth**: `C:\Users\Admin\AI_WORKSPACES\airo-second-brain` (Windows NTFS)
- **WSL Logical Path**: `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain` (Symlink)
- **Owner Platform Requirement**: `WINDOWS` (Windows Obsidian)
- **Git Backend**: Scoped WSL shim (`~/.local/bin/git`) delegating ASB commands to `C:\Program Files\Git\cmd\git.exe` (~106ms status latency)
- **Runtime Policy**: `PRESERVE_PRE_CUTOVER_RUNTIME_STATE` (Hermes baseline `NOT_RUNNING`)
- **Key Decision Records**:
  - `decisions/decision-log.md` -> `DEC-20260830-05`
  - `docs/continuity/ASB_WINDOWS_OBSIDIAN_A2WG_RECONCILIATION_20260830.md`
  - `docs/continuity/KCC_CLOSED_SESSION_VISIBILITY_DEFECT_20260829.md`

## 2. EAB / Finance / Orchestration State
- **Product Status**: `EAB_PRODUCT_STATUS=NOT_OPERATIONAL`
- **EAB Repair Chain**: `DEAD` (No further EAB patch loops)
- **Root Postmortem**: Live failure happened before Arfin specialist invocation (`ARFIN_SPECIALIST_CALL_OBSERVED=NO`).
- **Next Engineering Project**: `EARESMES_CAPABILITY_ROUTER_FOUNDATION`
- **Key Reference**:
  - `ecosystem/projects/earesmes-arfin-bridge/docs/EAB_POST_VNEXT_ORCHESTRATION_BOUNDARY_DECISION_20260830.md`
  - `decisions/decision-log.md` -> `DEC-20260830-06`

## 3. Operational Invariants
- `NO_ACTIVE_MIGRATION_WORK=YES`
- `ONE_PHYSICAL_ASB=YES`
- `SYNC_ENGINE=NONE`
- `GIT_PROMOTION_STATUS=LOCAL_CANONICAL_WORKTREE_UNPUSHED`


## 4. Remotely Save Device-Local State
- **REMOTELY_SAVE_STATUS**: `ACTIVE_SYNC_ACCEPTED`
- **A2WG_DEVICE_LOCAL_STATE_LESSON**: Git-ignored application-local state (`.obsidian/plugins/remotely-save/data.json`) requires explicit migration preservation.


- **REMOTELY_SAVE_STATUS**: `HEALTHY` (Active sync accepted after safe mtime repair)

- **REMOTELY_SAVE_REMOTE_SYNC_MUTATION**: `EXPECTED_SAFE_PUSH_ONLY` (2482 pushes, 0 deletes, 0 conflicts)
- **A2WG_PRODUCTION_STATUS**: `ACTIVE`


## 5. KCC Session Memory Architecture
- **KCC_SESSION_NOTE_POLICY**: `HUMAN_FIRST_V2` (Layer 1 Owner Visible in plain Indonesian + Layer 2 Machine Context comment block).
- **PRIMARY_AUDIENCE**: Owner (non-technical).
- **PREVIOUS_PROMOTION_CANDIDATE_STATUS**: `STALE_DO_NOT_PUSH` (Re-audit required after KCC V2 update).

