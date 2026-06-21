# AIRO Finance: Phase 6G Controlled Manual Email Write Pilot Audit & Design

**Date**: 2026-06-01  
**Current Position**: Phase 6G — Controlled Manual Email Write Pilot Approval Gate  
**Scope**: Non-executing technical audit, write schema mapping, and pilot execution safety design.

---

## 1. Executive Summary
This document outlines the design and readiness audit for the **Phase 6G Controlled Manual Email Write Pilot**. The goal is to safely transition from the read-only Phase 6E/6F (Telegram clarification and route preview) to a controlled write pilot where a single, real email candidate from **blu** is written to the **Review Queue**. 

The target candidate details:
* **Provider**: Blu
* **Sender**: receipts@blubybcadigital.id
* **Subject**: Transaksimu Pakai blu Berhasil
* **Message ID**: 19e7da2619bb892e
* **Amount**: Rp336.541
* **User Answer**: E (Manual Review)
* **Route Action**: `manual_review`
* **Target Tab**: `🧾 Review Queue`

---

## 2. Audit of Existing Write & Routing Functions

### A. Account Ledger Write
* **Function**: `writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab)`
* **Behavior**: Maps incoming parsed transaction data to standard ledger columns (`entry_id`, `date`, `account`, `amount_in`, `amount_out`, `balance`, `type`, `category`, `raw_text`, `source_tab`, `linked_txn_id`, `notes`).
* **Trigger**: Executed by the fallback or direct write path inside `writeRouted_`.

### B. Finance Events Write
* **Functions**: `writeFinanceEvent_(ss, event)` & `appendFinanceEvent_(ss, event)`
* **Behavior**: Logs transactions into the chronological index tab `📌 Finance Events` for downstream analytics.
* **Safety**: Designed to fail gracefully if event emission errors, never blocking the primary wallet/ledger writes.

### C. Review Queue Write
* **Function**: `appendByHeader_(ss, AIRO_CONFIG.tabs.review, data, { createIfMissing: false })`
* **Behavior**: The fallthrough write inside `writeRouted_` defaults to calling `appendByHeader_` for `🧾 Review Queue`.
* **Discovered Gap**: When `writeRouted_` falls through to the Review Queue path for raw messages, it passes `common` (which is `stagingResult = { rowId: ... }`) instead of the parsed finance fields. This is why previous Review Queue rows showed empty values for `queue_id`, `amount`, `account`, and `raw_text`.

### D. Post-Write Readback & Verification
* **Function**: `verifyAppendWrite_(ss, sheet, row, col, values)`
* **Behavior**: Reads values directly from the recently written cell range, checks for character-by-character equality against the input array, and returns a boolean flag `writeVerified`.

### E. Idempotency & Duplicate Guards
* **Gmail Candidates**: `airoSprint7FLogPendingCandidate_` guards the `_AIRO_Email_Ingestion_Log` using message-level deduplication against `message_id`.
* **Apps Script Review Queue**: There is **no** native duplicate checking in the Apps Script `appendByHeader_` path for the Review Queue sheet. Repeated execution of the same phrase appends duplicate rows.
* **Python E2E Sync**: Deduplication is performed downstream in `airo_full_auto_sheets_sync.py` via `duplicate_key` lookup against the exported sheet snapshot.

---

## 3. Proposed One-Row Write Pilot Design

Because the user answered `E` and the route action resolved to `manual_review`, the transaction belongs in the **Review Queue**, not the Account Ledger.

### A. Exact Write Target
* **Target Sheet**: `🧾 Review Queue`
* **Canonical Sheet Name**: `AIRO_CONFIG.tabs.review`

### B. Exact Write Fields Schema (V13 Specifications)
The following key-value pairs will be written to `🧾 Review Queue`:

| V13 Header | Value / Formula | Rationale |
| :--- | :--- | :--- |
| **queue_id** | `"review:emc:19e7da2619bb892e"` | Canonical ID derived from the email Message ID |
| **created_at** | `2026-06-01 11:10:17` | Creation timestamp |
| **source** | `"email"` | Original channel |
| **raw_text** | `"Subject: Transaksimu Pakai blu Berhasil \| Amount: Rp336.541 \| Sender: receipts@blubybcadigital.id"` | Summary message |
| **intent** | `"manual_review"` | Action type |
| **target_tab** | `"🧾 Review Queue"` | Destination sheet |
| **reason** | `"email_candidate_manual_review_pilot"` | Rationale for review placement |
| **amount** | `336541` | Extracted numeric amount (Rp336.541) |
| **account** | `"Blu"` | Originating wallet |
| **category** | `"Other / Review"` | Fallback category |
| **status** | `"pending"` | Initial review state |
| **notes** | `"Sprint 7F manual write pilot candidate"` | Log annotation |
| **parser** | `"email"` | Ingestion engine type |
| **duplicate_key** | `"review:emc:19e7da2619bb892e"` | Deduplication key |

