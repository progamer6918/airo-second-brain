# 01_PROJECT_CHARTER.md

<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 11-18
source_heading: AIRO Finance Command Center - Final Kitab v2
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 19-50
source_heading: 0. Executive Decision
migration_status: CURRENT
conflict_id: AUTHORITY_FINAL_KITAB_VS_ARFIN
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 51-65
source_heading: 1. Core Principles
migration_status: CURRENT
conflict_id: none
-->

## Project Purpose
The purpose of the AIRO Finance Project is to establish a secure, multi-tab transaction intake system linked to Google Sheets via Telegram bot and Gmail poller, ensuring accurate ledger updates and transaction categorizations.

## Owner-Approved Operating Principles
1. **Financial Safety**: The system MUST NOT execute automated ledger writes without Owner approval for staged items.
2. **Clarification-First Behavior**: Mismatched or ambiguous items MUST trigger clarification flows instead of writing default fallback data.
3. **No Speculative Reset**: Developers/AI MUST NOT redesign the core architecture from zero without explicit Owner approval.

## Product Boundary
- **Input Channels**: Telegram bot and Gmail poller.
- **Output Target**: Reconciled workbook (`Account Ledger`, `Credit Card`, `Hutang`, `Aset`, `Cicilan Rumah`).

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

# 03_ARFIN_RUNTIME_CONTRACT.md

<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 1-6
source_heading: ARFIN
migration_status: CURRENT
conflict_id: AUTHORITY_FINAL_KITAB_VS_ARFIN
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 7-12
source_heading: Read First
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 13-42
source_heading: Telegram UX
migration_status: CURRENT
conflict_id: LEGACY_ALPHA_UX_VS_NUMERIC_UX
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 43-67
source_heading: Email Flow
migration_status: CURRENT
conflict_id: EMAIL_DEFAULT_OFF_VS_ACTIVE_RUNTIME
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 68-103
source_heading: Direction
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 104-117
source_heading: Category
migration_status: CURRENT
conflict_id: LEGACY_ALPHA_UX_VS_NUMERIC_UX
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 118-131
source_heading: Admin
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 132-150
source_heading: Review Queue
migration_status: CURRENT
conflict_id: REVIEW_QUEUE_FALLBACK_VS_APPROVAL_STAGING
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 151-187
source_heading: Approval
migration_status: CURRENT
conflict_id: REVIEW_QUEUE_FALLBACK_VS_APPROVAL_STAGING
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 188-206
source_heading: Ledger
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 207-224
source_heading: Tests
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ARFIN.md
source_lines: 225-236
source_heading: Forbidden
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 122-141
source_heading: 3. Clarification Layer
migration_status: MERGED
conflict_id: LEGACY_ALPHA_UX_VS_NUMERIC_UX
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 142-159
source_heading: 3.1 Mandatory Ambiguity Types
migration_status: MERGED
conflict_id: LEGACY_ALPHA_UX_VS_NUMERIC_UX
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 160-174
source_heading: 3.2 Missing Category Policy
migration_status: MERGED
conflict_id: LEGACY_ALPHA_UX_VS_NUMERIC_UX
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 175-193
source_heading: 3.3 Critical Missing Fields
migration_status: MERGED
conflict_id: LEGACY_ALPHA_UX_VS_NUMERIC_UX
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 194-245
source_heading: 4. Email-to-Telegram Clarification Bridge
migration_status: MERGED
conflict_id: REVIEW_QUEUE_FALLBACK_VS_APPROVAL_STAGING
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 246-249
source_heading: 5. Email Security Policy
migration_status: MERGED
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 250-256
source_heading: 5.1 Default Mode
migration_status: MERGED
conflict_id: EMAIL_DEFAULT_OFF_VS_ACTIVE_RUNTIME
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 257-270
source_heading: 5.2 Allowed v1 Behavior
migration_status: MERGED
conflict_id: EMAIL_DEFAULT_OFF_VS_ACTIVE_RUNTIME
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 271-305
source_heading: 5.3 Sensitive Email Hard-Block
migration_status: MERGED
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 306-343
source_heading: 6. Router Policy
migration_status: MERGED
conflict_id: REVIEW_QUEUE_FALLBACK_VS_APPROVAL_STAGING
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 729-765
source_heading: 8. Partial Write Recovery
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 766-767
source_heading: 9. Reconciliation
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 768-782
source_heading: 9.1 Light Reconciliation
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 783-814
source_heading: 9.2 Full Reconciliation
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1215-1264
source_heading: 15. Proactive Telegram Alert Engine
migration_status: CURRENT
conflict_id: none
-->

## Active Runtime Contract
1. **Admin Preemption**: Admin commands MUST preempt any pending transaction clarification handler. Commands include:
   - `admin cek pending`
   - `admin clear pending clarification`
   - `/approval`
   - `/admin`
2. **Clear Command**: `admin clear pending clarification` is the canonical command to reset pending clarification states without mutations to the ledger or Review Queue.
3. **Ingestion Staging**: All resolved email transactions MUST be staged in the Review Queue under `APPROVAL_STAGING` and require explicit Owner approval via Telegram bot before any ledger posting.
4. **Outgoing Email Flow**: Direction -> Funding Account -> Category -> Subcategory -> Review Queue Staging -> Approval -> Ledger.
5. **Numeric Prompts**: Prompt menus and parsers MUST use numeric options (`1..N` for options and `0` for `Other / Review`). Letters A/B/C/D/E are legacy and MUST NOT be displayed in prompts.

### Timezone Discrepancy (SCRIPT_TIMEZONE_VS_POLLER_TIMEZONE)
The script uses Asia/Jakarta timezone for business calendar dates while the manifest is configured to Asia/Bangkok. This discrepancy is currently an unresolved normalization issue documented under trigger topology.

# 04_RUNTIME_TOPOLOGY.md

<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 68-75
source_heading: Layer 1 - Input Sources
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 76-89
source_heading: 2.1 Telegram Input
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 90-107
source_heading: 2.2 Email Notification Input
migration_status: CURRENT
conflict_id: EMAIL_DEFAULT_OFF_VS_ACTIVE_RUNTIME
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 108-121
source_heading: 2.3 Future Bank Mutation Input
migration_status: CURRENT
conflict_id: none
-->

## Apps Script Source Inventory
- **Active Handler File**: `AIRO_Finance_Multitab_Final_v1.js` is the sole entry point handling doPost.
- **Neutralized Compatible Source**: `Kode.js` contains a neutralized legacy doPost redirecting to the active handler to maintain compatibility.
- **Active doPost count in Kode.js**: 0.

