# EAB Scope-Locked Data & API Contracts Specification

- **STATUS**: `SCOPE_LOCKED`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **CANONICAL_STATUS**: `CANONICAL`
- **IMPLEMENTATION_STATE**: `NOT_STARTED`
- **IMPLEMENTATION_AUTHORIZED**: `NO`
- **AFPD_INC_011_IMPLEMENTATION_BLOCKER**: `YES`
- **OWNER_SCOPE_LOCK**: `APPROVED`
- **PROJECT**: `EARESMES_ARFIN_CLARIFICATION_BRIDGE` (`EAB`)

---

## 1. Batch & Itemized Entities

### 1. BatchClarificationRequest
```json
{
  "batch_id": "BATCH-20260728-001",
  "owner_chat_id": 123456789,
  "telegram_update_id": 987654321,
  "telegram_message_id": 4567,
  "submitted_at": "2026-07-28T20:05:00+07:00",
  "items": [
    {
      "batch_item_id": "ITEM-01",
      "operation_type": "CLARIFICATION",
      "pending_id": "uuid-v4-af-1042",
      "short_ref": "AF-1042",
      "expected_pending_version": 1,
      "owner_raw_line": "AF-1042 blu pocket makan luar",
      "idempotency_key": "987654321-4567-01",
      "canonical_proposed_fields": {
        "execution_account_id": "ACC_BLU_POCKET",
        "category_id": "CAT_FOOD_DRINK",
        "subcategory_id": "SUBCAT_MAKAN_LUAR"
      }
    },
    {
      "batch_item_id": "ITEM-02",
      "operation_type": "MANUAL_TRANSACTION",
      "pending_id": null,
      "short_ref": null,
      "expected_pending_version": null,
      "owner_raw_line": "catat 20rb jago transport online",
      "idempotency_key": "987654321-4567-02",
      "manual_transaction_payload": {
        "amount": 20000,
        "execution_account_id": "ACC_JAGO",
        "category_id": "CAT_TRANSPORT",
        "subcategory_id": "SUBCAT_ONLINE_TRANSPORT"
      }
    }
  ]
}
```

### 2. BatchClarificationReceipt
```json
{
  "ok": true,
  "batch_id": "BATCH-20260728-001",
  "batch_status": "PARTIAL_SUCCESS",
  "processed_at": "2026-07-28T20:05:01+07:00",
  "items": [
    {
      "batch_item_id": "ITEM-01",
      "item_status": "ACCEPTED",
      "pending_id": "uuid-v4-af-1042",
      "short_ref": "AF-1042",
      "review_queue_receipt_id": "TX-20260728-001",
      "review_queue_row": 42,
      "error_code": null,
      "message": "Staged to Review Queue"
    },
    {
      "batch_item_id": "ITEM-02",
      "item_status": "VALIDATION_FAILED",
      "pending_id": null,
      "short_ref": null,
      "review_queue_receipt_id": null,
      "review_queue_row": null,
      "error_code": "INVALID_ACCOUNT_ALIAS",
      "message": "Akun 'jago' tidak ditemukan dalam pendaftaran canonical."
    }
  ]
}
```

---

## 2. Bounded Adapter Methods (GAS Endpoint)

- `eabGetPending(pending_id)`: Fetches single `PendingClarification` object with current `pending_version` and status.
- `eabListPending(owner_context)`: Returns array of active `PendingClarification` items for `owner_chat_id`.
- `eabSubmitBatchClarification(payload)`: Evaluates batch items independently per line. Stages valid items via `writeRouted_`, returns itemized receipt.
- `eabCreateManualTransaction(payload)`: Stages manual single-line `catat` request to Review Queue via `writeRouted_`.

### Banned Methods (Fail-Closed)
- `eabApproveTransaction`: FORBIDDEN
- `eabWriteAccountLedger`: FORBIDDEN
- `arbitrary Apps Script execution`: FORBIDDEN
