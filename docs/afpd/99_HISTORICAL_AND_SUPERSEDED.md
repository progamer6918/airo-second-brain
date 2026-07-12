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

### Legacy Normative Rules

<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_002
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 9
integration: EXACT
-->
- **NKTB_002**: Current sprint must not advance beyond Sprint 0A until Sprint 0A Definition of Done is fully audited against this Kitab and committed as PASS.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_069
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1062
integration: EXACT
-->
- **NKTB_069**: After Sprint 3, Wallet Board must not read Cash Ledger.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_079
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1162
integration: EXACT
-->
- **NKTB_079**: Only show after Sprint 7 is active.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_081
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1175
integration: EXACT
-->
- **NKTB_081**: Do not show empty placeholder panel in Sprint 6.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_091
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1269
integration: EXACT
-->
- **NKTB_091**: No large historical migration required.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_092
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1280
integration: EXACT
-->
- **NKTB_092**: New data after cutover must be clean in Account Ledger/Finance Events.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_093
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1281
integration: EXACT
-->
- **NKTB_093**: Old data does not require full backfill.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_094
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1282
integration: EXACT
-->
- **NKTB_094**: Cash Ledger only needs archive/export before deletion.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_096
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1324
integration: EXACT
-->
- **NKTB_096**: Focus: execute current pending ambiguity work.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_097
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1350
integration: EXACT
-->
- **NKTB_097**: Review Queue only after failure/timeout.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_098
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1358
integration: EXACT
-->
- **NKTB_098**: Focus: research/design only, parallel and non-blocking.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_099
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1365
integration: EXACT
-->
- **NKTB_099**: OTP/security hard-block policy
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_100
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1375
integration: EXACT
-->
- **NKTB_100**: OTP/security hard-block policy is clear.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_101
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1404
integration: EXACT
-->
- **NKTB_101**: Internal transfer always has two sides.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_102
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1450
integration: EXACT
-->
- **NKTB_102**: No historical migration required.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_103
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1498
integration: EXACT
-->
- **NKTB_103**: light reconciliation after write
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_104
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1499
integration: EXACT
-->
- **NKTB_104**: full reconciliation admin command/scheduled
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_105
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1509
integration: EXACT
-->
- **NKTB_105**: Reconciliation outputs clean/warning/dirty.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_106
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1511
integration: EXACT
-->
- **NKTB_106**: Action Required appears for partial_failed.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_107
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1524
integration: EXACT
-->
- **NKTB_107**: Action Required
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_108
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1547
integration: EXACT
-->
- **NKTB_108**: Action Required contains real to-dos.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_109
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1563
integration: EXACT
-->
- **NKTB_109**: Telegram alert for pending clarification timeout
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_110
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1576
integration: EXACT
-->
- **NKTB_110**: Dashboard Action Required and Telegram alert are consistent.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_111
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1588
integration: EXACT
-->
- **NKTB_111**: read-only dry-run
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_112
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1591
integration: EXACT
-->
- **NKTB_112**: negative keyword hard-block
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_113
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1592
integration: EXACT
-->
- **NKTB_113**: metadata-only parsing
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_114
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1605
integration: EXACT
-->
- **NKTB_114**: High-confidence routing only after parser is proven.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_115
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1606
integration: EXACT
-->
- **NKTB_115**: Email Ingestion Status appears only when enabled.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_138
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 42
integration: EXACT
-->
- **NKTB_138**: Cash Ledger = transitional; delete after dependency removal
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_171
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1619
integration: EXACT
-->
- **NKTB_171**: 6. Cash Ledger is deleted after dependency removal.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_172
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1620
integration: EXACT
-->
- **NKTB_172**: 7. No large historical migration for Cash Ledger.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_183
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1696
integration: EXACT
-->
- **NKTB_183**: 5. Identifikasi next action paling tepat berdasarkan Sprint 0A.

### Legacy Normative Rules

<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_002
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 9
integration: EXACT
-->
- **NKTB_002**: Current sprint must not advance beyond Sprint 0A until Sprint 0A Definition of Done is fully audited against this Kitab and committed as PASS.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_069
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1062
integration: EXACT
-->
- **NKTB_069**: After Sprint 3, Wallet Board must not read Cash Ledger.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_079
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1162
integration: EXACT
-->
- **NKTB_079**: Only show after Sprint 7 is active.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_081
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1175
integration: EXACT
-->
- **NKTB_081**: Do not show empty placeholder panel in Sprint 6.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_091
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1269
integration: EXACT
-->
- **NKTB_091**: No large historical migration required.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_092
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1280
integration: EXACT
-->
- **NKTB_092**: New data after cutover must be clean in Account Ledger/Finance Events.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_093
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1281
integration: EXACT
-->
- **NKTB_093**: Old data does not require full backfill.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_094
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1282
integration: EXACT
-->
- **NKTB_094**: Cash Ledger only needs archive/export before deletion.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_096
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1324
integration: EXACT
-->
- **NKTB_096**: Focus: execute current pending ambiguity work.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_097
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1350
integration: EXACT
-->
- **NKTB_097**: Review Queue only after failure/timeout.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_098
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1358
integration: EXACT
-->
- **NKTB_098**: Focus: research/design only, parallel and non-blocking.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_099
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1365
integration: EXACT
-->
- **NKTB_099**: OTP/security hard-block policy
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_100
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1375
integration: EXACT
-->
- **NKTB_100**: OTP/security hard-block policy is clear.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_101
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1404
integration: EXACT
-->
- **NKTB_101**: Internal transfer always has two sides.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_102
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1450
integration: EXACT
-->
- **NKTB_102**: No historical migration required.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_103
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1498
integration: EXACT
-->
- **NKTB_103**: light reconciliation after write
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_104
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1499
integration: EXACT
-->
- **NKTB_104**: full reconciliation admin command/scheduled
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_105
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1509
integration: EXACT
-->
- **NKTB_105**: Reconciliation outputs clean/warning/dirty.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_106
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1511
integration: EXACT
-->
- **NKTB_106**: Action Required appears for partial_failed.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_107
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1524
integration: EXACT
-->
- **NKTB_107**: Action Required
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_108
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1547
integration: EXACT
-->
- **NKTB_108**: Action Required contains real to-dos.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_109
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1563
integration: EXACT
-->
- **NKTB_109**: Telegram alert for pending clarification timeout
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_110
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1576
integration: EXACT
-->
- **NKTB_110**: Dashboard Action Required and Telegram alert are consistent.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_111
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1588
integration: EXACT
-->
- **NKTB_111**: read-only dry-run
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_112
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1591
integration: EXACT
-->
- **NKTB_112**: negative keyword hard-block
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_113
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1592
integration: EXACT
-->
- **NKTB_113**: metadata-only parsing
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_114
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1605
integration: EXACT
-->
- **NKTB_114**: High-confidence routing only after parser is proven.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_115
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1606
integration: EXACT
-->
- **NKTB_115**: Email Ingestion Status appears only when enabled.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_138
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 42
integration: EXACT
-->
- **NKTB_138**: Cash Ledger = transitional; delete after dependency removal
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_171
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1619
integration: EXACT
-->
- **NKTB_171**: 6. Cash Ledger is deleted after dependency removal.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_172
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1620
integration: EXACT
-->
- **NKTB_172**: 7. No large historical migration for Cash Ledger.
<!-- AFPD_RULE_PROVENANCE
rule_id: NKTB_183
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_line: 1696
integration: EXACT
-->
- **NKTB_183**: 5. Identifikasi next action paling tepat berdasarkan Sprint 0A.

