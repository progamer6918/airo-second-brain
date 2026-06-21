# AIRO Finance - Sprint 3 Cash Ledger Removal Audit

Status: AUDIT STARTED
Sprint: Sprint 3 - Cash Ledger Removal
Generated at: 2026-05-24 14:36:59
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

Sprint 3 starts after Sprint 2 Domain Tab Maturation is CLOSED / PASS.

This micro-step audits all Cash Ledger dependency surfaces before any runtime removal.

No runtime patch is made in this micro-step.

## 2. Sprint 3 Boundary

Allowed now:

- inspect Cash Ledger runtime dependencies
- inspect Account Ledger replacement coverage
- inspect tests that guard Cash Ledger and Account Ledger behavior
- write deletion-safety plan
- define smallest safe test-first patch

Not allowed now:

- deleting Cash Ledger code
- deleting Cash Ledger tab support
- deleting dashboard formulas
- changing Account Ledger schema
- Finance Events implementation
- Email Ingestion implementation
- broad Apps Script refactor

## 3. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `writeCashLedger_` | 1474-1509 | FOUND | AIRO_CONFIG.tabs.cash:1, writeCashLedger_:1, syncCashLedgerRuntimeAmountColumns_:1, amount_start:1, amount_remaining:1, amount_in:1, amount_out:1, linked_txn_id:1, entry_id:1 |
| `syncCashLedgerRuntimeAmountColumns_` | 1463-1472 | FOUND | AIRO_CONFIG.tabs.cash:1, syncCashLedgerRuntimeAmountColumns_:1, amount_in:1, amount_out:1 |
| `writeAccountLedgerMirror_` | 1516-1570 | FOUND | AIRO_CONFIG.tabs.accountLedger:2, writeAccountLedgerMirror_:1, amount_in:1, amount_out:1, cash_in:1, cash_out:1, source_tab:1, linked_txn_id:3, entry_id:1 |
| `writeRouted_` | 1693-1735 | FOUND | AIRO_CONFIG.tabs.cash:1, AIRO_CONFIG.tabs.accountLedger:1, writeCashLedger_:1, writeAccountLedgerMirror_:2 |
| `writeInternalTransferToAccountLedger_` | 7448-7511 | FOUND | AIRO_CONFIG.tabs.accountLedger:1, writeCashLedger_:2, writeAccountLedgerMirror_:2, linked_txn_id:3, Cash Ledger:1 |
| `ensureAccountLedgerSheet_` | 1577-1611 | FOUND | AIRO_CONFIG.tabs.accountLedger:2, amount_in:1, amount_out:1, source_tab:1, linked_txn_id:1, entry_id:1 |
| `appendByHeader_` | 2000-2047 | FOUND |  |
| `findCashLedgerExactHeaderCol_` | 1449-1461 | FOUND |  |
| `auditCashLedgerAccountLedgerRuntime_` | MISSING | MISSING |  |
| `backfillCashLedgerToAccountLedger_` | MISSING | MISSING |  |
| `repairAccountLedgerSourceTab_` | MISSING | MISSING |  |
| `repairMissingAccountLedgerRowsFromCash_` | MISSING | MISSING |  |
| `setupDashboardCashLedgerPanel_` | MISSING | MISSING |  |
| `setupMonthlyCashLedgerPanel_` | MISSING | MISSING |  |

## 4. Existing Test Candidates

- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py

## 5. Risk Notes

- Cash Ledger tab is still referenced in runtime; deletion must be staged, not direct.
- writeCashLedger_ still exists; removal requires a compatibility plan or routing replacement.
- Cash Ledger runtime amount-column sync still exists; removal must verify no writer still needs it.
- writeRouted_ still routes Cash tab behavior; removal must preserve Account Ledger mirror first.
- Cash-specific amount_start / amount_remaining fields still exist; dashboard/formula dependencies must be audited before deletion.
- Repair/backfill surfaces exist; deletion must preserve rollback/recovery strategy.
- Account Ledger mirror has source_tab and linked_txn_id, which are required before Cash Ledger removal.

