# EAB G1.3 Pre-Submission Revalidation Contract

- **REQUIREMENT**: `REQ-008` (Pre-submission pending revalidation via `eabGetPending`)
- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Ordered 11-Step Revalidation Sequence

Before any clarification item is staged to the Review Queue, the adapter MUST execute this exact ordered read-only sequence:

```text
1. Service Authentication Guard (Verify X-EAB-Signature & Nonce)
2. Owner Principal Authorization Guard (Verify owner_chat_id allowlist & Phase 1 policy)
3. Schema Version Validation (Verify schema_version == "1.0")
4. Prompt-Context Binding Guard (Verify prompt_id matches owner_chat_id & active cycle)
5. Pending ID Lookup (Fetch pending record by pending_id / short_ref)
6. Lifecycle-State Validation (Verify pending_state == "ACTIVE")
7. Expected Pending Version Comparison (Verify expected_version == current_pending_version)
8. Root Source Record Lineage Validation (Verify root_source_record_id & reactivation_cycle)
9. Duplicate-Operation Uniqueness Validation (Check root_source_record_id + exact_mutation_hash)
10. Payload Completeness & Domain Validation (Verify required finance fields present)
11. Atomic Review Queue Staging (Stage item to Review Queue & update pending_state)
```

---

## 2. Revalidation Security Rules

1. **Read-Only Non-Mutating Revalidation**: Steps 1 through 10 are strictly read-only.
2. `READ_ONLY_REVALIDATION_VERSION_INCREMENT = NO`: Read-only revalidation MUST NOT increment `pending_version`.
3. `FAILED_REVALIDATION_REVIEW_QUEUE_EFFECT = NONE`: Failed revalidation creates zero Review Queue item.
4. `FAILED_REVALIDATION_ACCOUNT_LEDGER_EFFECT = NONE`: Failed revalidation creates zero Account Ledger effect.
5. `STALE_REPLY_FAIL_CLOSED = YES`: If `expected_version != current_pending_version`, fail immediately with `409 Conflict` (`ERR_STALE_PENDING_VERSION`).
6. **Compare-And-Swap Protection**: Step 11 uses an atomic compare-and-swap update (`WHERE pending_id = :id AND pending_version = :expected_version`) to prevent race conditions between revalidation and staging.
