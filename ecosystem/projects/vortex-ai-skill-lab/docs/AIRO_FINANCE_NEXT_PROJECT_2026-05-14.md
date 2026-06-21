# AIRO Finance Next Project Blueprint — 2026-05-14

## Status

Dokumen ini mencatat keputusan brainstorming untuk enhancement AIRO Finance berikutnya.

Mode kerja:
- Safe audit mode.
- Jangan ubah Apps Script.
- Jangan deploy.
- Jangan run script yang menulis ke Google Sheet.
- Jangan matikan/mengubah formula.
- Jangan auto-import PDF ke sheet final.
- Semua perubahan teknis harus dibuat bertahap setelah blueprint disetujui.

## Current Architecture

Arsitektur aktif saat ini:

Telegram Bot -> Cloudflare Worker -> Apps Script standalone -> Google Sheet -> Telegram reply

Worker:
https://airo-finance-telegram-proxy.progamer6918.workers.dev

Deploy Apps Script dari terminal:
scripts/personal-workflow/airo_apps_script_deploy.sh

Manual deploy UI tidak perlu kecuali deployment ID berubah.

## Current Project Boundary

AIRO Finance tetap fokus pada:
- Personal/household finance.
- Telegram bot.
- Apps Script.
- Google Sheet.
- PDF mutasi bank sebagai input closing bulanan.

Tidak boleh:
- Live trading.
- Private exchange API.
- Real-money trading automation.
- Meminta token, secret, .env, API key, private key, cookie, session, credential.

## Key Design Decision

AIRO Finance tidak akan memaksa user untuk chat semua transaksi harian ke Telegram.

Alasan:
- Input harian semua transaksi akan membuat user exhausted.
- Banyak transaksi harian BLU lebih cocok diproses secara batch saat closing bulan.
- Telegram lebih cocok untuk transaksi penting yang perlu kontrol aktif.

## Input Source Policy

### Telegram Manual Input

Telegram dipakai terutama untuk:

1. Cash Ledger
2. Credit Card
3. Cicilan Rumah / KPR
4. Hutang
5. Aset, terutama emas

Telegram tidak wajib dipakai untuk semua transaksi harian seperti QRIS makan, transfer kecil, dan pengeluaran BLU rutin.

### PDF Mutasi BLU

PDF mutasi BLU dipakai untuk:

1. Transactions / mutasi rekening bulanan
2. Closing bulan
3. Raw bank movement
4. Cleaned spending analysis
5. Audit pembanding terhadap data manual Telegram

PDF mutasi BLU tidak boleh langsung menulis ke final tab tanpa preview.

## PDF Processing Decision

Keputusan: B + E

- Dua dashboard dibuat dulu.
- PDF mutasi diproses sebagai preview.
- PDF tidak langsung tulis final ke Google Sheet.
- Collision engine penuh tidak dibuat di awal.

Opsi input PDF yang dipilih untuk tahap awal:
- Opsi A: upload PDF ke ChatGPT untuk dibuat preview CSV/tabel dulu.

Tahap berikutnya setelah pola stabil:
- Bisa naik ke local PDF importer di repo.
- PDF langsung ke Telegram tidak diprioritaskan pada tahap awal karena lebih rawan bug.

## Dashboard Architecture

AIRO Finance akan memakai 2 dashboard besar.

### Dashboard 1 — Dashboard Mutasi BLU

Sumber utama:
- PDF mutasi BLU bulanan.

Fokus:
- Raw movement.
- Cleaned spending.
- Saldo awal dan saldo akhir.
- Total pemasukan statement.
- Total pengeluaran statement.
- Internal transfer.
- Actual expense.
- Pocket movement.
- Possible duplicate/link.

Dashboard ini tidak otomatis mengubah CC, Hutang, Aset, atau Cash Ledger.

### Dashboard 2 — Dashboard Finance

Sumber utama:
- Telegram manual.
- Sheet khusus: Cash Ledger, Credit Card, Hutang, Cicilan Rumah, Aset/Gold Ledger.
- Data net worth yang sudah diklasifikasi.

