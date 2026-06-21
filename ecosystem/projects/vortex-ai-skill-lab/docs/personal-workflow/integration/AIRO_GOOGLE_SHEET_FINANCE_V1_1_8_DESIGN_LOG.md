# AIRO Google Sheet Finance v1.1.8 Design Log

Status: FINAL DESIGN DRAFT / READY FOR SYNC DESIGN
Final design version: Balanced+ v1.1.8-final
Date: 2026-05-10
Project: Airo Personal Workflow / Telegram Finance → Google Sheet Finance Design
Repo: progamer6918/vortex-ai-skill-lab
Branch: main

## 1. Context

Airo Personal Workflow is stable through Phase 8. Telegram finance captures no longer default to Notion Recent Captures. Finance intents are routed to Airo Personal Workflow and are persisted locally in SQLite before any future Google Sheets sync.

Current local staging/source DB:

- /home/egitaristorandas/.local/share/airo-personal-workflow/airo.sqlite3

Known relevant DB tables from previous context:

- accounts
- approval_queue
- attachments
- audit_log
- conflicts
- installment_payments
- installments
- sync_jobs
- transactions

Google Sheet Finance is designed as the human-facing finance cockpit, ledger, review surface, and reporting/sync output layer. Local SQLite remains the staging/source layer.

## 2. Major design decision

Final chosen design:

Balanced+ 11 tabs, automation-ready, finance-app-style dashboard.

Tabs:

1. 🏠 Dashboard
2. 💸 Transactions
3. 💵 Cash Ledger
4. 💳 Credit Card
5. 🏠 Cicilan Rumah
6. 🤝 Hutang
7. 🥇 Aset
8. 📅 Monthly Review
9. 🧾 Review Queue
10. ⚙️ Settings
11. 🔄 Sync Log

Rationale:

- Cash needs a focused ledger because cash spending is hard to monitor from bank mutations.
- Credit card needs its own workflow because Tokopedia Credit Card spending must also track transfer/allocation to BLU BCA pocket "Bayaran Kartu Kredit".
- Cicilan rumah needs progress tracking, due date, and payment history.
- Hutang needs per-person principal, repayment history, and remaining balance.
- Aset needs tabungan, gold in grams, and net worth estimate.
- Review Queue is required as a parser ambiguity guardrail.
- Sync Log is required for observability and duplicate/debug handling.

## 3. User-specific finance configuration

Accounts/payment methods:

- BCA
- BLU BCA
- Tokopedia Credit Card
- Mandiri
- GoPay
- ShopeePay
- Cash

Credit card:

- Tokopedia Credit Card
- Track what the CC spending was for and through which app/merchant.
- Track whether money has already been moved to BLU BCA pocket "Bayaran Kartu Kredit".
- Pocket allocation reduces "CC belum transfer ke BLU" indicator.
- CC pocket transfer is not an expense. It is an internal allocation for repayment readiness.

Cicilan rumah:

- Total tenor: 120
- Current known paid status as of May 2026: 53 / 120
- Standard installment: Rp 1.543.000
- User usually pays: Rp 1.570.000
- Due date: every month on date 7
- Sheet tracks payment history and progress.
- "Sisa Cicilan" in Aset is an estimated remaining cashflow obligation: (120 - last_paid_count) × standard installment.
- It is not bank outstanding principal.

Hutang active initial rows:

- HT-001 Mamak Egit: Rp 15.000.000
- HT-002 Bapak Egit: Rp 5.000.000
- HT-003 Mamak Nurul: Rp 5.000.000

Total initial hutang aktif: Rp 25.000.000

Common categories/subcategories:

- Makan: Makan Siang, Makan Malam, Jajan, Snack
- Transport: Bensin, Servis Motor, Parkir
- Tagihan: WiFi, PDAM, Token Listrik
- Digital: Kuota Internet, Streaming, Langganan
- Belanja: Belanja Umum, Galon Air, Rumah Tangga
- CC Payment: Transfer ke BLU, Bayar CC
- Cicilan: Cicilan Rumah
- Hutang: Bayar Hutang
- Aset: Beli Emas
- Tabungan
- Lainnya

## 4. Dashboard design

Dashboard is the command center. It is not the primary input surface.

Dashboard sections:

- Saldo Akun:
  - BCA
  - BLU BCA
  - Mandiri
  - GoPay
  - ShopeePay
  - Cash

- Alert & Reminder:
  - CC belum transfer ke BLU
  - Cicilan due
  - Total hutang aktif

- Snapshot Bulan Ini:
  - Total Masuk
  - Total Keluar
  - Net Bulan Ini

