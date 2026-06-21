# Live Pass: Phase 4B Cash Reporting Audit Alignment

## 1. Metadata
* **Verification Date**: 2026-05-31
* **Commit**: `118e9a2 fix(airo-finance): align cash reporting audit with dashboard layout`
* **Apps Script Deployment**: `@89`
* **Apps Script Deployment ID**: `AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie`

---

## 2. Implementation Overview
Phase 4B implements the cash reporting audit alignment and finalizes legacy cash ledger soft-archiving:
*   **Audit Target Alignment**: Updated `handleSpecialFinanceCommand_`'s cash reporting formula audit block to get and verify cell `K17` (Total Liquid Assets) instead of the obsolete `D17` cell, which was shifted during the Dashboard layout collision guard patch.
*   **Contract Test Alignment**: Updated targeted contract tests to assert on cell `K17` instead of `D17` for both `setupDashboardNetWorthPanel` and audit logs, and refactored the `doPost` write path test to inspect `airoOriginalDoPostForSprint7ParserPlan_` (supporting Sprint 7 middleware wrapper hooks).
*   **Safety Status**: No modifications were made to transaction routing, live email ingestion writing, or Gmail poller triggers.

---

## 3. Test & Verification Results

### Automated Tests (PASS)
*   **Targeted Tests**: `25 passed / 0 failed`
    *   `test_airo_dashboard_monthly_cash_read_contract.py`
    *   `test_airo_cash_ledger_removal_safety_contract.py`
    *   `test_airo_cash_ledger_remaining_dependency_contract.py`
*   **Regression Tests**: `25 passed / 0 failed`
    *   `test_airo_sprint6_backend_tab_styling_verifier.py`
    *   `test_airo_sprint6_reconciliation_dashboard_wiring_verifier.py`
    *   `test_airo_sprint7_email_source_contract_guard_live_pass.py`
    *   `test_airo_sprint7_email_ingestion_decision_gate.py`

### Telegram Smoke Verification (PASS)
1.  **Command**: `admin check cash formulas`
    *   **Response**:
        *   `Monthly B6 pakai Account Ledger: true`
        *   `Monthly E6 pakai Account Ledger: true`
        *   `Monthly B8 formula ada: true`
        *   `Dashboard K17 pakai Account Ledger: true`
2.  **Command**: `admin refresh cash formulas`
    *   **Response**: `Refresh completed. Monthly Review and Dashboard now read Account Ledger for Cash accounts.`
3.  **Command**: `admin check cash formulas` (Post-Refresh)
    *   **Response**: All formula checks resolved to `true` pointing to `📒 Account Ledger`.

*Note: Some Telegram emoji characters rendered as `?` / `??` in the refresh response due to a non-blocking encoding polish issue. This is tracked as polish debt and does not impact formula functionality.*

---

## 4. Soft-Archive Summary
*   **Cash Ledger Tab Status**: Manually hidden (soft-archived) by the user in the Google Sheets user interface.
*   **Deletion Status**: **Not deleted**. The sheet remains available for historical references and parity checks (e.g. `admin check cash parity`).
