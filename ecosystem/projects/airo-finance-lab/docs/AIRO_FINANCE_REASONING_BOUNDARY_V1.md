# AIRO Finance Lab — Reasoning Boundary Specification (v1.0)

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_REASONING_BOUNDARY_V1`
- **Status**: `LOCKED_DESIGN_SPECIFICATION`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_LAB_M85_FINANCE_REASONING_GAP_ANALYSIS_V1`
- **Role**: `AIRO Executor Agent`
- **Mode**: `DESIGN_ONLY`
- **Source of Truth**: `AIRO_FINANCE_INTELLIGENCE_BOUNDARY_V1`, `AIRO_FINANCE_HERMES_DECISION_V1`, M6-M8 Validation Evidence

---

## 1. Executive Summary & Core Objective

Dokumen ini mendefinisikan batas kognitif dan epistemik (*cognitive and epistemic boundary*) untuk penalaran finansial (*financial reasoning*) pada AIRO Hermes.

Tujuan utama spesifikasi ini adalah:
1. **Memetakan 4 Level Penalaran Finansial**: Membedakan secara absolut antara fakta numerik mentah, wawasan kalkulatif, interpretasi terikat asumsi, dan saran finansial preskriptif.
2. **Menjamin Landasan Data 100% (*Zero-Hallucination Grounding*)**: Mencegah Hermes membuat asumsi probabilistik atau tebakan angka di luar payload terverifikasi dari Finance Core.
3. **Mencegah Perangkap EAB**: Menolak otomatisasi preskriptif tingkat tinggi (Level 4) dan melarang keras hak mutasi buku besar bagi AI (*Zero Writes Rule*).

---

## 2. Taksonomi 4 Level Penalaran Finansial (*Financial Reasoning Hierarchy*)

