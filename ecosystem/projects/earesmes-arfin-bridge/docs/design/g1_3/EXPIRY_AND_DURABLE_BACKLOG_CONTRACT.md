# EAB G1.3 Expiry and Durable Backlog Contract

- **REQUIREMENT**: `REQ-004` (Active prompt TTL 24h) & `REQ-005` (Durable unresolved backlog) & `REQ-006` (Incomplete expired items no auto-stage)
- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Expiry & Retention Specifications

```ini
ACTIVE_PROMPT_TTL=24_HOURS
PROMPT_EXPIRY_TERMINATES_PROMPT_CONTEXT=YES
PENDING_RECORD_DELETED_ON_PROMPT_EXPIRY=NO
EXPIRED_ITEM_DESTINATION=DURABLE_UNRESOLVED_BACKLOG
PENDING_RECORD_RETENTION=UNTIL_RESOLVED_OR_IGNORED
AUTO_STAGE_INCOMPLETE_TO_NORMAL_REVIEW_QUEUE=NO
```

---

## 2. Expiry Lifecycle Rules

1. **24-Hour Active Prompt TTL**: Prompts active for > 24 hours expire from active Telegram prompt context.
2. **Prompt Context Termination**: Old Telegram messages associated with an expired prompt can no longer be answered directly (`410 Gone`, `ERR_EXPIRED_PROMPT`).
3. **Pending Record Retention**: Pending records are **NEVER DELETED** upon prompt expiry. The pending record moves to state `EXPIRED_UNRESOLVED` in the `DURABLE_UNRESOLVED_BACKLOG`.
4. **Version Effect on Expiry**: Expiry **DOES NOT INCREMENT** `pending_version` because version increments occur atomically only on state mutations.
5. **No Auto-Staging**: Unresolved expired items **MUST NOT** be auto-staged to the normal Review Queue. They remain safely in the unresolved backlog until explicit Owner reactivation or ignore action.
