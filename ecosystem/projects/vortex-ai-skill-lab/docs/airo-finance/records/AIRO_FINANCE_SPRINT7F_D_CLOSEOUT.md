# AIRO Finance - Sprint 7F-D Closeout Record

Timestamp: 2026-05-29 19:15 WIB
Apps Script Version: 74
Deployment ID: `AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie`

## Executive Summary

Sprint 7F-D successfully resolves the bug where the Telegram route preview for email candidates displayed `Nominal: Nominal belum terbaca` despite transient amount parsing success. The transient amount fields are now correctly persisted in the `PropertiesService` pending pointer payload and read back when handling the user's Telegram answer.

## Key Changes

1. **Pending Pointer Amount Preservation**:
   * Updated `airoSprint7FSavePendingPointer_` to store `display_amount`, `detected_amount`, `amount_idr`, and `amount_source` in the pending JSON pointer payload.
   * Removed the duplicate/incorrect properties and cleaned up `rowObj` in `airoSprint7FLogPendingCandidate_`.
2. **aaRun7FD Wrapper**:
   * Added the top-level wrapper function `aaRun7FD()` at the top of the Apps Script code (Lines 11–13) solely for editor manual run convenience (resolving the clasp-run API Executable limitation).
3. **Robust Static Testing**:
   * Updated `scripts/airo_finance_sprint7fd_amount_pointer_static_test.js` to target and assert on the `airoSprint7FSavePendingPointer_` block specifically, ensuring amount fields are present inside the pending pointer.

## Live Test Verification

* **Runner**: `aaRun7FD()` (wrapper to `runSprint7FSendOneClarificationAndLogPendingFromEditor()`)
* **Telegram Candidate Amount**: `Rp24.000` (correctly parsed from body)
* **Telegram Action**: Selected choice `A`
* **Bot Response Verification (PASS)**:
  * `Sprint 7F-D: Route Preview`
  * `Mode: no-write`
  * `Nominal: Rp24.000` (correctly formatted and preserved)
  * `Akun utama: Blu`
  * `Kategori/label: Makan`
  * `Event type: expense`
  * `Domain: Wallet`
  * `Target preview: Account Ledger + Finance Events`
  * `Status: ready_for_router_preview_only`

## Safety Metrics (Strictly Enforced)

* **Finance write**: `false`
* **Account Ledger write**: `false`
* **Finance Events write**: `false`
* **Review Queue write**: `false`
* **Gmail trigger**: `false`
* **Email modified**: `false`
* **Full email body stored**: `false`

## Category Clarification Policy v1

The Category Clarification Policy v1 is approved by the owner:
* Cat/subcat clarification asks two layers (category first, then subcategory) when unknown.
* Option E is mapped to category picker/manual resolution.
* This policy is **not yet implemented globally** in the parser or clarification prompt flows. It will be implemented in a focused separate sprint (Category Contract v1).

## Next Risks & Tasks

* **Category Contract v1**: The mappings and multi-layered category clarification flow must be implemented next.
* **OTP Block Hardening**: Ensure strict pattern matching to hard-block any sensitive/OTP bank messages before ingestion triggers are eventually enabled.