Fokus:
- Cash Ledger.
- Credit Card.
- Cicilan Rumah / KPR.
- Hutang.
- Aset emas.
- Net Worth.
- Ringkasan finance keluarga.

Dashboard Finance boleh meniru struktur contoh PDF AIRO Personal Finance:
- Net Worth Total.
- Aset likuid.
- Ekuitas rumah.
- Sisa KPR.
- Aset emas.
- Hutang aktif.
- Saldo akun.
- Cashflow bulan ini.
- Cicilan rumah.
- Kartu kredit.
- Aset emas.

Tahap awal dashboard di Google Sheets fokus ke logika dan angka yang benar.
Versi visual HTML/PDF yang mirip contoh dibuat setelah logic stabil.

## Dashboard Visual Decision

Dashboard contoh awal boleh dijadikan acuan, tetapi tidak wajib pixel-perfect di Google Sheets.

Estimasi kemiripan:
- Google Sheets dashboard: 70–85% mirip secara struktur dan isi.
- HTML/PDF dashboard: 90–98% mirip secara visual.

Strategi:
1. Buat dashboard fungsional di Google Sheets.
2. Pastikan angka dan logika benar.
3. Setelah stabil, buat versi HTML/PDF report yang lebih mirip contoh.

## Collision Rule Decision

Collision engine penuh tidak dibuat di awal.

Alasan:
- Risiko bug tinggi.
- Banyak transaksi BLU adalah internal movement.
- Ada potensi double count antara Telegram manual dan PDF mutasi.
- CC payment, tarik tunai, aset emas, hutang, dan internal pocket movement mudah salah dibaca sebagai expense baru.

Risiko collision engine penuh:
- Bug risk: tinggi.
- Debug: berat.
- Cocok nanti setelah staging dan dashboard stabil.

Keputusan sekarang:
- PDF masuk sebagai preview/staging.
- Jika transaksi PDF mirip dengan input Telegram, tandai sebagai possible duplicate/link.
- Jangan auto-update tab khusus.
- Jangan auto-link agresif.

## Reconciliation Policy

Jika PDF mutasi menemukan transaksi yang mirip dengan input Telegram:

Decision:
- Tandai sebagai possible duplicate/link.
- Jangan auto-update.
- Jangan auto-delete.
- Jangan auto-merge.
- Jangan ubah status CC/Hutang/Aset tanpa rule eksplisit dan approval.

Contoh:

1. PDF: Transfer Dana ke bluGether - Bayaran Kartu Kredit
   Telegram: bayar cc shopee 67rb dari blu
   Action: possible link to CC payment, bukan expense baru.

2. PDF: Tarik Tunai
   Telegram: cash masuk 100rb
   Action: possible link to Cash Ledger source, bukan expense.

3. PDF: Transfer untuk emas/invest emas
   Telegram: aset emas beli
   Action: possible link to asset funding, bukan expense.

4. PDF: Transfer ke keluarga/nama tertentu
   Telegram: bayar hutang
   Action: possible link to Hutang History, bukan expense umum.

5. PDF: QRIS makan/warung
   Tidak ada Telegram manual
   Action: masuk Transactions/Cleaned Spending jika lolos klasifikasi.

## Source of Truth by Domain

Cash Ledger:
- Source of truth: Telegram manual.

Credit Card:
- Source of truth: Telegram manual + CC sheet.
- PDF hanya bukti/possible link, bukan auto source awal.

Cicilan Rumah/KPR:
- Source of truth: KPR sheet/manual schedule.
- PDF hanya bukti bayar bila ada.

Hutang:
- Source of truth: Telegram manual + Hutang sheet.
- PDF hanya possible link.

Aset/Gold:
- Source of truth: Gold Ledger/Aset sheet.
- PDF hanya possible funding movement.

Transactions/Daily BLU:
- Source of truth: PDF mutasi BLU closing bulanan.

Dashboard:
- Source of truth: hasil klasifikasi dan rekonsiliasi, bukan raw import langsung.