## 6. Deletion-Safety Plan

Cash Ledger removal must be staged.

### Stage A - Lock Current Dependency Map

- Add/verify tests for every remaining `AIRO_CONFIG.tabs.cash` dependency.
- Add/verify tests for every `writeCashLedger_` call path.
- Add/verify tests for dashboard/monthly formulas that currently read Cash Ledger.
- Add/verify tests for Account Ledger fields replacing Cash Ledger fields.

### Stage B - Prove Account Ledger Replacement

Before deleting Cash Ledger, Account Ledger must provide:

- `amount_in`
- `amount_out`
- `source_tab`
- `linked_txn_id`
- cash movement row identity
- internal transfer two-side identity
- CC/debt/asset wallet outflow identity

### Stage C - Disable New Writes Before Deleting Reads

Removal order must be:

1. prove tests pass while Cash Ledger remains
2. stop new Cash Ledger writes behind a guarded compatibility path
3. verify Account Ledger writes remain complete
4. migrate dashboard/monthly reads away from Cash Ledger
5. only then remove Cash Ledger runtime dependency

### Stage D - Rollback Guard

Before any deletion patch, keep a rollback path:

- no schema destructive operation
- no historical row deletion
- no tab deletion by script
- only code-path removal after tests prove Account Ledger parity

## 7. Sprint 3 Readiness Matrix

| Area | Ready for deletion now? | Reason |
|---|---:|---|
| Cash Ledger writer | No | Dependency map must be locked first |
| Cash Ledger amount_start / amount_remaining | No | Formula/dashboard dependencies must be audited |
| Dashboard/monthly reads | No | Must be migrated after parity tests |
| Account Ledger mirror | Partially | Sprint 1 guards are present, but deletion-specific tests are still needed |
| Historical data | No | No destructive migration in Sprint 3 audit step |
| Cash Ledger tab deletion | No | Explicit non-goal until all replacement reads pass |

## 8. Recommended Next Patch

Add the smallest test-only Cash Ledger removal-safety contract first.

The regression should lock:

- `writeCashLedger_` still mirrors to Account Ledger
- `writeRouted_` still uses Account Ledger mirror for cash movements
- Account Ledger supports `amount_in`, `amount_out`, `source_tab`, and `linked_txn_id`
- Cash Ledger deletion is not allowed until dashboard/monthly dependencies are audited
- no script deletes the Cash Ledger tab

## 9. Direct Source Findings

