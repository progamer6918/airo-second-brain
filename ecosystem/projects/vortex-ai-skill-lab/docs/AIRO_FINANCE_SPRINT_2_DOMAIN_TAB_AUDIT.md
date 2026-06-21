# AIRO Finance - Sprint 2 Domain Tab Maturation Audit

Status: AUDIT STARTED
Sprint: Sprint 2 - Domain Tab Maturation
Generated at: 2026-05-24 13:27:56
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Sprint 2 Boundary

Sprint 2 starts after Sprint 1 Account Ledger Hardening is CLOSED / PASS.

This micro-step is read-only audit only.

Allowed:

- inspect domain tab runtime surfaces
- inspect existing tests
- map Credit Card, Hutang, Aset, Cicilan Rumah, and Review Queue maturity gaps
- define smallest safe patch order

Not allowed in this micro-step:

- runtime Apps Script patch
- schema migration
- dashboard finalization
- Finance Events implementation
- Cash Ledger deletion
- Sprint 3 work

## 2. Sprint 2 Candidate Domain Tabs

Domain tabs in scope for maturation audit:

- Credit Card
- Hutang
- Aset
- Cicilan Rumah
- Review Queue

Sprint 2 should mature domain tabs without breaking Sprint 1 Account Ledger source-of-truth behavior.

## 3. Function Surface Map

| Domain | Function | Lines | Status | Signals |
|---|---|---:|---:|---|
| Credit Card | `isCreditCardPaymentText_` | 5795-5802 | FOUND |  |
| Credit Card | `appendCreditCardPurchase_` | 6149-6195 | FOUND | appendByHeader_:1, linked_txn_id:3, status_pocket_blu:1, billing_cycle:1, issue_reason:1 |
| Credit Card | `markCreditCardPocketBluTransfer_` | 6199-6301 | FOUND | appendByHeader_:3, writeAccountLedgerMirror_:1, linked_txn_id:2, status_pocket_blu:1, issue_reason:3 |
| Credit Card | `normalizeCreditCardClarificationAnswer_` | 304-313 | FOUND |  |
| Credit Card | `creditCardClarificationResolvedText_` | 346-367 | FOUND |  |
| Credit Card | `createCreditCardBillingCycleSummary_` | MISSING | MISSING |  |
| Hutang | `writeHutangSafely_` | 5946-5983 | FOUND | appendByHeader_:3, issue_reason:3 |
| Hutang | `appendDebtPaymentAndUpdateMaster_` | 6406-6481 | FOUND | appendByHeader_:3, writeAccountLedgerMirror_:1, linked_txn_id:3, pay_id:1, issue_reason:3 |
| Hutang | `appendDebtIncreaseAndUpdateMaster_` | 6483-6544 | FOUND | appendByHeader_:3, linked_txn_id:1, pay_id:1, issue_reason:3 |
| Hutang | `appendDebtPaymentLog_` | 6546-6558 | FOUND |  |
| Hutang | `findHutangMasterHeader_` | 6303-6324 | FOUND |  |
| Hutang | `findHutangPaymentHeader_` | 6326-6347 | FOUND | pay_id:1 |
| Aset | `writeAssetSafely_` | 1739-1793 | FOUND | appendByHeader_:3, writeAccountLedgerMirror_:1, linked_txn_id:2, asset_section:1, fallback_reason:3 |
| Aset | `appendToAssetSection_` | 1799-1828 | FOUND | linked_txn_id:2, asset_section:2 |
| Aset | `appendGoldAssetRow_` | 3320-3406 | FOUND | linked_txn_id:1, gold_event_id:1 |
| Aset | `parseGoldAsset_` | 3466-3507 | FOUND |  |
| Aset | `parseAssetSection_` | 2531-2535 | FOUND |  |
| Aset | `setupAsetNetWorthHelpers_` | 3817-3865 | FOUND |  |
| Cicilan Rumah | `auditCicilanRumah_` | MISSING | MISSING |  |
| Cicilan Rumah | `findCicilanRumahPaymentHeader_` | MISSING | MISSING |  |
| Cicilan Rumah | `findCicilanRumahMasterHeader_` | MISSING | MISSING |  |
| Review Queue | `appendByHeader_` | 2000-2047 | FOUND | appendByHeader_:1 |
| Review Queue | `routeToTab_` | MISSING | MISSING |  |
| Review Queue | `handlePendingClarification_` | MISSING | MISSING |  |

