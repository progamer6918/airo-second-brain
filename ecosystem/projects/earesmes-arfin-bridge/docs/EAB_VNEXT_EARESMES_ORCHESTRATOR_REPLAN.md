# EAB vNext — Earesmes Orchestrator Replan

**Status:** DECISION_GRADE_REPLAN / PREPARATION  
**Date:** 2026-08-29  
**Related Defect Record:** [KCC Closed Session Visibility Defect (2026-08-29)](../../../docs/continuity/KCC_CLOSED_SESSION_VISIBILITY_DEFECT_20260829.md)  
**Previous Session Reference:** `1e97cbf6-2e62-4f2e-9385-dcd10b12c1c7` (Failed bounded recovery / Stop-loss triggered)  
**Active Context Reference:** [CURRENT_HANDOFF.md](./CURRENT_HANDOFF.md) | [01_PRD.md](./01_PRD.md) | [03_CONTRACTS.md](./03_CONTRACTS.md)  

---

## 1. Original Owner Need

* **Primary Interface:** Earesmes is intended to be the PRIMARY user-facing conversational interface for the Owner.
* **Domain Authority:** Arfin remains the authoritative system of record and financial domain authority.
* **Specialist / Admin Access:** Direct Arfin interaction can remain available as specialist, admin, or fallback access where appropriate, but is not the target daily intake UX.
* **Not a Dumb Forwarder:** Earesmes-Arfin Bridge (EAB) was NOT created merely to forward raw user messages verbatim from Earesmes to Arfin.
* **Value Proposition:** The Owner expects Earesmes to provide natural-language intelligence, conversational clarification UX, cross-turn context continuity, and orchestration value.
* **Strategic Rationale:** If Earesmes were only a dumb proxy/forwarder, there would be no reason for the Owner to route through Earesmes instead of using Arfin directly.

---

## 2. Larger Vision

* **Multi-Specialist Orchestration:** The Owner's longer-term vision is for Earesmes to serve as the intelligent orchestrator across multiple specialist domain workers/systems.
* **Target Topology:**
  ```text
  Owner
    │
    ▼
  Earesmes (Smart Orchestrator / Natural Language Front Door)
    ├──► Arfin (Authoritative Finance Specialist)
    ├──► Specialist Worker B (Future Domain)
    ├──► Specialist Worker C (Future Domain)
    └──► Future Subsystems
  ```
* **Unified Front Door:** The Owner interacts primarily with Earesmes without needing to track which backend specialist owns each command, entity, or workflow.
* **Strategic Role of EAB:** The EAB finance vertical is strategically critical because, once proven end-to-end, it serves as the reference orchestrator-to-specialist design pattern for all subsequent domain integrations.
* **Scope Guard:** No universal multi-agent framework is authorized or approved at this stage; work remains strictly bounded to proving this single vertical.

---

## 3. Intelligence vs Authority Boundary

The agreed conceptual separation between layers:

### EARESMES = SMART ORCHESTRATOR
* **Natural-Language Understanding:** Intent detection, entity extraction, conversational parsing.
* **Conversational Context:** Multi-turn draft continuity, clarifying missing values before dispatch.
* **Specialist Selection:** Routing verified intents to the appropriate specialist capability.
* **UX Presentation:** Formatting prompts, numbered choices, confirmations, and aggregating responses.
* **Strict Boundary:** Earesmes may PROPOSE domain interpretation (e.g. amount, raw text, suggested category), but must NOT become a duplicate store of authoritative financial truth.

### ARFIN = AUTHORITATIVE FINANCE SPECIALIST
* **Schema & Business Rules:** Canonical financial schema, validation rules, category/subcategory taxonomy.
* **State & Life-Cycle:** Account registry, pending clarification life-cycle, Review Queue staging.
* **Idempotency & Safety:** Idempotent request execution, deduplication keys, double-entry ledger boundary.
* **Strict Boundary:** Arfin makes authoritative acceptance/rejection decisions and commits financial state.

