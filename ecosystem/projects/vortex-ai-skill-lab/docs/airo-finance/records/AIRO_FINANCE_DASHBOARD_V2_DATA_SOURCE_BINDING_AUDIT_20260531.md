# AIRO Finance Dashboard v2 Data Source Binding Audit

**Document Date**: 2026-05-31  
**Sprint Phase**: Dashboard v2 Data Source Binding Audit  
**Status**: **PENDING OWNER APPROVAL**

This document establishes the precise data-source mapping, filtering logic, potential risks, and wiring readiness for every card, table, and narrative element in the preview tab `🏠 Dashboard v2` (grid range `A1:K41`).

---

## 1. Core Logic & Architecture Rules

Before detailing individual cells, the following architectural boundaries are confirmed and enforced:

> [!IMPORTANT]
> **1. Dynamic Period Selector Architecture (G2 & M2:M6)**
> The month selector cell `G2` contains a date object formatted as `📅 mmmm yyyy` (e.g., `2026-05-01`). This cell drives the following hidden helper columns in `M2:M6` to filter all dashboard data dynamically:
> * **`M2` (selected_month_label)**: `=TEXT(G2; "mmmm yyyy")`
> * **`M3` (period_start)**: `=G2`
> * **`M4` (period_end)**: `=EOMONTH(G2; 0)`
> * **`M5` (previous_period_start)**: `=EDATE(G2; -1)`
> * **`M6` (previous_period_end)**: `=EOMONTH(EDATE(G2; -1); 0)`

> [!NOTE]
> **2. Account Ledger vs. Finance Events Isolation**
> * **Wallet / Cashflow balances** MUST use `'📒 Account Ledger'` as the single source of truth for bank accounts, cash, and transfers.
> * **Spending Intelligence (Categories)** MUST use `'📌 Finance Events'` to isolate actual, categorized expense events and exclude internal transfers.

> [!WARNING]
> **3. Anti-Double-Counting & Special Exclusions**
> * **Internal Transfers**: Excluded from income (`Inflow`) and expenses (`Outflow`) by filtering out categories matching `'Transfer'` or `'Transfer internal'`, as they net to zero in net worth.
> * **Mortgages & Debt Separation**: Liabilities are divided into `'🤝 Hutang'` (outstanding general debts) and `'🏠 Cicilan Rumah'` (KPR mortgage principal outstanding). To prevent double-counting in Total Net Worth, mortgage entries must not be duplicated inside the general Hutang sheet.
> * **Missing Categories**: Transactions with blank or `'Lainnya'` categories are excluded from final spending categories and held in the Data Quality Center.

---

## 2. Row-by-Row Cell Mapping & Data Source Binding Directory

### A. Topbar Panel (Row 2)

| Cell / Range | Display Label / Component | Metric Meaning & Source | Source Tab | Source Columns | Filter by Period? | Planned Formula / Script Value | Fallback Behavior | Data Quality & Double-Count Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B2** | `● Synced: <timestamp>` | Timestamp of the last sync run | `_AIRO_Ops_Center` | Last execution log time | No | Apps Script writes on execution | Default to blank | None | **YES** |
| **D2** | `Data Status: <badge>` | Health status badge (`Trusted` / `Warning` / `Dirty`) | Apps Script Analyzer | Computed status | No | Apps Script writes on build | Default to `'Warning'` | Delay in script trigger shows stale status | **YES** |
| **E2** | `🔔 <count> alerts` | Count of active alerts | Apps Script Analyzer | Issue count | No | Apps Script writes on build | Default to `'0 alerts'` | None | **YES** |
| **G2** | `📅 Mei 2026` | Month Selector Dropdown | User Input | Dropdown validation list | No | `SpreadsheetApp` validation rule | Default to current active month | User inputs invalid string; handled by dropdown block | **YES** |
| **I2** | `Mode: Personal` | System operational mode | Apps Script Settings | Script property mode | No | Static text based on script property | Default to `'Personal'` | None | **YES** |

---

### B. Action Required Cards (Rows 4–7)
*Visual layout: 2x2 grid representing the top 4 active alerts sorted by priority (Critical first, Warning second).*

