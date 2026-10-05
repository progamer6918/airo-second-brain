# 🏛️ Architecture Decision Record: AIRO Hybrid Multi-Device Access Model

**ADR ID:** `ADR-AIRO-MULTI-DEVICE-ACCESS-V1`  
**Task ID:** `AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1`  
**Date:** 2026-09-05  
**Status:** `ACCEPTED` (Council Deep Deliberation & Owner-Confirmed)  
**Governance Authority:** Owner-Confirmed (ASB Architecture & Governance Restored)  
**Canonical File:** `docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md`  
**Parent Contracts:**  
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`  
- `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`  
- `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`  
- `docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md`  

---

## 1. Problem Statement & Context

The AIRO operational ecosystem has evolved beyond a single physical machine. Operational tasks, planning, automation, and continuous background processing now span multiple execution surfaces:
- **Primary Workstation (PC / WSL)**: Interactive engineering, coding, local tool orchestration, and large-scale model automation.
- **Mobile Workstation (Laptop)**: Field work, off-site monitoring, and mobile terminal access.
- **Cloud Infrastructure (Tencent VPS)**: Headless background daemons, persistent listener queues, and private sidecar storage.
- **AI Execution Agents (Antigravity Executor / Claude / ChatGPT)**: Autonomous coding agents executing bounded batches in isolated workspace scratch environments.

### The Multi-Device Risks:
Without a rigorous canonical architectural decision, operating across multiple devices creates critical operational risks:
1. **Divergent Runtime States**: Multiple nodes generating unsynchronized `active_session.json` files in independent `~/.local/state` trees.
2. **Ghost & Stale Sessions**: Sessions closed on one machine leaving frozen active cards on another machine's presentation surface (as observed in the recent WorkDesk current-work stale card incident).
3. **Fragmented Ownership**: Disputed authority over which machine represents "the real AIRO".
4. **Continuity Corruption**: Worklogs and milestone advancements recorded out of chronological sequence, breaking Obsidian WorkDesk and historical provenance.

---

## 2. Architecture Decision: The Hybrid Multi-Device Model

Council Deep deliberation has formally resolved that **AIRO operates as a Hybrid Multi-Device Architecture**.

The system strictly enforces a structural separation between **Identity & Control** and **Execution**:

```text
┌──────────────────────────────────────────────────────────────────┐
│                   CONTROL & IDENTITY PLANE                       │
│  - Authority: AIRO Second Brain Canonical Repository + Owner     │
│  - Enforces: Contracts, Policies, WorkDesk Governance, Approvals │
│  - Ground Truth: ONE SINGLE CANONICAL BRAIN (Git + Vault)        │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ Directs / Governs
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                       EXECUTION PLANE                            │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌─────────┐  │
│  │   PC WSL   │   │ Laptop WSL │   │ Tencent VPS│   │   AGY   │  │
│  │ Node (Local│   │ Node (Field│   │ Node (Cloud│   │ Executor│  │
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
