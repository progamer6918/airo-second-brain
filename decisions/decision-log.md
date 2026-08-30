last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Decision Log

Final decisions only. Do not write uncertain items here.

Pending or unresolved decisions belong in decisions/pending-decisions.md.

2026-06-10 — AIRO Brand Scope

Decision:

AIRO is the umbrella ecosystem brand.
AIRO Finance is one project inside the wider AIRO ecosystem.

Evidence:

Owner confirmed explicitly.

Superseded by:

—
2026-06-10 — Second Brain Architecture

Decision:

AIRO Second Brain will be the shared canonical knowledge base / AIRO Kernel.
It should support multiple consumers: ChatGPT, Claude, Hermes, Antigravity, OpenClaw, and local agents.
It should use a router-based structure, not a single giant file.

Evidence:

Owner approved the shared-brain direction.

Superseded by:

—
2026-06-10 — Raw Chat Policy

Decision:

Raw chat history is relevant as source material.
Raw chat should not be stored as default canonical context.
Important chats should be distilled into decisions, worklogs, lessons, and project summaries.

Evidence:

Owner asked to preserve cross-consumer context without bloating the default brain.

Superseded by:

—
2026-06-10 — Cross-Consumer Operator Model

Decision:

All AIRO consumers are interface-specific operators of the same AIRO ecosystem.
They should not behave as separate independent assistants.
Each consumer should load AIRO Second Brain at session start and produce closeout at session end.

Evidence:

Owner wants interaction to feel like one consistent assistant across tools.

Superseded by:

—
2026-06-10 — Auto-Write / Auto-Commit Policy

Decision:

Inbox/state/changelog append-only updates may be automated when configured.
Canonical files require owner approval.
Auto-commit is allowed only for configured local consumers with git access and only for non-canonical append-only updates.

Evidence:

Owner wants less manual logging but still needs safe canonical control.

Superseded by:

—

### 2026-08-15 — Formalization of Direct Apps Script Transport (AIRO_EAB_DIRECT_V1)
- **Decision:** Formalize `AIRO_EAB_DIRECT_V1` direct Apps Script transport as canonical EAB transport architecture.
- **Context:** HMAC-SHA256 signature is passed inside the payload JSON body (`key_id`, `timestamp`, `nonce`, `signature`).
- **Authority:** EAB Master Bundle 2026-08-15 R1 P1 Governance Recovery.
- **Status:** APPROVED.

### 2026-08-16 — EAB P8 Direct-Arfin Fallback Deferral & M13 Limited Owner Acceptance
- **Decision:** Stop further technical debugging of P8 inside EAB. Defer the Direct-Arfin multi-pending bare-selector defect to AIRO Finance as a separate incident (`AFPD-INC-012`). Remove/defer P8 as a blocking EAB Phase-1 requirement via explicit Owner scope waiver. Accept EAB M13 with recorded residual limitation (`APPROVED_WITH_RECORDED_LIMITATION`).
- **Semantics:**
  - `EAB_P8_SCOPE_DECISION`: `DEFERRED_BY_OWNER`
  - `P8_ACCEPTANCE_RESULT`: `FAIL_NOT_WAIVED_AS_PASS`
  - `P8_BLOCKING_REQUIREMENT_FOR_EAB_PHASE1`: `WAIVED_BY_OWNER`
  - `P8_DEFECT_OWNERSHIP`: `AIRO_FINANCE`
  - `P8_FUTURE_REPAIR`: `SEPARATE_DEFECT_WORK`
  - `EAB_CORE_LIVE_PATH_ACCEPTED`: `YES`
  - `P8_STATUS`: `DEFERRED_OPEN_DEFECT`
  - `P8_LIVE_ACCEPTANCE`: `FAIL`
  - `P8_BLOCKS_EAB_M13`: `NO_BY_EXPLICIT_OWNER_WAIVER`
  - `M13_STATUS`: `DONE`
  - `M13_OWNER_ACCEPTANCE`: `APPROVED_WITH_RECORDED_LIMITATION`
  - `M13_OWNER_SCOPE_WAIVER`: `P8_DIRECT_ARFIN_FALLBACK_DEFERRED`
  - `M13_PRIMARY_FLOW_COMPLETED`: `YES`
  - `M14_STATUS`: `NOT_STARTED`
  - `M14_AUTHORIZED`: `NO`
