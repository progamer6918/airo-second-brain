# EAB G1.2 Request and Response Envelopes Schema

- **SCHEMA_VERSION**: `1.0`
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Canonical Request Envelope (Itemized Batch Example)

```json
{
  "schema_version": "1.0",
  "request_id": "req_20260730_0001",
  "operation_id": "EAB_SUBMIT_BATCH_CLARIFICATION",
  "owner_chat_id": 123456789,
  "prompt_id": "prompt_881",
  "telegram_message_id": 4051,
  "idempotency_key": "idempotency_k101_v1",
  "request_timestamp": 1785412800,
  "payload": {
    "items": [
      {
        "client_item_id": "item_1",
        "pending_id": "pid_101",
        "short_ref": "AF-1042",
        "expected_version": 1,
        "category": "Makan",
        "notes": "Nasi goreng lunch"
      },
      {
        "client_item_id": "item_2",
        "pending_id": "pid_102",
        "short_ref": "AF-1043",
        "expected_version": 1,
        "category": "Transport",
        "notes": "Taxi fare"
      }
    ]
  }
}
```

---

## 2. Canonical Response Envelope (Itemized Batch Example)

```json
{
  "schema_version": "1.0",
  "request_id": "req_20260730_0001",
  "application_status": "PARTIALLY_SUCCEEDED",
  "application_error_code": "NONE",
  "transport_status_mapping": 200,
  "batch_summary": {
    "total_items": 2,
    "succeeded_items": 1,
    "failed_items": 1
  },
  "item_results": [
    {
      "item_index": 0,
      "client_item_id": "item_1",
      "pending_id": "pid_101",
      "short_ref": "AF-1042",
      "application_status": "SUCCESS",
      "application_error_code": "NONE",
      "current_pending_version": 2,
      "receipt_id": "receipt_staged_991",
      "retry_classification": "NON_RETRYABLE",
      "safe_user_message": "Clarification for AF-1042 successfully staged into Review Queue."
    },
    {
      "item_index": 1,
      "client_item_id": "item_2",
      "pending_id": "pid_102",
      "short_ref": "AF-1043",
      "application_status": "FAILED",
      "application_error_code": "ERR_STALE_PENDING_VERSION",
      "current_pending_version": 2,
      "receipt_id": null,
      "retry_classification": "NON_RETRYABLE",
      "safe_user_message": "Item AF-1043 failed due to version conflict (expected v1, current v2)."
    }
  ],
  "audit_correlation_id": "audit_corr_77123"
}
```
