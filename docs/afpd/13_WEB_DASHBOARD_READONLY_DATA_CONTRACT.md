<!-- AFPD_PROVENANCE
source_path: docs/afpd/13_WEB_DASHBOARD_READONLY_DATA_CONTRACT.md
source_lines: 1-200
source_heading: AIRO Finance Web Dashboard Read-Only MVP Data Contract
migration_status: CANONICAL
conflict_id: none
-->

# AIRO Finance Web Dashboard Read-Only MVP Data Contract

- **Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_DATA_CONTRACT_NO_DEPLOY`
- **Status**: `CANONICAL`
- **Mode**: `READ_ONLY`
- **Version**: `1.0`
- **Created**: `2026-07-21`

---

## A. MVP Scope Boundary & Safety Constraints
1. **Read-Only Operation**: Served strictly via Apps Script `HtmlService` as a browser view.
2. **No Approval Functionality**: Approval flow remains strictly inside Telegram Gateway / Review Queue.
3. **No Transaction Editing / Deletion**: Zero modification UI elements.
4. **No Ledger Writes**: Zero write operations to `Account Ledger`.
5. **No Review Queue Mutations**: Zero mutations to `Review Queue`.
6. **No External Outbound Triggers**: Zero Telegram bot messages or Gmail API calls.
7. **No Workbook Cell Mutations**: Zero grid clearing, breaking apart, or range formatting in Google Sheets.

---

## B. Source-of-Truth Priority Matrix
1. **Primary Source (MVP Metrics)**: `Account Ledger` approved/final rows. All totals (income, expense, cashflow, category breakdown) MUST be computed directly from finalized ledger entries.
2. **Secondary Source (Deferred Evaluation)**: `Finance Events` evaluated in future phases ONLY if data hygiene proves clean enough.
3. **Operational Warning Source**: `Review Queue` tab queried solely for pending item counts and warning badges. Review items MUST NOT be included in final spending totals.
4. **Frozen Reference**: Old Google Sheets Dashboard tab logic is frozen reference only and MUST NOT serve as a data source or calculation layer.

---

## C. Period Filter Contract
- **Inputs**: `selected_year` (e.g. 2026), `selected_month` (1–12).
- **Timezone Basis**: Script Timezone (`Asia/Jakarta` / GMT+7).
- **Transaction Date Basis**: `Date` column of `Account Ledger`.
- **Current Period Boundaries**:
  - `start`: First day of selected month at `00:00:00` (`new Date(year, month - 1, 1)`).
  - `end`: Last day of selected month at `23:59:59` (`new Date(year, month, 0, 23, 59, 59)`).
- **Previous Period Boundaries (MoM Comparison)**:
  - `previous_start`: First day of preceding month (`new Date(year, month - 2, 1)`).
  - `previous_end`: Last day of preceding month (`new Date(year, month - 1, 0, 23, 59, 59)`).
- **Fallback Rule**: Unparseable or missing transaction dates flag a Data Quality Warning and are excluded from period-specific totals.

---

## D. Included vs. Excluded Row Rules
1. **Included Income Rows**:
   - Rows where `type` === `income` or `pemasukan` OR `amount_in` > 0.
2. **Included Expense Rows**:
   - Rows where `type` === `expense` or `pengeluaran` OR `amount_out` > 0.
3. **Excluded Internal Transfers**:
   - Rows where `category` === `Transfer`, `type` === `transfer`, or `is_internal_transfer` === true are EXCLUDED from income and expense volume totals to prevent artificial cashflow inflation.
4. **Excluded Unapproved Rows**:
   - Pending/rejected rows in `Review Queue` are EXCLUDED from financial metrics.
5. **Excluded Dirty Rows**:
   - Uncategorized expense rows are excluded from clean spending intelligence, but surfaced in Data Quality Warnings.

---

## E. Metric Definitions & Formulas

### 1. Financial KPIs
- `total_income`: Sum of `amount_in` for all included income rows within selected period.
- `total_expense`: Sum of `amount_out` for all included expense rows within selected period.
- `net_cashflow`: `total_income - total_expense`.

### 2. Category & Subcategory Insights
- `category_spending`: Aggregation of `amount_out` grouped by `category` for included expense rows in selected period.
- `subcategory_spending`: Aggregation of `amount_out` grouped by `subcategory` for included expense rows in selected period.
- `contribution_percent`: `(category_current / total_clean_expense_current) * 100`.

### 3. MoM Growth Calculations
- `growth_amount`: `current_amount - previous_amount`.
- `growth_percent`: `((current_amount - previous_amount) / previous_amount) * 100`.
- **Edge Cases**:
  - `previous == 0` AND `current > 0`: Label as `NEW_BASELINE` (`baru bulan ini`), omit infinity percentage.
  - `previous > 0` AND `current == 0`: Label as `DISAPPEARED` (`-100%`).
  - `previous == 0` AND `current == 0`: Omit category from MoM comparison table.

### 4. Operational Panels
- `recent_ledger`: Latest 10 approved rows sorted by `date` descending.
- `review_queue_pending_count`: Count of items in `Review Queue` with status `pending`.
- `last_synced`: Timestamp of latest row entry in `Account Ledger` + web view render execution timestamp.

---

## F. Spending Intelligence Scope Boundaries

### Allowed in Read-Only MVP
- Top 5 spending categories + "Lainnya".
- Top spending subcategories per category.
- Category contribution percentage.
- MoM growth amount and percentage.
- New baseline indicator badges.
- Data quality alert counter.

### Forbidden in Read-Only MVP
- AI auto-recommendations or conversational advice.
- Complex statistical anomaly detection.
- Recurring subscription prediction engine.
- Automated budget allocation recommendations.
- Multi-year trend predictive analytics.
- Full Dashboard Final Kitab feature parity.

---

## G. Data Quality Status Matrix
- **CLEAN**: 0 uncategorized expense rows, 0 unparsed amounts, 0 unhandled date parse errors, 0 pending review queue items exceeding threshold.
- **WARNING**: 1+ uncategorized expense rows, 1+ pending review items, or 1+ zero/unparsed amount entries.
- **DIRTY**: Date parsing failure on core columns, corrupted ledger structure, or reconciled expense sum mismatch.

---

## H. Validation & Readback Gates (Before UI Implementation)
Before writing UI component code, prototype JSON generators MUST verify:
1. Period total expense matches independent `Account Ledger` recomputation.
2. Period total income matches independent `Account Ledger` recomputation.
3. Internal self-transfers are verifiably excluded from income/expense sums.
4. Sum of top categories + "Lainnya" equals `total_clean_expense`.
5. Existing self-test baseline remains 65/65 PASS.

---

## I. JSON Snapshot Schema Contract (`airoWebDashboardGetSnapshot_`)
```json
{
  "ok": true,
  "period": {
    "year": 2026,
    "month": 7,
    "month_name": "Juli",
    "start": "2026-07-01T00:00:00+07:00",
    "end": "2026-07-31T23:59:59+07:00",
    "previous_year": 2026,
    "previous_month": 6
  },
  "period_label": "Juli 2026",
  "data_status": "CLEAN",
  "last_synced": "2026-07-21T20:30:00+07:00",
  "totals": {
    "total_income": 15000000,
    "total_expense": 4500000,
    "net_cashflow": 10500000,
    "clean_expense_total": 4500000,
    "excluded_transfer_total": 2000000
  },
  "spending_intelligence": {
    "top_category": "Food & Drink",
    "top_subcategory": "Jajan",
    "categories": [
      {
        "category": "Food & Drink",
        "current_amount": 2500000,
        "previous_amount": 2000000,
        "contribution_percent": 55.56,
        "growth_amount": 500000,
        "growth_percent": 25.0,
        "growth_status": "UP"
      }
    ]
  },
  "wallet_snapshot": [],
  "recent_ledger": [],
  "review_queue": {
    "pending_count": 0
  },
  "warnings": [],
  "meta": {
    "ledger_total_rows": 150,
    "script_version": 385
  }
}
```
