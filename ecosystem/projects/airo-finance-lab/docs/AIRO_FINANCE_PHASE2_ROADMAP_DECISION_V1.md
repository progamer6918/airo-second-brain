# AIRO Finance Lab — Phase 2 Roadmap Decision (v1.0)

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_PHASE2_ROADMAP_DECISION_V1`
- **Status**: `LOCKED_PHASE_2_DECISION`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_LAB_PHASE2_ROADMAP_DECISION_V1`
- **Role**: `AIRO Executor Agent`
- **Mode**: `DESIGN_ONLY` (No Code / No Schema Change)
- **Source of Truth**: `AIRO_FINANCE_LAB_MVP_PRD_V1`, `AIRO_FINANCE_ASSISTANT_CAPABILITY_MAP_V1`, `AIRO_FINANCE_USER_EXPERIENCE_ACCEPTANCE_REPORT_V1`, M1-M9 Validation Evidence

---

## 1. Executive Summary & Jawaban Kunci

Dokumen ini mengunci urutan prioritas pengembangan untuk **Phase 2 (Post-MVP Expansion)** berdasarkan data empiris penggunaan nyata (*7-Day Trial Evidence*), analisis dependensi teknis, nilai guna harian bagi Owner, dan kepatuhan absolut terhadap batasan Anti-EAB.

### Pertanyaan Sukses Inti:
> **"Setelah MVP, apa hal pertama yang dibuat dan kenapa?"**

### Jawaban Tegas:
> **Hal pertama yang WAJIB dibuat adalah FEATURE A: TRANSFER FOUNDATION.**
> 
> **Alasan Fundamental**:
> 1. **Menutup Titik Kebocoran Integritas Data**: Pemindahan saldo antar rekening sendiri (misal: BCA ke Blu/Mandiri) adalah transaksi harian riil yang belum bisa dicatat melalui Telegram Quick Capture. Tanpa fitur ini, saldo buku besar cepat mengalami *desync* (hanyut) terhadap saldo m-Banking fisik, merusak peran sistem sebagai "Cermin Keuangan Obyektif".
> 2. **Nol Dependensi Baru & Kompleksitas Sangat Rendah**: Skema `transactions.direction` di Finance Core sudah memiliki nilai `'TRANSFER'`. Fitur ini murni penambahan parser regex deterministik di Telegram dan fungsi atomik ACID di Python tanpa perlu mengubah skema database, tanpa AI, dan tanpa dependensi eksternal.
> 3. **Fondasi Wajib Sebelum Fitur Lain**: Fitur interpretasi seperti *Safe-to-Spend* (Feature B) mengandalkan saldo kas per rekening yang akurat 100%. Membangun kalkulator kas di atas buku besar yang saldonya timpang akibat transfer yang tak tercatat adalah kesia-siaan (*garbage in, garbage out*).

---

## 2. Urutan Prioritas Resmi Phase 2 (*Official Priority Ordering*)

