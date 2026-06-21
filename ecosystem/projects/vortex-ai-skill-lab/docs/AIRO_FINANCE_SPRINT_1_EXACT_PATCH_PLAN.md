# AIRO Finance — Sprint 1 Exact Patch Plan

Status: EXACT PATCH PLAN
Sprint: Sprint 1 — Account Ledger Hardening
Generated at: 2026-05-24 12:44:39
Runtime scope: Documentation only; no runtime patch in this micro-step
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document maps exact active files and function surfaces before the first Sprint 1 runtime patch.

The first runtime patch must be small, tested, and limited to Sprint 1 Account Ledger hardening.

## 2. Active Source Surface

Primary active runtime file:

- scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs

Reason:

- Highest focused audit signal.
- Contains Account Ledger sheet config.
- Contains cash-to-Account-Ledger mirror logic.
- Contains Account Ledger schema/header helpers.
- Contains internal transfer detection and two-row writer.
- Contains source_tab and linked_txn_id handling.

## 3. Exact Function Candidate Map

| Rank | Function | Lines | Signal Score | Signals |
|---:|---|---:|---:|---|
| 1 | AIRO_BACKFILL_ACCOUNT_LEDGER_FROM_CASH_LEDGER | 6820-7076 | 37 | Account Ledger:6, accountLedger:4, Cash Ledger:5, source_tab:1, linked_txn_id:5, amount_in:7, amount_out:7, balance:2 |
| 2 | refreshCashReportingFormulas | 2932-2989 | 23 | Account Ledger:17, accountLedger:6 |
| 3 | writeAccountLedgerMirror_ | 1516-1577 | 13 | Account Ledger:1, accountLedger:5, source_tab:1, linked_txn_id:3, amount_in:1, amount_out:1, balance:1 |
| 4 | AIRO_AUDIT_ACCOUNT_LEDGER_BACKFILL_CLEANUP | 7128-7247 | 11 | Account Ledger:3, accountLedger:1, source_tab:3, amount_in:2, amount_out:2 |
| 5 | ensureAccountLedgerSheet_ | 1577-1613 | 10 | accountLedger:5, source_tab:1, linked_txn_id:1, amount_in:1, amount_out:1, balance:1 |
| 6 | writeInternalTransferToAccountLedger_ | 7404-7468 | 10 | accountLedger:5, InternalTransfer:1, Cash Ledger:1, linked_txn_id:3 |
| 7 | writeCashLedger_ | 1474-1516 | 5 | Account Ledger:1, linked_txn_id:1, amount_in:1, amount_out:1, balance:1 |
| 8 | refreshCashLedgerMaintenance | 2824-2896 | 4 | amount_in:2, amount_out:2 |
| 9 | detectInternalTransfer_ | 7371-7404 | 4 | Account Ledger:1, InternalTransfer:1, internal transfer:1, Cash Ledger:1 |
| 10 | appendCreditCardPurchase_ | 6129-6179 | 3 | linked_txn_id:3 |
| 11 | fixCreditCardDateMerchantFromRawText | 6746-6820 | 3 | Account Ledger:1, Cash Ledger:1, balance:1 |
| 12 | AIRO_CLEANUP_ACCOUNT_LEDGER_BACKFILL_DUPES_20260517 | 7247-7270 | 3 | Account Ledger:2, accountLedger:1 |
| 13 | creditCardClarificationResolvedText_ | 346-371 | 2 | cc_payment:2 |
| 14 | syncCashLedgerRuntimeAmountColumns_ | 1463-1474 | 2 | amount_in:1, amount_out:1 |
| 15 | styleAccountLedgerSheet_ | 1613-1643 | 2 | accountLedger:2 |
| 16 | applyAccountLedgerRowStyle_ | 1653-1662 | 2 | accountLedger:2 |
| 17 | applyAccountLedgerAccountStyles_ | 1662-1675 | 2 | accountLedger:2 |
| 18 | appendToAssetSection_ | 1779-1813 | 2 | linked_txn_id:2 |
| 19 | markCreditCardPocketBluTransfer_ | 6179-6271 | 2 | cc_payment:2 |
| 20 | normalizeCreditCardClarificationAnswer_ | 304-315 | 1 | cc_payment:1 |
| 21 | normalizeDebtAmbiguousClarificationAnswer_ | 382-393 | 1 | debt_payment:1 |
| 22 | debtAmbiguousClarificationResolvedText_ | 507-525 | 1 | debt_payment:1 |
| 23 | accountLedgerFontColorForAccount_ | 1643-1653 | 1 | accountLedger:1 |
| 24 | appendGoldAssetRow_ | 3300-3392 | 1 | linked_txn_id:1 |
| 25 | parseCcItemKeyword_ | 6078-6099 | 1 | cc_payment:1 |
| 26 | appendDebtPaymentAndUpdateMaster_ | 6374-6439 | 1 | linked_txn_id:1 |
| 27 | appendDebtIncreaseAndUpdateMaster_ | 6439-6502 | 1 | linked_txn_id:1 |
| 28 | normalizeSupportedAccount_ | 7360-7371 | 1 | internal transfer:1 |
| 29 | handleSpecialFinanceCommand_ | 4464-5622 | 44 | Account Ledger:13, accountLedger:5, internal transfer:10, Cash Ledger:4, source_tab:1, amount_in:6, amount_out:4, balance:1 |
| 30 | setupDashboardNetWorthPanel | 4237-4341 | 12 | Account Ledger:12 |
| 31 | buildRowByHeader_ | 2078-2162 | 11 | source_tab:3, linked_txn_id:1, amount_in:4, amount_out:3 |
| 32 | fieldForHeader_ | 2170-2234 | 11 | linked_txn_id:2, amount_in:4, amount_out:5 |
| 33 | writeRouted_ | 1693-1739 | 7 | accountLedger:4, InternalTransfer:2, Cash Ledger:1 |
| 34 | getRowKey | 7270-7360 | 7 | accountLedger:1, source_tab:4, amount_in:1, amount_out:1 |
| 35 | buildDedupKey_ | 7093-7128 | 4 | Account Ledger:1, source_tab:1, amount_in:1, amount_out:1 |
| 36 | normalizeDirectionClarificationAnswer_ | 183-195 | 2 | balance:2 |
| 37 | parseType_ | 2474-2500 | 2 | cc_payment:1, debt_payment:1 |
| 38 | failOrRetry_ | 699-1091 | 1 | cc_payment:1 |
| 39 | pick | 1878-1933 | 1 | Cash Ledger:1 |

