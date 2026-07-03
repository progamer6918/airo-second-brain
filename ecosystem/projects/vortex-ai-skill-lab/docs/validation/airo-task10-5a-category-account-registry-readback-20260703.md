# AIRO Task 10.5A — Category & Account Registry Readback Snapshot Report

**Date:** 2026-07-03 21:10:53  
**Status:** Read-only Registry Ingest PASS  
**Scope:** REGISTRY_READBACK_AND_DOCS_SNAPSHOT_ONLY  
**Target Workbook ID:** `1CKARXGurxZ0Rby3-_iisVS0_r65JM6ZaT6tbAJUF7sU`

---

## 1. Account Registry Snapshot

- **Total Rows:** 11 rows
- **Columns:** active, account_id, account_name, aliases, parent_account, pocket_name, account_type, dashboard_group, font_color_hex, fill_color_hex

| Active | Account ID | Account Name | Aliases | Parent Account | Pocket Name | Account Type | Dashboard Group | Font Color | Fill Color |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TRUE | ACC001 | Blu | blu, blu bca digital |  |  | Bank | Blu | #0284C7 | #E0F2FE |
| TRUE | ACC002 | Blu Pocket | blu pocket, pocket blu | Blu | General Pocket | Pocket | Blu | #0891B2 | #CFFAFE |
| TRUE | ACC003 | BCA | bca, rekening bca |  |  | Bank | BCA | #1E3A8A | #DBEAFE |
| TRUE | ACC004 | BCA Pocket | bca pocket, pocket bca | BCA | General Pocket | Pocket | BCA | #4338CA | #E0E7FF |
| TRUE | ACC005 | Cash Umum | cash, tunai, uang cash, cash umum | Cash |  | Cash | Cash | #15803D | #DCFCE7 |
| TRUE | ACC006 | Cash Bensin | cash bensin, uang bensin | Cash |  | Cash | Cash | #7A7C00 | #FEF3C7 |
| TRUE | ACC007 | Credit Card | cc, kartu kredit, credit card |  |  | Credit | Credit Card | #7E22CE | #F3E8FF |
| TRUE | ACC008 | Cash Makan | cash makan | Cash |  | Cash | Cash | #B45309 | #FFEDD5 |
| TRUE | ACC009 | Unknown | unknown, tidak diketahui |  |  | Unknown | Unknown | #B45309 | #FFEDD5 |
| 💡  CARA MENAMBAH POCKET BARU: Tambah baris baru → isi account_name (mis: 'BCA Tabungan'), isi parent_account dengan nama bank induk (mis: 'BCA'), isi account_type = 'Pocket', samakan dashboard_group dengan parent. |  |  |  |  |  |  |  |  |  |
| TRUE | blu_pocket_cc | Blu Pocket CC | Blu | bank | Blu | pocket cc | Blu | #4CD2FF | FALSE |


*Note: Includes helper row at index 10 and special `blu_pocket_cc` at index 11.*

---

## 2. Category Registry Grouped Table

- **Total Registry Rows:** 85 rows
- **Columns:** active, category, subcategory, aliases, transaction_scope, display_order, dashboard_group, requires_review

| Category | Transaction Scope | Subcategories |
| :--- | :--- | :--- |
| Food & Drink | Expense | Jajan, Makan di Luar, Kopi, Makan Siang |
| Transport | Expense | Ride Hailing, Parkir, Bensin, Tol, Transport Umum |
| Groceries | Expense | Belanja Harian, Belanja Bulanan, Kebutuhan Pokok, Peralatan Rumah, Others |
| Utilities | Expense | Listrik, Air, Internet, Pulsa & Data, Gas, Sampah |
| Pets | Expense | Pet Food, Vet, Grooming, Accessories, Medicine |
| Health | Expense | Medicine, Doctor, Hospital, Dental, Laboratory |
| Personal Care | Expense | Skincare, Haircut, Salon, Toiletries |
| Subscriptions | Expense | Digital, Streaming, Software, Cloud |
| Fees & Admin | Expense | Admin Bank, Transfer Fee, Penalty, Tax |
| Housing | Expense | Rent, Maintenance, Furniture, Renovation |
| Insurance | Expense | Asuransi Jiwa, Asuransi Kesehatan, BPJS, Asuransi Kendaraan |
| Lifestyle & Entertainment | Expense | Hiburan, Hobi, Bioskop, Game, Belanja Umum |
| Giving & Family | Expense | Hadiah, Keluarga, Donasi, Zakat & Sedekah |
| Education | Expense | Course, Books, Tuition, Certification |
| Savings | Transfer | Dana Darurat, Transfer Tabungan, Sinking Fund |
| Investment | Asset | Emas, Saham, Reksadana, Deposito |
| Income | Income | Salary, Refund, Bonus, Freelance, Interest, Gift Received |
| Other / Review | Review | Review |
| Debt & Obligations | Debt | Cicilan Rumah, Bayar Hutang Mamak |
| CC Payment |  |  |
| Credit Card Payment |  |  |
| Transfer |  |  |


---

## 3. Existing Category Prompt Behavior

1. **Hardcoded Category Choice Maps:**
   - In `airoSprint7FResolveAnswerLabel_`, choice letters A/B/C/D map strictly to `"Food & Drink"`, `"Transport"`, `"Groceries"`, and `"Utilities"`.
   - In `normalizeMissingCategoryClarificationAnswer_`, mappings for A/B/C/D map to `'makan'`, `'transport'`, `'tagihan'`, and `'belanja'`.
   
2. **Current Limitations:**
   - When new categories or subcategories are added to `📚 Category Registry` sheet, they are rendered dynamically by `buildMissingCategoryClarificationMessage_` but choices cannot be resolved since the answer parser is hardcoded.
   - This creates an mismatch where selection fails or maps incorrectly.

---

## 4. Feasibility of One-Question Subcategory Prompt

- **Feasibility:** **HIGHLY FEASIBLE**
- **Analysis:** 
  - Most subcategories (e.g., `Rent`, `Ride Hailing`, `Pet Food`, `Skincare`) are unique across all categories.
  - The system can look up a user-selected subcategory in the `📚 Category Registry` and automatically resolve its parent category.
  - Overlapping subcategories (like `Medicine` in both `Health` and `Pets`) can be resolved using category-prefixing (e.g. `Health: Medicine` vs `Pets: Medicine`) or by checking the transaction context.
  
---

## 5. Scope Boundaries

- **Dashboard Sync:** **OUT OF SCOPE** (no dashboard changes or audits performed in this task).
- **Telegram Add Category/Subcategory:** **OUT OF SCOPE** (no commands to modify registry or prompt for custom entries).
- **Next Step:** Design the real Telegram category/subcategory flow (Task 10.5B).
