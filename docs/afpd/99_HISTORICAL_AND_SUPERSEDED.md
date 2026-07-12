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

## Normative Rules
The following rules from legacy source documents are traceably migrated and preserved here:

- **NKTB_004** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L9): Current sprint must not advance beyond Sprint 0A until Sprint 0A Definition of Done is fully audited against this Kitab and committed as PASS.
- **NKTB_026** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L42): Cash Ledger = transitional; delete after dependency removal
- **NKTB_150** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1062): After Sprint 3, Wallet Board must not read Cash Ledger.
- **NKTB_162** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1162): Only show after Sprint 7 is active.
- **NKTB_164** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1175): Do not show empty placeholder panel in Sprint 6.
- **NKTB_174** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1269): No large historical migration required.
- **NKTB_175** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1280): New data after cutover must be clean in Account Ledger/Finance Events.
- **NKTB_176** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1281): Old data does not require full backfill.
- **NKTB_177** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1282): Cash Ledger only needs archive/export before deletion.
- **NKTB_179** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1324): Focus: execute current pending ambiguity work.
- **NKTB_180** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1350): Review Queue only after failure/timeout.
- **NKTB_181** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1358): Focus: research/design only, parallel and non-blocking.
- **NKTB_182** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1365): OTP/security hard-block policy
- **NKTB_183** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1375): OTP/security hard-block policy is clear.
- **NKTB_184** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1404): Internal transfer always has two sides.
- **NKTB_185** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1450): No historical migration required.
- **NKTB_186** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1498): light reconciliation after write
- **NKTB_187** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1499): full reconciliation admin command/scheduled
- **NKTB_188** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1509): Reconciliation outputs clean/warning/dirty.
- **NKTB_189** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1511): Action Required appears for partial_failed.
- **NKTB_190** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1524): Action Required
- **NKTB_191** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1547): Action Required contains real to-dos.
- **NKTB_192** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1563): Telegram alert for pending clarification timeout
- **NKTB_193** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1576): Dashboard Action Required and Telegram alert are consistent.
- **NKTB_194** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1588): read-only dry-run
- **NKTB_195** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1591): negative keyword hard-block
- **NKTB_196** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1592): metadata-only parsing
- **NKTB_197** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1605): High-confidence routing only after parser is proven.
- **NKTB_198** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1606): Email Ingestion Status appears only when enabled.
- **NKTB_204** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1619): 6. Cash Ledger is deleted after dependency removal.
- **NKTB_205** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1620): 7. No large historical migration for Cash Ledger.
- **NKTB_228** (ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md:L1696): 5. Identifikasi next action paling tepat berdasarkan Sprint 0A.
- **NARF_014** (ARFIN.md:L30): Legacy letter answers for subcategory may be accepted for backward compatibility, but prompts should not display A/B/C/D/E for category or subcategory.