## Category Design Decision

Kategori tidak dikunci dari template umum.

Keputusan interview:
1. Kategori utama memakai gabungan:
   - Jenis kebutuhan hidup.
   - Jenis cashflow.
   - Sumber/pocket.
2. PDAM, listrik, gas, galon, sampah, wifi digabung sebagai Kebutuhan Rumah.
3. Nurul adalah istri dan finance ini adalah finance keluarga.
   - Tidak perlu kategori khusus Nurul.
   - Nama Nurul cukup menjadi counterparty/catatan jika muncul di mutasi.
4. CC payment adalah pengurang sisa tagihan CC.
   - Bukan expense baru.
   - Bukan konsumsi baru.

Model data kategori yang disarankan:

- domain/tab
- cashflow_type
- category_main
- subcategory
- account
- counterparty/person_context
- source_origin
- linked_record
- possible_duplicate/link flag

Contoh cashflow_type:
- income
- expense
- transfer_internal
- liability_payment
- asset_allocation
- cash_movement
- review_needed

## Initial Category Direction

Kategori akan dibuat sebagai kategori utama + subkategori.

Contoh category_main yang masih perlu diperdalam:
- Kebutuhan Rumah
- Makan Harian
- Transport
- Kesehatan
- Belanja
- Langganan
- Hutang/Kewajiban
- Cicilan
- Aset/Tabungan
- Cash Movement
- Internal Transfer
- Review

Catatan:
- Jangan terlalu umum seperti dashboard template generik.
- Jangan terlalu detail sampai menyulitkan maintenance.
- Final kategori akan diputuskan melalui interview lanjutan.

## Telegram Input Design

AIRO Telegram harus bisa membaca 2 format:

1. Kalimat langsung.
2. Form key-value yang bisa dicopy dari /form.

Structured form harus diprioritaskan dibanding parser kalimat karena lebih eksplisit.

## /help Design

Command /help berfungsi sebagai panduan ringkas.

Draft:

/help

AIRO Finance bisa baca 2 format:

1. Kalimat langsung
Contoh:
cc beli shopee skincare 67rb
bayar cc shopee skincare 67rb dari blu
cash beli makan 13rb
cash masuk 100rb dari tarik tunai
bayar hutang ke mamak 1.1jt
aset emas beli 0.5 gram 24k
bayar cicilan rumah 1570000 bca

2. Form
Ketik /form untuk ambil template.
Isi form, lalu kirim ulang ke chat ini.

## /form Design

Command /form mengirim template yang bisa dicopy, diisi, lalu dikirim ulang.

Draft:

/form

Salin, isi, lalu kirim ulang:

tipe (cash/cc/cicilan_rumah/hutang/aset):
akun (bca/blu/mandiri/gopay/shopeepay/cash/cc):
aksi (beli/bayar/pesan/masuk/terima/refund/tf/pinjam):
deskripsi:
nominal (15000/15rb/1.5jt/1,5jt):
tanggal (hari ini/kemarin/tgl 15 mei):
catatan:

Contoh isi form:

tipe: cc
akun: cc
aksi: beli
deskripsi: shopee skincare
nominal: 67rb
tanggal: hari ini
catatan:

## Parser Form Rules

Jika input mengandung key-value seperti:
- tipe:
- akun:
- aksi:
- deskripsi:
- nominal:
- tanggal:
- catatan:

Maka parser harus membaca sebagai structured form.

Jika field wajib kosong:
- Jangan tebak agresif.
- Masuk Review Queue atau minta klarifikasi.
- Untuk tahap awal lebih aman masuk Review Queue.

Field minimal:
- tipe
- aksi
- deskripsi
- nominal, kecuali aset emas berbasis gram yang belum punya nominal
- tanggal optional default hari ini

## Dashboard Mutasi BLU Requirements

Dashboard Mutasi BLU harus memisahkan:

1. Raw Movement
   - Semua transaksi statement apa adanya.

2. Cleaned Spending
   - Expense aktual setelah internal transfer disaring.

