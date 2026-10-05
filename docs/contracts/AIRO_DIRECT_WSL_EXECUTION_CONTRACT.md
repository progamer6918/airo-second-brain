# AIRO Direct WSL Execution Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-11
**Authority**: OWNER_APPROVED

1. When Owner says `via WSL`, use direct WSL; do not redirect to Antigravity or a manual file-download workflow.
2. Prefer one copy-paste-ready bounded execution packet per Owner interaction.
3. A packet may contain multiple deterministic sub-steps when no new Owner decision is required.
4. Optimize for the fewest safe Owner interaction cycles, not one technical sub-step per turn.
5. Antigravity low-limit one-small-gate behavior is a separate execution mode.
6. Stop at genuine boundaries: new Owner approval, unresolved identity/ambiguity, owner-work conflict, remote divergence, remote-runtime authorization, or required Owner visual/live acceptance.
7. The Owner interactive parent WSL shell MUST survive every outcome. Never apply `set -e`, `set -u`, or `exit` to the parent shell.
8. Run strict execution inside an isolated child shell or subshell.
9. Capture stdout+stderr to a timestamped `/tmp` receipt through `tee`.
10. Finish Owner delivery with `scripts/airo-clipboard-receipt`; verified clipboard readback and content-hash match are mandatory.
11. Owner-facing commands must be chat-formatting-safe; literal nested Markdown fences inside an outer command fence are forbidden.
12. Every meaningful execution starts or continues `bin/airo-session`, records semantic terminal outcomes, and closes with a structured worklog at an objective or explicit pause boundary.
13. Session closeout writes permanent `worklog/sessions/...` and regenerates `worklog/daily/...` for Obsidian continuity.
14. Git push is never implied. Bundle it only with explicit Owner authorization, verified remote parity, exact-path staging, public-safety checks, and never force push.
15. Never reset, stash, rebase, clean, overwrite, or stage unrelated Owner work.
16. Script success is not task success; completion remains evidence-driven.
17. Acceptance evidence follows `AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`; direct WSL should automate backend acceptance when it can prove the required behavior without Owner manual review.


## Mandatory Operational Execution Continuity (KCC v1)

Every meaningful AIRO execution MUST automatically record semantic operational state:

1. **Resolve/Start/Continue Session**: Before execution, verify active session context (`bin/airo-session start`).
2. **Semantic PRE-EXECUTION Checkpoint**: Record action intent, active owner request, current position, and next action (`scripts/airo-capture --phase PRE_EXECUTION ...`).
3. **Bounded Execution**: Execute approved task.
4. **Semantic POST-EXECUTION Checkpoint**: Record factual outcome, evidence pointer, updated position, and next action (`scripts/airo-capture --phase POST_EXECUTION ...`).
5. **Live Obsidian Artifact**: Automatically refreshed at `worklog/sessions/<date>/<project>/SESSION_<id>.md` during the running session.

> **CRITICAL RULE**: `RAW COMMAND != KNOWLEDGE RECORD`. Do NOT store raw terminal command strings or raw prompt dumps as knowledge records. Record the semantic state around the execution.