---

## 4. Idempotency Rule for the Pilot

To ensure the pilot never writes duplicate entries:
1. **Search Constraint**: Prior to appending, query the sheet for any row containing `queue_id = "review:emc:19e7da2619bb892e"` or `duplicate_key = "review:emc:19e7da2619bb892e"`.
2. **Action Block**: If a matching row is found, abort the append operation and return the details of the existing row (status `dedupe_hit`).

---

## 5. Readback Verification Plan

Following the write, we will run:
1. `verifyAppendWrite_` on the appended row index.
2. An assertions check to confirm that the written row has the correct status (`pending`), amount (`336541`), and account (`Blu`).

---

## 6. Rollback / Manual Cleanup Plan

If the pilot write fails or needs to be undone:
1. **Locate Row**: Open the `🧾 Review Queue` tab in the Google Sheet.
2. **Delete Row**: Locate the row containing `review:emc:19e7da2619bb892e` in the `queue_id` column and delete the entire row.
3. **Reset Ingestion Log**: Locate the matching candidate in the `_AIRO_Email_Ingestion_Log` and reset `resolved_at`, `resolved_answer`, and `write_performed` columns if necessary.

---

## 7. Blockers & Recommendations

### Blockers Before Owner Approval
1. **Gap in default Review Queue write path**: The default fallthrough path in `writeRouted_` does not forward transaction fields to `appendByHeader_`. Directly executing the current routing flow would result in an empty Review Queue entry.
2. **Missing Apps Script deduplication**: The sheet lacks active prevention of double-submits at the Apps Script level.

### Proposed Solution (Safe Pilot Patch)
Before seeking owner approval to execute the pilot write, implement a **narrow non-destructive pilot runner** function inside the script. This function bypasses the generic write path to execute a single-row write with strict idempotency and validation.

```javascript
function runSprint7GManualWritePilotFromEditor() {
  const ss = SpreadsheetApp.openById(getProp_('SPREADSHEET_ID'));
  const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review);
  if (!sheet) throw new Error("Review Queue tab is missing.");
  
  // Strict Idempotency Guard
  const header = findHeader_(sheet);
  if (header) {
    const lastRow = sheet.getLastRow();
    if (lastRow > header.row) {
      const values = sheet.getRange(header.row + 1, 1, lastRow - header.row, sheet.getLastColumn()).getValues();
      const map = reviewHeaderMap_(header.headers);
      const queueIdCol = map['queue_id'] || 0;
      for (let i = 0; i < values.length; i++) {
        if (String(values[i][queueIdCol] || '').trim() === 'review:emc:19e7da2619bb892e') {
          return { ok: true, status: 'dedupe_hit', message: "Candidate already written." };
        }
      }
    }
  }

  // Construct exact V13 row data
  const rowData = {
    queue_id: "review:emc:19e7da2619bb892e",
    created_at: Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss"),
    source: "email",
    raw_text: "Subject: Transaksimu Pakai blu Berhasil | Amount: Rp336.541 | Sender: receipts@blubybcadigital.id",
    intent: "manual_review",
    target_tab: "🧾 Review Queue",
    reason: "email_candidate_manual_review_pilot",
    amount: 336541,
    account: "Blu",
    category: "Other / Review",
    status: "pending",
    notes: "Sprint 7F manual write pilot candidate",
    parser: "email",
    duplicate_key: "review:emc:19e7da2619bb892e"
  };

  const result = appendByHeader_(ss, AIRO_CONFIG.tabs.review, rowData, { createIfMissing: false });
  return {
    ok: true,
    status: 'success',
    write_result: result
  };
}
```

---

## 8. Risk Assessment
* **Data Corruption**: Low. The pilot targets `🧾 Review Queue` exclusively. No direct mutations are performed on Account Ledger or Credit Card tabs, eliminating ledger balance risks.
* **Gmail Alteration**: None. The pilot does not call any Gmail modification APIs.
* **Trigger Loops**: None. The pilot function is run manually from the editor.