## Webhook and Poller Topology
- **Telegram Webhook**: Registers bot tokens and dispatches user texts.
- **Gmail Ingestion Poller**: Triggered hourly to query Gmail messages.
- **State Storage**: Chat states are stored in properties with key prefix `AIRO_PENDING_CLARIFICATION_<chat_id>`.

## Timezone Normalization Issue
- The script manifest `appsscript.json` specifies `Asia/Bangkok`, while internal script logic calculates times using `Asia/Jakarta`. This remains a known discrepancy.

# 05_STATE_MACHINES.md

## Intake Flow States
- **email_outgoing_account_pending**: Awaiting funding account selection.
- **category_pending / category_expense**: Awaiting category mapping index.
- **category_search_pending**: Resolving category queries.
- **subcategory_pending**: Awaiting subcategory selection index.
- **direction_pending**: Awaiting selection between Pemasukan, Pengeluaran, or Transfer.
- **Review Queue Approval Staging**: Transaction parsed but awaiting manual approval.
- **Manual-Review Fallback**: Clarification failed or timed out; awaits manual corrections.
- **Approval Commit**: Staged transaction posted to ledger.
- **Reject Flow**: Item marked discarded.
- **Pending Removal**: Property state cleared.
- **Last-Prompt Pointer Arbitration**: Disambiguation tracking.

## Core Distinctions
- **Clarification Pending**: Temporary state in Properties Service before write.
- **Manual-Review Fallback**: Review Queue row marked with `issue_reason` fallback status.
- **Approval Staging**: Review Queue row with `pending` status awaiting `/approval`.
- **Committed Transaction**: Transaction finalized in Account Ledger.

# 06_DATA_AND_WORKBOOK_CONTRACTS.md

<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 344-345
source_heading: 7. Data Tabs
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 346-422
source_heading: 7.1 Account Ledger
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 423-451
source_heading: 7.2 Credit Card
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 452-475
source_heading: 7.3 Hutang
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 476-501
source_heading: 7.4 Aset
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 502-527
source_heading: 7.5 Cicilan Rumah
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 528-633
source_heading: 7.6 Finance Events
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 634-654
source_heading: 7.7 Review Queue
migration_status: MERGED
conflict_id: REVIEW_QUEUE_FALLBACK_VS_APPROVAL_STAGING
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 655-693
source_heading: 7.8 Audit Log
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 694-728
source_heading: 7.9 Email Ingestion Log
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 815-824
source_heading: 10. Data Status
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 825-835
source_heading: Trusted
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 836-846
source_heading: Warning
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 847-863
source_heading: Dirty
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 864-906
source_heading: 11. Net Worth Policy
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 907-930
source_heading: 12. Dashboard Final Vision
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 931-955
source_heading: 12.1 Visual Principles
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 956-969
source_heading: 12.2 Dashboard Layout
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 970-990
source_heading: 12.3 Topbar
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 991-1014
source_heading: 12.4 Action Required
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1015-1042
source_heading: 12.5 Executive Command Center
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1043-1066
source_heading: 12.6 Wallet & Cashflow Board
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1067-1088
source_heading: 12.7 Domain Health
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1089-1108
source_heading: 12.8 Spending Intelligence
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1109-1138
source_heading: 12.9 Data Quality Center
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1139-1153
source_heading: 12.10 Smart Insight Panel
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1154-1178
source_heading: 12.11 Conditional Email Ingestion Status
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1179-1200
source_heading: 13. Metric Source of Truth
migration_status: CURRENT
conflict_id: none
-->

## Review Queue Semantic Statuses
The Review Queue sheet columns AE through AH MUST distinguish between:
1. `MANUAL_REVIEW_FALLBACK`: Written when a parser fails, category is missing, or clarification times out. Marked with specific error tags in `issue_reason`.
2. `APPROVAL_STAGING`: Normal resolved flow (e.g., from email notifications) staging transactions with complete properties awaiting Owner approval.

# 07_OPERATIONS_DEPLOYMENT_TRIGGERS.md

## Deployment Safety
- **Source SHA Guards**: Verify file hashes locally before clasp push.
- **Immutable Versioning**: Create version descriptions matching `AIRO_ARFIN_BRIDGE_PERSISTENCE_V1_<timestamp>`.
- **Triggers Verification**: Checks if triggers like `processReviewQueueApprovedOnEdit` exist.
- **Rollback Routine**: Restores version to previous stable version (e.g., 365) if self-test fails.

*Note: No deployment operations were executed in this documentation-only phase.*

# 08_ROADMAP.md

<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1320-1321
source_heading: 18. Final Roadmap
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1322-1355
source_heading: Sprint 0A - Telegram Clarification Closure
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1356-1382
source_heading: Sprint 0B - Email Ambiguity Research & Bridge Design
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1383-1410
source_heading: Sprint 1 - Account Ledger Hardening
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1411-1434
source_heading: Sprint 2 - Domain Tabs Maturation
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1435-1459
source_heading: Sprint 3 - Cash Ledger Removal
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1460-1491
source_heading: Sprint 4 - Finance Events v1
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1492-1517
source_heading: Sprint 5 - Audit, Reconciliation, Partial Recovery
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1518-1554
source_heading: Sprint 6 - Dashboard Final
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1555-1580
source_heading: Sprint 6B - Proactive Telegram Alert Engine v1
migration_status: HISTORICAL
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 1581-1610
source_heading: Sprint 7 - Email Ingestion v1, Outline Only
migration_status: HISTORICAL
conflict_id: none
-->

## Active Roadmap
The current roadmap from the Living PRD defines active tasks:
- **Task 10.1**: Documentation reconciliation (Gate 12) IN_PROGRESS.
- **Task 10.2**: Deploy filter dropdown fix (Gate 11) PASS.

## Historical Sprints
- Sprint 0A through Sprint 7 are legacy records of completed features and MUST NOT be used for active task sequences.

# 09_DECISION_REGISTER.md

## Durable Decision Records
- **AFPD Proposed Authority Hierarchy**: Initiated Phase 3 skeleton creation to replace split authority between Final Kitab and ARFIN.md once canonical activation is granted.
- **Final Kitab Preservation**: Final Kitab is preserved unchanged during documentation migrations to maintain historical stability.
- **ARFIN Runtime Contract Integration**: Merged ARFIN.md behavior and Final Kitab rules in module 03.
- **Review Queue Dual Semantics**: Separate status mappings for Manual-Review Fallback and Approval Staging.
- **Numeric UX Prompts**: Prompts upgraded to numeric indexes (`1..N`, `0`). Alpha A-E remains legacy/unresolved.
- **Timezone Normalization Deferred**: Jakarta business timezone is active in script; Bangkok manifest timezone normalization is deferred.

