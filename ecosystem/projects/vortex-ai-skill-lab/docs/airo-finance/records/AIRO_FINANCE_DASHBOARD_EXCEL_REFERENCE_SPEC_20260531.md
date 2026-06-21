# AIRO Finance Dashboard Excel-Reference Spec

**Document Date**: 2026-05-31  
**Target File**: `AIRO_Finance_Dashboard.xlsx`  
**Target Google Sheets Preview Tab**: `🏠 Dashboard v2`  
**Status**: **PENDING OWNER APPROVAL**

This document establishes the exact layout geometry, styling tokens, formulas, and dynamic period filtering behavior for the clone of the canonical Excel sheet `Dashboard` inside Google Sheets `🏠 Dashboard v2`.

---

## 1. Grid & Column Specifications

The dashboard follows a strict two-column layout with padding and divider columns. Total used range is **A1:K41**.

| Column | Width (Excel) | Use / Role | Alignment (Default) |
| :--- | :--- | :--- | :--- |
| **Col A** | `1.5` | Left-side margin padding spacer | Left |
| **Col B** | `16.0` | Left panel Labels (Akun / Kategori / Action Required details) | Left |
| **Col C** | `13.0` | Left panel Saldo / % metric values | Right / Center |
| **Col D** | `24.0` | Left panel Unicode Progress Bars / Primary KPIs | Left / Center |
| **Col E** | `13.0` | Left panel Status Pills / Trend indicators | Center / Right |
| **Col F** | `1.5` | Middle vertical divider spacer | Left |
| **Col G** | `18.0` | Right panel Labels (Domain / Issue / Action Required details) | Left |
| **Col H** | `10.0` | Right panel secondary text / info details | Left |
| **Col I** | `12.0` | Right panel values / secondary KPIs | Right / Center |
| **Col J** | `14.0` | Right panel Status Pills / Action labels | Center |
| **Col K** | `1.5` | Right-side margin padding spacer | Left |

---

## 2. Row Specifications & Fills

| Row Range | Height | Header / Content Section | Background Hex | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Row 1** | `5.0`pt | Top padding spacer | `#1C1C1E` | |
| **Row 2** | `26.0`pt | Dynamic Topbar | `#2A2A2E` | Sync, Data status, alerts, month, mode |
| **Row 3** | `6.0`pt | Spacer row | `#1C1C1E` | |
| **Row 4** | `22.0`pt | Action Required Section Header | `#2A2A2E` | `⚡ ACTION REQUIRED` |
| **Row 5** | `26.0`pt | Action Required Card Row 1 (Critical) | `#3D1515` | Critical Alerts (Red) |
| **Row 6** | `26.0`pt | Action Required Card Row 2 (Warning) | `#3D2D0F` | Warning Alerts (Orange) |
| **Row 7** | `8.0`pt | Spacer row | `#1C1C1E` | |
| **Row 8** | `22.0`pt | Executive Command Center Section Header| `#2A2A2E` | `🎯 EXECUTIVE COMMAND CENTER` |
| **Row 9** | `20.0`pt | Executive KPIs Headers (Primary) | `#2D2D32` | Cell J9 has `#3D1515` fill |
| **Row 10** | `36.0`pt | Executive KPIs Values (Primary) | `#2D2D32` | Cells J10 & K10 have `#3D1515` fill |
| **Row 11** | `8.0`pt | Spacer row | `#1C1C1E` | |
| **Row 12** | `20.0`pt | Executive KPIs Headers (Secondary) | `#232328` | |
| **Row 13** | `30.0`pt | Executive KPIs Values (Secondary) | `#232328` | Progress bar in I13 |
| **Row 14** | `8.0`pt | Spacer row | `#1C1C1E` | |
| **Row 15** | `22.0`pt | Wallet & Domain Boards Split Headers | `#2A2A2E` | `💳 WALLET & CASHFLOW` / `🏦 DOMAIN HEALTH` |
| **Row 16** | `20.0`pt | Column Headers for Wallet & Domain Boards | `#2A2A2E` | |
| **Row 17-21**| `26.0`pt | Individual Wallet & Domain Health Rows | `#1C1C1E` | Highlight fills in E17-E21 & J17-J20 |
| **Row 22** | `22.0`pt | Inflow/Outflow summary / Domain sources | `#2A2A2E` | G22:J22 merged, background `#2A2A2E` |
| **Row 23** | `8.0`pt | Spacer row | `#1C1C1E` | |
| **Row 24** | `22.0`pt | Spending & Quality Split Headers | `#2A2A2E` | `📊 SPENDING` / `🔍 DATA QUALITY` |
| **Row 25** | `20.0`pt | Column Headers for Spending & Quality | `#2A2A2E` | |
| **Row 26-31**| `26.0`pt | Individual Category & Quality Check Rows | `#1C1C1E` | Merged G26:I26 to G31:I31, special fills |
| **Row 32** | `14.0`pt | Formula details & sources footer row | `#2A2A2E` | B32:E32 & G32:J32 merged |
| **Row 33** | `8.0`pt | Spacer row | `#1C1C1E` | |
| **Row 34** | `36.0`pt | Smart Insight Narrative Row 1 (Critical) | `#3D1515` | Merged B34:E34 & G34:J34 |
| **Row 35** | `36.0`pt | Smart Insight Narrative Row 2 (Warning) | `#3D2D0F` | Merged B35:E35 & G35:J35 |
| **Row 36** | `36.0`pt | Smart Insight Narrative Row 3 (Pos/Info) | Varying | B36:E36 (`#1A3D25`), G36:J36 (`#1A2D42`) |
| **Row 37** | `8.0`pt | Spacer row | `#1C1C1E` | |
| **Row 38-41**| `15.0`pt | Bottom Margin Buffer Rows | `#1C1C1E` | Spacer area |

