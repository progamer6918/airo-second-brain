# AIRO Finance - Sprint 2 Review Queue and Credit Card Surface Audit

Status: EXACT AUDIT
Sprint: Sprint 2 - Domain Tab Maturation
Generated at: 2026-05-24 13:29:09
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document performs the first exact Sprint 2 domain-surface audit.

Domains audited:

- Review Queue
- Credit Card

No runtime patch is made in this micro-step.

## 2. Function Surface Map

| Domain | Function | Lines | Status | Signals |
|---|---|---:|---:|---|
| Review Queue | `appendByHeader_` | 2000-2047 | FOUND | appendByHeader_:1, status:4 |
| Review Queue | `reviewIssueReasonForParsed_` | 2286-2321 | FOUND | review:1 |
| Review Queue | `reviewHeaderMap_` | 2787-2796 | FOUND | review:1 |
| Review Queue | `processReviewQueueApprovedRows_` | MISSING | MISSING |  |
| Review Queue | `getReviewValue_` | 2798-2807 | FOUND |  |
| Review Queue | `setReviewValue_` | 2809-2819 | FOUND |  |
| Review Queue | `inferTabFromRawText_` | MISSING | MISSING |  |
| Review Queue | `inferTargetTabForReviewRow_` | MISSING | MISSING |  |
| Review Queue | `routeParsedToTab_` | MISSING | MISSING |  |
| Credit Card | `isCreditCardPaymentText_` | 5795-5802 | FOUND |  |
| Credit Card | `normalizeCreditCardClarificationAnswer_` | 304-313 | FOUND | cc_payment:1 |
| Credit Card | `creditCardClarificationResolvedText_` | 346-367 | FOUND | cc_payment:1 |
| Credit Card | `appendCreditCardPurchase_` | 6149-6195 | FOUND | appendByHeader_:1, status:3, issue_reason:1, review:1, linked_txn_id:3, status_pocket_blu:1, billing_cycle_id:1, billing_start:1, billing_end:1, transferred_at:1 |
| Credit Card | `markCreditCardPocketBluTransfer_` | 6199-6301 | FOUND | appendByHeader_:3, status:10, issue_reason:3, review:3, writeAccountLedgerMirror_:1, linked_txn_id:2, status_pocket_blu:1, transferred_at:1, cc_payment:3, account_ledger_result:1 |
| Credit Card | `findCcHeaderRow_` | 6119-6139 | FOUND | status:1, status_pocket_blu:1 |
| Credit Card | `ccColMap_` | 6141-6147 | FOUND |  |
| Credit Card | `parseCcItemKeyword_` | 6098-6117 | FOUND | cc_payment:1 |
| Credit Card | `ensureCreditCardBillingCyclePanel_` | MISSING | MISSING |  |
| Credit Card | `refreshCreditCardBillingCycleSummary_` | MISSING | MISSING |  |
| Credit Card | `auditCreditCardCycleRuntime_` | MISSING | MISSING |  |

## 3. Existing Test Candidates

- tests/personal-workflow/test_airo_account_aliases.py
- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_credit_card_billing_cycle.py
- tests/personal-workflow/test_airo_credit_card_mirror_planner.py
- tests/personal-workflow/test_airo_finance_sheet_v12_mapper_preview.py
- tests/personal-workflow/test_airo_review_queue_planner.py

## 4. Review Queue Risk Notes

- Review Queue approved-row processor function not found by expected name
- Review Queue status handling needs exact regression

## 5. Credit Card Risk Notes

- No immediate Credit Card surface gap detected by heuristic scan.

## 6. Recommended Next Patch

Start with Review Queue status/reason contract if no exact regression exists; otherwise patch Credit Card billing/status guard.

Patch boundary:

- Add focused regression first.
- Patch one small surface only.
- Do not change Account Ledger source-of-truth behavior from Sprint 1.
- Do not start dashboard finalization.
- Do not touch Cash Ledger deletion.
- Do not start Sprint 3 work.

## 7. Direct Source Findings

