# EAB G1.3 Manual Transaction Contract

- **REQUIREMENT**: `REQ-009` (Manual multi-line catat intake)
- **STATUS**: `DESIGN_COMPLETE`

---

## 1. Manual Intake Specification

```ini
MANUAL_MULTI_TRANSACTION_FORMAT=ONE_CATAT_TRANSACTION_PER_LINE
AUTO_STAGE_INCOMPLETE_TO_NORMAL_REVIEW_QUEUE=NO
```

---

## 2. Itemized Manual Line Processing

1. **One Transaction Per Line**: Manual catat input evaluates strictly one transaction per input line (e.g. `catat 50rb makan siomay`).
2. **Required Normalized Fields**:
   - `AMOUNT` (Numeric value, required)
   - `CURRENCY_OR_DEFAULT_POLICY` (Default `"IDR"`)
   - `TRANSACTION_DIRECTION` (`"EXPENSE"` or `"INCOME"`)
   - `ACCOUNT_OR_POCKET` (Default `"Main Pocket"`)
   - `CATEGORY` (Parsed category string, e.g. `"Makan"`)
   - `DESCRIPTION` (Transaction notes/description)
   - `TRANSACTION_DATE` (Date string, default current date)
   - `CLIENT_ITEM_ID` & `IDEMPOTENCY_KEY`
3. **Incomplete Manual Lines**:
   - If amount or direction is missing/ambiguous, the line is rejected with `application_status: FAILED` and `application_error_code: ERR_INCOMPLETE_MANUAL_LINE`.
   - Incomplete lines **MUST NOT** be auto-staged to the Review Queue.
   - Specific user feedback is returned prompting for missing fields.
4. **Valid Manual Lines**:
   - Valid lines stage independently to Review Queue in `STAGED` state.
   - All manual Review Queue items require explicit Owner approval before ledger posting.
