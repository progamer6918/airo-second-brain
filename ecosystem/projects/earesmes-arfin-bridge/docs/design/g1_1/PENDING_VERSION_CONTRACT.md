# EAB Monotonic Pending Version, Idempotency & Operation Uniqueness Contract — Final V3

- **SPECIFICATION_ID**: `EAB-SPEC-VER-003`
- **STATUS**: `FINAL_CORRECTION_COMPLETE`
- **PREREQUISITE_MAPPING**: `PREREQ-004`
- **MILESTONE**: `M2` (`EAB_G1_1`)

---

## 1. Atomic Mutation Invariants

1. **Read-Only Revalidation Guard**:
   - Pre-submission revalidation (`eabRevalidatePending`) is **100% READ-ONLY**.
   - Revalidation **NEVER increments `pending_version`** (`READ_ONLY_REVALIDATION_VERSION_INCREMENT = NO`).

2. **Atomic Increment Rule**:
   - `pending_version` begins at `1` upon creation.
   - Incremented by `+1` **atomically ONLY on successful state mutation** in storage.
   - Failed validation (`400`), stale version rejection (`409`), and cached idempotent retries (`200` with cached receipt) do **NOT** increment `pending_version`.

## 2. Temporary Receipt Caching vs Durable Operation Uniqueness

1. **Temporary Idempotency Key Receipt Caching (72h TTL)**:
   - Key tuple: `(idempotency_key, pending_id, expected_pending_version, sha256(clarification_payload), user_id)`.
   - Same key + same payload -> returns original cached receipt (200 OK), version unchanged.
   - Same key + different payload -> fails with `IDEMPOTENCY_KEY_PAYLOAD_MISMATCH` (400 Bad Request).
   - Retained for **72 hours** (3x active prompt TTL).

2. **Durable Operation Uniqueness Guard (Durable Storage)**:
   - Duplicate-operation prevention does **NOT** depend solely on the 72h TTL cache (`IDEMPOTENCY_CACHE_IS_SOLE_DUPLICATE_GUARD = NO`).
   - A new idempotency key carrying an equivalent clarification for an already-staged item is blocked by a **durable uniqueness constraint** on `(root_source_record_id, exact_mutation_hash)` in Arfin Review Queue storage (`DURABLE_OPERATION_UNIQUENESS = ACTIVE_ON_ROOT_SOURCE_RECORD_EXACT_MUTATION_HASH`).
   - Fails with `DUPLICATE_STAGING_ATTEMPT_REJECTED` (409 Conflict). Durable uniqueness lasts until terminal state plus audit retention.

## 3. Application Error Codes & HTTP Transport Mappings

- `STALE_PENDING_VERSION_REJECTED` -> HTTP 409 Conflict
- `AMBIGUOUS_SHORT_REF_ERROR` -> HTTP 409 Conflict
- `UNKNOWN_SHORT_REF_ERROR` -> HTTP 404 Not Found
- `RESOLVED_PENDING_CANNOT_BE_REOPENED` -> HTTP 409 Conflict
- `EXPIRED_PROMPT_RETRY_REJECTED` -> HTTP 410 Gone
- `UNAUTHORIZED_OWNER_CHAT_ID` -> HTTP 403 Forbidden
- `IDEMPOTENCY_KEY_PAYLOAD_MISMATCH` -> HTTP 400 Bad Request
- `DUPLICATE_STAGING_ATTEMPT_REJECTED` -> HTTP 409 Conflict
- `STALE_PROMPT_REFERENCE_MISMATCH` -> HTTP 410 Gone
