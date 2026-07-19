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
