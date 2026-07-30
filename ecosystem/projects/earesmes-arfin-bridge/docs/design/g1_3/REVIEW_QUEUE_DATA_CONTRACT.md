# EAB G1.3 Review Queue Data Contract

- **SYSTEM**: Earesmes-Arfin Clarification Bridge (`EAB`)
- **MILESTONE**: `M4` / Gate `EAB_G1_3`
- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Review Queue Item Schema

Every Review Queue record created by EAB MUST adhere to the following schema:

```tsv
FIELD_NAME	DATA_TYPE	REQUIRED	DESCRIPTION
REVIEW_ITEM_ID	STRING	YES	Unique identifier for the Review Queue item (e.g. rev_staged_1001)
SOURCE_TYPE	ENUM	YES	Source origin: EARESMES_PROMPT_REPLY, EARESMES_MANUAL_CATAT, DIRECT_ARFIN_ENTRY
SOURCE_REQUEST_ID	STRING	YES	Request ID from the EAB bounded adapter envelope
SOURCE_OPERATION_ID	STRING	YES	EAB operation ID (EAB_SUBMIT_BATCH_CLARIFICATION or EAB_CREATE_MANUAL_TRANSACTION)
OWNER_PRINCIPAL	INTEGER64	YES	Numeric Telegram owner_chat_id / owner principal ID
ROOT_SOURCE_RECORD_ID	STRING	YES	Immutable lineage root identifier (e.g. root_100)
PENDING_ID	STRING	YES	Pending item identifier (e.g. pid_101)
PENDING_VERSION_AT_SUBMISSION	INTEGER	YES	Expected pending_version at submission time
REACTIVATION_CYCLE	INTEGER	YES	Reactivation cycle number (default 1)
IDEMPOTENCY_KEY	STRING	YES	Client-supplied idempotency key
EXACT_MUTATION_HASH	STRING	YES	SHA-256 digest of normalized mutation payload
PAYLOAD_SCHEMA_VERSION	STRING	YES	Schema version (default 1.0)
NORMALIZED_PAYLOAD	JSON_STRING	YES	Canonical JSON payload (amount, category, notes, date)
CREATED_AT	TIMESTAMP	YES	UNIX timestamp of Review Queue staging
REVIEW_STATUS	ENUM	YES	Current review state (STAGED, APPROVED, REJECTED, CANCELLED_STALE, etc.)
AUDIT_CORRELATION_ID	STRING	YES	Trace correlation ID
```

---

## 2. Review Queue Authority Rules

1. **Exclusive Creation & Mutation**: Only Arfin creates, mutates, or posts Review Queue records. Earesmes interacts strictly via the Bounded Adapter API.
2. **Mandatory Owner Approval**: Staged items remain in `STAGED` state until explicit Owner review and approval (`/approval` or Arfin UI).
3. **Account Ledger Protection**: Rejected, stale, or cancelled review items **NEVER** write to the Account Ledger.
4. **Stable Identity**: `REVIEW_ITEM_ID` remains stable throughout its entire lifecycle.
5. **No Auto-Staging of Incomplete Items**: Incomplete or malformed items MUST NOT be staged to the Review Queue.
