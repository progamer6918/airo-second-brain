# AIRO Ecosystem Roadmap Index

- **Status:** `ACTIVE_REFERENCE`
- **Last Updated:** 2026-08-04

---

## 1. Roadmap Index Table

| Scope / Project | Owner-Approved Status | Roadmap Pointer | Current Status Source | Notes / Blockers |
|---|---|---|---|---|
| **ASB_GLOBAL** | `ACTIVE` | `docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md` | `docs/roadmap/AIRO_SECOND_BRAIN_v0.6_MILESTONE_TRACKER.tsv` | ASB v0.6 7-Milestone Roadmap. Active milestone: M5 — Cross-Consumer & Failure Proof (Status: NOT_YET_PROVEN). Previous: M4 (DONE). See [Design Spec](docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md). |
| **AIRO Finance / vortex-ai-skill-lab** | `ACTIVE_PHASE_4_CICILAN_RUMAH` | `ecosystem/projects/vortex-ai-skill-lab/docs/plans/AIRO_FINANCE_WEB_APP_V2_EXECUTION_SLICE_PLAN.md` | Phase 4 Cicilan Rumah Active (Gate 4.0 Docs-Only Activation) + latest runtime evidence | Owner-approved Web App V2 track (Phases 0–8). Read-only cockpit architecture. Telegram foreign-message ingestion incident is open; no finance runtime mutation is authorized by this checkpoint. |
| **finance-bot-alternatives** | `EXPERIMENT_REFERENCE` | None | Folder contents | Classified as experiment reference. |
| **earnsai-pulse-trading-local-backups** | `ARCHIVE_LOCAL_BACKUP` | None | Folder contents | Local backup archive. |
| **earnsai-telegram-gateway** | `PARKED_UNTIL_VERIFIED` | None | Folder contents | Parked until gateway operation is verified. |
| **Earesmes / Hermes** | `INCIDENT_OPEN_RUNTIME_FAILED` | None | `ecosystem/earesmes-hermes.md` + latest runtime evidence | Owner live test failed: Earesmes did not reply and the message was handled by Arfin. Root cause not yet proven. |
| **earnsai-pulse-trading** | `PARKED_RUNTIME_DEGRADED` | None | Folder contents | Parked handover. |
| **github-handover** | `ARCHIVE_HANDOVER` | None | Folder contents | Archive handover. |
| **D-READY** | `ACTIVE` | `ecosystem/projects/d-ready/docs/roadmap/D_READY_ROADMAP.md` | `ecosystem/projects/d-ready/CURRENT_STATE.md` + latest validation evidence | Stage: `PILOT_LOGIC_VALIDATION`; Power BI implementation not yet proven. |
| **Report Automation VBA** | `FROZEN_BY_OWNER` | `docs/roadmap/report-automation-vba-rc4-self-service-onboarding-roadmap.md` | `CURRENT.md` + roadmap file | Not fully classified by ASB-GOV-1. Do not overclaim. |
| **Earesmes-Arfin Bridge (EAB)** | `ACTIVE_MVP_PHASE_1_PRE_IMPLEMENTATION` | `ecosystem/projects/earesmes-arfin-bridge/docs/05_EXECUTION_ROADMAP.md` | `ecosystem/projects/earesmes-arfin-bridge/docs/MILESTONE_TRACKER.tsv` | `M0=DONE`, `M1=PASS_WITH_LIMITATIONS`, `M2=DONE`, `M3=DONE`, `M4=DONE`, `CURRENT_MILESTONE=M5`, `CURRENT_GATE=EAB_G1_4`, `IMPLEMENTATION_ALLOWED=NO`. |

---

> [!WARNING]
> - `ROADMAP_INDEX` is a pointer-only reference index.
> - It does NOT supersede project-specific runtime evidence or commit histories.
> - It does NOT normalize or restructure legacy project roadmaps.

## AIRO Finance - Dashboard Lite Re-scope Pointer

- Status: owner-approved working scope, docs-only canonicalization.
- Current target: `AIRO Finance Dashboard Lite`.
- Active workbook tab remains: `Dashboard`.
- Previous dashboard baseline: `Dashboard v2 / Gate 11B Production Baseline`.
- Canonical data contract: `ecosystem/projects/vortex-ai-skill-lab/docs/design/airo-finance-dashboard-lite-data-contract-20260704.md`.
- Scheduler: parked/off unless the Owner explicitly approves Gate 12 scheduler work.
- Next safe action: read-only Dashboard Lite mapping audit.

## Telegram Runtime Isolation Incident Checkpoint

- **Marker:** `AIRO_TELEGRAM_CROSS_PROJECT_RUNTIME_INCIDENT_ASB_CHECKPOINT_DOCS_ONLY_NO_RUNTIME_MUTATION`
- **Report Automation VBA:** `FROZEN_BY_OWNER`; removed from active execution queue until Owner reopens it.
- **Earesmes / Hermes:** `INCIDENT_OPEN_RUNTIME_FAILED`; Owner live test received no Earesmes response.
- **AIRO Finance / Arfin:** remains `ACTIVE`; `TELEGRAM_FOREIGN_MESSAGE_INGESTION_INCIDENT_OPEN` is a P0 blocker.
- **EarnsAI Pulse Trading:** `PARKED_RUNTIME_DEGRADED`.
- **EarnsAI Telegram Gateway:** `PARKED_UNTIL_VERIFIED`.
- **Root cause:** `NOT_YET_PROVEN`.
- **EARESMES_ARFIN_CLARIFICATION_BRIDGE**: `ecosystem/projects/earesmes-arfin-bridge/docs/00_PROJECT_BOOT.md` (STATUS=SCOPE_LOCKED_DOCUMENTATION_INTEGRATED, CURRENT_GATE=EAB_G0_5I, IMPLEMENTATION_ALLOWED=NO).
