# AIRO Finance - Sprint 5 Dashboard Formula Inventory

Date: 2026-05-26
Sprint: Sprint 5 - Dashboard Analytics
Status: ACTIVE - READ ONLY INVENTORY

## 1. Summary

This inventory was generated from Apps Script source only.

No runtime patch, Apps Script deploy, Cloudflare Worker change, Telegram smoke, or live Google Sheet formula edit was performed.

## 2. Inventory Counts

- Dashboard/formula-related function candidates: 46
- Formula indicator lines: 42
- Formula lines referencing Account Ledger: 4
- Formula lines referencing Cash Ledger: 0
- Formula lines referencing Finance Events: 0
- Formula lines referencing Transactions: 0

## 3. Risk Model

- safe_account_ledger_based
- safe_finance_events_lineage
- domain_supporting_metric
- legacy_cash_ledger_primary_risk
- transactions_primary_risk
- unreconciled_formula_risk
- destructive_sheet_write_risk
- unknown_needs_manual_review

## 4. Function Inventory

### normalizeCashClarificationAnswer_

- Source line: 129
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### canAskCashAmbiguousClarification_

- Source line: 141
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### buildCashAmbiguousClarificationMessage_

- Source line: 156
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### cashClarificationResolvedText_

- Source line: 169
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### findCashLedgerExactHeaderCol_

- Source line: 1457
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### syncCashLedgerRuntimeAmountColumns_

- Source line: 1471
- Risk classification: legacy_cash_ledger_primary_risk
- Detected references: legacy_cash_ledger
- Evidence snippets: none

### isCashLedgerCompatibilityWriteEnabled_

- Source line: 1482
- Risk classification: legacy_cash_ledger_primary_risk
- Detected references: legacy_cash_ledger
- Evidence snippets:
  - L1484: // This flag is optional. Missing flag means legacy Cash Ledger writes stay disabled.

### writeCashLedgerCompatibility_

- Source line: 1606
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### writeCashLedger_

- Source line: 1617
- Risk classification: safe_account_ledger_based
- Detected references: account_ledger, legacy_cash_ledger
- Evidence snippets:
  - L1656: * Mirrors cash movement to the Account Ledger tab.

### writeAccountLedgerMirror_

- Source line: 1659
- Risk classification: safe_account_ledger_based
- Detected references: account_ledger, formula_write
- Evidence snippets:
  - L1705: const formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))';
  - L1706: sheet.getRange(r, 6).setFormula(formula);
  - L1716: * Ensures the 📒 Account Ledger tab exists with the correct headers.

### cashSessionId_

- Source line: 1818
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### cashAccountNameForLedger_

- Source line: 1822
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### isCashLedgerAccountName_

- Source line: 1826
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### isCashBensinText_

- Source line: 1831
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### reviewIssueReasonForParsed_

- Source line: 2537
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### isCashInflowText_

- Source line: 2729
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### isCashInflowData_

- Source line: 2749
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### processReviewQueueApproved

- Source line: 2884
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### processReviewQueueApprovedOnEdit

- Source line: 3005
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### setupReviewQueueAutoProcessor

- Source line: 3009
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### routeReviewApprovedTab_

- Source line: 3030
- Risk classification: legacy_cash_ledger_primary_risk, transactions_primary_risk
- Detected references: legacy_cash_ledger, transactions
- Evidence snippets: none

### reviewHeaderMap_

- Source line: 3056
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### getReviewValue_

- Source line: 3067
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### setReviewValue_

- Source line: 3078
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### normalizeReviewAmount_

- Source line: 3090
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### normalizeReviewAccount_

- Source line: 3096
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### refreshCashLedgerMaintenance

- Source line: 3113
- Risk classification: destructive_sheet_write_risk, legacy_cash_ledger_primary_risk
- Detected references: legacy_cash_ledger, monthly_review, destructive_write
- Evidence snippets:
  - L3167: sheet.getRange(r, 16).clearContent();           // amount_out
  - L3171: sheet.getRange(r, 17).clearContent();           // amount_in

### setFormulaNextToLabel_

