# EAB Project Execution Roadmap

PROJECT=EARESMES_ARFIN_CLARIFICATION_BRIDGE
ROADMAP_STATUS=CANONICAL
OWNER_APPROVAL_SOURCE=OWNER_INSTRUCTION_2026_07_29
MVP_SCOPE=PRODUCT_PHASE_1
PHASE_2_SCOPE=DEFERRED_OPTIONAL
IMPLEMENTATION_STATE=COMPLETE
IMPLEMENTATION_ALLOWED=YES
CURRENT_MILESTONE=M14
CURRENT_GATE=EAB_G2_7
PHASE1_MVP_STATUS=COMPLETE

PRE_EXISTING_CANONICAL_GATES=EAB_G1_0,EAB_G1_1,EAB_G1_2,EAB_G1_3,EAB_G1_4,EAB_G1_6
G1_5_STATUS=INTENTIONALLY_NOT_USED
NEW_OWNER_APPROVED_DELIVERY_GATES=EAB_G2_0,EAB_G2_1,EAB_G2_2,EAB_G2_3,EAB_G2_4,EAB_G2_5,EAB_G2_6,EAB_G2_7

TOTAL_REQUIREMENT_COUNT=14
MVP_REQUIRED_REQUIREMENT_COUNT=13
OPTIONAL_DEFERRED_REQUIREMENT_COUNT=1
REQ_014_REQUIRED_FOR_MVP=NO

---

## Roadmap Scope & Gate Lineage

1. **Gate Lineage**:
   - `EAB_G1_0` through `EAB_G1_6` are pre-existing canonical design and readiness gates. Gate `EAB_G1_5` is intentionally omitted.
   - `EAB_G2_0` through `EAB_G2_7` are new delivery and verification gates canonicalized by this Owner-approved roadmap.
   - No ad hoc or unapproved AI gates may be inserted into this execution sequence.

2. **Phase 1 MVP vs Phase 2 Deferred**:
   - Phase 1 MVP encompasses Milestones M0 through M14 and requirements REQ-001 through REQ-013 (13 MVP-required requirements).
   - Phase 2 (M15 / REQ-014: Cloud Inbox & Free-Form Comma Batch Parsing) is optional and deferred. REQ-014 does NOT block Phase 1 MVP completion.

---

## Milestone Execution Sequence (M0 – M15)

### M0 — Product Scope and Canonical Documentation
- **Gate**: `EAB_G0_1` through `EAB_G0_5DI`
- **Status**: `DONE`
- **Deliverables**: PRD, Architecture, Contracts, Acceptance Specification, Scope Lock, Traceability, Regression Guards, Canonical Closeout.
- **Exit Criteria**: Canonical documentation integrated into remote `main`; Owner ratification recorded.
- **Evidence**: Commits `626e1b0525f01c9580025903e776f068f01d72ae` and `a357ebbe774cce3c115e0867b73e26d057ae50bd`.

### M1 — Runtime and Workspace Readiness
- **Gate**: `EAB_G1_0`
- **Status**: `DONE`
- **Deliverables**: Dedicated clean implementation workspace strategy, local process ownership evidence, local getUpdates single-owner evidence, queue isolation evidence.
- **Final Closure Evidence**: M12 signed live canary PASS; bounded owner_chat_id enforcement and production route isolation verified; `AFPD-INC-011` RESOLVED.
- **Transition Result**: M1 transitioned to `DONE` at M12 and remains `DONE` at M14 Phase 1 closeout.
### M2 — Stable Pending Identity and Concurrency Contract
- **Gate**: `EAB_G1_1`
- **Status**: `DONE`
- **Evidence**: `ecosystem/projects/earesmes-arfin-bridge/docs/design/g1_1/`
- **Deliverables**: Canonical `pending_id` schema and lifecycle, collision-safe `short_ref` contract (`AF-XXXX`), `pending_version` monotonic contract, stale-reply fail-closed contract, migration/backfill strategy, unit-test vectors, exact candidate source paths.
- **Exit Criteria**: PREREQ-003 and PREREQ-004 design evidence `PASS`. Zero source code mutation.
- **Next Exact Action**: Produce one consolidated G1.1 implementation-design package.

### M3 — Bounded Adapter and Authentication Contract
- **Gate**: `EAB_G1_2`
- **Status**: `DONE`
- **Evidence**: `ecosystem/projects/earesmes-arfin-bridge/docs/design/g1_2/`
- **Deliverables**: 4 bounded API methods (`eabGetPending`, `eabListPending`, `eabSubmitBatchClarification`, `eabCreateManualTransaction`), `owner_chat_id` allowlist specification, caller authentication, least-privilege capability boundary, prohibited-method proof, error schemas.
- **Exit Criteria**: PREREQ-005 and PREREQ-006 design evidence `PASS`.

### M4 — Review Queue, Fallback, Batch, Expiry and Idempotency Contract
- **Gate**: `EAB_G1_3`
- **Status**: `DONE`
- **Evidence**: `ecosystem/projects/earesmes-arfin-bridge/docs/design/g1_3/`
- **Deliverables**: Itemized per-line batch behavior, partial success handling, pre-submission revalidation, direct-Arfin fallback route, idempotency, 24-hour TTL and unresolved backlog retention, manual catat parser spec.
- **Exit Criteria**: PREREQ-007 and PREREQ-008 design evidence `PASS`.

