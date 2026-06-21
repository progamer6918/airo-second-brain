# AIRO Finance — Sprint 1 Asset/Debt Payment Outflow Audit

Status: AUDIT / DECISION
Sprint: Sprint 1 — Account Ledger Hardening
Generated at: 2026-05-24 13:18:56
Scope: asset purchase and debt payment wallet outflow into Account Ledger
Runtime change in this micro-step: No

## 1. Purpose

Sprint 1 requires wallet outflows for asset purchase and debt payment to be visible in Account Ledger.

This audit checks whether the active Apps Script runtime already mirrors asset/debt outflow into Account Ledger.

## 2. Prior Sprint 1 Evidence

Already completed before this audit:

- internal transfer two-row Account Ledger contract
- Account Ledger mirror linked_txn_id consistency
- cash movement Account Ledger mirror contract
- CC payment Account Ledger outflow runtime fix

## 3. Active Source

Primary runtime source:

- scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs

## 4. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `appendToAssetSection_` | 1779-1808 | FOUND | linked_txn_id:2, amount:2, account:2, asset:2 |
| `appendGoldAssetRow_` | 3300-3386 | FOUND | linked_txn_id:1, amount:1, account:4 |
| `appendDebtPaymentAndUpdateMaster_` | 6386-6449 | FOUND | appendByHeader_:3, linked_txn_id:1, pay_id:1, amount:6, account:3, payment:4, hutang:10 |
| `appendDebtIncreaseAndUpdateMaster_` | 6451-6512 | FOUND | appendByHeader_:3, linked_txn_id:1, pay_id:1, amount:6, payment:3, hutang:8 |
| `appendDebtPaymentLog_` | 6514-6526 | FOUND | payment:5, hutang:1 |
| `writeAccountLedgerMirror_` | 1516-1570 | FOUND | writeAccountLedgerMirror_:1, AIRO_CONFIG.tabs.accountLedger:2, appendByHeader_:1, linked_txn_id:3, amount:6, account:8 |
| `normalizeDebtAmbiguousClarificationAnswer_` | 382-391 | FOUND | debt_payment:1, payment:1, hutang:2 |
| `debtAmbiguousClarificationResolvedText_` | 507-521 | FOUND | debt_payment:1, payment:1 |
| `assetClarificationResolvedText_` | MISSING | MISSING |  |

## 5. Decision

Current evidence:

- asset_has_account_ledger_outflow: `False`
- asset_outflow_evidence_functions: `none`
- debt_has_account_ledger_outflow: `False`
- debt_outflow_evidence_functions: `none`

Decision:

- `Add test-first runtime patch for one smaller gap: debt_payment Account Ledger outflow first, then asset_purchase.`

## 6. Direct Source Findings

