# EAB G1.2 Trust Boundary and Authority Contract

- **SYSTEM**: Earesmes-Arfin Clarification Bridge (`EAB`)
- **MILESTONE**: `M3` / Gate `EAB_G1_2`
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Authority Hierarchy and Boundary Definitions

```ini
PRIMARY_INTERFACE=EARESMES
FINANCE_AUTHORITY=ARFIN
DIRECT_ARFIN_FALLBACK=RETAIN
EARESMES_LEDGER_WRITE=FORBIDDEN
REVIEW_QUEUE_REQUIRED=YES
OWNER_APPROVAL_REQUIRED=YES
BATCH_PROCESSING=ITEMIZED_PER_LINE
VALID_BATCH_ITEMS_PROCESS_INDEPENDENTLY=YES
INVALID_BATCH_ITEMS_RETURN_SPECIFIC_FEEDBACK=YES
ATOMIC_BATCH_ROLLBACK_REQUIRED=NO
```

1. **Primary User Interface (`EARESMES`)**:
   - Earesmes handles incoming Telegram messages from the Owner.
   - Earesmes does NOT possess financial ledger authority.
   - Earesmes cannot modify accounts, post transactions to the Account Ledger, or bypass Review Queue.

2. **Finance System Authority (`ARFIN`)**:
   - Arfin is the sole authority for financial accounts, transaction categorization, and ledger posting.
   - Arfin exposes a strictly bounded adapter interface (`EAB Bounded Adapter`) for Earesmes interactions.

3. **Direct Arfin Fallback Route (`RETAINED`)**:
   - If Earesmes or the Telegram Bridge is unavailable, degraded, or compromised, the Owner retains full direct access to Arfin web/CLI interface.
   - The direct Arfin fallback path does NOT depend on EAB adapter availability.

4. **Review Queue Mandatory Staging**:
   - ALL user clarifications and manual transaction requests submitted via EAB MUST be staged into the Arfin Review Queue (`STAGED_REVIEW_QUEUE`).
   - Direct writes to the Account Ledger (`POSTED_ACCOUNT_LEDGER`) from EAB are **STRICTLY FORBIDDEN**.

5. **Itemized Per-Line Batch Semantics**:
   - Batch submissions operate **itemized per line**.
   - Valid items in a batch process independently and stage to Review Queue.
   - Invalid items in a batch return item-specific error codes and user messages.
   - Atomic all-or-nothing rollback for mixed batches is **REMOVED**.

6. **Owner Approval Mandatory Boundary**:
   - Every staged clarification requires explicit Owner review and approval (`/approval` command or web UI approval) before ledger posting.
