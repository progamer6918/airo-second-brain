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

### Integrated Operating Invariants

<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_006
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 56
integration: EXACT
-->
- **NKTB_006**: 4. Missing critical fields must block clean write.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_007
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 57
integration: EXACT
-->
- **NKTB_007**: 5. OTP/security email must be hard-blocked before finance parsing.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_008
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 58
integration: EXACT
-->
- **NKTB_008**: 6. Data quality must affect dashboard trust status.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_010
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 62
integration: EXACT
-->
- **NKTB_010**: 10. Dashboard must be actionable, data-trust aware, and visually disciplined.

### Integrated Operating Invariants

<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_006
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 56
integration: EXACT
-->
- **NKTB_006**: 4. Missing critical fields must block clean write.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_007
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 57
integration: EXACT
-->
- **NKTB_007**: 5. OTP/security email must be hard-blocked before finance parsing.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_008
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 58
integration: EXACT
-->
- **NKTB_008**: 6. Data quality must affect dashboard trust status.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_010
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 62
integration: EXACT
-->
- **NKTB_010**: 10. Dashboard must be actionable, data-trust aware, and visually disciplined.

### Integrated Operating Invariants

<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_006
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 56
integration: EXACT
-->
- **NKTB_006**: 4. Missing critical fields must block clean write.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_007
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 57
integration: EXACT
-->
- **NKTB_007**: 5. OTP/security email must be hard-blocked before finance parsing.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_008
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 58
integration: EXACT
-->
- **NKTB_008**: 6. Data quality must affect dashboard trust status.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_010
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 62
integration: EXACT
-->
- **NKTB_010**: 10. Dashboard must be actionable, data-trust aware, and visually disciplined.

