# AIRO Task 10.5Q — Funding Source Preservation in Outgoing Confirmation Validation Report

**Date:** 2026-07-04  
**Status:** PASS  
**Scope:** SOURCE_PATCH_AND_SYNTHETIC_TEST_ONLY  

---

## 1. Owner Evidence & Problem Scope

- **Detected issue:** During real production testing of `cash bayar makan rp 1`, selecting `Blu Pocket` as the funding source account incorrectly resulted in writing `Blu Pocket` directly as the expense transaction account.
- **Root cause:**
  - `airoHandleOutgoingConfirmationReply_` was overwriting `parsed.account` with `pending.confirmed_account` (the selected funding source), losing the original payment account (`pending.account`).
  - Furthermore, `resolvePostingModeAndFundingSource_` was unconditionally overwriting `parsed.funding_source_account` with the result of parsing the original text (which did not contain the selected source).
- **Corrected behavior:**
  - Preserve `parsed.account` as the original payment account (e.g. `Cash Umum`).
  - Store selected funding source as `parsed.funding_source_account` (e.g. `Blu Pocket`).
  - If selected source differs from payment account, set posting mode to `FUNDED_PAYMENT_ACCOUNT_OUTGOING` (3-row write plan).
  - If selected source equals payment account, set posting mode to `SINGLE_OUTGOING` (1-row write plan).

---

## 2. Implemented Rule & Patches

1. **`resolvePostingModeAndFundingSource_` Protection:**
   - Modified the resolver to check `if (!parsed.funding_source_account)` before calling the text-based extractor. This preserves the programmatically set funding source from the confirmation gate.
2. **`airoHandleOutgoingConfirmationReply_` Payload Fix:**
   - Modified final `resolved` step to instantiate `finalParsed` using `account: pending.account` (original) and `funding_source_account: pending.confirmed_account` (user-selected).
3. **`airoHandleOutgoingConfirmationReplyDryRun_` Alignment:**
   - Updated dry-run resolved step to return `finalParsed` containing both fields, execute the posting mode resolver, and return `rowCount = 3` for funded outgoing or `1` for single outgoing.
4. **Self-test Suite Expansion:**
   - Expanded `runTask105OutgoingConfirmationGateSelfTestFromEditor()` to assert 10.5Q specific cases (funded outgoing vs single outgoing plans).

---

## 3. Touched Functions

- `resolvePostingModeAndFundingSource_`
- `airoHandleOutgoingConfirmationReply_`
- `airoHandleOutgoingConfirmationReplyDryRun_`
- `runTask105OutgoingConfirmationGateSelfTestFromEditor`

---

## 4. Synthetic Test Matrix Results

All 18 test cases compiled and passed successfully:

- `resolve_funded_mode_preserves_fs`: **PASS** (Correctly preserves programmatically set funding source and sets `FUNDED_PAYMENT_ACCOUNT_OUTGOING` mode).
- `resolve_single_outgoing_same_account`: **PASS** (Correctly sets `SINGLE_OUTGOING` mode if funding source equals payment account).
- `account_prompt_is_numeric`: **PASS** (Prompt utilizes numeric options `1..N`).
- `invalid_account_selection`: **PASS** (Handles invalid accounts).
- `cancel_account_selection`: **PASS** (`0` fallback to Review Queue).
- `valid_account_selection_numeric`: **PASS** (Numeric choices resolved).
- `valid_account_selection_letter`: **PASS** (Legacy letter options preserved silently).
- `valid_account_selection_name`: **PASS** (Exact name matching resolves).
- `funded_payment_account_outgoing_3_rows`: **PASS** (Blu Pocket selected for Cash Umum transaction returns original account Cash Umum, funding source Blu Pocket, posting mode funded, and write plan row count 3).
- `single_outgoing_same_source_1_row`: **PASS** (Cash Umum selected for Cash Umum transaction returns posting mode single and row count 1).
- `non_cash_single_outgoing`: **PASS** (BCA selected for BCA transaction returns single and row count 1).
- `ambiguous_subcategory_selection`: **PASS** (Handles ambiguous Medicine subcategories).
- `category_only_selection`: **PASS** (Triggers subcategory browse for single category).
- `cancel_subcategory_selection`: **PASS** (0 routes back to Review at Step 2).
- `help_route_selection`: **PASS** (? routes to help).
- `add_flow_selection`: **PASS** (+ routes to add flow).
- `income_rejected_for_outgoing_category_only`: **PASS** (Blocks incompatible Income category).
- `income_rejected_for_outgoing_resolved`: **PASS** (Blocks incompatible Income > Salary subcategory).

---

## 5. Security & Governance Audits

- **Forbidden API Scan:** **PASS** (No calls to prohibited spreadsheet mutation/mail/trigger APIs).
- **Task 10.4 Preservation:** **YES** (Posting resolver functions remain fully present).
- **Workbook Mutation:** **NO**
- **Ledger/Sheet Write:** **NO**
- **Review Queue Write:** **NO**
- **Category Registry Mutation:** **NO**
- **Gmail Read:** **NO**
- **Telegram Send:** **NO**
- **Deploy Performed:** **NO**
- **clasp push/run Performed:** **NO**

---

## 6. Next Steps

- Deploy changes and update versioned web app deployment to parity (Task 10.5R) after owner approval.