# 11_INCIDENT_REGISTER.md

## Incidents Register

### Incident 1 — Old A/B/C/D/E Email Prompt at 08:51
- **incident_id**: INC_001
- **detected_at**: 2026-07-12 08:51 UTC
- **symptom**: Email expense prompts still displayed A/B/C/D/E letters instead of numeric options.
- **impact**: Confused users expecting the numeric Arfin prompt interface.
- **root_cause**: Legacy webhook endpoint connected to an unpatched development environment.
- **repair**: Forensic isolation of the webhook, routing to active multitab handler.
- **verification**: Check transaction triggers.
- **status**: RESOLVED
- **related_versions**: v370
- **related_evidence**: 08:51 runtime log capture
- **remaining_risk**: Inactive legacy endpoints.

### Incident 2 — Account Reply "2" Not Routed
- **incident_id**: INC_002
- **detected_at**: 2026-07-10 12:50 UTC
- **symptom**: Replying with numeric option "2" failed to resolve.
- **impact**: Blocked account resolution for selected option.
- **root_cause**: Parser checked string arrays instead of normal category strings.
- **repair**: Convert replies to strings before registry array parsing.
- **verification**: Selftest check cases.
- **status**: RESOLVED
- **related_versions**: v371
- **related_evidence**: test case `numeric_account_ux`
- **remaining_risk**: Array bounds check issues.

### Incident 3 — Typed "Blu Pocket" Resolving as "Blu"
- **incident_id**: INC_003
- **detected_at**: 2026-07-10 13:12 UTC
- **symptom**: User input "Blu Pocket" matched substring "Blu" instead of full name.
- **impact**: Routed transaction funding from wrong account.
- **root_cause**: Substring regex checked before exact match registry parser.
- **repair**: Shift exact match checks to higher priority level.
- **verification**: Selftest validation.
- **status**: RESOLVED
- **related_versions**: v374
- **related_evidence**: v374 diff
- **remaining_risk**: Regex greedy matching.

### Incident 4 — Expense Category "0" Fall-Through
- **incident_id**: INC_004
- **detected_at**: 2026-07-10 13:20 UTC
- **symptom**: Expense category "0" falling through parser before v375 and posting to ledger.
- **impact**: Data mapping pollution in Account Ledger.
- **root_cause**: Category parser missing strict validation block for "0" review route.
- **repair**: Direct category "0" explicitly to Review Queue fallback.
- **verification**: Staging selftest validation.
- **status**: RESOLVED
- **related_versions**: v375
- **related_evidence**: v375 test logs
- **remaining_risk**: Other fall-through keys.

### Incident 5 — Split Authority (Final Kitab vs ARFIN.md)
- **incident_id**: INC_005
- **detected_at**: 2026-07-12 09:40 UTC
- **symptom**: Split claims of canonical guidance between the two docs.
- **impact**: Ambiguity for developers updating codebase.
- **root_cause**: Reconciliations not unified in previous sessions.
- **repair**: Create unified AFPD modules (docs/afpd/).
- **status**: IN_PROGRESS
- **related_versions**: Phase 2/3
- **related_evidence**: Contradiction Matrix
- **remaining_risk**: Inactive activation stubs.

### Incident 6 — Missing Durable v371-v375 Documentation
- **incident_id**: INC_006
- **detected_at**: 2026-07-12 09:45 UTC
- **symptom**: Version changes absent from main documentation files.
- **impact**: Lack of traceability for past patches.
- **root_cause**: Rapid hotfixing bypass of documentation updates.
- **repair**: Backfill progress log entries in Phase 3.
- **status**: RESOLVED
- **related_versions**: Phase 3
- **related_evidence**: Progress log backfill plan
- **remaining_risk**: None.

### Incident 7 — Manifest Timezone vs Business Timezone
- **incident_id**: INC_007
- **detected_at**: 2026-07-12 09:48 UTC
- **symptom**: appsscript.json manifest timezone discrepancy.
- **impact**: Deployed times in GCP mismatched with local Jakarta times.
- **root_cause**: Manifest left at default Asia/Bangkok while code uses Asia/Jakarta.
- **repair**: Documented unresolved discrepancy in trigger topology. Normalization deferred.
- **status**: UNRESOLVED
- **related_versions**: Phase 3
- **related_evidence**: appsscript.json manifest
- **remaining_risk**: Date conversion offsets in logs.

### Incident 8 — Undercounted Phase 4 Normative Extractor
- **incident_id**: AFPD-INC-008
- **detected_at**: 2026-07-12 10:12 WIB
- **symptom**: Phase 4 declared readiness using an undercounted normative extractor.
- **impact**: Canonical activation could have occurred with missing rules.
- **root_cause**: Audit implementation used selected or hardcoded rules instead of the full dynamic baseline.
- **repair**: Independent extraction and full normative remediation mapping 377 rules.
- **verification**: Phase 4.2 post-remediation audit.
- **status**: OPEN until Phase 4.3 PASS
- **related_versions**: Phase 4/4.1/4.2
- **related_evidence**: /tmp/airo_afpd_phase4_1_20260712_101527
- **remaining_risk**: Gaps in newly appended sections.

### Incident 8 Update — Undercounted Phase 4 Normative Extractor
- **incident_id**: AFPD-INC-008
- **detected_at**: 2026-07-12 10:12 WIB
- **status**: OPEN (Pending Phase 4.5 independent semantic re-audit)

### Incident 9 — Manual Telegram Resolution Bypassed Review Queue

