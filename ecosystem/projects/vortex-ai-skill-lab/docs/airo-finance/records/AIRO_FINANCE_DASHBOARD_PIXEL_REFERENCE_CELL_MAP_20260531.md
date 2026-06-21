# Dashboard Pixel-Reference Cell Map (Revised v2)

**Date**: 2026-05-31  
**Sprint Phase**: Dashboard Pixel-Reference Redesign Pass  
**Status**: **PENDING OWNER APPROVAL**

This document defines the exact layout grid, visual structure, data sources, and formatting rules of the redesigned **AIRO Finance Cockpit** to be built in the preview tab `🏠 Dashboard v2`. No code modifications will be executed until this design is approved.

---

## 1. Visual Cockpit Architecture

The main Dashboard is designed as a clean, user-facing personal finance cockpit. It is entirely free of raw operational metrics (such as clasp version, safe/live trigger counts, deployment IDs, and raw heartbeat logs).

All technical details are moved to a separate sheet called `_AIRO_Ops_Center` to keep the cockpit clean.

---

## 2. Spreadsheet Grid Cell Map (`🏠 Dashboard v2`)

Below is the exact row and column configuration mapped from row 1 to 95, across columns A to N.

### Column Mapping
- **Columns A–G (7 columns)**: Left-side cockpit panel.
- **Column H (1 column)**: Vertical divider spacer (fixed width: `20px`, background: `#121212`).
- **Columns I–N (6 columns)**: Right-side cockpit panel.

---

### Row-by-Row Layout Configuration

#### A1:N4 — Top Status Bar
- **A1:N1 Merged**: Cockpit Title -> "AIRO Finance Cockpit v2" (size 18, Bold, White, background `#2d2d2d`)
- **Row 2**: Metadata row (background `#1e1e1e`, text `#e0e0e0`)
  - `A2:B2` Merged: "Synced:" (label)
  - `C2:D2` Merged: Sync timestamp value (dynamic date format)
  - `E2:F2` Merged: "Data Status:" (label)
  - `G2`: Status Badge (`Trusted` [Green] / `Warning` [Amber] / `Dirty` [Red])
  - `I2:J2` Merged: "Month:" (label)
  - `K2:L2` Merged: Selector value (e.g. `'Mei 2026'`)
  - `M2`: Alert count badge (dynamic number of active issues)
  - `N2`: Menu indicator `[Menu]`
- **Row 3**: Border row (`A3:N3` Merged, `#333333` solid bottom border)
- **Rows 4-5**: Spacer rows (height `10px` total, background: `#121212`)

#### A6:N16 — Action Required (2x2 Cards)
- **A6:N6 Merged**: Section Header -> "🚨 ACTION REQUIRED" (background `#2d2d2d`, Bold, White)
- **Rows 7–11**: Action Card Row 1
  - `A7:G11` (Card 1: Left) -> Message, severity, action recommendation for issue 1.
  - `I7:N11` (Card 2: Right) -> Message, severity, action recommendation for issue 2.
- **Rows 12–16**: Action Card Row 2
  - `A12:G16` (Card 3: Left) -> Message, severity, action recommendation for issue 3.
  - `I12:N16` (Card 4: Right) -> Message, severity, action recommendation for issue 4.
- **Fallback Behavior**: If active issues < 4, empty slots show a clean placeholder card: `"Clean / No Action Required"` with a green checkmark visual and background `#1e1e1e`.
- **Row 17**: Spacer row (height `10px`, background: `#121212`)

#### A18:N35 — Executive Command Center KPI Cards
- **A18:N18 Merged**: Section Header -> "📊 EXECUTIVE COMMAND CENTER" (background `#2d2d2d`, Bold, White)
- **Rows 19–26 (Primary Cards Row)**:
  - `A19:C26` (Card 1: Net Worth) -> Displays Total Net Worth and Liquid Net Worth.
  - `D19:F26` (Card 2: Cash Tersedia) -> BCA, Blu, Mandiri, Cash total.
  - `G19:I26` (Card 3: Cashflow Bulan Ini) -> Pemasukan, Pengeluaran, Net cashflow.
  - `J19:N26` (Card 4: Critical Alerts) -> Dynamic count of critical issues + severity color.
- **Rows 27–34 (Secondary Cards Row)**:
  - `A27:C34` (Card 5: Total Aset) -> Live valuation of assets.
  - `D27:F34` (Card 6: Total Hutang) -> Outstanding debt.
  - `G27:J34` (Card 7: Saving Rate) -> Target vs actual percentage.
  - `K27:N34` (Card 8: Cicilan Rumah) -> Installments progress (e.g. 53/120).
