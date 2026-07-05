# AIRO Finance Dashboard Lite — V2 Range and Style Mapping Analysis Report

**Date/time:** 2026-07-05 10:06 Asia/Jakarta  
**Status:** OWNER_CANDIDATE_REVIEW_BLOCKED  
**Scope:** DOCS_ONLY_FROM_EXISTING_READBACK_OUTPUT  
**Raw output file:** `/tmp/airo_task10_5y_range_style_helper_20260705_095753.txt`

---

## 1. Analysis of `🏠 Dashboard v2` Template Layout
The visual style mapping check returned the exact coordinates and spacing patterns of the template:

### Grid Structure
- **Columns (A to K)**: Widths pattern = `[9, 111, 90, 167, 90, 9, 125, 69, 83, 97, 9]`
  - Left panel (spending categories & wallets): Columns B, C, D, E.
  - Margin separator: Column F (9px width).
  - Right panel (spending subcategories & domains): Columns G, H, I, J.
- **Inspected Area**: `A1:K35` (perfectly bounds the cockpit layout).
- **Row Heights**: Bounded area heights range from 6px to 48px:
  - Title row (Row 2): 34px.
  - Card title blocks: 29px.
  - Table rows (spending, wallets, domains): 34px.

### Visual Themes & Typography
- **Backgrounds**:
  - Main cockpit background (e.g. `B1`): `#1c1c1e` (Dark Gray).
  - Active headers/filters (e.g. `B2`, `B4`): `#2a2a2e` (Medium Dark Gray).
  - Data cards background (e.g. `B5`, `G5`): `#1e1e1e` (Sleek Panel Dark).
  - Font colors: `#e8e8e8` (soft white) and `#8a8a8e` (light gray) for high readability. No default black text.

---

## 2. Proposed Dashboard Lite Placement Map
To adopt the V2 template layout while keeping content simplified, we will map Lite content directly into the pre-styled zones:

| Section | V2 Template Target Range | Structure/Merges | Lite Content Payload |
| :--- | :--- | :--- | :--- |
| **Topbar & Filters** | `B1:K3` | Merged title box, filter cells `G2='Juni'`, `I2='2026'` | Sync date & period |
| **Wallets Card** | `B16:C21` | Rows 17-20 content, Row 21 Total | Top 4 active wallets + 1 "Lainnya" row |
| **Credit Card Card** | `G17:J17` | Standard horizontal card | Unbilled/Due balance, Safe status |
| **Emas Card** | `G19:J19` | Standard horizontal card | Total gram & current market value |
| **Cicilan Rumah Card**| `G20:J20` | Standard horizontal card | Progress count (`53 / 120`), progress % |
| **Category Spending** | `B24:E31` | Rows 25-30 content, Row 31 Total | Top 5 categories + 1 "Lainnya" row |
| **Subcat Spending** | `G24:J31` | Rows 25-30 content (G:I merged) | Top 5 subcategories + 1 "Lainnya" row |

---

## 3. Cleansing Constraints (What to Avoid & Clear)
To maintain the "Lite" simplicity and visual cleanliness:
1. **Clear Wallet LEVEL/STATUS columns**: Clear `D17:E21` content and formatting to keep wallets clean.
2. **Clear Action Required Panel**: Clear `B4:K6` (removes large unnecessary blank space).
3. **Clear Secondary Action Panel**: Clear `B12:K13` (removes secondary metrics to simplify).
4. **Clear Data Quality Center**: Clear `G21:K35` entirely to clean up the right panel below the domain cards.
5. **No Style Overwrites**: Do not delete formatting or colors. Use `clearContent()` instead of `clear()` to keep background grid colors.
