# AIRO Finance Validation Report — Task 10.5S

## 🧭 AIRO ROADMAP SNAPSHOT
✅ Task 10.5R — Deploy funding-source preservation and run live self-test — PASS
🟡 POSISI SEKARANG: Task 10.5S — Fix funded outgoing live ledger write missing funding-source OUT row — PASS (SOURCE_PATCH_AND_SYNTHETIC_TEST_ONLY)
⛔ Blocker — None
🎯 Next — Deploy and execute production self-test

---

## 1. Context & Goal
During live Telegram testing after Task 10.5R, a funded outgoing transaction (e.g. `cash bayar makan rp 1` funded from `Blu Pocket`) failed to write the first row (`Blu Pocket OUT Rp1`) to the `Account Ledger` sheet. Only Row 2 (`Cash Umum IN`) and Row 3 (`Cash Umum OUT`) were recorded.
Additionally, the subcategory confirmation prompt incorrectly displayed `"Akun: Blu Pocket"`, failing to preserve the transaction's primary account (`Cash Umum`) and misleading the user.

Task 10.5S fixes both issues under a strict local source patch and synthetic verification scope.

---

## 2. Root Cause Analysis
1. **Missing OUT Row**:
   - `normalizeValueForValidation_` checks the values in each column against the Google Sheet's data validation rules.
   - If a cell has a validation dropdown and the written value is not found in that list, `normalizeValueForValidation_` blanks it to `''`.
   - The dropdown list extension function `ensureDropdownAcceptsCurrentValues_` only extends the `category` and `type` fields, leaving the `Account` column validation range untouched.
   - As a result, when writing Row 1 with `account: "Blu Pocket"`, since `"Blu Pocket"` was not in the `Account Ledger`'s static dropdown range, it got blanked to `''`. The row was either written with a blank account or verification readback mismatched, causing a silent loss of the debit row.
2. **Subcategory Prompt Layout**:
   - `airoBuildSubcategoryGroupedPromptMessage_` was hardcoded to display `"Akun: " + account` (which was the funding source `"Blu Pocket"`). It did not accept or display the primary payment account (`Cash Umum`).

---

## 3. Implementation Details

### A. Validation Normalization Fix
Modified `normalizeValueForValidation_` to check if a value exists in the list of eligible registry accounts via `getEligibleFundingSourceAccounts_()` before blanking it:
```javascript
  if (!allowedLower.includes(currentLower)) {
    try {
      const eligible = getEligibleFundingSourceAccounts_().map(v => v.toLowerCase());
      if (eligible.includes(currentLower)) {
        return value;
      }
    } catch (e) {}
  }
```

### B. Prompt Layout Update
Updated `airoBuildSubcategoryGroupedPromptMessage_` to receive an optional `paymentAccount` parameter:
```javascript
function airoBuildSubcategoryGroupedPromptMessage_(amount, account, description, registry, paymentAccount) {
  var accountLines = [];
  if (paymentAccount && String(paymentAccount).toLowerCase() !== String(account).toLowerCase()) {
    accountLines.push("Akun transaksi: " + paymentAccount);
    accountLines.push("Sumber dana: " + account);
  } else {
    accountLines.push("Akun: " + account);
  }
  ...
```
Updated all callers in `airoHandleOutgoingConfirmationReply_` to pass `pending.account`.

---

## 4. Synthetic Test Results
Compiled and ran `runTask105OutgoingConfirmationGateSelfTestFromEditor()` in Node.js test harness. All 17/17 test cases passed:

1. **`invalid_account_selection`**: PASS
2. **`cancel_account_selection`**: PASS
3. **`valid_account_selection_numeric`**: PASS
4. **`valid_account_selection_letter`**: PASS
5. **`valid_account_selection_name`**: PASS
6. **`funded_payment_account_outgoing_3_rows`**: PASS (determines `post_mode = FUNDED_PAYMENT_ACCOUNT_OUTGOING` and generates 3-row write plan)
7. **`single_outgoing_same_source_1_row`**: PASS
8. **`non_cash_single_outgoing`**: PASS
9. **`funded_prompt_display`**: PASS (successfully prints separate `Akun transaksi` and `Sumber dana` labels)
10. **`ambiguous_subcategory_selection`**: PASS
11. **`category_only_selection`**: PASS
12. **`cancel_subcategory_selection`**: PASS
13. **`help_route_selection`**: PASS
14. **`add_flow_selection`**: PASS
15. **`income_rejected_for_outgoing_category_only`**: PASS
16. **`income_rejected_for_outgoing_resolved`**: PASS
17. **`normalize_validation_preserves_valid_account`**: PASS (verifies that `"Blu Pocket"` is preserved even if range validation excludes it)

---

## 5. Security & Static Scan
- **Forbidden API Scan**: PASS (No instances of `setValues` or other spreadsheet modification APIs inside prompt/handling helpers)
- **Secrets/Credentials Check**: PASS (None detected or committed)