- **incident_id**: AFPD-INC-009
- **detected_at**: 2026-07-12, Owner-reported Telegram transaction flow
- **symptom**: After manual account and subcategory selection, Arfin reported success and changed ledger state without Review Queue approval.
- **impact**: Premature ledger mutation, false-success messaging, and possible loss of execution-account versus funding-account semantics.
- **root_cause**: `airoHandleOutgoingConfirmationReply_` called `writeRouted_` directly in the resolved-subcategory branch and cleared pending state before governed staging/readback.
- **repair**: Replace direct ledger write with `telegram_manual` approval staging, source-scoped approval guards, deterministic dedupe identity, category-scoped prompts, and posting-plan metadata restoration.
- **repository_source_commit**: `22caa64774977fdedcd5ae8555e3c805b20feac8`
- **source_sha256**: `aca69b3750ce63ce2015ce416880d9b225e704166f8b030a9783623056a93b52`
- **stable_patch_id**: `1d3c4a7f0a88efc4ccce2bb22fa3d0351e3baea5`
- **verification**: Independent semantic review, content-equivalence audit, syntax validation, same-account 1-row test, funded-payment 3-row test, and repeat-approval zero-extra-row test.
- **status**: REPAIR_INTEGRATED_NOT_DEPLOYED
- **production_resolution**: PENDING
- **related_evidence**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642.md`
- **remaining_risk**: Apps Script deployment parity and live Telegram/workbook behavior remain unproven.
- **next_gate**: Owner-authorized Gate P2 deployment and production runtime/readback proof.

#### `AFPD-INC-009` Gate P1.1 update — self-test contract aligned

- **Timestamp**: 2026-07-13 19:17:45 WIB
- **Marker**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1`
- **Source repair commit**: `36bb37c228999efedaeb3ee305e03354f54cbf1a`
- **Change**: Added `plannedPostingRowCount` to the resolved dry-run and replaced stale pre-approval `rowCount === 3/1` assertions.
- **Runtime implementation changed**: NO
- **Built-in self-test result**: PASS
- **Deployment performed**: NO
- **Incident status**: REPAIR_INTEGRATED_NOT_DEPLOYED
- **Evidence**: `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745.md`

- 2026-07-19: Repaired Gate P1.2 self-test harness dependency alignment (`AIRO_ARFIN_SELFTEST_HARNESS_REPAIR_P1_2`). Self-test pass rate: 17/17.

- 2026-07-19: Documented Gate P2 rollback status and runtime failure evidence (`AIRO_ARFIN_GATE_P2_ROLLBACK_STATUS_AND_FAILURE_EVIDENCE`). Rollback confirmed to version 377.

- 2026-07-19: Documented Gate P2 runtime failure RCA (`AIRO_ARFIN_GATE_P2_RUNTIME_FAILURE_RCA_NO_DEPLOY`). Classification: `CLASP_RUN_CONTEXT_NOT_AUTHORIZED_FOR_SCRIPT_FUNCTION`.

- 2026-07-19: Formulated Gate P2 clasp runtime permission remediation plan (`AIRO_ARFIN_GATE_P2_CLASP_RUNTIME_PERMISSION_REMEDIATION_NO_DEPLOY`). Route: `OWNER_ENABLE_APPS_SCRIPT_API_AND_EXECUTION_API_CONTEXT`.

- 2026-07-19: Documented Gate P2 runtime proof method decision (`AIRO_ARFIN_GATE_P2_RUNTIME_PROOF_METHOD_DECISION_NO_DEPLOY`). Decision: `MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS`.

- 2026-07-19: Executed Gate P2 guarded deployment retry to version `379` (`AIRO_ARFIN_GATE_P2_GUARDED_DEPLOYMENT_RETRY_EXECUTION_MANUAL_RUNTIME_PROOF_METHOD`). Awaiting post-deploy manual editor runtime proof.

- 2026-07-19: Documented post-deploy manual editor runtime proof for version 379 (`AIRO_ARFIN_GATE_P2_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`). Status: PASS 17/17.

# 12_EVIDENCE_INDEX.md

## Phase Evidence Index

### Phase 1 Audit Artifacts
- `/tmp/airo_afpd_phase1_20260712_094619/AFPD_READINESS_REPORT.md` (readiness)
- `/tmp/airo_afpd_phase1_20260712_094619/AFPD_DOCUMENT_INVENTORY.csv` (inventory)
- `/tmp/airo_afpd_phase1_20260712_094619/AFPD_CONTRADICTION_MATRIX.tsv` (contradictions)

### Phase 1.5 Blocker Artifacts
- `/tmp/airo_afpd_phase1_5_20260712_094937/AFPD_PHASE1_5_EXACT_BLOCKERS.txt` (blockers txt)
- `/tmp/airo_afpd_phase1_5_20260712_094937/AFPD_PHASE1_5_EXACT_BLOCKERS.json` (blockers json)

### Phase 2 Documents & Commit
- `docs/afpd/AFPD_MIGRATION_MANIFEST.md`
- `docs/afpd/AFPD_AUTHORITY_MATRIX.md`
- `docs/afpd/AFPD_SECTION_DESTINATION_MAP.tsv`
- Commit: `a675395` (push success)

### v371-v375 Deployment & Runtime Evidence
- **Source SHA**: `dde3e8cec69ef45d33e7e54a6a4e16ee07084a3016f73c7b02d6d169eee4947d`
- **Self-Test Result**: `LOCAL_SELFTEST=PASS` (8 cases passed)

### Live Intake & Approval Proofs
- **Live Rp1 Other / Review Staging Proof**:
  - `SESSION_EVIDENCE_NEEDS_DURABLE_CAPTURE` (exists in session stdout)
- **Live Rp205.000 Utilities / Internet Approval Proof**:
  - `SESSION_EVIDENCE_NEEDS_DURABLE_CAPTURE` (exists in session stdout)
- **Account Ledger Row 169 Dedupe PASS**:
  - `SESSION_EVIDENCE_NEEDS_DURABLE_CAPTURE` (deduplication check passed)
### Phase 4.2 Hardened Evidence
- `docs/evidence/airo-finance/AFPD_OWNER_PROVIDED_TELEGRAM_TRANSCRIPTS_20260712.md`
- `docs/evidence/airo-finance/AFPD_PRODUCTION_DEPLOYMENT_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_TRIGGER_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_WORKBOOK_ROW169_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_REVIEW_QUEUE_RP1_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_OWNER_PROVIDED_TELEGRAM_TRANSCRIPTS_20260712.md`
- `docs/evidence/airo-finance/AFPD_PRODUCTION_DEPLOYMENT_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_TRIGGER_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_WORKBOOK_ROW169_READBACK_20260712_102116.md`
- `docs/evidence/airo-finance/AFPD_REVIEW_QUEUE_RP1_READBACK_20260712_102116.md`

### ARFIN Manual Approval Staging — Gate P1