| Card Slot | Target Cell | Default / Example Label | Metric Meaning & Source | Source Tab | Source Columns | Filter by Period? | Planned Formula / Script Value | Fallback Behavior | Risks & Exclusions | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Slot 1 (Left T)** | `B5:D5` (Msg)<br>`E5` (Action) | `● CC jatuh tempo...`<br>`→ BAYAR` | Outstanding CC payment due within 5 days | `'💳 Credit Card'` | Due dates & unpaid status | Yes (`<= M4`) | Apps Script analyzes and writes dynamically | Show Placeholder: `"✓ Clean / No Action Required"` (Green, `#1A3D25`) | CC payment already wired but not matched | **YES** |
| **Slot 2 (Right T)** | `G5:I5` (Msg)<br>`J5` (Action) | `● Cash umum...`<br>`→ ISI` | Cash umum balance is below critical threshold | `'📒 Account Ledger'` | `amount_in`, `amount_out` | Yes (`<= M4`) | Apps Script checks balance vs threshold | Show Placeholder: `"✓ Clean / No Action Required"` | Target threshold hardcoded in settings vs live ledger | **YES** |
| **Slot 3 (Left B)** | `B6:D6` (Msg)<br>`E6` (Action) | `● 3 transaksi...`<br>`→ REVIEW` | Unmatched purchases in review queue | `'🧾 Review Queue'` | `status` | Yes (`>= M3`, `<= M4`) | Apps Script checks pending rows | Show Placeholder: `"✓ Clean / No Action Required"` | Legacy pending rows counted as active; isolated via cutover timestamp | **YES** |
| **Slot 4 (Right B)** | `G6:I6` (Msg)<br>`J6` (Action) | `● 2 entri missing...`<br>`→ FIX` | Blank categories or missing domain refs | `'📒 Account Ledger'` / `'📌 Finance Events'` | `category`, `domain` | Yes (`>= M3`, `<= M4`) | Apps Script checks blank fields | Show Placeholder: `"✓ Clean / No Action Required"` | Dual source checks could double-count same row; resolved by strict ID matching | **YES** |

---

### C. Executive Command Center KPI Cards (Rows 8–14)

| Cell | Display Label | Metric Meaning | Source Tab | Source Columns / Cells | Filter by Period? | Planned Formula | Fallback | Data Quality & Double-Count Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **D10** | `Net worth` | Cumulative assets minus cumulative liabilities | `'🥇 Aset'`<br>`'🤝 Hutang'`<br>`'🏠 Cicilan Rumah'` | `value`, `outstanding` | Yes (`<= M4`) | `=SUMIFS('🥇 Aset'!D:D; '🥇 Aset'!A:A; "<="&M4) - (SUMIFS('🤝 Hutang'!D:D; '🤝 Hutang'!A:A; "<="&M4) + SUMIFS('🏠 Cicilan Rumah'!D:D; '🏠 Cicilan Rumah'!A:A; "<="&M4))` | `0` | Asset/debt tables missing historical valuations | **YES** |
| **E10** | `Cash tersedia` | Total liquid cash balances across accounts | `'📒 Account Ledger'` | `amount_in`, `amount_out`, `account` | Yes (`<= M4`) | `=SUMIFS('📒 Account Ledger'!D:D; '📒 Account Ledger'!C:C; "<>"; '📒 Account Ledger'!B:B; "<="&M4) - SUMIFS('📒 Account Ledger'!E:E; '📒 Account Ledger'!C:C; "<>"; '📒 Account Ledger'!B:B; "<="&M4)` (filtering for BCA, Blu, Mandiri, Cash bensin, Cash umum) | `0` | Includes non-cash entries if type mapping is wrong | **YES** |
| **G10** | `Cashflow bln ini` | Total Inflow minus Outflow in current month | `'📌 Finance Events'` | `amount`, `event_type` | Yes (`>= M3`, `<= M4`) | `=SUMIFS('📌 Finance Events'!J:J; '📌 Finance Events'!C:C; "Inflow"; '📌 Finance Events'!B:B; ">="&M3; '📌 Finance Events'!B:B; "<="&M4) - SUMIFS('📌 Finance Events'!J:J; '📌 Finance Events'!C:C; "Outflow"; '📌 Finance Events'!B:B; ">="&M3; '📌 Finance Events'!B:B; "<="&M4)` | `0` | Includes internal transfer double counting; eliminated by filtering category != `'Transfer'` | **YES** |
| **J10** | `Critical alerts` | Count of critical errors in the Quality board | `🏠 Dashboard v2` | `J26:J31` | No | `=COUNTIF(J26:J31; "*critical*") + COUNTIF(J26:J31; "⊗*")` | `0` | Dependent on Data Quality cells formulas | **YES** |
| **C13** | `Total aset` | Total assets valuation | `'🥇 Aset'` | `value` | Yes (`<= M4`) | `=SUMIFS('🥇 Aset'!D:D; '🥇 Aset'!A:A; "<="&M4)` | `0` | Out-of-date valuation | **YES** |
| **E13** | `Total hutang` | Total general debt + mortgage liabilities | `'🤝 Hutang'`<br>`'🏠 Cicilan Rumah'` | `outstanding` | Yes (`<= M4`) | `=SUMIFS('🤝 Hutang'!D:D; '🤝 Hutang'!A:A; "<="&M4) + SUMIFS('🏠 Cicilan Rumah'!D:D; '🏠 Cicilan Rumah'!A:A; "<="&M4)` | `0` | Double counts if mortgage is written to regular Hutang sheet | **YES** |
| **G13** | `Saving rate` | Net Cashflow / Inflow % | `🏠 Dashboard v2` | `G10`, `Inflow` | Yes | `=IF(Inflow_Total=0; 0; (Inflow_Total - Outflow_Total) / Inflow_Total)` | `0%` | Distorted if massive one-off asset transfer occurs | **YES** |
| **I13** | `Cicilan rumah` | Principal progress of home loan | `'🏠 Cicilan Rumah'` | `principal_paid` | Yes (`<= M4`) | Unicode progress bar formula based on cumulative payments vs total principal | `"0%"` | Data not updated | **YES** |

