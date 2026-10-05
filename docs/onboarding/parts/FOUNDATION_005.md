                           │ [TUJUAN / EXPECTED / MUTATION]
                           ▼
┌────────────────────────────────────────────────────────┐
│             Antigravity (Executor Only Layer)           │
│  - Executes bounded plan via terminal automation       │
│  - Bundles safe WSL sub-steps & collects logs          │
└──────────────────────────┬─────────────────────────────┘
                           │ [WSL Commands & Shell Scripts]
                           ▼
┌────────────────────────────────────────────────────────┐
│               WSL (Runtime Execution Layer)            │
│  - Executes binaries, python scripts, & git ops        │
│  - Captures stdout+stderr to /tmp log files            │
└──────────────────────────┬─────────────────────────────┘
                           │ [tee + airo-clipboard-receipt]
                           ▼
┌────────────────────────────────────────────────────────┐
│            Verified Status & Evidence Receipt          │
│  - 🧭 AIRO STATUS Header                                │
│  - Verified Clipboard Receipt (CLIPBOARD_READBACK=PASS)│
└────────────────────────────────────────────────────────┘
```

---

## 4. Compliance & Verification

All AIRO execution sessions and prompts MUST adhere to this contract. Any violation (such as Antigravity altering architecture without planning approval, or ChatGPT attempting direct terminal mutation) constitutes a governance breach and invalidates the session verdict.

## Codex — Owner-authorized planning and execution

Codex preserves its own consumer identity. It may plan, review and execute tasks within explicit Owner authorization. Execution must satisfy applicable ASB session continuity, evidence, remote target identity, git and delivery safeguards. AGY-specific gateway requirements apply only where their applicability conditions are met. Reading ASB does not grant automatic canonical semantic promotion or public publication authority.

Authority: explicit Owner decision in the onboarding discussion, 2026-10-05 (UTC+7). Claude execution scope is not changed by this addition.

<!-- SOURCE_END docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_CONTRACT.md -->

# Source: docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_CONTRACT.md

---
type: contract
project: GLOBAL
status: CANONICAL
authority: OWNER_APPROVED
date: 2026-09-05
audience: all_airo_operators_and_ai_consumers
---

# 📜 AIRO Knowledge Continuity Contract (KCC)

**Contract ID:** `AIRO_CONTRACT_KNOWLEDGE_CONTINUITY_V1`  
**Effective Date:** 2026-09-05  
**Canonical Path:** `docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_CONTRACT.md`  
**Parent Architecture Record:** `docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md`  
**Parent Governance Contracts:**  
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`  
- `docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md`  
- `docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`  
- `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`  
- `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`  

---

## 1. Purpose & The "Fresh AI" Problem

### 1.1 The Fresh AI Dilemma
In an ecosystem powered by large language models, AI execution agents (ChatGPT, Claude, Antigravity, OpenClaw, Earesmes/Hermes, WSL scripts) operate statelessly. Every new chat thread, session timeout, or context truncation produces a **"Fresh AI"** with zero conversational memory of prior sessions.

Without a rigorous, deterministic Knowledge Continuity Contract:
1. **Context Fragmentation**: Fresh AIs hallucinate prior decisions, re-ask resolved questions, and reinvent architectures.
2. **Knowledge Drift**: Ephemeral chat summaries corrupt canonical system truth.
3. **Continuity Corruption**: Worklogs and milestone advancements lose chronological provenance.

### 1.2 Purpose of KCC
The Knowledge Continuity Contract establishes the canonical rules for how institutional knowledge, architectural truth, and active work context are organized, ingested, promoted, and consumed so that **any Fresh AI can instantly onboard and execute with 100% operational fidelity and zero memory loss.**

---

## 2. Knowledge Hierarchy & Layer Model

The AIRO Second Brain (ASB) organizes all knowledge into six strict hierarchical layers:

