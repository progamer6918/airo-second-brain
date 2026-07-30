# EAB G1.4 Data Migration and Backout Contract

- **STATUS**: `REMEDIATED_R2_DESIGN_COMPLETE`

---

## 1. Legacy Migration Identity Concepts Separation

Identity derivation during migration strictly separates three distinct concepts:

1. `SOURCE_RECORD_ID`: The original legacy source record identifier (e.g. legacy transaction UUID or row ID in pre-EAB store). Identity MUST NOT be derived from mutable business fields (such as amount, category, or date).
2. `PERSISTED_LEGACY_MAPPING`: A dedicated, durable mapping table (`eab_legacy_identity_mapping`) that stores the explicit link `(source_record_id -> root_source_record_id)`.
3. `ROOT_SOURCE_RECORD_ID`: The new immutable root lineage identifier generated during migration for EAB lifecycle management.

```text
source_record_id  --->  persisted_legacy_mapping  --->  root_source_record_id
```

`root_source_record_id` MUST NOT be described as the original source identity when it is created by the migration script.

---

## 2. Migration Execution & Scoped Backout Rules

1. **Pre-Migration Immutable Export**: Immutable database export created immediately prior to executing any migration.
2. **Dry-Run Mode Mandatory**: Dry-run mode (`--dry-run`) validates transformations and constraints with zero writes.
3. **Global Collision Preflight**: Pre-migration checks scan all datasets for identity collisions **BEFORE THE FIRST WRITE IS EXECUTED**. Any collision halts migration immediately with zero partial writes.
4. **Idempotent Migration Reruns**: Rerunning migration scripts produces identical results without creating duplicate rows.
5. **Reconciliation Counts**: Exact row and total hash reconciliation counts compared before and after migration.
6. **Per-Source Migration Audit**: Migration audit record logged per migrated source record.
7. **Interrupted-Run Recovery**: Interrupted migrations detect progress via persisted migration audit records and resume safely.
8. **Scoped Table Backout**: Database backout MUST NOT overwrite unrelated concurrent Arfin data with full stale snapshots. Point-in-time recovery, table-scoped backout, or explicit forward-fix MUST be used.
