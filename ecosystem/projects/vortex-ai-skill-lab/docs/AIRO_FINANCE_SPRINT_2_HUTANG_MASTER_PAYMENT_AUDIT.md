# AIRO Finance - Sprint 2 Hutang Master / Payment Consistency Audit

Status: EXACT AUDIT
Sprint: Sprint 2 - Domain Tab Maturation
Generated at: 2026-05-24 14:21:41
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document audits Hutang domain-tab maturity after Review Queue and Credit Card contracts are locked.

Scope:

- Hutang master rows
- Hutang payment history rows
- debt increase flow
- debt payment flow
- linked transaction ID consistency
- Account Ledger outflow compatibility from Sprint 1

No runtime patch is made in this micro-step.

## 2. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `writeHutangSafely_` | 5946-5983 | FOUND | appendByHeader_:3, person:1, payment:1, issue_reason:3, AIRO_CONFIG.tabs.hutang:1, AIRO_CONFIG.tabs.review:3 |
| `appendDebtPaymentAndUpdateMaster_` | 6406-6481 | FOUND | appendByHeader_:3, writeAccountLedgerMirror_:1, debt_payment:1, linked_txn_id:3, person:6, payment:5, issue_reason:3, AIRO_CONFIG.tabs.hutang:1, AIRO_CONFIG.tabs.review:3 |
| `appendDebtIncreaseAndUpdateMaster_` | 6483-6544 | FOUND | appendByHeader_:3, debt_in:1, linked_txn_id:1, person:6, paid:2, payment:3, issue_reason:3, AIRO_CONFIG.tabs.review:3 |
| `appendDebtPaymentLog_` | 6546-6558 | FOUND | payment:5 |
| `findHutangMasterHeader_` | 6303-6324 | FOUND |  |
| `findHutangPaymentHeader_` | 6326-6347 | FOUND |  |
| `parseDebtPerson_` | 6368-6378 | FOUND |  |
| `parseCreditor_` | 2520-2523 | FOUND |  |
| `isDebtPaymentText_` | 5815-5819 | FOUND |  |
| `isBorrowInText_` | 5806-5813 | FOUND |  |
| `normalizeDebtAmbiguousClarificationAnswer_` | 382-391 | FOUND | debt_payment:1, debt_in:1, payment:1 |
| `canAskDebtAmbiguousClarification_` | 393-403 | FOUND |  |
| `buildDebtAmbiguousClarificationMessage_` | 405-417 | FOUND |  |
| `debtAmbiguousClarificationResolvedText_` | 507-521 | FOUND | debt_payment:1, debt_in:1, payment:1 |

## 3. Existing Test Candidates

- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_hutang_planner.py
- tests/personal-workflow/test_airo_review_queue_planner.py
- tests/personal-workflow/test_airo_review_queue_status_reason_contract.py

## 4. Risk Notes

- Hutang top-level writer delegates payment; Account Ledger mirror must be verified through delegated function.
- Debt payment remaining-balance signal not obvious by text scan; exact regression recommended.
- Debt payment log may not preserve linked_txn_id; exact regression recommended.

## 5. Hutang Maturity Questions

| Area | Question | Runtime Patch Now? |
|---|---|---:|
| Debt increase | Does new debt update master consistently and avoid false wallet outflow? | No |
| Debt payment | Does payment update master, append payment log, and mirror Account Ledger outflow? | No |
| Linked ID | Do master/payment/Account Ledger rows preserve linked transaction ID lineage? | No |
| Person/Creditor | Is creditor/person parsing stable for Telegram natural text? | No |
| Review fallback | Does unclear Hutang route to Review Queue instead of unsafe write? | No |

## 6. Recommended Next Patch

Add a focused Hutang master/payment contract regression first.

The regression should lock:

- debt payment uses `appendDebtPaymentAndUpdateMaster_`
- debt payment writes payment history
- debt payment mirrors Account Ledger outflow through `writeAccountLedgerMirror_`
- debt payment preserves `linked_txn_id`
- debt increase remains separate from debt payment
- unclear Hutang/person falls back safely instead of corrupting master/payment rows

Patch boundary:

- test-only first
- no dashboard changes
- no Cash Ledger deletion
- no Finance Events implementation
- no Email Ingestion implementation
- no broad refactor

## 7. Direct Source Findings

