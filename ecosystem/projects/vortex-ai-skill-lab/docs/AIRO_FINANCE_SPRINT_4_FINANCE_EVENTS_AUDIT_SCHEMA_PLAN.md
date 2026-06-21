# AIRO Finance - Sprint 4 Finance Events Audit and Schema Plan

Status: EXACT AUDIT / SCHEMA PLAN
Sprint: Sprint 4 - Finance Events
Generated at: 2026-05-24 15:17:33
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

Sprint 4 starts after Sprint 3 Cash Ledger Removal is CLOSED / PASS.

This micro-step audits current runtime surfaces and defines the Finance Events schema before any runtime implementation.

No runtime patch is made in this micro-step.

## 2. Sprint 4 Boundary

Allowed now:

- inspect transaction write surfaces
- inspect Account Ledger lineage fields
- inspect Review Queue approval path
- inspect Cash Ledger compatibility behavior
- define Finance Events schema and emission policy
- define smallest safe test-first patch

Not allowed now:

- implementing Finance Events writer
- adding new runtime tab writes
- changing Account Ledger schema
- re-enabling Cash Ledger writes
- deleting Cash Ledger tab or historical rows
- Email Ingestion implementation
- dashboard finalization
- broad Apps Script refactor

## 3. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `ensureFinanceEventsSheet_` | MISSING | MISSING |  |
| `writeFinanceEvent_` | MISSING | MISSING |  |
| `appendFinanceEvent_` | MISSING | MISSING |  |
| `buildFinanceEvent_` | MISSING | MISSING |  |
| `emitFinanceEvent_` | MISSING | MISSING |  |
| `logFinanceEvent_` | MISSING | MISSING |  |
| `writeRouted_` | 1712-1754 | FOUND | writeAccountLedgerMirror_:2, writeCashLedgerCompatibility_:1, appendByHeader_:1, AIRO_CONFIG.tabs.accountLedger:1, AIRO_CONFIG.tabs.cash:1 |
| `doPost` | 1091-1431 | FOUND | AIRO_CONFIG.tabs.review:1 |
| `processReviewQueueApproved` | 2634-2753 | FOUND | AIRO_CONFIG.tabs.review:1 |
| `appendByHeader_` | 2019-2066 | FOUND | appendByHeader_:1 |
| `writeAccountLedgerMirror_` | 1535-1589 | FOUND | source_tab:1, linked_txn_id:3, entry_id:1, writeAccountLedgerMirror_:1, appendByHeader_:1, AIRO_CONFIG.tabs.accountLedger:2 |
| `writeCashLedgerCompatibility_` | 1482-1491 | FOUND | writeCashLedgerCompatibility_:1 |
| `writeInternalTransferToAccountLedger_` | 7467-7530 | FOUND | linked_txn_id:3, writeAccountLedgerMirror_:2, writeCashLedgerCompatibility_:2, AIRO_CONFIG.tabs.accountLedger:1 |
| `appendCreditCardPurchase_` | 6168-6214 | FOUND | linked_txn_id:3, entry_id:1, appendByHeader_:1, AIRO_CONFIG.tabs.review:1 |
| `appendDebtPaymentAndUpdateMaster_` | 6425-6500 | FOUND | linked_txn_id:3, writeAccountLedgerMirror_:1, appendByHeader_:3, AIRO_CONFIG.tabs.review:3, AIRO_CONFIG.tabs.hutang:1 |
| `writeAssetSafely_` | 1758-1812 | FOUND | linked_txn_id:2, writeAccountLedgerMirror_:1, appendByHeader_:3, AIRO_CONFIG.tabs.review:3, AIRO_CONFIG.tabs.aset:2 |

## 4. Existing Test Candidates

