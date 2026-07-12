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
