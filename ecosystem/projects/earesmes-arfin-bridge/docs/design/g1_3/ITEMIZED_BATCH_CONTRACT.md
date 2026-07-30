# EAB G1.3 Itemized Batch Processing Contract

- **REQUIREMENT**: `REQ-007` (Itemized per-line batch evaluation)
- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Itemized Batch Specification

```ini
BATCH_PROCESSING=ITEMIZED_PER_LINE
VALID_BATCH_ITEMS_PROCESS_INDEPENDENTLY=YES
INVALID_BATCH_ITEMS_RETURN_SPECIFIC_FEEDBACK=YES
ATOMIC_BATCH_ROLLBACK_REQUIRED=NO
COMMA_SEPARATED_FREE_FORM_BATCH=DEFERRED
```

---

## 2. Independent Item Processing

1. **Line-by-Line Independence**: Each item in a batch request is evaluated and processed independently.
2. **Mixed Batch Handling**:
   - Item 1 (Valid): Successfully staged to Review Queue -> `application_status: SUCCESS`.
   - Item 2 (Stale version): Fails revalidation -> `application_status: FAILED`, `application_error_code: ERR_STALE_PENDING_VERSION`.
   - Item 3 (Valid): Successfully staged to Review Queue -> `application_status: SUCCESS`.
3. **No All-or-Nothing Rollback**: Valid items (Item 1 & Item 3) remain staged and are **NOT ROLLED BACK** merely because Item 2 failed.
4. **Itemized Response Correlation**: `item_results[]` array preserves the exact input `item_index` and `client_item_id` for client correlation.
5. **Batch Status Summary**:
   - `ALL_SUCCEEDED`: All items succeeded.
   - `PARTIALLY_SUCCEEDED`: At least one item succeeded and at least one item failed.
   - `ALL_FAILED`: All items failed.
6. **Zero Direct Ledger Write**: Neither valid nor invalid batch items write directly to Account Ledger.
