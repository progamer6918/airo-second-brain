# EAB G1.3 Idempotency and Duplicate-Operation Contract

- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Durable Uniqueness Contract

Durable operation uniqueness inherits the exact G1.1 and G1.2 contract:

```text
DURABLE_MUTATION_KEY = root_source_record_id + exact_mutation_hash
```

Where `exact_mutation_hash` = SHA-256 digest of the normalized mutation payload (`category`, `amount`, `notes`, `date`).

---

## 2. Three-Tier Idempotency Evaluation

1. **Tier 1: Request Receipt Cache (Same Key + Same Payload)**:
   - Same `idempotency_key` and identical payload -> Return cached response receipt (`200 OK`, `application_status: SUCCESS`, `ERR_IDEMPOTENCY_SAME_PAYLOAD`). Zero version increment or double staging.
2. **Tier 2: Key Reuse Payload Mismatch (Same Key + Different Payload)**:
   - Same `idempotency_key` with DIFFERENT payload -> Reject immediately (`400 Bad Request`, `ERR_IDEMPOTENCY_PAYLOAD_MISMATCH`). Zero write.
3. **Tier 3: Durable Duplicate Mutation Guard (New Key + Equivalent Staged Mutation)**:
   - New `idempotency_key` but `root_source_record_id` + `exact_mutation_hash` is ALREADY STAGED in Review Queue -> Reject duplicate staging (`409 Conflict`, `ERR_DUPLICATE_STAGING_MUTATION`).
4. **Legitimate Later Non-Equivalent Mutation**:
   - New `idempotency_key` with a DIFFERENT mutation payload on the same pending item -> Allowed when version and lifecycle rules permit (TV-017 / TV-021 verified).
