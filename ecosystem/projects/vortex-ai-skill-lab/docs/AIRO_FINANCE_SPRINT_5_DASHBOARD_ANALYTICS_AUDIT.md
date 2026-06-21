# AIRO Finance - Sprint 5 Dashboard / Analytics Audit

Status: EXACT AUDIT
Sprint: Sprint 5 - Dashboard / Analytics
Generated at: 2026-05-24 15:42:31
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

Sprint 5 starts after Sprint 4 Finance Events is CLOSED / PASS.

This micro-step audits dashboard, monthly review, reporting, and analytics surfaces before any runtime implementation.

No runtime patch is made in this micro-step.

## 2. Sprint 5 Boundary

Allowed now:

- inspect Dashboard and Monthly Review formulas
- inspect existing dashboard panel setup functions
- inspect analytics candidate sources
- inspect Finance Events as future analytics source
- inspect Account Ledger, domain tabs, and Review Queue as reporting sources
- define smallest safe test-first patch

Not allowed now:

- dashboard layout refactor
- formula rewrite
- chart creation
- analytics automation
- Finance Events event emission expansion
- Email Ingestion implementation
- Cash Ledger write re-enable
- destructive sheet or row operations
- broad Apps Script refactor

## 3. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `refreshCashReportingFormulas` | 3113-3168 | FOUND | Dashboard:2, dashboard:8, Monthly Review:2, monthly:16, getRange:3, setFormula:4, Cash Aktif:2, Account Ledger:17, SUMIFS:6, FILTER:2 |
| `refreshCashMonthlyReviewFormulas` | 3105-3107 | FOUND |  |
| `setupDashboardNetWorthPanel` | 4418-4520 | FOUND | Dashboard:3, dashboard:49, getRange:35, setFormula:10, setValue:12, merge:12, panel:2, Net Worth:5, Hutang:1, Aset:10, Account Ledger:12, SUMIFS:6 |
| `setupDashboardCreditCardCyclePanel` | 4255-4415 | FOUND | Dashboard:3, dashboard:40, getRange:34, setValue:22, merge:12, panel:1, Credit Card:1 |
| `setupAsetNetWorthHelpers_` | 3978-4026 | FOUND | dashboard:1, getRange:17, setFormula:2, setValue:9, panel:1, Aset:2 |
| `setupAsetHomeEquityPanel_` | MISSING | MISSING |  |
| `dashboardLayoutReadOnlyAudit_` | 4582-4642 | FOUND | Dashboard:1, dashboard:10, getRange:1, Net Worth:1, Credit Card:1, Hutang:1, Review Queue:1 |
| `handleSpecialFinanceCommand_` | 4645-5796 | FOUND | Dashboard:16, dashboard:32, Monthly Review:3, monthly:27, reporting:9, formula:13, getRange:23, setValue:3, panel:2, Net Worth:1, Credit Card:11, Aset:1, Cicilan Rumah:4, Account Ledger:13, amount_in:6, amount_out:4, source_tab:1 |
| `writeFinanceEvent_` | 1575-1580 | FOUND |  |
| `recordFinanceEventForWriteResult_` | 1816-1844 | FOUND | event_type:2, event_source:2, source_tab:2, linked_txn_id:3 |
| `writeAccountLedgerMirror_` | 1639-1693 | FOUND | formula:2, getRange:1, setFormula:1, SUMIFS:2, amount_in:1, amount_out:1, source_tab:1, linked_txn_id:3 |
| `ensureAccountLedgerSheet_` | 1700-1734 | FOUND | getRange:3, setValue:2, setValues:2, amount_in:1, amount_out:1, source_tab:1, linked_txn_id:1 |
| `ensureFinanceEventsSheet_` | 1503-1533 | FOUND | getRange:2, setValue:1, setValues:1 |
| `processReviewQueueApproved` | 2776-2895 | FOUND | getRange:2 |

## 4. Runtime Notes

- Dashboard Net Worth surface exists and should be audited before layout changes.
- Monthly Review cash reporting formulas exist and currently read Account Ledger for Cash reporting.
- Credit Card dashboard/cycle panel exists and should be guarded before Sprint 5 runtime changes.
- Finance Events exists and may become an analytics source, but Sprint 5 must not change event emission in the audit step.
- Account Ledger remains the primary wallet movement source for dashboard cash analytics.
- No sheet deletion or bulk row deletion pattern detected in active source.
- No Email Ingestion runtime surface detected.

## 5. Dashboard / Analytics Surface Matrix

| Surface | Current source candidate | Status | Sprint 5 risk |
|---|---|---:|---|
| Dashboard Cash Aktif | Account Ledger formulas | Existing | Needs layout/contract audit before changes |
| Dashboard Net Worth | Account Ledger + Aset formulas | Existing | Needs contract before any redesign |
| Monthly Review cash B6/E6/B8 | Account Ledger formulas | Existing | Already guarded by Sprint 3, keep baseline |
| Credit Card cycle panel | Credit Card tab formulas/helpers | Existing | Needs read-only audit before modification |
| Aset net worth helpers | Aset tab helper formulas | Existing | Needs guard before analytics refactor |
| Finance Events analytics | Finance Events tab | Candidate | Do not implement analytics yet; audit only |
| Review Queue analytics | Review Queue tab | Candidate | Needs policy before dashboard exposure |

## 6. Existing Relevant Test Files

- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_aset_savings_gold_contract.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cash_ledger_remaining_dependency_contract.py
- tests/personal-workflow/test_airo_cash_ledger_removal_safety_contract.py
- tests/personal-workflow/test_airo_cash_ledger_write_disable_flag_contract.py
- tests/personal-workflow/test_airo_cicilan_rumah_payment_history_contract.py
- tests/personal-workflow/test_airo_cicilan_rumah_planner.py
- tests/personal-workflow/test_airo_credit_card_billing_cycle.py
- tests/personal-workflow/test_airo_credit_card_billing_status_contract.py
- tests/personal-workflow/test_airo_credit_card_mirror_planner.py
- tests/personal-workflow/test_airo_dashboard_monthly_cash_read_contract.py
- tests/personal-workflow/test_airo_finance_events_append_writer_contract.py
- tests/personal-workflow/test_airo_finance_events_runtime_schema_contract.py
- tests/personal-workflow/test_airo_finance_events_schema_contract.py
- tests/personal-workflow/test_airo_finance_events_write_routed_emission_contract.py
- tests/personal-workflow/test_airo_hutang_master_payment_contract.py
- tests/personal-workflow/test_airo_hutang_planner.py

## 7. Recommended Next Patch

Add the smallest test-only Dashboard / Analytics contract.

The regression should lock:

- Dashboard Net Worth panel reads Account Ledger and Aset sources
- Monthly Review cash B6/E6/B8 still reads Account Ledger
- Dashboard Cash Aktif still reads Account Ledger
- Credit Card cycle dashboard panel remains present
- Finance Events exists but no analytics dashboard is implemented yet
- no Email Ingestion runtime is added
- no destructive sheet/row deletion is introduced
- Sprint 4 Finance Events emission scope remains unchanged

## 8. Direct Source Findings