| Line | Source Text |
|---:|---|
| 16 | creditCard: '💳 Credit Card', |
| 21 | review: '🧾 Review Queue' |
| 64 | if (/^(d\|4)$/i.test(t) \|\| /\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t)) return 'Credit Card'; |
| 80 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 111 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 123 | '- 15000 credit card' |
| 205 | const hasClearAction = /\b(beli\|bayar\|makan\|minum\|kopi\|jajan\|transfer\|tf\|dari\|ke\|masuk\|keluar\|gaji\|refund\|terima\|diterima\|topup\|tarik\|cc\|credit card\|cash\|tunai)\b/i.test(text); |
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
| 546 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 591 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 609 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 654 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 673 | 'D. Credit Card\n' + |
| 729 | status: 'review_queue_fallback_after_clarification_failed', |
| 733 | sprint0a_guard: 'review_queue_after_clarification_failed' |
| 774 | const resolvedText = creditCardClarificationResolvedText_(pending, rawText); |
| 787 | if (resolvedText === 'CC_PAYMENT_HELP_ONLY') { |
| 1068 | 'D. Credit Card\n' + |
| 1210 | if (canAskCreditCardAmbiguousClarification_(parsed, effectiveRawText)) { |
| 1221 | sendTelegram_(chatId, buildCreditCardAmbiguousClarificationMessage_(parsed)); |
| 1397 | const finalTab = parsed.needsReview ? AIRO_CONFIG.tabs.review : plannedTab; |
| 1504 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.cash, row, { createIfMissing: false }); |
| 1523 | const explicitOutflowTypes = ['expense', 'transfer_out', 'cash_out', 'cc_payment', 'debt_payment', 'asset_purchase']; |
| 1555 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1697 | if (key.includes('credit card')) { |
| 1698 | return writeCreditCardSafely_(ss, parsed, rawText, common); |
| 1734 | return appendByHeader_(ss, tabName, common, { createIfMissing: false }); |
| 1744 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1747 | fallback_reason: 'asset_tab_missing' |
| 1767 | account_ledger_result: accountLedgerResult \|\| null |
| 1781 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1784 | fallback_reason: 'asset_section_unclear_or_header_not_found' |
| 1787 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1790 | fallback_reason: 'asset_write_error: ' + String(err && err.message ? err.message : err) |
| 1929 | // Review Queue status validation |
| 2000 | function appendByHeader_(ss, tabName, data, options) { |
| 2235 | billing_cycle_id: ['billing_cycle_id', 'billing cycle id', 'cycle_id', 'billing_cycle'], |
| 2238 | fallback_reason: ['fallback_reason', 'reason', 'alasan'], |
| 2257 | if (parsed.needsReview) return AIRO_CONFIG.tabs.review; |
| 2262 | isCreditCardPaymentText_(text) |
| 2264 | return AIRO_CONFIG.tabs.creditCard; |
| 2286 | function reviewIssueReasonForParsed_(rawText, data) { |
| 2355 | : reviewIssueReasonForParsed_(rawText, parsed); |
| 2357 | parsed.issue_reason = issueReason; |
| 2358 | parsed.needsReview = Boolean(issueReason); |
| 2414 | if (typeof isCreditCardPaymentText_ === 'function' && isCreditCardPaymentText_(t)) return 'Blu'; |
| 2416 | // "cc beli ..." / "cc bayar pdam ..." means purchase using credit card. |
| 2417 | if (typeof isCreditCardPurchaseText_ === 'function' && isCreditCardPurchaseText_(t)) return 'Credit Card'; |
| 2425 | if (/\b(tokopedia\s*cc\|tokopedia\s*card\|credit\s*card\|kartu\s*kredit\|\bcc\b)\b/i.test(t)) return 'Credit Card'; |
| 2446 | if (isCreditCardPaymentText_(t)) return 'CC Payment'; |
| 2498 | if (isCreditCardPaymentText_(t)) return 'cc_payment'; |
| 2499 | if (isCreditCardPurchaseText_(t)) return 'cc_purchase'; |
| 2603 | * Process Review Queue rows that have been manually marked approved/edited. |
| 2606 | * - Edit row in 🧾 Review Queue |
| 2607 | * - Set review_status to approved or edited |
| 2608 | * - Run processReviewQueueApproved() |
| 2615 | function processReviewQueueApproved() { |
| 2624 | return { ok: false, reason: 'review_queue_sheet_missing' }; |
| 2629 | return { ok: false, reason: 'review_queue_header_missing' }; |
| 2644 | const map = reviewHeaderMap_(headers); |
| 2654 | const status = String(getReviewValue_(row, map, ['review_status', 'status']) \|\| '').toLowerCase(); |
| 2678 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_amount_missing'); |
| 2684 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_account_missing'); |
| 2701 | needsReview: false |
| 2713 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'processed_to_' + result.writtenTab); |
| 2716 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_failed_' + (result.reason \|\| 'unknown')); |
| 2720 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_error_' + String(err && err.message ? err.message : err)); |
| 2736 | function processReviewQueueApprovedOnEdit(e) { |
| 2737 | processReviewQueueApproved(); |
| 2744 | if (t.getHandlerFunction && t.getHandlerFunction() === 'processReviewQueueApprovedOnEdit') { |
| 2750 | .newTrigger('processReviewQueueApprovedOnEdit') |
| 2757 | trigger: 'processReviewQueueApprovedOnEdit' |
| 2765 | return AIRO_CONFIG.tabs.creditCard; |
| 2787 | function reviewHeaderMap_(headers) { |
| 3881 | function setupCreditCardTabCycleHeader_() { |
| 3884 | getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard) \|\| |
| 3885 | getSheetLoose_(ss, 'Credit Card'); |
| 3900 | const required = ['amount', 'status_pocket_blu', 'billing_cycle_id']; |
| 3944 | const status = String(row[map.status_pocket_blu - 1] \|\| '').toLowerCase(); |
| 3945 | const cycleId = String(row[map.billing_cycle_id - 1] \|\| '').trim(); |
| 4057 | if (refreshedLastRow > header.row && refreshedMap.billing_cycle_id) { |
| 4062 | const cycleId = String(row[refreshedMap.billing_cycle_id - 1] \|\| '').trim(); |
| 4094 | function setupDashboardCreditCardCyclePanel() { |
| 4102 | getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard) \|\| |
| 4103 | getSheetLoose_(ss, 'Credit Card'); |
| 4112 | const required = ['amount', 'status_pocket_blu', 'billing_cycle_id', 'billing_start', 'billing_end']; |
| 4156 | const status = String(row[map.status_pocket_blu - 1] \|\| '').toLowerCase(); |
| 4157 | const cycleId = String(row[map.billing_cycle_id - 1] \|\| '').trim(); |
| 4186 | dashboard.getRange('B25').setValue('💳 CREDIT CARD — TOKOPEDIA CC'); |
| 4454 | 'Credit Card', |
| 4458 | 'Review Queue', |
| 4507 | const result = fixCreditCardDateMerchantFromRawText(); |
| 4509 | const cc = getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard); |
| 4514 | '✅ Tanggal dan merchant Credit Card dirapikan.\n\n' + |
| 4532 | const result = moveCreditCardStatusAfterAmount(); |
| 4534 | const cc = getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard); |
| 4539 | '✅ Kolom Credit Card dirapikan.\n\n' + |
| 4540 | 'status_pocket_blu sekarang berada setelah amount dan sebelum description.\n\n' + |
| 4794 | const result = setupCreditCardTabCycleHeader_(); |
| 4799 | 'Credit Card tab cycle header direfresh.\n\n' + |
| 4805 | (link ? 'Buka Credit Card: ' + link : '') |
| 4817 | const result = setupDashboardCreditCardCyclePanel(); |
| 4822 | 'Credit Card Dashboard cycle panel direfresh.\n\n' + |
| 4843 | const cc = getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard); |
| 4846 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: tab Credit Card tidak ditemukan.'); |
| 4857 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: header Credit Card tidak ditemukan.'); |
| 4899 | const cycle = cell_(row, map.billing_cycle_id); |
| 4910 | status: cell_(row, map.status_pocket_blu), |
| 4939 | 'Credit Card cycle audit selesai.\n\n' + |
| 4960 | 'Credit Card cycle audit error.\n\n' + |
| 5795 | function isCreditCardPaymentText_(text) { |
| 5800 | /^bayar\s+tagihan\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t) |
| 5897 | function isCreditCardPurchaseText_(text) { |
| 5900 | if (isCreditCardPaymentText_(t)) return false; |
| 5901 | if (isCreditCardRefundText_(t)) return false; |
| 5910 | function isCreditCardRefundText_(text) { |
| 5911 | return /\b(refund\|pengembalian\|dikembalikan\|retur)\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i |
| 5915 | function writeCreditCardSafely_(ss, parsed, rawText, common) { |
| 5916 | const tabName = AIRO_CONFIG.tabs.creditCard; |
| 5920 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5923 | issue_reason: 'credit_card_tab_missing' |
| 5930 | if (isCreditCardRefundText_(text)) { |
| 5931 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5935 | issue_reason: 'cc_refund_needs_manual_review' |
| 5939 | if (isCreditCardPaymentText_(text)) { |
| 5940 | return markCreditCardPocketBluTransfer_(ss, sheet, parsed, rawText, common); |
| 5943 | return appendCreditCardPurchase_(ss, sheet, parsed, rawText, common); |
| 5951 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5954 | issue_reason: 'hutang_tab_missing' |
| 5962 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5966 | issue_reason: 'orang_bayar_hutang_ke_saya_needs_piutang_flow' |
| 5978 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5981 | issue_reason: 'hutang_intent_unclear' |
| 6116 | return t \|\| 'cc_payment'; |
| 6129 | normalized.includes('status_pocket_blu') |
| 6149 | function appendCreditCardPurchase_(ss, sheet, parsed, rawText, common) { |
| 6153 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6156 | issue_reason: 'cc_header_not_found' |
| 6170 | status_pocket_blu: '⏳ Belum', |
| 6172 | transferred_at: '', |
| 6175 | billing_cycle_id: cycle.id, |
| 6199 | function markCreditCardPocketBluTransfer_(ss, sheet, parsed, rawText, common) { |
| 6203 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6206 | issue_reason: 'cc_header_not_found' |
| 6212 | const statusCol = map.status_pocket_blu; |
| 6213 | const transferredCol = map.transferred_at; |
| 6221 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6224 | issue_reason: 'cc_payment_amount_or_columns_missing' |
| 6258 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6262 | issue_reason: 'cc_payment_no_matching_pending_purchase' |
| 6267 | type: 'cc_payment', |
| 6268 | category: parsed.category \|\| 'Credit Card Payment', |
| 6275 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.creditCard); |
| 6298 | account_ledger_result: accountLedgerResult \|\| null, |
| 6411 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6414 | issue_reason: 'hutang_header_missing' |
| 6422 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6425 | issue_reason: 'hutang_payment_person_or_amount_missing' |
| 6432 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6435 | issue_reason: 'hutang_person_not_found_in_master' |
| 6488 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6491 | issue_reason: 'hutang_header_missing' |
| 6499 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6502 | issue_reason: 'hutang_increase_person_or_amount_missing' |
| 6509 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6512 | issue_reason: 'hutang_person_not_found_in_master' |
| 6560 | function fixCreditCardStatusDropdownValues() { |
| 6562 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard); |
| 6574 | const statusCol = map.status_pocket_blu; |
| 6577 | return { ok: false, reason: 'status_pocket_blu_col_missing' }; |
| 6637 | function moveCreditCardStatusAfterAmount() { |
| 6639 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard); |
| 6652 | const statusCol = map.status_pocket_blu; |
| 6668 | fixCreditCardStatusDropdownValues(); |
| 6679 | // amount \| description \| status_pocket_blu |
| 6681 | // amount \| status_pocket_blu \| description |
| 6712 | sheet.getRange(startRow, targetStatusCol).setValue('status_pocket_blu'); |
| 6716 | fixCreditCardStatusDropdownValues(); |
| 6721 | moved: 'status_pocket_blu after amount', |
| 6790 | function fixCreditCardDateMerchantFromRawText() { |
| 6792 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.creditCard); |
| 6808 | const cycleCol = map.billing_cycle_id; |
| 7083 | var result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |

## 8. Next Micro-Step

Recommended next command:

- add Review Queue status/reason contract regression if missing
- or add Credit Card billing/status contract regression if Review Queue is already locked
- run Sprint 1 focused regressions as safety baseline
- run domain tests
- commit the smallest test-only patch first
