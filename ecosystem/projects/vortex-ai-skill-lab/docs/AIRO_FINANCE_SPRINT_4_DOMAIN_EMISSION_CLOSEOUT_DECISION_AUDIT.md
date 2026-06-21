# AIRO Finance - Sprint 4 Domain Emission Closeout Decision Audit

Status: EXACT AUDIT
Sprint: Sprint 4 - Finance Events
Generated at: 2026-05-24 15:37:44
Runtime scope: Read-only audit / documentation only
Canonical source: docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md

## 1. Purpose

This document audits whether Sprint 4 needs domain-specific Finance Events emission after the first safe emission path was implemented.

No runtime patch is made in this micro-step.

## 2. Current Confirmed Position

- Finance Events schema exists.
- Finance Events tab creation helper exists.
- Finance Events append-only writer exists.
- Generic `writeRouted_` append success path emits one best-effort `transaction_created` event.
- Special domain writer paths are not wired to Finance Events yet.
- No Email Ingestion implementation is present.
- No ledger behavior change is required for this audit.

## 3. Function Surface Map

| Function | Lines | Status | Signals |
|---|---:|---:|---|
| `recordFinanceEventForWriteResult_` | 1816-1844 | FOUND | recordFinanceEventForWriteResult_:1, writeFinanceEvent_:1, event_type:2, event_source:2, transaction_created:1, source_tab:2, source_row:2, linked_txn_id:3 |
| `writeFinanceEvent_` | 1575-1580 | FOUND | writeFinanceEvent_:1, appendByHeader_:1 |
| `appendFinanceEvent_` | 1582-1584 | FOUND | writeFinanceEvent_:1, appendFinanceEvent_:1 |
| `buildFinanceEvent_` | 1554-1573 | FOUND | event_type:2, event_source:2, source_tab:2, source_row:2, linked_txn_id:2 |
| `writeRouted_` | 1846-1896 | FOUND | recordFinanceEventForWriteResult_:1, event_type:1, event_source:1, transaction_created:1, source_tab:1, source_row:1, linked_txn_id:2, Hutang:1, writeAccountLedgerMirror_:2, appendByHeader_:1 |
| `writeAccountLedgerMirror_` | 1639-1693 | FOUND | source_tab:1, linked_txn_id:3, writeAccountLedgerMirror_:1, appendByHeader_:1 |
| `writeInternalTransferToAccountLedger_` | 7609-7672 | FOUND | linked_txn_id:3, Cash Ledger:1, writeAccountLedgerMirror_:2 |
| `writeCreditCardSafely_` | 6076-6105 | FOUND | appendByHeader_:2 |
| `writeHutangSafely_` | 6107-6144 | FOUND | Hutang:1, appendByHeader_:3 |
| `writeAssetSafely_` | 1900-1954 | FOUND | linked_txn_id:2, Aset:1, writeAccountLedgerMirror_:1, appendByHeader_:3 |
| `processReviewQueueApproved` | 2776-2895 | FOUND |  |
| `appendCreditCardPurchase_` | 6310-6356 | FOUND | linked_txn_id:3, appendByHeader_:1 |
| `appendDebtPaymentAndUpdateMaster_` | 6567-6642 | FOUND | linked_txn_id:3, Hutang:3, writeAccountLedgerMirror_:1, appendByHeader_:3 |
| `appendDebtIncreaseAndUpdateMaster_` | 6644-6705 | FOUND | linked_txn_id:1, Hutang:2, appendByHeader_:3 |
| `mirrorAssetPurchaseToAccountLedger_` | 1912-1930 | FOUND | linked_txn_id:2, Aset:1, writeAccountLedgerMirror_:1 |
| `appendGoldAssetRow_` | 3481-3567 | FOUND | linked_txn_id:1 |
| `ensureFinanceEventsSheet_` | 1503-1533 | FOUND |  |
| `writeCashLedgerCompatibility_` | 1586-1595 | FOUND |  |

## 4. Runtime Notes

