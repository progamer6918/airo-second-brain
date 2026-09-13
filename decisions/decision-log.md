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
