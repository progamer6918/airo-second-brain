# AIRO Finance Web Dashboard Separate Cash Accounts and Top Subcategory Repair Summary

- **Gate**: `AIRO_FINANCE_WEB_DASHBOARD_SEPARATE_CASH_ACCOUNTS_AND_TOP_SUBCATEGORY_LOCAL_REPAIR_NO_DEPLOY`
- **Timestamp**: `20260722_193756`
- **Active Apps Script Version**: `388`
- **Mode**: `OWNER_CONTRACT_RECORD_AND_LOCAL_SOURCE_HTML_REPAIR_NO_DEPLOY`
- **Source Patch Performed**: `YES`
- **HTML Patch Performed**: `YES`
- **Workbook Mutation**: `NO`
- **Deployment Performed**: `NO`
- **Clasp Push/Version/Deploy**: `NO`

## Canonical Owner Decision Recorded

- **CASH_ACCOUNT_MODEL**: `SEPARATE`
- **CASH**: `NOT_USED`
- **CASH_UMUM**: `ACTIVE`
- **CASH_BENSIN**: `ACTIVE`
- **CASH_MAKAN**: `ACTIVE`
- **CASH_AND_CASH_UMUM_ARE_SAME_ACCOUNT**: `NO`

### Implications
1. `Cash` is NOT an alias for `Cash Umum`.
2. `Cash` is NOT a parent/group account for balance aggregation.
3. `Cash Umum`, `Cash Bensin`, and `Cash Makan` are three independent active wallet accounts.
4. Regex collapsing of accounts containing `cash` or `tunai` to `Cash` has been REMOVED.
5. Wallet account matching uses exact canonical Account Registry account names (with case-insensitive trim lookup).
6. HTML dashboard now renders `Top Subcategory` alongside `Top Category`.

## Account Registry State Audit & Proposed Mutation Table

| Account | Current state | Target state | Required action |
|---|---|---|---|
| Cash | ABSENT (Group header) | NOT_USED (FALSE) | Insert row with active=FALSE |
| Cash Umum | Row 7 (ACTIVE) | ACTIVE (TRUE) | Retain ACTIVE |
| Cash Bensin | Row 8 (ACTIVE) | ACTIVE (TRUE) | Retain ACTIVE |
| Cash Makan | ABSENT | ACTIVE (TRUE) | Insert row with active=TRUE |

**REGISTRY_REPAIR_REQUIRED**: `YES` (No sheet mutations executed in this gate).

## Verification Results
- **Local Selftest Status**: `PASS` (117/117 test cases)
- **DoPost Unchanged**: `PASS`
- **Read-Only Static Guard**: `PASS`
- **Next Safe Gate**: `AIRO_FINANCE_ACCOUNT_REGISTRY_SEPARATE_CASH_ACCOUNTS_GUARDED_MUTATION_PREFLIGHT_NO_MUTATION`
