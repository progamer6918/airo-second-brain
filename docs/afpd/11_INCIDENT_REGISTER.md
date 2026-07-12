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
