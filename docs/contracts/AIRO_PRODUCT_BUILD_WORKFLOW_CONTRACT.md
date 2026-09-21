---
type: contract
project: GLOBAL
status: CANONICAL
authority: OWNER_APPROVED
date: 2026-09-21
audience: all_airo_operators_and_ai_consumers
---

# 📜 AIRO Product Build Workflow Contract

**Contract ID:** `AIRO_CONTRACT_PRODUCT_BUILD_WORKFLOW_V1`  
**Effective Date:** 2026-09-21  
**Canonical Path:** `docs/contracts/AIRO_PRODUCT_BUILD_WORKFLOW_CONTRACT.md`  
**Parent Governance Contracts:**  
- `docs/contracts/AIRO_CAPABILITY_DISCOVERY_GATE_CONTRACT.md`  
- `docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md`  
- `docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_CONTRACT.md`  
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`  
- `docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`  

---

## 1. Purpose & Architecture Principles

The **AIRO Product Build Workflow V1** establishes the canonical, end-to-end lifecycle for product and capability development across the AIRO ecosystem without introducing external frameworks, duplicate authorities, or redundant agent hierarchies.

### 1.1 Governance Guardrails
- **NO New Framework:** Do NOT install or fork BMAD, OpenSpec, or Spec Kit.
- **NO Duplicate PRD System:** Capability briefs and PRD artifacts share a single canonical specification format in ASB.
- **NO Duplicate Authority or Hierarchy:** ChatGPT remains the Planning/Intelligence Layer, Antigravity (AGY) the Executor, and WSL the Runtime.
- **Council Reused:** Reuses existing canonical AIRO Council deliberation (from KCC / ADR conventions) for high-impact architecture choices.

### 1.2 Target Workflow Architecture

```text
OWNER INTENT
  ↓
INTENT CLASSIFICATION
  ↓
ADAPTIVE ROUTING

    Simple Question
        ↓
    Answer

    Bug Investigation
        ↓
    Evidence → Diagnosis → Fix

    Small Change (e.g., UI text / localized fix)
        ↓
    Direct Execution

    New Capability
        ↓
    Interview Protocol
        ↓
    Capability / PRD Artifact

    High Impact Decision
        ↓
    Council Deliberation

  ↓
Technical Design Gate (when required)
  ↓
Execution Contract
  ↓
Antigravity (AGY Executor)
  ↓
