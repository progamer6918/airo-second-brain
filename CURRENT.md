
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Current State
Active Focus
AIRO Second Brain: being upgraded into a shared canonical knowledge base / AIRO Kernel.
Earesmes/Hermes: local WSL AI agent via Telegram, intended as the main local operator node.
AIRO Finance: active project, but canonical status lives in the vortex-ai-skill-lab repo.
Owner Preferences Quick Reference
Owner-facing communication: Bahasa Indonesia.
Preferred execution style: safe, explicit, no hallucinated status.
Coding skill assumption: owner is beginner; commands must be copy-paste friendly.
Do not overwrite local changes without approval.
Do not claim PASS or DONE without evidence.
Distill knowledge; do not dump raw chat into canonical files.
Different consumers should behave as one AIRO operator across tools.
Current Architecture Decision

AIRO Second Brain is not a raw transcript dump.

Use this layer model:

inbox/ = session closeout capture.
state/ = current active context.
decisions/ = final and pending decisions.
projects/ = project pointers and summaries.
identity/, systems/, agents/, meta/ = stable operating knowledge.
Read Next
For owner preferences: identity/working-principles.md
For project list: projects/_index.md
For execution rules: AGENTS.md
For safety rules: SECURITY.md
For AIRO Finance: projects/airo-finance.md, then canonical repo docs

For Earesmes/Hermes: projects/earesmes-hermes.md
<!-- AIRO:REPORT_AUTOMATION_VBA_CURRENT -->

## Active Workstream: Report Automation VBA

Primary active workstream: Report Automation VBA.

Relevant project file:

- `projects/report-automation-vba.md`

Related registry:

- `systems/repository-registry.md`

Current focus:

- Stabilize Excel/VBA Command Center report automation.
- Preserve the confirmed R4/R5 Monitoring Dealer baseline.
- Extend the same `SALES_5PIVOT` engine to Report Per Type with formula-safe handling.
- Focus on Automated Template Onboarding and Mapping Engine (Result VE is only the first proof case).

Current rule:

AIRO Second Brain is the canonical knowledge hub. Repository-specific work may live in other repos, but durable operator context should be summarized or linked from this repo.

- **Status:** OPERATIONAL_COMPLETE.
- **Next Step:** Normal Operation (Scheduler hidden via VBS, Telegram active/quiet).

<!-- AIRO:REPORT_AUTOMATION_VBA_CURRENT:BEGIN -->
## Active Workstream: Report Automation VBA

- Canonical project: `projects/report-automation-vba.md`.
- Current baseline: R8.11 `FROZEN STABLE BASELINE`; reopen persistence PASS.
- RPT001 Monitoring Dealer: PASS.
- RPT002 Report Per Type: runtime and business-output PASS.
- RPT003 Result VE: `MAPPING_REQUIRED`, disabled, not processed.
- Active next milestone: Automated Template Onboarding and Mapping Engine (Result VE is only proof case).
- Protect R8.11; future work uses copied candidate workbook/module.
<!-- AIRO:REPORT_AUTOMATION_VBA_CURRENT:END -->
