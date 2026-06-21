# AIRO Finance - Sprint 3 Remaining Cash Ledger Dependency Audit

Status: EXACT AUDIT
Sprint: Sprint 3 - Cash Ledger Removal
Generated at: 2026-05-24 14:50:59
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document audits remaining Cash Ledger read, backfill, repair, and compatibility surfaces after new Cash Ledger writes were disabled behind a compatibility flag.

No runtime patch is made in this micro-step.

Sprint 3 cannot delete the Cash Ledger tab or remove raw compatibility code until all remaining runtime dependencies are classified and guarded.

## 2. Current Confirmed Position

- New Cash Ledger writes are disabled by default through `writeCashLedgerCompatibility_`.
- `writeCashLedger_` remains available as a compatibility target.
- Dashboard and Monthly Review Cash reads are already locked to Account Ledger formulas.
- Cash Ledger historical tab/rows must not be deleted yet.
- Next safe work is test-first dependency classification.

## 3. Remaining Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `isCashLedgerCompatibilityWriteEnabled_` | 1474-1480 | FOUND | AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED:1 |
| `writeCashLedgerCompatibility_` | 1482-1491 | FOUND | writeCashLedger_:1, writeCashLedgerCompatibility_:1, cash_ledger_compat_writes_disabled:1 |
| `writeCashLedger_` | 1493-1528 | FOUND | AIRO_CONFIG.tabs.cash:1, writeCashLedger_:1, amount_in:1, amount_out:1, linked_txn_id:1, appendByHeader_:1 |
| `writeRouted_` | 1712-1754 | FOUND | AIRO_CONFIG.tabs.cash:1, writeCashLedgerCompatibility_:1, appendByHeader_:1 |
| `writeInternalTransferToAccountLedger_` | 7467-7530 | FOUND | Cash Ledger:1, writeCashLedgerCompatibility_:2, linked_txn_id:3 |
| `refreshCashLedgerMaintenance` | 2863-2933 | FOUND | AIRO_CONFIG.tabs.cash:1, refreshCashLedgerMaintenance:1, amount_in:2, amount_out:2, clearContent:2, setValue:10 |
| `refreshCashMonthlyReviewFormulas` | 2963-2965 | FOUND |  |
| `refreshCashReportingFormulas` | 2971-3026 | FOUND | Account Ledger:17 |
| `setupDashboardNetWorthPanel` | 4276-4378 | FOUND | Account Ledger:12, setValue:12 |
| `handleSpecialFinanceCommand_` | 4503-5654 | FOUND | AIRO_CONFIG.tabs.cash:4, Cash Ledger:4, Account Ledger:13, amount_in:6, amount_out:4, source_tab:1, setValue:3 |
| `migrateCashLedgerToAccountLedger` | MISSING | MISSING |  |
| `auditAccountLedgerMigration` | MISSING | MISSING |  |
| `cleanupAccountLedgerMigrationIssues` | MISSING | MISSING |  |
| `routePlannedTab_` | 2273-2299 | FOUND | AIRO_CONFIG.tabs.cash:1 |
| `routeReviewApprovedTab_` | 2780-2804 | FOUND | AIRO_CONFIG.tabs.cash:1 |

## 4. Runtime Notes

- New Cash Ledger writes are disabled by default behind `writeCashLedgerCompatibility_`.
- Raw `writeCashLedger_` still exists as compatibility target only; do not delete until remaining dependencies are closed.
- `refreshCashLedgerMaintenance` remains a legacy repair/maintenance surface that reads and mutates Cash Ledger rows.
- Routing still sends cash/tunai planned tab to Cash Ledger; writeRouted currently intercepts this with compatibility flag.
- Review Queue approved cash rows still route to Cash Ledger planned tab; writeRouted compatibility behavior must be locked.
- No `deleteSheet` call found in active source.
- No bulk `deleteRows` call found in active source.
- Some single-row cleanup utilities exist, but current audit must distinguish Cash Ledger deletion from unrelated domain cleanup.
- Clear operations exist in maintenance/layout utilities; next test must scope destructive checks to Cash Ledger tab deletion/removal only.