- **Incident**: `AFPD-INC-009`
- **Source integration commit**: `22caa64774977fdedcd5ae8555e3c805b20feac8`
- **Stable patch ID**: `1d3c4a7f0a88efc4ccce2bb22fa3d0351e3baea5`
- **Source SHA-256**: `aca69b3750ce63ce2015ce416880d9b225e704166f8b030a9783623056a93b52`
- **Packet archive SHA-256**: `28440fe31df503959aca551382336ba962cea9eda41a22f0857db2122f52f6c7`
- **Integration evidence**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642.md`
- **Independent semantic review**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642_INDEPENDENT_REVIEW.md`
- **Executable results**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642_EXECUTABLE_RESULTS.json`
- **Fresh/content verification**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642_FRESH_VERIFICATION.txt`
- **Deployment evidence**: NOT YET AVAILABLE
- **Workbook readback evidence**: NOT YET AVAILABLE

### ARFIN Gate P1.1 — self-test contract repair

- **Marker**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1`
- **Incident**: `AFPD-INC-009`
- **Source repair commit**: `36bb37c228999efedaeb3ee305e03354f54cbf1a`
- **Summary**: `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745.md`
- **Static review**: `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745_STATIC_REVIEW.md`
- **Executable results**: `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745_EXECUTABLE_RESULTS.json`
- **Executable harness**: `docs/evidence/airo-finance/AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1_20260713_191745_HARNESS.js`
- **Apps Script deployment evidence**: NOT YET AVAILABLE

- 2026-07-19: Repaired Gate P1.2 self-test harness dependency alignment (`AIRO_ARFIN_SELFTEST_HARNESS_REPAIR_P1_2`). Self-test pass rate: 17/17.

- 2026-07-19: Documented Gate P2 rollback status and runtime failure evidence (`AIRO_ARFIN_GATE_P2_ROLLBACK_STATUS_AND_FAILURE_EVIDENCE`). Rollback confirmed to version 377.

- 2026-07-19: Documented Gate P2 runtime failure RCA (`AIRO_ARFIN_GATE_P2_RUNTIME_FAILURE_RCA_NO_DEPLOY`). Classification: `CLASP_RUN_CONTEXT_NOT_AUTHORIZED_FOR_SCRIPT_FUNCTION`.

- 2026-07-19: Formulated Gate P2 clasp runtime permission remediation plan (`AIRO_ARFIN_GATE_P2_CLASP_RUNTIME_PERMISSION_REMEDIATION_NO_DEPLOY`). Route: `OWNER_ENABLE_APPS_SCRIPT_API_AND_EXECUTION_API_CONTEXT`.

- 2026-07-19: Documented Gate P2 runtime proof method decision (`AIRO_ARFIN_GATE_P2_RUNTIME_PROOF_METHOD_DECISION_NO_DEPLOY`). Decision: `MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS`.

- 2026-07-19: Executed Gate P2 guarded deployment retry to version `379` (`AIRO_ARFIN_GATE_P2_GUARDED_DEPLOYMENT_RETRY_EXECUTION_MANUAL_RUNTIME_PROOF_METHOD`). Awaiting post-deploy manual editor runtime proof.

- 2026-07-19: Documented post-deploy manual editor runtime proof for version 379 (`AIRO_ARFIN_GATE_P2_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`). Status: PASS 17/17.

# 99_HISTORICAL_AND_SUPERSEDED.md

## Superseded and Historical Materials

### Legacy Canonical Roadmap Lock
- Preserved historical lock metadata from Sprint 6/7.

### Email Default-OFF Policy
- Historical security modes specifying ingestion poller default de-activated.

### Deprecated Cash Ledger and Transactions Tab
- Specifications for the old `Cash Ledger` and `Transactions` sheets, which were removed/neutralized in Sprint 3 in favor of a single Account Ledger database.

### Legacy A/B/C/D/E prompt layouts
- Early prompts asking for direction, category, or subcategory options using letters instead of numeric options.

### Fallback-Only Review Queue Interpretation
- The earlier interpretation that Review Queue was only used as a fallback error pool rather than a normal staging pool.

# 10_PROGRESS_LOG.md

## Version History Logs

### Version v371 — Admin Preemption Behavior
- **Timestamp**: 2026-07-10 12:49:50 UTC
- **Problem**: Admin commands were swallowed by pending clarification handlers.
- **Root Cause**: Reply checks ran before command preemption evaluations.
- **Decision**: Inject command checks at top of text processors.
- **Source SHA Before**: `2090aec170cfc0279996dee6e158a5b56f005aeb38fa436a4112e88e9d8a2e7f`
- **Source SHA After**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Apps Script Version**: 366
- **Deployment Fingerprint**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Functions Changed**: `tryHandlePendingClarificationReply_`
- **Tests**: `airoArfinRuntimeAlignV1SelfTest_()`
- **Live Proof**: Command `admin cek pending` succeeds during active prompt.
- **Workbook Proof**: No workbook writes.
- **Mutation Summary**: Added regex command bypass.
- **Remaining Risk**: Command name updates.
- **Next Step**: Document bypass checks.

### Version v372 — Poller Window & Email Prompt Ownership
- **Timestamp**: 2026-07-10 13:00:15 UTC
- **Problem**: Duplicate email ingestion logs.
- **Root Cause**: Greedy queries without caching processed threads.
- **Decision**: Cache processed thread IDs in script properties.
- **Source SHA Before**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Source SHA After**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Apps Script Version**: 367
- **Deployment Fingerprint**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Functions Changed**: `pollGmailNotifications_`
- **Tests**: Dry-run Gmail checks.
- **Live Proof**: Process times <500ms.
- **Workbook Proof**: Ingestion log rows added correctly.
- **Mutation Summary**: Property-based thread tracker.
- **Remaining Risk**: Property size limits.
- **Next Step**: Add thread key pruning.

### Version v373 — Pending Ownership & Pointer Arbitration
- **Timestamp**: 2026-07-10 13:10:17 UTC
- **Problem**: Concurrent chats overwriting pending states.
- **Root Cause**: Global property key instead of namespaced chat key.
- **Decision**: Prefix chat-level states with chat IDs.
- **Source SHA Before**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Source SHA After**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Apps Script Version**: 368
- **Deployment Fingerprint**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Functions Changed**: `savePendingClarification_`
- **Tests**: Parallel simulator.
- **Live Proof**: Verified independent chat flows.
- **Workbook Proof**: No workbook writes.
- **Mutation Summary**: Namespaced properties keys.
- **Remaining Risk**: Cache cleanup delays.
- **Next Step**: Add automatic sweeps.

### Version v374 — Account Parser Repair & Exact Name Precedence
- **Timestamp**: 2026-07-10 13:18:21 UTC
- **Problem**: Custom names matching sub-strings of other accounts.
- **Root Cause**: Index prefix matches ran before exact registry matches.
- **Decision**: Validate exact matches first before calling substring checks.
- **Source SHA Before**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Source SHA After**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Apps Script Version**: 369
- **Deployment Fingerprint**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Functions Changed**: `parseAccount_`
- **Tests**: Exact name match cases.
- **Live Proof**: Typed `Blu Pocket` resolves exactly to `Blu Pocket`, not substring `Blu`.
- **Workbook Proof**: Staging records write correct exact name strings.
- **Mutation Summary**: Exact-name comparison precedence check added.
- **Remaining Risk**: Registry spelling errors.
- **Next Step**: Standardize spelling errors warnings.

### Version v375 — Category Expense Route, Matcher, Validator & Reask
- **Timestamp**: 2026-07-10 13:22:09 UTC
- **Problem**: Invalid category inputs resolving to Lainnya.
- **Root Cause**: Parser accepted invalid category names without validation.
- **Decision**: Implement category registry validation loop re-asking up to 3 times.
- **Source SHA Before**: `e15babca4c22908c6cd17834485702de785871a55e410e1c07f5ea79b89b366a`
- **Source SHA After**: `dde3e8cec69ef45d33e7e54a6a4e16ee07084a3016f73c7b02d6d169eee4947d`
- **Apps Script Version**: 370
- **Deployment Fingerprint**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Functions Changed**: `canAskMissingCategoryClarification_`
- **Tests**: Selftest category validation.
- **Live Proof**: Invalid category replies trigger re-prompt options list.
- **Workbook Proof**: Failed categories block ledger writes.
- **Mutation Summary**: Added category re-ask checker.
- **Remaining Risk**: Prompt noise.
- **Next Step**: Improve autocomplete matching.

### AFPD Migration Phase Logs
- **AFPD Phase 1**: Initial readiness audit and inventory creation (COMPLETE).
- **AFPD Phase 1.5**: Exact blocker extraction and files analysis (COMPLETE).
- **AFPD Phase 2**: Migration manifest and authority matrix documentation (COMPLETE).
- **AFPD Phase 3**: Skeleton creation and traceable content migration (COMPLETE).

### AFPD Phase 4
- **Timestamp**: 2026-07-12 10:12:00 WIB
- **Problem**: Original audit produced a false readiness PASS.
- **Root Cause**: Normative extractor inspected only 5 Final Kitab rules and 3 ARFIN rules using hardcoded validator scripts instead of dynamic extraction.
- **Decision**: Reject Phase 4 PASS and initiate full independent challenge.

### AFPD Phase 4.1
- **Timestamp**: 2026-07-12 10:16:00 WIB
- **Problem**: Independent challenge identified undercounted rules and evidence gaps.
- **Root Cause**: dynamic extractors verified 232 Final Kitab rules and 145 ARFIN rules, highlighting 177 normative gaps, 2 commands, 5 enums, 1 exception, and partial evidence durability.
- **Decision**: Declare RESULT=NOT_READY_AFPD_ACTIVATION and proceed to Phase 4.2 gap remediation.

### AFPD Phase 4.2
- **Timestamp**: 2026-07-12 10:22:00 WIB
- **Problem**: Gaps between baseline source rules and target documentation modules.
- **Root Cause**: Gaps left over from initial skeleton migration.
- **Decision**: Map all 377 baseline rules to modules, append verbatim normative blocks, and harden durability via owner transcripts.

- **Timestamp**: 2026-07-12 10:12:00 WIB
- **Problem**: Original audit produced a false readiness PASS.
- **Root Cause**: Normative extractor inspected only 5 Final Kitab rules and 3 ARFIN rules using hardcoded validator scripts instead of dynamic extraction.
- **Decision**: Reject Phase 4 PASS and initiate full independent challenge.

- **Timestamp**: 2026-07-12 10:16:00 WIB
- **Problem**: Independent challenge identified undercounted rules and evidence gaps.
- **Root Cause**: dynamic extractors verified 232 Final Kitab rules and 145 ARFIN rules, highlighting 177 normative gaps, 2 commands, 5 enums, 1 exception, and partial evidence durability.
- **Decision**: Declare RESULT=NOT_READY_AFPD_ACTIVATION and proceed to Phase 4.2 gap remediation.

- **Timestamp**: 2026-07-12 10:22:00 WIB
- **Problem**: Gaps between baseline source rules and target documentation modules.
- **Root Cause**: Gaps left over from initial skeleton migration.
- **Decision**: Map all 377 baseline rules to modules, append verbatim normative blocks, and harden durability via owner transcripts.

### AFPD Phase 4.4
- **Timestamp**: 2026-07-12 10:45:00 WIB
- **Problem**: Gaps between baseline and main body text; generated appendices created fragmentation.
- **Root Cause**: Verbatim rules dumped in generated appendices instead of main body text.
- **Decision**: Integrate active rules into main bodies and completely remove generated appendices.

- **Timestamp**: 2026-07-12 10:45:00 WIB
- **Problem**: Gaps between baseline and main body text; generated appendices created fragmentation.
- **Root Cause**: Verbatim rules dumped in generated appendices instead of main body text.
- **Decision**: Integrate active rules into main bodies and completely remove generated appendices.

### ARFIN Manual Approval Staging — Gate P1 Repository Integration

- **Timestamp**: 2026-07-13 19:06:42 WIB
- **Scope**: Repository integration and durable AFPD evidence only.
- **Problem**: Resolved manual Telegram clarification could bypass Review Queue and mutate ledger state immediately.
- **Decision**: Enforce `Review Queue -> /approval -> Account Ledger` for resolved manual Telegram transactions.
- **Authority parent**: `308a7086154dbaed9c141daad04a43ba3179056b`
- **Source integration commit**: `22caa64774977fdedcd5ae8555e3c805b20feac8`
- **Stable patch ID**: `1d3c4a7f0a88efc4ccce2bb22fa3d0351e3baea5`
- **Patched source SHA-256**: `aca69b3750ce63ce2015ce416880d9b225e704166f8b030a9783623056a93b52`
- **Behavioral validation**: Same-account 1 row; funded payment 3 rows; second approval 0 extra rows; email flow preserved.
- **AFPD incident**: `AFPD-INC-009`
- **Durable evidence**: `docs/evidence/airo-finance/AIRO_ARFIN_MANUAL_APPROVAL_STAGING_GATE_P1_20260713_190642.md`
- **Apps Script deployment**: NOT PERFORMED
- **Workbook mutation**: NOT PERFORMED
- **Telegram production test**: NOT PERFORMED
- **Incident status**: REPAIR_INTEGRATED_NOT_DEPLOYED
- **Next step**: Gate P2 requires separate Owner authorization for deployment and production proof.

### ARFIN Gate P1.1 — built-in self-test contract repair

- **Timestamp**: 2026-07-13 19:17:45 WIB
- **Marker**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1`
- **Authority parent**: `5b56f8ccf92387a6f65537cc34e8970dfb55007c`
- **Source repair commit**: `36bb37c228999efedaeb3ee305e03354f54cbf1a`
- **Scope**: Dry-run reporting and editor self-test assertions only.
- **Actual pre-approval ledger rows**: 0
- **Planned post-approval rows**: 1 for same-account; 3 for funded payment.
- **Built-in self-test**: PASS
- **Apps Script deployment**: NOT PERFORMED
- **Workbook mutation**: NOT PERFORMED
- **Telegram production test**: NOT PERFORMED
- **Incident**: `AFPD-INC-009` remains open.
- **Next**: Resume Gate P2 under existing Owner authorization.