```text
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 1: RUNTIME & EXECUTION STATE (Machine Truth)              │
│  - ~/.local/state/airo/second-brain/.../active_session.json      │
│  - events/raw/events.ndjson, live Git HEAD, OS processes         │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 2: CANONICAL GOVERNANCE & CONTRACTS (Authority Truth)     │
│  - docs/contracts/, docs/governance/, decisions/                 │
│  - Explicit Owner rules, architectural decision records (ADRs)   │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 3: CANONICAL PROJECT & DOMAIN KNOWLEDGE (Core Truth)      │
│  - control/, projects/, docs/specs/, docs/prd/, docs/roadmap/    │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 4: SESSION WORKLOGS & HANDOFFS (Chronological Memory)     │
│  - worklog/sessions/, worklog/daily/, docs/continuity/           │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 5: PRESENTATION & OPERATIONAL COCKPITS (Derived Views)    │
│  - wiki/workdesk/HOME.md, state/active-session.md, current-work  │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 6: STAGING & INTAKE (Ephemeral / Pending Approval)        │
│  - inbox/, inbox/session-closeouts/, /tmp/ receipt logs          │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Fact Authority vs Decision Authority

To prevent hallucinated status and ungrounded policy mutations, ASB strictly bifurcates authority into two distinct categories:

```text
┌──────────────────────────────────────────────────────────────────┐
│                      FACT AUTHORITY (Empirical)                  │
│  - Ground Truth: Live runtime evidence, exit codes, git HEAD     │
│  - Rule: Machine facts CANNOT be decided or negotiated by chat.  │
│  - Invariant: A feature is NOT done until proven by evidence.    │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ Governed by
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DECISION AUTHORITY (Normative)                │
│  - Ground Truth: Owner approvals, ADRs, canonical contracts      │
│  - Rule: Policy and scope CANNOT be assumed by machine or model. │
│  - Invariant: Runtime code cannot redefine ecosystem governance. │
└──────────────────────────────────────────────────────────────────┘
```

1. **Fact Authority**:
   - Represents empirical reality: test outcomes, verified receipts, clipboard content hashes, file mtimes, process states.
   - **Boundary**: No agent or chat summary can declare a task complete (`BERHASIL`) or milestone advanced (`CAN_ADVANCE=YES`) without verified backend/runtime evidence.
2. **Decision Authority**:
   - Represents intent, governance, and architecture: Owner approvals, Council deliberations, milestone scopes, and contract rules.
   - **Boundary**: No executor script or autonomous agent can alter project objectives, waive security constraints, or adopt new architectural patterns without explicit Owner authorization.

---

## 4. Knowledge Conflict Resolution Protocol

When a Fresh AI encounters conflicting information across documents, chat summaries, or runtime states, it MUST execute this deterministic 4-step protocol:

```text
┌────────────────────────┐
│  1. ISOLATE CONFLICT   │ Identify exact conflicting statements, files, and timestamps.
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 2. APPLY 9-TIER SOURCE │ Follow Source of Truth Priority (Tier 1 overrides Tier 9).
│    PRIORITY PROTOCOL   │ Live Evidence > Canonical Contracts > Specs > Handoffs...
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  3. NEWEST ADR/RECORD  │ If two canonical contracts conflict, the latest Owner-approved
│     SUPERSEDES OLD     │ ADR or contract date takes precedence.
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 4. RECORD & ESCALATE   │ If unresolved ambiguity remains, STOP and escalate to Owner.
└────────────────────────┘
```

### 4.1 The 9-Tier Source Priority Invariant:
1. **Tier 1: Live Runtime Evidence**: Measured post-state, exit codes, unit test receipts, clipboard hashes.
2. **Tier 2: Canonical Governance & Contracts**: `docs/contracts/`, `docs/governance/`, `decisions/`.
3. **Tier 3: Canonical Project Specifications**: `control/*.md`, `projects/*.md`, `docs/prd/`, `docs/roadmap/`.
4. **Tier 4: Current Session State & Continuity Handoffs**: `active_session.json`, `docs/continuity/*.md`.
5. **Tier 5: Historical Worklogs**: `worklog/sessions/YYYY-MM-DD/`, `worklog/daily/`.
6. **Tier 6: Operational Projections & Indexes**: `wiki/workdesk/HOME.md`, `CURRENT.md`, `PRD_INDEX.md`.
7. **Tier 7: Ephemeral Staging & Inbox**: `inbox/`, `inbox/session-closeouts/`.
8. **Tier 8: Chat Summaries & Transcripts**: Conversation history.
9. **Tier 9: Model Memory (Lowest Priority)**: LLM internal weights. **Never overrides repository truth.**

---

## 5. Canonical vs Derivative Knowledge

To prevent knowledge duplication and state divergence, ASB enforces a strict separation between Canonical and Derivative knowledge:

### 5.1 Canonical Knowledge (Source of Truth)
- **Definition**: The single, authoritative, handcrafted, or owner-approved source for a fact, contract, specification, or code.
- **Examples**: `docs/contracts/*.md`, `control/<project>.md`, `bin/airo-session`, production source code.
- **Mutation Rule**: Requires explicit plan review, acceptance criteria validation, and Owner approval before mutation.

### 5.2 Derivative Knowledge (Operational Projections)
- **Definition**: Views, indexes, digests, dashboard tables, and transclusions mechanically compiled from canonical sources.
- **Examples**: `state/active-session.md`, `runtime/workdesk/current-work.md`, `worklog/daily/YYYY-MM-DD.md`, `PRD_INDEX.md`.
- **Derivation Invariant**:
  > [!IMPORTANT]
  > Derivative knowledge MUST NEVER be edited directly as an authority source. If a derivative view contains errors or becomes stale, it must be regenerated or reset by its canonical generator (e.g. `scripts/airo-session-projection-sync`).

---

## 6. Fresh AI Universal Onboarding Protocol

Every Fresh AI agent starting a new turn, chat thread, or subagent branch MUST execute the following deterministic onboarding sequence:

```text
┌────────────────────────────────────────────────────────┐
│              STEP 1: BOOT & ROUTING GUARD              │
│  - Read BOOT.md                                        │
│  - Read CURRENT.md (Check active phase & overrides)   │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│            STEP 2: GOVERNANCE & IDENTITY               │
│  - Read AGENTS.md & CONTEXT.md                         │
│  - Read SECURITY.md (Safety & secret rules)            │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│          STEP 3: TARGET PROJECT DISCOVERY              │
│  - Read PRD_INDEX.md & ROADMAP_INDEX.md                │
│  - Read relevant control/<project>.md                  │
│  - Read latest handoff in docs/continuity/             │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│             STEP 4: SESSION LIFECYCLE GUARD            │
│  - Check runtime status: bin/airo-session status       │
│  - Start / continue session with Session Guard         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│            STEP 5: EMIT STATUS RECEIPT                 │
│  - Output standardized 🧭 AIRO STATUS header           │
└────────────────────────────────────────────────────────┘
```

**Guardrail**: Fresh AIs must NEVER begin by reading raw `inbox/` or `archive/` directories unless explicitly ordered to perform historical forensic audits.

---

## 7. Fresh AI Uncertainty Handling Rule

When a Fresh AI encounters ambiguity, underspecified instructions, missing credentials, or unresolvable source contradictions:

1. **Strict Non-Assumption**: The agent is STRICTLY FORBIDDEN from guessing Owner intent, inventing configurations, or proceeding on model memory assumptions.
2. **Controlled Stop**: Execution MUST stop before performing any state mutations or ungrounded planning.
3. **Structured Clarification Receipt**: The agent must output `🧭 AIRO STATUS` reporting:
   - `Kesimpulan: BELUM_TERBUKTI / BUTUH_KLARIFIKASI`
   - `Boleh lanjut: TIDAK`
   - `⛔ Hambatan: <Exact Ambiguity or Missing Information>`
   - `➡️ Berikutnya: Await Owner clarification on concrete options [A / B]`

---

## 8. Decision Lineage & Provenance Requirement

To prevent "ghost policies" and unjustified architecture shifts, every architectural, technical, or governance decision recorded in ASB must possess complete decision lineage:

1. **Explicit Identification**: Distinct ADR/Task ID (e.g. `ADR-AIRO-MULTI-DEVICE-ACCESS-V1`).
2. **Timestamp & Date Context**: ISO 8601 creation timestamp and execution host context.
3. **Authority Level**: Owner-Approved, Council-Deliberated, or Experimental.
4. **Parent Reference**: Direct linkage to parent contracts, specs, and PRDs.
5. **Trade-off Traceability**: Explicit record of alternative options evaluated and rejected rationale.
6. **Execution Provenance**: Recorded origin device, executor node, and repository identity.

> [!NOTE]
> No AI agent may enforce a rule or constrain architecture without being able to cite its canonical path under `docs/contracts/`, `docs/governance/`, or `decisions/`.

---

## 9. Knowledge Promotion Rules (Staging → Canonical)

Knowledge transitions through a controlled promotion lifecycle to protect canonical purity:

```text
┌─────────────────────────┐     1. Ingestion / Closeout      ┌─────────────────────────┐
│     RAW OWNER INPUT     │ ───────────────────────────────► │   STAGE 1: INBOX /      │
│  (Chat, Files, Voice)   │                                  │   SESSION CLOSEOUTS     │
└─────────────────────────┘                                  └───────────┬─────────────┘
                                                                         │
                                                                         │ 2. Distillation &
                                                                         │    Validation Proof
                                                                         ▼
┌─────────────────────────┐      3. Owner Approval Gate      ┌─────────────────────────┐
│   CANONICAL SECOND      │ ◄─────────────────────────────── │   STAGE 2: VALIDATION   │
│   BRAIN (docs/control)  │                                  │   & HANDOFFS            │
└─────────────────────────┘                                  └─────────────────────────┘
```

1. **Zero Direct-to-Canonical Chat Dumps**: Raw chat transcripts, model musings, or speculative prose must never be appended directly to canonical files.
2. **Distillation Requirement**: Information must be synthesized, deduplicated, and formatted per `AIRO_INPUT_PROCESSING_CONTRACT.md`.
