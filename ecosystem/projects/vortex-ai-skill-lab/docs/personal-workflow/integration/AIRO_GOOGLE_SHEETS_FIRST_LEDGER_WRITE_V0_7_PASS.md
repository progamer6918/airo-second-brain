# AIRO Google Sheets First Ledger Write v0.7 PASS

Status: PASS
Date: 2026-05-10
Function: airoFinanceFirstLedgerWriteV07

## Observed Apps Script log

- AIRO_FIRST_LEDGER_WRITE_V07=PASS
- google_write_performed=true
- finance_ledger_write_performed=true
- write_scope=transactions_only
- transaction_id=trx_29f527902571
- duplicate_key=transactions:trx_29f527902571
- run_id=first_ledger_write_v0_7_20260510_090316_5a1099

## Result

The first real finance ledger row was written to:

- 💸 Transactions

An audit row was written to:

- 🔄 Sync Log

## Scope confirmation

Written:

- 💸 Transactions: 1 row
- 🔄 Sync Log: 1 audit row

Not written:

- 💳 Credit Card
- 🧾 Review Queue
- 💵 Cash Ledger
- 🏠 Cicilan Rumah
- 🤝 Hutang
- 🥇 Aset
- 📅 Monthly Review

## Transaction

- transaction_id: trx_29f527902571
- duplicate_key: transactions:trx_29f527902571
- amount: 12000
- category: Makan
- account: BLU BCA
- source: telegram

## Next verification

Run sheet key exporter and write_preview again.

Expected:

- transactions:trx_29f527902571 appears in 💸 Transactions sheet keys
- write_preview changes from insert_candidate to skip_duplicate for this duplicate_key