---

## 3. Theme Styling and Typography Tokens

To ensure high-fidelity Parity styling, the Google Sheet builder must apply these styling rules:

### A. Color Palette
- **Sheet Background**: Deep Charcoal (`#1C1C1E`) — applied as the default background for all cell ranges outside of card containers.
- **Section Headers & Topbar**: Slate Gray (`#2A2A2E`) with light-gray text (`#8A8A8E` for metadata/labels, `#E8E8E8` for selectors).
- **Primary Cards Background**: Charcoal Slate (`#2D2D32`).
- **Secondary Cards Background**: Dark Charcoal (`#232328`).
- **Accent Status Colors**:
  - **Critical Alert**: Background `#3D1515`, Font `#FF6B6B` (Red)
  - **Warning Alert**: Background `#3D2D0F`, Font `#FFAA40` (Amber/Orange)
  - **Positive / Aman**: Background `#1A3D25`, Font `#5FD87A` (Green)
  - **Info / On Track**: Background `#1A2D42`, Font `#5AAFF0` (Blue)
  - **Stale / Normal Text**: `#FFE8E8E8` (Light Gray/White)
  - **Label / Subtitle**: `#FF8A8A8E` or `#FF555558` (Dark Gray)

### B. Typography
- **Primary Font Family**: `Arial` for all labels, amounts, and headers.
- **Monospace Font Family**: `Courier New` (Size `12.0`, Normal weight) exclusively for cells containing unicode progress bars (`D17:D21`, `D26:D31`, `I13`).
- **Font Sizes**:
  - Net Worth / Cash / Cashflow large displays: `15.0`pt (Bold)
  - Secondary Cards (Asset/Hutang/Saving): `13.0`pt (Bold)
  - Primary text: `10.0`pt
  - Header text / status badges / action badges: `9.0`pt (Bold for badges)
  - Subtitles / metadata details: `8.0`pt

---

## 4. Merged Cells Matrix

The sheet must strictly apply these cell merges (and unmerge any pre-existing merges in their target ranges):
- **G22:J22** (Domain health summary note)
- **G26:I26** to **G31:I31** (Data Quality Center issues list)
- **B32:E32** (Spending Intelligence summary formula label)
- **G32:J32** (Data Quality Center source logs note)
- **B34:E34** / **B35:E35** / **B36:E36** (Smart Insight Left narratives)
- **G34:J34** / **G35:J35** / **G36:J36** (Smart Insight Right narratives)

---

## 5. Dynamic Month Selector & Period Filter Architecture

To satisfy the requirement that G2 acts as a dynamic month filter, the following structure will be established:

### A. The Dropdown Selector (Cell `G2`)
- **Location**: `G2`
- **Data Validation**: A dropdown linked to actual date values (the 1st of each month in the dataset, e.g., `2026-04-01`, `2026-05-01`, `2026-06-01`, etc.).
- **Formatting**: Number format set to `'📅 'mmmm yyyy` (displays as `📅 Mei 2026` or similar, but contains the raw date object `2026-05-01`).

