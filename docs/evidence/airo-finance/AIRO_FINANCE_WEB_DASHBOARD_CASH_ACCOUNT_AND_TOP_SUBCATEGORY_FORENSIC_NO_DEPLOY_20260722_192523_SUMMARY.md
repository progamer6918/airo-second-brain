# AIRO Finance Web Dashboard Cash Account and Top Subcategory Forensic Summary

- **Gate**: `AIRO_FINANCE_WEB_DASHBOARD_CASH_ACCOUNT_AND_TOP_SUBCATEGORY_FORENSIC_NO_DEPLOY`
- **Timestamp**: `20260722_192523`
- **Active Apps Script Version**: `388`
- **Mode**: `READ_ONLY_FORENSIC_NO_PATCH_NO_DEPLOY`
- **Source Patch Performed**: `NO`
- **HTML Patch Performed**: `NO`
- **Workbook Mutation**: `NO`
- **Deployment Performed**: `NO`

## Key Forensic Findings

### A. Top Subcategory Forensic
1. **Backend Return**: `airoWebDashboardGetSnapshot_` in `AIRO_Finance_Multitab_Final_v1.js` returns `spending_intelligence.top_subcategories`.
2. **Output Shape**: Array of objects: `[{ category: string, subcategory: string, amount: number }]`, sorted descending by amount and capped at top 10.
3. **HTML Rendering**: `AIRO_Finance_WebDashboard.html`'s `renderDashboard(data)` function currently ONLY renders `spending_intelligence.top_categories`. The `top_subcategories` field is ignored in the HTML DOM rendering loop.
4. **Fix Classification**: `TOP_SUBCATEGORY_FIX_CLASS=FRONTEND_ONLY_SMALL_FIX`. Adding a rendering card for Top Subcategories in HTML will display the data immediately without backend logic changes.

### B. Cash Account & Wallet Snapshot Forensic
1. **Account Registry Seed**: Contains `Cash Umum` (active) and `Cash Bensin` (active). `Cash Makan` is absent from the static Account Registry seed data but used in Telegram prompt options.
2. **Parent/Group Fields**: `Cash Umum` and `Cash Bensin` have `parent_account = "Cash"` and `dashboard_group = "Cash"` in Account Registry.
3. **Root Cause of Objections**:
   - In `airoWebDashboardGetSnapshot_` (line 29552), any account name matching `/cash|tunai/i` is normalized to `normAcc = "Cash"`.
   - Initial wallet map keys default to `['BCA', 'Blu', 'Cash']`.
   - When iterating over ledger rows, rows for `Cash Umum`, `Cash Bensin`, and `Cash Makan` all match `/cash|tunai/i` and overwrite `walletMap["Cash"]`.
   - The final balance displayed under `Cash` is simply the `balance` field of whichever single row had the latest date/row index across ALL cash accounts.
   - Consequently, `Cash Bensin` and `Cash Makan` do NOT appear as separate wallet accounts, and the displayed `Cash` balance does not equal any single account's true balance or a combined sum.
4. **Fix Classification**: `CASH_ACCOUNT_FIX_CLASS=CONTRACT_DECISION_REQUIRED`. Owner contract decision required on whether wallet snapshot should:
   - (Option 1) Render exact active Account Registry accounts (`Cash Umum`, `Cash Bensin`, etc.) individually, or
   - (Option 2) Aggregate balances by `parent_account` / `dashboard_group` (`Cash`).