- **Residual Limitation:** Direct-Arfin multi-pending fallback using bare transaction-number selection is not accepted and must not be relied upon until the separate AIRO Finance defect is resolved.
- **Authority:** EAB Completion Master Bundle 2026-08-16 R5 Owner Decision.
- **Status:** APPROVED.

### 2026-08-16 — EAB M14 Stage 4 Production Activation & 24h Observation Window Entry
- **Decision:** Enter M14 Stage 4 Production Activation using post-M13-waiver canonical state. Live topology is active and verified (`PRODUCTION_ACTIVATION_CHANGE_REQUIRED=NO`). Start mandatory 24h post-activation observation window.
- **Semantics:**
  - `M14_AUTHORIZED`: `YES`
  - `M14_STAGE4_STATUS`: `DONE`
  - `M14_STAGE5_STATUS`: `IN_PROGRESS`
  - `M14_STATUS`: `IN_PROGRESS_24H_OBSERVATION`
  - `PRODUCTION_ACTIVATION_STATUS`: `ACTIVE_VERIFIED`
  - `OBSERVATION_START`: `2026-08-16 09:56:47 +07:00`
  - `OBSERVATION_REQUIRED_HOURS`: `24`
  - `OBSERVATION_NOT_BEFORE_END`: `2026-08-17 09:56:47 +07:00`
  - `P8_STATUS`: `DEFERRED_OPEN_DEFECT`
- **Authority:** EAB Completion Master Bundle 2026-08-16 R5 M14 Stage 4.
- **Status:** APPROVED.

### 2026-08-16 — EAB Final Project Freeze, Retrospective & Session Closeout
- **Decision:** Freeze and permanently close EAB Phase-1 project with recorded limitations (`CLOSED_WITH_RECORDED_LIMITATIONS`). Retain operational core bridge (`EAB_CORE_PRIMARY_PATH_STATUS=OPERATIONAL_ACCEPTED`). Waive 24h Stage-5 observation without claiming 24h stability PASS. Retain P8 multi-pending bare selector defect as an open incident under AIRO Finance (`AFPD-INC-012`). Persist retrospective and error history index.
- **Semantics:**
  - `PROJECT_STATUS`: `CLOSED_WITH_RECORDED_LIMITATIONS`
  - `PROJECT_DEVELOPMENT_FROZEN`: `YES`
  - `M14_STAGE4_STATUS`: `DONE`
  - `M14_STAGE5_STATUS`: `WAIVED_BY_OWNER_BEFORE_24H_COMPLETION`
  - `M14_24H_ZERO_OUTAGE_CLAIM`: `NOT_MADE`
  - `M14_STATUS`: `DONE_WITH_RECORDED_LIMITATION`
  - `P8_STATUS`: `DEFERRED_OPEN_DEFECT`
- **Authority:** EAB Master Bundle 2026-08-16 R5 Final Closeout Decision.
- **Status:** APPROVED.

### 2026-08-16 — EAB Post-Close Product Outcome Correction
- **Decision:** Correct EAB project classification to `CLOSED_INCOMPLETE_PARTIAL_IMPLEMENTATION` after post-close live test proved manual transaction creation via Earesmes is not operational (`EAB_MVP_PRODUCT_OUTCOME=NOT_ACHIEVED`). `LIST_PENDING` read path remains operational (`EAB_LIST_PENDING_READ_PATH=OPERATIONAL_PROVEN`). Project remains frozen/closed.
- **Semantics:**
  - `EAB_PROJECT_LIFECYCLE_STATUS`: `CLOSED`
  - `EAB_FINAL_CLASSIFICATION`: `CLOSED_INCOMPLETE_PARTIAL_IMPLEMENTATION`
  - `EAB_MVP_PRODUCT_OUTCOME`: `NOT_ACHIEVED`
  - `EAB_LIST_PENDING_READ_PATH`: `OPERATIONAL_PROVEN`
  - `EAB_MANUAL_CREATE_VIA_EARESMES`: `NOT_OPERATIONAL`
  - `PROJECT_DEVELOPMENT_FROZEN`: `YES`
  - `NEXT_EAB_ACTION`: `NONE`
- **Authority:** EAB Master Bundle 2026-08-16 R5 Correction Decision.
- **Status:** APPROVED.


