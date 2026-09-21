---
type: contract
project: GLOBAL
status: CANONICAL
authority: OWNER_APPROVED
date: 2026-09-21
audience: all_airo_operators_and_ai_consumers
---

# 📜 AIRO Capability Discovery Gate Contract

**Contract ID:** `AIRO_CONTRACT_CAPABILITY_DISCOVERY_GATE_V1`  
**Effective Date:** 2026-09-21  
**Canonical Path:** `docs/contracts/AIRO_CAPABILITY_DISCOVERY_GATE_CONTRACT.md`  
**Parent Governance Contracts:**  
- `docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md`  
- `docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_CONTRACT.md`  
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`  
- `docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`  

---

## 1. Purpose & Core Objective

The **AIRO Capability Discovery Gate** defines a minimal, lightweight discovery checkpoint prior to capability creation or major architectural changes.

### 1.1 The Lifecycle Evolution

**Previous Lifecycle:**
```text
Intent → Capability → Approval → Execution → Evidence
```

**Target Lifecycle (Enforced by this Contract):**
```text
Intent
  ↓
Intent Classification
  ↓
(if capability request) Discovery Checkpoint
  ↓
Capability Definition / Spec
  ↓
Approval
  ↓
Execution
  ↓
Evidence
```

---

## 2. Intent Classification & Gating Rules

Before any code modification or capability specification begins, incoming requests MUST be classified to determine if discovery is required or skipped.

### 2.1 When Discovery is Required
Discovery is strictly mandatory when:
1. **New Capability Request:** Creation of a new tool, adapter, subsystem, engine, agent skill, or workflow.
2. **Major Capability Change:** Significant refactoring, interface changes, or behavior changes to an existing capability.

### 2.2 When Discovery is Skipped
Discovery is explicitly skipped (direct progress to execution/response) for:
1. **Simple Questions:** Information retrieval, codebase queries, status inquiries.
2. **Bug Investigations:** Diagnostic research, defect analysis, root-cause isolation without architectural scope changes.
3. **Small Changes:** Localized bug fixes, documentation typos, configuration adjustments, trivial non-breaking tweaks.

---

## 3. Mandatory Discovery Checkpoint Fields

When discovery is required, the discovery checkpoint MUST capture ONLY the following 5 dimensions:

1. **Problem:** What specific problem, friction, or limitation does this capability solve?
2. **Primary User:** Who or what is the primary consumer (Owner, ChatGPT Planning Layer, Antigravity Executor, Hermes, Telegram Operator)?
3. **Current Workflow:** How is the task or problem currently handled (or why does the current system fail to handle it)?
4. **Desired Outcome:** What is the exact expected result, output format, or behavior upon completion?
5. **Constraints:** What are the non-negotiables, boundary restrictions, security limits, or forbidden mutations?

No additional heavy framework artifacts, speculative user personas, or verbose boilerplates are permitted.

---

## 4. Technical Specification Threshold Rule

To maintain agile velocity and avoid unnecessary overhead:

### 4.1 When Technical Specification is Required
A formal Technical Specification is required **ONLY** when one or more of the following conditions are met:
1. **Multiple Subsystem Impact:** The capability affects two or more distinct subsystems (e.g., Hermes + Telegram Gateway + ASB).
2. **Architecture Boundary Changes:** The capability crosses or modifies existing architectural boundaries (e.g., Intelligence Layer vs Execution Layer, VPS vs Local WSL).
3. **External Integration Changes:** The capability introduces, alters, or replaces third-party APIs, credentials, or external network integrations.

### 4.2 When Technical Specification is Skipped
For single-subsystem capabilities, modular adapters, and bounded internal additions, a formal technical spec is **SKIPPED**. The 5-point Discovery Checkpoint is sufficient to proceed directly to Approval and Execution.

---

## 5. Governance & Framework Guardrails

To preserve repository hygiene and avoid governance bloat:
- **NO New Framework:** Do NOT introduce heavyweight product management frameworks.
- **NO BMAD Fork:** Do NOT fork or introduce BMAD methodologies.
- **NO OpenSpec / Spec Kit:** Do NOT install or depend on OpenSpec, Spec Kit, or external specification toolchains.
- **NO Parallel PRD System:** PRDs remain indexed in `PRD_INDEX.md`; do not build duplicate parallel PRD structures.
- **NO Duplicate Authority:** Canonical authority resides strictly in ASB repository contracts.
- **NO Redesign of KCC or Execution Contracts:** This contract serves strictly as an upstream intake gate.