---

## 4. What Failed in Current EAB Approach

The bounded recovery attempt on 2026-08-29 established the following field facts:
1. **Local Test Success:** Natural-order parser repairs, missing-amount draft continuations, and multi-pending numbered selection all passed local automated test suites (T1–T10, C1–C10).
2. **Technical Activation:** Production runtime trial activation of the worker succeeded (clean reload via systemd user service, signed `list_pending` canary returned `SUCCESS`).
3. **Real Owner Acceptance Failure:** The live Owner test (`catat makan 1` → `cash`) failed to write to Review Queue.
4. **First RCA Findings:** Worker hardcoded defaults (`Other / Review` + `Lainnya`) were rejected by Apps Script category pair validation (`ERR_INVALID_CATEGORY_SUBCATEGORY`) prior to staging.
5. **One Causal Repair Attempt:** Causal repair applied canonical fallback (`Other / Review` + `Review`) and legacy draft normalization.
6. **Second Acceptance Failure:** Owner retry with `cash` again failed to reach Review Queue confirmation.
7. **Stop-Loss Execution:** Stop-loss triggered deterministically (no third repair attempt allowed).
8. **Rollback & Safety:** Durable canonical worker SHA `e4d9f3b3f2dbc2079a00da7cc2ae268179702ed5c3a31ccbadb37ced0df607fe` was restored. Review Queue exact matches remained `0`, direct Account Ledger writes remained `NO`, and financial safety state was confirmed `SAFE`.
9. **Failed Request Reference:** `manual_8482041086_0e05a012b44f48ec` (retained safely in drafts, untouched).

---

## 5. Structural Lessons

* **A. Semantic Duplication:** Finance-domain category registries and validation semantics became duplicated across worker Python code and Apps Script backend, causing brittle drift.
* **B. Late Acceptance Reality:** Technical green tests on isolated mocks created false confidence because real end-to-end acceptance through live backend validation happened too late in the cycle.
* **C. Synthetic Multi-Pending Limits:** Mocking numbered selection in worker memory does not validate whether the live backend substrate can reliably persist and clarify concurrent pending records.
* **D. Substrate Coupling:** The current substrate has heavy legacy coupling inside monolithic Apps Script files.
* **E. Vision Validity:** The root cause is architectural coupling and semantic leakage, NOT an inherent flaw in the orchestrator-specialist paradigm.
* **F. Repair Path Exhaustion:** The in-place incremental repair approach for legacy EAB worker bindings is fully exhausted and must not be resumed.

---

## 6. Owner Execution Requirements

To prevent regression to previous failure modes, all future AI sessions must adhere to:
* **No Endless Gates:** Execute bounded multi-step packets rather than creating excessive intermediate milestone gates.
* **No Premature Optimism:** Never mark tasks `DONE`/`PASS` based solely on technical mocks when real Owner acceptance is required.
* **Owner Primacy:** Real Owner operational outcome strictly outranks technical mock milestones.
* **Antigravity Role:** Executor-only mode; adhere strictly to low-token, no-brainer execution policies.
* **WSL Noninteractive:** Direct WSL execution; never emit interactive `exit`/`logout` commands.
* **Deterministic Receipts:** Produce timestamped logs, verified clipboard copies, readback verification, and SHA256 hashes.
* **Token Efficiency:** No redundant preambles, canonical re-summaries, or repeated deep scans.
* **Strict Stop-Loss:** One bounded causal cycle followed by hard stop/rollback rather than endless patching loops.
* **Knowledge Continuity:** Enable a fresh AI instance to immediately resume from ASB repository state without requiring the Owner to repeat explanations.

---

## 7. External Architecture References / Research Direction