- Source line: 3185
- Risk classification: unknown_needs_manual_review
- Detected references: formula_write
- Evidence snippets:
  - L3185: function setFormulaNextToLabel_(sheet, labels, formula) {
  - L3204: sheet.getRange(r + 1, targetCol).setFormula(formula);

### refreshCashMonthlyReviewFormulas

- Source line: 3213
- Risk classification: unknown_needs_manual_review
- Detected references: monthly_review
- Evidence snippets: none

### refreshCashReportingFormulas

- Source line: 3221
- Risk classification: safe_account_ledger_based
- Detected references: account_ledger, dashboard, monthly_review, formula_write
- Evidence snippets:
  - L3225: getSheetLoose_(ss, '🏠 Dashboard') ||
  - L3226: getSheetLoose_(ss, 'Dashboard');
  - L3229: getSheetLoose_(ss, '📆 Monthly Review') ||
  - L3230: getSheetLoose_(ss, 'Monthly Review');
  - L3233: `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`;
  - L3236: `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum| Bensin)?$")`;
  - L3239: `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`;
  - L3242: `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`;
  - L3248: `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;
  - L3257: monthly.getRange('B6').setFormula(monthlyCashInFormula);
  - L3258: monthly.getRange('E6').setFormula(monthlyCashOutFormula);
  - L3259: monthly.getRange('B8').setFormula(monthlyNetFormula);

### refreshCashMonthlyReviewFormulas

- Source line: 3278
- Risk classification: unknown_needs_manual_review
- Detected references: monthly_review
- Evidence snippets: none

### setFormulaOnCellContaining_

- Source line: 3282
- Risk classification: unknown_needs_manual_review
- Detected references: formula_write
- Evidence snippets:
  - L3282: function setFormulaOnCellContaining_(sheet, labels, formula) {
  - L3297: sheet.getRange(r + 1, c + 1).setFormula(formula);

### parseHumanMoney_

- Source line: 3990
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### setupNetWorthMetrics

- Source line: 4057
- Risk classification: unknown_needs_manual_review
- Detected references: dashboard
- Evidence snippets:
  - L4065: getSheetLoose_(ss, '🏠 Dashboard') ||
  - L4066: getSheetLoose_(ss, 'Dashboard');
  - L4077: const panel = setupDashboardNetWorthPanel();

### setupAsetNetWorthHelpers_

- Source line: 4086
- Risk classification: destructive_sheet_write_risk
- Detected references: dashboard, destructive_write, formula_write
- Evidence snippets:
  - L4099: asset.getRange('AA16:AE22').clearFormat().clearDataValidations();
  - L4109: asset.getRange('AB19').setFormula('=IFERROR(AB17*(1-AB18);0)');
  - L4115: asset.getRange('AB21').setFormula('=IFERROR(AB19-AB20;0)');

### setupDashboardCreditCardCyclePanel

- Source line: 4363
- Risk classification: destructive_sheet_write_risk
- Detected references: dashboard, destructive_write
- Evidence snippets:
  - L4363: function setupDashboardCreditCardCyclePanel() {
  - L4367: getSheetLoose_(ss, '🏠 Dashboard') ||
  - L4368: getSheetLoose_(ss, 'Dashboard');
  - L4387: safeClearRange_(dashboard, 'B25:G34');

### setupDashboardNetWorthPanel

- Source line: 4526
- Risk classification: destructive_sheet_write_risk, safe_account_ledger_based
- Detected references: account_ledger, dashboard, destructive_write, formula_write
- Evidence snippets:
  - L4526: function setupDashboardNetWorthPanel() {
  - L4530: getSheetLoose_(ss, '🏠 Dashboard') ||
  - L4531: getSheetLoose_(ss, 'Dashboard');
  - L4540: safeClearRange_(dashboard, 'B16:G24');
  - L4547: dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Led
  - L4550: dashboard.getRange('D18').setFormula(`=IFERROR('🥇 Aset'!F18;0)`);
  - L4553: dashboard.getRange('D19').setFormula('=IFERROR(D17-D18;0)');
  - L4556: dashboard.getRange('D20').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`);
  - L4559: dashboard.getRange('D21').setFormula('=IFERROR(D19+D20;0)');
  - L4563: dashboard.getRange('G17').setFormula(`=IFERROR('🥇 Aset'!AB17;0)`);
  - L4566: dashboard.getRange('G18').setFormula(`=IFERROR('🥇 Aset'!AB18;0)`);
  - L4569: dashboard.getRange('G19').setFormula(`=IFERROR('🥇 Aset'!AB19;0)`);