| Line | Source Text |
|---:|---|
| 15 | cash: '💵 Cash Ledger', |
| 20 | accountLedger: '📒 Account Ledger', |
| 131 | if (/^(a\|1)$/i.test(t) \|\| /\b(masuk\|terima\|diterima\|income\|pemasukan)\b/i.test(t)) return 'cash_in'; |
| 132 | if (/^(b\|2)$/i.test(t) \|\| /\b(keluar\|kepake\|terpakai\|pakai\|bayar\|beli\|expense\|pengeluaran)\b/i.test(t)) return 'cash_out'; |
| 174 | if (direction === 'cash_in') return ('cash masuk ' + amount + ' ' + tail).trim(); |
| 175 | if (direction === 'cash_out') return ('cash keluar ' + amount + ' ' + tail).trim(); |
| 1449 | function findCashLedgerExactHeaderCol_(sheet, headerName) { |
| 1463 | function syncCashLedgerRuntimeAmountColumns_(ss, rowNumber, inflow, amount) { |
| 1465 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 1467 | const inCol = findCashLedgerExactHeaderCol_(sheet, 'amount_in'); |
| 1468 | const outCol = findCashLedgerExactHeaderCol_(sheet, 'amount_out'); |
| 1474 | function writeCashLedger_(ss, parsed, rawText, common) { |
| 1481 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1490 | amount_start: cashInflow ? parsed.amount : '', |
| 1491 | amount_remaining: cashInflow ? parsed.amount : '', |
| 1498 | amount_in: cashInflow ? parsed.amount : '', |
| 1499 | amount_out: cashInflow ? '' : parsed.amount, |
| 1504 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.cash, row, { createIfMissing: false }); |
| 1506 | syncCashLedgerRuntimeAmountColumns_(ss, result.row, cashInflow, parsed.amount); |
| 1513 | * Mirrors cash movement to the Account Ledger tab. |
| 1516 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1517 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1522 | const explicitInflowTypes = ['income', 'transfer_in', 'cash_in']; |
| 1523 | const explicitOutflowTypes = ['expense', 'transfer_out', 'cash_out', 'cc_payment', 'debt_payment', 'asset_purchase']; |
| 1542 | amount_in: isInflow ? amount : '', |
| 1543 | amount_out: isInflow ? '' : amount, |
| 1549 | source_tab: sourceTab, |
| 1550 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1554 | try { ensureAccountLedgerSheet_(ss); } catch (e) {} |
| 1555 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1559 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 1564 | applyAccountLedgerRowStyle_(sheet, r); |
| 1573 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1577 | function ensureAccountLedgerSheet_(ss) { |
| 1579 | 'entry_id', 'date', 'account', 'amount_in', 'amount_out', |
| 1581 | 'source_tab', 'linked_txn_id', 'notes' |
| 1585 | var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 1588 | sheet = ss.insertSheet(AIRO_CONFIG.tabs.accountLedger); |
| 1591 | styleAccountLedgerSheet_(sheet); |
| 1606 | styleAccountLedgerSheet_(sheet); |
| 1613 | function styleAccountLedgerSheet_(sheet) { |
| 1632 | applyAccountLedgerAccountStyles_(sheet); |
| 1643 | function accountLedgerFontColorForAccount_(account) { |
| 1653 | function applyAccountLedgerRowStyle_(sheet, row) { |
| 1657 | var color = accountLedgerFontColorForAccount_(account); |
| 1662 | function applyAccountLedgerAccountStyles_(sheet) { |
| 1669 | var color = accountLedgerFontColorForAccount_(values[i][0]); |
| 1683 | function isCashLedgerAccountName_(value) { |
| 1711 | return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer); |
| 1714 | if (key.includes('cash ledger')) { |
| 1715 | const cashResult = writeCashLedger_(ss, parsed, rawText, common); |
| 1717 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1724 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1728 | writtenTab: AIRO_CONFIG.tabs.accountLedger |
| 1751 | function mirrorAssetPurchaseToAccountLedger_(result) { |
| 1761 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 1763 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1767 | account_ledger_result: accountLedgerResult \|\| null |
| 1773 | return mirrorAssetPurchaseToAccountLedger_(appendGoldAssetRow_(sheet, parsed, rawText, common)); |
| 1778 | if (result.status === 'written') return mirrorAssetPurchaseToAccountLedger_({ ...result, writtenTab: tabName }); |
| 1818 | linked_txn_id: data.linked_txn_id, |
| 1908 | // Cash Ledger movement type validation. |
| 1916 | if (['expense', 'cash_out', 'transfer_out'].includes(type)) { |
| 2108 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2119 | if (headerKey === 'amount_start' \|\| headerKey.includes('amount_start')) { |
| 2120 | return data.amount_start ?? ''; |
| 2123 | if (headerKey === 'amount_remaining' \|\| headerKey.includes('amount_remaining')) { |
| 2124 | return data.amount_remaining ?? ''; |
| 2136 | headerKey === 'amount_out' \|\| |
| 2137 | headerKey.includes('amount_out') \|\| |
| 2138 | headerKey === 'cash_out' \|\| |
| 2139 | headerKey.includes('cash_out') \|\| |
| 2145 | return cashInflow ? '' : (data.amount_out ?? data.amount ?? ''); |
| 2149 | headerKey === 'amount_in' \|\| |
| 2150 | headerKey.includes('amount_in') \|\| |
| 2151 | headerKey === 'cash_in' \|\| |
| 2152 | headerKey.includes('cash_in') \|\| |
| 2158 | return cashInflow ? (data.amount_in \|\| data.amount \|\| '') : (data.amount_in ?? ''); |
| 2169 | if (headerKey === 'source_tab' \|\| headerKey.includes('source_tab')) { |
| 2170 | return data.source_tab \|\| data.source \|\| ''; |
| 2194 | // Important: check amount_in / amount_out before generic amount, |
| 2195 | // otherwise amount_out may be filled as expense for cash inflow rows. |
| 2197 | h === 'amount_in' \|\| |
| 2198 | h.includes('amount_in') \|\| |
| 2199 | h === 'cash_in' \|\| |
| 2200 | h.includes('cash_in') \|\| |
| 2206 | return 'amount_in'; |
| 2210 | h === 'amount_out' \|\| |
| 2211 | h.includes('amount_out') \|\| |
| 2212 | h === 'cash_out' \|\| |
| 2213 | h.includes('cash_out') \|\| |
| 2219 | return 'amount_out'; |
| 2234 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2258 | if (/\b(cash\|tunai)\b/i.test(text)) return AIRO_CONFIG.tabs.cash; |
| 2491 | return isCashInflowText_(text) \|\| ['transfer_in', 'cash_in', 'income'].includes(type); |
| 2781 | return AIRO_CONFIG.tabs.cash; |
| 2844 | function refreshCashLedgerMaintenance() { |
| 2846 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 2883 | sheet.getRange(r, 3).setValue(amount);          // amount_start |
| 2884 | sheet.getRange(r, 5).setValue(amount);          // amount_remaining |
| 2898 | sheet.getRange(r, 16).clearContent();           // amount_out |
| 2899 | sheet.getRange(r, 17).setValue(amount);         // amount_in |
| 2901 | sheet.getRange(r, 16).setValue(amount);         // amount_out |
| 2902 | sheet.getRange(r, 17).clearContent();           // amount_in |
| 2908 | refreshCashMonthlyReviewFormulas(); |
| 2944 | function refreshCashMonthlyReviewFormulas() { |
| 2955 | const dashboard = |
| 2956 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 2957 | getSheetLoose_(ss, 'Dashboard'); |
| 2959 | const monthly = |
| 2960 | getSheetLoose_(ss, '📆 Monthly Review') \|\| |
| 2961 | getSheetLoose_(ss, 'Monthly Review'); |
| 2963 | const accountLedgerMonthKeyFormula = |
| 2964 | `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`; |
| 2966 | const accountLedgerCashAccountFilterFormula = |
| 2967 | `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`; |
| 2969 | const monthlyCashInFormula = |
| 2970 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2972 | const monthlyCashOutFormula = |
| 2973 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2975 | const monthlyNetFormula = |
| 2978 | const dashboardCashAktifFormula = |
| 2979 | `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`; |
| 2983 | dashboard: {}, |
| 2984 | monthly: {} |
| 2987 | if (monthly) { |
| 2988 | monthly.getRange('B6').setFormula(monthlyCashInFormula); |
| 2989 | monthly.getRange('E6').setFormula(monthlyCashOutFormula); |
| 2990 | monthly.getRange('B8').setFormula(monthlyNetFormula); |
| 2992 | result.monthly.cash_masuk = 'B6'; |
| 2993 | result.monthly.cash_keluar = 'E6'; |
| 2994 | result.monthly.net = 'B8'; |
| 2996 | result.monthly.missing = true; |
| 2999 | if (dashboard) { |
| 3000 | result.dashboard.cash_aktif = |
| 3001 | setFormulaOnCellContaining_(dashboard, ['cash aktif'], dashboardCashAktifFormula); |
| 3003 | result.dashboard.missing = true; |
| 3009 | function refreshCashMonthlyReviewFormulas() { |
| 3381 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 3795 | const dashboard = |
| 3796 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 3797 | getSheetLoose_(ss, 'Dashboard'); |
| 3803 | if (!dashboard) { |
| 3804 | return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 3808 | const panel = setupDashboardNetWorthPanel(); |
| 3820 | // Helper cells only. They may be hidden; dashboard is the visible panel. |
| 4094 | function setupDashboardCreditCardCyclePanel() { |
| 4097 | const dashboard = |
| 4098 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 4099 | getSheetLoose_(ss, 'Dashboard'); |
| 4105 | if (!dashboard) return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 4117 | ensureSheetSize_(dashboard, 38, 8); |
| 4118 | safeClearRange_(dashboard, 'B25:G34'); |
| 4185 | dashboard.getRange('B25:G25').merge(); |
| 4186 | dashboard.getRange('B25').setValue('💳 CREDIT CARD — TOKOPEDIA CC'); |
| 4188 | dashboard.getRange('B26:C26').merge().setValue('Tagihan Jatuh Tempo'); |
| 4189 | dashboard.getRange('D26').setValue(payableCycle.id); |
| 4190 | dashboard.getRange('E26:F26').merge().setValue(formatDateYmd_(payableCycle.start) + ' – ' + formatDateYmd_(payableCycle.end)); |
| 4191 | dashboard.getRange('G26').setValue('Due ' + formatDateYmd_(payableDueDate)); |
| 4193 | dashboard.getRange('B27:C27').merge().setValue('Total Tagihan'); |
| 4194 | dashboard.getRange('D27').setValue(stats.payable_total); |
| 4195 | dashboard.getRange('E27:F27').merge().setValue('Belum ke Blu'); |
| 4196 | dashboard.getRange('G27').setValue(stats.payable_belum_blu); |
| 4198 | dashboard.getRange('B28:C28').merge().setValue('Status'); |
| 4199 | dashboard.getRange('D28').setValue(overdue ? 'OVERDUE / CEK BLU' : (stats.payable_belum_blu > 0 ? 'PERLU SIAPKAN BLU' : 'AMAN')); |
| 4200 | dashboard.getRange('E28:F28').merge().setValue('Rows'); |
| 4201 | dashboard.getRange('G28').setValue(stats.payable_rows); |
| 4203 | dashboard.getRange('B30:C30').merge().setValue('Periode Berjalan / Unbilled'); |
| 4204 | dashboard.getRange('D30').setValue(currentCycle.id); |
| 4205 | dashboard.getRange('E30:F30').merge().setValue(formatDateYmd_(currentCycle.start) + ' – ' + formatDateYmd_(currentCycle.end)); |
| 4206 | dashboard.getRange('G30').setValue('Belum closing'); |
| 4208 | dashboard.getRange('B31:C31').merge().setValue('Total Sementara'); |
| 4209 | dashboard.getRange('D31').setValue(stats.unbilled_total); |
| 4210 | dashboard.getRange('E31:F31').merge().setValue('Belum ke Blu'); |
| 4211 | dashboard.getRange('G31').setValue(stats.unbilled_belum_blu); |
| 4213 | dashboard.getRange('B33:G33').merge(); |
| 4214 | dashboard.getRange('B33').setValue('Catatan: “Belum ke Blu” = dana bayar CC belum disiapkan di Pocket Blu khusus pembayaran CC.'); |
| 4216 | dashboard.getRange('D27:G27').setNumberFormat('"Rp" #,##0'); |
| 4217 | dashboard.getRange('D31:G31').setNumberFormat('"Rp" #,##0'); |
| 4219 | dashboard.getRange('B25:G25') |
| 4225 | dashboard.getRange('B26:G28') |
| 4229 | dashboard.getRange('B30:G31') |
| 4233 | dashboard.getRange('B33:G33') |
| 4237 | dashboard.getRange('B25:G33').setVerticalAlignment('middle'); |
| 4238 | dashboard.getRange('B26:C31').setFontWeight('bold'); |
| 4239 | dashboard.getRange('E26:F31').setFontWeight('bold'); |
| 4243 | dashboard_panel: 'B25:G33', |
| 4252 | tab_url: getSheetTabUrl_(ss, dashboard) |
| 4257 | function setupDashboardNetWorthPanel() { |
| 4260 | const dashboard = |
| 4261 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 4262 | getSheetLoose_(ss, 'Dashboard'); |
| 4264 | if (!dashboard) { |
| 4265 | return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 4268 | ensureSheetSize_(dashboard, 26, 8); |
| 4270 | // Visible dashboard panel area. |
| 4271 | safeClearRange_(dashboard, 'B16:G24'); |
| 4273 | dashboard.getRange('B16:G16').merge(); |
| 4274 | dashboard.getRange('B16').setValue('💰 NET WORTH & HOME EQUITY'); |
| 4277 | dashboard.getRange('B17:C17').merge().setValue('Total Aset Likuid'); |
| 4278 | dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`); |
| 4280 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4281 | dashboard.getRange('D18').setFormula(`=IFERROR('🥇 Aset'!F18;0)`); |
| 4283 | dashboard.getRange('B19:C19').merge().setValue('Net Worth Likuid'); |
| 4284 | dashboard.getRange('D19').setFormula('=IFERROR(D17-D18;0)'); |
| 4286 | dashboard.getRange('B20:C20').merge().setValue('Ekuitas Rumah'); |
| 4287 | dashboard.getRange('D20').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4289 | dashboard.getRange('B21:C21').merge().setValue('Net Worth Total'); |
| 4290 | dashboard.getRange('D21').setFormula('=IFERROR(D19+D20;0)'); |
| 4293 | dashboard.getRange('E17:F17').merge().setValue('Nilai Rumah Pasar'); |
| 4294 | dashboard.getRange('G17').setFormula(`=IFERROR('🥇 Aset'!AB17;0)`); |
| 4296 | dashboard.getRange('E18:F18').merge().setValue('Haircut Konservatif'); |
| 4297 | dashboard.getRange('G18').setFormula(`=IFERROR('🥇 Aset'!AB18;0)`); |
| 4299 | dashboard.getRange('E19:F19').merge().setValue('Nilai Rumah Konservatif'); |
| 4300 | dashboard.getRange('G19').setFormula(`=IFERROR('🥇 Aset'!AB19;0)`); |
| 4302 | dashboard.getRange('E20:F20').merge().setValue('Sisa Pokok Rumah'); |
| 4303 | dashboard.getRange('G20').setFormula(`=IFERROR('🥇 Aset'!AB20;0)`); |
| 4305 | dashboard.getRange('E21:F21').merge().setValue('Ekuitas Rumah'); |
| 4306 | dashboard.getRange('G21').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4308 | dashboard.getRange('B23:G23').merge(); |
| 4309 | dashboard.getRange('B23').setValue('Catatan: Net Worth Likuid tidak memasukkan rumah. Net Worth Total memasukkan ekuitas rumah konservatif.'); |
| 4312 | dashboard.getRange('D17:D21').setNumberFormat('"Rp" #,##0'); |
| 4313 | dashboard.getRange('G17:G21').setNumberFormat('"Rp" #,##0'); |
| 4314 | dashboard.getRange('G18').setNumberFormat('0.00%'); |
| 4316 | dashboard.getRange('B16:G16') |
| 4322 | dashboard.getRange('B17:C21') |
| 4326 | dashboard.getRange('E17:F21') |
| 4330 | dashboard.getRange('D19:D21') |
| 4334 | dashboard.getRange('G21') |
| 4338 | dashboard.getRange('B16:G21').setBorder(true, true, true, true, true, true); |
| 4340 | dashboard.getRange('B23:G23') |
| 4345 | dashboard.setColumnWidth(2, 135); // B |
| 4346 | dashboard.setColumnWidth(3, 95);  // C |
| 4347 | dashboard.setColumnWidth(4, 150); // D |
| 4348 | dashboard.setColumnWidth(5, 135); // E |
| 4349 | dashboard.setColumnWidth(6, 95);  // F |
| 4350 | dashboard.setColumnWidth(7, 150); // G |
| 4352 | dashboard.getRange('B16:G23').setVerticalAlignment('middle'); |
| 4356 | dashboard_panel: 'B16:G23', |
| 4357 | tab_url: getSheetTabUrl_(ss, dashboard) |
| 4421 | function dashboardLayoutReadOnlyAudit_(ss) { |
| 4422 | const dashboard = |
| 4423 | getSheetLoose_(ss, AIRO_CONFIG.tabs.dashboard) \|\| |
| 4424 | getSheetLoose_(ss, 'Dashboard'); |
| 4426 | if (!dashboard) { |
| 4429 | reason: 'dashboard_sheet_missing' |
| 4433 | const maxRows = Math.min(dashboard.getMaxRows(), 80); |
| 4434 | const maxCols = Math.min(dashboard.getMaxColumns(), 12); |
| 4435 | const values = dashboard.getRange(1, 1, maxRows, maxCols).getDisplayValues(); |
| 4472 | command: 'dashboard_layout_read_only_audit', |
| 4473 | sheet_name: dashboard.getName(), |
| 4714 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 4715 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 4816 | if (/^admin\s+(refresh\|sync\|update\|reload)\s+cc\s+(dashboard\|cycle\s+dashboard\|billing\s+dashboard\|tagihan\s+dashboard)/i.test(text)) { |
| 4817 | const result = setupDashboardCreditCardCyclePanel(); |
| 4822 | 'Credit Card Dashboard cycle panel direfresh.\n\n' + |
| 4828 | 'Panel: ' + ((result && result.dashboard_panel) \|\| '-') + '\n\n' + |
| 4829 | (link ? '🔗 Buka Dashboard: ' + link : '') |
| 4835 | command: 'cc_dashboard_cycle_refresh', |
| 4975 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5046 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5047 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5094 | const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16); |
| 5095 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5097 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5098 | const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5); |
| 5116 | cash_in_col: cashInCol, |
| 5117 | cash_out_col: cashOutCol, |
| 5127 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5128 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5178 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5180 | const cashAmountStartCol = findColumn_(cashInfo, ['amount_start', 'start_amount'], 3); |
| 5192 | (typeVal === 'income' \|\| typeVal === 'transfer_in' \|\| typeVal === 'cash_in' \|\| statusVal === 'aktif') |
| 5201 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5203 | const accountSourceCol = findColumn_(accountInfo, ['source_tab', 'source'], 11); |
| 5216 | if (isCashLedgerAccountName_(account) && amount > 0) { |
| 5262 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5264 | 'Cash Ledger inflows recent/top:\n' + |
| 5269 | 'Buka Account Ledger: ' + link |
| 5291 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5292 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5343 | const sumCashLedgerInWithFallback_ = function(sheet, cashInCol, info) { |
| 5347 | const amountStartCol = findColumn_(info, ['amount_start', 'start_amount'], 3); |
| 5360 | (typeVal === 'income' \|\| typeVal === 'transfer_in' \|\| typeVal === 'cash_in' \|\| statusVal === 'aktif') |
| 5371 | const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16); |
| 5372 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5375 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5376 | const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5); |
| 5379 | const cashIn = sumCashLedgerInWithFallback_(cashSheet, cashInCol, cashInfo); |
| 5389 | if (isCashLedgerAccountName_(account)) { |
| 5410 | account_ledger_cash_in: accountIn, |
| 5411 | account_ledger_cash_out: accountOut, |
| 5438 | 'Cash Ledger in: Rp' + cashIn + '\n' + |
| 5439 | 'Cash Ledger out: Rp' + cashOut + '\n' + |
| 5440 | 'Cash Ledger net: Rp' + cashNet + '\n\n' + |
| 5441 | 'Account Ledger Cash in: Rp' + accountIn + '\n' + |
| 5442 | 'Account Ledger Cash out: Rp' + accountOut + '\n' + |
| 5443 | 'Account Ledger Cash net: Rp' + accountNet + '\n\n' + |
| 5446 | 'Buka Account Ledger: ' + link |
| 5458 | if (/^admin\s+(audit\|check\|cek)\s+dashboard\s+(layout\|sheet\|read\s*only\|readonly)/i.test(text)) { |
| 5460 | const result = dashboardLayoutReadOnlyAudit_(ss); |
| 5463 | 'Dashboard layout audit selesai.\n\n' + |
| 5471 | command: 'dashboard_layout_read_only_audit', |
| 5476 | if (/^admin\s+(audit\|check\|cek)\s+(cash\s+)?(reporting\|report\|formula\|formulas\|dashboard)/i.test(text)) { |
| 5478 | const dashboard = |
| 5479 | getSheetLoose_(ss, '?? Dashboard') \|\| |
| 5480 | getSheetLoose_(ss, 'Dashboard'); |
| 5481 | const monthly = |
| 5482 | getSheetLoose_(ss, '?? Monthly Review') \|\| |
| 5483 | getSheetLoose_(ss, 'Monthly Review'); |
| 5485 | const monthlyB6 = monthly ? monthly.getRange('B6').getFormula() : ''; |
| 5486 | const monthlyE6 = monthly ? monthly.getRange('E6').getFormula() : ''; |
| 5487 | const monthlyB8 = monthly ? monthly.getRange('B8').getFormula() : ''; |
| 5488 | const dashboardD17 = dashboard ? dashboard.getRange('D17').getFormula() : ''; |
| 5494 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5495 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5496 | monthly_b8_present: Boolean(monthlyB8), |
| 5497 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5500 | const link = dashboard ? getSheetTabUrl_(ss, dashboard) : ss.getUrl(); |
| 5505 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5506 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5507 | 'Monthly B8 formula ada: ' + result.monthly_b8_present + '\n' + |
| 5508 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5509 | 'B6: ' + formulaSnippet_(monthlyB6) + '\n' + |
| 5510 | 'E6: ' + formulaSnippet_(monthlyE6) + '\n' + |
| 5511 | 'D17: ' + formulaSnippet_(dashboardD17) + '\n\n' + |
| 5512 | '?? Buka Dashboard: ' + link |
| 5521 | monthly_b6: monthlyB6, |
| 5522 | monthly_e6: monthlyE6, |
| 5523 | monthly_b8: monthlyB8, |
| 5524 | dashboard_d17: dashboardD17 |
| 5526 | dashboard_url: link |
| 5530 | if (/^admin\s+(refresh\|sync\|update\|reload)\s+(cash\s+)?(reporting\|report\|formula\|formulas\|dashboard)/i.test(text)) { |
| 5532 | const netWorth = setupDashboardNetWorthPanel(); |
| 5535 | const dashboard = |
| 5536 | getSheetLoose_(ss, '?? Dashboard') \|\| |
| 5537 | getSheetLoose_(ss, 'Dashboard'); |
| 5538 | const link = dashboard ? getSheetTabUrl_(ss, dashboard) : ss.getUrl(); |
| 5543 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 5544 | '?? Buka Dashboard: ' + link |

## 10. Next Micro-Step

Recommended next command:

- add Cash Ledger removal-safety contract regression
- run Sprint 1 Account Ledger baselines
- run Sprint 2 domain baselines
- run Apps Script syntax check
- commit the smallest test-only patch