- tests/personal-workflow/test_airo_account_ledger_asset_purchase_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_cash_movement_contract.py
- tests/personal-workflow/test_airo_account_ledger_cc_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_debt_payment_outflow_contract.py
- tests/personal-workflow/test_airo_account_ledger_internal_transfer_contract.py
- tests/personal-workflow/test_airo_aset_savings_gold_contract.py
- tests/personal-workflow/test_airo_asset_event_planner.py
- tests/personal-workflow/test_airo_asset_event_planner_skip_deleted.py
- tests/personal-workflow/test_airo_cash_ledger_planner.py
- tests/personal-workflow/test_airo_cash_ledger_remaining_dependency_contract.py
- tests/personal-workflow/test_airo_cash_ledger_removal_safety_contract.py
- tests/personal-workflow/test_airo_cash_ledger_write_disable_flag_contract.py
- tests/personal-workflow/test_airo_cicilan_rumah_payment_history_contract.py
- tests/personal-workflow/test_airo_cicilan_rumah_planner.py
- tests/personal-workflow/test_airo_credit_card_billing_cycle.py
- tests/personal-workflow/test_airo_credit_card_billing_status_contract.py
- tests/personal-workflow/test_airo_credit_card_mirror_planner.py
- tests/personal-workflow/test_airo_hutang_master_payment_contract.py
- tests/personal-workflow/test_airo_hutang_planner.py
- tests/personal-workflow/test_airo_review_queue_planner.py
- tests/personal-workflow/test_airo_review_queue_status_reason_contract.py

## 5. Risk Notes

- No Finance Events runtime tab/writer surface is obvious in active source.
- writeRouted_ is the primary candidate event emission point because it centralizes tab writes.
- Account Ledger mirror already provides source_tab and linked_txn_id; Finance Events must not replace Account Ledger.
- Cash Ledger writes are gated; Finance Events must not re-enable Cash Ledger writes.
- Review Queue approval path must emit or preserve event lineage only after an explicit contract.
- No deleteSheet pattern found in active source.
- Email Ingestion remains out of runtime scope for Sprint 4.

## 6. Proposed Finance Events Schema

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `event_id` | string | required | Stable unique event ID. Must be deterministic or safely generated once. |
| `event_ts` | date/string | required | Event timestamp, preferably same date source as transaction row. |
| `event_type` | string | required | Canonical type: transaction_created, review_approved, account_mirror_written, domain_row_written, compatibility_skipped. |
| `event_source` | string | required | Source layer: telegram, review_queue, admin, system. |
| `source_tab` | string | required | The tab that caused the event or was written. |
| `source_row` | number/string | optional | Row number if known after append. |
| `linked_txn_id` | string | required when available | Lineage key shared with Account Ledger and domain rows. |
| `account` | string | optional | Canonical account when relevant. |
| `category` | string | optional | Canonical category when relevant. |
| `amount` | number | optional | Nominal amount when relevant. |
| `direction` | string | optional | in/out/neutral/unknown. |
| `status` | string | required | ok/skipped/error. |
| `reason` | string | optional | Machine-readable reason for skipped/error events. |
| `payload_json` | string | optional | Small redacted JSON payload. No full email body, no OTP/security content. |
| `notes` | string | optional | Human-safe note. |

## 7. Event Type Policy

Initial allowed event types:

| Event Type | Emission Candidate | Runtime Patch Now? |
|---|---|---:|
| `transaction_created` | after a successful `writeRouted_` write | No |
| `account_mirror_written` | after `writeAccountLedgerMirror_` returns ok | No |
| `domain_row_written` | after domain writer returns ok | No |
| `review_approved` | after `processReviewQueueApproved` writes approved row | No |
| `compatibility_skipped` | when `writeCashLedgerCompatibility_` skips Cash Ledger write | No |
| `write_failed` | when a write returns ok false or throws handled error | No |

## 8. Event Source Policy

Initial allowed event sources:

- `telegram`
- `review_queue`
- `admin`
- `system`

Event source must be explicit. Do not infer email source in Sprint 4.

## 9. Privacy / Safety Policy

Finance Events must not store:

- full raw email body
- OTP/security content
- bank OTP
- passwords
- access tokens
- full sensitive message dumps

Finance Events may store:

- redacted raw text snippet only if already allowed by existing runtime policy
- linked transaction ID
- tab name
- row number
- event type/status/reason
- compact JSON payload for debugging

## 10. Relationship to Existing Ledgers

Finance Events is not a replacement for:

- Account Ledger
- domain tabs
- Review Queue
- Credit Card billing/status rows
- Hutang master/payment rows
- Aset savings/gold rows
- Cicilan Rumah payment history

Finance Events is an append-only observability and lineage surface.

## 11. Recommended Next Patch

Add the smallest test-only Finance Events schema contract first.

The regression should lock:

- Finance Events tab is not implemented yet
- proposed schema fields are documented
- `writeRouted_`, `writeAccountLedgerMirror_`, and `processReviewQueueApproved` are candidate emission points
- Account Ledger remains source of truth for wallet movements
- Cash Ledger compatibility flag remains default OFF
- no Email Ingestion implementation is introduced
- no new runtime writer is added in the test-only step

## 12. Direct Source Findings

| Line | Source Text |
|---:|---|
| 9 | * Telegram -> Cloudflare Worker -> Apps Script doPost -> Google Sheet -> Telegram reply |
| 15 | cash: '💵 Cash Ledger', |
| 16 | creditCard: '💳 Credit Card', |
| 17 | cicilanRumah: '🏠 Cicilan Rumah', |
| 18 | hutang: '🤝 Hutang', |
| 19 | aset: '🥇 Aset', |
| 20 | accountLedger: '📒 Account Ledger', |
| 21 | review: '🧾 Review Queue' |
| 64 | if (/^(d\|4)$/i.test(t) \|\| /\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t)) return 'Credit Card'; |
| 80 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|sarapan\|siang\|malam\|cash\|tunai\|bca\|blu\|cc\|credit card\|kartu kredit\|tokopedia\|shopee\|grab\|gojek\|transfer\|tf\|topup\|tarik\|masuk\|keluar\|terima\|diterima\|gaji\|refund\|hutang\|utang\|pinjam\|cicilan\|kpr\|angsuran\|emas\|aset\|saldo)\b/i.test(text); |
| 111 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan\|kpr\|angsuran\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) return false; |
| 123 | '- 15000 credit card' |
| 205 | const hasClearAction = /\b(beli\|bayar\|makan\|minum\|kopi\|jajan\|transfer\|tf\|dari\|ke\|masuk\|keluar\|gaji\|refund\|terima\|diterima\|topup\|tarik\|cc\|credit card\|cash\|tunai)\b/i.test(text); |
| 307 | if (/^(a\|1)(\b\|[\s.:-])/i.test(t) \|\| /\b(belanja\|beli\|purchase\|transaksi baru\|pakai cc\|pakai credit card)\b/i.test(t)) return 'cc_purchase'; |
| 320 | if (!/\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(text)) return false; |
| 333 | 'Saya tangkap ada transaksi Credit Card Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 335 | 'A. Belanja pakai Credit Card\n' + |
| 336 | 'B. Bayar tagihan Credit Card\n' + |
| 354 | .replace(/\b(belanja\|beli\|purchase\|transaksi baru\|pakai cc\|pakai credit card)\b/ig, ' ') |
| 385 | if (/^(a\|1)$/i.test(t) \|\| /\b(pinjam\|pinjaman\|saya pinjam\|tambah hutang\|tambah utang)\b/i.test(t)) return 'debt_in'; |
| 386 | if (/^(b\|2)$/i.test(t) \|\| /\b(bayar hutang\|bayar utang\|lunasi\|nyicil\|cicil)\b/i.test(t)) return 'debt_payment'; |
| 398 | if (!/\b(hutang\|utang\|pinjaman\|pinjam)\b/i.test(text)) return false; |
| 407 | 'Saya tangkap ada transaksi Hutang Rp' + ((parsed && parsed.amount) \|\| 0) + ', tapi maksudnya belum jelas.\n\n' + |
| 409 | 'A. Saya pinjam / tambah hutang\n' + |
| 410 | 'B. Saya bayar hutang\n' + |
| 411 | 'C. Orang bayar hutang ke saya / piutang\n' + |
| 415 | '- bayar hutang ke Budi 50000 dari bca' |
| 424 | if (/^(c\|3\|aset\|tabung\|tabungan\|saving\|savings\|biasa)\b/i.test(t)) return 'savings'; |
| 438 | const isGoldAsset = /\b(aset\s+emas\|emas\|gold\|antam\|logam\s+mulia)\b/i.test(text); |
| 446 | if (category && category !== 'aset') return false; |
| 454 | 'Saya tangkap ada transaksi Aset/Emas' + |
| 460 | 'C. Catat sebagai aset/tabungan biasa\n' + |
| 477 | .replace(/\baset\s+emas\b/ig, 'aset') |
| 478 | .replace(/\b(logam\s+mulia\|antam\|emas\|gold)\b/ig, 'aset') |
| 487 | return doPost({ |
| 546 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar\|saldo\|tagihan\|angsuran)\b/i.test(original); |
| 591 | /\b(beli\|bayar\|jajan\|makan\|minum\|kopi\|bensin\|parkir\|tol\|grab\|gojek\|shopee\|tokopedia\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|hutang\|utang\|pinjam\|cicilan\|kpr\|emas\|gold\|aset\|nabung\|tabung\|saving\|gaji\|refund\|terima\|masuk\|keluar)\b/i.test(text); |
| 609 | if (/\b(transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card\|hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|nabung\|tabung\|saving\|savings\|investasi\|gaji\|refund\|terima\|diterima\|masuk)\b/i.test(text)) return false; |
| 654 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|emas\|gold\|aset\|transfer\|tf\|topup\|tarik\|cash\|tunai\|cc\|credit card\|kartu kredit)\b/i.test(text)) { |
| 673 | 'D. Credit Card\n' + |
| 717 | const fallbackResult = writeRouted_( |
| 867 | 'Saya belum mencatat transaksi Aset/Emas ini.' |
| 886 | 'Saya butuh detail orang dan format lengkap untuk Hutang.\n\n' + |
| 889 | '- bayar hutang ke Budi 50000 dari bca' |
| 897 | 'Saya belum mencatat piutang/orang bayar hutang ke saya karena flow piutang belum dikunci.\n\n' + |
| 911 | 'Saya belum mencatat transaksi Hutang ini.\n\n' + |
| 914 | '- bayar hutang ke Budi 50000 dari bca' |
| 1068 | 'D. Credit Card\n' + |
| 1091 | function doPost(e) { |
| 1398 | const routedResult = writeRouted_(ss, finalTab, parsed, effectiveRawText, stagingResult); |
| 1500 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1523 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.cash, row, { createIfMissing: false }); |
| 1532 | * Mirrors cash movement to the Account Ledger tab. |
| 1536 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1568 | source_tab: sourceTab, |
| 1569 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1574 | const result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 1592 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1600 | 'source_tab', 'linked_txn_id', 'notes' |
| 1712 | function writeRouted_(ss, plannedTab, parsed, rawText, common) { |
| 1716 | if (key.includes('credit card')) { |
| 1720 | if (key.includes('hutang')) { |
| 1721 | return writeHutangSafely_(ss, parsed, rawText, common); |
| 1724 | if (key.includes('aset')) { |
| 1733 | if (key.includes('cash ledger')) { |
| 1753 | return appendByHeader_(ss, tabName, common, { createIfMissing: false }); |
| 1759 | const tabName = AIRO_CONFIG.tabs.aset; |
| 1763 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1770 | function mirrorAssetPurchaseToAccountLedger_(result) { |
| 1775 | category: parsed.category \|\| 'Aset', |
| 1780 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 1782 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1792 | return mirrorAssetPurchaseToAccountLedger_(appendGoldAssetRow_(sheet, parsed, rawText, common)); |
| 1797 | if (result.status === 'written') return mirrorAssetPurchaseToAccountLedger_({ ...result, writtenTab: tabName }); |
| 1800 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1806 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 1837 | linked_txn_id: data.linked_txn_id, |
| 1927 | // Cash Ledger movement type validation. |
| 1948 | // Review Queue status validation |
| 2019 | function appendByHeader_(ss, tabName, data, options) { |
| 2127 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2188 | if (headerKey === 'source_tab' \|\| headerKey.includes('source_tab')) { |
| 2189 | return data.source_tab \|\| data.source \|\| ''; |
| 2244 | type: ['type', 'jenis', 'event_type', 'jenis_transaksi', 'transaction_type'], |
| 2253 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
| 2255 | creditor: ['creditor', 'kreditur', 'pemberi_hutang', 'pemberi_utang', 'lender'], |
| 2286 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text)) return AIRO_CONFIG.tabs.cicilanRumah; |
| 2289 | /\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| |
| 2293 | return AIRO_CONFIG.tabs.hutang; |
| 2296 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia\|nabung\|tabung\|saving\|savings\|aset\|investasi\|dana darurat)\b/i.test(text)) return AIRO_CONFIG.tabs.aset; |
| 2322 | if (/\b(hutang\|utang\|pinjam\|pinjaman\|cicilan rumah\|kpr\|angsuran rumah\|cash\|tunai)\b/i.test(text)) { |
| 2327 | if (/\b(hutang\|utang\|pinjam\|pinjaman)\b/i.test(text) && !parseCreditor_(text)) { |
| 2331 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) && !/\b\d+(?:[.,]\d+)?\s*(jt\|juta\|rb\|ribu\|k)?\b/i.test(text)) { |
| 2435 | // "cc beli ..." / "cc bayar pdam ..." means purchase using credit card. |
| 2436 | if (typeof isCreditCardPurchaseText_ === 'function' && isCreditCardPurchaseText_(t)) return 'Credit Card'; |
| 2444 | if (/\b(tokopedia\s*cc\|tokopedia\s*card\|credit\s*card\|kartu\s*kredit\|\bcc\b)\b/i.test(t)) return 'Credit Card'; |
| 2466 | if (isBorrowInText_(t) \|\| isDebtPaymentText_(t)) return 'Hutang'; |
| 2471 | if (/\b(cicilan rumah\|kpr\|angsuran rumah)\b/i.test(t)) return 'Cicilan Rumah'; |
| 2472 | if (/\b(hutang\|utang)\b/i.test(t)) return 'Hutang'; |
| 2473 | if (/\b(nabung\|tabung\|saving\|aset\|investasi\|emas\|gold)\b/i.test(t)) return 'Aset'; |
| 2518 | if (isCreditCardPurchaseText_(t)) return 'cc_purchase'; |
| 2526 | if (/\b(nabung\|tabung\|saving\|investasi\|aset)\b/i.test(t)) { |
| 2551 | if (/\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text)) return 'gold'; |
| 2552 | if (/\b(nabung\|tabung\|saving\|savings\|dana darurat\|investasi\|aset)\b/i.test(text)) return 'savings'; |
| 2622 | * Process Review Queue rows that have been manually marked approved/edited. |
| 2625 | * - Edit row in 🧾 Review Queue |
| 2627 | * - Run processReviewQueueApproved() |
| 2634 | function processReviewQueueApproved() { |
| 2727 | const result = writeRouted_(ss, plannedTab, parsed, rawText, stagingResult); |
| 2755 | function processReviewQueueApprovedOnEdit(e) { |
| 2756 | processReviewQueueApproved(); |
| 2763 | if (t.getHandlerFunction && t.getHandlerFunction() === 'processReviewQueueApprovedOnEdit') { |
| 2769 | .newTrigger('processReviewQueueApprovedOnEdit') |
| 2776 | trigger: 'processReviewQueueApprovedOnEdit' |
| 2787 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) \|\| parsed.category === 'Cicilan Rumah') { |
| 2791 | if (/\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| parsed.category === 'Hutang') { |
| 2792 | return AIRO_CONFIG.tabs.hutang; |
| 2795 | if (/\b(nabung\|tabung\|saving\|savings\|aset\|investasi\|emas\|gold\|dana darurat)\b/i.test(text) \|\| parsed.category === 'Aset') { |
| 2796 | return AIRO_CONFIG.tabs.aset; |
| 2983 | `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`; |
| 2986 | `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`; |
| 2989 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2992 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 2998 | `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`; |
| 3207 | * Sync current gold price from Script Properties to the Aset sheet. |
| 3212 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3239 | * 3. Write price to Aset!F12 |
| 3280 | writes_to: '🥇 Aset!F12' |
| 3387 | // A gold_event_id |
| 3400 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 3439 | const hasGoldEvent = normalized.includes('gold_event_id'); |
| 3462 | gold_event_id: ['gold_event_id', 'event_id', 'id'], |
| 3487 | const isGoldAsset = /\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text); |
| 3598 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3615 | const isGoldRow = eventId.startsWith('tg:') \|\| rawText.includes('aset emas') \|\| rawText.includes('emas'); |
| 3649 | normalized.includes('gold_event_id') && |
| 3695 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3811 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 3812 | getSheetLoose_(ss, 'Aset'); |
| 3826 | const helper = setupAsetNetWorthHelpers_(asset); |
| 3836 | function setupAsetNetWorthHelpers_(asset) { |
| 3870 | // Hide helper columns if possible so Aset stays clean. |
| 3904 | getSheetLoose_(ss, 'Credit Card'); |
| 4122 | getSheetLoose_(ss, 'Credit Card'); |
| 4205 | dashboard.getRange('B25').setValue('💳 CREDIT CARD — TOKOPEDIA CC'); |
| 4296 | dashboard.getRange('B17:C17').merge().setValue('Total Aset Likuid'); |
| 4297 | dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`); |
| 4299 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4300 | dashboard.getRange('D18').setFormula(`=IFERROR('🥇 Aset'!F18;0)`); |
| 4306 | dashboard.getRange('D20').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4313 | dashboard.getRange('G17').setFormula(`=IFERROR('🥇 Aset'!AB17;0)`); |
| 4316 | dashboard.getRange('G18').setFormula(`=IFERROR('🥇 Aset'!AB18;0)`); |
| 4319 | dashboard.getRange('G19').setFormula(`=IFERROR('🥇 Aset'!AB19;0)`); |
| 4322 | dashboard.getRange('G20').setFormula(`=IFERROR('🥇 Aset'!AB20;0)`); |
| 4325 | dashboard.getRange('G21').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4384 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 4385 | getSheetLoose_(ss, 'Aset'); |
| 4393 | // Remove visible duplicate panels from Aset only. |
| 4473 | 'Credit Card', |
| 4475 | 'Hutang', |
| 4477 | 'Review Queue', |
| 4533 | '✅ Tanggal dan merchant Credit Card dirapikan.\n\n' + |
| 4558 | '✅ Kolom Credit Card dirapikan.\n\n' + |
| 4578 | sendTelegram_(chatId, 'Cicilan Rumah audit gagal: sheet Cicilan Rumah tidak ditemukan.'); |
| 4619 | 'Cicilan Rumah audit gagal: header payment history tidak ditemukan.\n\n' + |
| 4708 | 'Cicilan Rumah runtime audit selesai.\n\n' + |
| 4818 | 'Credit Card tab cycle header direfresh.\n\n' + |
| 4824 | (link ? 'Buka Credit Card: ' + link : '') |
| 4841 | 'Credit Card Dashboard cycle panel direfresh.\n\n' + |
| 4865 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: tab Credit Card tidak ditemukan.'); |
| 4876 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: header Credit Card tidak ditemukan.'); |
| 4958 | 'Credit Card cycle audit selesai.\n\n' + |
| 4979 | 'Credit Card cycle audit error.\n\n' + |
| 5222 | const accountSourceCol = findColumn_(accountInfo, ['source_tab', 'source'], 11); |
| 5281 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5283 | 'Cash Ledger inflows recent/top:\n' + |
| 5288 | 'Buka Account Ledger: ' + link |
| 5457 | 'Cash Ledger in: Rp' + cashIn + '\n' + |
| 5458 | 'Cash Ledger out: Rp' + cashOut + '\n' + |
| 5459 | 'Cash Ledger net: Rp' + cashNet + '\n\n' + |
| 5460 | 'Account Ledger Cash in: Rp' + accountIn + '\n' + |
| 5461 | 'Account Ledger Cash out: Rp' + accountOut + '\n' + |
| 5462 | 'Account Ledger Cash net: Rp' + accountNet + '\n\n' + |
| 5465 | 'Buka Account Ledger: ' + link |
| 5513 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5514 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5516 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5524 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5525 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5527 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5562 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 5583 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5584 | getSheetLoose_(ss, 'Aset'); |
| 5658 | * Hide legacy net worth block in 🥇 Aset. |
| 5661 | function hideLegacyAsetNetWorthPanel() { |
| 5664 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5665 | getSheetLoose_(ss, 'Aset'); |
| 5672 | // row 16-21 contains old ESTIMASI NET WORTH that still subtracts cicilan rumah. |
| 5679 | note: 'Legacy Aset Net Worth hidden. Use Dashboard Net Worth panel as source of truth.' |
| 5683 | function showLegacyAsetNetWorthPanel() { |
| 5686 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5687 | getSheetLoose_(ss, 'Aset'); |
| 5819 | /^bayar\s+tagihan\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t) |
| 5829 | /\b(pinjam\|dipinjamkan\|minjem\|hutang ke saya\|utang ke saya\|dipinjami)\b/i.test(t) \|\| |
| 5830 | /\b(dapat\|terima)\s+(pinjaman\|hutang\|utang)\b/i.test(t) |
| 5837 | return /\b(bayar\|lunasi\|nyicil\|cicil)\b.*\b(hutang\|utang\|pinjaman)\b/i.test(t); |
| 5916 | function isCreditCardPurchaseText_(text) { |
| 5930 | return /\b(refund\|pengembalian\|dikembalikan\|retur)\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i |
| 5939 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5950 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5965 | function writeHutangSafely_(ss, parsed, rawText, common) { |
| 5966 | const tabName = AIRO_CONFIG.tabs.hutang; |
| 5970 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5973 | issue_reason: 'hutang_tab_missing' |
| 5979 | // "mamak bayar hutang ke saya" is receivable/piutang, not current personal debt payment. |
| 5980 | if (/\bbayar\b.*\b(hutang\|utang)\b.*\bke saya\b/i.test(text)) { |
| 5981 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 5985 | issue_reason: 'orang_bayar_hutang_ke_saya_needs_piutang_flow' |
| 5997 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6000 | issue_reason: 'hutang_intent_unclear' |
| 6172 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6185 | cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6192 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6222 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6240 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6277 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6287 | category: parsed.category \|\| 'Credit Card Payment', |
| 6292 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 6322 | function findHutangMasterHeader_(sheet) { |
| 6330 | normalized.includes('hutang_id') && |
| 6345 | function findHutangPaymentHeader_(sheet) { |
| 6354 | normalized.includes('hutang_id') && |
| 6368 | function hutangColMap_(headers) { |
| 6390 | let m = text.match(/\bbayar\s+(?:hutang\|utang)\s+ke\s+(.+?)\s+\d/i); |
| 6400 | const map = hutangColMap_(masterHeader.headers); |
| 6426 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6427 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6430 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6433 | issue_reason: 'hutang_header_missing' |
| 6441 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6444 | issue_reason: 'hutang_payment_person_or_amount_missing' |
| 6451 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6454 | issue_reason: 'hutang_person_not_found_in_master' |
| 6459 | const hutangId = map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : ''; |
| 6467 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6471 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6472 | hutang_id: hutangId, |
| 6483 | category: parsed.category \|\| 'Hutang', |
| 6488 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 6490 | writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.hutang); |
| 6503 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6504 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6507 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6510 | issue_reason: 'hutang_header_missing' |
| 6518 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6521 | issue_reason: 'hutang_increase_person_or_amount_missing' |
| 6528 | return appendByHeader_(ss, AIRO_CONFIG.tabs.review, { |
| 6531 | issue_reason: 'hutang_person_not_found_in_master' |
| 6542 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6546 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6547 | hutang_id: map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : '', |
| 6566 | const map = hutangColMap_(paymentHeader.headers); |
| 6879 | * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger. |
| 6889 | throw new Error('Cash Ledger sheet not found'); |
| 6894 | throw new Error('Failed to ensure Account Ledger sheet exists'); |
| 6899 | throw new Error('Header not found in Cash Ledger'); |
| 6904 | throw new Error('Header not found in Account Ledger'); |
| 6910 | // Validate required fields in Cash Ledger |
| 6929 | throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)'); |
| 6932 | // Validate required fields in Account Ledger |
| 6950 | throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)'); |
| 6953 | // Read Cash Ledger rows |
| 6973 | var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders); |
| 6997 | // Read Account Ledger rows for dedup |
| 7023 | var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders); |
| 7035 | var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders); |
| 7054 | // Construct new row object for Account Ledger |
| 7097 | source_tab: AIRO_CONFIG.tabs.cash, |
| 7098 | linked_txn_id: getFieldValue_(cashRow, 'linked_txn_id', cashHeaders) \|\| '', |
| 7102 | var result = appendByHeader_(ss, AIRO_CONFIG.tabs.accountLedger, row, { createIfMissing: false }); |
| 7188 | * Audit function for Account Ledger to identify missing source_tab, cash backfill rows, and duplicate candidates. |
| 7197 | throw new Error('Account Ledger sheet not found'); |
| 7202 | throw new Error('Header not found in Account Ledger'); |
| 7231 | var sourceTabVal = String(rowObj['source_tab'] \|\| '').trim(); |
| 7235 | // Check empty source_tab |
| 7308 | * Safe, specific manual cleanup function for duplicate rows and blank source_tab in Account Ledger. |
| 7316 | throw new Error('Account Ledger sheet not found'); |
| 7321 | throw new Error('Header not found in Account Ledger'); |
| 7386 | // Find column index of source_tab |
| 7389 | if (canonicalKey_(headers[c]) === 'source_tab') { |
| 7396 | throw new Error('Could not find column index of source_tab'); |
| 7399 | // Repair missing source_tab values for remaining rows |
| 7464 | * Writes an internal transfer to the Account Ledger as two separate entries (outflow and inflow) |
| 7465 | * and synchronizes with the Cash Ledger compatibility layer if one of the accounts is Cash. |
| 7468 | var sharedTxnId = (common && (common.linked_txn_id \|\| common.rowId)) \|\| makeTxnId_({}, rawText); |
| 7480 | linked_txn_id: sharedTxnId + ':in' |
| 7494 | linked_txn_id: sharedTxnId + ':out' |
| 7498 | // Cash Ledger compatibility layer synchronization |

## 13. Next Micro-Step

Recommended next command:

- add test-only Finance Events schema contract
- run Sprint 3 Cash Ledger regressions
- run Sprint 2 domain baselines
- run Sprint 1 Account Ledger baselines
- run Apps Script syntax check
- commit the smallest test-only patch