### cleanupDuplicateNetWorthPanels

- Source line: 4630
- Risk classification: destructive_sheet_write_risk
- Detected references: destructive_write
- Evidence snippets:
  - L4671: safeClearRange_(asset, a1);

### polishNetWorthLayout

- Source line: 4685
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### dashboardLayoutReadOnlyAudit_

- Source line: 4690
- Risk classification: unknown_needs_manual_review
- Detected references: dashboard
- Evidence snippets:
  - L4693: getSheetLoose_(ss, 'Dashboard');

### airoFindSmokeRowPreview_

- Source line: 4775
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### airoFindSmokeAcrossWorkbook_

- Source line: 4784
- Risk classification: safe_account_ledger_based, safe_finance_events_lineage
- Detected references: account_ledger, finance_events, legacy_cash_ledger, transactions
- Evidence snippets:
  - L4787: // Use: admin find smoke all <QUERY> to include every tab.
  - L4801: '📒 Account Ledger',
  - L4802: '💵 Cash Ledger',

### handleSpecialFinanceCommand_

- Source line: 4931
- Risk classification: safe_account_ledger_based
- Detected references: account_ledger, legacy_cash_ledger, dashboard, monthly_review
- Evidence snippets:
  - L5333: const result = setupDashboardCreditCardCyclePanel();
  - L5338: 'Credit Card Dashboard cycle panel direfresh.\n\n' +
  - L5345: (link ? '🔗 Buka Dashboard: ' + link : '')
  - L5778: 'Account Ledger Cash inflows recent/top:\n' +
  - L5780: 'Cash Ledger inflows recent/top:\n' +
  - L5785: 'Buka Account Ledger: ' + link
  - L5954: 'Cash Ledger in: Rp' + cashIn + '\n' +
  - L5955: 'Cash Ledger out: Rp' + cashOut + '\n' +
  - L5956: 'Cash Ledger net: Rp' + cashNet + '\n\n' +
  - L5957: 'Account Ledger Cash in: Rp' + accountIn + '\n' +
  - L5958: 'Account Ledger Cash out: Rp' + accountOut + '\n' +
  - L5959: 'Account Ledger Cash net: Rp' + accountNet + '\n\n' +

### hideLegacyAsetNetWorthPanel

- Source line: 6158
- Risk classification: unknown_needs_manual_review
- Detected references: dashboard
- Evidence snippets:
  - L6176: note: 'Legacy Aset Net Worth hidden. Use Dashboard Net Worth panel as source of truth.'

### showLegacyAsetNetWorthPanel

- Source line: 6180
- Risk classification: unknown_needs_manual_review
- Detected references: none
- Evidence snippets: none

### AIRO_BACKFILL_ACCOUNT_LEDGER_FROM_CASH_LEDGER

- Source line: 7557
- Risk classification: safe_account_ledger_based
- Detected references: account_ledger, legacy_cash_ledger, formula_write
- Evidence snippets:
  - L7563: throw new Error('Cash Ledger sheet not found');
  - L7568: throw new Error('Failed to ensure Account Ledger sheet exists');
  - L7573: throw new Error('Header not found in Cash Ledger');
  - L7578: throw new Error('Header not found in Account Ledger');
  - L7584: // Validate required fields in Cash Ledger
  - L7603: throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)');
  - L7606: // Validate required fields in Account Ledger
  - L7624: throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)');
  - L7627: // Read Cash Ledger rows
  - L7671: // Read Account Ledger rows for dedup
  - L7728: // Construct new row object for Account Ledger
  - L7782: var formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))';

## 5. Formula Indicator Lines

