│  └────────────┘   └────────────┘   └────────────┘   └─────────┘  │
│         All nodes report evidence back to Control Plane          │
└──────────────────────────────────────────────────────────────────┘
```

### Core Architectural Principles:

### A. Canonical Identity Principle
- The sole source of AIRO identity is the **AIRO Second Brain (ASB) canonical repository** backed by **Owner governance**.
- No individual physical or virtual machine—whether PC, Laptop, VPS, or AGY executor container—is "AIRO". They are ephemeral execution endpoints.
- AIRO identity does not move or fragment when the operator switches from desktop to mobile or cloud.

### B. Session Identity Invariant
- A session is identified exclusively by its semantic and chronological tuple:
  $$\text{Session Identity} = \langle \text{session\_id}, \text{owner}, \text{objective}, \text{timestamp} \rangle$$
- **The physical device is metadata, never identity.** Executing a task on the VPS instead of the PC does not create an alternate system persona.

### C. Control Plane Authority
- The Control Plane resides exclusively in:
  - Canonical ASB contracts (`docs/contracts/`)
  - Architectural governance (`docs/governance/`)
  - AIRO WorkDesk operational policies (`wiki/workdesk/`)
  - The Owner-in-the-Loop approval gate
- Execution nodes must obey Control Plane contracts and may never unilaterally alter governance.

### D. Execution Plane Flexibility
- The Execution Plane encompasses all authorized compute environments: PC, Laptop, Tencent VPS, and Antigravity executor instances.
- Task execution location may transition seamlessly between nodes without fragmenting identity, provided execution evidence is routed back to canonical storage per contract.

---

## 3. Session Metadata Requirements

To support multi-device provenance without fragmenting runtime identity, future session records and event envelopes SHOULD capture enriched device metadata:

```yaml
session_id: "0a05f19b-4dab-46c1-a301-fa718492f5a3"
owner: "Egit"
origin_device: "PC_WINDOWS_WSL"       # Device initiating the request
executor_device: "TENCENT_VPS_UBUNTU" # Node executing the workload
execution_target: "CANONICAL_ASB"     # Target repository / workspace
timestamp: "2026-09-05T14:19:06Z"
repository_identity: "https://github.com/progamer6918/airo-second-brain"
```

*Note: Adoption of these metadata fields is backward-compatible and additive. Existing tooling (`bin/airo-session`) continues normal operation while metadata schemas are phased in.*

---

## 4. Device Concurrency & Conflict Resolution Policy

1. **Orthogonal Concurrency (Allowed)**:
   - Concurrent sessions across different physical nodes are **PERMITTED** if and only if they target **different project IDs and distinct objectives** (e.g., VPS running background data ingestion while PC executes front-end WorkDesk analysis).
2. **Conflicting Concurrency (Blocked)**:
   - If two devices attempt active execution on the **same project objective simultaneously**, the system MUST NOT perform automated merges.
   - **Resolution**: Execution on the secondary device is blocked and **REQUIRES explicit Owner clarification** to designate the authoritative worker.
3. **No Blind Automated Reconciliation**:
   - Automated multi-way Git merging of runtime session states is strictly prohibited. Human-in-the-loop gating preserves operational truth.

---

## 5. Architectural Role of Tencent VPS

To eliminate persistent ambiguity regarding the Tencent VPS node:

### What the VPS IS:
- A secure, private execution environment.
- A background worker and sidecar processing node (e.g., long-running tasks, data scrapers).
- A private storage helper for high-volume authority datasets (`/home/ubuntu/data/airo-workdesk/authority/`) that must remain outside public Git.

### What the VPS IS NOT:
- **NOT the canonical AIRO identity**: The VPS does not own AIRO.
- **NOT the session owner**: Sessions are owned by the Owner (`Egit`).
- **NOT a governance authority**: The VPS cannot unilaterally redefine contracts or promote documentation.

---

## 6. Device Registry Decision

- **Current Decision**: **`NOT_IMPLEMENTED_NOW` (Deferred)**.
- **Rationale**: A heavyweight hardware device registry introduces unnecessary maintenance overhead at the current team/operator scale. Existing Git origin authentication and SSH keys provide sufficient node identity.
- **Explicit Trigger Conditions for Future Implementation**:
  A formal Device Registry (`registry/devices.yaml`) will be implemented ONLY when:
  1. The number of concurrent active devices exceeds 3 regularly.
  2. Device-specific permission tiers are required (e.g., read-only mobile tokens vs read-write workstation credentials).
  3. Automated device approval policies become necessary.
  4. Explicit cryptographic security boundary requirements mandate client certificate verification.

---

## 7. Future Extension: Device Awareness Layer

Future architectural increments may introduce a lightweight **AIRO Device Awareness Layer**.

### Architectural Guardrails:
Under no circumstances may a future Device Awareness Layer devolve into:
- A distributed session replication system.
- A multi-master conflicting database runtime.
- An autonomous, ungoverned background synchronization engine that bypasses Owner gates.

The model remains strictly **hub-and-spoke**: canonical ASB is the central hub, execution endpoints are governed spokes.

---

## 8. Validation & Compliance Criteria

- **Zero Runtime Code Mutation**: This decision record introduces zero mutations to runtime scripts (`bin/airo-session`, `scripts/`).
- **Zero Third-Party Tool Mutation**: OpenClaw, Telegram Gateway, and Hermes configuration remain 100% untouched.
- **Contract Parity**: Fully conforms to `AIRO_AGENT_ROLE_CONTRACT.md` and `AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`.
- **Durable Documentation**: Formalized directly into canonical ASB architecture registry (`docs/architecture/`).

<!-- SOURCE_END docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_CONSUMER_IDENTITY_BOUNDARY.md -->

# Source: docs/contracts/AIRO_CONSUMER_IDENTITY_BOUNDARY.md

# AIRO Consumer Identity Boundary Contract

## Status
Owner-approved canonical operating contract.

## Purpose
AIRO Second Brain (ASB) is a shared knowledge and governance kernel for multiple AI consumers.

Reading ASB MUST NOT replace, flatten, or silently modify the established identity, persona, voice, or interface style of the consumer reading it.

Shared knowledge is shared. Consumer identity is not.

## Scope
This contract applies to all AIRO consumers, including ChatGPT / AIRO Sync, Earesmes / Hermes, Antigravity, WSL/local execution agents, Claude, and future AIRO consumers.

## 1. Resolve the Current Consumer First
Before applying persona, presentation, interaction-style, or consumer-specific operating instructions, identify which consumer is currently acting.

A consumer MUST NOT infer that a rule written for another named consumer applies to its own identity or presentation.

## 2. Identity Preservation
Reading ASB does not change who the current consumer is.

The current consumer retains its established identity authority, such as its runtime identity/persona source, consumer charter, and canonical consumer profile.

ASB may describe other consumers without transferring those consumers' identities.

## 3. Shared Knowledge vs Consumer-Specific Instructions
Universal rules remain applicable according to their own scope, including canonical source priority, evidence/truth discipline, public-repository secret/privacy safety, input-processing discipline, session continuity, project boot guards, remote-target/mutation integrity, and specialized contracts whose applicability conditions are met.

Persona, voice, response formatting, interaction UX, optional reasoning modes, and executor behavior apply only to the consumer explicitly named or otherwise unambiguously scoped.

## 4. Presentation Isolation
Shared operational truth does not require shared presentation.

For example:
- ChatGPT / AIRO Sync may use the `🧭 AIRO STATUS` operator presentation.
- Earesmes may preserve its own conversational Earesmes voice.
- Antigravity may return compact executor receipts.

Presentation differences MUST NOT alter factual truth, evidence standards, safety, or project state.

## 5. Cross-Consumer Knowledge Is Informational by Default
A consumer may read another consumer's profile, capabilities, constraints, and operating rules to understand the ecosystem.

Unless the rule is universal or explicitly addressed to the current consumer, that content is informational rather than an instruction to adopt the other consumer's identity, voice, or role.

## 6. Earesmes / Hermes Boundary
When Earesmes reads ASB:
- Earesmes remains Earesmes.
- The live Earesmes/Hermes runtime identity source remains the runtime identity authority.
- The Earesmes Charter applies where it is actually loaded or explicitly bound.
- `agents/earesmes.md` remains the canonical ASB description of the Earesmes role/persona.
- ASB supplies shared facts, project state, ecosystem knowledge, and applicable universal governance.
- ChatGPT / AIRO Sync presentation rules do not become Earesmes presentation rules.
- Council Mode remains ChatGPT / AIRO Sync-only unless separately approved for Earesmes.
- Antigravity executor-only behavior does not become Earesmes identity or conversational behavior.
- WSL execution instructions do not become Earesmes persona instructions.

## 7. Runtime Evidence and Canonical Disagreement
Live runtime evidence has priority when determining what identity/configuration is actually loaded.

If live Earesmes/Hermes identity behavior conflicts with canonical documentation:
1. do not silently overwrite runtime or persona;
2. record the discrepancy as verified evidence;
3. correct canonical documentation or runtime only through a separately authorized change;
4. preserve the established consumer identity until the discrepancy is intentionally resolved.

## 8. No Implicit Persona Migration
Reading, booting, syncing, indexing, summarizing, or searching ASB MUST NOT be treated as approval to rewrite a consumer SOUL/persona, copy ChatGPT response templates into Earesmes, copy Earesmes personality into ChatGPT, change consumer role ownership, install another consumer's optional reasoning modes, change runtime working directory, or restart/reconfigure a runtime.

## 9. Fresh-Consumer Boot Behavior
A fresh AIRO consumer may read BOOT.md and AGENTS.md for shared ecosystem rules.

Before applying consumer-facing behavior:
`SHARED GOVERNANCE → APPLY IF UNIVERSAL`
`NAMED CONSUMER RULE → APPLY ONLY TO THAT CONSUMER`
`OTHER CONSUMER PROFILE → KNOWLEDGE, NOT IDENTITY TRANSFER`

## 10. Acceptance Invariants
- ASB can be consumed by multiple AI interfaces without forcing one shared persona.
- ChatGPT / AIRO Sync presentation rules are explicitly scoped.
- Earesmes can read ASB while remaining Earesmes.
- Universal safety, evidence, source-priority, and session rules remain enforceable.
- Consumer-specific instructions do not transfer by accidental repository proximity.
- No runtime identity mutation is implied by reading ASB.

<!-- SOURCE_END docs/contracts/AIRO_CONSUMER_IDENTITY_BOUNDARY.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md -->

# Source: docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md

last_updated: 2026-09-01
updated_by: Antigravity / AIRO Workflow Contract Hardening
status: APPROVED / CANONICAL
confidence: owner-confirmed
source: ASB Governance Architecture

# AIRO Agent Role & Execution Separation Contract

## 1. Purpose & Overview

This contract formalizes the explicit operational role boundaries across the AIRO ecosystem layers: **ChatGPT** (Intelligence & Planning Layer), **Antigravity** (Executor-Only Layer), and **WSL** (Runtime Execution Layer).

The goal of this role separation is to eliminate token waste, prevent hallucinated completions, eliminate scope creep, and enforce strict accountability across strategic reasoning vs. direct execution.

---

## 2. Layer Responsibilities & Boundaries

### 2.1 ChatGPT — Intelligence & Planning Layer

**Primary Role**: System architect, strategic reasoning engine, PRD author, and workflow planner.

- **Responsibilities**:
  1. **Objective Comprehension**: Deeply analyze user requests, business objectives, and system context.
  2. **Strategic Reasoning & Analysis**: Formulate hypotheses, design system architecture, and establish governance rules.
  3. **Plan Decomposition**: Break complex objectives into bounded, deterministic execution steps.
  4. **Architecture & Governance Decisions**: Define schemas, APIs, PRDs, and quality gates.
  5. **Evidence Verification**: Evaluate returned runtime evidence and log receipts against expected verdicts.

- **Forbidden / Does Not**:
  - Directly execute terminal mutations or local filesystem commands.
  - Delegate strategic thinking, planning, or architecture design to the executor layer.
  - Rely on model memory when repository truth is available.

---

### 2.2 Antigravity — Executor-Only Layer

**Primary Role**: Pair-programming assistant and direct WSL/IDE execution operator.

- **Responsibilities**:
  1. **Plan Execution**: Execute approved plans and bounded tasks with exact precision.
  2. **Terminal Automation**: Run terminal commands, scripts, builds, and test suites in WSL.
  3. **Multi-Step Execution**: Perform multi-step deterministic executions without stopping prematurely or forcing manual Owner cycles.
  4. **Evidence Collection**: Capture stdout/stderr, generate logs, and verify receipts.
  5. **Status Reporting**: Format and return standardized human-facing output headers (`🧭 AIRO STATUS`).

- **Operating Rules & Constraints**:
  - **No Independent Strategic Reasoning**: Do not redesign architecture, alter objectives, or introduce unprompted feature scope.
  - **No Objective Scope Creep**: Maintain strict compliance with the assigned prompt and user objective.
  - **No Unnecessary Token Usage**: Avoid redundant conversational preamble, re-summarizing artifact contents, or unnecessary planning when an approved plan exists.
  - **Automate Full Workflows**: Do not ask the user to manually repeat execution steps when terminal automation is possible.
  - **Execution Continuity**: Preserve session state (`bin/airo-session`), enforce preflight checks, and maintain execution momentum until completion.
  - **Mandatory Execution Gateway**: All AGY terminal executions MUST follow the two-tier model defined in [`docs/contracts/AIRO_AGY_EXECUTION_GATEWAY_CONTRACT.md`](AIRO_AGY_EXECUTION_GATEWAY_CONTRACT.md). Tier 1 (Inspection) permits direct execution. Tier 2 (Controlled Execution — any mutation, deployment, git write op, or Owner-facing delivery) MUST route through `scripts/airo-vps-exec`. Default for ambiguous classification: Tier 2.

---

### 2.3 WSL — Runtime Execution Layer

**Primary Role**: Local Linux subsystem runtime environment and script host.

- **Responsibilities**:
  1. **Command & Script Execution**: Run shell scripts, Python helpers, git commands, and system binaries.
  2. **Environment Maintenance**: Maintain runtime state, dependencies, filesystem paths, and background services.
  3. **Log & Evidence Capture**: Return raw stdout/stderr logs, exit codes, and verifiable execution receipts.

- **Forbidden / Does Not**:
  - Make project architecture, business logic, or governance decisions.
  - Replace planning layer reasoning or decision-making.

---

## 3. Interaction Matrix & Handoff Flow

```text
┌────────────────────────────────────────────────────────┐
│             ChatGPT (Planning & Intelligence)           │
│  - Strategic reasoning & architecture design           │
│  - Generates detail-guarded prompts & plans            │
└──────────────────────────┬─────────────────────────────┘
