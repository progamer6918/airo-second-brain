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