- 2026-07-19: Repaired Gate P1.2 self-test harness dependency alignment (`AIRO_ARFIN_SELFTEST_HARNESS_REPAIR_P1_2`). Self-test pass rate: 17/17.

- 2026-07-19: Documented Gate P2 rollback status and runtime failure evidence (`AIRO_ARFIN_GATE_P2_ROLLBACK_STATUS_AND_FAILURE_EVIDENCE`). Rollback confirmed to version 377.

- 2026-07-19: Documented Gate P2 runtime failure RCA (`AIRO_ARFIN_GATE_P2_RUNTIME_FAILURE_RCA_NO_DEPLOY`). Classification: `CLASP_RUN_CONTEXT_NOT_AUTHORIZED_FOR_SCRIPT_FUNCTION`.

- 2026-07-19: Formulated Gate P2 clasp runtime permission remediation plan (`AIRO_ARFIN_GATE_P2_CLASP_RUNTIME_PERMISSION_REMEDIATION_NO_DEPLOY`). Route: `OWNER_ENABLE_APPS_SCRIPT_API_AND_EXECUTION_API_CONTEXT`.

- 2026-07-19: Documented Gate P2 runtime proof method decision (`AIRO_ARFIN_GATE_P2_RUNTIME_PROOF_METHOD_DECISION_NO_DEPLOY`). Decision: `MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS`.

