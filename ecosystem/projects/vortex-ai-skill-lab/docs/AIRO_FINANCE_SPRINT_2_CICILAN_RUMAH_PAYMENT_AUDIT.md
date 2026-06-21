# AIRO Finance - Sprint 2 Cicilan Rumah Payment History Audit

Status: EXACT AUDIT
Sprint: Sprint 2 - Domain Tab Maturation
Generated at: 2026-05-24 14:31:31
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document audits Cicilan Rumah domain-tab maturity after Review Queue, Credit Card, Hutang, and Aset contracts are locked.

Scope:

- Cicilan Rumah payment history
- payment ID consistency
- remaining balance / remaining principal fields
- Review Queue approved-row routing into Cicilan Rumah
- safe fallback when amount/header/remaining evidence is incomplete

No runtime patch is made in this micro-step.

## 2. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `auditCicilanRumah_` | MISSING | MISSING |  |
| `findCicilanRumahPaymentHeader_` | MISSING | MISSING |  |
| `findCicilanRumahMasterHeader_` | MISSING | MISSING |  |
| `writeCicilanRumahSafely_` | MISSING | MISSING |  |
| `appendCicilanRumahPayment_` | MISSING | MISSING |  |
| `appendCicilanRumahPaymentLog_` | MISSING | MISSING |  |
| `updateCicilanRumahMaster_` | MISSING | MISSING |  |
| `parseCicilanRumahPayment_` | MISSING | MISSING |  |
| `parseMortgagePayment_` | MISSING | MISSING |  |
| `routeReviewApprovedTab_` | 2761-2785 | FOUND | cicilan:2, kpr:1, rumah:3, AIRO_CONFIG.tabs.cicilanRumah:1 |
| `processReviewQueueApproved` | 2615-2734 | FOUND | amount:8, issue_reason:5, AIRO_CONFIG.tabs.review:1 |

## 3. Existing Test Candidates

- tests/personal-workflow/test_airo_cicilan_rumah_planner.py
- tests/personal-workflow/test_airo_review_queue_planner.py
- tests/personal-workflow/test_airo_review_queue_status_reason_contract.py

## 4. Risk Notes

- findCicilanRumahPaymentHeader_ missing by expected name; payment-history header detection needs exact mapping.
- findCicilanRumahMasterHeader_ missing by expected name; master balance header detection needs exact mapping.
- auditCicilanRumah_ missing by expected name; existing audit command surface may use a different function name.
- Review Queue approval routes through routeReviewApprovedTab_; Cicilan Rumah routing should be covered by contract before runtime patch.

## 5. Cicilan Rumah Maturity Questions

| Area | Question | Runtime Patch Now? |
|---|---|---:|
| Payment history | Does a payment append a durable history row with payment_id/date/amount? | No |
| Remaining balance | Does payment update or preserve remaining principal/balance consistently? | No |
| Header mapping | Are master/payment headers detected by canonical names instead of fragile column indexes? | No |
| Review Queue routing | Can approved Cicilan Rumah rows route safely from Review Queue? | No |
| Fallback | Does unclear Cicilan Rumah route to Review Queue instead of unsafe write? | No |

## 6. Recommended Next Patch

Add a focused Cicilan Rumah payment-history contract regression first.

The regression should lock:

- payment history header detection
- payment_id / date / amount / remaining fields
- safe Review Queue routing for Cicilan Rumah/KPR terms
- no Cash Ledger deletion
- no dashboard migration
- no Finance Events implementation
- no Email Ingestion implementation

Patch boundary:

- test-only first
- no broad refactor
- no runtime patch until the contract exposes an actual gap
- preserve Sprint 1 Account Ledger behavior

## 7. Direct Source Findings