---

### D. Wallet & Cashflow Board (Left Panel, Rows 15–23)

| Cell / Range | Account Label | Metric Meaning | Source Tab | Source Columns | Filter by Period? | Planned Formula | Fallback | Data Quality & Double-Count Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B17:E17** | `BCA` | BCA balance & status bar | `'📒 Account Ledger'` | `amount_in`, `amount_out` | Yes (`<= M4`) | `=SUMIFS('📒 Account Ledger'!D:D; '📒 Account Ledger'!C:C; "BCA"; '📒 Account Ledger'!B:B; "<="&M4) - SUMIFS('📒 Account Ledger'!E:E; '📒 Account Ledger'!C:C; "BCA"; '📒 Account Ledger'!B:B; "<="&M4)` | `0` | Missing historical entries | **YES** |
| **B18:E18** | `Blu` | Blu balance & status bar | `'📒 Account Ledger'` | `amount_in`, `amount_out` | Yes (`<= M4`) | Same as BCA, replacing account with `"Blu"` | `0` | None | **YES** |
| **B19:E19** | `Mandiri` | Mandiri balance & status bar | `'📒 Account Ledger'` | `amount_in`, `amount_out` | Yes (`<= M4`) | Same, replacing with `"Mandiri"` | `0` | None | **YES** |
| **B20:E20** | `Cash bensin` | Cash bensin pocket balance | `'📒 Account Ledger'` | `amount_in`, `amount_out` | Yes (`<= M4`) | Same, replacing with `"Cash bensin"` | `0` | None | **YES** |
| **B21:E21** | `Cash umum` | Cash umum pocket balance | `'📒 Account Ledger'` | `amount_in`, `amount_out` | Yes (`<= M4`) | Same, replacing with `"Cash umum"` | `0` | None | **YES** |
| **B22:C22** | `Inflow` | Cumulative Inflows | `'📒 Account Ledger'` | `amount_in`, `type` | Yes (`[M3, M4]`) | `=SUMIFS('📒 Account Ledger'!D:D; '📒 Account Ledger'!G:G; "Inflow"; '📒 Account Ledger'!B:B; ">="&M3; '📒 Account Ledger'!B:B; "<="&M4)` | `0` | Double counts internal transfers if category != `'Transfer'` | **YES** |
| **D22:E22** | `Outflow` | Cumulative Outflows | `'📒 Account Ledger'` | `amount_out`, `type` | Yes (`[M3, M4]`) | `=SUMIFS('📒 Account Ledger'!E:E; '📒 Account Ledger'!G:G; "Outflow"; '📒 Account Ledger'!B:B; ">="&M3; '📒 Account Ledger'!B:B; "<="&M4)` | `0` | None | **YES** |

