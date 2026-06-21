# AIRO Finance - Sprint 3 Dashboard / Monthly Cash Read Audit

Status: EXACT AUDIT
Sprint: Sprint 3 - Cash Ledger Removal
Generated at: 2026-05-24 14:43:35
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document audits dashboard and monthly Cash read dependencies before disabling any Cash Ledger writes.

Sprint 3 cannot remove or disable Cash Ledger write paths until dashboard/monthly read paths are proven to use Account Ledger or are explicitly migrated.

No runtime patch is made in this micro-step.

## 2. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `refreshCashReportingFormulas` | 2952-3007 | FOUND | Account Ledger:17, Monthly Review:2, Dashboard:2, monthlyCashInFormula:2, monthlyCashOutFormula:2, monthlyNetFormula:2, dashboardCashAktifFormula:2, getRange('B6'):1, getRange('E6'):1, getRange('B8'):1, SUMIFS:6, FILTER:2 |
| `refreshCashMonthlyReviewFormulas` | 2944-2946 | FOUND |  |
| `dashboardLayoutReadOnlyAudit_` | 4421-4481 | FOUND | Dashboard:1 |
| `setupDashboardCreditCardCyclePanel` | 4094-4254 | FOUND | Dashboard:3 |
| `setupAsetNetWorthHelpers_` | 3817-3865 | FOUND |  |
| `setupAsetHomeEquityPanel_` | MISSING | MISSING |  |
| `handleAdminFinanceCommand_` | MISSING | MISSING |  |
| `writeCashLedger_` | 1474-1509 | FOUND | AIRO_CONFIG.tabs.cash:1, amount_in:1, amount_out:1, linked_txn_id:1 |
| `writeAccountLedgerMirror_` | 1516-1570 | FOUND | AIRO_CONFIG.tabs.accountLedger:2, SUMIFS:2, amount_in:1, amount_out:1, cash_in:1, cash_out:1, source_tab:1, linked_txn_id:3 |
| `writeRouted_` | 1693-1735 | FOUND | AIRO_CONFIG.tabs.cash:1, AIRO_CONFIG.tabs.accountLedger:1 |

## 3. Existing Test Candidates

- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cash_ledger_removal_safety_contract.py

## 4. Risk Notes

- refreshCashMonthlyReviewFormulas is a wrapper; deletion-safety tests must inspect refreshCashReportingFormulas.
- Monthly B6/E6/B8 and dashboard cash-active formula already have Account Ledger replacement path.
- No deleteSheet pattern found in active source.

## 5. Dashboard / Monthly Read Matrix

| Surface | Expected Cash source after Sprint 3 migration | Current audit status | Disable Cash Ledger writes now? |
|---|---|---:|---:|
| Monthly Review B6 cash masuk | Account Ledger `amount_in` for Cash accounts | Needs contract test | No |
| Monthly Review E6 cash keluar | Account Ledger `amount_out` for Cash accounts | Needs contract test | No |
| Monthly Review B8 net | B6 - E6 or equivalent Account Ledger formula | Needs contract test | No |
| Dashboard Cash Aktif | Account Ledger cash account inflow/outflow net | Needs contract test | No |
| Net Worth liquid cash | Account Ledger cash account net | Needs contract test | No |
| Admin reporting audit | Formula read-only audit | Present, needs contract test | No |

## 6. Recommended Next Patch

Add the smallest test-only dashboard/monthly Cash read contract.

The regression should lock:

- `refreshCashMonthlyReviewFormulas` delegates to `refreshCashReportingFormulas`
- `refreshCashReportingFormulas` writes Monthly Review B6/E6/B8 formulas
- B6/E6 formulas read Account Ledger, not Cash Ledger
- Dashboard Cash Aktif formula reads Account Ledger, not Cash Ledger
- admin read-only audit checks monthly B6/E6 and dashboard D17 Account Ledger usage
- no Cash Ledger write disabling occurs in this test-only step

## 7. Direct Source Findings