- **Row 35**: Spacer row (height `10px`, background: `#121212`)

#### A36:N58 — Wallet & Domain Board
- **Split Section Headers (Row 36)**:
  - `A36:G36` Merged Left: "💳 WALLET & CASHFLOW" (background `#2d2d2d`, Bold, White)
  - `H36` Divider: Spacer (`#121212` background)
  - `I36:N36` Merged Right: "🧭 DOMAIN HEALTH" (background `#2d2d2d`, Bold, White)
- **Left Panel (Wallet Rows A37:G58)**:
  - Items: BCA, Blu, Mandiri, Cash bensin, Cash umum, Inflow, Outflow, Transfer internal.
  - Each item structure:
    - Col A: Account/Metric Label
    - Col B: Unicode progress bar (`██████░░░░`) relative to target threshold
    - Col C: Target limit
    - Col D: Current balance/value
    - Col E:G Merged: Status Pill (`Aman` [Green] / `Hampir Habis` [Amber] / `Kritis Rendah` [Red])
- **Right Panel (Domain Rows I37:N58)**:
  - Items: Credit Card, Hutang, Aset / Emas, Cicilan Rumah.
  - Each item structure:
    - Col I: Color block / icon
    - Col J: Label + Subtitle
    - Col K:L Merged: Value (formatted currency)
    - Col M:N Merged: Status Pill
- **Row 59**: Spacer row (height `10px`, background: `#121212`)

#### A60:N78 — Spending & Quality Board
- **Split Section Headers (Row 60)**:
  - `A60:G60` Merged Left: "🎯 SPENDING INTELLIGENCE" (background `#2d2d2d`, Bold, White)
  - `H60` Divider: Spacer (`#121212` background)
  - `I60:N60` Merged Right: "🔍 DATA QUALITY CENTER" (background `#2d2d2d`, Bold, White)
- **Left Panel (Spending Rows A61:G78)**:
  - Items: Makanan, Transport, CC payment, Utilities, Bensin, Lainnya.
  - Each item structure:
    - Col A: Category name
    - Col B: Unicode progress bar (`████████░░`)
    - Col C: Percentage (amount / total spending)
    - Col D:G Merged: Trend Delta (e.g. `+5% vs last month` or `-2% vs last month` with arrow/colors)
- **Right Panel (Quality Checks Rows I61:N78)**:
  - Items: CC payment belum match, Finance Events tanpa domain ref, Pending clarification, Missing category, Rekonsiliasi terakhir clean, Audit log.
  - Each check structure:
    - Col I:L Merged: Checklist description (User-Facing only; no trigger or runtime code metadata)
    - Col M:N Merged: Check status pill (`OK` [Green] / `WARNING` [Amber] / `CRITICAL` [Red])
- **Row 79**: Spacer row (height `10px`, background: `#121212`)

#### A80:N95 — Smart Insight Panel
- **A80:N80 Merged**: Section Header -> "💡 SMART INSIGHTS" (background `#2d2d2d`, Bold, White)
- **Rows 81–94 (2-Column Narrative Layout)**:
  - **Left side (Columns A-G)**:
    - `A81:G87` Merged Card: **Critical** narrative card (red border/accent text). Actionable alert info.
    - `A88:G94` Merged Card: **Warning** narrative card (amber border/accent text). Actionable warning details.
  - **Right side (Columns I-N)**:
    - `I81:N87` Merged Card: **Positive** narrative card (green border/accent text). Positive milestones.
    - `I88:N94` Merged Card: **Info** narrative card (blue border/accent text). General financial recommendations.
- **Row 95**: Spacer row (height `10px`, background: `#121212`)

---

## 3. General Styling and Technical Offloads

- **Target Preview Tab**: The build function will create this layout inside a new tab named `🏠 Dashboard v2` for initial inspection.
- **Theme Palette**: 
  - Main background: `#121212` (deep charcoal)
  - Card background: `#1e1e1e` (charcoal)
  - Headers: `#2d2d2d` (dark slate)
  - Borders: `#333333` solid
- **Typography**: Font family `'Roboto'` applied across all cells in A1:N95.
- **Offloaded Ops Tab**: Technical/operational metrics (`Live Trigger Count`, `Safe Trigger Count`, `Last Safe/Live Heartbeat` logs, deployment ID, runtime version, and raw Script Properties) are stored in `_AIRO_Ops_Center` (hidden tab) and excluded from `🏠 Dashboard v2`.
