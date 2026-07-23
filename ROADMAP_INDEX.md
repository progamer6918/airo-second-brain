# AIRO Ecosystem Roadmap Index

- **Status:** `ACTIVE_REFERENCE`
- **Last Updated:** 2026-07-23

---

## 1. Roadmap Index Table

| Scope / Project | Owner-Approved Status | Roadmap Pointer | Current Status Source | Notes / Blockers |
|---|---|---|---|---|
| **ASB_GLOBAL** | `ACTIVE` | None yet | `CURRENT.md` + `decisions/approved/asb-gov-0c-owner-decisions-20260702.md` | Use current snapshots and decision logs until a dedicated ASB global roadmap is created. |
| **AIRO Finance / vortex-ai-skill-lab** | `ACTIVE` | `ecosystem/projects/vortex-ai-skill-lab/docs/plans/AIRO_FINANCE_WEB_APP_V2_EXECUTION_SLICE_PLAN.md` | AFPD current handoff + Web App V2 PRD addendum + latest runtime evidence | Owner-approved Web App V2 track (Phases 0–8). Read-only cockpit architecture. Telegram foreign-message ingestion incident is open; no finance runtime mutation is authorized by this checkpoint. |
| **finance-bot-alternatives** | `EXPERIMENT_REFERENCE` | None | Folder contents | Classified as experiment reference. |
| **earnsai-pulse-trading-local-backups** | `ARCHIVE_LOCAL_BACKUP` | None | Folder contents | Local backup archive. |
| **earnsai-telegram-gateway** | `PARKED_UNTIL_VERIFIED` | None | Folder contents | Parked until gateway operation is verified. |
| **Earesmes / Hermes** | `INCIDENT_OPEN_RUNTIME_FAILED` | None | `ecosystem/earesmes-hermes.md` + latest runtime evidence | Owner live test failed: Earesmes did not reply and the message was handled by Arfin. Root cause not yet proven. |
| **earnsai-pulse-trading** | `PARKED_RUNTIME_DEGRADED` | None | Folder contents | Parked handover. |
| **github-handover** | `ARCHIVE_HANDOVER` | None | Folder contents | Archive handover. |
| **D-READY** | `ACTIVE` | `ecosystem/projects/d-ready/docs/roadmap/D_READY_ROADMAP.md` | `ecosystem/projects/d-ready/CURRENT_STATE.md` + latest validation evidence | Stage: `PILOT_LOGIC_VALIDATION`; Power BI implementation not yet proven. |
| **Report Automation VBA** | `FROZEN_BY_OWNER` | `docs/roadmap/report-automation-vba-rc4-self-service-onboarding-roadmap.md` | `CURRENT.md` + roadmap file | Not fully classified by ASB-GOV-1. Do not overclaim. |

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



## Telegram Runtime Isolation Incident Checkpoint — 2026-07-23
- **Marker:** `AIRO_TELEGRAM_CROSS_PROJECT_RUNTIME_INCIDENT_ASB_CHECKPOINT_DOCS_ONLY_NO_RUNTIME_MUTATION`
- **Report Automation VBA:** `FROZEN_BY_OWNER`; removed from the active execution queue until the Owner reopens it.
- **Earesmes / Hermes:** `INCIDENT_OPEN_RUNTIME_FAILED`; Owner live test received no Earesmes response and the message was handled by Arfin.
- **AIRO Finance / Arfin:** remains `ACTIVE`; `TELEGRAM_FOREIGN_MESSAGE_INGESTION_INCIDENT_OPEN` is a P0 runtime-isolation blocker.
- **EarnsAI Pulse Trading:** `PARKED_RUNTIME_DEGRADED`; repeated startup banners do not prove paper-engine continuity.
- **EarnsAI Telegram Gateway:** remains `PARKED_UNTIL_VERIFIED`; consumer ownership and routing require read-only forensic proof.
- **Root cause:** `NOT_YET_PROVEN`.
- **Next gate:** `AIRO_TELEGRAM_MULTI_BOT_TOPOLOGY_SCHEDULER_AND_ROUTING_FORENSIC_READ_ONLY_NO_MUTATION`.