- Status Domain Keuangan:
  - Cicilan Rumah
  - Total Hutang
  - Aset Emas
  - Cash Aktif
  - CC Outstanding
  - Review Pending

Dashboard reads from source tabs. It should not be manually edited except layout/formatting.

## 5. Transactions design

Transactions is the main digital/non-cash transaction ledger.

Core columns:

- transaction_id
- date
- month
- type
- category
- subcategory
- description
- merchant
- amount
- account
- source
- status
- confidence
- raw_text
- synced_at
- notes
- currency
- review_status
- local_db_table
- local_db_rowid
- sync_hash
- duplicate_key
- created_at
- updated_at
- from_account
- to_account
- transfer_purpose
- asset_bucket
- pocket_name
- cashflow_treatment

Important transfer design:

- Transfer to savings is not income and not expense.
- Transfer to pocket "Bayaran Kartu Kredit" is internal allocation, not expense.
- Buying gold is asset conversion / asset purchase and should update both Transactions and Gold Ledger.
- Cash withdrawal/deposit should be routed carefully so it does not become duplicate spending.

## 6. Cash Ledger design

Cash is intentionally separated from digital transactions.

Cash has two sections:

Cash Sessions:

- session_id
- date_start
- amount_start
- date_end
- amount_remaining
- days_lasted
- status
- notes

Cash Transactions:

- entry_id
- session_id
- date
- type
- category
- description
- amount_out
- amount_in
- balance
- source
- notes

Example final behavior:

Input:
"saya hari ini pegang cash 100rb"

Expected:

- New cash session with amount_start 100000
- status active
- Dashboard Cash Aktif updates

Input:
"hari ini cash kepake beli makan 20rb"

Expected:

- New cash transaction under active session
- amount_out 20000
- category Makan
- running cash balance decreases

## 7. Credit Card design

Credit Card tab focuses on Tokopedia Credit Card and BLU BCA pocket readiness.

Columns:

- cc_entry_id
- date
- merchant_app
- amount
- description
- status_pocket_blu
- transferred_at
- linked_txn_id
- notes

Summary:

- Bulan
- Total Belanja CC
- Sudah Transfer BLU
- Sisa Belum Transfer

Example:

Input:
"Catat ini: beli makan 50k pakai tokopedia credit card"

Expected:

- Transactions row: expense, Makan, Rp 50.000, account Tokopedia CC
- Credit Card row: amount Rp 50.000, status_pocket_blu = Belum
- Dashboard CC belum transfer increases

## 8. Cicilan Rumah design

Cicilan Rumah tracks progress and history.

Fixed info:

- tanggal mulai cicilan: user fills later
- total cicilan: 120
- nominal standar: 1543000
- nominal dibayar: 1570000
- due date: 7
- current known payment: 53 / 120

Payment history columns:

- payment_id
- cicilan_ke
- date_paid
- amount_paid
- status
- notes

Example:

Input:
"hari ini sudah bayar cicilan rumah"

Expected:

- Add next payment row
- increment cicilan_ke from last payment
- default amount may use 1570000 unless user specifies different amount
- Dashboard updates progress

## 9. Hutang design

Hutang tracks debt owed by the user to people.

Master columns:

- hutang_id
- nama
- keterangan
- jumlah_pokok
- total_dibayar
- sisa_hutang
- status
- notes

Payment history:

- pay_id
- hutang_id
- nama
- date
- amount
- sisa_setelah
- source
- notes

Example:

Input:
"hari ini bayar hutang ke mamak egit 1 juta"

Expected:

- Add payment history row for HT-001
- Reduce Mamak Egit remaining balance
- Optional Transactions row with type transfer/debt_payment depending sync mapping

## 10. Aset design

Aset uses a hybrid model:

- Tabungan summary with manual opening/reconciliation balance
- Savings / Transfer Ledger for automation
- Gold Summary + Gold Ledger
- Net Worth estimate

### 10.1 Tabungan per Akun

Columns:

- akun
- jenis
- saldo_terakhir_auto
- updated_at
- notes
- opening_or_manual_balance
- savings_in
- savings_out
- balance_source

Rule:

saldo_terakhir_auto = opening_or_manual_balance + savings_in - savings_out

Manual input should go into opening_or_manual_balance, not saldo_terakhir_auto.

### 10.2 Savings / Transfer Ledger

Columns:

- savings_event_id
- date
- type
- from_account
- to_account
- purpose
- amount
- source
- raw_text
- linked_transaction_id
- sync_hash
- notes

Example:

Input:
"tf 5 juta dari BCA ke BLU BCA tabungan"

Expected:

- type = internal_transfer or savings_deposit
- from_account = BCA
- to_account = BLU BCA
- purpose = general_savings
- amount = 5000000
- Monthly expense does not increase
- Dashboard balances update

Example:

Input:
"tf 500 ribu ke pocket Bayaran Kartu Kredit dari BCA"

Expected:

- type = cc_pocket_allocation
- from_account = BCA
- to_account = Bayaran Kartu Kredit
- purpose = cc_payment_pocket
- amount = 500000
- Reduce CC unpaid allocation indicator later

### 10.3 Gold design

Gold must be tracked primarily by grams, with rupiah valuation.

Gold Summary:

- Total Gram
- Total Modal Beli
- Harga Emas Sekarang
- Nilai Emas Saat Ini
- Floating P/L
- Avg Cost / Gram

Gold Ledger columns:

- gold_event_id
- date
- action
- grams_in
- grams_out
- price_per_gram
- fee
- total_amount
- source_account
- source
- raw_text
- sync_hash
- notes

Rule:

- Quantity ledger = gram
- Valuation ledger = rupiah
- Current value = total_grams × current_gold_price
- Floating P/L = current_value - total_cost_basis

Example:

Input:
"hari ini beli emas 1 gram harga 1.350.000 pakai BCA"

Expected:

- Gold Ledger row: action buy, grams_in 1, price_per_gram 1350000
- Transactions row: asset purchase / asset conversion
- Aset summary updates total grams and value

Gold sell method recommendation for future:

- Use average cost first for personal finance simplicity.
- FIFO can be added later if required.

## 11. Review Queue design

Low-confidence or ambiguous parser output should go to Review Queue.

Columns:

- queue_id
- created_at
- source
- raw_text
- parsed_type
- parsed_category
- parsed_subcategory
- parsed_amount
- parsed_currency
- parsed_account
- parser_confidence
- issue_reason
- suggested_fix
- review_status
- reviewed_at
- approved_transaction_id
- local_db_table
- local_db_rowid
- sync_hash
- notes

Rule:

- High confidence: sync to final ledger
- Low confidence: sync to Review Queue
- Ambiguous "nabung 5 juta" without from/to account should go to Review Queue
- Ambiguous payment method should go to Review Queue

## 12. Monthly Review

Monthly Review is formula-driven. It reads:

- Transactions
- Cash Ledger
- Credit Card
- Hutang
- Cicilan Rumah
- Aset summary

Core output:

- total income
- total expense
- net month
- breakdown by category
- cash summary
- CC summary
- hutang/cicilan summary

## 13. Sync Log

Sync Log is technical and may be hidden by default.

Columns:

- sync_id
- run_id
- source_db
- source_table
- source_rowid
- target_tab
- transaction_id
- action
- status
- records_seen
- records_inserted
- records_updated
- records_skipped
- records_failed
- error_message
- started_at
- finished_at
- synced_at
- notes

Sync Log is required for debugging, duplicate prevention, and auditability.

## 14. Safety / guardrails

Active guardrails:

- Do not read token, .env, credentials, OAuth secret/client, private key, cookies, sessions, or browser profile.
- Do not commit local DB, receipt files, runtime state, credentials, OAuth token/client, or secret files.
- Do not touch EarnsAI, runtime, or trading.
- Do not enable live trading.
- Do not hard-delete finance records.
- Do not perform real Google write without explicit approval gate.
- Do not patch/restart OpenClaw service without explicit approval.
- Keep SQLite as local staging/source.
- Google Sheets is reporting/sync/human-facing layer.
- Use Review Queue for ambiguity.
- Use Sync Log for observability.
- Use transaction_id + sync_hash for deduplication.

## 15. Final Apps Script status

A final, ramped-down single Apps Script version is defined as:

- Airo Personal Finance Google Sheets Setup Script
- Version: v1.1.8-final
- Main function: setupAiroFinance
- Builds Balanced+ 11 tabs directly
- Replaces patch chain v1.0 → v1.1.8
- Must be pasted into Apps Script manually unless later stored in repo as a separate script artifact

User preference from latest turn:

- Do not require downloading helper files for GitHub records.
- Use commands to write documentation into repo.
- Apps Script final can be handled separately from the GitHub docs command.

## 16. Official next action

Next item after this GitHub documentation record:

Design SQLite → Google Sheets sync dry-run.

The sync design must come before implementation and must include:

- DB schema discovery command, safe and redacted
- table-to-tab mapping
- row routing rules
- deduplication strategy
- dry-run report
- explicit approval gate before real Google write
- no secret read
- no DB commit
- no service restart
