# EAB Pending Model Migration & Idempotent Backfill Plan — Final V3

- **PLAN_ID**: `EAB-MIG-003`
- **STATUS**: `FINAL_CORRECTION_COMPLETE`
- **EXECUTION_GATE**: `EAB_G2_0` (Implementation Phase)

---

## 1. Persisted Mapping & Non-Mutable Origin Strategy

1. **Elimination of Mutable Field Hashing**:
   - Legacy backfill does **NOT** derive canonical identity from mutable business fields (date, amount, description) as its persistent source of truth (`LEGACY_ID_USES_MUTABLE_BUSINESS_FIELDS = NO`).
   - Legacy records use immutable existing `root_source_record_id` (Arfin transaction GUID/ID).

2. **Durable Persisted Mapping Table**:
   - `pending_id` (UUIDv4) and `short_ref` (`AF-1001` upwards) are generated **ONCE** and persisted into a durable mapping table:
     `arfin_pending_mapping (root_source_record_id, pending_id, short_ref, initial_version=1, reactivation_cycle=1)`.
   - `LEGACY_MAPPING_PERSISTED = YES`.

3. **Dry-Run Mode & Collision Check**:
   - Migration script executes a mandatory **dry-run mode** first, generating a collision report.
   - If any collision or un-attributed record is detected: script **blocks completely without any partial write** (`MIGRATION_PARTIAL_WRITE_ON_COLLISION = NO`).

4. **Idempotent Rerun**:
   - Rerunning the migration script reads directly from `arfin_pending_mapping`.
   - `MIGRATION_RERUN_IDEMPOTENT = PASS`.

5. **Zero-Ledger-Mutation Guarantee**:
   - Migration script runs purely on Arfin Review Queue metadata.
   - **Zero mutation** of Account Ledger rows.
   - **Zero mutation** of canonical Git repository during design.