- L1705: const formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))';
- L1706: sheet.getRange(r, 6).setFormula(formula);
- L3167: sheet.getRange(r, 16).clearContent();           // amount_out
- L3171: sheet.getRange(r, 17).clearContent();           // amount_in
- L3185: function setFormulaNextToLabel_(sheet, labels, formula) {
- L3204: sheet.getRange(r + 1, targetCol).setFormula(formula);
- L3239: `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`;
- L3242: `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`;
- L3248: `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledge
- L3257: monthly.getRange('B6').setFormula(monthlyCashInFormula);
- L3258: monthly.getRange('E6').setFormula(monthlyCashOutFormula);
- L3259: monthly.getRange('B8').setFormula(monthlyNetFormula);
- L3270: setFormulaOnCellContaining_(dashboard, ['cash aktif'], dashboardCashAktifFormula);
- L3282: function setFormulaOnCellContaining_(sheet, labels, formula) {
- L3297: sheet.getRange(r + 1, c + 1).setFormula(formula);
- L4046: function safeClearRange_(sheet, a1Notation) {
- L4050: range.clearContent();
- L4051: range.clearFormat();
- L4099: asset.getRange('AA16:AE22').clearFormat().clearDataValidations();
- L4109: asset.getRange('AB19').setFormula('=IFERROR(AB17*(1-AB18);0)');
- L4115: asset.getRange('AB21').setFormula('=IFERROR(AB19-AB20;0)');
- L4175: safeClearRange_(cc, 'A1:N6');
- L4387: safeClearRange_(dashboard, 'B25:G34');
- L4540: safeClearRange_(dashboard, 'B16:G24');
- L4547: dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Acco
- L4550: dashboard.getRange('D18').setFormula(`=IFERROR('🥇 Aset'!F18;0)`);
- L4553: dashboard.getRange('D19').setFormula('=IFERROR(D17-D18;0)');
- L4556: dashboard.getRange('D20').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`);
- L4559: dashboard.getRange('D21').setFormula('=IFERROR(D19+D20;0)');
- L4563: dashboard.getRange('G17').setFormula(`=IFERROR('🥇 Aset'!AB17;0)`);
- L4566: dashboard.getRange('G18').setFormula(`=IFERROR('🥇 Aset'!AB18;0)`);
- L4569: dashboard.getRange('G19').setFormula(`=IFERROR('🥇 Aset'!AB19;0)`);
- L4572: dashboard.getRange('G20').setFormula(`=IFERROR('🥇 Aset'!AB20;0)`);
- L4575: dashboard.getRange('G21').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`);
- L4671: safeClearRange_(asset, a1);
- L4787: // Use: admin find smoke all <QUERY> to include every tab.
- L6001: const monthlyB6 = monthly ? monthly.getRange('B6').getFormula() : '';
- L6002: const monthlyE6 = monthly ? monthly.getRange('E6').getFormula() : '';
- L6003: const monthlyB8 = monthly ? monthly.getRange('B8').getFormula() : '';
- L6004: const dashboardD17 = dashboard ? dashboard.getRange('D17').getFormula() : '';
- L7782: var formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))';
- L7783: accountSheet.getRange(r, 6).setFormula(formula);

## 6. Initial Findings

1. Monthly Review cash formulas already reference Account Ledger for cash in, cash out, and net.
2. Dashboard Cash Aktif and Net Worth formulas reference Account Ledger for cash balances.
3. Dashboard credit card cycle panel reads Credit Card domain data and writes visible dashboard cells.
4. Dashboard Net Worth panel writes visible dashboard cells and clears a fixed dashboard range before repainting.
5. Some dashboard helpers are destructive by design because they clear and repaint fixed dashboard ranges.
6. Finance Events is not yet used for dashboard lineage analytics formulas.
7. Reconciliation status layer is not yet implemented as a dashboard surface.

## 7. Minimum Safe Patch Direction

A future patch should start with a read-only reconciliation/audit helper before changing dashboard visuals.

Recommended first runtime patch candidate:

- Add admin read-only reconciliation command that summarizes Account Ledger and Finance Events consistency.
- Do not overwrite dashboard cells yet.
- Return counts for missing Finance Events, missing Account Ledger references, duplicate linked_txn_id candidates, and Lainnya category warnings.
- Only after read-only reconciliation is proven should dashboard formulas be patched.

## 8. Non-goals

This inventory does not close Sprint 5.

This inventory does not deploy Apps Script.

This inventory does not modify Google Sheet formulas.

This inventory does not touch birthday reminder files.