| Line | Source Text |
|---:|---|
| 18 | hutang: '🤝 Hutang', |
| 80 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 111 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 134 | if (/^(d\|4)$/i.test(t) \|\| /\b(sisa\|remaining\|saldo akhir\|akhir)\b/i.test(t)) return 'cash_remaining'; |
| 177 | if (direction === 'cash_remaining') return ('sisa cash ' + amount + ' saldo akhir ' + tail).trim(); |
| 189 | if (/^(d\|4)$/i.test(t) \|\| /\b(saldo\|balance\|tercatat\|awal\|akhir)\b/i.test(t)) return 'balance'; |
| 385 | if (/^(a\|1)$/i.test(t) \|\| /\b(pinjam\|pinjaman\|saya pinjam\|tambah hutang\|tambah utang)\b/i.test(t)) return 'debt_in'; |
| 386 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment'; |
| 387 | if (/^(c\|3)$/i.test(t) \|\| /\b(piutang\|orang bayar\|ke saya)\b/i.test(t)) return 'piutang_help'; |
| 398 | if (!/\b(hutang\|utang\|pinjaman\|pinjam)\b/i.test(text)) return false; |
| 400 | if ((isBorrowInText_(text) \|\| isDebtPaymentText_(text)) && parseDebtPerson_(rawText)) return false; |
| 407 | 'Saya tangkap ada transaksi Hutang Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 409 | 'A. Saya pinjam / tambah hutang\n' + |
| 410 | 'B. Saya bayar hutang\n' + |
| 411 | 'C. Orang bayar hutang ke saya / piutang\n' + |
| 415 | '- bayar hutang ke Budi 50000 dari bca' |
| 512 | if ((isBorrowInText_(lower) \|\| isDebtPaymentText_(lower)) && parseDebtPerson_(text)) { |
| 516 | if (choice === 'debt_in') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 517 | if (choice === 'debt_payment') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 518 | if (choice === 'piutang_help') return 'DEBT_PIUTANG_HELP_ONLY'; |
| 546 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 591 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 609 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 654 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 886 | 'Saya butuh detail orang dan format lengkap untuk Hutang.\n\n' + |
| 889 | '- bayar hutang ke Budi 50000 dari bca' |
| 893 | if (resolvedText === 'DEBT_PIUTANG_HELP_ONLY') { |
| 897 | 'Saya belum mencatat piutang/orang bayar hutang ke saya karena flow piutang belum dikunci.\n\n' + |
| 898 | 'Untuk sekarang tulis manual nanti setelah flow piutang tersedia.' |
| 911 | 'Saya belum mencatat transaksi Hutang ini.\n\n' + |
| 914 | '- bayar hutang ke Budi 50000 dari bca' |
| 1481 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1491 | amount_remaining: cashInflow ? parsed.amount : '', |
| 1514 | * Balance is intentionally left blank for Google Sheet formulas. |
| 1516 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1517 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1523 | const explicitOutflowTypes = ['expense', 'transfer_out', 'cash_out', 'cc_payment', 'debt_payment', 'asset_purchase']; |
| 1544 | balance: '', |
| 1550 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1580 | 'balance', 'type', 'category', 'description', 'raw_text', |
| 1581 | 'source_tab', 'linked_txn_id', 'notes' |
| 1701 | if (key.includes('hutang')) { |
| 1702 | return writeHutangSafely_(ss, parsed, rawText, common); |
| 1717 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1724 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1747 | fallback_reason: 'asset_tab_missing' |
| 1761 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 1763 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1767 | account_ledger_result: accountLedgerResult \|\| null |
| 1784 | fallback_reason: 'asset_section_unclear_or_header_not_found' |
| 1790 | fallback_reason: 'asset_write_error: ' + String(err && err.message ? err.message : err) |
| 1818 | linked_txn_id: data.linked_txn_id, |
| 2108 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2123 | if (headerKey === 'amount_remaining' \|\| headerKey.includes('amount_remaining')) { |
| 2124 | return data.amount_remaining ?? ''; |
| 2234 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2236 | creditor: ['creditor', 'kreditur', 'pemberi_hutang', 'pemberi_utang', 'lender'], |
| 2238 | fallback_reason: ['fallback_reason', 'reason', 'alasan'], |
| 2270 | /\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| |
| 2271 | isBorrowInText_(text) \|\| |
| 2272 | isDebtPaymentText_(text) |
| 2274 | return AIRO_CONFIG.tabs.hutang; |
| 2303 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) { |
| 2308 | if (/\b(hutang\|utang\|pinjam\|pinjaman)\b/i.test(text) && !parseCreditor_(text)) { |
| 2338 | creditor: parseCreditor_(text), |
| 2357 | parsed.issue_reason = issueReason; |
| 2447 | if (isBorrowInText_(t) \|\| isDebtPaymentText_(t)) return 'Hutang'; |
| 2453 | if (/\b(hutang\|utang)\b/i.test(t)) return 'Hutang'; |
| 2500 | if (isBorrowInText_(t)) return 'debt_in'; |
| 2501 | if (isDebtPaymentText_(t)) return 'debt_payment'; |
| 2520 | function parseCreditor_(text) { |
| 2678 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_amount_missing'); |
| 2684 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_account_missing'); |
| 2697 | creditor: parseCreditor_(rawText \|\| ''), |
| 2713 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'processed_to_' + result.writtenTab); |
| 2716 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_failed_' + (result.reason \|\| 'unknown')); |
| 2720 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_error_' + String(err && err.message ? err.message : err)); |
| 2772 | if (/\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| parsed.category === 'Hutang') { |
| 2773 | return AIRO_CONFIG.tabs.hutang; |
| 2875 | const amountRemaining = Number(row[4] \|\| 0); |
| 2876 | const amount = amountIn \|\| amountOut \|\| amountStart \|\| amountRemaining \|\| 0; |
| 2884 | sheet.getRange(r, 5).setValue(amount);          // amount_remaining |
| 3381 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 3951 | status.indexOf('paid') >= 0 \|\| |
| 3993 | cc.getRange('A3').setValue('Tagihan jatuh tempo tetap tampil sampai dana pembayaran disiapkan di Pocket Blu khusus CC / paid / closed.'); |
| 4163 | status.indexOf('paid') >= 0 \|\| |
| 4280 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4456 | 'Hutang', |
| 4629 | date: findCol_(['date', 'tanggal', 'payment_date', 'tanggal_bayar', 'date_paid', 'paid_date']), |
| 4630 | amount: findCol_(['amount', 'nominal', 'jumlah', 'payment_amount', 'amount_paid', 'paid_amount', 'angsuran']), |
| 4632 | remaining: findCol_(['remaining_after_payment', 'remaining', 'sisa_cicilan', 'sisa']), |
| 4656 | remaining: col.remaining ? row[col.remaining - 1] : '', |
| 4677 | ' \| remaining=' + formatText_(item.remaining) + |
| 4694 | 'payment_id=' + col.payment_id + ', date=' + col.date + ', amount=' + col.amount + ', cicilan_ke=' + col.cicilan_ke + ', remaining=' + col.remaining + ', notes=' + col.notes + '\n\n' + |
| 5289 | if (/^admin\s+(audit\|check\|cek)\s+cash\s+(parity\|balance\|total\|ledger)/i.test(text)) { |
| 5806 | function isBorrowInText_(text) { |
| 5810 | /\b(pinjam\|dipinjamkan\|minjem\|hutang ke saya\|utang ke saya\|dipinjami)\b/i.test(t) \|\| |
| 5811 | /\b(dapat\|terima)\s+(pinjaman\|hutang\|utang)\b/i.test(t) |
| 5812 | ) && !isDebtPaymentText_(t); |
| 5815 | function isDebtPaymentText_(text) { |
| 5818 | return /\b(bayar\|lunasi\|nyicil\|cicil)\b.*\b(hutang\|utang\|pinjaman)\b/i.test(t); |
| 5828 | // This prevents category/type like Gaji, CC Payment, debt_in from being blanked. |
| 5923 | issue_reason: 'credit_card_tab_missing' |
| 5935 | issue_reason: 'cc_refund_needs_manual_review' |
| 5946 | function writeHutangSafely_(ss, parsed, rawText, common) { |
| 5947 | const tabName = AIRO_CONFIG.tabs.hutang; |
| 5954 | issue_reason: 'hutang_tab_missing' |
| 5960 | // "mamak bayar hutang ke saya" is receivable/piutang, not current personal debt payment. |
| 5961 | if (/\bbayar\b.*\b(hutang\|utang)\b.*\bke saya\b/i.test(text)) { |
| 5964 | category: 'Piutang', |
| 5966 | issue_reason: 'orang_bayar_hutang_ke_saya_needs_piutang_flow' |
| 5970 | if (isDebtPaymentText_(text)) { |
| 5971 | return appendDebtPaymentAndUpdateMaster_(ss, sheet, parsed, rawText, common); |
| 5974 | if (isBorrowInText_(text)) { |
| 5975 | return appendDebtIncreaseAndUpdateMaster_(ss, sheet, parsed, rawText, common); |
| 5981 | issue_reason: 'hutang_intent_unclear' |
| 6156 | issue_reason: 'cc_header_not_found' |
| 6166 | cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6173 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6206 | issue_reason: 'cc_header_not_found' |
| 6224 | issue_reason: 'cc_payment_amount_or_columns_missing' |
| 6243 | rowStatus === 'paid' \|\| |
| 6262 | issue_reason: 'cc_payment_no_matching_pending_purchase' |
| 6273 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 6275 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.creditCard); |
| 6298 | account_ledger_result: accountLedgerResult \|\| null, |
| 6303 | function findHutangMasterHeader_(sheet) { |
| 6311 | normalized.includes('hutang_id') && |
| 6326 | function findHutangPaymentHeader_(sheet) { |
| 6335 | normalized.includes('hutang_id') && |
| 6349 | function hutangColMap_(headers) { |
| 6368 | function parseDebtPerson_(rawText) { |
| 6371 | let m = text.match(/\bbayar\s+(?:hutang\|utang)\s+ke\s+(.+?)\s+\d/i); |
| 6381 | const map = hutangColMap_(masterHeader.headers); |
| 6406 | function appendDebtPaymentAndUpdateMaster_(ss, sheet, parsed, rawText, common) { |
| 6407 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6408 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6414 | issue_reason: 'hutang_header_missing' |
| 6418 | const person = parseDebtPerson_(rawText); |
| 6425 | issue_reason: 'hutang_payment_person_or_amount_missing' |
| 6435 | issue_reason: 'hutang_person_not_found_in_master' |
| 6440 | const hutangId = map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : ''; |
| 6443 | const oldPaid = map.total_dibayar ? Number(sheet.getRange(master.row, map.total_dibayar).getValue() \|\| 0) : 0; |
| 6444 | const newPaid = oldPaid + amount; |
| 6445 | const sisa = Math.max(0, pokok - newPaid); |
| 6447 | if (map.total_dibayar) sheet.getRange(master.row, map.total_dibayar).setValue(newPaid); |
| 6448 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6451 | appendDebtPaymentLog_(sheet, paymentHeader, { |
| 6452 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6453 | hutang_id: hutangId, |
| 6463 | type: 'debt_payment', |
| 6464 | category: parsed.category \|\| 'Hutang', |
| 6469 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 6471 | writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.hutang); |
| 6483 | function appendDebtIncreaseAndUpdateMaster_(ss, sheet, parsed, rawText, common) { |
| 6484 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6485 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6491 | issue_reason: 'hutang_header_missing' |
| 6495 | const person = parseDebtPerson_(rawText); |
| 6502 | issue_reason: 'hutang_increase_person_or_amount_missing' |
| 6512 | issue_reason: 'hutang_person_not_found_in_master' |
| 6518 | const paid = map.total_dibayar ? Number(sheet.getRange(master.row, map.total_dibayar).getValue() \|\| 0) : 0; |
| 6520 | const sisa = Math.max(0, newPokok - paid); |
| 6523 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6526 | appendDebtPaymentLog_(sheet, paymentHeader, { |
| 6527 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6528 | hutang_id: map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : '', |
| 6534 | notes: 'debt_increase: ' + stripQaTag_(rawText) |
| 6546 | function appendDebtPaymentLog_(sheet, paymentHeader, data) { |
| 6547 | const map = hutangColMap_(paymentHeader.headers); |
| 6598 | low === 'paid' \|\| |
| 6609 | low === 'unpaid' \|\| |
| 6618 | low === 'partially_paid' \|\| |
| 6862 | * and key properties, and populates balance formulas dynamically without overwriting existing data. |
| 6954 | var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders); |
| 7004 | var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders); |
| 7016 | var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders); |
| 7073 | balance: '', |
| 7079 | linked_txn_id: getFieldValue_(cashRow, 'linked_txn_id', cashHeaders) \|\| '', |
| 7086 | // Set formula balance |
| 7380 | // Repair missing source_tab values for remaining rows |
| 7449 | var sharedTxnId = (common && (common.linked_txn_id \|\| common.rowId)) \|\| makeTxnId_({}, rawText); |
| 7461 | linked_txn_id: sharedTxnId + ':in' |
| 7463 | var outResult = writeAccountLedgerMirror_(ss, parsedOut, rawText, commonOut, transfer.sourceAccount); |
| 7475 | linked_txn_id: sharedTxnId + ':out' |
| 7477 | var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount); |

## 8. Next Micro-Step

Recommended next command:

- add Hutang master/payment consistency regression
- run existing Hutang and Account Ledger debt payment regressions
- run Review Queue and Credit Card Sprint 2 baselines
- run Apps Script syntax check
- commit the smallest test-only patch