Acceptance Evidence
```

---

## 2. Intent Classification & Adaptive Routing

Every incoming Owner intent is deterministically classified into one of the following execution paths:

| Intent Category | Routing Action | Interview Required | Capability/PRD Artifact | Tech Design Gate | Council Deliberation |
|---|---|---|---|---|---|
| `SIMPLE_QUESTION` | Direct Answer | **NO** | **NO** | **NO** | **NO** |
| `BUG_INVESTIGATION` | Evidence → Diagnosis → Fix | **NO** | **NO** | **NO** | **NO** |
| `SMALL_CHANGE` (UI text / tweak) | Direct Execution | **NO** | **NO** | **NO** | **NO** |
| `NEW_CAPABILITY` | Interview Protocol → Artifact | **YES** | **YES** | Conditional | Conditional |
| `HIGH_IMPACT_DECISION` | Council Deliberation | As needed | As needed | Conditional | **YES** |

---

## 3. AIRO Interview Protocol

When intent is classified as `NEW_CAPABILITY`, AIRO must thoroughly discover and align requirements before producing the capability artifact.

### 3.1 Three Discovery Categories
1. **Problem Discovery:**
   - `Problem`: Exact problem or limitation being addressed.
   - `Current Pain`: Concrete friction, inefficiency, or failure in the current setup.
   - `Expected Improvement`: Specific measurable benefit or desired state.
2. **Product Discovery:**
   - `Primary User`: Primary consumer (Owner, ChatGPT, Antigravity, Hermes, Telegram Operator).
   - `Desired Outcome`: Target functionality and deliverable format.
   - `Scope`: Boundaries of what is explicitly included.
   - `Non Scope`: Boundaries of what is explicitly excluded.
3. **Constraint Discovery:**
   - `Business Constraint`: Commercial, operational, or brand limits.
   - `Technical Constraint`: Stack, runtime, platform, or dependencies limits.
   - `Resource Constraint`: Time, quota, hardware, or model limits.

### 3.2 The Strict UNKNOWN Rule
> [!IMPORTANT]
> If any critical piece of information is not supplied by the Owner or supported by canonical evidence, **DO NOT INFER OR HALLUCINATE**.
> AIRO must explicitly designate the field as `UNKNOWN` and prompt the Owner for clarification.

---

## 4. Capability / PRD Artifact Structure

Capability and PRD definitions are unified in a single structured specification avoiding parallel PRD silos:

- **Objective:** High-level strategic goal.
- **Problem:** Root problem statement.
- **Primary User:** Intended user / actor.
- **Current Workflow:** Current process or workaround.
- **Desired Outcome:** Expected behavior and deliverables.
- **Scope:** In-scope components and milestones.
- **Non Scope:** Explicit exclusions.
- **Acceptance Criteria:** Observable DoD conditions.
- **Open Questions:** Unresolved trade-offs.
- **Constraints:** Technical, business, and operational guardrails.
- **Unknowns:** Explicit list of `UNKNOWN` items awaiting Owner clarification.

---

## 5. Design Context Hook (Optional)

Applicable **ONLY** when UI or user interaction is involved (UI-heavy capabilities, visual dashboards, game/product interfaces, user-facing workflows). For non-UI / backend capabilities, design context is **SKIPPED**.

### 5.1 Design Context Fields
- **User Flow:** Ordered sequence of user interaction steps.
- **UI Impact:** Affected screens, components, widgets, or CLI prompts.
- **Interaction Notes:** Responsiveness, validations, hover/click behaviors, error feedback.
- **Prototype Required:** `YES` or `NO`.

### 5.2 Tooling Boundary
> [!NOTE]
> Do NOT install external design dependencies (e.g., Penpot, Figma integrations). Pure Markdown specifications, text wireframes, and lightweight diagrams (Mermaid / SVG) are canonical.

---

## 6. Technical Design Gate

### 6.1 When Technical Design is Required
A formal Technical Design section or document is required **ONLY** when one or more triggers exist:
1. **Multiple Subsystem Impact:** Affects 2 or more distinct subsystems (e.g., Hermes + Telegram Gateway + ASB).
2. **Architecture Boundary Change:** Crosses or mutates system boundaries (e.g., Intelligence Layer vs Execution Layer, VPS vs Local WSL).
3. **External Integration:** Adds or mutates third-party APIs, OAuth credentials, or network protocols.
4. **Major Data Model Change:** Alters schemas, storage contracts, SQLite databases, or event streams.

### 6.2 When Technical Design is Skipped
Skipped for isolated changes, documentation updates, bug fixes, localized script adjustments, and bounded UI text changes.

### 6.3 Technical Design Structure
When required, capture:
- **Architecture:** Structural overview and component breakdown.
- **Data Flow:** Pipeline and communication protocols.
- **Dependencies:** Required packages, services, or tools.
- **Trade-offs:** Rejected alternatives and rationale.
- **Risks:** Failure modes and mitigations.
- **Migration Plan:** Rollout, cutover, or rebase procedures.

---

## 7. Council Deliberation Integration

Reuses existing AIRO Council deliberation conventions (established in KCC & architecture decision records).

### 7.1 Council Nature & Scope
The Council is **NOT**:
- An autonomous multi-agent hierarchy;
- An execution engine;
- A democratic voting mechanism.

### 7.2 Council Triggers
Council deliberation is triggered **ONLY** for:
- Architecture choices;
- Strategic direction changes;
- Major trade-off evaluations;
- Irreversible decisions;
- Cross-project impacts.

### 7.3 Epistemic Output Format
Council deliberation outputs must strictly preserve:
- **FACT:** Directly verifiable evidence from code, logs, or canonical repositories.
- **INFERENCE:** Logical deduction derived explicitly from facts.
- **ASSUMPTION:** Working hypothesis requiring empirical validation.
- **UNKNOWN:** Explicit lack of knowledge requiring Owner guidance or research.