```text
+-----------------------------------------------------------------------------------+
| LEVEL 1: FACT QUERY (Lookup Mentah)                                               |
| Sifat: Deterministik, 1:1 terhadap baris database.                                |
| Contoh: "Berapa pengeluaran bulan ini?", "Berapa saldo BCA saya?"                 |
| Kebutuhan: SELECT query pada ledger & accounts. Status: 100% SUPPORTED (M6/M7).   |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| LEVEL 2: DERIVED INSIGHT (Kalkulasi & Komparasi Deterministik)                    |
| Sifat: Agregasi matematis, rasio persentase, komparasi antar-kategori.            |
| Contoh: "Kategori mana paling boros?", "Ada pengeluaran tidak biasa?"             |
| Kebutuhan: Read models (SUM, AVG, %, Anomaly rules). Status: 100% SUPPORTED (M6). |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| LEVEL 3: FINANCIAL INTERPRETATION (Sintesis Posisi & Daya Tahan Finansial)        |
| Sifat: Estimasi berbasis formula terikat batas parameter eksplisit.               |
| Contoh: "Berapa uang aman saya?", "Apakah saldo cukup sampai gajian?"             |
| Kebutuhan: Saldo likuid + Komitmen tetap + Burn-rate + Safety Floor.             |
| Status: CAPABILITY GAP IDENTIFIED (Butuh parameter deterministik tambahan).       |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
| LEVEL 4: FINANCIAL ADVICE (Rekomendasi Preskriptif Keputusan Hidup)               |
| Sifat: Bergantung pada variabel eksternal subjektif, risiko, & komitmen tak rekam. |
| Contoh: "Apakah saya boleh beli mobil?", "Investasi ke mana sisa uang saya?"       |
| Default: STRICTLY DO NOT AUTOMATE. Refusal script + Sajikan Fakta Obyektif saja.  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Tipe Pertanyaan yang Didukung (*Supported Question Types*)

Hermes diizinkan memproses dan menjawab pertanyaan yang termasuk dalam kategori berikut:

### 3.1 Level 1: Fact Queries (Didukung Penuh)
1. **Pengecekan Saldo Akun**:
   - Pola: *"Berapa saldo BCA / Mandiri / Cash?"*, *"Berapa total uang saya?"*
   - Sumber Data: `AccountOverview` (M6 API).
2. **Ringkasan Arus Kas Masuk & Keluar**:
   - Pola: *"Berapa pengeluaran bulan ini?"*, *"Berapa total pemasukan September?"*
   - Sumber Data: `MonthlySummary` (M6 API).
3. **Histori Aktivitas Terakhir**:
   - Pola: *"Apa transaksi terakhir saya?"*, *"5 pengeluaran terakhir apa saja?"*
   - Sumber Data: `RecentActivityItem` (M6 API).

### 3.2 Level 2: Derived Insights (Didukung Penuh)
1. **Dominasi Belanja Kategori**:
   - Pola: *"Kategori apa yang paling boros / paling besar?"*
   - Logika: Pengurutan nominal belanja descending + kalkulasi persentase terhadap total pengeluaran.
   - Sumber Data: `CategorySpendingReport` (M6 API).
2. **Deteksi Anomali Pengeluaran**:
   - Pola: *"Ada pengeluaran anomali / tidak biasa bulan ini?"*
   - Logika: Transaksi tunggal $>2.5	imes$ rata-rata atau kategori mendominasi $>40\%$.
   - Sumber Data: `SpendingAnomaly` (M6 API).
3. **Pacing Anggaran (*Budget Burn-Rate*)**:
   - Pola: *"Berapa rata-rata belanja harian saya?"*, *"Apakah belanja makan terlalu cepat?"*
   - Logika: $	ext{Total Belanja} / 	ext{Hari Berjalan}$ dibandingkan alokasi harian yang direncanakan.

### 3.3 Level 3: Bounded Financial Interpretation (Didukung Terbatas / Conditional)
Hermes HANYA diizinkan menjawab jika seluruh parameter formula tersedia secara eksplisit:
1. **Safe-to-Spend (Uang Aman Belanja)**:
   - Formula Wajib:
     $$	ext{Safe-to-Spend} = 	ext{Total Saldo Likuid} - 	ext{Komitmen Tetap} - 	ext{Ambang Cadangan Aman (Safety Floor)}$$
   - Aturan: Jika komitmen tetap atau ambang cadangan belum didefinisikan oleh Owner di sistem, Hermes **DILARANG MENEBAK** dan wajib menyatakan batasan formula.
2. **Estimasi Runway Sederhana**:
   - Formula Wajib:
     $$	ext{Runway Hari} = rac{	ext{Saldo Likuid Aktif}}{	ext{Rata-rata Pengeluaran Harian (30 Hari Terakhir)}}$$
   - Aturan: Wajib mencantumkan klausul asumsi bahwa tingkat pengeluaran dianggap konstan tanpa pengeluaran mendadak.

---

## 4. Tipe Pertanyaan yang Dilarang / Tidak Didukung (*Unsupported Question Types*)

Hermes **DILARANG KERAS** memberikan jawaban spekulatif atau preskriptif untuk kategori pertanyaan berikut:

1. **Rekomendasi Pembelian Aset Besar (*Big-Ticket Discretionary Purchases*)**:
   - Contoh: *"Apakah saya sanggup beli iPhone 16 Pro / mobil baru?"*
   - Alasan: Melibatkan variabel di luar pembukuan (stabilitas karier, kebutuhan darurat masa depan, prioritas keluarga).
2. **Saran Investasi & Pemilihan Instrumen (*Investment Advice*)**:
   - Contoh: *"Sisa uang sebaiknya ditaruh di saham BBCA atau reksadana pasar uang?"*
   - Alasan: AIRO Finance Lab adalah pencatatan keuangan pribadi, bukan pengelola investasi atau penasihat keuangan berlisensi.
3. **Penilaian Kelayakan Utang Baru (*Debt Affordability Assessment*)**:
   - Contoh: *"Apakah saya boleh ambil pinjaman KPR 6 juta per bulan?"*
   - Alasan: Rasio DTI (Debt-to-Income) riil membutuhkan audit komprehensif atas beban tanggungan yang tidak terekam dalam ledger harian.
4. **Peramalan Keuangan Probabilistik (*Speculative Financial Forecasting*)**:
   - Contoh: *"Kira-kira berapa kekayaan saya tahun depan?"*
   - Alasan: Membuka celah halusinasi tren fiktif tanpa dasar matematis tertutup.
5. **Perintah Mutasi Transaksi via AI (*AI Write Commands*)**:
   - Contoh: *"Hermes, tolong transfer 200k ke BCA"*, *"Hermes, tolong catat makan 35k"*
   - Alasan: Pelanggaran mutlak terhadap Zero Writes Rule. Seluruh mutasi hanya melalui Telegram Quick Capture (M3) atau Web Dashboard Modal (M2).

---

## 5. Kebutuhan Data & Kesenjangan Kemampuan (*Capability Gap*)

Untuk mendukung Level 1 hingga Level 3 secara aman, berikut adalah perbandingan antara ketersediaan data saat ini vs kebutuhan:

| Dimensi Data | Ketersediaan di M1-M8 | Dibutuhkan untuk Level | Status Kesenjangan (*Gap*) |
|---|---|---|---|
| **Saldo Likuid Rekening** | Tersedia (`accounts.balance`) | Level 1, 2, 3 | **NO GAP** (Sudah ada di Finance Core) |
| **Histori Mutasi & Tanggal** | Tersedia (`transactions`) | Level 1, 2, 3 | **NO GAP** (Sudah ada di Finance Core) |
| **Kategori & Pengeluaran Bulanan** | Tersedia (`categories`, M6 Service) | Level 1, 2 | **NO GAP** (Sudah ada di Finance Core) |
| **Plafon Anggaran Bulanan** | Tersedia (`budgets.limit_amount`) | Level 1, 2 | **NO GAP** (Sudah ada di Finance Core) |
| **Tagihan Tetap / Komitmen Bulanan** | **TIDAK TERSEDIA** (Belum ada flag `is_recurring` atau tabel komitmen) | Level 3 (Safe-to-Spend) | **GAP 1: COMMITTED EXPENSES DATA MISSING** |
| **Siklus Gajian / Tanggal Pemasukan Berikutnya** | **TIDAK TERSEDIA** (Belum ada parameter tanggal gajian) | Level 3 (Kecukupan s.d. Gajian) | **GAP 2: INCOME CADENCE PARAMETER MISSING** |
| **Ambang Batas Dana Darurat (Safety Floor)** | **TIDAK TERSEDIA** (Belum ada konfigurasi saldo minimal) | Level 3 (Uang Aman Belanja) | **GAP 3: SAFETY FLOOR CONFIGURATION MISSING** |

### Dampak Kesenjangan (*Gap Impact*):
Tanpa resolusi GAP 1, 2, dan 3 secara deterministik di Finance Core, **pertanyaan Level 3 TIDAK BOLEH dijawab secara definitif oleh Hermes**, karena akan memaksa LLM mengasumsikan angka komitmen atau saldo aman secara sepihak.

---

## 6. Aturan Keyakinan (*Confidence Rules*)

Penetapan tingkat keyakinan (*confidence level*) dalam penalaran Hermes diatur sebagai berikut:

1. **Determinisme 100% (High Confidence)**:
   - Berlaku untuk Level 1 dan Level 2.
   - Semua angka dihitung langsung oleh Python/SQL.
   - Hermes menyajikan fakta dengan keyakinan penuh tanpa kata-kata keraguan seperti *"mungkin"* atau *"kira-kira"*.
2. **Kondisional dengan Deklarasi Asumsi (Bounded / Conditional Confidence)**:
   - Berlaku untuk Level 3 jika formula terpenuhi.
   - Hermes **WAJIB** menyatakan secara terbuka asumsi yang digunakan di awal kalimat:
     *Contoh*: *"Berdasarkan saldo likuid saat ini sebesar Rp4.500.000 dan asumsi pengeluaran rata-rata harian Rp75.000 tanpa pengeluaran tak terduga, estimasi dana Anda bertahan sekitar 60 hari."*
3. **Zero Confidence (Refusal Triggered)**:
   - Jika satu atau lebih variabel formula matematis tidak tersedia di database, tingkat keyakinan dinyatakan **0% (UNAVAILABLE)**.
   - LLM dilarang mengisi kekosongan data dengan tebakan intuisi. Hermes wajib mengeksekusi *Refusal Rule*.

---

## 7. Aturan Penolakan & Templat Standar (*Refusal Rules & Standard Scripts*)

Ketika menghadapi pertanyaan yang melampaui batas kewenangan atau ketiadaan data, Hermes wajib menolak secara sopan, lugas, dan mengarahkan kembali ke fakta yang tersedia.

### 7.1 Refusal Trigger R1: Pertanyaan Saran Hidup / Keputusan Finansial (Level 4)
- **Aturan**: Tolak memberikan instruksi "boleh/tidak boleh" beli. Sajikan posisi saldo likuid dan dampak nominalnya terhadap kas, lalu serahkan keputusan sepenuhnya kepada Owner.
- **Templat Standar**:
  > *"Sebagai asisten pencatatan keuangan, saya tidak dapat memutuskan apakah Anda sebaiknya [membeli X / mengambil komitmen Y]. Namun berdasarkan data riil saat ini, total saldo likuid Anda adalah [Rp Saldo] dan pengeluaran bulan berjalan tercatat [Rp Pengeluaran]. Pembelian tersebut akan mengurangi likuiditas kas Anda sebesar [X% / Rp Nominal]. Silakan sesuaikan dengan prioritas dan rencana kebutuhan mendesak Anda."*

### 7.2 Refusal Trigger R2: Ketiadaan Data Historis atau Parameter Formula (Level 3 Gap)
- **Aturan**: Tolak membuat estimasi jika variabel pendukung tidak lengkap di database.
- **Templat Standar**:
  > *"Saya belum dapat menghitung [uang aman belanja / kecukupan saldo s.d. gajian] secara akurat karena sistem belum memiliki data komitmen tagihan rutin dan tanggal gajian berikutnya. Data yang tersedia saat ini adalah total saldo kas sebesar [Rp Saldo]."*

### 7.3 Refusal Trigger R3: Upaya Mutasi Data via Chat Hermes (Write Access Attempt)
- **Aturan**: Tegaskan bahwa Hermes adalah modul baca murni (*read-only*) dan arahkan ke jalur mutasi resmi.
- **Templat Standar**:
  > *"Saya adalah modul baca finansial dan tidak memiliki akses menulis atau mencatat ke buku besar. Untuk mencatat transaksi baru, silakan ketik langsung di chat bot pencatat (contoh: 'makan 35k bca') atau gunakan formulir tambah transaksi di Web Dashboard."*

---

## 8. Anti-EAB Invariants

1. **No Autonomous AI Decision Engine**: Hermes tidak pernah menjalankan evaluasi "kelayakan finansial" mandiri tanpa permintaan langsung dari Owner.
2. **No Hallucinated Parameters**: Tidak ada *default hardcoded* tersembunyi untuk komitmen hidup Owner di dalam prompt LLM.
3. **Document-First Resolution**: Setiap ekspansi kemampuan baru wajib diawali dengan penambahan skema/data deterministik di Finance Core sebelum tool Hermes dibuka.
