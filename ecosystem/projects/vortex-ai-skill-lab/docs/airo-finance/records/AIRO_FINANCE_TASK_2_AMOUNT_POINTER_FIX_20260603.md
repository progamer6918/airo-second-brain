# AIRO Finance - Task 2 Amount Pointer Fix

Timestamp: 2026-06-03 21:48 WIB
Apps Script Version: @242
Deployment ID: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`

## Executive Summary

Task 2 resolves amount pointer issues and missing email subjects in the email ingestion flow. Specifically:
1. `display_amount`, `detected_amount`, and `amount_idr` are cleaned up and normalized dynamically before formatting/resolving.
2. Email subjects are correctly persisted to the `PropertiesService` pending pointer payload so that they do not log as `undefined` when resolved.
3. The resolved Telegram confirmation message correctly formats Rupiah amounts with period delimiters (e.g. `Rp101.000` instead of `Rp101000`).

## Key Changes

1. **Subject Preservation**:
   * Updated `airoSprint7FSavePendingPointer_` to store `subject: candidate.subject || ""` in the pending JSON pointer payload. This ensures that when the user replies, the subject is read back and logged in the Review Queue.
2. **Robust Amount Normalization**:
   * Updated `airoSprint7FFormatRupiah_` to clean up string amounts and extract digits before trying to convert to number, eliminating `Nominal belum terbaca` fallbacks when strings contain non-digit characters.
   * Updated `airoSprint7FDAmount_` to strip trailing cents `,00` before extracting digits.
3. **Correct Resolved Confirmation**:
   * Updated `airoSprint7HResolveToReviewQueueFallback_` to call the robust `airoSprint7FDAmount_(pending)` instead of `Number(...)` which failed on formatted strings.
   * Updated the Telegram resolution reply in `airoSprint7HResolveToReviewQueueFallback_` to format the nominal amount using `airoSprint7FFormatRupiah_(amount)`, ensuring period-delimited format (e.g. `Rp101.000`).

## Verification Results

* **Local Node.js Simulation**:
  * Simulated saving and loading a pending candidate with amount `101000`.
  * Simulated user reply of `A` (Food & Drink) followed by `C` (Kopi).
  * Observed output shows the correct formatted Nominal and correct subject:
    ```text
    [appendByHeader_] Mock write to: 🧾 Review Queue {"queue_id":"review:emc:test_msg_id","created_at":"2026-06-03T14:47:10.782Z","source":"email","raw_text":"Subject: Transaksimu Pakai blu Berhasil | Amount: Rp101000 | Sender: receipts@blubybcadigital.id","intent":"resolved_review","target_tab":"🧾 Review Queue","reason":"email_candidate_resolved_ingestion","amount":101000,"account":"Blu","category":"Food & Drink / Kopi","status":"pending",...}
    [sendTelegram_] Send to 8482041086 :
    Resolusi transaksi email tersimpan ke Review Queue.

    Nominal: Rp101.000
    Akun: Blu
    Kategori: Food & Drink / Kopi
    Status: pending
    Readback: Verified (PASS)
    ```
* **Static Node Tests (All PASS)**:
  * `scripts/airo_finance_sprint7fd_amount_pointer_static_test.js`
  * `scripts/airo_finance_sprint7fd_email_answer_route_preview_static_test.js`
  * `scripts/airo_finance_sprint7h_static_test.js`

## Safety Metrics

* **Gmail mutation**: `false` (No email archive/delete/label operations performed)
* **Account Ledger write**: `false` (Staged only to Review Queue)
* **Finance Events write**: `false` (Staged only to Review Queue)
* **Scheduled trigger install**: `false` (No triggers touched)