| Line | Source Text |
|---:|---|
| 16 | creditCard: '💳 Credit Card', |
| 17 | cicilanRumah: '🏠 Cicilan Rumah', |
| 18 | hutang: '🤝 Hutang', |
| 19 | aset: '🥇 Aset', |
| 20 | accountLedger: '📒 Account Ledger', |
| 21 | financeEvents: '📌 Finance Events', |
| 22 | review: '🧾 Review Queue' |
| 65 | if (/^(d\|4)$/i.test(t) \|\| /\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t)) return 'Credit Card'; |
| 81 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 112 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 124 | '- 15000 credit card' |
| 206 | const hasClearAction = /\b(beli\|bayar\|makan\|minum\|kopi\|jajan\|transfer\|tf\|dari\|ke\|masuk\|keluar\|gaji\|refund\|terima\|diterima\|topup\|tarik\|cc\|credit card\|cash\|tunai)\b/i.test(text); |
| 308 | if (/^(a\|1)(\b\|[\s.:-])/i.test(t) \|\| /\b(belanja\|beli\|purchase\|transaksi baru\|pakai cc\|pakai credit card)\b/i.test(t)) return 'cc_purchase'; |
| 321 | if (!/\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(text)) return false; |
| 334 | 'Saya tangkap ada transaksi Credit Card Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 336 | 'A. Belanja pakai Credit Card\n' + |
| 337 | 'B. Bayar tagihan Credit Card\n' + |
| 355 | .replace(/\b(belanja\|beli\|purchase\|transaksi baru\|pakai cc\|pakai credit card)\b/ig, ' ') |
| 386 | if (/^(a\|1)$/i.test(t) \|\| /\b(pinjam\|pinjaman\|saya pinjam\|tambah hutang\|tambah utang)\b/i.test(t)) return 'debt_in'; |
| 387 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment'; |
| 399 | if (!/\b(hutang\|utang\|pinjaman\|pinjam)\b/i.test(text)) return false; |
| 408 | 'Saya tangkap ada transaksi Hutang Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 410 | 'A. Saya pinjam / tambah hutang\n' + |
| 411 | 'B. Saya bayar hutang\n' + |
| 412 | 'C. Orang bayar hutang ke saya / piutang\n' + |
| 416 | '- bayar hutang ke Budi 50000 dari bca' |
| 425 | if (/^(c\|3\|aset\|tabung\|tabungan\|saving\|savings\|biasa)\b/i.test(t)) return 'savings'; |
| 439 | const isGoldAsset = /\b(aset\s+emas\|emas\|gold\|antam\|logam\s+mulia)\b/i.test(text); |
| 447 | if (category && category !== 'aset') return false; |
| 455 | 'Saya tangkap ada transaksi Aset/Emas' + |
| 461 | 'C. Catat sebagai aset/tabungan biasa\n' + |
| 478 | .replace(/\baset\s+emas\b/ig, 'aset') |
| 479 | .replace(/\b(logam\s+mulia\|antam\|emas\|gold)\b/ig, 'aset') |
| 547 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 592 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 610 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 655 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 674 | 'D. Credit Card\n' + |
| 868 | 'Saya belum mencatat transaksi Aset/Emas ini.' |
| 887 | 'Saya butuh detail orang dan format lengkap untuk Hutang.\n\n' + |
| 890 | '- bayar hutang ke Budi 50000 dari bca' |
| 898 | 'Saya belum mencatat piutang/orang bayar hutang ke saya karena flow piutang belum dikunci.\n\n' + |
| 912 | 'Saya belum mencatat transaksi Hutang ini.\n\n' + |
| 915 | '- bayar hutang ke Budi 50000 dari bca' |
| 1069 | 'D. Credit Card\n' + |
| 1483 | function getFinanceEventsHeaders_() { |
| 1485 | 'event_id', |
| 1486 | 'event_ts', |
| 1487 | 'event_type', |
| 1488 | 'event_source', |
| 1503 | function ensureFinanceEventsSheet_(ss) { |
| 1505 | const headers = getFinanceEventsHeaders_(); |
| 1506 | let sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.financeEvents); |
| 1508 | sheet = ss.insertSheet(AIRO_CONFIG.tabs.financeEvents); |
| 1530 | tabName: AIRO_CONFIG.tabs.financeEvents, |
| 1535 | function financeEventPayloadJson_(payload) { |
| 1554 | function buildFinanceEvent_(event) { |
| 1555 | event = event \|\| {}; |
| 1557 | event_id: event.event_id \|\| ('fe:' + Utilities.getUuid()), |
| 1558 | event_ts: event.event_ts \|\| new Date(), |
| 1559 | event_type: event.event_type \|\| 'manual_event', |
| 1560 | event_source: event.event_source \|\| 'system', |
| 1561 | source_tab: event.source_tab \|\| '', |
| 1562 | source_row: event.source_row \|\| '', |
| 1563 | linked_txn_id: event.linked_txn_id \|\| event.entry_id \|\| '', |
| 1564 | account: event.account \|\| '', |
| 1565 | category: event.category \|\| '', |
| 1566 | amount: event.amount \|\| '', |
| 1567 | direction: event.direction \|\| '', |
| 1568 | status: event.status \|\| 'ok', |
| 1569 | reason: event.reason \|\| '', |
| 1570 | payload_json: financeEventPayloadJson_(event.payload_json \|\| event.payload \|\| ''), |
| 1571 | notes: event.notes \|\| '' |
| 1575 | function writeFinanceEvent_(ss, event) { |
| 1577 | ensureFinanceEventsSheet_(ss); |
| 1578 | const row = buildFinanceEvent_(event); |
| 1579 | return appendByHeader_(ss, AIRO_CONFIG.tabs.financeEvents, row, { createIfMissing: false }); |
| 1582 | function appendFinanceEvent_(ss, event) { |
| 1583 | return writeFinanceEvent_(ss, event); |
| 1636 | * Mirrors cash movement to the Account Ledger tab. |
| 1637 | * Balance is intentionally left blank for Google Sheet formulas. |
| 1685 | const formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))'; |
| 1686 | sheet.getRange(r, 6).setFormula(formula); |
| 1696 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1757 | if (!sheet.getFilter()) { |
| 1760 | dataRange.createFilter(); |
| 1816 | function recordFinanceEventForWriteResult_(ss, result, common, parsed, rawText, event) { |
| 1820 | event = event \|\| {}; |
| 1821 | writeFinanceEvent_(ss, { |
| 1822 | event_type: event.event_type \|\| 'transaction_created', |
| 1823 | event_source: event.event_source \|\| 'telegram', |
| 1824 | source_tab: event.source_tab \|\| result.writtenTab \|\| '', |
| 1825 | source_row: event.source_row \|\| result.row \|\| '', |
| 1826 | linked_txn_id: event.linked_txn_id \|\| common.linked_txn_id \|\| common.rowId \|\| result.rowId \|\| '', |
| 1827 | account: event.account \|\| parsed.account \|\| '', |
| 1828 | category: event.category \|\| parsed.category \|\| '', |
| 1829 | amount: event.amount \|\| parsed.amount \|\| '', |
| 1830 | direction: event.direction \|\| '', |
| 1832 | reason: event.reason \|\| '', |
| 1839 | notes: event.notes \|\| '' |
| 1850 | if (key.includes('credit card')) { |
| 1854 | if (key.includes('hutang')) { |
| 1855 | return writeHutangSafely_(ss, parsed, rawText, common); |
| 1858 | if (key.includes('aset')) { |
| 1888 | recordFinanceEventForWriteResult_(ss, result, common, parsed, rawText, { |
| 1889 | event_type: 'transaction_created', |
| 1890 | event_source: 'telegram', |
| 1901 | const tabName = AIRO_CONFIG.tabs.aset; |
| 1912 | function mirrorAssetPurchaseToAccountLedger_(result) { |
| 1917 | category: parsed.category \|\| 'Aset', |
| 1924 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1934 | return mirrorAssetPurchaseToAccountLedger_(appendGoldAssetRow_(sheet, parsed, rawText, common)); |
| 1939 | if (result.status === 'written') return mirrorAssetPurchaseToAccountLedger_({ ...result, writtenTab: tabName }); |
| 1971 | type: section === 'savings' ? savingsEventType_(data) : data.type, |
| 1994 | function savingsEventType_(data) { |
| 2047 | .filter(Boolean); |
| 2090 | // Review Queue status validation |
| 2097 | const eventType = savingsEventType_(data); |
| 2098 | if (allowedLower.includes(String(eventType).toLowerCase())) { |
| 2099 | return pick(eventType); |
| 2344 | const fields = row.map(h => fieldForHeader_(h)).filter(Boolean); |
| 2348 | .filter(f => unique.includes(f)).length; |
| 2386 | type: ['type', 'jenis', 'event_type', 'jenis_transaksi', 'transaction_type'], |
| 2397 | creditor: ['creditor', 'kreditur', 'pemberi_hutang', 'pemberi_utang', 'lender'], |
| 2428 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text)) return AIRO_CONFIG.tabs.cicilanRumah; |
| 2431 | /\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| |
| 2435 | return AIRO_CONFIG.tabs.hutang; |
| 2438 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia\|nabung\|tabung\|saving\|savings\|aset\|investasi\|dana darurat)\b/i.test(text)) return AIRO_CONFIG.tabs.aset; |
| 2464 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) { |
| 2469 | if (/\b(hutang\|utang\|pinjam\|pinjaman)\b/i.test(text) && !parseCreditor_(text)) { |
| 2473 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) && !/\b\d+(?:[.,]\d+)?\s*(jt\|juta\|rb\|ribu\|k)?\b/i.test(text)) { |
| 2577 | // "cc beli ..." / "cc bayar pdam ..." means purchase using credit card. |
| 2578 | if (typeof isCreditCardPurchaseText_ === 'function' && isCreditCardPurchaseText_(t)) return 'Credit Card'; |
| 2586 | if (/\b(tokopedia\s*cc\|tokopedia\s*card\|credit\s*card\|kartu\s*kredit\|\bcc\b)\b/i.test(t)) return 'Credit Card'; |
| 2608 | if (isBorrowInText_(t) \|\| isDebtPaymentText_(t)) return 'Hutang'; |
| 2613 | if (/\b(cicilan rumah\|kpr\|angsuran rumah)\b/i.test(t)) return 'Cicilan Rumah'; |
| 2614 | if (/\b(hutang\|utang)\b/i.test(t)) return 'Hutang'; |
| 2615 | if (/\b(nabung\|tabung\|saving\|aset\|investasi\|emas\|gold)\b/i.test(t)) return 'Aset'; |
| 2660 | if (isCreditCardPurchaseText_(t)) return 'cc_purchase'; |
| 2668 | if (/\b(nabung\|tabung\|saving\|investasi\|aset)\b/i.test(t)) { |
| 2693 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text)) return 'gold'; |
| 2694 | if (/\b(nabung\|tabung\|saving\|savings\|dana darurat\|investasi\|aset)\b/i.test(text)) return 'savings'; |
| 2764 | * Process Review Queue rows that have been manually marked approved/edited. |
| 2767 | * - Edit row in 🧾 Review Queue |
| 2929 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) \|\| parsed.category === 'Cicilan Rumah') { |
| 2933 | if (/\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| parsed.category === 'Hutang') { |
| 2934 | return AIRO_CONFIG.tabs.hutang; |
| 2937 | if (/\b(nabung\|tabung\|saving\|savings\|aset\|investasi\|emas\|gold\|dana darurat)\b/i.test(text) \|\| parsed.category === 'Aset') { |
| 2938 | return AIRO_CONFIG.tabs.aset; |
| 3069 | refreshCashMonthlyReviewFormulas(); |
| 3077 | function setFormulaNextToLabel_(sheet, labels, formula) { |
| 3096 | sheet.getRange(r + 1, targetCol).setFormula(formula); |
| 3105 | function refreshCashMonthlyReviewFormulas() { |
| 3106 | return refreshCashReportingFormulas(); |
| 3113 | function refreshCashReportingFormulas() { |
| 3116 | const dashboard = |
| 3117 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 3118 | getSheetLoose_(ss, 'Dashboard'); |
| 3120 | const monthly = |
| 3121 | getSheetLoose_(ss, '📆 Monthly Review') \|\| |
| 3122 | getSheetLoose_(ss, 'Monthly Review'); |
| 3124 | const accountLedgerMonthKeyFormula = |
| 3125 | `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`; |
| 3127 | const accountLedgerCashAccountFilterFormula = |
| 3128 | `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`; |
| 3130 | const monthlyCashInFormula = |
| 3131 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 3133 | const monthlyCashOutFormula = |
| 3134 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 3136 | const monthlyNetFormula = |
| 3139 | const dashboardCashAktifFormula = |
| 3140 | `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`; |
| 3144 | dashboard: {}, |
| 3145 | monthly: {} |
| 3148 | if (monthly) { |
| 3149 | monthly.getRange('B6').setFormula(monthlyCashInFormula); |
| 3150 | monthly.getRange('E6').setFormula(monthlyCashOutFormula); |
| 3151 | monthly.getRange('B8').setFormula(monthlyNetFormula); |
| 3153 | result.monthly.cash_masuk = 'B6'; |
| 3154 | result.monthly.cash_keluar = 'E6'; |
| 3155 | result.monthly.net = 'B8'; |
| 3157 | result.monthly.missing = true; |
| 3160 | if (dashboard) { |
| 3161 | result.dashboard.cash_aktif = |
| 3162 | setFormulaOnCellContaining_(dashboard, ['cash aktif'], dashboardCashAktifFormula); |
| 3164 | result.dashboard.missing = true; |
| 3170 | function refreshCashMonthlyReviewFormulas() { |
| 3171 | return refreshCashReportingFormulas(); |
| 3174 | function setFormulaOnCellContaining_(sheet, labels, formula) { |
| 3189 | sheet.getRange(r + 1, c + 1).setFormula(formula); |
| 3349 | * Sync current gold price from Script Properties to the Aset sheet. |
| 3354 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3381 | * 3. Write price to Aset!F12 |
| 3422 | writes_to: '🥇 Aset!F12' |
| 3524 | ].filter(Boolean).join(' \| '); |
| 3529 | // A gold_event_id |
| 3581 | const hasGoldEvent = normalized.includes('gold_event_id'); |
| 3585 | if (hasGoldEvent && hasGramsIn && hasRawText) { |
| 3604 | gold_event_id: ['gold_event_id', 'event_id', 'id'], |
| 3629 | const isGoldAsset = /\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text); |
| 3740 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3752 | const eventId = String(row[0] \|\| ''); |
| 3757 | const isGoldRow = eventId.startsWith('tg:') \|\| rawText.includes('aset emas') \|\| rawText.includes('emas'); |
| 3791 | normalized.includes('gold_event_id') && |
| 3837 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3898 | * Remove old duplicate Net Worth/Home Equity panels from earlier layout attempts. |
| 3899 | * Keeps only the final safe panel in: |
| 3901 | * - AD:AE = Net Worth Final |
| 3953 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 3954 | getSheetLoose_(ss, 'Aset'); |
| 3956 | const dashboard = |
| 3957 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 3958 | getSheetLoose_(ss, 'Dashboard'); |
| 3964 | if (!dashboard) { |
| 3965 | return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 3968 | const helper = setupAsetNetWorthHelpers_(asset); |
| 3969 | const panel = setupDashboardNetWorthPanel(); |
| 3974 | panel |
| 3978 | function setupAsetNetWorthHelpers_(asset) { |
| 3981 | // Helper cells only. They may be hidden; dashboard is the visible panel. |
| 4001 | asset.getRange('AB19').setFormula('=IFERROR(AB17*(1-AB18);0)'); |
| 4007 | asset.getRange('AB21').setFormula('=IFERROR(AB19-AB20;0)'); |
| 4012 | // Hide helper columns if possible so Aset stays clean. |
| 4046 | getSheetLoose_(ss, 'Credit Card'); |
| 4255 | function setupDashboardCreditCardCyclePanel() { |
| 4258 | const dashboard = |
| 4259 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 4260 | getSheetLoose_(ss, 'Dashboard'); |
| 4264 | getSheetLoose_(ss, 'Credit Card'); |
| 4266 | if (!dashboard) return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 4278 | ensureSheetSize_(dashboard, 38, 8); |
| 4279 | safeClearRange_(dashboard, 'B25:G34'); |
| 4346 | dashboard.getRange('B25:G25').merge(); |
| 4347 | dashboard.getRange('B25').setValue('💳 CREDIT CARD — TOKOPEDIA CC'); |
| 4349 | dashboard.getRange('B26:C26').merge().setValue('Tagihan Jatuh Tempo'); |
| 4350 | dashboard.getRange('D26').setValue(payableCycle.id); |
| 4351 | dashboard.getRange('E26:F26').merge().setValue(formatDateYmd_(payableCycle.start) + ' – ' + formatDateYmd_(payableCycle.end)); |
| 4352 | dashboard.getRange('G26').setValue('Due ' + formatDateYmd_(payableDueDate)); |
| 4354 | dashboard.getRange('B27:C27').merge().setValue('Total Tagihan'); |
| 4355 | dashboard.getRange('D27').setValue(stats.payable_total); |
| 4356 | dashboard.getRange('E27:F27').merge().setValue('Belum ke Blu'); |
| 4357 | dashboard.getRange('G27').setValue(stats.payable_belum_blu); |
| 4359 | dashboard.getRange('B28:C28').merge().setValue('Status'); |
| 4360 | dashboard.getRange('D28').setValue(overdue ? 'OVERDUE / CEK BLU' : (stats.payable_belum_blu > 0 ? 'PERLU SIAPKAN BLU' : 'AMAN')); |
| 4361 | dashboard.getRange('E28:F28').merge().setValue('Rows'); |
| 4362 | dashboard.getRange('G28').setValue(stats.payable_rows); |
| 4364 | dashboard.getRange('B30:C30').merge().setValue('Periode Berjalan / Unbilled'); |
| 4365 | dashboard.getRange('D30').setValue(currentCycle.id); |
| 4366 | dashboard.getRange('E30:F30').merge().setValue(formatDateYmd_(currentCycle.start) + ' – ' + formatDateYmd_(currentCycle.end)); |
| 4367 | dashboard.getRange('G30').setValue('Belum closing'); |
| 4369 | dashboard.getRange('B31:C31').merge().setValue('Total Sementara'); |
| 4370 | dashboard.getRange('D31').setValue(stats.unbilled_total); |
| 4371 | dashboard.getRange('E31:F31').merge().setValue('Belum ke Blu'); |
| 4372 | dashboard.getRange('G31').setValue(stats.unbilled_belum_blu); |
| 4374 | dashboard.getRange('B33:G33').merge(); |
| 4375 | dashboard.getRange('B33').setValue('Catatan: “Belum ke Blu” = dana bayar CC belum disiapkan di Pocket Blu khusus pembayaran CC.'); |
| 4377 | dashboard.getRange('D27:G27').setNumberFormat('"Rp" #,##0'); |
| 4378 | dashboard.getRange('D31:G31').setNumberFormat('"Rp" #,##0'); |
| 4380 | dashboard.getRange('B25:G25') |
| 4386 | dashboard.getRange('B26:G28') |
| 4390 | dashboard.getRange('B30:G31') |
| 4394 | dashboard.getRange('B33:G33') |
| 4398 | dashboard.getRange('B25:G33').setVerticalAlignment('middle'); |
| 4399 | dashboard.getRange('B26:C31').setFontWeight('bold'); |
| 4400 | dashboard.getRange('E26:F31').setFontWeight('bold'); |
| 4404 | dashboard_panel: 'B25:G33', |
| 4413 | tab_url: getSheetTabUrl_(ss, dashboard) |
| 4418 | function setupDashboardNetWorthPanel() { |
| 4421 | const dashboard = |
| 4422 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 4423 | getSheetLoose_(ss, 'Dashboard'); |
| 4425 | if (!dashboard) { |
| 4426 | return { ok: false, reason: 'dashboard_sheet_missing' }; |
| 4429 | ensureSheetSize_(dashboard, 26, 8); |
| 4431 | // Visible dashboard panel area. |
| 4432 | safeClearRange_(dashboard, 'B16:G24'); |
| 4434 | dashboard.getRange('B16:G16').merge(); |
| 4435 | dashboard.getRange('B16').setValue('💰 NET WORTH & HOME EQUITY'); |
| 4437 | // Left block: Net Worth |
| 4438 | dashboard.getRange('B17:C17').merge().setValue('Total Aset Likuid'); |
| 4439 | dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`); |
| 4441 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4442 | dashboard.getRange('D18').setFormula(`=IFERROR('🥇 Aset'!F18;0)`); |
| 4444 | dashboard.getRange('B19:C19').merge().setValue('Net Worth Likuid'); |
| 4445 | dashboard.getRange('D19').setFormula('=IFERROR(D17-D18;0)'); |
| 4447 | dashboard.getRange('B20:C20').merge().setValue('Ekuitas Rumah'); |
| 4448 | dashboard.getRange('D20').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4450 | dashboard.getRange('B21:C21').merge().setValue('Net Worth Total'); |
| 4451 | dashboard.getRange('D21').setFormula('=IFERROR(D19+D20;0)'); |
| 4454 | dashboard.getRange('E17:F17').merge().setValue('Nilai Rumah Pasar'); |
| 4455 | dashboard.getRange('G17').setFormula(`=IFERROR('🥇 Aset'!AB17;0)`); |
| 4457 | dashboard.getRange('E18:F18').merge().setValue('Haircut Konservatif'); |
| 4458 | dashboard.getRange('G18').setFormula(`=IFERROR('🥇 Aset'!AB18;0)`); |
| 4460 | dashboard.getRange('E19:F19').merge().setValue('Nilai Rumah Konservatif'); |
| 4461 | dashboard.getRange('G19').setFormula(`=IFERROR('🥇 Aset'!AB19;0)`); |
| 4463 | dashboard.getRange('E20:F20').merge().setValue('Sisa Pokok Rumah'); |
| 4464 | dashboard.getRange('G20').setFormula(`=IFERROR('🥇 Aset'!AB20;0)`); |
| 4466 | dashboard.getRange('E21:F21').merge().setValue('Ekuitas Rumah'); |
| 4467 | dashboard.getRange('G21').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4469 | dashboard.getRange('B23:G23').merge(); |
| 4470 | dashboard.getRange('B23').setValue('Catatan: Net Worth Likuid tidak memasukkan rumah. Net Worth Total memasukkan ekuitas rumah konservatif.'); |
| 4473 | dashboard.getRange('D17:D21').setNumberFormat('"Rp" #,##0'); |
| 4474 | dashboard.getRange('G17:G21').setNumberFormat('"Rp" #,##0'); |
| 4475 | dashboard.getRange('G18').setNumberFormat('0.00%'); |
| 4477 | dashboard.getRange('B16:G16') |
| 4483 | dashboard.getRange('B17:C21') |
| 4487 | dashboard.getRange('E17:F21') |
| 4491 | dashboard.getRange('D19:D21') |
| 4495 | dashboard.getRange('G21') |
| 4499 | dashboard.getRange('B16:G21').setBorder(true, true, true, true, true, true); |
| 4501 | dashboard.getRange('B23:G23') |
| 4506 | dashboard.setColumnWidth(2, 135); // B |
| 4507 | dashboard.setColumnWidth(3, 95);  // C |
| 4508 | dashboard.setColumnWidth(4, 150); // D |
| 4509 | dashboard.setColumnWidth(5, 135); // E |
| 4510 | dashboard.setColumnWidth(6, 95);  // F |
| 4511 | dashboard.setColumnWidth(7, 150); // G |
| 4513 | dashboard.getRange('B16:G23').setVerticalAlignment('middle'); |
| 4517 | dashboard_panel: 'B16:G23', |
| 4518 | tab_url: getSheetTabUrl_(ss, dashboard) |
| 4522 | function cleanupDuplicateNetWorthPanels() { |
| 4526 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 4527 | getSheetLoose_(ss, 'Aset'); |
| 4535 | // Remove visible duplicate panels from Aset only. |
| 4536 | // Do not touch Gold Summary, Gold Ledger, or original Estimasi Net Worth. |
| 4547 | const isDuplicatePanel = |
| 4549 | text.includes('net worth final'); |
| 4551 | if (!isDuplicatePanel) continue; |
| 4582 | function dashboardLayoutReadOnlyAudit_(ss) { |
| 4583 | const dashboard = |
| 4584 | getSheetLoose_(ss, AIRO_CONFIG.tabs.dashboard) \|\| |
| 4585 | getSheetLoose_(ss, 'Dashboard'); |
| 4587 | if (!dashboard) { |
| 4590 | reason: 'dashboard_sheet_missing' |
| 4594 | const maxRows = Math.min(dashboard.getMaxRows(), 80); |
| 4595 | const maxCols = Math.min(dashboard.getMaxColumns(), 12); |
| 4596 | const values = dashboard.getRange(1, 1, maxRows, maxCols).getDisplayValues(); |
| 4612 | 'Net Worth', |
| 4615 | 'Credit Card', |
| 4617 | 'Hutang', |
| 4619 | 'Review Queue', |
| 4633 | command: 'dashboard_layout_read_only_audit', |
| 4634 | sheet_name: dashboard.getName(), |
| 4675 | '✅ Tanggal dan merchant Credit Card dirapikan.\n\n' + |
| 4700 | '✅ Kolom Credit Card dirapikan.\n\n' + |
| 4720 | sendTelegram_(chatId, 'Cicilan Rumah audit gagal: sheet Cicilan Rumah tidak ditemukan.'); |
| 4761 | 'Cicilan Rumah audit gagal: header payment history tidak ditemukan.\n\n' + |
| 4850 | 'Cicilan Rumah runtime audit selesai.\n\n' + |
| 4960 | 'Credit Card tab cycle header direfresh.\n\n' + |
| 4966 | (link ? 'Buka Credit Card: ' + link : '') |
| 4977 | if (/^admin\s+(refresh\|sync\|update\|reload)\s+cc\s+(dashboard\|cycle\s+dashboard\|billing\s+dashboard\|tagihan\s+dashboard)/i.test(text)) { |
| 4978 | const result = setupDashboardCreditCardCyclePanel(); |
| 4983 | 'Credit Card Dashboard cycle panel direfresh.\n\n' + |
| 4989 | 'Panel: ' + ((result && result.dashboard_panel) \|\| '-') + '\n\n' + |
| 4990 | (link ? '🔗 Buka Dashboard: ' + link : '') |
| 4996 | command: 'cc_dashboard_cycle_refresh', |
| 5007 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: tab Credit Card tidak ditemukan.'); |
| 5018 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: header Credit Card tidak ditemukan.'); |
| 5100 | 'Credit Card cycle audit selesai.\n\n' + |
| 5121 | 'Credit Card cycle audit error.\n\n' + |
| 5423 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5430 | 'Buka Account Ledger: ' + link |
| 5602 | 'Account Ledger Cash in: Rp' + accountIn + '\n' + |
| 5603 | 'Account Ledger Cash out: Rp' + accountOut + '\n' + |
| 5604 | 'Account Ledger Cash net: Rp' + accountNet + '\n\n' + |
| 5607 | 'Buka Account Ledger: ' + link |
| 5619 | if (/^admin\s+(audit\|check\|cek)\s+dashboard\s+(layout\|sheet\|read\s*only\|readonly)/i.test(text)) { |
| 5621 | const result = dashboardLayoutReadOnlyAudit_(ss); |
| 5624 | 'Dashboard layout audit selesai.\n\n' + |
| 5632 | command: 'dashboard_layout_read_only_audit', |
| 5637 | if (/^admin\s+(audit\|check\|cek)\s+(cash\s+)?(reporting\|report\|formula\|formulas\|dashboard)/i.test(text)) { |
| 5639 | const dashboard = |
| 5640 | getSheetLoose_(ss, '?? Dashboard') \|\| |
| 5641 | getSheetLoose_(ss, 'Dashboard'); |
| 5642 | const monthly = |
| 5643 | getSheetLoose_(ss, '?? Monthly Review') \|\| |
| 5644 | getSheetLoose_(ss, 'Monthly Review'); |
| 5646 | const monthlyB6 = monthly ? monthly.getRange('B6').getFormula() : ''; |
| 5647 | const monthlyE6 = monthly ? monthly.getRange('E6').getFormula() : ''; |
| 5648 | const monthlyB8 = monthly ? monthly.getRange('B8').getFormula() : ''; |
| 5649 | const dashboardD17 = dashboard ? dashboard.getRange('D17').getFormula() : ''; |
| 5650 | const formulaSnippet_ = function(value) { |
| 5655 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5656 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5657 | monthly_b8_present: Boolean(monthlyB8), |
| 5658 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5661 | const link = dashboard ? getSheetTabUrl_(ss, dashboard) : ss.getUrl(); |
| 5665 | '? Audit formula cash reporting selesai.\n\n' + |
| 5666 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5667 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5668 | 'Monthly B8 formula ada: ' + result.monthly_b8_present + '\n' + |
| 5669 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5670 | 'B6: ' + formulaSnippet_(monthlyB6) + '\n' + |
| 5671 | 'E6: ' + formulaSnippet_(monthlyE6) + '\n' + |
| 5672 | 'D17: ' + formulaSnippet_(dashboardD17) + '\n\n' + |
| 5673 | '?? Buka Dashboard: ' + link |
| 5679 | command: 'cash_reporting_formula_audit', |
| 5681 | formulas: { |
| 5682 | monthly_b6: monthlyB6, |
| 5683 | monthly_e6: monthlyE6, |
| 5684 | monthly_b8: monthlyB8, |
| 5685 | dashboard_d17: dashboardD17 |
| 5687 | dashboard_url: link |
| 5691 | if (/^admin\s+(refresh\|sync\|update\|reload)\s+(cash\s+)?(reporting\|report\|formula\|formulas\|dashboard)/i.test(text)) { |
| 5692 | const reporting = refreshCashReportingFormulas(); |
| 5693 | const netWorth = setupDashboardNetWorthPanel(); |
| 5696 | const dashboard = |
| 5697 | getSheetLoose_(ss, '?? Dashboard') \|\| |
| 5698 | getSheetLoose_(ss, 'Dashboard'); |
| 5699 | const link = dashboard ? getSheetTabUrl_(ss, dashboard) : ss.getUrl(); |
| 5703 | '? Reporting formula direfresh.\n\n' + |
| 5704 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 5705 | '?? Buka Dashboard: ' + link |
| 5710 | ok: Boolean(reporting && reporting.ok), |
| 5711 | command: 'cash_reporting_refresh', |
| 5712 | reporting, |
| 5714 | dashboard_url: link |
| 5725 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5726 | getSheetLoose_(ss, 'Aset'); |
| 5728 | const dashboard = |
| 5729 | getSheetLoose_(ss, '🏠 Dashboard') \|\| |
| 5730 | getSheetLoose_(ss, 'Dashboard'); |
| 5732 | if (!asset \|\| !dashboard) { |
| 5776 | const link = getSheetTabUrl_(ss, dashboard); |
| 5783 | '✅ Konfigurasi Net Worth diperbarui.\n\n' + |
| 5785 | '🔗 Buka Dashboard: ' + link |
| 5794 | dashboard_url: link |
| 5800 | * Hide legacy net worth block in 🥇 Aset. |
| 5801 | * It is kept for formula compatibility, but final Net Worth source of truth is Dashboard. |
| 5803 | function hideLegacyAsetNetWorthPanel() { |
| 5806 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5807 | getSheetLoose_(ss, 'Aset'); |
| 5814 | // row 16-21 contains old ESTIMASI NET WORTH that still subtracts cicilan rumah. |
| 5815 | // Keep values/formulas but hide visually. |
| 5821 | note: 'Legacy Aset Net Worth hidden. Use Dashboard Net Worth panel as source of truth.' |
| 5825 | function showLegacyAsetNetWorthPanel() { |
| 5828 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5829 | getSheetLoose_(ss, 'Aset'); |
| 5961 | /^bayar\s+tagihan\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t) |
| 5971 | /\b(pinjam\|dipinjamkan\|minjem\|hutang ke saya\|utang ke saya\|dipinjami)\b/i.test(t) \|\| |
| 5972 | /\b(dapat\|terima)\s+(pinjaman\|hutang\|utang)\b/i.test(t) |
| 5979 | return /\b(bayar\|lunasi\|nyicil\|cicil)\b.*\b(hutang\|utang\|pinjaman)\b/i.test(t); |
| 5989 | // This prevents category/type like Gaji, CC Payment, debt_in from being blanked. |
| 6007 | .filter(Boolean); |
| 6033 | .filter(Boolean); |
| 6058 | function isCreditCardPurchaseText_(text) { |
| 6072 | return /\b(refund\|pengembalian\|dikembalikan\|retur)\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i |
| 6107 | function writeHutangSafely_(ss, parsed, rawText, common) { |
| 6108 | const tabName = AIRO_CONFIG.tabs.hutang; |
| 6115 | issue_reason: 'hutang_tab_missing' |
| 6121 | // "mamak bayar hutang ke saya" is receivable/piutang, not current personal debt payment. |
| 6122 | if (/\bbayar\b.*\b(hutang\|utang)\b.*\bke saya\b/i.test(text)) { |
| 6127 | issue_reason: 'orang_bayar_hutang_ke_saya_needs_piutang_flow' |
| 6142 | issue_reason: 'hutang_intent_unclear' |
| 6253 | const words = t.split(/\s+/).filter(Boolean).slice(0, 3); |
| 6409 | const words = keyword.split(/\s+/).filter(w => w.length >= 3); |
| 6429 | category: parsed.category \|\| 'Credit Card Payment', |
| 6449 | ].filter(Boolean).join(' \| '); |
| 6464 | function findHutangMasterHeader_(sheet) { |
| 6472 | normalized.includes('hutang_id') && |
| 6487 | function findHutangPaymentHeader_(sheet) { |
| 6496 | normalized.includes('hutang_id') && |
| 6510 | function hutangColMap_(headers) { |
| 6532 | let m = text.match(/\bbayar\s+(?:hutang\|utang)\s+ke\s+(.+?)\s+\d/i); |
| 6542 | const map = hutangColMap_(masterHeader.headers); |
| 6568 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6569 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6575 | issue_reason: 'hutang_header_missing' |
| 6586 | issue_reason: 'hutang_payment_person_or_amount_missing' |
| 6596 | issue_reason: 'hutang_person_not_found_in_master' |
| 6601 | const hutangId = map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : ''; |
| 6609 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6614 | hutang_id: hutangId, |
| 6625 | category: parsed.category \|\| 'Hutang', |
| 6632 | writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.hutang); |
| 6645 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6646 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6652 | issue_reason: 'hutang_header_missing' |
| 6663 | issue_reason: 'hutang_increase_person_or_amount_missing' |
| 6673 | issue_reason: 'hutang_person_not_found_in_master' |
| 6684 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6689 | hutang_id: map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : '', |
| 6708 | const map = hutangColMap_(paymentHeader.headers); |
| 6892 | .filter(Boolean) |
| 7021 | * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger. |
| 7023 | * and key properties, and populates balance formulas dynamically without overwriting existing data. |
| 7036 | throw new Error('Failed to ensure Account Ledger sheet exists'); |
| 7046 | throw new Error('Header not found in Account Ledger'); |
| 7074 | // Validate required fields in Account Ledger |
| 7092 | throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)'); |
| 7114 | // Filter empty rows |
| 7139 | // Read Account Ledger rows for dedup |
| 7196 | // Construct new row object for Account Ledger |
| 7247 | // Set formula balance |
| 7250 | var formula = '=IF(C' + r + '="";"";SUMIFS($D$2:D' + r + ';$C$2:C' + r + ';C' + r + ')-SUMIFS($E$2:E' + r + ';$C$2:C' + r + ';C' + r + '))'; |
| 7251 | accountSheet.getRange(r, 6).setFormula(formula); |
| 7330 | * Audit function for Account Ledger to identify missing source_tab, cash backfill rows, and duplicate candidates. |
| 7339 | throw new Error('Account Ledger sheet not found'); |
| 7344 | throw new Error('Header not found in Account Ledger'); |
| 7450 | * Safe, specific manual cleanup function for duplicate rows and blank source_tab in Account Ledger. |
| 7458 | throw new Error('Account Ledger sheet not found'); |
| 7463 | throw new Error('Header not found in Account Ledger'); |
| 7606 | * Writes an internal transfer to the Account Ledger as two separate entries (outflow and inflow) |

## 9. Next Micro-Step

Recommended next command:

- add test-only Dashboard / Analytics contract
- run Sprint 5 audit contract
- run Sprint 4 Finance Events baselines
- run Sprint 3 Cash Ledger baselines
- run Sprint 2 domain baselines
- run Sprint 1 Account Ledger baselines
- run Apps Script syntax check
- commit the smallest test-only patch