### DEC-20260825-01: Semantic State as Primary Knowledge Record
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Raw chat/command/prompt is not the primary AIRO knowledge record; semantic state (owner request, position, progress, blocker, next action) is.

### DEC-20260825-02: Fresh-AI Contextual Readiness Retrieval Target
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Fresh-AI target is contextual readiness via canonical BOOT/retrieval order, not brute-force consumption of 100% ASB.

### DEC-20260825-03: Operational Capture vs Knowledge Promotion Separation
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Operational capture is automatic/lightweight at every meaningful executor boundary; knowledge promotion to DECISION/PRD is selective.

### DEC-20260825-04: Manual Session Capture Command as Failsafe Override
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: 'catat sesi ini ke ASB' is a manual override/failsafe, not the primary operational capture mechanism.

### DEC-20260825-05: Live Obsidian Session Visibility Prior to Close
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Running session state and Owner Request must be human-readable in Obsidian before session close via live markdown rendering.

### DEC-20260825-06: Bidirectional Decision Lifecycle Supersession
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Historical decision retrieval must inspect ACTIVE/SUPERSEDED status and use bidirectional supersession (DEC-YYYYMMDD-NN).

### DEC-20260825-07: Scoped Retrieval Claims for Negative Findings
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Negative historical retrieval claims must state actual search scope rather than unsupported 'tidak pernah dibahas'.

### DEC-20260825-08: V1 Remote Persistence Policy
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: Operational capture local=AUTO; GitHub auto-push per execution=NO; remote durability uses checkpoint/session Git flow.

### DEC-20260825-09: Verified Clipboard Receipt Transport Contract
- **Date**: 2026-08-25
- **Status**: `ACTIVE`
- **Summary**: AIRO executor evidence transport uses final receipt + clipboard readback/hash, not raw terminal output as proof of successful handoff.


### DEC-20260830-01: Windows Obsidian Hard Requirement for ASB Architecture
- **Date**: 2026-08-30
- **Status**: `ACTIVE`
- **Context**: Closed session visibility defect revealed a dual-vault split-brain between canonical WSL ASB and stale Windows clone. Direct Windows Obsidian to WSL UNC access was tested and failed real UI acceptance.
- **Decision**: Any future ASB physical-layout or projection architecture must retain native Windows Obsidian as the Owner-facing application.
- **Rejected Approaches**:
  - Replacing Windows Obsidian with Linux/WSLg Obsidian (`OBSIDIAN_LINUX_WSLG=REJECTED_BY_OWNER`).
  - Retrying direct WSL UNC vault access without new explicit evidence (`DIRECT_WINDOWS_OBSIDIAN_TO_WSL_UNC=REJECTED_FOR_CURRENT_ENVIRONMENT`).
  - Silently treating stale Windows clone as canonical (`STALE_WINDOWS_ASB_AUTHORITY=NON_CANONICAL`).
- **Open Architecture Candidates for Council Feasibility**:
  - **Option A**: One physical ASB tree accessible natively to Windows Obsidian and safely to WSL/AIRO (e.g. Windows-native canonical ASB accessed via `/mnt/c/`).
  - **Option B**: Canonical WSL ASB plus deterministic Windows Obsidian projection where the projection is explicitly non-authoritative.
- **Next Question**: Given Windows Obsidian is mandatory and direct WSL UNC vault access is rejected, what is the lowest-risk architecture that preserves one authoritative ASB truth while keeping AIRO/Hermes/Antigravity reliable?



### DEC-20260830-02: A2-WG Selected ASB Architecture Candidate & Reconciliation Gate
- **Date**: 2026-08-30
- **Status**: `ACTIVE`
- **Decision**: Option A2-WG (Windows-native physical ASB repository + Windows native Git interop shim) is selected as the ASB architecture candidate.
- **Architectural Rationale**:
  - Windows Obsidian UX is a locked Owner requirement.
  - Direct Windows Obsidian to WSL UNC access failed real UI acceptance.
  - Bidirectional mirror sync creates unacceptable split-brain risk.
  - Linux Git over 9p DrvFS incurs prohibitive ~3.0s status latency.
  - Windows native Git interop reduces status latency to ~106ms with 100% path and safety compatibility.
  - Scoped `git` shim covers 100% of AIRO callers without per-file edits.
- **Reconciliation Status**: Candidate generated (AMBIGUOUS_OWNER_CONFLICTS_FOUND). Live migration remains blocked until formal migration gate approval.