## 5. Existing Relevant Test Files

- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cash_ledger_removal_safety_contract.py
- tests/personal-workflow/test_airo_cash_ledger_write_disable_flag_contract.py
- tests/personal-workflow/test_airo_dashboard_monthly_cash_read_contract.py

## 6. Dependency Classification Matrix

| Surface | Type | Current Risk | Required Next Guard |
|---|---|---:|---|
| `writeCashLedgerCompatibility_` | compatibility write gate | Low | Keep default OFF and preserve opt-in property |
| `writeCashLedger_` | legacy raw writer | Medium | Keep only as compatibility target until closeout |
| `writeRouted_` cash path | route interception | Medium | Assert Account Ledger mirror remains primary and Cash Ledger write is skipped by default |
| `writeInternalTransferToAccountLedger_` cash sync | compatibility sync | Medium | Assert internal transfer Account Ledger rows remain complete when Cash Ledger sync is skipped |
| `refreshCashLedgerMaintenance` | legacy repair/maintenance | High | Guard as legacy-only; do not call in normal Telegram write path |
| Cash Ledger to Account Ledger migration/backfill | historical migration/repair | High | Audit exact callable names and ensure no automatic destructive operation |
| Dashboard / Monthly Review formulas | read formulas | Low | Already locked to Account Ledger, keep regression |
| Review Queue approved cash route | manual replay route | Medium | Assert compatibility flag behavior also applies to approved Review Queue cash rows |

## 7. Recommended Next Patch

Add the smallest test-only dependency contract.

The regression should lock:

- `refreshCashLedgerMaintenance` is not called from normal Telegram write path
- Cash Ledger compatibility flag remains default OFF
- raw `writeCashLedger_` exists only behind `writeCashLedgerCompatibility_`
- migration/backfill functions are manual/admin-only and not called automatically from `doPost`
- no Cash Ledger sheet deletion is introduced
- dashboard/monthly formulas continue to read Account Ledger

## 8. Direct Source Findings

