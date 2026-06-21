# AIRO Finance — Phase 6H Controlled Activation Decision v3

Date: 2026-06-01  
Scope: Phase 6 — Controlled Activation Decision / Regression  
Mode: Docs-only Decision Record  

## Decision Status
`DECISION_PHASE6H_CONTROLLED_ACTIVATION=APPROVED_V3`

This decision record sets the official design guidelines for scheduled email polling ingestion and the multi-step Telegram clarification state machine, superseding previous oversimplified design assumptions.

---

## 1. Core Architecture & Product Decision

Adopt **"Scheduled Polling + Multi-step Telegram Clarification State Machine + Review Queue-first + Conditional Auto-resolve."**

### 1.1 Shift from Single-Variable to Multi-Variable Clarification
AIRO must support multi-variable clarification when more than one field is uncertain. Clarification is not limited to category. The priority order of safety blocks and clarification variables is defined as:
1. **Security Hard-Block**: Stop evaluation immediately for security emails (e.g., OTP, login, password reset, 2FA, verification emails) before any parsing or forwarding to Telegram.
2. **Transaction Type / Direction**: Confirm if the email represents an expense (pengeluaran), income (pemasukan), internal transfer, or is non-financial.
3. **Account**: Map the target wallet/account (e.g., BCA, Blu, Cash, CC).
4. **Amount**: Extract and normalize numeric currency values.
5. **Category**: Resolve the high-level expense/income classification (Layer 1).
6. **Subcategory**: Resolve the granular classification (Layer 2).
7. **Merchant / Notes**: Confirm payee information and transaction notes.
8. **Final Route / Write Confirmation**: Validate execution readiness.

### 1.2 Two-Layer Category Clarification Flow
Category clarification must support a strict two-layer architecture:
* **Layer 1**: High-level Category.
* **Layer 2**: Specific Subcategory.

#### Option E (Category Search & Discovery) Behavior
* E is **not** a final category (does not resolve to `Other / Review` or `manual_review` directly for automatic writing).
* Option E signifies **Category Discovery / Broader Search** because quick choices A/B/C/D are insufficient.
* Selecting E transitions the candidate state to `category_search_pending`.
* AIRO will prompt the user to search/select a valid category/subcategory.
* If the user selects a valid final category/subcategory, the candidate is marked eligible for the write policy.
* If the user does not select a valid category, chooses Other/Review, or the result remains ambiguous, the candidate is written to the **Review Queue** for manual review. Under no circumstances should E auto-resolve directly to the Account Ledger without a confirmed final category.

---

## 2. Target Ingestion & Scheduled Polling Design

### 2.1 Polling Window & Interval
* **Interval**: Every 15 minutes.
* **Active Window**: 07:00–22:00 WIB (Western Indonesian Time).
* **Outside Active Window (Fast Exit)**: If triggered outside this window, the function must execute a fast exit immediately:
  * No Gmail reads.
  * No Telegram prompts sent.
  * No Google Sheet writes.

### 2.2 Gmail Ingestion & Safety Policy
* **Allowed Senders**: Ingestion is restricted to these verified addresses only:
  * `receipts@blubybcadigital.id`
  * `noreply@tokopedia.com`
* **Search Query & Fallback**:
  * Primary search query: `label:"Info Terbaru" (from:receipts@blubybcadigital.id OR from:noreply@tokopedia.com)`
  * Fallbacks if primary query returns 0 threads:
    * `category:updates from:receipts@blubybcadigital.id`
    * `category:updates from:noreply@tokopedia.com`
    * `from:receipts@blubybcadigital.id`
    * `from:noreply@tokopedia.com`
* **Gmail Mutation Block**: The ingestion engine must never modify Gmail.
  * No archiving (`moveToArchive`).
  * No deleting / moving to trash.
  * No marking read/unread.
  * No label changes unless explicitly approved in a separate phase closeout.

### 2.3 Ingestion Trigger Safety Guards (Kill Switch & Caps)
Every ingestion run must run under strict safety constraints:
* **Kill Switch**: A global Script Property boolean `EMAIL_INGESTION_DISABLED` to stop execution.
* **Status Command**: Telegram command to fetch trigger runtime status, heartbeat, error counts, and caps.
* **Heartbeat**: Runtime execution stats written to `_AIRO_Ops_Center` / `_AIRO_Audit_Log`.
* **Dedupe Guard**: Strict deduplication by `message_id` and `thread_id` to prevent repeating Telegram clarification prompts.
* **Caps Per Run**:
  * Maximum candidates processed per run.
  * Maximum Telegram clarification messages sent per run.
* **No Direct Writing**: Trigger executions must **not** write to the `Account Ledger`, `Finance Events`, or any domain tabs (`Credit Card`, `Hutang`, `Aset`, etc.) directly.

### 2.4 Baseline Write Policy (Review Queue-first)
* The baseline target write sheet is strictly the **Review Queue** (`🧾 Review Queue`).
* Review Queue writes must enforce:
  * Strict idempotency by `message_id` or unique candidate ID.
  * Readback verification after write to ensure data parity.
* **No Automatic Account Ledger Write**: Direct automatic ledger writes remain disabled in the initial baseline scheduled polling implementation.

### 2.5 Conditional Auto-Resolve Policy
Automatic writing to `Account Ledger` is **disabled** and will only be activated conditionally after a separate manual Account Ledger write pilot proves:
1. Idempotency guards prevent duplicate ledger entries.
2. Amount extraction parses all formatted strings correctly.
3. Account mappings match sheet destinations accurately.
4. Category/subcategory mapping maps to valid registry targets.
5. Account Ledger readback verification successfully passes.
6. Co-emission checks verify whether `Finance Events` should also be updated.
7. Rollback and manual cleanup paths exist.

Candidates resolved via quick options (A/B/C/D) or resolved after searching under E become eligible for auto-resolve **only** after this pilot has passed. Option E without a validated final category must never auto-resolve.

---

## 3. Rejected Alternatives & Rationale

### 3.1 Rejected: "A/B/C/D/E all directly auto-resolve to Account Ledger"
This approach is rejected because:
1. E represents a search/discovery state, not a final category selection.
2. Direct automatic ledger writes risk corrupting dashboard and balances before the email-to-Account Ledger write path has been proven safe via readback.
3. It bypasses the requirement for a two-layer clarification mechanism.
4. It lacks rollback safeguards for automated writes.

---

## 4. Next Recommended Phase

### Phase 6H-A — Regression + Scheduled Polling Design Audit
A docs-and-static-only design audit to prepare for scheduled polling execution:
* Confirm latest git state and verify that the Phase 6G closeout record exists.
* Audit and verify that all Sprint 7E/7F/7G ingestion, parsing, and readback functions exist.
* Confirm that the Gmail trigger is currently disabled.
* Confirm that automatic email writes are disabled.
* Run all static tests to check for regression safety.
* Design the scheduled polling engine skeleton under the required caps, active window limits, and Review Queue-first baseline policy.
