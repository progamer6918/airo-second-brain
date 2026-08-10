# Canonical ASB Migration Plan - Candidate

## Rule zero

Do **not** delete and replace `wiki/workdesk/` wholesale. Existing WorkDesk is the chassis; v1 reconstruction replaces/enriches semantic depth and adds private-memory interfaces.

## Phase A - Read-only reconciliation

Before repo mutation:

1. refresh canonical ASB;
2. start/continue the canonical AIRO WorkDesk session using `bin/airo-session`;
3. inventory current `wiki/workdesk/`, WorkDesk evidence, tests, and current status;
4. compare every candidate public file with its canonical target;
5. classify each target: `KEEP | REFINE | MERGE | REPLACE_BODY | CREATE | SUPERSEDE | NO_IMPORT`;
6. secret/PII scan candidate;
7. verify no private-sidecar file has a public target.

## Phase B - Candidate validation

Required before mutation:

- source/provenance checks;
- internal link check;
- stale-currentness check;
- public/private boundary check;
- explicit-source vs inference check;
- fresh-AI knowledge + applied + adversarial tests;
- truthful status flags.

## Phase C - Surgical public import

- Human cockpit: keep/refine existing `HOME.md`, do not regress user-first UX.
- Add response-plane/currentness/private-sidecar contracts.
- Merge reconstructed human knowledge into existing domain/playbook/deliverable locations.
- Do not expose private operational values or PII.
- Preserve historical evidence; mark invalid/stale reconstruction artifacts as superseded, not authoritative.
- Update `CURRENT.md` only after measured migration state is known.

## Phase D - Deterministic deployment

Antigravity acts as repo operator only:

- semantic rewriting: forbidden;
- inference: forbidden;
- exact candidate-to-target mapping only;
- exact-path staging only;
- no `git add .` / `git add -A`;
- no force push/rebase/reset/stash/clean;
- stop on divergence/dirty-owner conflicts;
- validate remote commit/tree parity after push.

## Private sidecar

`PRIVATE_SIDECAR_CANDIDATE/` has **no public ASB import path**. It is a local/private knowledge layer. Public ASB may contain only safe contracts/pointers describing how such data is used.