- Generic writeRouted_ append success path emits one best-effort `transaction_created` Finance Event.
- Emission helper is best-effort and returns the original write result.
- Credit Card domain writer has no direct Finance Events emission yet.
- Hutang domain writer has no direct Finance Events emission yet.
- Aset domain writer has no direct Finance Events emission yet.
- Account Ledger mirror does not directly emit Finance Events yet.
- Review Queue approval path does not directly emit Finance Events yet.
- No Email Ingestion runtime surface detected.
- No sheet deletion or bulk row deletion pattern detected.

## 5. Domain Emission Decision Matrix

| Surface | Direct domain event implemented? | Sprint 4 decision | Reason |
|---|---:|---:|---|
| Generic writeRouted_ append | Implemented | PASS | Already emits best-effort transaction_created event. |
| Credit Card writer | Not implemented | Defer | Specialized writer already has domain tests; direct emission adds risk without closeout need. |
| Hutang writer | Not implemented | Defer | Hutang payment/increase split is sensitive; defer until dedicated event contract. |
| Aset writer | Not implemented | Defer | Aset savings/gold flows are specialized; defer until dedicated event contract. |
| Account Ledger mirror | Not implemented | Defer | Would create high event volume and needs dedupe policy. |
| Internal transfer | Not implemented | Defer | Two-sided events need explicit pair/link policy. |
| Review Queue approval | Not implemented | Defer | Manual approval needs separate event source/replay policy. |
| Cash Ledger compatibility skipped | Not implemented | Defer | Can be added later if needed; Sprint 3 guards already cover skipped writes. |

## 6. Recommendation

Sprint 4 can close after the first safe generic emission path.

Rationale:

- Finance Events infrastructure is now present.
- Append-only writer is guarded.
- One low-risk generic write path emits successfully.
- Domain-specific emitters are not required to prove Sprint 4 viability.
- Direct domain emissions need separate dedupe and event-type policy per domain.
- Account Ledger mirror emissions need volume/dedupe policy.
- Internal transfer emissions need pair/link semantics.
- Review Queue emissions need replay/approval semantics.

Therefore, the safest next step is Sprint 4 closeout audit, not another runtime emission patch.

## 7. Explicitly Deferred Domain Emission Work

Deferred to later micro-sprints:

- Credit Card direct `domain_row_written` event
- Hutang `debt_payment` / `debt_in` domain events
- Aset `asset_purchase` / gold/savings events
- Account Ledger `account_mirror_written` events
- Internal transfer paired events
- Review Queue `review_approved` events
- Cash Ledger `compatibility_skipped` events

## 8. Existing Finance Events Tests

- tests/personal-workflow/test_airo_finance_events_append_writer_contract.py
- tests/personal-workflow/test_airo_finance_events_runtime_schema_contract.py
- tests/personal-workflow/test_airo_finance_events_schema_contract.py
- tests/personal-workflow/test_airo_finance_events_write_routed_emission_contract.py

## 9. Closeout Preconditions

Sprint 4 closeout may proceed if all are true:

- Finance Events schema contract passes
- Finance Events runtime schema contract passes
- Finance Events append writer contract passes
- Finance Events writeRouted emission contract passes
- Sprint 3 Cash Ledger guards pass
- Sprint 2 domain guards pass
- Sprint 1 Account Ledger guards pass
- Apps Script syntax check passes
- no Email Ingestion runtime appears
- no destructive sheet/row deletion appears

## 10. Direct Source Findings