### DEC-20260830-04: Mandatory Rollback of A2-WG Production Activation
- **Date**: 2026-08-30
- **Status**: `ACTIVE`
- **Decision**: A2-WG production cutover rolled back due to runtime acceptance failure (`HERMES_ACTIVE=NO`).
- **Restoration**: Canonical physical WSL ASB and Windows clone restored to exact pre-cutover state.
- **Evidence**: Failed A2-WG tree retained at `C:\Users\Admin\AI_WORKSPACES\airo-second-brain.failed-a2wg-20260830_090632` for diagnostic reference.
- **Next Step**: Return to AIRO Sync / Architecture Council.



### DEC-20260830-05: A2-WG Production Attempt #2 Active and Accepted (Baseline-Aware)
- **Date**: 2026-08-30
- **Status**: `ACTIVE`
- **Architecture**: `A2_WG` (Windows Physical ASB + Windows Native Git Interop)
- **Active Physical Repository**: `C:\Users\Admin\AI_WORKSPACES\airo-second-brain`
- **WSL Logical Path**: `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain` (symlink)
- **WSL Physical Realpath**: `/mnt/c/Users/Admin/AI_WORKSPACES/airo-second-brain`
- **Git Backend**: `~/.local/bin/git` scoped shim delegating ASB operations to `C:\Program Files\Git\cmd\git.exe` (~106ms status latency).
- **Runtime Acceptance Policy**: `PRESERVE_PRE_CUTOVER_RUNTIME_STATE` (Hermes baseline preserved).
- **Owner Content Preservation**: 159/159 Owner deltas preserved from Windows clone.
- **Rollback Authority**: Attempt #1 failed candidate (`C:\Users\Admin\AI_WORKSPACES\airo-second-brain.failed-a2wg-20260830_090632`), Attempt #2 WSL backup (`/home/egitaristorandas/AI_WORKSPACES/airo-second-brain.pre-a2wg-attempt2-20260830_091926`), and Attempt #2 Windows backup (`C:\Users\Admin\AI_WORKSPACES\airo-second-brain.pre-a2wg-attempt2-windows-20260830_091926`) retained for rollback only.



### DEC-20260830-06: EAB Repair Chain Closure & Transition to Earesmes Capability Router
- **Date**: 2026-08-30
- **Status**: `ACTIVE`
- **Decision**: Close current EAB patch/repair chain. Next architecture project is `EARESMES_CAPABILITY_ROUTER_FOUNDATION`.
- **Rationale**: Live vNext acceptance failure occurred in Earesmes/Hermes dispatch and session state precedence before Arfin specialist invocation (`ARFIN_SPECIALIST_CALL_OBSERVED=NO`). Arfin specialist architecture is not proven invalid.
- **Reference**: `ecosystem/projects/earesmes-arfin-bridge/docs/EAB_POST_VNEXT_ORCHESTRATION_BOUNDARY_DECISION_20260830.md`



## DEC-20260830-07: KCC Human-First Session Memory V2 & Owner-Facing Note Architecture
- **Date**: 2026-08-30
- **Context**: Previous permanent session notes in Obsidian suffered from technical overload, repetitive generic placeholders ("Permintaan Owner belum tercatat secara semantik", "Pekerjaan sesi telah selesai dieksekusi dan diverifikasi"), and failed to serve the non-technical Owner as the primary audience.
- **Decision**:
  1. **Primary Audience**: The visible permanent session note is for the Owner (plain Indonesian, concise, non-engineer friendly).
  2. **Two-Layer Architecture**:
     - **Layer 1 (Owner Visible)**: `# Title`, `## Ringkasnya`, `## Yang lo minta`, `## Yang dikerjakan`, `## Hasil`, `## Batasan / yang belum selesai`, `## Berikutnya`.
     - **Layer 2 (Machine Context)**: Preserved in a hidden HTML comment block (`<!-- AIRO_MACHINE_CONTEXT_BEGIN ... AIRO_MACHINE_CONTEXT_END -->`) with full JSON structured metadata for AI reading.
  3. **Strict Validation**: Closeout validation rejects any note containing prohibited generic placeholders.
  4. **Semantic Request Capture**: Mandatory capture (`EXPLICIT` or `INFERRED_FROM_TASK_CONTEXT`) for all Owner-initiated sessions.
- **Status**: APPROVED & ACTIVE

