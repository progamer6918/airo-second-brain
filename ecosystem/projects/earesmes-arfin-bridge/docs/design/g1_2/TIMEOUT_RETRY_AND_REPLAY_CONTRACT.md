# EAB G1.2 Timeout, Retry, and Replay Contract

- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Operational Values Classification

The following values are classified as `PROPOSED_DEPLOYMENT_DEFAULT_REQUIRING_RUNTIME_VALIDATION` and will be validated in milestone `M11` (Controlled Integration Dry Run) and `M12` (Fresh Live Canary):
- `EAB_ADAPTER_CONNECTION_TIMEOUT_MS` = 3000 ms (`IMPLEMENTATION_CONFIGURATION_CONSTRAINT`)
- `EAB_ADAPTER_OPERATION_TIMEOUT_MS` = 8000 ms (`IMPLEMENTATION_CONFIGURATION_CONSTRAINT`)
- `EAB_MAX_RETRY_COUNT` = 2 (`IMPLEMENTATION_CONFIGURATION_CONSTRAINT`)
- `EAB_REPLAY_WINDOW_SECONDS` = 300 s (`IMPLEMENTATION_CONFIGURATION_CONSTRAINT`)

---

## 2. Replay Protection & Signature Verification

- **Timestamp Skew Tolerance**: ± 300 seconds (5 minutes).
- **Nonce Store**: Unique `(key_id, nonce)` pairs cached for 600 seconds. Replayed nonces are rejected immediately.

---

## 3. G1.1 Durable Uniqueness Contract Inheritance

Idempotency and deduplication inherit the exact G1.1 contract:
```text
DURABLE_STAGING_KEY = root_source_record_id + exact_mutation_hash
```

- **Uncertain Write Reconciliation**: When a write operation times out (`ERR_ADAPTER_TIMEOUT`), the client MUST NOT classify the write as generically safe to retry. Reconciliation MUST occur by re-submitting with the **EXACT SAME IDEMPOTENCY KEY AND PAYLOAD**, or by querying operation status via receipt lookup.
- **Selective Mutation Blocking (TV-014 Correction)**: A duplicate staging attempt with a new idempotency key is blocked ONLY IF the exact same mutation (`exact_mutation_hash`) is already staged. Legitimate, non-equivalent future operations on the same pending record are **NOT BLOCKED**.
