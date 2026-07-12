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

## Normative Rules
The following rules from legacy source documents are traceably migrated and preserved here:

- **NKTB_015** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L29): + audit/reconciliation safety
- **NKTB_021** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L37): Account Ledger = wallet/account movement ledger
- **NKTB_022** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L38): Domain Tabs = Credit Card, Hutang, Aset, Cicilan Rumah
- **NKTB_023** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L39): Finance Events = central event index, not a balance ledger
- **NKTB_024** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L40): Dashboard = intelligence cockpit, not source-of-truth
- **NKTB_025** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L41): Transactions = reserved/future project for PDF/bank mutation work
- **NKTB_027** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L43): Email Ingestion = optional passive input, default OFF
- **NKTB_028** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L44): Review Queue = fallback after clarification fails, not first destination
- **NKTB_030** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L47): The system must continue from existing routing and workbook structure. It must not force all data into a new architecture or rebuild from zero.
- **NKTB_075** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L118): Do not mix this with Finance Events for the current personal finance command center.
- **NKTB_148** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1039): Critical alerts must stand out.
- **NKTB_149** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1040): Net worth must obey home_value_mode.
- **NKTB_199** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1614): 1. Do not rewrite existing architecture.
- **NKTB_200** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1615): 2. Do not use Transactions as master for this scope.
- **NKTB_201** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1616): 3. Account Ledger is wallet movement only.
- **NKTB_202** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1617): 4. Domain detail stays in domain tabs.
- **NKTB_203** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1618): 5. Finance Events is event index, not balance ledger.
- **NKTB_206** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1621): 8. Use cutover-forward model.
- **NKTB_207** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1622): 9. Clarification-first is mandatory for Telegram and Email.
- **NKTB_208** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1623): 10. Review Queue is fallback after clarification fails.
- **NKTB_209** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1624): 11. Missing category is ambiguity.
- **NKTB_210** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1625): 12. Missing critical fields must not clean write.
- **NKTB_211** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1626): 13. OTP/security email is hard-blocked.
- **NKTB_212** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1627): 14. Email ingestion is default OFF.
- **NKTB_213** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1628): 15. Do not store full email body.
- **NKTB_214** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1629): 16. Do not send OTP/security content to Telegram.
- **NKTB_215** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1630): 17. Finance Events must support soft-delete/archive.
- **NKTB_216** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1631): 18. Partial write must be detected and retryable.
- **NKTB_217** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1632): 19. Dashboard must have Data Status and Action Required.
- **NKTB_218** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1633): 20. Net worth must follow home_value_mode.
- **NKTB_219** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1634): 21. Proactive Telegram Alert is required for critical issues.
- **NKTB_220** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1635): 22. Audit and Reconciliation are required before dashboard is trustworthy.
- **NKTB_221** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1648): The new chat must run:
- **NKTB_222** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1656): Then it must summarize:
- **NKTB_223** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1672): Do not propose a new architecture unless the user explicitly asks to revise the kitab.
- **NKTB_224** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1692): 1. Ringkas current architecture secara akurat.
- **NKTB_225** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1693): 2. Jelaskan source-of-truth per layer.
- **NKTB_226** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1694): 3. Jelaskan dashboard final vision.
- **NKTB_227** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1695): 4. Jelaskan roadmap sprint final.
- **NKTB_229** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1697): 6. Sebelum membuat patch, audit repo existing agar tidak menimpa perubahan lokal.
- **NKTB_230** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1698): 7. Semua command harus safe, tidak overwrite, pakai output capture, dan diakhiri dengan command yang copy output agar bisa dipaste ke chat.
- **NKTB_231** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1707): - OTP/security email hard-block.
- **NKTB_232** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1709): - Dashboard wajib Data Status + Action Required.