---

### E. Domain Health Board (Right Panel, Rows 15–23)

| Cell / Range | Domain Label | Metric Meaning | Source Tab | Source Columns | Filter by Period? | Planned Formula / Script Value | Fallback | Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **G17:J17** | `Credit Card` | CC outstanding balance | `'💳 Credit Card'` | `balance` | Yes (`<= M4`) | Outstanding balance as of `M4` | `0` | Unmatched purchases not yet reflected | **YES** |
| **G18:J18** | `Hutang` | Outstanding general liabilities | `'🤝 Hutang'` | `balance` | Yes (`<= M4`) | Sum of unpaid principal as of `M4` | `0` | Double counting with mortgage | **YES** |
| **G19:J19** | `Aset / Emas` | Emas valuation | `'🥇 Aset'` | `valuation` | Yes (`<= M4`) | Cumulative gold valuation as of `M4` | `0` | Stale gold price | **YES** |
| **G20:J20** | `Cicilan Rumah` | Remaining mortgage liability | `'🏠 Cicilan Rumah'` | `outstanding` | Yes (`<= M4`) | Remaining home loan outstanding principal | `0` | None | **YES** |
| **G22:J22** | `Source Note` | Description of domain updates | Static | None | No | Merged cell string: `"Source: Credit Card / Hutang / Aset / Cicilan"` | N/A | None | **YES** |

---

### F. Spending Intelligence Board (Left Panel, Rows 24–32)
*All percentages and trend indicators are calculated relative to total outflow.*

| Cell / Range | Category | Metric Meaning | Source Tab | Source Columns | Filter by Period? | Planned Formula | Fallback | Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B26:E26** | `Makanan` | Makanan spending % & trend | `'📌 Finance Events'` | `amount`, `category`, `direction` | Yes | `=SUMIFS('📌 Finance Events'!J:J; '📌 Finance Events'!I:I; "Makanan"; '📌 Finance Events'!K:K; "Outflow"; '📌 Finance Events'!B:B; ">="&M3; '📌 Finance Events'!B:B; "<="&M4) / Total_Outflow` (trend uses M5:M6) | `0%` | Misclassification | **YES** |
| **B27:E27** | `Transport` | Transport spending % & trend | `'📌 Finance Events'` | `amount`, `category` | Yes | Same as Makanan, replacing category with `"Transport"` | `0%` | None | **YES** |
| **B28:E28** | `CC payment` | CC payment transfers | `'📌 Finance Events'` | `amount`, `category` | Yes | Same, replacing category with `"CC payment"` | `0%` | Double counts if outflow is counted twice | **YES** |
| **B29:E29** | `Utilities` | Utility bills spending % | `'📌 Finance Events'` | `amount`, `category` | Yes | Same, replacing category with `"Utilities"` | `0%` | None | **YES** |
| **B30:E30** | `Bensin` | Bensin spending % | `'📌 Finance Events'` | `amount`, `category` | Yes | Same, replacing category with `"Bensin"` | `0%` | None | **YES** |
| **B31:E31** | `Lainnya` | Uncategorized/misc spending % | `'📌 Finance Events'` | `amount`, `category` | Yes | Same, replacing category with `"Lainnya"` | `0%` | High Lainnya ratio signals data quality issues | **YES** |
| **B32:E32** | `Source Info` | Footnote showing spending sources | Static | None | No | Merged cell string: `"  =SUMIF(FinanceEvents, category, bulan) — hanya data clean"` | N/A | None | **YES** |

---

### G. Data Quality Center Board (Right Panel, Rows 24–32)

