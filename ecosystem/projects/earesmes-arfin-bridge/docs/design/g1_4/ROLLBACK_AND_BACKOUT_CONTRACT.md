# EAB G1.4 Rollback and Backout Contract

- **REQUIREMENT**: `PREREQ-009` (Zero-loss rollback topology)
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Corrected Rollback State Semantics

Rollback protocols strictly distinguish between four execution states:

1. `ROLLBACK_BEFORE_STAGE`:
   - Incident occurs during revalidation or before Review Queue write.
   - Action: Cancel request, return fail-closed error.
   - Data Effect: Zero state mutation. Zero Review Queue item created.
2. `ROLLBACK_AFTER_STAGE_BEFORE_APPROVAL`:
   - Incident occurs after Review Queue staging (e.g. infrastructure or database outage).
   - **Corrected Rule**: Valid items in `STAGED` state **RETAIN `REVIEW_STATUS = STAGED`**. Further processing is paused and items are reconciled upon recovery. Items are **NOT** automatically transitioned to `CANCELLED_STALE` unless an actual stale-domain conflict is proven.
3. `ROLLBACK_AFTER_APPROVAL_BEFORE_LEDGER_POST`:
   - Incident occurs after Owner approval, before ledger posting.
   - **Corrected Rule**: Historical Owner approval **IS PRESERVED** (`REVIEW_STATUS = APPROVED`). Posting execution is tracked separately via `LEDGER_POST_STATUS` (`NOT_STARTED`, `PENDING`, `SUCCEEDED`, `FAILED_REQUIRES_RECONCILIATION`). If ledger posting never succeeded, ledger effect is `NONE`.
4. `INCIDENT_AFTER_LEDGER_POST`:
   - Incident occurs after transaction is posted to Account Ledger.
   - **Corrected Rule**: Rollback **MUST NOT AUTOMATICALLY CREATE COMPENSATING TRANSACTIONS**. An explicit Arfin/Owner-authorized compensating workflow is required. Original posted entry and complete audit linkage are strictly preserved.

---

## 2. Queue, Canary, and Database Backout Rules

```ini
ROLLBACK_DELETES_AUDIT_EVIDENCE=NO
ROLLBACK_SILENTLY_DELETES_POSTED_LEDGER_ENTRY=NO
AUTOMATIC_COMPENSATING_LEDGER_WRITE=NO
QUEUE_FLUSH_ON_ROLLBACK=NO
CANARY_ABORT_CANCELS_VALID_STAGED_ITEMS=NO
DUPLICATE_GUARDS_SURVIVE_RESTART_AND_ROLLBACK=YES
DIRECT_ARFIN_FALLBACK_DURING_ROLLBACK=RETAIN
```

1. **Queue Message Retention**: Rollback MUST NOT flush unprocessed or uncertain queue messages. Messages are paused and retained for durable idempotency reconciliation.
2. **Canary Abort Semantics**: Canary abort freezes processing and retains current review states. It does NOT blanket-cancel valid staged items.
3. **Scoped Database Backout**: Database backout MUST NOT overwrite unrelated concurrent Arfin data with full stale snapshots. Point-in-time recovery, scoped table migration backout, or explicit forward-fix MUST be used.