3. Internal Transfer
   - bluGether movement.
   - bluSaving movement.
   - transfer antar pocket.
   - tarik tunai jika menjadi cash movement.

4. Liability Payment
   - CC payment.
   - hutang payment jika terdeteksi.
   - bukan expense konsumsi.

5. Asset Allocation
   - emas/investasi.
   - bukan expense konsumsi.

6. Review Needed
   - ambiguous.
   - possible duplicate/link.
   - unknown category.

## Dashboard Finance Requirements

Dashboard Finance bertahap dari basic dulu:

Phase awal:
- Cash Ledger.
- Credit Card.
- Hutang.
- Cicilan Rumah/KPR.
- Aset Emas.
- Net Worth.

Belum wajib:
- budget detail.
- alert.
- trend.
- forecast.

Setelah stabil:
- Budget per kategori.
- Warning/overbudget.
- Alert CC belum transfer.
- Hutang due.
- Trend 3–6 bulan.
- Forecast cashflow.

## PDF Preview Flow

Tahap awal:

1. User upload PDF mutasi BLU ke ChatGPT.
2. ChatGPT bantu ekstrak menjadi preview tabel/CSV.
3. Preview dibaca dan dicek dulu.
4. Data tidak langsung masuk final Google Sheet.
5. Jika disetujui, baru masuk staging/import.
6. Cleaned spending dan raw movement dipisahkan.
7. Possible duplicate/link diberi flag, bukan auto-merge.

## Implementation Roadmap

Phase 0 — Safety Audit Mode
- Tidak run Apps Script.
- Tidak deploy.
- Tidak ubah formula.
- Tidak patch tanpa approval.

Phase 1 — Record Blueprint
- Simpan dokumen keputusan ini ke GitHub.

Phase 2 — Stabilization Baseline
- Selesaikan bug CC payment matcher setelah approval.
- Smoke test.
- Deploy aman.
- Commit aman.

Phase 3 — Telegram Input Contract
- Implement /help read-only.
- Implement /form read-only.
- Implement parser structured form.

Phase 4 — Dashboard Split
- Buat Dashboard Mutasi BLU.
- Buat Dashboard Finance.
- Jangan collision engine penuh.

Phase 5 — PDF Preview Pipeline
- Mulai dari upload PDF ke ChatGPT.
- Buat format preview CSV/tabel.
- Rancang staging schema.

Phase 6 — Category Interview
- Finalisasi category_main dan subcategory personal.
- Jangan pakai template umum mentah-mentah.

Phase 7 — Safe Reconciliation
- Tambah possible duplicate/link.
- Tidak auto-update tab khusus.

Phase 8 — Visual Dashboard
- Google Sheets dashboard functional.
- HTML/PDF report menyusul setelah angka stabil.

Phase 9 — Budget, Alerts, Trend, Forecast
- Budget kategori.
- Alert CC.
- Alert hutang.
- Trend 3–6 bulan.
- Forecast cashflow.

## Estimated Execution Time

Versi aman pertama:
- 1–2 hari kerja fokus.

Versi rapi dan bisa dipakai bulanan:
- 3–5 hari kerja bertahap.

Dengan PDF importer lokal semi-otomatis:
- Tambahan 1 minggu atau lebih tergantung stabilitas ekstraksi PDF.

## Open Questions

1. Final category_main dan subcategory belum dikunci.
2. Format staging untuk PDF mutasi BLU belum dibuat.
3. Visual dashboard akan mulai dari Google Sheets atau langsung HTML/PDF belum dikunci.
4. Parser /form belum diimplementasikan.
5. Collision rule penuh ditunda.
6. Possible duplicate/link schema belum dibuat.
7. CC payment matcher masih perlu distabilkan sebelum enhancement besar.

## Safety Notes

- Jangan commit folder untracked seperti EarnsAI, runtime, trading sebelum diaudit.
- Jangan commit token/secret/env.
- Jangan menjalankan deploy sebelum smoke test.
- Jangan mengubah formula/dashboard live tanpa backup.
- Jangan memproses PDF langsung ke final sheet.