| Line | Source Text |
|---:|---|
| 15 | cash: '💵 Cash Ledger', |
| 16 | creditCard: '💳 Credit Card', |
| 17 | cicilanRumah: '🏠 Cicilan Rumah', |
| 18 | hutang: '🤝 Hutang', |
| 19 | aset: '🥇 Aset', |
| 20 | accountLedger: '📒 Account Ledger', |
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
| 718 | const fallbackResult = writeRouted_( |
| 868 | 'Saya belum mencatat transaksi Aset/Emas ini.' |
| 887 | 'Saya butuh detail orang dan format lengkap untuk Hutang.\n\n' + |
| 890 | '- bayar hutang ke Budi 50000 dari bca' |
| 898 | 'Saya belum mencatat piutang/orang bayar hutang ke saya karena flow piutang belum dikunci.\n\n' + |
| 912 | 'Saya belum mencatat transaksi Hutang ini.\n\n' + |
| 915 | '- bayar hutang ke Budi 50000 dari bca' |
| 1069 | 'D. Credit Card\n' + |
| 1399 | const routedResult = writeRouted_(ss, finalTab, parsed, effectiveRawText, stagingResult); |
| 1487 | 'event_type', |
| 1488 | 'event_source', |
| 1489 | 'source_tab', |
| 1490 | 'source_row', |
| 1491 | 'linked_txn_id', |
| 1559 | event_type: event.event_type \|\| 'manual_event', |
| 1560 | event_source: event.event_source \|\| 'system', |
| 1561 | source_tab: event.source_tab \|\| '', |
| 1562 | source_row: event.source_row \|\| '', |
| 1563 | linked_txn_id: event.linked_txn_id \|\| event.entry_id \|\| '', |
| 1575 | function writeFinanceEvent_(ss, event) { |
| 1582 | function appendFinanceEvent_(ss, event) { |
| 1583 | return writeFinanceEvent_(ss, event); |
| 1604 | const entryId = common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1636 | * Mirrors cash movement to the Account Ledger tab. |
| 1639 | function writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab) { |
| 1640 | const entryId = common.rowId \|\| common.linked_txn_id \|\| makeTxnId_({}, rawText); |
| 1672 | source_tab: sourceTab, |
| 1673 | linked_txn_id: common.linked_txn_id \|\| entryId, |
| 1696 | * Ensures the 📒 Account Ledger tab exists with the correct headers. |
| 1704 | 'source_tab', 'linked_txn_id', 'notes' |
| 1816 | function recordFinanceEventForWriteResult_(ss, result, common, parsed, rawText, event) { |
| 1821 | writeFinanceEvent_(ss, { |
| 1822 | event_type: event.event_type \|\| 'transaction_created', |
| 1823 | event_source: event.event_source \|\| 'telegram', |
| 1824 | source_tab: event.source_tab \|\| result.writtenTab \|\| '', |
| 1825 | source_row: event.source_row \|\| result.row \|\| '', |
| 1826 | linked_txn_id: event.linked_txn_id \|\| common.linked_txn_id \|\| common.rowId \|\| result.rowId \|\| '', |
| 1846 | function writeRouted_(ss, plannedTab, parsed, rawText, common) { |
| 1850 | if (key.includes('credit card')) { |
| 1851 | return writeCreditCardSafely_(ss, parsed, rawText, common); |
| 1854 | if (key.includes('hutang')) { |
| 1855 | return writeHutangSafely_(ss, parsed, rawText, common); |
| 1858 | if (key.includes('aset')) { |
| 1859 | return writeAssetSafely_(ss, parsed, rawText, common); |
| 1864 | return writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer); |
| 1867 | if (key.includes('cash ledger')) { |
| 1870 | writeAccountLedgerMirror_(ss, parsed, rawText, common, AIRO_CONFIG.tabs.cash); |
| 1877 | const result = writeAccountLedgerMirror_(ss, parsed, rawText, common, sourceTab); |
| 1888 | recordFinanceEventForWriteResult_(ss, result, common, parsed, rawText, { |
| 1889 | event_type: 'transaction_created', |
| 1890 | event_source: 'telegram', |
| 1891 | source_tab: result.writtenTab \|\| tabName, |
| 1892 | source_row: result.row \|\| '', |
| 1893 | linked_txn_id: common.linked_txn_id \|\| common.rowId \|\| '' |
| 1900 | function writeAssetSafely_(ss, parsed, rawText, common) { |
| 1901 | const tabName = AIRO_CONFIG.tabs.aset; |
| 1912 | function mirrorAssetPurchaseToAccountLedger_(result) { |
| 1917 | category: parsed.category \|\| 'Aset', |
| 1922 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 1924 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.aset); |
| 1934 | return mirrorAssetPurchaseToAccountLedger_(appendGoldAssetRow_(sheet, parsed, rawText, common)); |
| 1939 | if (result.status === 'written') return mirrorAssetPurchaseToAccountLedger_({ ...result, writtenTab: tabName }); |
| 1979 | linked_txn_id: data.linked_txn_id, |
| 2069 | // Cash Ledger movement type validation. |
| 2090 | // Review Queue status validation |
| 2269 | return data.entry_id \|\| data.linked_txn_id \|\| ''; |
| 2330 | if (headerKey === 'source_tab' \|\| headerKey.includes('source_tab')) { |
| 2331 | return data.source_tab \|\| data.source \|\| ''; |
| 2386 | type: ['type', 'jenis', 'event_type', 'jenis_transaksi', 'transaction_type'], |
| 2395 | linked_txn_id: ['linked_txn_id', 'linked transaction id', 'transaction_id', 'txn_id', 'linked_id'], |
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
| 2769 | * - Run processReviewQueueApproved() |
| 2776 | function processReviewQueueApproved() { |
| 2869 | const result = writeRouted_(ss, plannedTab, parsed, rawText, stagingResult); |
| 2897 | function processReviewQueueApprovedOnEdit(e) { |
| 2898 | processReviewQueueApproved(); |
| 2905 | if (t.getHandlerFunction && t.getHandlerFunction() === 'processReviewQueueApprovedOnEdit') { |
| 2911 | .newTrigger('processReviewQueueApprovedOnEdit') |
| 2918 | trigger: 'processReviewQueueApprovedOnEdit' |
| 2929 | if (/\b(cicilan rumah\|kpr\|angsuran rumah\|bayar rumah)\b/i.test(text) \|\| parsed.category === 'Cicilan Rumah') { |
| 2933 | if (/\b(hutang\|utang\|bayar hutang\|bayar utang\|pinjam\|pinjaman)\b/i.test(text) \|\| parsed.category === 'Hutang') { |
| 2934 | return AIRO_CONFIG.tabs.hutang; |
| 2937 | if (/\b(nabung\|tabung\|saving\|savings\|aset\|investasi\|emas\|gold\|dana darurat)\b/i.test(text) \|\| parsed.category === 'Aset') { |
| 2938 | return AIRO_CONFIG.tabs.aset; |
| 3125 | `ARRAYFORMULA(IFERROR(TEXT('📒 Account Ledger'!B:B;"yyyy-mm");LEFT(TO_TEXT('📒 Account Ledger'!B:B);7)))`; |
| 3128 | `REGEXMATCH('📒 Account Ledger'!C:C;"^Cash( Umum\| Bensin)?$")`; |
| 3131 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!D:D;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 3134 | `=IFERROR(SUM(FILTER('📒 Account Ledger'!E:E;${accountLedgerCashAccountFilterFormula};${accountLedgerMonthKeyFormula}=TO_TEXT($B$2)));0)`; |
| 3140 | `=IFERROR("💵 Cash Aktif"&CHAR(10)&TEXT((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin"));"Rp #,##0");"💵 Cash Aktif"&CHAR(10)&"— catat dulu —")`; |
| 3349 | * Sync current gold price from Script Properties to the Aset sheet. |
| 3354 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3381 | * 3. Write price to Aset!F12 |
| 3422 | writes_to: '🥇 Aset!F12' |
| 3542 | common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 3629 | const isGoldAsset = /\b(aset\s+emas\|emas\|gold\|antam\|logam mulia)\b/i.test(text); |
| 3740 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3757 | const isGoldRow = eventId.startsWith('tg:') \|\| rawText.includes('aset emas') \|\| rawText.includes('emas'); |
| 3837 | const sheet = getSheetLoose_(ss, AIRO_CONFIG.tabs.aset); |
| 3953 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 3954 | getSheetLoose_(ss, 'Aset'); |
| 3968 | const helper = setupAsetNetWorthHelpers_(asset); |
| 3978 | function setupAsetNetWorthHelpers_(asset) { |
| 4012 | // Hide helper columns if possible so Aset stays clean. |
| 4046 | getSheetLoose_(ss, 'Credit Card'); |
| 4264 | getSheetLoose_(ss, 'Credit Card'); |
| 4347 | dashboard.getRange('B25').setValue('💳 CREDIT CARD — TOKOPEDIA CC'); |
| 4438 | dashboard.getRange('B17:C17').merge().setValue('Total Aset Likuid'); |
| 4439 | dashboard.getRange('D17').setFormula(`=IFERROR(((SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!D:D;'📒 Account Ledger'!C:C;"Cash Bensin"))-(SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Umum")+SUMIFS('📒 Account Ledger'!E:E;'📒 Account Ledger'!C:C;"Cash Bensin")))+'🥇 Aset'!B17+'🥇 Aset'!B18;0)`); |
| 4441 | dashboard.getRange('B18:C18').merge().setValue('Hutang Non-Rumah'); |
| 4442 | dashboard.getRange('D18').setFormula(`=IFERROR('🥇 Aset'!F18;0)`); |
| 4448 | dashboard.getRange('D20').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4455 | dashboard.getRange('G17').setFormula(`=IFERROR('🥇 Aset'!AB17;0)`); |
| 4458 | dashboard.getRange('G18').setFormula(`=IFERROR('🥇 Aset'!AB18;0)`); |
| 4461 | dashboard.getRange('G19').setFormula(`=IFERROR('🥇 Aset'!AB19;0)`); |
| 4464 | dashboard.getRange('G20').setFormula(`=IFERROR('🥇 Aset'!AB20;0)`); |
| 4467 | dashboard.getRange('G21').setFormula(`=IFERROR('🥇 Aset'!AB21;0)`); |
| 4526 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 4527 | getSheetLoose_(ss, 'Aset'); |
| 4535 | // Remove visible duplicate panels from Aset only. |
| 4615 | 'Credit Card', |
| 4617 | 'Hutang', |
| 4619 | 'Review Queue', |
| 4675 | '✅ Tanggal dan merchant Credit Card dirapikan.\n\n' + |
| 4700 | '✅ Kolom Credit Card dirapikan.\n\n' + |
| 4720 | sendTelegram_(chatId, 'Cicilan Rumah audit gagal: sheet Cicilan Rumah tidak ditemukan.'); |
| 4761 | 'Cicilan Rumah audit gagal: header payment history tidak ditemukan.\n\n' + |
| 4850 | 'Cicilan Rumah runtime audit selesai.\n\n' + |
| 4960 | 'Credit Card tab cycle header direfresh.\n\n' + |
| 4966 | (link ? 'Buka Credit Card: ' + link : '') |
| 4983 | 'Credit Card Dashboard cycle panel direfresh.\n\n' + |
| 5007 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: tab Credit Card tidak ditemukan.'); |
| 5018 | sendTelegram_(chatId, 'Credit Card cycle audit gagal: header Credit Card tidak ditemukan.'); |
| 5100 | 'Credit Card cycle audit selesai.\n\n' + |
| 5121 | 'Credit Card cycle audit error.\n\n' + |
| 5364 | const accountSourceCol = findColumn_(accountInfo, ['source_tab', 'source'], 11); |
| 5423 | 'Account Ledger Cash inflows recent/top:\n' + |
| 5425 | 'Cash Ledger inflows recent/top:\n' + |
| 5430 | 'Buka Account Ledger: ' + link |
| 5599 | 'Cash Ledger in: Rp' + cashIn + '\n' + |
| 5600 | 'Cash Ledger out: Rp' + cashOut + '\n' + |
| 5601 | 'Cash Ledger net: Rp' + cashNet + '\n\n' + |
| 5602 | 'Account Ledger Cash in: Rp' + accountIn + '\n' + |
| 5603 | 'Account Ledger Cash out: Rp' + accountOut + '\n' + |
| 5604 | 'Account Ledger Cash net: Rp' + accountNet + '\n\n' + |
| 5607 | 'Buka Account Ledger: ' + link |
| 5655 | monthly_b6_uses_account_ledger: monthlyB6.indexOf('Account Ledger') >= 0, |
| 5656 | monthly_e6_uses_account_ledger: monthlyE6.indexOf('Account Ledger') >= 0, |
| 5658 | dashboard_d17_uses_account_ledger: dashboardD17.indexOf('Account Ledger') >= 0 |
| 5666 | 'Monthly B6 pakai Account Ledger: ' + result.monthly_b6_uses_account_ledger + '\n' + |
| 5667 | 'Monthly E6 pakai Account Ledger: ' + result.monthly_e6_uses_account_ledger + '\n' + |
| 5669 | 'Dashboard D17 pakai Account Ledger: ' + result.dashboard_d17_uses_account_ledger + '\n\n' + |
| 5704 | 'Monthly Review dan Dashboard sekarang membaca ?? Account Ledger untuk akun Cash.\n\n' + |
| 5725 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5726 | getSheetLoose_(ss, 'Aset'); |
| 5800 | * Hide legacy net worth block in 🥇 Aset. |
| 5803 | function hideLegacyAsetNetWorthPanel() { |
| 5806 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5807 | getSheetLoose_(ss, 'Aset'); |
| 5814 | // row 16-21 contains old ESTIMASI NET WORTH that still subtracts cicilan rumah. |
| 5821 | note: 'Legacy Aset Net Worth hidden. Use Dashboard Net Worth panel as source of truth.' |
| 5825 | function showLegacyAsetNetWorthPanel() { |
| 5828 | getSheetLoose_(ss, AIRO_CONFIG.tabs.aset) \|\| |
| 5829 | getSheetLoose_(ss, 'Aset'); |
| 5961 | /^bayar\s+tagihan\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i.test(t) |
| 5971 | /\b(pinjam\|dipinjamkan\|minjem\|hutang ke saya\|utang ke saya\|dipinjami)\b/i.test(t) \|\| |
| 5972 | /\b(dapat\|terima)\s+(pinjaman\|hutang\|utang)\b/i.test(t) |
| 5979 | return /\b(bayar\|lunasi\|nyicil\|cicil)\b.*\b(hutang\|utang\|pinjaman)\b/i.test(t); |
| 6058 | function isCreditCardPurchaseText_(text) { |
| 6072 | return /\b(refund\|pengembalian\|dikembalikan\|retur)\b.*\b(cc\|credit card\|kartu kredit\|tokopedia cc\|tokopedia card)\b/i |
| 6076 | function writeCreditCardSafely_(ss, parsed, rawText, common) { |
| 6107 | function writeHutangSafely_(ss, parsed, rawText, common) { |
| 6108 | const tabName = AIRO_CONFIG.tabs.hutang; |
| 6115 | issue_reason: 'hutang_tab_missing' |
| 6121 | // "mamak bayar hutang ke saya" is receivable/piutang, not current personal debt payment. |
| 6122 | if (/\bbayar\b.*\b(hutang\|utang)\b.*\bke saya\b/i.test(text)) { |
| 6127 | issue_reason: 'orang_bayar_hutang_ke_saya_needs_piutang_flow' |
| 6142 | issue_reason: 'hutang_intent_unclear' |
| 6327 | cc_entry_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6334 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6429 | category: parsed.category \|\| 'Credit Card Payment', |
| 6434 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 6436 | const accountLedgerResult = writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.creditCard); |
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
| 6613 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6614 | hutang_id: hutangId, |
| 6625 | category: parsed.category \|\| 'Hutang', |
| 6630 | linked_txn_id: common.linked_txn_id \|\| makeTxnId_({}, rawText) |
| 6632 | writeAccountLedgerMirror_(ss, accountParsed, rawText, accountCommon, AIRO_CONFIG.tabs.hutang); |
| 6645 | const masterHeader = findHutangMasterHeader_(sheet); |
| 6646 | const paymentHeader = findHutangPaymentHeader_(sheet); |
| 6652 | issue_reason: 'hutang_header_missing' |
| 6663 | issue_reason: 'hutang_increase_person_or_amount_missing' |
| 6673 | issue_reason: 'hutang_person_not_found_in_master' |
| 6684 | if (map.sisa_hutang) sheet.getRange(master.row, map.sisa_hutang).setValue(sisa); |
| 6688 | pay_id: common.linked_txn_id \|\| makeTxnId_({}, rawText), |
| 6689 | hutang_id: map.hutang_id ? sheet.getRange(master.row, map.hutang_id).getValue() : '', |
| 6708 | const map = hutangColMap_(paymentHeader.headers); |
| 7021 | * Manual backfill function to migrate historical data from 💵 Cash Ledger to 📒 Account Ledger. |
| 7031 | throw new Error('Cash Ledger sheet not found'); |
| 7036 | throw new Error('Failed to ensure Account Ledger sheet exists'); |
| 7041 | throw new Error('Header not found in Cash Ledger'); |
| 7046 | throw new Error('Header not found in Account Ledger'); |
| 7052 | // Validate required fields in Cash Ledger |
| 7071 | throw new Error('Cash Ledger is missing required columns (Date, Account, Amount, or Description)'); |
| 7074 | // Validate required fields in Account Ledger |
| 7092 | throw new Error('Account Ledger is missing required target columns (date, account, amount_in, amount_out, or description)'); |
| 7095 | // Read Cash Ledger rows |
| 7115 | var entryId = getFieldValue_(rowObj, 'entry_id', cashHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', cashHeaders); |
| 7139 | // Read Account Ledger rows for dedup |
| 7165 | var entryId = getFieldValue_(rowObj, 'entry_id', accountHeaders) \|\| getFieldValue_(rowObj, 'linked_txn_id', accountHeaders); |
| 7177 | var cashEntryId = getFieldValue_(cashRow, 'entry_id', cashHeaders) \|\| getFieldValue_(cashRow, 'linked_txn_id', cashHeaders); |
| 7196 | // Construct new row object for Account Ledger |
| 7239 | source_tab: AIRO_CONFIG.tabs.cash, |
| 7240 | linked_txn_id: getFieldValue_(cashRow, 'linked_txn_id', cashHeaders) \|\| '', |
| 7330 | * Audit function for Account Ledger to identify missing source_tab, cash backfill rows, and duplicate candidates. |
| 7339 | throw new Error('Account Ledger sheet not found'); |
| 7344 | throw new Error('Header not found in Account Ledger'); |
| 7373 | var sourceTabVal = String(rowObj['source_tab'] \|\| '').trim(); |
| 7377 | // Check empty source_tab |
| 7450 | * Safe, specific manual cleanup function for duplicate rows and blank source_tab in Account Ledger. |
| 7458 | throw new Error('Account Ledger sheet not found'); |
| 7463 | throw new Error('Header not found in Account Ledger'); |
| 7528 | // Find column index of source_tab |
| 7531 | if (canonicalKey_(headers[c]) === 'source_tab') { |
| 7538 | throw new Error('Could not find column index of source_tab'); |
| 7541 | // Repair missing source_tab values for remaining rows |
| 7606 | * Writes an internal transfer to the Account Ledger as two separate entries (outflow and inflow) |
| 7607 | * and synchronizes with the Cash Ledger compatibility layer if one of the accounts is Cash. |
| 7609 | function writeInternalTransferToAccountLedger_(ss, parsed, rawText, common, transfer) { |
| 7610 | var sharedTxnId = (common && (common.linked_txn_id \|\| common.rowId)) \|\| makeTxnId_({}, rawText); |
| 7622 | linked_txn_id: sharedTxnId + ':in' |
| 7624 | var outResult = writeAccountLedgerMirror_(ss, parsedOut, rawText, commonOut, transfer.sourceAccount); |
| 7636 | linked_txn_id: sharedTxnId + ':out' |
| 7638 | var inResult = writeAccountLedgerMirror_(ss, parsedIn, rawText, commonIn, transfer.targetAccount); |
| 7640 | // Cash Ledger compatibility layer synchronization |

## 11. Next Micro-Step

Recommended next command:

- prepare Sprint 4 closeout audit
- rerun Sprint 4, Sprint 3, Sprint 2, and Sprint 1 regressions
- verify no Email Ingestion or destructive behavior
- create Sprint 4 final PASS doc
