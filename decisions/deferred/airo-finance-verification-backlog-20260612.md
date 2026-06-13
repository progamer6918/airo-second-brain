# AIRO Finance Verification & Project Backlog — 2026-06-12

This backlog stores pending verification checks and deferred project items that are not blocking the runtime activation.

## Deferred Verification Backlog (VERIFY_FIRST)

### 1. CC Ledger-first Production Deploy
- **Status**: Deferred verification
- **Details**: Verify if CC ledger-first source patch is deployed to production Apps Script version 288 (ID `AKfycbzu0...`, description: `"AIRO Task 9 CC ledger-first guard"`).
- **Required Evidence**: direct inspection of Apps Script deployment or live smoke test.

### 2. CC Ledger-first Source Patch
- **Status**: Deferred verification
- **Details**: Verify if Credit Card source patch is committed in the local AIRO Finance repository (commit `9297b1d7d166484b82d6ff9770fd6e78fa55e8ec`).
- **Required Evidence**: git log check or static diff check.

### 3. Task 9 CC Parser Deploy
- **Status**: Deferred verification
- **Details**: Verify if Credit Card parser amount deploy (Task 9 checkpoint) is active in version 291.
- **Required Evidence**: direct inspection of Apps Script deployment or live smoke test.

### 4. AIRO Sync Operating Rule
- **Status**: Deferred verification
- **Details**: Verify if the AIRO Sync cross-session closeout rules should be formalized in canonical documents.
- **Required Evidence**: review of AGENTS.md and CURRENT.md updates.

## Deferred Project Backlog (DEFER)

### 5. Dashboard Audit + Patch Split Decision
- **Status**: Deferred project item
- **Details**: Dashboard migration away from Finance Events toward Account Ledger/domain source tabs.
- **Required Evidence**: direct review of Dashboard formulas and script dependency graph.