### B. Hidden Helper Date Cells (Columns `M2:M6`)
We reserve columns `L` and `M` for logic. These columns are kept unformatted (or hidden) to keep the cockpit clean.
- **`M2` (selected_month_label)**: `=TEXT(G2, "mmmm yyyy")`
- **`M3` (period_start)**: `=G2`
- **`M4` (period_end)**: `=EOMONTH(G2, 0)`
- **`M5` (previous_period_start)**: `=EDATE(G2, -1)`
- **`M6` (previous_period_end)**: `=EOMONTH(EDATE(G2, -1), 0)`

---

## 6. Dynamic Card & Table Formulas

All data cards must derive their values dynamically from `period_start` (`M3`) and `period_end` (`M4`) using formula patterns:

### A. Executive Command Center (Primary)
- **Net worth** (`D10`):
  ```excel
  =SUMIFS('Asset Valuation'!D:D, 'Asset Valuation'!A:A, "<="&M4) - SUMIFS('Hutang Valuation'!D:D, 'Hutang Valuation'!A:A, "<="&M4)
  ```
- **Cash tersedia** (`E10`):
  Calculates the sum of BCA, Blu, Mandiri, Cash bensin, and Cash umum balances as of `period_end`.
- **Cashflow bln ini** (`G10`):
  ```excel
  =SUMIFS('Finance Events'!D:D, 'Finance Events'!B:B, "Inflow", 'Finance Events'!A:A, ">="&M3, 'Finance Events'!A:A, "<="&M4) - SUMIFS('Finance Events'!D:D, 'Finance Events'!B:B, "Outflow", 'Finance Events'!A:A, ">="&M3, 'Finance Events'!A:A, "<="&M4)
  ```
- **Critical Alerts** (`J10`):
  Counts active critical checks in the Data Quality panel:
  ```excel
  =COUNTIF(J26:J31, "1 item") + COUNTIF(J26:J31, "critical*")
  ```

### B. Executive Command Center (Secondary)
- **Total Aset** (`C13`): Sum of assets at `period_end`.
- **Total Hutang** (`E13`): Sum of debts at `period_end`.
- **Saving rate** (`G13`): Dynamic ratio:
  ```excel
  =IF(Inflow_Total=0, 0, (Inflow_Total - Outflow_Total) / Inflow_Total)
  ```
- **Cicilan rumah** (`I13`): Unicode progress string showing amount paid relative to total principal.

### C. Progress Bar Cells
The unicode progress bars are generated dynamically with formulas:
- **Wallet progress formula** (e.g. `D17`):
  ```excel
  =REPT("█", MIN(10, ROUND(Current_Balance / Target_Limit * 10))) & REPT("░", 10 - MIN(10, ROUND(Current_Balance / Target_Limit * 10)))
  ```
- **Monospace Font**: Placed in `D17:D21`, `D26:D31`, and `I13` to prevent character misalignment.

### D. Spending Category Percentages
- **Category %** (e.g., `C26` for Makanan):
  ```excel
  =SUMIFS('Finance Events'!D:D, 'Finance Events'!C:C, "Makanan", 'Finance Events'!A:A, ">="&M3, 'Finance Events'!A:A, "<="&M4) / Total_Outflow
  ```

### E. Data Quality Check counts
- **Counts** (`J26:J31`): Calculated dynamically by checking the Review Queue and Finance Events sheets for issues with timestamps falling in `[M3, M4]`.

---

## 7. Apps Script / Server-Driven Updates

For components that cannot be easily written as pure Google Sheets formulas (such as generating specific text warnings in the **Action Required** card list or **Smart Insight Panel**):
- When trigger updates execute, the Apps Script code must read G2:
  ```javascript
  const sheet = ss.getSheetByName("🏠 Dashboard v2");
  const selectedPeriodStart = sheet.getRange("M3").getValue(); // period_start
  const selectedPeriodEnd = sheet.getRange("M4").getValue();   // period_end
  ```
- All log counts, audit queue summaries, and card recommendation generation must filter transaction data by `selectedPeriodStart` and `selectedPeriodEnd` before outputting narrative cards.
- If no date is selected or invalid, the script defaults to the current active calendar month as fallback.
