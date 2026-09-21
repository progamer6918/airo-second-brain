# AIRO Ecosystem PRD & Spec Index

- **Status:** `ACTIVE_REFERENCE`
- **Last Updated:** 2026-09-05

---

## 1. Governance Contracts & Architecture Decisions

| Scope / Contract | Document Path | Status | Description |
|---|---|---|---|
| **Knowledge Continuity** | `docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_CONTRACT.md` | `CANONICAL` | KCC governance layer for Fresh AI onboarding, fact vs decision authority, and conflict resolution. |
| **Multi-Device Architecture** | `docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md` | `ACCEPTED` | ADR for hybrid multi-device access, hub-and-spoke model, and provenance metadata. |
| **Session Projection Sync** | `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md` | `CANONICAL` | Deterministic synchronization of active-session.md and current-work.md surfaces. |
| **Agent Role Contract** | `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md` | `CANONICAL` | Operational boundaries between ChatGPT (Planning), Antigravity (Executor), and WSL (Runtime). |
| **Input Processing Contract** | `docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md` | `CANONICAL` | Sustainable input intake and reconciliation rules. |
| **Acceptance Evidence Contract** | `docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md` | `CANONICAL` | Evidence-based task completion and DoD standards. |
| **Capability Discovery Gate** | `docs/contracts/AIRO_CAPABILITY_DISCOVERY_GATE_CONTRACT.md` | `CANONICAL` | Lightweight discovery checkpoint for capability creation, intent classification & tech spec rules. |
| **Product Build Workflow** | `docs/contracts/AIRO_PRODUCT_BUILD_WORKFLOW_CONTRACT.md` | `CANONICAL` | End-to-end lifecycle, Interview Protocol, Capability/PRD artifact, Design Context hook, Council integration. |

---

## 2. Project PRD & Spec Index Table

| Project / Scope | Document Path | Role / Status | Notes / Constraints |
|---|---|---|---|
| **ASB_GLOBAL** | `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md` | `OWNER_APPROVED_IMPLEMENTATION_TARGET` | Primary active canonical spec target for ASB v0.6. Links to [Design Spec](docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md). |
| **ASB_GLOBAL** | `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md` | `ACTIVE_CANONICAL` | Implemented runtime baseline, inherited by v0.6.0 until M6 cutover. |
| **ASB_GLOBAL** | `docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md` | `SUPERSEDED_ARCHIVE_REFERENCE` | Legacy spec, superseded by v0.5.1. |
| **AIRO Finance / vortex-ai-skill-lab** | `ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_WEB_APP_V2_PRD_ADDENDUM.md` | `OWNER_APPROVED_ACTIVE_PROJECT_ADDENDUM` | Owner-approved Web App V2 read-only cockpit addendum. Preserves `ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_PRD_LIVING.md` as active reference candidate. |
| **Report Automation VBA** | `docs/prd/report-automation-vba-rc4c2-baby-friendly-command-center-onboarding-ux-prd-20260615.md` | `ACTIVE_REFERENCE_CANDIDATE` | VBA onboarding spec. Project classification not fully resolved in ASB-GOV-1. |
| **D-READY** | `ecosystem/projects/d-ready/D_READY_PRD_LIVING.md` | `ACTIVE_REFERENCE_CANDIDATE` | Public-safe project contract. Excel logic prototype with Power BI target architecture. |
| **Earesmes-Arfin Bridge (EAB)** | `ecosystem/projects/earesmes-arfin-bridge/docs/01_PRD.md` | `OWNER_SCOPE_LOCKED` | EAB PRD (STATUS=SCOPE_LOCKED, OWNER_SCOPE_LOCK=APPROVED). |
| **AIRO Finance Lab** | `ecosystem/projects/airo-finance-lab/docs/AIRO_FINANCE_LAB_PRD_V1.md` | `CANONICAL_PRD` | Clean-slate personal finance architecture & PRD. Decoupled Python engine, stateless parse-and-confirm, 7-day daily value proof rule. |
| **Other Projects** | None confirmed | `PENDING_FUTURE_CLASSIFICATION` | No active canonical PRD confirmed yet. |

---

> [!WARNING]
> - `PRD_INDEX` is a pointer-only index.
> - It does NOT rewrite or supersede project PRDs or specifications unless explicitly approved.
> - In case of context or status conflict, refer to owner-approved decisions and verify using latest live evidence.