### M5 — Rollback, Observability, Attribution and Consolidated Readiness
- **Gate**: `EAB_G1_4`
- **Status**: `DONE`
- **Deliverables**: Rollback topology, source/runtime/deployment attribution, trace IDs and safe logging, exact implementation source paths, implementation slices, test map, canary/rollback plan.
- **Exit Criteria**: PREREQ-009 and PREREQ-010 `PASS`. All design packages internally consistent.

### M6 — Owner Implementation Authorization
- **Gate**: `EAB_G1_6`
- **Status**: `DONE`
- **Deliverables**: Exact remote baseline hash, exact source and test paths, exact mutation scope, exact commit/deployment scope, exact rollback boundary, explicit Owner authorization receipt.
- **Exit Criteria**: PREREQ-011 `PASS`. Source code implementation explicitly authorized by Owner.

### M7 — Arfin Pending Model Implementation
- **Gate**: `EAB_G2_0`
- **Status**: `DONE`
- **Deliverables**: Stable `pending_id`, `short_ref`, `pending_version`, state lifecycle, TTL and backlog management, safe migration/backfill scripts.
- **Exit Criteria**: Pending model unit tests `PASS`. Stale write creates zero Review Queue effect.

### M8 — Bounded Arfin Adapter Implementation
- **Gate**: `EAB_G2_1`
- **Status**: `DONE`
- **Deliverables**: Implementation of 4 bounded methods, `owner_chat_id` enforcement, least-privilege capability boundary.
- **Exit Criteria**: Unauthorized callers rejected. Direct ledger and approval methods absent. Review Queue staging only.

### M9 — Earesmes and Hermes Bridge Implementation
- **Gate**: `EAB_G2_2`
- **Status**: `DONE`
- **Deliverables**: Pending list renderer, short reference resolver, natural-language clarification parser, multiline batch parser, manual catat parser, pre-submission revalidation client, itemized receipts.
- **Exit Criteria**: Earesmes Gateway remains sole getUpdates owner. Hermes worker remains bounded queue consumer.

### M10 — Automated Verification
- **Gate**: `EAB_G2_3`
- **Status**: `DONE`
- **Deliverables**: Static/syntax tests, contract tests, parser tests, concurrency tests, allowlist/security tests, idempotency tests, expiry tests, direct-ledger denial tests.
- **Exit Criteria**: All 13 MVP-required requirements REQ-001 through REQ-013 have automated test evidence (`PASS`). Zero critical regression failures.

### M11 — Controlled Integration Dry Run
- **Gate**: `EAB_G2_4`
- **Status**: `DONE`
- **Deliverables**: Synthetic pending flow, synthetic stale flow, synthetic batch partial success, synthetic unauthorized caller, synthetic manual catat, Review Queue-only effect verification.
- **Exit Criteria**: Integration test suite `PASS`. Account Ledger receives zero pre-approval writes. Rollback rehearsal `PASS`.

### M12 — Fresh Live Canary
- **Gate**: `EAB_G2_5`
- **Status**: `DONE`
- **Deliverables**: Live pending clarification, stale/replay rejection, manual catat, batch partial success, unauthorized message rejection, direct-Arfin fallback check.
- **Exit Criteria**: Live canary test suite `PASS`. Review Queue mandatory. Zero direct Account Ledger write. `AFPD-INC-011` close condition directly verified. M1 transitions to `DONE`.

### M13 — Owner Acceptance
- **Gate**: `EAB_G2_6`
- **Status**: `DONE`
- **Deliverables**: Owner tests primary Earesmes flow, direct Arfin fallback, Review Queue approval, and final ledger effect.
- **Exit Criteria**: Explicit Owner acceptance receipt signed.

### M14 — Production Activation and Project Closeout
- **Gate**: `EAB_G2_7`
- **Status**: `DONE`
- **Deliverables**: Production source/runtime/deployment attribution, health monitoring, rollback target, canonical progress and handoff closeout.
- **Exit Criteria**: All required milestones M0–M14 `DONE`. M1 transitioned to `DONE`. All 13 MVP-required requirements REQ-001 through REQ-013 `PASS`. Live canary `PASS`. Owner acceptance `PASS`.

### M15 — Optional Product Phase 2 (Deferred)
- **Gate**: `EAB_PHASE_2`
- **Status**: `DEFERRED`
- **Required for MVP**: `NO`
- **Deliverables**: Cloud inbox integration, free-form comma-separated batch parsing (REQ-014).

---

## EAB Definition of Done (DoD)

EAB Phase 1 MVP is complete ONLY when:
1. Milestones M0 through M14 are all `DONE` (including M1 transition to `DONE` at M12).
2. All 13 MVP-required product requirements (REQ-001 through REQ-013) have direct implementation and test evidence (`PASS`).
3. REQ-014 belongs to optional deferred Product Phase 2 and does NOT block EAB Phase 1 MVP completion.
4. Source code implementation is complete and verified.
5. Automated verification test suite passes 100% for REQ-001 through REQ-013.
6. Controlled integration dry run passes.
7. Fresh live canary passes.
8. Owner acceptance passes.
9. Direct Arfin fallback path passes.
10. All valid transactions flow strictly through Review Queue.
11. Earesmes has zero direct Account Ledger write capability.
12. Rollback proof passes.
13. Production attribution and canonical closeout are complete.

> *Documentation completion alone is NOT project completion.*
