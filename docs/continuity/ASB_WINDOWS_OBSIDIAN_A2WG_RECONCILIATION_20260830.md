# ASB Windows Obsidian A2-WG Reconciliation Record

**Date**: 2026-08-30  
**Session ID**: `015a196c-af0c-4a2e-b1a0-dff7888dc83d`  
**Selected Architecture**: `A2_WG` (Windows Physical ASB + Windows Native Git Interop)  
**Reconciliation Status**: `CLEAN_AUTOMERGE_CANDIDATE_READY`  
**Migration Readiness**: `READY_FOR_ONE_SHOT_A2WG_CUTOVER`  

## 1. Source Trees and Heads
- **Canonical WSL ASB**: `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain` (HEAD: `6a2c4d7b1df5226ab5c0527a1246d3f2e5a38143`)
- **Windows Live Clone**: `C:\Users\Admin\AI_WORKSPACES\airo-second-brain` (HEAD: `7fd70d426535cfd26d6b3fe103e654f47c1c21a2`)
- **Reconciliation Base**: `7fd70d426535cfd26d6b3fe103e654f47c1c21a2` (Windows clone is ancestor of canonical)

## 2. Reconciliation Summary
- **Total Windows Owner Deltas Analyzed**: 159 paths
- **Prior Safe Preserved Changes**: 154 paths
- **Final Five Conflicts Resolved**: 5 paths (all proven stale subsets of canonical authority)
- **Total Preserved Safe Changes**: 159 / 159 paths (100%)
- **Ambiguous Conflicts Remaining**: 0

## 3. Provenance Resolution of Five Ambiguous Paths
1. `state/deferred-work.json`: Windows copy is a stale subset lacking post-session-06 items; Canonical authority preserved.
2. `wiki/workdesk/STATUS_DATA.md`: Machine-generated WorkDesk status projection; Canonical authority preserved.
3. `worklog/daily/2026-08-25.md`: Duplicate session links already in Canonical; Canonical authority preserved.
4. `worklog/daily/2026-08-27.md`: Duplicate session links already in Canonical; Canonical authority preserved.
5. `worklog/sessions/2026-08-27/AIRO WorkDesk/06 - AWD Root Close Eligibility Repair.md`: Identical session UUID (`35e39665-...`), Windows copy is incomplete draft; Canonical completed session authority preserved.

## 4. Final Migration Candidate Artifacts
- **Reconciliation Patch**: `/tmp/asb_a2wg_final_reconciliation_patch_20260830_085917.patch` (SHA256: `abed100259229804e8ed4d246b7b0b3e4b7ad8e8ec3b5d6724aa770f26682e3d`)
- **Operation Manifest**: `/tmp/asb_a2wg_final_reconciliation_manifest_20260830_085917.json` (SHA256: `2f6e6589cd78218c305a5e5ce453c77e6e9c79d26f71603b646cea647f44d309`)

## 5. Invariants
- **Live Migration Performed**: `NO`
- **Both Trees Mutated**: `NO`


## 6. Mandatory Rollback Execution Record (2026-08-30)
- **Cutover ID**: `20260830_090632`
- **Rollback Status**: `ROLLED_BACK_AFTER_FAILED_ACCEPTANCE`
- **Reason**: Production acceptance criterion `HERMES_ACTIVE=YES` failed (actual: `NO`).
- **Contract Enforcement**: Post-failure repair forbidden; exact preauthorized rollback executed.
- **Failed Evidence Preserved**: `C:\Users\Admin\AI_WORKSPACES\airo-second-brain.failed-a2wg-20260830_090632`
- **Restored State**:
  - Canonical WSL ASB restored to physical directory `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain`.
  - Windows clone restored to `C:\Users\Admin\AI_WORKSPACES\airo-second-brain`.
  - Scoped Git shim removed.
- **Future Governance**: Architecture A2-WG remains technically proven in design, but production activation FAILED under one-attempt contract. Any future attempt requires a new Architecture Council decision and explicit Owner approval.



## 7. Device-Local State Preservation Lesson (Remotely Save)
- **Incident**: Remotely Save sync failed post-cutover because `.obsidian/plugins/remotely-save/data.json` is Git-ignored and was not synchronized with device-local active credentials during initial candidate construction.
- **Repair**: Exact pre-cutover `data.json` restored from `airo-second-brain.pre-a2wg-attempt2-windows-20260830_091926`.
- **Sync Acceptance**: `PASS` (`ACTIVE_SYNC_ACCEPTED`).
- **Lesson**: Future ASB filesystem cutovers must inventory and preserve required Git-ignored application-local configuration files separately from Git repository tracking.



## 8. Remotely Save 97.3% Safety Abort Forensic & Correction (2026-08-30)
- **Status Correction**: Prior automated sync acceptance was a `FALSE_POSITIVE` (command palette completed, but plugin triggered 50% safety abort modal `5399/5546=97.3%`).
- **Real Status**: `FAIL_97_3_PERCENT_SAFETY_ABORT` (Plugin is currently `BROKEN_PENDING_SAFE_METADATA_REPAIR`).
- **Forensic Finding**: 99.28% of shared files are byte-identical but have newer `mtime` timestamps due to Git checkout during candidate build (median delta ~73.4 days). Remotely Save compares `localMtime > lastSyncMtime` and scheduled 5,399 files for re-upload.
- **Protection Maintained**: 50% safety abort prevented bulk redundant remote re-upload.
- **Recommended Repair**: Safe timestamp normalization for byte-identical files (`RESTORE_SAFE_MTIMES_FOR_BYTE_IDENTICAL_FILES`).



## 9. Remotely Save Safe Mtime Repair & Sync Acceptance (2026-08-30)
- **Status**: `REMOTELY_SAVE_POST_A2WG_STATUS=ACTIVE_SYNC_ACCEPTED_AFTER_SAFE_MTIME_REPAIR`
- **Root Cause**: `A2WG_MIGRATION_MTIME_CHURN_WITH_PRESERVED_SYNC_BASELINE`
- **Repair Executed**: Safe mtime restoration applied to 2917 byte-identical files.
- **Sync Reproof**: Planned changes reduced from 5399 (97.3%) to 2482 (44.75%), safely below the 50% protection threshold.
- **Acceptance**: Real sync executed and verified with zero destructive operations and zero aborts.
- **Architectural Lesson**: Filesystem cutovers must preserve both device-local application state and sync-sensitive metadata (mtime) where external tools rely on timestamps.



## 10. Remote Mutation Evidence Correction (2026-08-30)
- **Evidence Correction**: Previous receipt note on remote mutation is clarified: `REMOTE_MUTATION_OCCURRED=YES` (`EXPECTED_SAFE_PUSH_ONLY`).
- **Sync Transfer Breakdown**:
  - `REMOTE_PUSH_COUNT`: 2482 (Safe upload of genuine post-cutover changes/deltas)
  - `REMOTE_PULL_COUNT`: 0
  - `REMOTE_DELETE_COUNT`: 0
  - `LOCAL_DELETE_COUNT`: 0
  - `CONFLICT_COUNT`: 0
- **Durable Verdict**: Remotely Save sync is healthy, authorized, and completely accepted with zero destructive actions.