| Line | Source Text |
|---:|---|
| 15 | cash: '💵 Cash Ledger', |
| 20 | accountLedger: '📒 Account Ledger', |
| 1449 | function findCashLedgerExactHeaderCol_(sheet, headerName) { |
| 1463 | function syncCashLedgerRuntimeAmountColumns_(ss, rowNumber, inflow, amount) { |
| 1465 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 1467 | const inCol = findCashLedgerExactHeaderCol_(sheet, 'amount_in'); |
| 1468 | const outCol = findCashLedgerExactHeaderCol_(sheet, 'amount_out'); |
| 1469 | if (inCol) sheet.getRange(rowNumber, inCol).setValue(inflow ? amount : ''); |
| 1470 | if (outCol) sheet.getRange(rowNumber, outCol).setValue(inflow ? '' : amount); |
| 1474 | function isCashLedgerCompatibilityWriteEnabled_() { |
| 1475 | const value = getProp_('AIRO_CASH_LEDGER_COMPAT_WRITES_ENABLED'); |
| 1482 | function writeCashLedgerCompatibility_(ss, parsed, rawText, common) { |
| 1483 | if (!isCashLedgerCompatibilityWriteEnabled_()) { |
| 1487 | reason: 'cash_ledger_compat_writes_disabled' |
| 1490 | return writeCashLedger_(ss, parsed, rawText, common); |
| 1493 | function writeCashLedger_(ss, parsed, rawText, common) { |
| 1523 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.cash, row, { createIfMissing: false }); |
| 1525 | syncCashLedgerRuntimeAmountColumns_(ss, result.row, cashInflow, parsed.amount); |
| 1532 | * Mirrors cash movement to the Account Ledger tab. |
| 1574 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1592 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1609 | .setValues([ACCOUNT_LEDGER_HEADERS]); |
| 1622 | .setValues([ACCOUNT_LEDGER_HEADERS]); |
| 1702 | function isCashLedgerAccountName_(value) { |
| 1733 | if (key.includes('cash ledger')) { |
| 1734 | const cashResult = writeCashLedgerCompatibility_(ss, parsed, rawText, common); |
| 1736 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1753 | return appendByHeader_(ss, tabName, common, { createIfMissing: false }); |
| 1763 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1800 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1806 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1844 | sheet.getRange(targetRow, spec.startCol, 1, values.length).setValues([values]); |
| 1927 | // Cash Ledger movement type validation. |
| 2019 | function appendByHeader_(ss, tabName, data, options) { |
| 2028 | created.getRange(1, 1, 1, headers.length).setValues([headers]); |
| 2030 | created.getRange(2, 1, 1, headers.length).setValues([createdValues]); |
| 2053 | sheet.getRange(targetRow, 1, 1, values.length).setValues([values]); |
| 2277 | if (/\b(cash\|tunai)\b/i.test(text)) return AIRO_CONFIG.tabs.cash; |
| 2800 | return AIRO_CONFIG.tabs.cash; |
| 2832 | sheet.getRange(rowNumber, map[c] + 1).setValue(value); |
| 2863 | function refreshCashLedgerMaintenance() { |
| 2865 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 2868 | return { ok: false, reason: 'cash_ledger_missing' }; |
| 2901 | sheet.getRange(r, 1).setValue(sessionId);       // session_id |
| 2902 | sheet.getRange(r, 3).setValue(amount);          // amount_start |
| 2903 | sheet.getRange(r, 5).setValue(amount);          // amount_remaining |
| 2904 | sheet.getRange(r, 7).setValue('aktif');         // status |
| 2905 | sheet.getRange(r, 8).setValue(text);            // notes |
| 2909 | sheet.getRange(r, 11).setValue(sessionId);        // session_id |
| 2910 | sheet.getRange(r, 13).setValue(inflow ? 'transfer_in' : 'expense'); // type |
| 2913 | sheet.getRange(r, 14).setValue('Transport');    // category |
| 2917 | sheet.getRange(r, 16).clearContent();           // amount_out |
| 2918 | sheet.getRange(r, 17).setValue(amount);         // amount_in |
| 2920 | sheet.getRange(r, 16).setValue(amount);         // amount_out |
| 2921 | sheet.getRange(r, 17).clearContent();           // amount_in |
| 2983 | `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`; |
| 2986 | `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`; |
| 2989 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2992 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2998 | `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`; |
| 3224 | sheet.getRange('F12').setValue(price); |
| 3415 | sheet.getRange(targetRow, 1, 1, width).setValues([row.slice(0, width)]); |
| 3629 | sheet.deleteRow(r); |
| 3719 | sheet.deleteRow(r); |
| 3800 | range.clearContent(); |
| 3851 | asset.getRange('AA16').setValue('NET_WORTH_HELPER_DO_NOT_EDIT_RANDOMLY'); |
| 3852 | asset.getRange('AA17').setValue('Nilai Rumah Pasar'); |
| 3853 | asset.getRange('AB17').setValue(homeValue); |
| 3855 | asset.getRange('AA18').setValue('Haircut Konservatif'); |
| 3856 | asset.getRange('AB18').setValue(haircut); |
| 3858 | asset.getRange('AA19').setValue('Nilai Rumah Konservatif'); |
| 3861 | asset.getRange('AA20').setValue('Sisa Pokok Rumah'); |
| 3862 | asset.getRange('AB20').setValue(principal); |
| 3864 | asset.getRange('AA21').setValue('Ekuitas Rumah'); |
| 3995 | cc.getRange('A1').setValue( |
| 4002 | cc.getRange('A2').setValue('Total Tagihan'); |
| 4003 | cc.getRange('B2').setValue(stats.payable_total); |
| 4004 | cc.getRange('C2').setValue('Sudah Blu'); |
| 4005 | cc.getRange('D2').setValue(stats.payable_sudah_blu); |
| 4006 | cc.getRange('E2').setValue('Belum Blu'); |
| 4007 | cc.getRange('F2').setValue(stats.payable_belum_blu); |
| 4008 | cc.getRange('G2').setValue('Status'); |
| 4009 | cc.getRange('H2').setValue(payableStatus); |
| 4012 | cc.getRange('A3').setValue('Tagihan jatuh tempo tetap tampil sampai dana pembayaran disiapkan di Pocket Blu khusus CC / paid / closed.'); |
| 4016 | cc.getRange('A4').setValue( |
| 4023 | cc.getRange('A5').setValue('Total Sementara'); |
| 4024 | cc.getRange('B5').setValue(stats.unbilled_total); |
| 4025 | cc.getRange('C5').setValue('Transaksi'); |
| 4026 | cc.getRange('D5').setValue(stats.unbilled_rows); |
| 4027 | cc.getRange('E5').setValue('Belum Blu'); |
| 4028 | cc.getRange('F5').setValue(stats.unbilled_belum_blu); |
| 4029 | cc.getRange('G5').setValue('Status'); |
| 4030 | cc.getRange('H5').setValue('Tracking'); |
| 4033 | cc.getRange('A6').setValue('Periode berjalan tidak dicampur ke tagihan jatuh tempo sebelumnya.'); |
| 4205 | dashboard.getRange('B25').setValue('💳 CREDIT CARD — TOKOPEDIA CC'); |
| 4207 | dashboard.getRange('B26:C26').merge().setValue('Tagihan Jatuh Tempo'); |
| 4208 | dashboard.getRange('D26').setValue(payableCycle.id); |
| 4209 | dashboard.getRange('E26:F26').merge().setValue(formatDateYmd_(payableCycle.start) + ' – ' + formatDateYmd_(payableCycle.end)); |
| 4210 | dashboard.getRange('G26').setValue('Due ' + formatDateYmd_(payableDueDate)); |
| 4212 | dashboard.getRange('B27:C27').merge().setValue('Total Tagihan'); |
| 4213 | dashboard.getRange('D27').setValue(stats.payable_total); |
| 4214 | dashboard.getRange('E27:F27').merge().setValue('Belum ke Blu'); |
| 4215 | dashboard.getRange('G27').setValue(stats.payable_belum_blu); |
| 4217 | dashboard.getRange('B28:C28').merge().setValue('Status'); |
| 4218 | dashboard.getRange('D28').setValue(overdue ? 'OVERDUE / CEK BLU' : (stats.payable_belum_blu > 0 ? 'PERLU SIAPKAN BLU' : 'AMAN')); |
| 4219 | dashboard.getRange('E28:F28').merge().setValue('Rows'); |
| 4220 | dashboard.getRange('G28').setValue(stats.payable_rows); |
| 4222 | dashboard.getRange('B30:C30').merge().setValue('Periode Berjalan / Unbilled'); |
| 4223 | dashboard.getRange('D30').setValue(currentCycle.id); |
| 4224 | dashboard.getRange('E30:F30').merge().setValue(formatDateYmd_(currentCycle.start) + ' – ' + formatDateYmd_(currentCycle.end)); |
| 4225 | dashboard.getRange('G30').setValue('Belum closing'); |
| 4227 | dashboard.getRange('B31:C31').merge().setValue('Total Sementara'); |
| 4228 | dashboard.getRange('D31').setValue(stats.unbilled_total); |
| 4229 | dashboard.getRange('E31:F31').merge().setValue('Belum ke Blu'); |
| 4230 | dashboard.getRange('G31').setValue(stats.unbilled_belum_blu); |
| 4233 | dashboard.getRange('B33').setValue('Catatan: “Belum ke Blu” = dana bayar CC belum disiapkan di Pocket Blu khusus pembayaran CC.'); |
| 4293 | dashboard.getRange('B16').setValue('💰 NET WORTH & HOME EQUITY'); |
| 4296 | dashboard.getRange('B17:C17').merge().setValue('Total Aset Likuid'); |
| 4297 | dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`); |
| 4299 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4302 | dashboard.getRange('B19:C19').merge().setValue('Net Worth Likuid'); |
| 4305 | dashboard.getRange('B20:C20').merge().setValue('Ekuitas Rumah'); |
| 4308 | dashboard.getRange('B21:C21').merge().setValue('Net Worth Total'); |
| 4312 | dashboard.getRange('E17:F17').merge().setValue('Nilai Rumah Pasar'); |
| 4315 | dashboard.getRange('E18:F18').merge().setValue('Haircut Konservatif'); |
| 4318 | dashboard.getRange('E19:F19').merge().setValue('Nilai Rumah Konservatif'); |
| 4321 | dashboard.getRange('E20:F20').merge().setValue('Sisa Pokok Rumah'); |
| 4324 | dashboard.getRange('E21:F21').merge().setValue('Ekuitas Rumah'); |
| 4328 | dashboard.getRange('B23').setValue('Catatan: Net Worth Likuid tidak memasukkan rumah. Net Worth Total memasukkan ekuitas rumah konservatif.'); |
| 4733 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5065 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5146 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5235 | if (isCashLedgerAccountName_(account) && amount > 0) { |
| 5281 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5283 | 'Cash Ledger inflows recent/top:\n' + |
| 5288 | 'Buka Account Ledger: ' + link |
| 5294 | command: 'cash_ledger_account_parity_detail_audit', |
| 5310 | const cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 5362 | const sumCashLedgerInWithFallback_ = function(sheet, cashInCol, info) { |
| 5398 | const cashIn = sumCashLedgerInWithFallback_(cashSheet, cashInCol, cashInfo); |
| 5408 | if (isCashLedgerAccountName_(account)) { |
| 5426 | cash_ledger_in: cashIn, |
| 5427 | cash_ledger_out: cashOut, |
| 5428 | cash_ledger_net: cashNet, |
| 5457 | 'Cash Ledger in: Rp' + cashIn + '\n' + |
| 5458 | 'Cash Ledger out: Rp' + cashOut + '\n' + |
| 5459 | 'Cash Ledger net: Rp' + cashNet + '\n\n' + |
| 5460 | 'Account Ledger Cash in: Rp' + accountIn + '\n' + |
| 5461 | 'Account Ledger Cash out: Rp' + accountOut + '\n' + |
| 5462 | 'Account Ledger Cash net: Rp' + accountNet + '\n\n' + |
| 5465 | 'Buka Account Ledger: ' + link |
| 5471 | command: 'cash_ledger_account_parity_audit', |
| 5513 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5514 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5516 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5524 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5525 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5527 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5562 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 5606 | asset.getRange('AB17').setValue(value); |
| 5614 | asset.getRange('AB20').setValue(value); |
| 5622 | asset.getRange('AB18').setValue(value); |
| 5775 | sheet.getRange(1, 1, 1, 6).setValues([[ |
| 5904 | allowedRange.getCell(r + 1, c + 1).setValue(current); |
| 5939 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5950 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5970 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5981 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5997 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6172 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6205 | sheet.getRange(targetRow, 1, 1, row.length).setValues([row]); |
| 6222 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6240 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6277 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6296 | sheet.getRange(bestRow, statusCol).setValue('✅ Sudah'); |
| 6299 | sheet.getRange(bestRow, transferredCol).setValue(todayDate_()); |
| 6309 | sheet.getRange(bestRow, notesCol).setValue(newNotes); |
| 6430 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6441 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6451 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6466 | if (map.total_dibayar) sheet.getRange(master.row, map.total_dibayar).setValue(newPaid); |
| 6467 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6468 | if (map.status) sheet.getRange(master.row, map.status).setValue(sisa <= 0 ? 'lunas' : 'aktif'); |
| 6507 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6518 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6528 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6541 | if (map.jumlah_pokok) sheet.getRange(master.row, map.jumlah_pokok).setValue(newPokok); |
| 6542 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6543 | if (map.status) sheet.getRange(master.row, map.status).setValue(sisa <= 0 ? 'lunas' : 'aktif'); |
| 6574 | sheet.getRange(targetRow, 1, 1, row.length).setValues([row]); |
| 6647 | range.setValues(fixed); |
| 6723 | descRange.setValues(statusValues); |
| 6727 | statusRange.setValues(descValues); |
| 6731 | sheet.getRange(startRow, targetStatusCol).setValue('status_pocket_blu'); |
| 6732 | sheet.getRange(startRow, statusCol).setValue('description'); |
| 6860 | sheet.getRange(r, dateCol).setValue(parsedDate); |
| 6861 | sheet.getRange(r, merchantCol).setValue(merchant); |
| 6863 | if (cycleCol) sheet.getRange(r, cycleCol).setValue(cycle.id); |
| 6864 | if (startCol) sheet.getRange(r, startCol).setValue(cycle.start); |
| 6865 | if (endCol) sheet.getRange(r, endCol).setValue(cycle.end); |
| 6866 | if (statementCol) sheet.getRange(r, statementCol).setValue(cycle.statementMonth); |
| 6879 | * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger. |
| 6883 | function AIRO_BACKFILL_ACCOUNT_LEDGER_FROM_CASH_LEDGER() { |
| 6887 | var cashSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cash); |
| 6889 | throw new Error('Cash Ledger sheet not found'); |
| 6894 | throw new Error('Failed to ensure Account Ledger sheet exists'); |
| 6899 | throw new Error('Header not found in Cash Ledger'); |
| 6904 | throw new Error('Header not found in Account Ledger'); |
| 6910 | // Validate required fields in Cash Ledger |
| 6929 | throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)'); |
| 6932 | // Validate required fields in Account Ledger |
| 6950 | throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)'); |
| 6953 | // Read Cash Ledger rows |
| 6997 | // Read Account Ledger rows for dedup |
| 7054 | // Construct new row object for Account Ledger |
| 7097 | source_tab: AIRO_CONFIG.tabs.cash, |
| 7102 | var result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 7188 | * Audit function for Account Ledger to identify missing source_tab, cash backfill rows, and duplicate candidates. |
| 7197 | throw new Error('Account Ledger sheet not found'); |
| 7202 | throw new Error('Header not found in Account Ledger'); |
| 7308 | * Safe, specific manual cleanup function for duplicate rows and blank source_tab in Account Ledger. |
| 7316 | throw new Error('Account Ledger sheet not found'); |
| 7321 | throw new Error('Header not found in Account Ledger'); |
| 7381 | sheet.deleteRow(15); |
| 7382 | sheet.deleteRow(14); |
| 7383 | sheet.deleteRow(13); |
| 7384 | sheet.deleteRow(12); |
| 7405 | sheet.getRange(r, sourceTabColIdx).setValue(AIRO_CONFIG.tabs.cash); |
| 7464 | * Writes an internal transfer to the Account Ledger as two separate entries (outflow and inflow) |
| 7465 | * and synchronizes with the Cash Ledger compatibility layer if one of the accounts is Cash. |
| 7498 | // Cash Ledger compatibility layer synchronization |
| 7507 | cashResult = writeCashLedgerCompatibility_(ss, parsedCashIn, rawText, common); |
| 7515 | cashResult = writeCashLedgerCompatibility_(ss, parsedCashOut, rawText, common); |
| 7528 | cashLedgerRow: (cashResult && cashResult.row) ? cashResult.row : null |

## 9. Next Micro-Step

Recommended next command:

- add test-only remaining Cash Ledger dependency contract
- run Sprint 3 Cash Ledger regressions
- run Sprint 1 Account Ledger baselines
- run Sprint 2 domain baselines
- run Apps Script syntax check
- commit the smallest test-only patch