## 4. Existing Test Candidates

- tests/personal-workflow/test_airo_account_aliases.py
- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_asset_event_planner.py
- tests/personal-workflow/test_airo_asset_event_planner_skip_deleted.py
- tests/personal-workflow/test_airo_asset_section_update_mapping.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cicilan_rumah_planner.py
- tests/personal-workflow/test_airo_credit_card_billing_cycle.py
- tests/personal-workflow/test_airo_credit_card_mirror_planner.py
- tests/personal-workflow/test_airo_finance_sheet_v12_mapper_preview.py
- tests/personal-workflow/test_airo_hutang_planner.py
- tests/personal-workflow/test_airo_review_queue_planner.py

## 5. Direct Source Findings

| Line | Source Text |
|---:|---|
| 16 | creditCard: '💳 Credit Card', |
| 17 | cicilanRumah: '🏠 Cicilan Rumah', |
| 18 | hutang: '🤝 Hutang', |
| 19 | aset: '🥇 Aset', |
| 21 | review: '🧾 Review Queue' |
| 64 | if (/^(d\|4)$/i.test(t) \|\| /\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t)) return 'Credit Card'; |
| 80 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 111 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 123 | '- 15000 credit card' |
| 131 | if (/^(a\|1)$/i.test(t) \|\| /\b(masuk\|terima\|diterima\|income\|pemasukan)\b/i.test(t)) return 'cash_in'; |
| 187 | if (/^(b\|2)$/i.test(t) \|\| /\b(masuk\|pemasukan\|income\|terima\|diterima\|refund\|gaji)\b/i.test(t)) return 'in'; |
| 205 | const hasClearAction = /\b(beli\|bayar\|makan\|minum\|kopi\|jajan\|transfer\|tf\|dari\|ke\|masuk\|keluar\|gaji\|refund\|terima\|diterima\|topup\|tarik\|cc\|credit card\|cash\|tunai)\b/i.test(text); |
| 231 | if (direction === 'in') return ('pemasukan ' + amount + ' ke ' + account + ' ' + tail).trim(); |
| 304 | function normalizeCreditCardClarificationAnswer_(text) { |
| 307 | if (/^(a\|1)(\b\|[\s.:-])/i.test(t) \|\| /\b(belanja\|beli\|purchase\|transaksi baru\|pakai cc\|pakai credit card)\b/i.test(t)) return 'cc_purchase'; |
| 308 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar tagihan\|bayar cc\|payment\|tagihan\|lunas\|pelunasan)\b/i.test(t)) return 'cc_payment'; |
| 315 | function canAskCreditCardAmbiguousClarification_(parsed, rawText) { |
| 320 | if (!/\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(text)) return false; |
| 331 | function buildCreditCardAmbiguousClarificationMessage_(parsed) { |
| 333 | 'Saya tangkap ada transaksi Credit Card Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 335 | 'A. Belanja pakai Credit Card\n' + |
| 336 | 'B. Bayar tagihan Credit Card\n' + |
| 346 | function creditCardClarificationResolvedText_(pending, rawText) { |
| 347 | const choice = normalizeCreditCardClarificationAnswer_(rawText); |
| 354 | .replace(/\b(belanja\|beli\|purchase\|transaksi baru\|pakai cc\|pakai credit card)\b/ig, ' ') |
| 363 | if (choice === 'cc_payment') return 'CC_PAYMENT_HELP_ONLY'; |
| 385 | if (/^(a\|1)$/i.test(t) \|\| /\b(pinjam\|pinjaman\|saya pinjam\|tambah hutang\|tambah utang)\b/i.test(t)) return 'debt_in'; |
| 386 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment'; |
| 387 | if (/^(c\|3)$/i.test(t) \|\| /\b(piutang\|orang bayar\|ke saya)\b/i.test(t)) return 'piutang_help'; |
| 398 | if (!/\b(hutang\|utang\|pinjaman\|pinjam)\b/i.test(text)) return false; |
| 407 | 'Saya tangkap ada transaksi Hutang Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 409 | 'A. Saya pinjam / tambah hutang\n' + |
| 410 | 'B. Saya bayar hutang\n' + |
| 411 | 'C. Orang bayar hutang ke saya / piutang\n' + |
| 415 | '- bayar hutang ke Budi 50000 dari bca' |
| 419 | function normalizeAssetGoldAmbiguousClarificationAnswer_(text) { |
| 424 | if (/^(c\|3\|aset\|tabung\|tabungan\|saving\|savings\|biasa)\b/i.test(t)) return 'savings'; |
| 430 | function hasExplicitAssetGoldAction_(text) { |
| 436 | function canAskAssetGoldAmbiguousClarification_(parsed, rawText) { |
| 438 | const isGoldAsset = /\b(aset\s+emas\|emas\|gold\|antam\|logam\s+mulia)\b/i.test(text); |
| 440 | if (!isGoldAsset) return false; |
| 441 | if (hasExplicitAssetGoldAction_(text)) return false; |
| 446 | if (category && category !== 'aset') return false; |
| 447 | if (type && type !== 'asset') return false; |
| 452 | function buildAssetGoldAmbiguousClarificationMessage_(parsed) { |
| 454 | 'Saya tangkap ada transaksi Aset/Emas' + |
| 458 | 'A. Beli / tambah emas\n' + |
| 459 | 'B. Jual / kurangi emas\n' + |
| 460 | 'C. Catat sebagai aset/tabungan biasa\n' + |
| 463 | '- beli emas 2 gram harga 3jt\n' + |
| 464 | '- jual emas 1 gram harga 1.5jt\n' + |
| 469 | function buildAssetGoldClarifiedText_(choice, rawText) { |
| 472 | if (choice === 'buy') return hasExplicitAssetGoldAction_(text) ? text : 'beli ' + text; |
| 473 | if (choice === 'sell') return hasExplicitAssetGoldAction_(text) ? text : 'jual ' + text; |
| 477 | .replace(/\baset\s+emas\b/ig, 'aset') |
| 478 | .replace(/\b(logam\s+mulia\|antam\|emas\|gold)\b/ig, 'aset') |
| 516 | if (choice === 'debt_in') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 517 | if (choice === 'debt_payment') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 518 | if (choice === 'piutang_help') return 'DEBT_PIUTANG_HELP_ONLY'; |
| 546 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 591 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 609 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 653 | // First implementation target: regular expense-like purchase, not debts/assets/cash movement/CC payment. |
| 654 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 673 | 'D. Credit Card\n' + |
| 683 | 'Saya belum bisa memastikan transaksi ini, jadi belum saya catat.\n\n' + |
| 719 | AIRO_CONFIG.tabs.review, |
| 728 | fallback_to_review: true, |
| 729 | status: 'review_queue_fallback_after_clarification_failed', |
| 731 | written_tab: fallbackResult.writtenTab \|\| AIRO_CONFIG.tabs.review, |
| 733 | sprint0a_guard: 'review_queue_after_clarification_failed' |
| 774 | const resolvedText = creditCardClarificationResolvedText_(pending, rawText); |
| 787 | if (resolvedText === 'CC_PAYMENT_HELP_ONLY') { |
| 849 | if (pending.type === 'asset_gold_ambiguous') { |
| 850 | const choice = normalizeAssetGoldAmbiguousClarificationAnswer_(rawText); |
| 853 | sendTelegram_(chatId, buildAssetGoldAmbiguousClarificationMessage_(pending.parsed \|\| pending \|\| {})); |
| 858 | clarification_type: 'asset_gold_ambiguous' |
| 867 | 'Saya belum mencatat transaksi Aset/Emas ini.' |
| 873 | clarification_type: 'asset_gold_ambiguous' |
| 877 | const clarifiedText = buildAssetGoldClarifiedText_(choice, pending.rawText \|\| pending.original_text \|\| pending.text \|\| ''); |
| 886 | 'Saya butuh detail orang dan format lengkap untuk Hutang.\n\n' + |
| 889 | '- bayar hutang ke Budi 50000 dari bca' |
| 893 | if (resolvedText === 'DEBT_PIUTANG_HELP_ONLY') { |
| 897 | 'Saya belum mencatat piutang/orang bayar hutang ke saya karena flow piutang belum dikunci.\n\n' + |
| 898 | 'Untuk sekarang tulis manual nanti setelah flow piutang tersedia.' |
| 911 | 'Saya belum mencatat transaksi Hutang ini.\n\n' + |
| 914 | '- bayar hutang ke Budi 50000 dari bca' |
| 955 | 'Saya belum bisa memastikan kategorinya.\n\n' + |
| 1010 | 'Saya belum bisa memastikan arah transaksinya.\n\n' + |
| 1037 | 'Saya belum bisa memastikan maksud cash-nya.\n\n' + |
| 1063 | 'Saya belum bisa memastikan akunnya.\n\n' + |
| 1068 | 'D. Credit Card\n' + |
| 1164 | if (canAskAssetGoldAmbiguousClarification_(parsed, effectiveRawText)) { |
| 1166 | type: 'asset_gold_ambiguous', |
| 1175 | sendTelegram_(chatId, buildAssetGoldAmbiguousClarificationMessage_(parsed)); |
| 1180 | clarification_type: 'asset_gold_ambiguous', |
| 1210 | if (canAskCreditCardAmbiguousClarification_(parsed, effectiveRawText)) { |
| 1221 | sendTelegram_(chatId, buildCreditCardAmbiguousClarificationMessage_(parsed)); |
| 1397 | const finalTab = parsed.needsReview ? AIRO_CONFIG.tabs.review : plannedTab; |
| 1481 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1504 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.cash, row, { createIfMissing: false }); |
| 1516 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1517 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1523 | const explicitOutflowTypes = ['expense', 'transfer_out', 'cash_out', 'cc_payment', 'debt_payment', 'asset_purchase']; |
| 1549 | source_tab: sourceTab, |
| 1550 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1555 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1581 | 'source_tab', 'linked_txn_id', 'notes' |
| 1697 | if (key.includes('credit card')) { |
| 1698 | return writeCreditCardSafely_(ss, parsed, rawText, common); |
| 1701 | if (key.includes('hutang')) { |
| 1702 | return writeHutangSafely_(ss, parsed, rawText, common); |
| 1705 | if (key.includes('aset')) { |
| 1706 | return writeAssetSafely_(ss, parsed, rawText, common); |
| 1717 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1724 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1734 | return appendByHeader_(ss, tabName, common, { createIfMissing: false }); |
| 1739 | function writeAssetSafely_(ss, parsed, rawText, common) { |
| 1740 | const tabName = AIRO_CONFIG.tabs.aset; |
| 1744 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1746 | status: 'review', |
| 1747 | fallback_reason: 'asset_tab_missing' |
| 1751 | function mirrorAssetPurchaseToAccountLedger_(result) { |
| 1755 | type: 'asset_purchase', |
| 1756 | category: parsed.category \|\| 'Aset', |
| 1761 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 1763 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1772 | if (parsed.assetSection === 'gold') { |
| 1773 | return mirrorAssetPurchaseToAccountLedger_(appendGoldAssetRow_(sheet, parsed, rawText, common)); |
| 1776 | if (parsed.assetSection === 'savings') { |
| 1777 | const result = appendToAssetSection_(sheet, 'savings', common); |
| 1778 | if (result.status === 'written') return mirrorAssetPurchaseToAccountLedger_({ ...result, writtenTab: tabName }); |
| 1781 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1783 | status: 'review', |
| 1784 | fallback_reason: 'asset_section_unclear_or_header_not_found' |
| 1787 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1789 | status: 'review', |
| 1790 | fallback_reason: 'asset_write_error: ' + String(err && err.message ? err.message : err) |
| 1799 | function appendToAssetSection_(sheet, section, data) { |
| 1800 | const spec = section === 'gold' |
| 1805 | if (!header) return { status: 'fallback', reason: 'asset_section_header_not_found' }; |
| 1818 | linked_txn_id: data.linked_txn_id, |
| 1819 | asset_section: section |
| 1922 | if (allowedLower.includes('auto_approved') && allowedLower.includes('needs_review')) { |
| 1923 | if (['review', 'pending', 'needs_review'].includes(currentLower)) { |
| 1924 | return pick('needs_review'); |
| 1929 | // Review Queue status validation |
| 1934 | // Asset savings validation |
| 1956 | const reviewTab = canonicalSheetName_(AIRO_CONFIG.tabs.review); |
| 1958 | if (canonicalTab === reviewTab) { |
| 1959 | if (!d.status \|\| d.status === 'review' \|\| d.status === 'posted') { |
| 2000 | function appendByHeader_(ss, tabName, data, options) { |
| 2108 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2169 | if (headerKey === 'source_tab' \|\| headerKey.includes('source_tab')) { |
| 2170 | return data.source_tab \|\| data.source \|\| ''; |
| 2234 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2235 | billing_cycle_id: ['billing_cycle_id', 'billing cycle id', 'cycle_id', 'billing_cycle'], |
| 2236 | creditor: ['creditor', 'kreditur', 'pemberi_hutang', 'pemberi_utang', 'lender'], |
| 2238 | fallback_reason: ['fallback_reason', 'reason', 'alasan'], |
| 2239 | asset_section: ['asset_section', 'section', 'bagian'] |
| 2257 | if (parsed.needsReview) return AIRO_CONFIG.tabs.review; |
| 2262 | isCreditCardPaymentText_(text) |
| 2264 | return AIRO_CONFIG.tabs.creditCard; |
| 2267 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text)) return AIRO_CONFIG.tabs.cicilanRumah; |
| 2270 | /\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| |
| 2274 | return AIRO_CONFIG.tabs.hutang; |
| 2277 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia\|nabung\|tabung\|saving\|savings\|aset\|investasi\|dana darurat)\b/i.test(text)) return AIRO_CONFIG.tabs.aset; |
| 2286 | function reviewIssueReasonForParsed_(rawText, data) { |
| 2303 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) { |
| 2308 | if (/\b(hutang\|utang\|pinjam\|pinjaman)\b/i.test(text) && !parseCreditor_(text)) { |
| 2312 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) && !/\b\d+(?:[.,]\d+)?\s*(jt\|juta\|rb\|ribu\|k)?\b/i.test(text)) { |
| 2313 | return 'cicilan_rumah_amount_unclear'; |
| 2325 | const gold = parseGoldAsset_(rawText); |
| 2327 | const amount = gold.isGoldAsset |
| 2328 | ? (gold.purchasePrice \|\| gold.estimatedValue \|\| 0) |
| 2332 | date: gold.purchaseDate \|\| parseDate_(text), |
| 2333 | type: gold.isGoldAsset ? 'asset' : parseType_(text), |
| 2341 | assetSection: parseAssetSection_(text), |
| 2342 | goldAction: gold.action, |
| 2343 | goldKarat: gold.karat, |
| 2344 | goldWeightGram: gold.weightGram, |
| 2345 | goldPureGram: gold.pureGram, |
| 2346 | goldPurchasePrice: gold.purchasePrice, |
| 2347 | goldPurchaseDate: gold.purchaseDate, |
| 2348 | goldNotes: gold.notes, |
| 2349 | goldEstimatedValue: gold.estimatedValue, |
| 2350 | goldMarketPrice24k: gold.marketPrice24k |
| 2353 | const issueReason = gold.isGoldAsset |
| 2354 | ? ((!gold.weightGram \|\| gold.weightGram <= 0) ? 'gold_weight_missing_or_zero' : '') |
| 2355 | : reviewIssueReasonForParsed_(rawText, parsed); |
| 2357 | parsed.issue_reason = issueReason; |
| 2358 | parsed.needsReview = Boolean(issueReason); |
| 2414 | if (typeof isCreditCardPaymentText_ === 'function' && isCreditCardPaymentText_(t)) return 'Blu'; |
| 2416 | // "cc beli ..." / "cc bayar pdam ..." means purchase using credit card. |
| 2417 | if (typeof isCreditCardPurchaseText_ === 'function' && isCreditCardPurchaseText_(t)) return 'Credit Card'; |
| 2425 | if (/\b(tokopedia\s*cc\|tokopedia\s*card\|credit\s*card\|kartu\s*kredit\|\bcc\b)\b/i.test(t)) return 'Credit Card'; |
| 2445 | if (/\b(gaji\|salary\|income\|pemasukan\|terima gaji\|gajian)\b/i.test(t)) return 'Gaji'; |
| 2446 | if (isCreditCardPaymentText_(t)) return 'CC Payment'; |
| 2447 | if (isBorrowInText_(t) \|\| isDebtPaymentText_(t)) return 'Hutang'; |
| 2452 | if (/\b(cicilan rumah\|kpr\|angsuran rumah)\b/i.test(t)) return 'Cicilan Rumah'; |
| 2453 | if (/\b(hutang\|utang)\b/i.test(t)) return 'Hutang'; |
| 2454 | if (/\b(nabung\|tabung\|saving\|aset\|investasi\|emas\|gold)\b/i.test(t)) return 'Aset'; |
| 2498 | if (isCreditCardPaymentText_(t)) return 'cc_payment'; |
| 2499 | if (isCreditCardPurchaseText_(t)) return 'cc_purchase'; |
| 2500 | if (isBorrowInText_(t)) return 'debt_in'; |
| 2501 | if (isDebtPaymentText_(t)) return 'debt_payment'; |
| 2503 | if (/\b(gaji\|salary\|income\|pemasukan\|terima gaji\|gajian\|dibayar\|refund\|reimburse\|reimbursement\|uang masuk\|dana masuk\|transfer masuk\|terima\|diterima\|dapat\|dapet)\b/i.test(t)) { |
| 2507 | if (/\b(nabung\|tabung\|saving\|investasi\|aset)\b/i.test(t)) { |
| 2531 | function parseAssetSection_(text) { |
| 2532 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text)) return 'gold'; |
| 2533 | if (/\b(nabung\|tabung\|saving\|savings\|dana darurat\|investasi\|aset)\b/i.test(text)) return 'savings'; |
| 2603 | * Process Review Queue rows that have been manually marked approved/edited. |
| 2606 | * - Edit row in 🧾 Review Queue |
| 2607 | * - Set review_status to approved or edited |
| 2608 | * - Run processReviewQueueApproved() |
| 2611 | * - Run setupReviewQueueAutoProcessor() once |
| 2615 | function processReviewQueueApproved() { |
| 2621 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.review); |
| 2624 | return { ok: false, reason: 'review_queue_sheet_missing' }; |
| 2629 | return { ok: false, reason: 'review_queue_header_missing' }; |
| 2644 | const map = reviewHeaderMap_(headers); |
| 2654 | const status = String(getReviewValue_(row, map, ['review_status', 'status']) \|\| '').toLowerCase(); |
| 2655 | const approvedTxnId = String(getReviewValue_(row, map, ['approved_transaction_id']) \|\| '').trim(); |
| 2668 | const rawText = String(getReviewValue_(row, map, ['raw_text', 'message', 'telegram_text']) \|\| '').trim(); |
| 2669 | const parsedAmount = getReviewValue_(row, map, ['parsed_amount', 'amount', 'nominal']); |
| 2670 | const amount = normalizeReviewAmount_(parsedAmount); |
| 2672 | const parsedAccount = String(getReviewValue_(row, map, ['parsed_account', 'account', 'akun']) \|\| '').trim(); |
| 2673 | const parsedCategory = String(getReviewValue_(row, map, ['parsed_category', 'category', 'kategori']) \|\| '').trim(); |
| 2674 | const parsedSubcategory = String(getReviewValue_(row, map, ['parsed_subcategory', 'subcategory']) \|\| '').trim(); |
| 2675 | const parsedType = String(getReviewValue_(row, map, ['parsed_type', 'type', 'jenis']) \|\| '').trim(); |
| 2678 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_amount_missing'); |
| 2684 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_account_missing'); |
| 2694 | description: rawText \|\| String(getReviewValue_(row, map, ['suggested_fix']) \|\| ''), |
| 2696 | account: normalizeReviewAccount_(parsedAccount), |
| 2700 | assetSection: parseAssetSection_(rawText \|\| ''), |
| 2701 | needsReview: false |
| 2704 | const plannedTab = routeReviewApprovedTab_(parsed, rawText); |
| 2705 | const queueId = String(getReviewValue_(row, map, ['queue_id']) \|\| ('row_' + sheetRow)); |
| 2706 | const stagingResult = { rowId: 'review:' + queueId }; |
| 2711 | setReviewValue_(sheet, sheetRow, map, ['approved_transaction_id'], result.rowId \|\| (result.writtenTab + ':' + result.row)); |
| 2712 | setReviewValue_(sheet, sheetRow, map, ['reviewed_at'], new Date()); |
| 2713 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'processed_to_' + result.writtenTab); |
| 2716 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_failed_' + (result.reason \|\| 'unknown')); |
| 2720 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_error_' + String(err && err.message ? err.message : err)); |
| 2736 | function processReviewQueueApprovedOnEdit(e) { |
| 2737 | processReviewQueueApproved(); |
| 2740 | function setupReviewQueueAutoProcessor() { |
| 2744 | if (t.getHandlerFunction && t.getHandlerFunction() === 'processReviewQueueApprovedOnEdit') { |
| 2750 | .newTrigger('processReviewQueueApprovedOnEdit') |
| 2757 | trigger: 'processReviewQueueApprovedOnEdit' |
| 2761 | function routeReviewApprovedTab_(parsed, rawText) { |
| 2765 | return AIRO_CONFIG.tabs.creditCard; |
| 2768 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) \|\| parsed.category === 'Cicilan Rumah') { |
| 2769 | return AIRO_CONFIG.tabs.cicilanRumah; |
| 2772 | if (/\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| parsed.category === 'Hutang') { |
| 2773 | return AIRO_CONFIG.tabs.hutang; |
| 2776 | if (/\b(nabung\|tabung\|saving\|savings\|aset\|investasi\|emas\|gold\|dana darurat)\b/i.test(text) \|\| parsed.category === 'Aset') { |
| 2777 | return AIRO_CONFIG.tabs.aset; |
| 2787 | function reviewHeaderMap_(headers) { |
| 2798 | function getReviewValue_(row, map, keys) { |

## 6. Initial Gap Matrix

| Domain | Audit Question | Current Status | Runtime Patch Now? |
|---|---|---:|---:|
| Credit Card | Are purchase, payment, status_pocket_blu, and billing cycle flows mature and tested? | Pending exact audit | No |
| Hutang | Are debt increase, debt payment, master balance, payment log, and Account Ledger mirror consistent? | Pending exact audit | No |
| Aset | Are savings/gold flows, asset_section, gold_event_id, and Account Ledger mirror consistent? | Pending exact audit | No |
| Cicilan Rumah | Are payment history, remaining balance, and audit helpers stable? | Pending exact audit | No |
| Review Queue | Are fallback reasons, issue reasons, and unresolved ambiguity rows consistent? | Pending exact audit | No |

## 7. Proposed Patch Order

Start with the smallest low-risk domain maturity gap after exact audit.

Recommended order:

1. Review Queue reason/status consistency audit.
2. Credit Card status_pocket_blu and billing cycle guard audit.
3. Hutang master/payment consistency audit.
4. Aset savings/gold consistency audit.
5. Cicilan Rumah payment history audit.

Do not start with dashboard migration or Cash Ledger deletion.

## 8. Next Micro-Step

Run exact domain-surface audit for Review Queue and Credit Card first.

The next command should produce:

- exact function map
- current test map
- missing regression list
- smallest patch recommendation
- no runtime changes
