# EAB Scope-Locked Architecture Specification

- **STATUS**: `SCOPE_LOCKED`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **CANONICAL_STATUS**: `CANONICAL`
- **IMPLEMENTATION_STATE**: `NOT_STARTED`
- **IMPLEMENTATION_AUTHORIZED**: `NO`
- **AFPD_INC_011_IMPLEMENTATION_BLOCKER**: `YES`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **PROJECT**: `EARESMES_ARFIN_CLARIFICATION_BRIDGE` (`EAB`)

---

## 1. System Topology & Processing Pipeline

```
+-----------------------------------------------------------------------------------+
|                                  OWNER TELEGRAM                                   |
+-----------------------------------------------------------------------------------+
        |                                                           |
        | (Primary Chat)                                            | (Fallback Chat)
        v                                                           v
+-----------------------+                                   +-----------------------+
| EARESMES BOT GATEWAY  |                                   |   ARFIN BOT WEBHOOK   |
| (ops/telegram/        |                                   | (Apps Script doPost)  |
|  telegram-gateway.py) |                                   +-----------------------+
| PID 440 (getUpdates)  |                                               |
+-----------------------+                                               |
        |                                                               |
        v (Atomic JSON Queue)                                           |
+-----------------------+                                               |
|  HERMES LOCAL WORKER  |                                               |
| (inbox/telegram-      |                                               |
|  nl-queue/) PID 316   |                                               |
+-----------------------+                                               |
        |                                                               |
        v (Pre-Submission Revalidation: eabGetPending)                  |
+---------------------------------------------------+                   |
|               ARFIN BOUNDED ADAPTER               |                   |
| - Verify owner_chat_id allowlist                  |                   |
| - Verify stable pending_id UUID & pending_version |                   |
| - Perform Itemized Batch Evaluation               |                   |
| - Stage valid items to Review Queue (writeRouted_)|                   |
+---------------------------------------------------+                   |
        |                                                               |
        +-------------------------------+-------------------------------+
                                        |
                                        v
                        +-------------------------------+
                        |      ARFIN REVIEW QUEUE       |
                        |      (Read-Only Staging)      |
                        +-------------------------------+
                                        |
                                        v (Owner /approval Command)
                        +-------------------------------+
                        |     ARFIN ACCOUNT LEDGER      |
                        |   (Authoritative Balance)     |
                        +-------------------------------+
```

---

## 2. Explicit Architecture Invariants & Capability Denial

- **ARCH-INV-001**: Earesmes local runtime has ZERO capability to execute direct Account Ledger write functions (`writeInternalTransferToAccountLedger_`).
- **ARCH-INV-002**: Arfin Bounded Adapter validates all canonical account, category, and subcategory IDs against read-only registry sheets.
- **ARCH-INV-003**: Every transaction MUST reach Review Queue before Owner `/approval`.
- **ARCH-INV-004**: Every pending item has a stable `pending_id` UUID and short reference (`AF-1042`).
- **ARCH-INV-005**: Every clarification submission MUST supply expected `pending_version` integer.
- **ARCH-INV-006**: Stale replies (`expected_version != current_version`) fail closed (`STALE_REPLY_FAIL_CLOSED = YES`).
- **ARCH-INV-007**: Duplicate inputs identified by `telegram_update_id` / `idempotency_key` are idempotent per line item.
- **ARCH-INV-008**: Pre-submission revalidation via `eabGetPending` is mandatory before sending a clarification proposal.
- **ARCH-INV-009**: Batch processing evaluates items independently per line (`BATCH_PROCESSING = ITEMIZED_PER_LINE`). Valid items stage independently; invalid items return specific feedback. Whole-batch rollback is forbidden.
- **ARCH-INV-010**: Prompt TTL (24h) is separate from Pending Record Retention (`UNTIL_RESOLVED_OR_IGNORED`). Expired items move to Durable Unresolved Backlog (`EXPIRED_ITEM_DESTINATION = DURABLE_UNRESOLVED_BACKLOG`). Incomplete expired records DO NOT auto-stage to normal Review Queue.
- **ARCH-INV-011**: AFPD-INC-011 cross-project Telegram collision remains an explicit implementation activation blocker (`AFPD_INC_011_IMPLEMENTATION_ACTIVATION_BLOCKER = YES`).

---

## 3. Explicit Capability Denial Matrix

Earesmes / Hermes credentials and adapter methods MUST NOT permit:
1. `eabApproveTransaction` -> FORBIDDEN (Approval strictly reserved for `/approval` admin command).
2. `eabWriteAccountLedger` -> FORBIDDEN (Direct ledger write forbidden).
3. `arbitrary Apps Script execution` -> FORBIDDEN.
4. `arbitrary sheet write` -> FORBIDDEN.
5. `unscoped pending deletion` -> FORBIDDEN.