| Line | Source Text |
|---:|---|
| 17 | cicilanRumah: '🏠 Cicilan Rumah', |
| 73 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 80 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 83 | amount > 0 \|\| |
| 91 | function parseAmountAccountClarificationAnswer_(text) { |
| 92 | const amount = parseAmount_(String(text \|\| '').toLowerCase()); |
| 96 | amount: amount, |
| 101 | function canAskMissingAmountAccountClarification_(parsed, rawText) { |
| 103 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 106 | if (amount > 0) return false; |
| 111 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 116 | function buildMissingAmountAccountClarificationMessage_(parsed) { |
| 134 | if (/^(d\|4)$/i.test(t) \|\| /\b(sisa\|remaining\|saldo akhir\|akhir)\b/i.test(t)) return 'cash_remaining'; |
| 142 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 146 | if (amount <= 0) return false; |
| 150 | const hasClearMeaning = /\b(masuk\|keluar\|terima\|diterima\|beli\|bayar\|kepake\|terpakai\|pegang\|saldo\|sisa\|dari\|ke\|bensin\|bbm)\b/i.test(text); |
| 157 | 'Saya tangkap ada transaksi Cash Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 162 | 'D. Sisa cash\n' + |
| 170 | const amount = String(Number((pending && pending.amount) \|\| 0)); |
| 174 | if (direction === 'cash_in') return ('cash masuk ' + amount + ' ' + tail).trim(); |
| 175 | if (direction === 'cash_out') return ('cash keluar ' + amount + ' ' + tail).trim(); |
| 176 | if (direction === 'cash_start') return ('saya pegang cash ' + amount + ' saldo awal ' + tail).trim(); |
| 177 | if (direction === 'cash_remaining') return ('sisa cash ' + amount + ' saldo akhir ' + tail).trim(); |
| 197 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 201 | if (amount <= 0) return false; |
| 212 | 'Saya tangkap akun ' + ((parsed && parsed.account) \|\| '-') + ' Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi arahnya belum jelas.\n\n' + |
| 225 | const amount = String(Number((pending && pending.amount) \|\| 0)); |
| 230 | if (direction === 'out') return ('pengeluaran ' + amount + ' pakai ' + account + ' ' + tail).trim(); |
| 231 | if (direction === 'in') return ('pemasukan ' + amount + ' ke ' + account + ' ' + tail).trim(); |
| 272 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 274 | if (amount <= 0) return false; |
| 285 | 'Transfer Rp' + ((parsed && parsed.amount) \|\| 0) + ' ini dari akun mana ke akun mana?\n\n' + |
| 299 | const amount = String(Number((pending && pending.amount) \|\| 0)); |
| 300 | return 'transfer ' + amount + ' dari ' + route.source.toLowerCase() + ' ke ' + route.target.toLowerCase(); |
| 308 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar tagihan\|bayar cc\|payment\|tagihan\|lunas\|pelunasan)\b/i.test(t)) return 'cc_payment'; |
| 317 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 319 | if (amount <= 0) return false; |
| 333 | 'Saya tangkap ada transaksi Credit Card Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 348 | const amount = String(Number((pending && pending.amount) \|\| 0)); |
| 360 | return 'cc beli ' + detail + ' ' + amount; |
| 363 | if (choice === 'cc_payment') return 'CC_PAYMENT_HELP_ONLY'; |
| 386 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment'; |
| 395 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 397 | if (amount <= 0) return false; |
| 400 | if ((isBorrowInText_(text) \|\| isDebtPaymentText_(text)) && parseDebtPerson_(rawText)) return false; |
| 407 | 'Saya tangkap ada transaksi Hutang Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 455 | ((parsed && parsed.amount) ? ' Rp' + parsed.amount : '') + |
| 512 | if ((isBorrowInText_(lower) \|\| isDebtPaymentText_(lower)) && parseDebtPerson_(text)) { |
| 517 | if (choice === 'debt_payment') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 546 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 562 | function canAskAmountOnlyMissingCategoryClarification_(parsed, rawText) { |
| 566 | const amount = Number(parsed && parsed.amount ? parsed.amount : 0); |
| 567 | if (!amount \|\| amount <= 0) return false; |
| 575 | // URL/gid/chat transcript noise must not become amount/category evidence. |
| 591 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 601 | const amount = Number((parsed && parsed.amount) \|\| 0); |
| 605 | if (amount <= 0) return false; |
| 609 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 616 | 'Saya tangkap transaksi Rp' + ((parsed && parsed.amount) \|\| 0) + |
| 645 | if (!parsed.amount \|\| Number(parsed.amount) <= 0) return false; |
| 653 | // First implementation target: regular expense-like purchase, not debts/assets/cash movement/CC payment. |
| 654 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 668 | ' Rp' + (parsed.amount \|\| 0) + '.\n\n' + |
| 746 | if (pending.type === 'missing_amount_account') { |
| 747 | const answer = parseAmountAccountClarificationAnswer_(rawText); |
| 749 | if (!answer.amount \|\| !answer.account) { |
| 767 | ' ' + String(answer.amount) + |
| 787 | if (resolvedText === 'CC_PAYMENT_HELP_ONLY') { |
| 1042 | 'D. Sisa cash\n' + |
| 1169 | amount: parsed.amount, |
| 1181 | amount: parsed.amount, |
| 1192 | amount: parsed.amount, |
| 1204 | amount: parsed.amount, |
| 1215 | amount: parsed.amount, |
| 1227 | amount: parsed.amount, |
| 1238 | amount: parsed.amount, |
| 1250 | amount: parsed.amount, |
| 1261 | amount: parsed.amount, |
| 1273 | amount: parsed.amount, |
| 1284 | amount: parsed.amount, |
| 1295 | amount: parsed.amount, |
| 1301 | if (canAskAmountOnlyMissingCategoryClarification_(parsed, effectiveRawText)) { |
| 1306 | amount: parsed.amount, |
| 1318 | amount: parsed.amount, |
| 1321 | sprint0a_guard: 'amount_only_missing_category' |
| 1325 | if (canAskMissingAmountAccountClarification_(parsed, effectiveRawText)) { |
| 1327 | type: 'missing_amount_account', |
| 1330 | amount: parsed.amount, |
| 1335 | sendTelegram_(chatId, buildMissingAmountAccountClarificationMessage_(parsed)); |
| 1340 | clarification_type: 'missing_amount_account', |
| 1341 | amount: parsed.amount, |
| 1352 | amount: parsed.amount, |
| 1364 | amount: parsed.amount, |
| 1375 | amount: parsed.amount, |
| 1386 | amount: parsed.amount, |
| 1408 | 'Nominal: Rp' + parsed.amount + '\n\n' + |
| 1424 | amount: parsed.amount, |
| 1463 | function syncCashLedgerRuntimeAmountColumns_(ss, rowNumber, inflow, amount) { |
| 1467 | const inCol = findCashLedgerExactHeaderCol_(sheet, 'amount_in'); |
| 1468 | const outCol = findCashLedgerExactHeaderCol_(sheet, 'amount_out'); |
| 1469 | if (inCol) sheet.getRange(rowNumber, inCol).setValue(inflow ? amount : ''); |
| 1470 | if (outCol) sheet.getRange(rowNumber, outCol).setValue(inflow ? '' : amount); |
| 1481 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1490 | amount_start: cashInflow ? parsed.amount : '', |
| 1491 | amount_remaining: cashInflow ? parsed.amount : '', |
| 1497 | amount: parsed.amount, |
| 1498 | amount_in: cashInflow ? parsed.amount : '', |
| 1499 | amount_out: cashInflow ? '' : parsed.amount, |
| 1504 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.cash, row, { createIfMissing: false }); |
| 1506 | syncCashLedgerRuntimeAmountColumns_(ss, result.row, cashInflow, parsed.amount); |
| 1516 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1517 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1520 | const amount = parsed.amount \|\| 0; |
| 1523 | const explicitOutflowTypes = ['expense', 'transfer_out', 'cash_out', 'cc_payment', 'debt_payment', 'asset_purchase']; |
| 1542 | amount_in: isInflow ? amount : '', |
| 1543 | amount_out: isInflow ? '' : amount, |
| 1550 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1555 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1579 | 'entry_id', 'date', 'account', 'amount_in', 'amount_out', |
| 1581 | 'source_tab', 'linked_txn_id', 'notes' |
| 1717 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1724 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1734 | return appendByHeader_(ss, tabName, common, { createIfMissing: false }); |
| 1744 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1747 | fallback_reason: 'asset_tab_missing' |
| 1758 | amount: parsed.amount \|\| amountForIntent_(parsed, rawText) |
| 1761 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 1763 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1781 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1784 | fallback_reason: 'asset_section_unclear_or_header_not_found' |
| 1787 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1790 | fallback_reason: 'asset_write_error: ' + String(err && err.message ? err.message : err) |
| 1813 | amount: data.amount, |
| 1818 | linked_txn_id: data.linked_txn_id, |
| 2000 | function appendByHeader_(ss, tabName, data, options) { |
| 2108 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2119 | if (headerKey === 'amount_start' \|\| headerKey.includes('amount_start')) { |
| 2120 | return data.amount_start ?? ''; |
| 2123 | if (headerKey === 'amount_remaining' \|\| headerKey.includes('amount_remaining')) { |
| 2124 | return data.amount_remaining ?? ''; |
| 2136 | headerKey === 'amount_out' \|\| |
| 2137 | headerKey.includes('amount_out') \|\| |
| 2145 | return cashInflow ? '' : (data.amount_out ?? data.amount ?? ''); |
| 2149 | headerKey === 'amount_in' \|\| |
| 2150 | headerKey.includes('amount_in') \|\| |
| 2158 | return cashInflow ? (data.amount_in \|\| data.amount \|\| '') : (data.amount_in ?? ''); |
| 2186 | return ['date', 'amount', 'description', 'category', 'account', 'status', 'raw_text', 'type'] |
| 2194 | // Important: check amount_in / amount_out before generic amount, |
| 2195 | // otherwise amount_out may be filled as expense for cash inflow rows. |
| 2197 | h === 'amount_in' \|\| |
| 2198 | h.includes('amount_in') \|\| |
| 2206 | return 'amount_in'; |
| 2210 | h === 'amount_out' \|\| |
| 2211 | h.includes('amount_out') \|\| |
| 2219 | return 'amount_out'; |
| 2224 | date: ['date', 'tanggal', 'tgl', 'payment_date', 'tanggal_bayar', 'tanggal_transaksi'], |
| 2228 | amount: ['amount', 'nominal', 'jumlah', 'nilai', 'total', 'payment_amount', 'nominal_bayar', 'jumlah_bayar', 'angsuran'], |
| 2229 | account: ['account', 'akun', 'wallet', 'rekening', 'sumber_dana', 'payment_account'], |
| 2234 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2238 | fallback_reason: ['fallback_reason', 'reason', 'alasan'], |
| 2262 | isCreditCardPaymentText_(text) |
| 2267 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text)) return AIRO_CONFIG.tabs.cicilanRumah; |
| 2272 | isDebtPaymentText_(text) |
| 2288 | const amount = Number(data && data.amount ? data.amount : 0); |
| 2292 | if (!amount \|\| amount <= 0) return 'amount_missing_or_zero'; |
| 2303 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) { |
| 2312 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) && !/\b\d+(?:[.,]\d+)?\s*(jt\|juta\|rb\|ribu\|k)?\b/i.test(text)) { |
| 2313 | return 'cicilan_rumah_amount_unclear'; |
| 2326 | const baseAmount = parseAmount_(text); |
| 2327 | const amount = gold.isGoldAsset |
| 2329 | : baseAmount; |
| 2336 | amount, |
| 2357 | parsed.issue_reason = issueReason; |
| 2367 | function parseAmount_(text) { |
| 2399 | function cleanAmount_(s) { |
| 2414 | if (typeof isCreditCardPaymentText_ === 'function' && isCreditCardPaymentText_(t)) return 'Blu'; |
| 2446 | if (isCreditCardPaymentText_(t)) return 'CC Payment'; |
| 2447 | if (isBorrowInText_(t) \|\| isDebtPaymentText_(t)) return 'Hutang'; |
| 2452 | if (/\b(cicilan rumah\|kpr\|angsuran rumah)\b/i.test(t)) return 'Cicilan Rumah'; |
| 2498 | if (isCreditCardPaymentText_(t)) return 'cc_payment'; |
| 2501 | if (isDebtPaymentText_(t)) return 'debt_payment'; |
| 2669 | const parsedAmount = getReviewValue_(row, map, ['parsed_amount', 'amount', 'nominal']); |
| 2670 | const amount = normalizeReviewAmount_(parsedAmount); |
| 2677 | if (!amount \|\| amount <= 0) { |
| 2678 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_amount_missing'); |
| 2684 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'approved_but_account_missing'); |
| 2695 | amount: amount, |
| 2704 | const plannedTab = routeReviewApprovedTab_(parsed, rawText); |
| 2713 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'processed_to_' + result.writtenTab); |
| 2716 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_failed_' + (result.reason \|\| 'unknown')); |
| 2720 | setReviewValue_(sheet, sheetRow, map, ['issue_reason'], 'process_error_' + String(err && err.message ? err.message : err)); |
| 2761 | function routeReviewApprovedTab_(parsed, rawText) { |
| 2768 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) \|\| parsed.category === 'Cicilan Rumah') { |
| 2769 | return AIRO_CONFIG.tabs.cicilanRumah; |
| 2821 | function normalizeReviewAmount_(value) { |
| 2824 | return cleanAmount_(String(value \|\| '')); |
| 2872 | const amountIn = Number(row[16] \|\| 0); |
| 2873 | const amountOut = Number(row[15] \|\| 0); |
| 2874 | const amountStart = Number(row[2] \|\| 0); |
| 2875 | const amountRemaining = Number(row[4] \|\| 0); |
| 2876 | const amount = amountIn \|\| amountOut \|\| amountStart \|\| amountRemaining \|\| 0; |
| 2878 | if (!amount) return; |
| 2883 | sheet.getRange(r, 3).setValue(amount);          // amount_start |
| 2884 | sheet.getRange(r, 5).setValue(amount);          // amount_remaining |
| 2898 | sheet.getRange(r, 16).clearContent();           // amount_out |
| 2899 | sheet.getRange(r, 17).setValue(amount);         // amount_in |
| 2901 | sheet.getRange(r, 16).setValue(amount);         // amount_out |
| 2902 | sheet.getRange(r, 17).clearContent();           // amount_in |
| 3115 | const price = cleanAmount_(m[1]); |
| 3355 | const totalAmount = purchasePrice \|\| (price24k && pureGramRounded ? Math.round(price24k * pureGramRounded) : ''); |
| 3375 | // H total_amount |
| 3381 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 3388 | totalAmount \|\| '', |
| 3450 | total_amount: ['total_amount', 'total', 'harga_beli', 'modal', 'nilai_beli'], |
| 3541 | return cleanAmount_(buy[2]); |
| 3733 | return cleanAmount_(raw); |
| 3823 | const oldPrincipal = asset.getRange('AB20').getValue(); |
| 3827 | const principal = oldPrincipal \|\| 145000000; |
| 3833 | asset.getRange('AA17').setValue('Nilai Rumah Pasar'); |
| 3839 | asset.getRange('AA19').setValue('Nilai Rumah Konservatif'); |
| 3842 | asset.getRange('AA20').setValue('Sisa Pokok Rumah'); |
| 3843 | asset.getRange('AB20').setValue(principal); |
| 3845 | asset.getRange('AA21').setValue('Ekuitas Rumah'); |
| 3862 | principal |
| 3900 | const required = ['amount', 'status_pocket_blu', 'billing_cycle_id']; |
| 3914 | const amountFromDisplay_ = function(value) { |
| 3943 | const amount = amountFromDisplay_(row[map.amount - 1]); |
| 3947 | if (!amount \|\| !cycleId) return; |
| 3951 | status.indexOf('paid') >= 0 \|\| |
| 3956 | stats.payable_total += amount; |
| 3958 | if (isSudahBlu) stats.payable_sudah_blu += amount; |
| 3959 | else stats.payable_belum_blu += amount; |
| 3963 | stats.unbilled_total += amount; |
| 3965 | if (isSudahBlu) stats.unbilled_sudah_blu += amount; |
| 3966 | else stats.unbilled_belum_blu += amount; |
| 3993 | cc.getRange('A3').setValue('Tagihan jatuh tempo tetap tampil sampai dana pembayaran disiapkan di Pocket Blu khusus CC / paid / closed.'); |
| 4112 | const required = ['amount', 'status_pocket_blu', 'billing_cycle_id', 'billing_start', 'billing_end']; |
| 4140 | const amountFromDisplay_ = function(value) { |
| 4155 | const amount = amountFromDisplay_(row[map.amount - 1]); |
| 4159 | if (!amount \|\| !cycleId) return; |
| 4163 | status.indexOf('paid') >= 0 \|\| |
| 4168 | stats.payable_total += amount; |
| 4170 | if (isSudahBlu) stats.payable_sudah_blu += amount; |
| 4171 | else stats.payable_belum_blu += amount; |
| 4175 | stats.unbilled_total += amount; |
| 4177 | if (isSudahBlu) stats.unbilled_sudah_blu += amount; |
| 4178 | else stats.unbilled_belum_blu += amount; |
| 4280 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4286 | dashboard.getRange('B20:C20').merge().setValue('Ekuitas Rumah'); |
| 4293 | dashboard.getRange('E17:F17').merge().setValue('Nilai Rumah Pasar'); |
| 4299 | dashboard.getRange('E19:F19').merge().setValue('Nilai Rumah Konservatif'); |
| 4302 | dashboard.getRange('E20:F20').merge().setValue('Sisa Pokok Rumah'); |
| 4305 | dashboard.getRange('E21:F21').merge().setValue('Ekuitas Rumah'); |
| 4309 | dashboard.getRange('B23').setValue('Catatan: Net Worth Likuid tidak memasukkan rumah. Net Worth Total memasukkan ekuitas rumah konservatif.'); |
| 4387 | (text.includes('rumah') && text.includes('home equity')) \|\| |
| 4532 | const result = moveCreditCardStatusAfterAmount(); |
| 4540 | 'status_pocket_blu sekarang berada setelah amount dan sebelum description.\n\n' + |
| 4554 | if (/^admin\s+(audit\|check\|cek)\s+(cicilan\s+rumah\|cicilan\|kpr\|angsuran\s+rumah)\s+(rows\|row\|headers\|header\|testrows\|test\|status)/i.test(text)) { |
| 4556 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.cicilanRumah); |
| 4559 | sendTelegram_(chatId, 'Cicilan Rumah audit gagal: sheet Cicilan Rumah tidak ditemukan.'); |
| 4563 | command: 'cicilan_rumah_rows_runtime_audit', |
| 4564 | reason: 'cicilan_rumah_sheet_missing' |
| 4579 | const hasPaymentId = normalized.indexOf('payment_id') >= 0; |
| 4580 | const hasCicilanKe = normalized.indexOf('cicilan_ke') >= 0 \|\| normalized.indexOf('angsuran_ke') >= 0; |
| 4581 | const hasAmount = normalized.indexOf('amount') >= 0 \|\| normalized.indexOf('nominal') >= 0 \|\| normalized.indexOf('jumlah') >= 0; |
| 4584 | if (hasPaymentId \|\| (hasCicilanKe && hasAmount) \|\| (hasDate && hasAmount && values[r].join(' ').toLowerCase().indexOf('cicilan') >= 0)) { |
| 4600 | 'Cicilan Rumah audit gagal: header payment history tidak ditemukan.\n\n' + |
| 4607 | command: 'cicilan_rumah_rows_runtime_audit', |
| 4608 | reason: 'cicilan_rumah_header_missing' |
| 4628 | payment_id: findCol_(['payment_id', 'payment id', 'id_pembayaran']), |
| 4629 | date: findCol_(['date', 'tanggal', 'payment_date', 'tanggal_bayar', 'date_paid', 'paid_date']), |
| 4630 | amount: findCol_(['amount', 'nominal', 'jumlah', 'payment_amount', 'amount_paid', 'paid_amount', 'angsuran']), |
| 4631 | cicilan_ke: findCol_(['cicilan_ke', 'cicilan ke', 'angsuran_ke', 'installment_no']), |
| 4632 | remaining: findCol_(['remaining_after_payment', 'remaining', 'sisa_cicilan', 'sisa']), |
| 4652 | payment_id: col.payment_id ? row[col.payment_id - 1] : '', |
| 4654 | amount: col.amount ? row[col.amount - 1] : '', |
| 4656 | remaining: col.remaining ? row[col.remaining - 1] : '', |
| 4673 | ' \| payment_id=' + formatText_(item.payment_id) + |
| 4675 | ' \| amount=' + formatText_(item.amount) + |
| 4677 | ' \| remaining=' + formatText_(item.remaining) + |
| 4689 | 'Cicilan Rumah runtime audit selesai.\n\n' + |
| 4694 | 'payment_id=' + col.payment_id + ', date=' + col.date + ', amount=' + col.amount + ', cicilan_ke=' + col.cicilan_ke + ', remaining=' + col.remaining + ', notes=' + col.notes + '\n\n' + |
| 4705 | command: 'cicilan_rumah_rows_runtime_audit', |
| 4879 | const amountFromDisplay_ = function(value) { |
| 4898 | const amountText = cell_(row, map.amount); |
| 4901 | if (!desc && !amountText && !cycle) return; |
| 4903 | const amount = amountFromDisplay_(amountText); |
| 4904 | if (cycle) cycleTotals[cycle] = (cycleTotals[cycle] \|\| 0) + amount; |
| 4909 | amount: amountText, |
| 4922 | ' \| ' + (item.amount \|\| '-') + |
| 5094 | const cashOutCol = findColumn_(cashInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 16); |
| 5095 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5097 | const accountInCol = findColumn_(accountInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 4); |
| 5098 | const accountOutCol = findColumn_(accountInfo, ['amount_out', 'cash_out', 'nominal_keluar', 'keluar'], 5); |
| 5178 | const cashInCol = findColumn_(cashInfo, ['amount_in', 'cash_in', 'nominal_masuk', 'masuk'], 17); |
| 5180 | const cashAmountStartCol = findColumn_(cashInfo, ['amount_start', 'start_amount'], 3); |
| 5184 | const cashInAmountFromRow_ = function(row) { |
| 5187 | const amountStart = toNumber_(row[cashAmountStartCol - 1]); |
| 5191 | amountStart > 0 && |
| 5194 | return amountStart; |

## 8. Next Micro-Step

Recommended next command:

- add Cicilan Rumah payment-history consistency regression
- run any Cicilan Rumah/KPR tests found by filename scan
- run Sprint 2 domain baselines
- run Sprint 1 Account Ledger baselines
- run Apps Script syntax check
- commit the smallest test-only patch