| Line | Source Text |
|---:|---|
| 18 | hutang: '🤝 Hutang', |
| 19 | aset: '🥇 Aset', |
| 80 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 111 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 131 | if (/^(a\|1)$/i.test(t) \|\| /\b(masuk\|terima\|diterima\|income\|pemasukan)\b/i.test(t)) return 'cash_in'; |
| 187 | if (/^(b\|2)$/i.test(t) \|\| /\b(masuk\|pemasukan\|income\|terima\|diterima\|refund\|gaji)\b/i.test(t)) return 'in'; |
| 231 | if (direction === 'in') return ('pemasukan ' + amount + ' ke ' + account + ' ' + tail).trim(); |
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
| 517 | if (choice === 'debt_payment') return 'DEBT_NEEDS_COMPLETE_REWRITE'; |
| 518 | if (choice === 'piutang_help') return 'DEBT_PIUTANG_HELP_ONLY'; |
| 546 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 591 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 609 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 653 | // First implementation target: regular expense-like purchase, not debts/assets/cash movement/CC payment. |
| 654 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 683 | 'Saya belum bisa memastikan transaksi ini, jadi belum saya catat.\n\n' + |
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
| 1164 | if (canAskAssetGoldAmbiguousClarification_(parsed, effectiveRawText)) { |
| 1166 | type: 'asset_gold_ambiguous', |
| 1175 | sendTelegram_(chatId, buildAssetGoldAmbiguousClarificationMessage_(parsed)); |
| 1180 | clarification_type: 'asset_gold_ambiguous', |
| 1481 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1516 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1517 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1550 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1555 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1559 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 1581 | 'source_tab', 'linked_txn_id', 'notes' |
| 1585 | var sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.accountLedger); |
| 1588 | sheet = ss.insertSheet(AIRO_CONFIG.tabs.accountLedger); |
| 1701 | if (key.includes('hutang')) { |
| 1702 | return writeHutangSafely_(ss, parsed, rawText, common); |
| 1705 | if (key.includes('aset')) { |
| 1706 | return writeAssetSafely_(ss, parsed, rawText, common); |
| 1717 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1724 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1728 | writtenTab: AIRO_CONFIG.tabs.accountLedger |
| 1739 | function writeAssetSafely_(ss, parsed, rawText, common) { |
| 1740 | const tabName = AIRO_CONFIG.tabs.aset; |
| 1747 | fallback_reason: 'asset_tab_missing' |
| 1752 | if (parsed.assetSection === 'gold') { |
| 1753 | return appendGoldAssetRow_(sheet, parsed, rawText, common); |
| 1756 | if (parsed.assetSection === 'savings') { |
| 1757 | const result = appendToAssetSection_(sheet, 'savings', common); |
| 1764 | fallback_reason: 'asset_section_unclear_or_header_not_found' |
| 1770 | fallback_reason: 'asset_write_error: ' + String(err && err.message ? err.message : err) |
| 1779 | function appendToAssetSection_(sheet, section, data) { |
| 1780 | const spec = section === 'gold' |
| 1785 | if (!header) return { status: 'fallback', reason: 'asset_section_header_not_found' }; |
| 1798 | linked_txn_id: data.linked_txn_id, |
| 1799 | asset_section: section |
| 1914 | // Asset savings validation |
| 2088 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2214 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2216 | creditor: ['creditor', 'kreditur', 'pemberi_hutang', 'pemberi_utang', 'lender'], |
| 2219 | asset_section: ['asset_section', 'section', 'bagian'] |
| 2250 | /\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| |
| 2254 | return AIRO_CONFIG.tabs.hutang; |
| 2257 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia\|nabung\|tabung\|saving\|savings\|aset\|investasi\|dana darurat)\b/i.test(text)) return AIRO_CONFIG.tabs.aset; |
| 2283 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) { |
| 2288 | if (/\b(hutang\|utang\|pinjam\|pinjaman)\b/i.test(text) && !parseCreditor_(text)) { |
| 2305 | const gold = parseGoldAsset_(rawText); |
| 2307 | const amount = gold.isGoldAsset |
| 2308 | ? (gold.purchasePrice \|\| gold.estimatedValue \|\| 0) |
| 2312 | date: gold.purchaseDate \|\| parseDate_(text), |
| 2313 | type: gold.isGoldAsset ? 'asset' : parseType_(text), |
| 2321 | assetSection: parseAssetSection_(text), |
| 2322 | goldAction: gold.action, |
| 2323 | goldKarat: gold.karat, |
| 2324 | goldWeightGram: gold.weightGram, |
| 2325 | goldPureGram: gold.pureGram, |
| 2326 | goldPurchasePrice: gold.purchasePrice, |
| 2327 | goldPurchaseDate: gold.purchaseDate, |
| 2328 | goldNotes: gold.notes, |
| 2329 | goldEstimatedValue: gold.estimatedValue, |
| 2330 | goldMarketPrice24k: gold.marketPrice24k |
| 2333 | const issueReason = gold.isGoldAsset |
| 2334 | ? ((!gold.weightGram \|\| gold.weightGram <= 0) ? 'gold_weight_missing_or_zero' : '') |
| 2397 | if (typeof isCreditCardPurchaseText_ === 'function' && isCreditCardPurchaseText_(t)) return 'Credit Card'; |
| 2425 | if (/\b(gaji\|salary\|income\|pemasukan\|terima gaji\|gajian)\b/i.test(t)) return 'Gaji'; |
| 2427 | if (isBorrowInText_(t) \|\| isDebtPaymentText_(t)) return 'Hutang'; |
| 2433 | if (/\b(hutang\|utang)\b/i.test(t)) return 'Hutang'; |
| 2434 | if (/\b(nabung\|tabung\|saving\|aset\|investasi\|emas\|gold)\b/i.test(t)) return 'Aset'; |
| 2479 | if (isCreditCardPurchaseText_(t)) return 'cc_purchase'; |
| 2481 | if (isDebtPaymentText_(t)) return 'debt_payment'; |
| 2483 | if (/\b(gaji\|salary\|income\|pemasukan\|terima gaji\|gajian\|dibayar\|refund\|reimburse\|reimbursement\|uang masuk\|dana masuk\|transfer masuk\|terima\|diterima\|dapat\|dapet)\b/i.test(t)) { |
| 2487 | if (/\b(nabung\|tabung\|saving\|investasi\|aset)\b/i.test(t)) { |
| 2511 | function parseAssetSection_(text) { |
| 2512 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text)) return 'gold'; |
| 2513 | if (/\b(nabung\|tabung\|saving\|savings\|dana darurat\|investasi\|aset)\b/i.test(text)) return 'savings'; |
| 2680 | assetSection: parseAssetSection_(rawText \|\| ''), |
| 2752 | if (/\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| parsed.category === 'Hutang') { |
| 2753 | return AIRO_CONFIG.tabs.hutang; |
| 2756 | if (/\b(nabung\|tabung\|saving\|savings\|aset\|investasi\|emas\|gold\|dana darurat)\b/i.test(text) \|\| parsed.category === 'Aset') { |
| 2757 | return AIRO_CONFIG.tabs.aset; |
| 3022 | * Daily ANTAM / Logam Mulia gold price updater. |
| 3025 | * - Update GOLD_24K_PRICE_PER_GRAM_IDR once per day. |
| 3033 | function updateAntamGoldPriceDaily() { |
| 3034 | const url = 'https://www.logammulia.com/harga-emas-hari-ini'; |
| 3041 | 'User-Agent': 'Mozilla/5.0 AIRO-Finance-Gold-Price-Updater' |
| 3049 | return recordGoldPriceUpdateFailure_('http_' + code); |
| 3055 | return recordGoldPriceUpdateFailure_('price_parse_failed'); |
| 3061 | props.setProperty('GOLD_24K_PRICE_PER_GRAM_IDR', String(price)); |
| 3062 | props.setProperty('GOLD_24K_PRICE_SOURCE', 'logammulia.com/harga-emas-hari-ini'); |
| 3063 | props.setProperty('GOLD_24K_PRICE_UPDATED_AT', now.toISOString()); |
| 3064 | props.setProperty('GOLD_24K_PRICE_UPDATE_STATUS', 'ok'); |
| 3069 | source: 'logammulia.com/harga-emas-hari-ini', |
| 3107 | function recordGoldPriceUpdateFailure_(reason) { |
| 3110 | const lastPrice = Number(props.getProperty('GOLD_24K_PRICE_PER_GRAM_IDR') \|\| 0); |
| 3112 | props.setProperty('GOLD_24K_PRICE_UPDATE_STATUS', 'failed:' + reason); |
| 3113 | props.setProperty('GOLD_24K_PRICE_LAST_FAILURE_AT', now.toISOString()); |
| 3123 | function setupDailyAntamGoldPriceTrigger() { |
| 3127 | trigger.getHandlerFunction() === 'updateAntamGoldPriceDaily' |
| 3134 | .newTrigger('updateAntamGoldPriceDaily') |
| 3144 | trigger: 'updateAntamGoldPriceDaily', |
| 3150 | function getCurrentGoldPriceStatus() { |
| 3155 | GOLD_24K_PRICE_PER_GRAM_IDR: props.getProperty('GOLD_24K_PRICE_PER_GRAM_IDR') \|\| '', |
| 3156 | GOLD_24K_PRICE_SOURCE: props.getProperty('GOLD_24K_PRICE_SOURCE') \|\| '', |
| 3157 | GOLD_24K_PRICE_UPDATED_AT: props.getProperty('GOLD_24K_PRICE_UPDATED_AT') \|\| '', |
| 3158 | GOLD_24K_PRICE_UPDATE_STATUS: props.getProperty('GOLD_24K_PRICE_UPDATE_STATUS') \|\| '' |
| 3162 | function forceGoldPriceTodayAntam() { |
| 3163 | return updateAntamGoldPriceDaily(); |
| 3168 | * Sync current gold price from Script Properties to the Aset sheet. |
| 3169 | * The current sheet note says: update Harga Emas Sekarang in F12. |
| 3171 | function syncGoldPriceToAssetSheet() { |
| 3173 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3176 | return { ok: false, reason: 'asset_sheet_missing' }; |
| 3179 | const price = getGoldMarketPrice24kPerGram_(); |
| 3182 | return { ok: false, reason: 'gold_price_missing_or_zero' }; |
| 3200 | * 3. Write price to Aset!F12 |
| 3202 | function updateAntamGoldPriceDailyAndSyncSheet() { |
| 3203 | const update = updateAntamGoldPriceDaily(); |
| 3204 | const sync = syncGoldPriceToAssetSheet(); |
| 3214 | * Replace old daily gold trigger with synced daily trigger. |
| 3216 | function setupDailyAntamGoldPriceTriggerSynced() { |
| 3221 | fn === 'updateAntamGoldPriceDaily' \|\| |
| 3222 | fn === 'updateAntamGoldPriceDailyAndSyncSheet' |
| 3229 | .newTrigger('updateAntamGoldPriceDailyAndSyncSheet') |
| 3239 | trigger: 'updateAntamGoldPriceDailyAndSyncSheet', |
| 3241 | writes_to: '🥇 Aset!F12' |
| 3250 | * Read latest 24K gold price per gram from Script Properties. |
| 3251 | * Main property is updated by updateAntamGoldPriceDaily(). |
| 3253 | function getGoldMarketPrice24kPerGram_() { |
| 3256 | const price = Number(props.getProperty('GOLD_24K_PRICE_PER_GRAM_IDR') \|\| 0); |
| 3269 | function setGoldMarketPrice24kPerGram(value) { |
| 3273 | throw new Error('Invalid GOLD_24K_PRICE_PER_GRAM_IDR value'); |
| 3278 | .setProperty('GOLD_24K_PRICE_PER_GRAM_IDR', String(Math.round(n))); |
| 3282 | .setProperty('GOLD_24K_PRICE_UPDATE_STATUS', 'manual_ok'); |
| 3284 | syncGoldPriceToAssetSheet(); |
| 3288 | GOLD_24K_PRICE_PER_GRAM_IDR: Math.round(n) |
| 3296 | function setGoldPriceManualToday() { |
| 3297 | return setGoldMarketPrice24kPerGram(2839000); |
| 3300 | function appendGoldAssetRow_(sheet, parsed, rawText, common) { |
| 3301 | const headerRow = findGoldLedgerHeaderRow_(sheet); |
| 3306 | reason: 'gold_ledger_header_not_found' |
| 3310 | const price24k = Number(parsed.goldMarketPrice24k \|\| getGoldMarketPrice24kPerGram_() \|\| 0); |
| 3311 | const physicalGram = Number(parsed.goldWeightGram \|\| 0); |
| 3312 | const karat = Number(parsed.goldKarat \|\| 24); |
| 3314 | const purchasePrice = Number(parsed.goldPurchasePrice \|\| 0); |
| 3315 | const action = parsed.goldAction \|\| parseGoldAction_(rawText); |
| 3321 | reason: 'gold_weight_missing' |
| 3325 | const pureGramRounded = roundGoldGram_(pureGram); |
| 3338 | parsed.goldNotes ? 'catatan: ' + parsed.goldNotes : '', |
| 3342 | isSell ? 'gold_outflow: true' : '' |
| 3345 | const targetRow = findNextGoldLedgerRow_(sheet, headerRow); |
| 3347 | // Gold Ledger fixed columns: |
| 3348 | // A gold_event_id |
| 3361 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 3362 | parsed.goldPurchaseDate \|\| parsed.date \|\| parseDate_(rawText), |
| 3384 | section: 'gold' |
| 3392 | function findGoldLedgerHeader_(sheet) { |
| 3400 | const hasGoldEvent = normalized.includes('gold_event_id'); |
| 3404 | if (hasGoldEvent && hasGramsIn && hasRawText) { |
| 3419 | function goldFieldForHeader_(header) { |

## 7. Gap Assessment

If no direct Account Ledger outflow exists for asset/debt payment surfaces, the next patch should stay deliberately small.

Debt payment outflow target:

- write one Account Ledger outflow row for the paying account
- preserve linked_txn_id
- set source_tab to Hutang/payment source evidence
- do not rewrite debt master logic
- do not rewrite payment history logic

Asset purchase outflow target:

- write one Account Ledger outflow row for the paying account
- preserve linked_txn_id
- set source_tab to Asset/source evidence
- do not rewrite asset master logic
- do not rewrite gold ledger logic

## 8. Test-First Patch Boundary

Allowed next patch:

- add focused static/runtime contract test
- add minimal Apps Script mirror call if missing
- rerun focused tests and syntax check

Not allowed:

- full asset module rewrite
- full debt module rewrite
- Cash Ledger deletion
- dashboard migration
- Account Ledger schema migration
- Finance Events implementation
- Sprint 2+ work