```text
+-----------------------------------------------------------------------------------+
| PRIORITAS 1: FEATURE A — TRANSFER FOUNDATION (MUST BUILD FIRST)                   |
| Sifat: Core Ledger Completeness & Quick Capture Ergonomics                        |
| Sasaran: Mendukung "trf 500k bca ke mandiri" via Telegram & Core ACID Transfer.   |
| Status: APPROVED FOR IMMEDIATE IMPLEMENTATION                                     |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| PRIORITAS 2: FEATURE B — SAFE-TO-SPEND MODEL (BUILD SECOND)                       |
| Sifat: Financial Awareness & Mental Relief (Level 3 Reasoning)                    |
| Sasaran: Menutup 3 Data Gap (Komitmen Tetap, Tanggal Gajian, Safety Floor).       |
| Status: APPROVED FOR PHASE 2.2 (Data Modeling First, Then Hermes Adapter)         |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| PRIORITAS 3: FEATURE C — WEEKLY FINANCE RECAP (MODIFIED / ON-DEMAND FIRST)        |
| Sifat: Passive Cadence Review                                                     |
| Sasaran: Ringkasan belanja 7 hari terakhir (Hari Minggu).                          |
| Status: MODIFIED AS ON-DEMAND QUERY FIRST (Background cron daemons DEFERRED)     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Evaluasi Mendalam Tiap Fitur Kandidat (*Detailed Feature Evaluation*)

### 3.1 FEATURE A: TRANSFER FOUNDATION
- **Problem Solved**:
  Owner sering memindahkan kas dari rekening operasional (BCA) ke kantong tabungan/belanja digital (Blu BCA atau Mandiri). Saat ini, Telegram Quick Capture menolak input transfer karena regex hanya mengenali pengeluaran dan pemasukan. Owner terpaksa membuka formulir web atau membiarkan data tidak sinkron.
- **User Value**:
  **Sangat Tinggi**. Menghilangkan friksi terbesar dalam siklus pencatatan kas harian dan menjamin saldo di ponsel selalu identik 100% dengan saldo m-Banking fisik.
- **Dependency**:
  **Nol (Zero External Dependencies)**. Tabel `accounts` dan `transactions` sudah siap. Skema SQLite sudah mengizinkan `'TRANSFER'`.
- **Implementation Complexity**:
  **Rendah**.
  1. Tambah pattern regex di `telegram_capture.py`: `^(?:trf|transfer|pindah)\s+(\d+[k|rb|jt]*)\s+(?:dari\s+)?([a-zA-Z0-9_-]+)\s+ke\s+([a-zA-Z0-9_-]+)(?:\s+(.*))?$`.
  2. Tambah fungsi atomik `transfer_funds(from_acc, to_acc, amount, note)` di `engine.py` yang mendebit akun asal, mengkredit akun tujuan, dan mencatat audit log dalam satu blok transaksi database ACID.
- **Risk**:
  **Sangat Rendah**. Net saldo likuid kas tidak berubah ($\Delta = 0$). Nol risiko halusinasi karena prosesnya 100% deterministik.
- **Keputusan**: **KEEP & SET AS PRIORITY 1**.

---

### 3.2 FEATURE B: SAFE-TO-SPEND MODEL
- **Problem Solved**:
  Menyelesaikan *Anxiety Gap* (Kecemasan Kas). Saldo kas sebesar Rp7.000.000 terlihat besar di layar, tetapi Owner tidak tahu berapa bagian yang "bebas dijajankan" setelah memperhitungkan uang sewa/kos yang jatuh tempo, tagihan bulanan, dan batas aman tabungan.
- **User Value**:
  **Sangat Tinggi**. Mengubah Hermes dari sekadar alat *lookup* kaku menjadi asisten finansial yang memberikan ketenangan pikiran (*peace of mind*).
- **Dependency**:
  **Menengah**. Membutuhkan penyelesaian 3 kesenjangan data deterministik (M8.5):
  1. Penanda kewajiban rutin (`is_recurring` pada transaksi atau tabel `fixed_obligations`).
  2. Parameter tanggal gajian rutin (`payday_day`).
  3. Parameter batas saldo cadangan minimal (`safety_floor`).
- **Implementation Complexity**:
  **Menengah**.
  1. Tahap B.1: Tambahkan skema data komitmen dan konfigurasi profil keuangan sederhana.
  2. Tahap B.2: Implementasikan kalkulator deterministik murni di `insights.py`:
     $$	ext{Safe-to-Spend} = 	ext{Saldo Likuid} - 	ext{Komitmen Rutin Tersisa} - 	ext{Safety Floor}$$
     $$	ext{Payday Runway} = rac{	ext{Saldo Likuid Aktif}}{	ext{Rata-rata Burn Rate Harian}}$$
  3. Tahap B.3: Hubungkan ke `FinanceHermesReadAdapter` dengan klausul deklarasi asumsi eksplisit dan aturan penolakan preskriptif (Level 4 Refusal).
- **Risk**:
  **Menengah (Terkontrol)**. Jika formula salah, pengguna bisa salah mengalokasikan uang. Risiko ini dicegah dengan mendasarkan seluruh perhitungan pada matematika Python murni (bukan estimasi LLM) dan kewajiban menampilkan asumsi secara transparan.
- **Keputusan**: **MODIFY & SET AS PRIORITY 2**. Dibangun bertahap (Data Modeling $ightarrow$ Engine Read Model $ightarrow$ Hermes Intent).

---

### 3.3 FEATURE C: WEEKLY FINANCE RECAP
- **Problem Solved**:
  Memberikan tinjauan pasif berkala setiap akhir pekan tanpa memaksa Owner membuka dashboard atau mengetik kueri manual.
- **User Value**:
  **Menengah**. Membangun kebiasaan evaluasi keuangan mingguan yang tenang.
- **Dependency**:
  Membutuhkan data histori 7 hari dan modul agregasi ringkasan mingguan.
- **Implementation Complexity & Anti-EAB Conflict**:
  **Menengah ke Tinggi jika dipaksakan otomatisasi cron**.
  - Aturan PRD MVP: `❌ NO Background Schedulers: Tidak ada cron background otomatis yang berjalan tanpa intervensi.`
  - Jika membuat proses background daemon baru yang berjalan 24/7 di WSL hanya untuk menunggu hari Minggu malam, sistem akan mengulang pola kegagalan daemonic/zombie process EAB.
- **Risk**:
  **Tinggi pada Lapisan Automasi**. Menambah titik rapuh proses gantung dan potensi spam chat Telegram jika error loop.
- **Keputusan**: **MODIFY & DEFER AUTOMATION DAEMON (PRIORITY 3)**.
  - *Modifikasi Desain*: Implementasikan terlebih dahulu sebagai **On-Demand Query di Hermes** (contoh: *"Hermes, rekap minggu ini"* atau command `/rekap`).
  - *Otomatisasi Cron*: Ditunda sampai infrastruktur gateway background AIRO ekosistem (Telegram Gateway Runner resmi) telah diverifikasi stabil.

---

## 4. Batasan Lingkup Phase 2 (*Scope Boundaries & Anti-EAB Invariants*)

Untuk menjaga integritas sistem selama Phase 2, aturan berikut dikunci permanen:

1. **Zero Direct Coding Before Plan Approval**: Dilarang menulis kode implementasi sebelum dokumen keputusan ini disetujui Owner.
2. **Zero AI Write Access**: Penambahan fitur transfer dan kalkulator Safe-to-Spend tetap tunduk pada *Zero Writes Rule*. Hermes tetap 100% read-only.
3. **Single Unified Hermes Persona**: Dilarang membuat bot atau sub-agent terpisah bernama "Arfin Transfer" atau "Finance Advisor Agent". Semua interaksi percakapan tetap berada di dalam persona tunggal Hermes.
4. **No Premature Background Daemons**: Tidak ada cron background loop independen baru yang ditambahkan ke runtime WSL pada Phase 2 awal.

---

## 5. Rekomendasi Langkah Implementasi Berikutnya (*Next Implementation Recommendation*)

Jika Owner menyetujui roadmap ini, langkah eksekusi teknis berikutnya adalah:

### Paket Kerja 1: Milestone 2.1 — Transfer Foundation Vertical Slice
1. **Target**: Membuka jalur input `"trf 500k bca ke mandiri"` di Telegram Quick Capture.
2. **Komponen yang Disentuh**:
   - `src/airo_finance_core/engine.py`: Tambahkan method `transfer_funds(from_id, to_id, amount, note)`.
   - `src/airo_finance_core/telegram_capture.py`: Perluas `SimpleTransactionParser` untuk mendeteksi kata kunci `trf|transfer|pindah`, dan format kartu konfirmasi transfer interaktif.
   - `tests/test_telegram_capture.py`: Tambahkan 5 test case validasi transfer (sukses, akun tidak valid, saldo kurang, pembatalan 1-klik, idempotency).
3. **Verifikasi**: Test suite lulus 100%, zero regression pada M1-M9.