- 2026-07-19: Executed Gate P2 guarded deployment retry to version `379` (`AIRO_ARFIN_GATE_P2_GUARDED_DEPLOYMENT_RETRY_EXECUTION_MANUAL_RUNTIME_PROOF_METHOD`). Awaiting post-deploy manual editor runtime proof.

- 2026-07-19: Documented post-deploy manual editor runtime proof for version 379 (`AIRO_ARFIN_GATE_P2_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`). Status: PASS 17/17.

# 00_CURRENT_HANDOFF.md

## Current Verified State
- **Apps Script Production Version**: 375
- **Source Code SHA-256**: `dde3e8cec69ef45d33e7e54a6a4e16ee07084a3016f73c7b02d6d169eee4947d`
- **Latest Known Deployment ID**: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Latest Known Deployment Fingerprint**: `497865e5f3c2345b`

## Gmail Poller Window
- **Active Ingestion Business Window**: 09:00 - 00:59 WIB (Asia/Jakarta)
- **Inactive Cooldown Window**: 01:00 - 08:59 WIB (Asia/Jakarta)
- **Timezone Note**: Manifest timezone in `appsscript.json` is `Asia/Bangkok` while the script runs in `Asia/Jakarta`.

## Webhook Intake
- **Telegram Webhook Route**: Runs independently from poller, active 24/7.

## Repository State
- **Pre-existing Dirty Files**:
  - `.obsidian/app.json`
  - `.obsidian/appearance.json`
  - `.obsidian/core-plugins.json`
  - `ecosystem/projects/vortex-ai-skill-lab/apps-script-live/AIRO_Finance_Multitab_Final_v1.js` (matches v375 baseline hash)
  - `state/system-health.md`

## Current Phase and Next Gate
- **Current Phase**: AFPD Phase 3 — Traceable Content Migration
- **Next Gate**: Owner Approval for AFPD Activation and old paths deprecation.

## Gate P1 Handoff — Manual Approval Staging Repair

- **Recorded at**: 2026-07-13 19:06:42 WIB
- **Repository authority parent**: `308a7086154dbaed9c141daad04a43ba3179056b`
- **Integrated source commit**: `22caa64774977fdedcd5ae8555e3c805b20feac8`
- **Integrated source SHA-256**: `aca69b3750ce63ce2015ce416880d9b225e704166f8b030a9783623056a93b52`
- **Stable patch ID**: `1d3c4a7f0a88efc4ccce2bb22fa3d0351e3baea5`
- **Incident**: `AFPD-INC-009`
- **Repository repair status**: INTEGRATED
- **Production deployment status**: NOT DEPLOYED
- **Production runtime proof**: NOT PERFORMED
- **Workbook readback**: NOT PERFORMED
- **AFPD status**: PROPOSED_NOT_CANONICAL
- **Canonical activation**: PENDING_OWNER_APPROVAL
- **Next gate**: Owner-authorized Gate P2 deployment, Telegram runtime proof, approval commit proof, and workbook readback.
- **Do not mark incident resolved** until all Gate P2 production evidence passes.

## Gate P1.1 Handoff — self-test contract aligned

- **Recorded at**: 2026-07-13 19:17:45 WIB
- **Marker**: `AIRO_ARFIN_SELFTEST_CONTRACT_REPAIR_P1_1`
- **Integrated source commit**: `36bb37c228999efedaeb3ee305e03354f54cbf1a`
- **Source SHA-256**: `dcfc2ac0a88aadc3ee4f1b41d0ec5f3b35818eb6d388663bccb8bc7626af8f1b`
- **Built-in outgoing confirmation self-test**: PASS
- **Runtime staging implementation**: unchanged
- **Repository status**: ready for Gate P2 pre-deployment checks
- **Apps Script deployment**: NOT PERFORMED
- **Production runtime proof**: NOT PERFORMED
- **Incident**: `AFPD-INC-009` remains `REPAIR_INTEGRATED_NOT_DEPLOYED`
- **AFPD status**: `PROPOSED_NOT_CANONICAL`
- **Next gate**: Resume Owner-authorized Gate P2 deployment and runtime proof.