These patterns serve as conceptual references only:
* **OpenAI Agents (Manager / Agents-as-Tools):** Orchestrator manages top-level context and invokes specialists as tools with typed schemas.
* **LangGraph (Supervisor Pattern):** Supervisor coordinates specialized workers with deterministic handoff boundaries.
* **Microsoft Agent Orchestration:** Clear distinction between orchestrator-retained context ownership versus complete domain handoff.
* **Model Context Protocol (MCP):** Standardized, typed, discoverable capability interfaces between client/orchestrator and tool providers.

> **Decision Rule:** COPY PATTERNS, NOT FRAMEWORKS.  
> No migration to Temporal, LangGraph, OpenAI Agents SDK, Semantic Kernel, or external orchestration frameworks is authorized.

---

## 8. Current Council Direction

* **No Repair #3:** Do not attempt further patches on the legacy EAB script integration.
* **No Generic Framework:** Do not attempt to build a universal multi-agent framework before proving one domain.
* **Reframe:** Reframe the initiative as **EAB vNext — Orchestrated Finance Vertical**.
* **Keep Core Separation:** Earesmes remains the intelligent conversational orchestrator; Arfin remains the authoritative finance specialist.
* **Vertical First:** Prove the single finance vertical end-to-end before generalizing capability contracts.

---

## 9. Ordered Next Work

```text
[NEXT_1: KCC Closed-Session Defect Verification]
   │
   ▼
[NEXT_2: Read-Only EAB vNext Specialist Feasibility Study]
   │
   ▼
[NEXT_3: Council GO / NO-GO Decision]
   │
   ├─► IF GO: [NEXT_4: Build Single Real Vertical (catat makan 1 -> cash -> Review Queue)]
   │             │
   │             ▼
   │          [NEXT_5: True Backend Multi-Pending Capability Proof]
   │             │
   │             ▼
   │          [NEXT_6: Extract Generic Specialist Capability Contract]
   │
   └─► IF NO-GO: Stop & Re-architect with Council
```

1. `NEXT_1`: Verify KCC closed-session visibility and semantic integrity defect ([KCC Defect Record](../../../docs/continuity/KCC_CLOSED_SESSION_VISIBILITY_DEFECT_20260829.md)).
2. `NEXT_2`: Perform read-only feasibility study: Can current Arfin expose a bounded specialist capability contract without duplicating finance semantics into Hermes and without new infrastructure?
3. `NEXT_3`: Council Deep GO/NO-GO evaluation based on feasibility findings.
4. `NEXT_4` *(Conditional on GO)*: Implement minimum real vertical (`catat makan 1` → clarification prompt → `cash` → verified Review Queue entry).
5. `NEXT_5`: Validate backend multi-pending clarification persistence.
6. `NEXT_6`: Formalize generic Specialist Capability Contract for subsequent domain workers.

---

## 10. GO / NO-GO Boundaries

Preliminary architectural constraints for EAB vNext GO decision:
* **No New Infrastructure:** No additional Telegram bots, background daemons, standalone databases, or GCP projects.
* **No Monolithic Rewrite:** No large-scale rewrite of Arfin core accounting engine.
* **Authoritative Domain Integrity:** Finance validation rules stay exclusively inside Arfin.
* **Bounded Surface Area:** Well-defined input/output contracts between Earesmes and Arfin specialist adapter.
* **No-Go Trigger:** If feasibility indicates that clean orchestration requires heavy new infrastructure or deep rewrite of Arfin core, return to Council for formal NO-GO/re-architecture rather than silently expanding scope.

---

## 11. Product Truth

```ini
EARESMES_ORCHESTRATOR_VISION=VALID_DIRECTION_NOT_YET_PROVEN
EAB_ORIGINAL_PRODUCT_NEED=VALID
CURRENT_EAB_REPAIR_PATH=EXHAUSTED
EAB_RECOVERY_RESULT=FAILED_BOUNDED_ATTEMPT
EAB_VNEXT_IMPLEMENTATION_AUTHORIZED=NO
EAB_VNEXT_FEASIBILITY_AUTHORIZED_NEXT=YES
```
