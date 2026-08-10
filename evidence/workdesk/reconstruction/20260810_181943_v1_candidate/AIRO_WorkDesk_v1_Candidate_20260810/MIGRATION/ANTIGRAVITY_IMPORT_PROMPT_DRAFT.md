# Antigravity Import Prompt - DRAFT ONLY

**Do not run until candidate validation and Owner import approval.**

TUJUAN=Import the approved public-safe AIRO WorkDesk v1 candidate into canonical ASB using the exact approved import manifest.
EXPECTED=Session guard PASS; refreshed repo SoT; candidate/hash verification; public-safety PASS; exact-path diff; tests PASS; task verdict; commit/push/remote parity.
MUTATION=DOCS_AND_WORKDESK_EVIDENCE_ONLY_EXACT_MANIFEST_PATHS
STOP_IF=Session switch required; repo divergence; unexpected dirty Owner files overlap targets; hash mismatch; private-sidecar path appears in public import; secret/PII hit; broken links; task verdict blocks advancement.

## Mandatory Session Workflow Guard

Before any mutation run:

`python3 bin/airo-session start --project-id AIRO_WORKDESK --project-name "AIRO WorkDesk" --objective "Full Corpus Semantic Reconstruction" --title "WorkDesk v1 Surgical Migration" --position "V1_CANDIDATE_MIGRATION"`

- same project + objective → continue existing;
- no active session → started;
- different project/objective → `SESSION_SWITCH_REQUIRES_CLOSE=YES` and STOP.

After every meaningful verified result/state change run `python3 bin/airo-session event ...` with distilled safe evidence. Event coverage must include blocker/error paths.

## Semantic boundary

`SEMANTIC_AUTHORING_ALLOWED=NO`
`CONTENT_REWRITING_ALLOWED=NO`
`INFERENCE_ALLOWED=NO`

Antigravity is a deterministic importer/validator only. ChatGPT-authored candidate content may be imported only according to the approved manifest and reconciliation decisions.

## Git safety

- fetch and prove expected remote/branch identity;
- exact-path staging only;
- never `git add .` or `git add -A`;
- no force push, reset, stash, clean, pull/rebase automation;
- stop on divergence;
- prove remote commit/tree parity after push.

## Completion

Script success is not task success. Use canonical `scripts/airo-task-verdict` from explicit JSON evidence. Do not claim WorkDesk semantic completion merely because import succeeds.
