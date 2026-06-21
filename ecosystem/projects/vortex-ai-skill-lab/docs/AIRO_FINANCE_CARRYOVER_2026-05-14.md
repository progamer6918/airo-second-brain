# AIRO Finance Carry-Over — 2026-05-14

## Repo
~/vortex-ai-skill-lab

## New Chat Rules
- Jangan mulai dari nol.
- Jangan mengarang status project.
- Baca handoff/carryover repo dulu.
- Jangan minta token, secret, .env, API key, private key, cookie, session, atau credential.
- Fokus personal finance, Telegram bot, Apps Script, Google Sheet.
- Jangan aktifkan live trading/private exchange API/real-money trading.
- Jawab step-by-step, padat, jangan lompat.
- Kalau kasih command, buat copy-paste safe.
- Jangan minta output panjang.
- Untuk test pakai format ringkas:
  case | planned | written | category | account | amount | status

## Files to Read First
1. docs/AIRO_FINANCE_HANDOFF_2026-05-13.md
2. docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md
3. scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs
4. apps-script-live/AIRO_Finance_Multitab_Final_v1.js jika ada

## Current Architecture
Telegram Bot -> Cloudflare Worker -> Apps Script standalone -> Google Sheet -> Telegram reply

Worker:
https://airo-finance-telegram-proxy.progamer6918.workers.dev

Deploy Apps Script dari terminal:
scripts/personal-workflow/airo_apps_script_deploy.sh

Manual deploy UI tidak perlu kecuali deployment ID berubah.

## Validated So Far
- Multi-tab routing jalan.
- n8n_Transactions legacy removed.
- Airo_Schema_Audit legacy removed.
- Cash umum dan cash bensin jalan.
- Cash inflow phrases: cash masuk, cash terima, dapat cash, uang masuk cash.
- Gold buy/sell jalan.
- Harga Antam harian intended.
- Dashboard Net Worth sudah jadi source of truth.
- Aset legacy Net Worth bukan source of truth.
- Telegram duplicate retry guard sudah dipatch.
- CLI deploy sudah jalan.

## Credit Card Rules
CC purchase/spending:
- "cc beli ..."
- "cc bayar pdam ..."
- "cc pesan ..."
Efek:
- row belanja CC baru
- menambah Total Belanja CC
- status awal: ⏳ Belum
- menambah Sisa Belum Transfer

CC payment/transfer ke Pocket BLU:
- "bayar cc tisu ..."
- "bayar cc pdam ..."
Efek:
- tidak membuat row belanja baru
- match item CC lama by amount + keyword
- update status_pocket_blu jadi ✅ Sudah
- isi transferred_at
- menambah Sudah Transfer BLU
- mengurangi Sisa Belum Transfer

Dropdown status CC harus:
- ✅ Sudah
- ⏳ Belum
- ⚠️ Sebagian

Kolom CC diminta:
amount | status_pocket_blu | description

merchant_app CC harus satu kata setelah "cc beli/bayar/pesan":
- cc beli shopeefood pisang 26rb -> Shopeefood
- cc bayar pdam 62rb -> PDAM
- cc pesan grabcar 7rb -> Grabcar

Periode CC saat ini:
16 bulan sebelumnya sampai 15 bulan berjalan.
Contoh TOKPED_CC_2026-05 = 16 Apr 2026 sampai 15 Mei 2026.

## Hutang Rules
Contoh:
- bayar hutang ke mamak egit 1,1 jt
- bayar hutang ke bapak egit 350rb

Efek:
- masuk history pembayaran
- match nama di master
- total_dibayar naik
- sisa_hutang turun
- 1,1 jt harus jadi 1.100.000, bukan 11

## Transactions Tab Purpose
Transactions adalah ledger umum bank/e-wallet yang tidak punya tab khusus.

Masuk Transactions:
- bca gaji masuk
- blu beli makan
- bca bayar pdam
- mandiri beli pulsa
- gopay bayar parkir
- refund masuk bca
- reimbursement masuk bca

Tidak masuk Transactions:
- cash/tunai -> Cash Ledger
- cc/bayar cc -> Credit Card
- cicilan rumah/kpr -> Cicilan Rumah
- bayar hutang -> Hutang
- aset/emas/nabung aset -> Aset
- ambiguous -> Review Queue

Kategori boleh sama, tapi tab ditentukan domain/source pembayaran.

## Cash Ledger Concepts
Pocket/session:
session_id, date_start, amount_start, date_end, amount_remaining, days_lasted, status, notes

Transaction ledger:
entry_id, session_id, date, type, category, description, amount_out, amount_in, balance

amount_start = uang awal pocket cash
amount_remaining = sisa cash sekarang
amount_in = cash masuk
amount_out = cash keluar
balance = saldo berjalan, masih perlu audit

User ingin amount_out, amount_in, balance lebih dekat kiri setelah header Cash Ledger diaudit.

## Dashboard Plan
Dashboard finance-app-like boleh dibuat setelah classification stabil.

Hindari double count:
- bayar cc bukan expense baru
- transfer internal bukan expense
- nabung aset/beli emas = asset allocation, bukan konsumsi
- hutang payment = cashflow out/liability reduction, bukan konsumsi biasa

Suggested blocks:
Income Bulan Ini, Spending Bulan Ini, CC Spending, Cash Out, Cicilan Rumah, Bayar Hutang, Asset Allocation, Net Cashflow, Net Worth.

## Pending Before 100% Mature
1. Verifikasi patch terakhir CC merchant/date/dashboard sudah ada dan deployed.
2. Verifikasi CC summary: Total Belanja CC, Sudah Transfer BLU, Sisa Belum Transfer.
3. Verifikasi Hutang master: total_dibayar dan sisa_hutang berubah benar.
4. Test Review Queue ambigu + nominal lalu approved auto-route.
5. Audit Cash Ledger balance dan layout amount_in/out/balance.
6. Buat Dashboard tracker setelah data classification stabil.
7. Bersihkan QA rows.
8. Commit/push setiap milestone stabil.

## New Chat First Commands
Run:
cd ~/vortex-ai-skill-lab && git status --short && git log --oneline -5 && tail -n 220 docs/AIRO_FINANCE_CARRYOVER_2026-05-14.md

Then inspect:
cd ~/vortex-ai-skill-lab/apps-script-live && grep -n "parseCcMerchant_\\|fixDashboardCardsAfterCcCashChanges\\|writeCreditCardSafely_\\|writeHutangSafely_\\|parseAmount_\\|writeRouted_\\|fixCreditCardDateMerchantFromRawText" AIRO_Finance_Multitab_Final_v1.js

## Next Project Pointer — Enhancement Blueprint

Added next project blueprint:
- docs/AIRO_FINANCE_NEXT_PROJECT_2026-05-14.md

Key decisions:
- Use two dashboards first: Dashboard Mutasi BLU and Dashboard Finance.
- PDF mutasi BLU must be processed as preview/staging first, not direct final write.
- Telegram manual input is mainly for Cash Ledger, Credit Card, Cicilan Rumah, Hutang, and Aset.
- Daily BLU transactions are better handled through monthly PDF closing.
- Full collision engine is postponed.
- Possible duplicate/link is preferred over auto-merge.
- /help and /form will be added as separate Telegram commands.
- Category system must be personal and interviewed further, not copied from generic templates.
- Nurul is part of household finance context, not a separate finance category.