- 2026-07-19: Repaired Gate P1.2 self-test harness dependency alignment (`AIRO_ARFIN_SELFTEST_HARNESS_REPAIR_P1_2`). Self-test pass rate: 17/17.

## Gate P2 Rollback Confirmation
- **AFPD-INC-009**: DEPLOYMENT_ATTEMPTED_RUNTIME_PROOF_FAILED_ROLLBACK_CONFIRMED
- **APPS_SCRIPT_DEPLOYMENT**: ATTEMPTED_VERSION_378_ROLLED_BACK_TO_377
- **RUNTIME_PROOF**: FAIL
- **ROLLBACK_STATUS**: CONFIRMED_TO_VERSION_377
- **NEXT_SAFE_GATE**: GATE_P2_RUNTIME_FAILURE_ROOT_CAUSE_ANALYSIS_NO_DEPLOY
- **Marker**: `AIRO_ARFIN_GATE_P2_ROLLBACK_STATUS_AND_FAILURE_EVIDENCE`

## Gate P2 Root Cause Analysis
- **AFPD-INC-009**: RUNTIME_PROOF_FAILED_ROLLBACK_CONFIRMED_RCA_IN_PROGRESS
- **APPS_SCRIPT_DEPLOYMENT**: ATTEMPTED_VERSION_378_ROLLED_BACK_TO_377
- **RUNTIME_PROOF**: FAIL_PERMISSION_OR_AUTH_CONTEXT
- **RCA_STATUS**: CLASP_RUN_CONTEXT_NOT_AUTHORIZED_FOR_SCRIPT_FUNCTION
- **NEXT_SAFE_GATE**: GATE_P2_CLASP_RUNTIME_PERMISSION_REMEDIATION_NO_DEPLOY
- **Marker**: `AIRO_ARFIN_GATE_P2_RUNTIME_FAILURE_RCA_NO_DEPLOY`

## Gate P2 Remediation Plan Status
- **AFPD-INC-009**: RUNTIME_PROOF_FAILED_PERMISSION_REMEDIATION_REQUIRED
- **APPS_SCRIPT_DEPLOYMENT**: ATTEMPTED_VERSION_378_ROLLED_BACK_TO_377
- **RUNTIME_PROOF**: FAIL_PERMISSION_OR_AUTH_CONTEXT
- **REMEDIATION_STATUS**: OWNER_ACTION_REQUIRED
- **NEXT_SAFE_GATE**: GATE_P2_OWNER_MANUAL_APPS_SCRIPT_PERMISSION_REMEDIATION
- **Marker**: `AIRO_ARFIN_GATE_P2_CLASP_RUNTIME_PERMISSION_REMEDIATION_NO_DEPLOY`

## Gate P2 Runtime Proof Method Decision Status
- **AFPD-INC-009**: RUNTIME_PROOF_METHOD_DECIDED_MANUAL_EDITOR_SELFTEST_ACCEPTED_WITH_LIMITATIONS
- **APPS_SCRIPT_DEPLOYMENT**: ATTEMPTED_VERSION_378_ROLLED_BACK_TO_377
- **RUNTIME_PROOF_METHOD**: MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS
- **CLASP_RUN_STATUS**: BLOCKED_PERMISSION_OR_EXECUTION_API_CONTEXT
- **TELEGRAM_LIVE_PROOF**: NOT_YET_PERFORMED
- **WORKBOOK_READBACK**: NOT_YET_PERFORMED
- **INCIDENT_RESOLVED**: NO
- **NEXT_SAFE_GATE**: GATE_P2_GUARDED_DEPLOYMENT_RETRY_PREFLIGHT_MANUAL_RUNTIME_PROOF_METHOD
- **Marker**: `AIRO_ARFIN_GATE_P2_RUNTIME_PROOF_METHOD_DECISION_NO_DEPLOY`

## Gate P2 Guarded Deployment Retry Execution Status
- **AFPD-INC-009**: DEPLOYMENT_RETRY_DEPLOYED_AWAITING_MANUAL_EDITOR_RUNTIME_PROOF
- **APPS_SCRIPT_DEPLOYMENT**: RETRY_DEPLOYED_VERSION_379
- **PREVIOUS_ACTIVE_DEPLOYMENT_VERSION**: 377
- **FAILED_HISTORICAL_DEPLOYMENT_VERSION**: 378
- **RUNTIME_PROOF_METHOD**: MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS
- **POST_DEPLOY_RUNTIME_PROOF**: NOT_YET_PERFORMED
- **CLASP_RUN_STATUS**: BLOCKED_PERMISSION_OR_EXECUTION_API_CONTEXT
- **TELEGRAM_LIVE_PROOF**: NOT_YET_PERFORMED
- **WORKBOOK_READBACK**: NOT_YET_PERFORMED
- **INCIDENT_RESOLVED**: NO
- **NEXT_SAFE_GATE**: GATE_P2_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF
- **Marker**: `AIRO_ARFIN_GATE_P2_GUARDED_DEPLOYMENT_RETRY_EXECUTION_MANUAL_RUNTIME_PROOF_METHOD`

## Gate P2 Post-Deploy Manual Editor Runtime Proof Status
- **AFPD-INC-009**: POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF_PASS_AWAITING_TELEGRAM_LIVE_PROOF
- **APPS_SCRIPT_DEPLOYMENT**: RETRY_DEPLOYED_VERSION_379
- **POST_DEPLOY_RUNTIME_PROOF**: PASS_17_OF_17
- **RUNTIME_PROOF_METHOD**: MANUAL_APPS_SCRIPT_EDITOR_RUNTIME_PROOF_ACCEPTED_FOR_SELFTEST_VERIFICATION_WITH_LIMITATIONS
- **CLASP_RUN_STATUS**: BLOCKED_PERMISSION_OR_EXECUTION_API_CONTEXT
- **TELEGRAM_LIVE_PROOF**: NOT_YET_PERFORMED
- **WORKBOOK_READBACK**: NOT_YET_PERFORMED
- **INCIDENT_RESOLVED**: NO
- **NEXT_SAFE_GATE**: GATE_P2_TELEGRAM_FUNDING_FIRST_LIVE_PROOF_PREFLIGHT
- **Marker**: `AIRO_ARFIN_GATE_P2_POST_DEPLOY_MANUAL_EDITOR_RUNTIME_PROOF`
