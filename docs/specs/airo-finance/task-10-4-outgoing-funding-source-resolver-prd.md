# AIRO Finance Task 10.4 — Outgoing Transaction Funding Source Resolver PRD

## 1. Background
Task 10.3 is already closed (`cek saldo` / `saldo` / `balance` behavior). Task 10.4 is a separate workstream and must not modify `cek saldo` behavior or dashboard layouts.

## 2. Problem Statement
The current outgoing transaction flow prompts the user with a generic list of payment accounts:
- A. BCA
- B. Blu
- C. Cash
- D. Credit Card
- E. Lainnya / tulis manual

When the user selects option **E / manual**, the current system repeats the generic options instead of presenting or querying the **Account Registry**. This behavior is incorrect and fails to leverage registered accounts.

## 3. Owner-Locked Requirement
For every outgoing transaction, Arfin must resolve the funding/source account from the **Account Registry**, even if the payment rail seems obvious from the input.

### Examples:
- **Email Blu transaction:** The payment rail is Blu, but the source account must still be resolved from all eligible **Account Registry** accounts.
- **Chat "blu beli makan rp 1":** The payment rail is Blu, but the source account must still be queried.
- **Chat "cash beli makan rp 1":** The word "cash" acts only as a hint; the actual source account must still be resolved from the registry.

## 4. Locked Owner Decisions
The implementation must adhere strictly to these locked decisions:

- **1C:** Source choices must be populated from the **Account Registry** (active accounts, plus inactive accounts if they hold a non-zero balance).
- **2E:** If "other/manual" is selected, query the **Account Registry** and allow manual/partial text entry.
- **3B:** For the "cash" case, the system must ask for the source account from all eligible accounts, not limit the prompt to cash accounts.
- **4C:** If the selected source account differs from the payment account, Arfin must log a double-entry representation:
  - Source Out $\rightarrow$ Payment Account In
  - Payment Account Out $\rightarrow$ Merchant
- **5B:** If the selected source account equals the payment account, Arfin logs only a single outflow entry:
  - Payment Account Out $\rightarrow$ Merchant
- **6B:** Credit Cards are credit lines, not asset accounts, and must not be used as a funding source.
- **7E:** The source picker prompt must display accounts grouped, show their latest balance, and provide a search/manual option.
- **8C:** An insufficient or negative balance in the selected source account should trigger a warning but allow the user to proceed.
- **9A:** Every outgoing transaction must explicitly query and resolve its funding source.
- **10C:** For email Blu transactions, the default payment account is determined by the email provider (e.g., Blu).
- **11D:** In chat commands like "cash beli makan", the word "cash" is treated as a hint. The source and payment accounts follow the selected registry account unless explicit payment rail logic is defined.
- **12A:** In chat commands like "blu beli makan", the payment account is Blu and the source account must still be queried.
- **13C:** Write a multi-entry representation to the sheet if the source account does not equal the payment account.
- **14B:** Once the source is resolved, do not introduce a new final confirmation step specifically for the funding source. This must not bypass existing category or subcategory clarifications.
- **15B:** Credit Cards must not appear in the funding source picker.
- **16C:** "Unknown" must not be selectable; the system must block it and ask for a valid account.
- **17A:** Incoming transaction flows remain unchanged.
- **18B:** If partial account text matches multiple registered accounts, Arfin must ask for disambiguation.
- **19C:** This requirement applies to both chat and email pathways, but must be implemented step-by-step.

## 5. Critical Flow Constraint
The funding-source resolver must integrate smoothly into the existing clarification state machine and must not break:
- Missing category clarification
- Category search/paging
- Subcategory clarification
- Email pending candidate resolution
- Review queue staging
- `writeRouted_` safety and deduplication checks

## 6. Gate 0 Audit Findings
- **Gate 0 read-only audit:** PASS.
- **Local/origin HEAD:** `acdcc3913550ce84b32befb4027f877b9f7cac03`.
- **Live/production SHA:** `7e0aecc273f5afa8e968b74df636ed64b9adbe8d5f3dcce9ec5234fbd59edc1b`.
- **Findings:**
  - Current generic payment account prompt found.
  - Current "other/manual" option handler found.
  - `funding_source_pending` literal found in structural definitions.
  - `category_pending` and `subcategory_pending` state literals found.
  - `Account Registry` literal found.
  - Verification: No source code modifications, clasp deployments, workbook edits, or Telegram/Gmail API calls have been executed.

## 7. Implementation Guardrails
The upcoming patch must NOT:
- Mutate the `🏠 Dashboard` sheet formulas or layout.
- Alter the behavior of Task 10.3 `cek saldo`.
- Allow "Credit Card" or "Unknown" to be selected as a funding source.
- Skip or bypass any active category or subcategory clarification.
- Write transaction rows to the sheet before the funding source is fully resolved.
- Deploy via clasp before passing all offline synthetic test runs.
- Mark the task as `DONE` before providing E2E Telegram proof and obtaining owner visual verification.

## 8. Proposed Gate Plan
- **Gate 1:** PRD/spec lock (This document).
- **Gate 2:** Source code design audit (Read-only, no mutations).
- **Gate 3:** Isolated funding-source resolver patch.
- **Gate 4:** Synthetic Telegram chat testing.
- **Gate 5:** Synthetic email candidate testing.
- **Gate 6:** Clasp push and remote readback verification.
- **Gate 7:** Webhook deployment update and controlled live smoke test.
- **Gate 8:** Owner visual confirmation.
- **Gate 9:** Closeout documentation.
