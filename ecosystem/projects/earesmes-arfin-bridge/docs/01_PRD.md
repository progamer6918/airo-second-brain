# EAB Scope-Locked Product Requirements Document (PRD)

- **STATUS**: `SCOPE_LOCKED`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **CANONICAL_STATUS**: `CANONICAL`
- **IMPLEMENTATION_STATE**: `NOT_STARTED`
- **IMPLEMENTATION_AUTHORIZED**: `NO`
- **AFPD_INC_011_IMPLEMENTATION_BLOCKER**: `YES`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **PROJECT**: `EARESMES_ARFIN_CLARIFICATION_BRIDGE` (`EAB`)

---

## 1. Executive Summary & Approved Owner Decisions

The Owner has formally approved the EAB MVP Scope Lock baseline:

- `PRIMARY_INTERFACE = EARESMES`
- `FINANCE_AUTHORITY = ARFIN`
- `DIRECT_ARFIN_FALLBACK = RETAIN`
- `MULTI_PENDING_UX = COMPACT_LIST_WITH_STABLE_PENDING_REFERENCE` (e.g. `AF-1042 · Rp50.000 · GrabFood`)
- `ACTIVE_PROMPT_TTL = 24_HOURS`
- `PENDING_RECORD_RETENTION = UNTIL_RESOLVED_OR_IGNORED`
- `EXPIRED_ITEM_DESTINATION = DURABLE_UNRESOLVED_BACKLOG`
- `AUTO_STAGE_INCOMPLETE_TO_NORMAL_REVIEW_QUEUE = NO`
- `BATCH_PROCESSING = ITEMIZED_PER_LINE`
- `PRE_SUBMISSION_PENDING_REVALIDATION = REQUIRED`
- `STALE_REPLY_FAIL_CLOSED = YES`
- `MANUAL_MULTI_TRANSACTION_FORMAT = ONE_CATAT_TRANSACTION_PER_LINE`
- `EARESMES_LEDGER_WRITE = FORBIDDEN`
- `CLOUD_INBOX = PHASE_2`

---

## 2. Product Outcome & Scope Boundaries

### MVP Scope (Phase 1)
- **Interactive NL Interface**: Earesmes Bot handles natural language clarification answers and manual `catat` transaction logging.
- **Stable Short References**: Multi-pending items display stable short references (e.g., `AF-1042`) derived from `pending_id` UUIDs. Display shortcuts `#1`, `#2` optional, but payload always carries stable `pending_id`.
- **Itemized Batch Evaluation**: Multi-line batch clarification submissions evaluate each line independently. Valid items stage to Review Queue; invalid items return explicit itemized feedback. Whole-batch rollback is forbidden.
- **Pre-Submission Revalidation**: Earesmes worker calls `eabGetPending` before submitting a clarification to ensure the item was not already resolved directly in Arfin Bot. Stale replies fail closed (`STALE_REPLY_FAIL_CLOSED = YES`).
- **Conversational TTL vs Record Retention**: Prompt/session expires after 24 hours (`ACTIVE_PROMPT_TTL = 24_HOURS`), moving expired items to Durable Unresolved Backlog (`EXPIRED_ITEM_DESTINATION = DURABLE_UNRESOLVED_BACKLOG`). Incomplete records DO NOT enter normal Review Queue (`AUTO_STAGE_INCOMPLETE_TO_NORMAL_REVIEW_QUEUE = NO`).
- **Manual Intake**: Manual entries require one explicit `catat` transaction per line (e.g., `catat 50k makan
catat 20k bensin`). Free-form comma batch deferred to Phase 2.
- **Review Queue Mandatory Staging**: All clarified and manual transactions stage to Arfin `Review Queue` sheet (`writeRouted_`) before Owner `/approval`.

### Phase 2 Scope (Deferred)
- **Cloud Inbox**: 24/7 Cloudflare Worker webhook buffer for PC-off >24h.
- **Free-Form Comma-Separated Batch Parsing**: Untyped multi-transaction parsing in single line.

### Forbidden Non-Goals
- `NO_DIRECT_LEDGER_WRITE`: Earesmes cannot write to Account Ledger directly.
- `NO_NEW_TELEGRAM_BOT`: No third bot creation.
- `NO_AUTOMATIC_APPROVAL`: Mandatory Owner `/approval` retained.