## 4. Important Direct Line Findings

These are direct source lines with Sprint 1-relevant signals.

| Line | Source Text |
|---:|---|
| 15 | cash: '💵 Cash Ledger', |
| 20 | accountLedger: '📒 Account Ledger', |
| 189 | if (/^(d\|4)$/i.test(t) \|\| /\b(saldo\|balance\|tercatat\|awal\|akhir)\b/i.test(t)) return 'balance'; |
| 308 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar tagihan\|bayar cc\|payment\|tagihan\|lunas\|pelunasan)\b/i.test(t)) return 'cc_payment'; |
| 363 | if (choice === 'cc_payment') return 'CC_PAYMENT_HELP_ONLY'; |
| 386 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment'; |
| 517 | if (choice === 'debt_payment') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 787 | if (resolvedText === 'CC_PAYMENT_HELP_ONLY') { |
| 1467 | const inCol = findCashLedgerExactHeaderCol_(sheet, 'amount_in'); |
| 1468 | const outCol = findCashLedgerExactHeaderCol_(sheet, 'amount_out'); |
| 1481 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1498 | amount_in: cashInflow ? parsed.amount : '', |
| 1499 | amount_out: cashInflow ? '' : parsed.amount, |
| 1513 | * Mirrors cash movement to the Account Ledger tab. |
| 1514 | * Balance is intentionally left blank for Google Sheet formulas. |
| 1516 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1517 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1542 | amount_in: isInflow ? amount : '', |
| 1543 | amount_out: isInflow ? '' : amount, |
| 1544 | balance: '', |
| 1549 | source_tab: sourceTab, |
| 1550 | linked_txn_id: common.linked_txn_id \|\| '', |
| 1554 | try { ensureAccountLedgerSheet_(ss); } catch (e) {} |
| 1555 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1559 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 1564 | applyAccountLedgerRowStyle_(sheet, r); |
| 1573 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1577 | function ensureAccountLedgerSheet_(ss) { |
| 1579 | 'entry_id', 'date', 'account', 'amount_in', 'amount_out', |
| 1580 | 'balance', 'type', 'category', 'description', 'raw_text', |
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
| 1709 | var transfer = detectInternalTransfer_(parsed, rawText); |
| 1711 | return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer); |
| 1714 | if (key.includes('cash ledger')) { |
| 1717 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1724 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1728 | writtenTab: AIRO_CONFIG.tabs.accountLedger |
| 1798 | linked_txn_id: data.linked_txn_id, |
| 1888 | // Cash Ledger movement type validation. |
| 2088 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2116 | headerKey === 'amount_out' \|\| |
| 2117 | headerKey.includes('amount_out') \|\| |
| 2125 | return cashInflow ? '' : (data.amount_out ?? data.amount ?? ''); |
| 2129 | headerKey === 'amount_in' \|\| |
| 2130 | headerKey.includes('amount_in') \|\| |
| 2138 | return cashInflow ? (data.amount_in \|\| data.amount \|\| '') : (data.amount_in ?? ''); |
| 2149 | if (headerKey === 'source_tab' \|\| headerKey.includes('source_tab')) { |
| 2150 | return data.source_tab \|\| data.source \|\| ''; |
| 2174 | // Important: check amount_in / amount_out before generic amount, |
| 2175 | // otherwise amount_out may be filled as expense for cash inflow rows. |
| 2177 | h === 'amount_in' \|\| |
| 2178 | h.includes('amount_in') \|\| |
| 2186 | return 'amount_in'; |
| 2190 | h === 'amount_out' \|\| |
| 2191 | h.includes('amount_out') \|\| |
| 2199 | return 'amount_out'; |
| 2214 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2478 | if (isCreditCardPaymentText_(t)) return 'cc_payment'; |
| 2481 | if (isDebtPaymentText_(t)) return 'debt_payment'; |
| 2878 | sheet.getRange(r, 16).clearContent();           // amount_out |
| 2879 | sheet.getRange(r, 17).setValue(amount);         // amount_in |
| 2881 | sheet.getRange(r, 16).setValue(amount);         // amount_out |
| 2882 | sheet.getRange(r, 17).clearContent();           // amount_in |
| 2943 | const accountLedgerMonthKeyFormula = |
| 2944 | `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`; |
| 2946 | const accountLedgerCashAccountFilterFormula = |
| 2947 | `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`; |
| 2950 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2953 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2959 | `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`; |
| 3361 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 4258 | dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`); |
| 4695 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 4701 | 'test phase d internal transfer blu cash', |
| 4702 | 'test phase d internal transfer cash blu', |
| 4703 | 'test phase d internal transfer bca cash', |
| 4704 | 'test phase d internal transfer cash bca', |
| 4955 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 4957 | 'test phase d internal transfer bca blu', |
| 4958 | 'test phase d internal transfer blu cash', |
| 4959 | 'test phase d internal transfer cash blu', |
| 4960 | 'test phase d internal transfer blu bca', |
| 4961 | 'test phase d internal transfer bca cash', |
| 4962 | 'test phase d internal transfer cash bca', |
| 5027 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5074 | const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16); |
| 5075 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5077 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5078 | const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5); |
| 5108 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5158 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5181 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5183 | const accountSourceCol = findColumn_(accountInfo, ['source_tab', 'source'], 11); |
| 5242 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5244 | 'Cash Ledger inflows recent/top:\n' + |
| 5249 | 'Buka Account Ledger: ' + link |
| 5269 | if (/^admin\s+(audit\|check\|cek)\s+cash\s+(parity\|balance\|total\|ledger)/i.test(text)) { |
| 5272 | const accountSheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 5351 | const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16); |
| 5352 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5355 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5356 | const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5); |
| 5418 | 'Cash Ledger in: Rp' + cashIn + '\n' + |
| 5419 | 'Cash Ledger out: Rp' + cashOut + '\n' + |
| 5420 | 'Cash Ledger net: Rp' + cashNet + '\n\n' + |
| 5421 | 'Account Ledger Cash in: Rp' + accountIn + '\n' + |
| 5422 | 'Account Ledger Cash out: Rp' + accountOut + '\n' + |
| 5423 | 'Account Ledger Cash net: Rp' + accountNet + '\n\n' + |
| 5426 | 'Buka Account Ledger: ' + link |
| 5474 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5475 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5477 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5485 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5486 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5488 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5523 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 6096 | return t \|\| 'cc_payment'; |
| 6146 | cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6153 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6204 | issue_reason: 'cc_payment_amount_or_columns_missing' |
| 6242 | issue_reason: 'cc_payment_no_matching_pending_purchase' |
| 6420 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6483 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6816 | * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger. |
| 6818 | * and key properties, and populates balance formulas dynamically without overwriting existing data. |
| 6826 | throw new Error('Cash Ledger sheet not found'); |
| 6829 | var accountSheet = ensureAccountLedgerSheet_(ss); |
| 6831 | throw new Error('Failed to ensure Account Ledger sheet exists'); |
| 6836 | throw new Error('Header not found in Cash Ledger'); |
| 6841 | throw new Error('Header not found in Account Ledger'); |
| 6847 | // Validate required fields in Cash Ledger |
| 6858 | return f === 'amount' \|\| f === 'amount_in' \|\| f === 'amount_out' \|\| canonicalKey_(h) === 'amount'; |
| 6866 | throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)'); |
| 6869 | // Validate required fields in Account Ledger |
| 6877 | return canonicalKey_(h) === 'amount_in'; |
| 6880 | return canonicalKey_(h) === 'amount_out'; |
| 6887 | throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)'); |
| 6890 | // Read Cash Ledger rows |
| 6910 | var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders); |
| 6912 | var amt = getFieldValue_(rowObj, 'amount', cashHeaders) \|\| getFieldValue_(rowObj, 'amount_in', cashHeaders) \|\| getFieldValue_(rowObj, 'amount_out', cashHeaders); |
| 6934 | // Read Account Ledger rows for dedup |
| 6960 | var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders); |
| 6972 | var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders); |
| 6991 | // Construct new row object for Account Ledger |
| 6998 | var amountIn = getFieldValue_(cashRow, 'amount_in', cashHeaders); |
| 6999 | var amountOut = getFieldValue_(cashRow, 'amount_out', cashHeaders); |
| 7001 | // If amount_in / amount_out is not explicitly present, calculate based on amount & type |
| 7027 | amount_in: amountIn, |
| 7028 | amount_out: amountOut, |

## 5. Runtime Candidate Files

- docs/personal-workflow/integration/AIRO_ASSET_PLANNER_SKIP_SOFT_DELETED_TRANSACTIONS.md
- docs/personal-workflow/integration/AIRO_ASSET_SECTION_UPDATE_MAPPING_FIX.md
- docs/personal-workflow/integration/AIRO_CASH_LEDGER_ROUTE_PLANNER_V1_2.md
- docs/personal-workflow/integration/AIRO_CICILAN_RUMAH_ROUTE_PLANNER_V1_2.md
- docs/personal-workflow/integration/AIRO_CICILAN_RUMAH_RUNTIME_AUDIT_PASS_2026_05_20.md
- docs/personal-workflow/integration/AIRO_CREDIT_CARD_BILLING_CYCLE_V0_8.md
- docs/personal-workflow/integration/AIRO_CREDIT_CARD_BILLING_CYCLE_V0_8_VALIDATE_PASS.md
- docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_DECISION_V1_2.md
- docs/personal-workflow/integration/AIRO_CREDIT_CARD_CYCLE_FOCUS_LOCK_2026_05_20.md
- docs/personal-workflow/integration/AIRO_CREDIT_CARD_MIRROR_PLANNER_V0_9.md
- docs/personal-workflow/integration/AIRO_CREDIT_CARD_MIRROR_PLANNER_V0_9_1_DEDUP.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_ASSET_SYNC_V1_2A_PLANNER.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_ASSET_SYNC_V1_2B_INTEGRATION.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_ASSET_SYNC_V1_2C_LIVE_PASS.md
- docs/personal-workflow/integration/AIRO_FULL_AUTO_ASSET_SYNC_V1_2D_DEDUPE_KEY_FIX.md
- docs/personal-workflow/integration/AIRO_HUTANG_ROUTE_PLANNER_V1_2.md
- docs/personal-workflow/integration/AIRO_V12_ASSET_APPEND_ONLY_REGRESSION_PASS.md
- scripts/personal-workflow/airo_asset_event_planner.py
- scripts/personal-workflow/airo_cash_ledger_planner.py
- scripts/personal-workflow/airo_cicilan_rumah_planner.py
- scripts/personal-workflow/airo_credit_card_billing_cycle.py
- scripts/personal-workflow/airo_credit_card_mirror_planner.py
- scripts/personal-workflow/airo_hutang_planner.py
- scripts/personal-workflow/airo_sheets_sync.py
- scripts/personal-workflow/airo_sheets_sync_dry_run.py
- scripts/personal-workflow/airo_sheets_sync_write_preview.py
- scripts/personal-workflow/apps-script/airo_credit_card_billing_cycle_v0_8.gs
- scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs
- tests/personal-workflow/test_airo_asset_event_planner.py
- tests/personal-workflow/test_airo_asset_event_planner_skip_deleted.py
- tests/personal-workflow/test_airo_asset_section_update_mapping.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cicilan_rumah_planner.py
- tests/personal-workflow/test_airo_credit_card_billing_cycle.py
- tests/personal-workflow/test_airo_credit_card_mirror_planner.py
- tests/personal-workflow/test_airo_hutang_planner.py
- tests/personal-workflow/test_airo_sheets_sync_skip_deleted.py

## 6. Test / Regression Candidate Files

- docs/personal-workflow/integration/AIRO_FULL_AUTO_SHEETS_SYNC_V1_1_1_SMOKE_HARDENING.md
- docs/personal-workflow/integration/AIRO_GOOGLE_SHEET_FINANCE_V1_2_UNIFIED_REGRESSION.md
- docs/personal-workflow/integration/AIRO_V12_ASSET_APPEND_ONLY_REGRESSION_PASS.md
- docs/personal-workflow/phase-8/AIRO_PHASE_8C_FINAL_SMOKE_TEST_SUITE.md
- scripts/airo_gateway_smoke.py
- scripts/airo_integration_contract_smoke.py
- scripts/personal-workflow/airo_final_smoke.py
- scripts/personal-workflow/airo_finance_prod_regression.sh
- scripts/personal-workflow/airo_finance_sheet_v12_regression.py
- scripts/personal-workflow/airo_regression_smoke.sh
- scripts/personal-workflow/runtime-tests/airo_finance_clarification_regression.sh
- scripts/personal_workflow_db_smoke.py
- scripts/personal_workflow_export_smoke.py
- scripts/personal_workflow_smoke.py
- scripts/personal_workflow_telegram_smoke.py
- tests/personal-workflow/test_airo_account_aliases.py
- tests/personal-workflow/test_airo_asset_event_planner.py
- tests/personal-workflow/test_airo_asset_event_planner_skip_deleted.py
- tests/personal-workflow/test_airo_asset_section_update_mapping.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cicilan_rumah_planner.py
- tests/personal-workflow/test_airo_credit_card_billing_cycle.py
- tests/personal-workflow/test_airo_credit_card_mirror_planner.py
- tests/personal-workflow/test_airo_finance_contract_v1_1.py
- tests/personal-workflow/test_airo_finance_language_contract.py
- tests/personal-workflow/test_airo_finance_sheet_v12_mapper_preview.py
- tests/personal-workflow/test_airo_finance_sheet_v12_regression.py
- tests/personal-workflow/test_airo_finance_sheet_v12_status.py
- tests/personal-workflow/test_airo_full_auto_sheets_sync_v13_write_path.py
- tests/personal-workflow/test_airo_gateway_finance_contract.py
- tests/personal-workflow/test_airo_gateway_idempotency_reply_safety.py
- tests/personal-workflow/test_airo_hutang_planner.py
- tests/personal-workflow/test_airo_intent_router_v13_finance_force.py
- tests/personal-workflow/test_airo_review_queue_planner.py
- tests/personal-workflow/test_airo_sheets_sync_skip_deleted.py
- tests/personal-workflow/test_airo_transaction_amount_parser.py

## 7. First Smallest Safe Patch Recommendation

Recommended first runtime patch:

Add a local regression harness for Account Ledger internal transfer row-shape and ID/source consistency before changing production logic.

Why this is first:

- Internal transfer two-sided behavior is explicitly in Sprint 1 Definition of Done.
- Active Apps Script already has internal transfer detection and writer surfaces.
- The patch can be small and local.
- The test can lock desired Account Ledger row contract before modifying runtime code.
- It avoids Cash Ledger deletion, which belongs to Sprint 3.
- It avoids broad dashboard or Finance Events work.

Expected contract to lock:

- internal transfer creates exactly two Account Ledger rows
- outflow row has amount_out populated and amount_in empty/zero
- inflow row has amount_in populated and amount_out empty/zero
- both rows share one base transaction identity
- linked_txn_id or entry_id suffixes are consistent as :out and :in
- source_tab is populated
- account values represent source and destination accounts
- no clean single-sided transfer is allowed

## 8. Patch Boundary for Next Micro-Step

Allowed next micro-step:

- add focused local test or dry-run harness
- inspect and reuse existing function names
- no Google Sheets live write
- no deploy yet unless test and syntax pass
- no Cash Ledger removal
- no Dashboard work
- no Sprint 2+ work

Not allowed next micro-step:

- full Account Ledger rewrite
- schema migration
- historical backfill
- Cash Ledger deletion
- Finance Events implementation
- dashboard source migration

## 9. Proposed Next Command

Next command should:

1. Extract the exact active functions around internal transfer and Account Ledger row mapping.
2. Add a focused regression test or static contract test.
3. Run existing Python tests.
4. Run Apps Script syntax/static checks if available.
5. Commit only the smallest test/runtime-safe patch.

If no clean test harness exists, create a docs-only patch plan update instead of runtime code.
