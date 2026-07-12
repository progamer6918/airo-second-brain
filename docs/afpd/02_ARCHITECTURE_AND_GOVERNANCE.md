# 02_ARCHITECTURE_AND_GOVERNANCE.md

<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1-10
source_heading: CANONICAL ROADMAP LOCK
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 66-67
source_heading: 2. Final Layer Architecture
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1201-1214
source_heading: 14. Dashboard Gating Rules
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1611-1639
source_heading: 19. Rules for Future AI/Developer
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1640-1675
source_heading: 20. New Chat Bootstrap
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1676-1712
source_heading: 21. New Chat Execution Prompt
migration_status: CURRENT
conflict_id: none
-->

## Durable Architecture Overview
- **Telegram Gateway**: Dispatches inbound events.
- **Clarification Layer**: Prompts for direction, category, subcategory.
- **Review Queue Staging**: Persists pending transactions.
- **Ledger Posting**: Writes to Account Ledger after manual approval.

## Proposed Future AFPD Authority Hierarchy
- This hierarchy is proposed and not yet canonical:
  1. `AFPD.md`
  2. `00_CURRENT_HANDOFF.md`
  3. `03_ARFIN_RUNTIME_CONTRACT.md`
  4. `02_ARCHITECTURE_AND_GOVERNANCE.md`

## Documentation Update Contract
- Every substantive AIRO Finance task MUST produce a progress log entry in `10_PROGRESS_LOG.md`.
- Every defect or repair MUST produce or update an incident entry in `11_INCIDENT_REGISTER.md`.
- Every architecture decision MUST produce a decision entry in `09_DECISION_REGISTER.md`.
- Every deployment MUST record source SHA, version, deployment ID, and self-test verification.
- Every completed session MUST update `00_CURRENT_HANDOFF.md`.
- No task is considered closed until these records are fully updated.
