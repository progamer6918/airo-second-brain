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

The **AIRO Capability Discovery Gate** defines a minimal, lightweight discovery and brief checkpoint prior to capability creation, technical design, or execution.

### 1.1 Target Lifecycle

The complete lifecycle for all AIRO capability requests is:

```text
Intent
  ↓
Intent Classification
  ↓
Discovery Gate
  ↓
Capability Brief
  ↓
(Optional Technical Design)
  ↓
Approval
  ↓
Execution
  ↓
Evidence
```

---

## 2. Intent Classification & Gating Rules

Before code modification or capability specification begins, incoming requests MUST be classified to determine gating requirements.

### 2.1 When Discovery & Capability Brief Are Required
Discovery and a Capability Brief are strictly mandatory when:
1. **New Capability Request:** Creation of a new tool, adapter, subsystem, engine, agent skill, or workflow.
2. **Major Capability Change:** Significant refactoring, interface alterations, or fundamental behavior modifications.

### 2.2 When Discovery & Capability Brief Are Skipped
Discovery and Capability Briefs are explicitly **SKIPPED** (direct progress to execution/response) for:
1. **Questions:** Information retrieval, codebase queries, status inquiries, or conceptual explanations.
2. **Bug Investigations:** Diagnostic research, defect analysis, log audits, or root-cause isolation without architectural scope changes.
3. **Small Changes:** Localized bug fixes, documentation/typo corrections, configuration tweaks, or minor bounded updates.

---

## 3. Capability Brief Structure & Mandatory Fields

When a capability is created or significantly altered, a **Capability Brief** must be produced capturing the following structured sections:

### 3.1 Capability Context
1. **Problem:** What specific problem, friction, or limitation does this capability solve?
2. **Primary User:** Who or what is the primary consumer (Owner, ChatGPT Planning Layer, Antigravity Executor, Hermes, Telegram Operator)?
3. **Current Workflow:** How is the task or problem currently handled (or why does the current system fail to handle it)?
4. **Desired Outcome:** What is the exact expected result, output format, or behavior upon completion?
5. **Constraints:** What are the non-negotiables, boundary restrictions, security limits, or forbidden mutations?

### 3.2 Acceptance Criteria
Define observable, deterministically verifiable success conditions.
> [!IMPORTANT]
> **No Assumption Rule:** Do NOT fill unknown information with speculative assumptions. Use `UNKNOWN` whenever Owner input or clarification is required.

### 3.3 Design Context (Optional)
Applicable **ONLY** when UI or user interaction is affected:
- **User Flow:** Sequential interaction steps taken by the user.
- **UI Impact:** Affected screens, components, views, or message formats.
- **Interaction Notes:** Expected behaviors, edge case handling, or responsive feedback.

> [!NOTE]
> Do NOT introduce Penpot, Figma integrations, or external design tools. Pure Markdown descriptions, text flows, or simple ASCII/Mermaid mockups are canonical.

---

## 4. Technical Design Decision Gate

To prevent spec bloat and maintain fast execution velocity:

### 4.1 When Technical Design is Required
A formal Technical Design document is required **ONLY** when one or more of the following triggers exist:
1. **Multiple Subsystem Impact:** Affects two or more distinct subsystems (e.g., Hermes + Telegram Gateway + ASB).
2. **Architecture Boundary Change:** Crosses or modifies existing architectural boundaries (e.g., Planning vs Execution Layer, VPS vs Local WSL, ASB vs AWD).
3. **External Integration:** Introduces, alters, or replaces third-party APIs, credentials, or external network integrations.
4. **Significant Data Model Change:** Alters database schemas, event stream models, or persistent state contracts.

### 4.2 When Technical Design is Skipped
A formal Technical Design document is **NOT REQUIRED** for:
- Simple local changes;
- Documentation and contract updates;
- Isolated bug fixes;
- Bounded UI/text/config adjustments.

> [!CAUTION]
> Do NOT create a mandatory technical spec / design document for every task. For single-subsystem, bounded additions, the Capability Brief provides sufficient design context to proceed directly to Approval and Execution.

---

## 5. Governance & Framework Guardrails

To preserve repository hygiene and avoid governance bloat:
- **NO New Framework:** Do NOT introduce heavyweight product management frameworks.
- **NO BMAD Fork:** Do NOT fork or introduce BMAD methodologies.
- **NO OpenSpec / Spec Kit:** Do NOT install or depend on OpenSpec, Spec Kit, or external specification toolchains.
- **NO Parallel PRD System:** PRDs remain indexed in `PRD_INDEX.md`; do not build duplicate parallel PRD structures.
- **NO Duplicate Authority:** Canonical authority resides strictly in ASB repository contracts.
- **NO Redesign of KCC or Execution Contracts:** This contract serves strictly as an upstream intake and design gate.
