# ANTIGRAVITY EXECUTION PROMPT — AIRO Second Brain v0.4.1

## Handoff Prompt for Future Phases

Gunakan prompt berikut untuk memulai sesi eksekusi berikutnya pada AIRO Second Brain v0.4.1:

```text
You are executing AIRO Second Brain PRD v0.4.1 No-Brainer Execution Edition.

Repo:
/home/egitaristorandas/AI_WORKSPACES/airo-second-brain

Project repo:
/home/egitaristorandas/vortex-ai-skill-lab

## Core Rules
1. Do not redesign the architecture.
2. Do not add new modules (the count is locked at exactly 9 modules).
3. Do not implement v2 features.
4. Do not migrate repos into monorepo or introduce submodules.
5. Do not introduce browser extensions or AIRO Gateway.
6. Do not promote semantic canonical updates automatically.
7. Do not let Earesmes promote canonical knowledge.
8. Execute phases in order. Do not skip any phase.
9. Phase 1 starts only after Phase 0 PASS.

## Execution Sequence
Phase 0: Canonicalize PRD and execution docs. [CURRENT STATUS: PASS]
Phase 1: Registry & inventory.
Phase 2: Capture & health.
Phase 3: Sync & preflight.
Phase 4: Bootstrap & organize.
Phase 5: Distill & promote.
Phase 6: Stabilization & abuse testing.

## Post-Phase Protocol
After each phase:
1. Run the phase-specific validation commands.
2. Produce a clear PASS/FAIL/BLOCKED validation report.
3. Commit changes only if the validation returns PASS.
4. Push to remote origin only after the Secret Guard validation returns PASS.
5. STOP and wait for owner review if any of the following occur:
   - Secret guard hit (blocking commit/push)
   - Git merge conflict
   - Registry serialization or corruption errors
   - Unexpected dirty critical governed repository

## Technical Specifications
- Bootstrap must call preflight automatically. Consumers must not be expected to remember preflight.
- Required health output: state/system-health.md
- Required registry: registry/repos.yaml
- Required scripts:
  * scripts/airo-inventory
  * scripts/airo-bootstrap
  * scripts/airo-preflight
  * scripts/airo-capture
  * scripts/airo-sync
  * scripts/airo-organize
  * scripts/airo-distill
  * scripts/airo-promote
  * scripts/airo-health

Each script must support:
- --help
- --dry-run (where relevant)
- --json (where relevant)

Final results of each phase must include a clean git status, pushed remote GitHub state, master validation checklist updates, and no secret-like files committed.
```