| Cell / Range | Quality Check Label | Metric Meaning | Source Tab | Source Columns | Filter by Period? | Planned Formula / Script Value | Fallback | Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **G26:J26** | `CC payment belum match` | Unmatched active credit card items count | `'🧾 Review Queue'` | `status`, `account` | Yes (`[M3, M4]`) | Count of pending CC rows | `0` | Stale review data | **YES** |
| **G27:J27** | `Finance Events tanpa domain ref` | Event rows lacking domain mapping | `'📌 Finance Events'` | `domain` | Yes | Count of empty domain cells | `0` | None | **YES** |
| **G28:J28** | `Pending clarification` | Count of pending clarification items | `'🧾 Review Queue'` | `status` | Yes | Count of active pending rows | `0` | Double counting legacy issues | **YES** |
| **G29:J29** | `Missing category` | Count of blank category transactions | `'📒 Account Ledger'` | `category` | Yes | `=COUNTIFS('📒 Account Ledger'!B:B; ">="&M3; '📒 Account Ledger'!B:B; "<="&M4; '📒 Account Ledger'!H:H; "")` | `0` | None | **YES** |
| **G30:J30** | `Rekonsiliasi terakhir` | Last recon health status pill | Apps Script | Analysis result | No | Apps Script writes `'clean'` or `'needs review'` | `'clean'` | Execution lag | **YES** |
| **G31:J31** | `Audit log (scratch)` | Quality checklist indicator | `_AIRO_Audit_Log` | Row count | No | Count of audit logs written | `0` | Large logs | **YES** |

---

### H. Smart Insight Narrative Cards (Rows 33–36)
*All narratives are dynamic text blocks written by the Alert/Insight Engine during build, filtered by the active period.*

| Card Slot | Target Cell | Label / Role | Source Tab / logic | Filter by Period? | Planned Value | Fallback | Risks | Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Slot 1 (Left T)** | `B34:E34` | **Critical Narrative** | Active critical alerts analysis | Yes | Dynamic advice text | `"No critical alerts for this period."` | Stale alerts | **YES_WITH_FALLBACK** |
| **Slot 2 (Right T)** | `G34:J34` | **Critical Narrative** | Active critical cash alerts | Yes | Dynamic advice text | `"Liquid positions are healthy."` | None | **YES_WITH_FALLBACK** |
| **Slot 3 (Left M)** | `B35:E35` | **Warning Narrative** | Outflow trend & budget alerts | Yes | Dynamic advice text | `"Spending remains within normal limits."` | Budget thresholds not set | **YES_WITH_FALLBACK** |
| **Slot 4 (Right M)** | `G35:J35` | **Warning Narrative** | Cash depletion & warning cards | Yes | Dynamic advice text | `"No warning-level alerts."` | None | **YES_WITH_FALLBACK** |
| **Slot 5 (Left B)** | `B36:E36` | **Positive Narrative** | Saving rate & milestones advice | Yes | Dynamic advice text | `"Keep tracking your financial metrics."` | None | **YES_WITH_FALLBACK** |
| **Slot 6 (Right B)** | `G36:J36` | **Info Narrative** | Investment updates & advice | Yes | Dynamic advice text | `"Insights will be populated on sync."` | None | **YES_WITH_FALLBACK** |

---

## 3. Special Verification Checkpoints

Before formula wiring, the following checkpoints must be explicitly aligned:

1. **G2 Selected Month Mapping Verification**:
   * Cells `M3` and `M4` represent the absolute date boundaries. All cell sum and count formulas MUST reference `M3` and `M4` directly (e.g. `">="&M3` and `"<="&M4`). No hardcoded date offsets are allowed in the sheet.
2. **Exclusion of Internal Transfers**:
   * To prevent inflated cashflow figures, internal transfers (transactions matching account transfer category `'Transfer'` or `'Transfer internal'`) MUST be excluded from inflows and outflows.
3. **Liabilities Aggregation Verification**:
   * Total liabilities is `Total Hutang` + `Cicilan Rumah`. Both sheets `'🤝 Hutang'` and `'🏠 Cicilan Rumah'` must be verified to have disjoint account labels and records so no mortgage debt is reflected under general debt.
4. **Technical Ops Cleanliness**:
   * No technical variables (`deployment_id`, `safe_trigger_count`, `script_version`) may be read or written inside `A1:K41`. These variables must reside exclusively in `_AIRO_Ops_Center`.

---

## 4. Overall Readiness Recommendation

* **Wallet & Cashflow, ECC, Domain Health, Spending, Quality Center boards**: **READY (YES)**. Pure Google Sheets formulas are defined and fully compatible.
* **Smart Insight Panel & Action Required list**: **READY WITH FALLBACK (YES_WITH_FALLBACK)**. These elements require Apps Script to process the transaction datasets and evaluate narrative advice text. Pure spreadsheet formulas cannot construct the warning strings; the script must calculate them on every synchronization trigger and write plain text values into the merged cells.

No formula wiring code is implemented in this phase.
