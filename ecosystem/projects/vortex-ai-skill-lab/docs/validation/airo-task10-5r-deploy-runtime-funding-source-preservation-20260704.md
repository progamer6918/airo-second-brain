# AIRO Task 10.5R — Deploy Funding Source Preservation and Production Runtime Validation Report

**Date:** 2026-07-04  
**Status:** PASS  
**Scope:** DEPLOY_AND_RUNTIME_SELF_TEST_ONLY  

---

## 1. Local & Deployment Baseline

- **Baseline Commit:** `684386bc47b6986ca9a82c414a9210f86d1c066b`
- **Local Source SHA256:** `67188f723732c8c9d006c3103da166310310cee1a5f47825d27e9fcbeb195b5e`
- **Remote Source SHA256:** `67188f723732c8c9d006c3103da166310310cee1a5f47825d27e9fcbeb195b5e`
- **Remote Source Parity:** YES
- **Production Web App Deployment:** `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`
- **Updated Version:** `333`

---

## 2. Production Runtime Self-Test Matrix

Ran `npx clasp run runTask105OutgoingConfirmationGateSelfTestFromEditor` on target:
- **Result status:** PASS
- **Test cases evaluated:**
  - `resolve_funded_mode_preserves_fs`: PASS
  - `resolve_single_outgoing_same_account`: PASS
  - `account_prompt_is_numeric`: PASS
  - `invalid_account_selection`: PASS
  - `cancel_account_selection`: PASS
  - `valid_account_selection_numeric`: PASS
  - `valid_account_selection_letter`: PASS
  - `valid_account_selection_name`: PASS
  - `funded_payment_account_outgoing_3_rows`: PASS
  - `single_outgoing_same_source_1_row`: PASS
  - `non_cash_single_outgoing`: PASS
  - `ambiguous_subcategory_selection`: PASS
  - `category_only_selection`: PASS
  - `cancel_subcategory_selection`: PASS
  - `help_route_selection`: PASS
  - `add_flow_selection`: PASS
  - `income_rejected_for_outgoing_category_only`: PASS
  - `income_rejected_for_outgoing_resolved`: PASS

---

## 3. Webhook & Proxy Alignment

- **Live Telegram Webhook Target:** `https://airo-finance-telegram-proxy.earnsai.workers.dev`
- **Webhook Alignment:** YES (Proxy automatically routes incoming Telegram payloads to Web App version **`333`** of deployment **`AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`**).

---

## 4. Forbidden Actions Audit

- `WORKBOOK_MUTATION` = NO
- `LEDGER_WRITE` = NO
- `ACCOUNT_LEDGER_WRITE` = NO
- `FINANCE_EVENTS_WRITE` = NO
- `REVIEW_QUEUE_WRITE` = NO
- `CATEGORY_REGISTRY_MUTATION` = NO
- `DASHBOARD_MUTATION` = NO
- `GMAIL_READ` = NO
- `TELEGRAM_SEND` = NO
- `TRIGGER_CREATION` = NO
- `SCHEDULED_TRIGGER` = NO
- `REAL_TRANSACTION_APPROVAL` = NO

---

## 5. Next Steps

- Owner can run one manual real Telegram smoke test (e.g., sending `cash bayar makan rp 1` to bot, choosing funding source, category, and checking ledger/review queue results).