| Line | Source Text |
|---:|---|
| 15 | cash: '💵 Cash Ledger', |
| 20 | accountLedger: '📒 Account Ledger', |
| 1513 | * Mirrors cash movement to the Account Ledger tab. |
| 1514 | * Balance is intentionally left blank for Google Sheet formulas. |
| 1562 | const formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))'; |
| 1563 | sheet.getRange(r, 6).setFormula(formula); |
| 1573 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1634 | if (!sheet.getFilter()) { |
| 1637 | dataRange.createFilter(); |
| 1714 | if (key.includes('cash ledger')) { |
| 1886 | .filter(Boolean); |
| 1908 | // Cash Ledger movement type validation. |
| 2183 | const fields = row.map(h => fieldForHeader_(h)).filter(Boolean); |
| 2187 | .filter(f => unique.includes(f)).length; |
| 2908 | refreshCashMonthlyReviewFormulas(); |
| 2916 | function setFormulaNextToLabel_(sheet, labels, formula) { |
| 2935 | sheet.getRange(r + 1, targetCol).setFormula(formula); |
| 2944 | function refreshCashMonthlyReviewFormulas() { |
| 2945 | return refreshCashReportingFormulas(); |
| 2952 | function refreshCashReportingFormulas() { |
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
| 3010 | return refreshCashReportingFormulas(); |
| 3013 | function setFormulaOnCellContaining_(sheet, labels, formula) { |
| 3028 | sheet.getRange(r + 1, c + 1).setFormula(formula); |
| 3363 | ].filter(Boolean).join(' \| '); |
| 3795 | const dashboard = |
| 3796 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 3797 | getSheetLoose_(ss, 'Dashboard'); |
| 3803 | if (!dashboard) { |
| 3804 | return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 3808 | const panel = setupDashboardNetWorthPanel(); |
| 3820 | // Helper cells only. They may be hidden; dashboard is the visible panel. |
| 3840 | asset.getRange('AB19').setFormula('=IFERROR(AB17*(1-AB18);0)'); |
| 3846 | asset.getRange('AB21').setFormula('=IFERROR(AB19-AB20;0)'); |
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
| 4816 | if (/^admin\s+(refresh\|sync\|update\|reload)\s+cc\s+(dashboard\|cycle\s+dashboard\|billing\s+dashboard\|tagihan\s+dashboard)/i.test(text)) { |
| 4817 | const result = setupDashboardCreditCardCyclePanel(); |
| 4822 | 'Credit Card Dashboard cycle panel direfresh.\n\n' + |
| 4828 | 'Panel: ' + ((result && result.dashboard_panel) \|\| '-') + '\n\n' + |
| 4829 | (link ? '🔗 Buka Dashboard: ' + link : '') |
| 4835 | command: 'cc_dashboard_cycle_refresh', |
| 5262 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5264 | 'Cash Ledger inflows recent/top:\n' + |
| 5269 | 'Buka Account Ledger: ' + link |
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
| 5489 | const formulaSnippet_ = function(value) { |
| 5494 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5495 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5496 | monthly_b8_present: Boolean(monthlyB8), |
| 5497 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5500 | const link = dashboard ? getSheetTabUrl_(ss, dashboard) : ss.getUrl(); |
| 5504 | '? Audit formula cash reporting selesai.\n\n' + |
| 5505 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5506 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5507 | 'Monthly B8 formula ada: ' + result.monthly_b8_present + '\n' + |
| 5508 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5509 | 'B6: ' + formulaSnippet_(monthlyB6) + '\n' + |
| 5510 | 'E6: ' + formulaSnippet_(monthlyE6) + '\n' + |
| 5511 | 'D17: ' + formulaSnippet_(dashboardD17) + '\n\n' + |
| 5512 | '?? Buka Dashboard: ' + link |
| 5518 | command: 'cash_reporting_formula_audit', |
| 5520 | formulas: { |
| 5521 | monthly_b6: monthlyB6, |
| 5522 | monthly_e6: monthlyE6, |
| 5523 | monthly_b8: monthlyB8, |
| 5524 | dashboard_d17: dashboardD17 |
| 5526 | dashboard_url: link |
| 5530 | if (/^admin\s+(refresh\|sync\|update\|reload)\s+(cash\s+)?(reporting\|report\|formula\|formulas\|dashboard)/i.test(text)) { |
| 5531 | const reporting = refreshCashReportingFormulas(); |
| 5532 | const netWorth = setupDashboardNetWorthPanel(); |
| 5535 | const dashboard = |
| 5536 | getSheetLoose_(ss, '?? Dashboard') \|\| |
| 5537 | getSheetLoose_(ss, 'Dashboard'); |
| 5538 | const link = dashboard ? getSheetTabUrl_(ss, dashboard) : ss.getUrl(); |
| 5542 | '? Reporting formula direfresh.\n\n' + |
| 5543 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 5544 | '?? Buka Dashboard: ' + link |
| 5549 | ok: Boolean(reporting && reporting.ok), |
| 5550 | command: 'cash_reporting_refresh', |
| 5551 | reporting, |
| 5553 | dashboard_url: link |
| 5567 | const dashboard = |
| 5568 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 5569 | getSheetLoose_(ss, 'Dashboard'); |
| 5571 | if (!asset \|\| !dashboard) { |
| 5615 | const link = getSheetTabUrl_(ss, dashboard); |
| 5624 | '🔗 Buka Dashboard: ' + link |
| 5633 | dashboard_url: link |
| 5640 | * It is kept for formula compatibility, but final Net Worth source of truth is Dashboard. |
| 5654 | // Keep values/formulas but hide visually. |
| 5660 | note: 'Legacy Aset Net Worth hidden. Use Dashboard Net Worth panel as source of truth.' |
| 5846 | .filter(Boolean); |
| 5872 | .filter(Boolean); |
| 6092 | const words = t.split(/\s+/).filter(Boolean).slice(0, 3); |
| 6248 | const words = keyword.split(/\s+/).filter(w => w.length >= 3); |
| 6288 | ].filter(Boolean).join(' \| '); |
| 6731 | .filter(Boolean) |
| 6860 | * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger. |
| 6862 | * and key properties, and populates balance formulas dynamically without overwriting existing data. |
| 6870 | throw new Error('Cash Ledger sheet not found'); |
| 6875 | throw new Error('Failed to ensure Account Ledger sheet exists'); |
| 6880 | throw new Error('Header not found in Cash Ledger'); |
| 6885 | throw new Error('Header not found in Account Ledger'); |
| 6891 | // Validate required fields in Cash Ledger |
| 6910 | throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)'); |
| 6913 | // Validate required fields in Account Ledger |
| 6931 | throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)'); |
| 6934 | // Read Cash Ledger rows |
| 6953 | // Filter empty rows |
| 6978 | // Read Account Ledger rows for dedup |
| 7035 | // Construct new row object for Account Ledger |
| 7086 | // Set formula balance |
| 7089 | var formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))'; |
| 7090 | accountSheet.getRange(r, 6).setFormula(formula); |
| 7169 | * Audit function for Account Ledger to identify missing source_tab, cash backfill rows, and duplicate candidates. |
| 7178 | throw new Error('Account Ledger sheet not found'); |
| 7183 | throw new Error('Header not found in Account Ledger'); |
| 7289 | * Safe, specific manual cleanup function for duplicate rows and blank source_tab in Account Ledger. |
| 7297 | throw new Error('Account Ledger sheet not found'); |
| 7302 | throw new Error('Header not found in Account Ledger'); |
| 7445 | * Writes an internal transfer to the Account Ledger as two separate entries (outflow and inflow) |
| 7446 | * and synchronizes with the Cash Ledger compatibility layer if one of the accounts is Cash. |
| 7479 | // Cash Ledger compatibility layer synchronization |

## 8. Next Micro-Step

Recommended next command:

- add dashboard/monthly Cash read contract regression
- run Cash Ledger removal-safety regression
- run Sprint 1 Account Ledger baselines
- run Sprint 2 domain baselines
- run Apps Script syntax check
- commit the smallest test-only patch
