# AIRO Finance Assistant — Capability Map (v1.0)

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_ASSISTANT_CAPABILITY_MAP_V1`
- **Status**: `LOCKED_CAPABILITY_MAP`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_ASSISTANT_CAPABILITY_MAP_V1`
- **Role**: `AIRO Sync Planning`
- **Mode**: `DESIGN_ONLY`
- **Source of Truth**: `AIRO_FINANCE_LAB_MVP_PRD_V1`, `AIRO_FINANCE_INTELLIGENCE_BOUNDARY_V1`, `AIRO_FINANCE_HERMES_DECISION_V1`, `AIRO_FINANCE_QUERY_CAPABILITY_MATRIX_V1`, M1-M9 Validation Evidence

---

## 1. Identitas Strategis: AIRO Finance Sebenarnya Ingin Menjadi Apa?

AIRO Finance bukanlah bot pencatat monolitik, bukan accounting software enterprise, dan bukan penasihat keuangan otonom (*autonomous robo-advisor*).

### Definisi Identitas Inti:
> **"AIRO Finance Assistant adalah Personal Finance Intelligence Assistant yang terintegrasi di dalam persona tunggal AIRO Hermes, berfungsi sebagai Cermin Keuangan Obyektif (Financial Mirror) dan Pengasah Kesadaran Finansial (Financial Awareness Enhancer) tanpa friksi kognitif."**

Tiga pilar operasionalnya:
1. **Financial Mirror (Cermin Keuangan)**: Melaporkan posisi kas, histori pengeluaran, dan fakta pembukuan secara instan (<1 detik), presisi 100%, dan bebas halusinasi.
2. **Awareness Enhancer (Pengingat Kesadaran)**: Membantu Owner melihat pola boros, anomali belanja, dan laju pemakaian anggaran (*burn rate*) sebelum uang habis.
3. **Trade-off Reasoning Partner (Mitra Simulasi Pilihan)**: Membantu Owner menghitung dampak matematis dari suatu pengeluaran terhadap cadangan kas aman, **tanpa pernah bersikap menggurui atau mengambil keputusan hidup sepihak**.

---

## 2. Pemetaan 5 Area Kemampuan (*5 Core Capability Areas*)

Setiap kapabilitas dianalisis terhadap kondisi saat ini dan diklasifikasikan ke dalam:
- **`KEEP`**: Sudah ada, terbukti efektif, dan dipertahankan.
- **`EXTEND`**: Fondasi tersedia di Finance Core/Adapter, membutuhkan pengembangan terukur.
- **`DEFER`**: Bernilai potensial, namun ditunda agar tidak mengganggu fokus stabilitas inti.
- **`REJECT`**: Bertentangan mutlak dengan batas keamanan, memicu halusinasi, atau mengulang pola kegagalan EAB.

---

### AREA 1: CAPTURE ASSISTANCE (Bantuan Pencatatan Data)
*Pertanyaan Utama: Bagaimana AI membantu user memasukkan data?*

| No | Kapabilitas | Deskripsi Teknis | Status Saat Ini | Klasifikasi | Justifikasi Arsitektur |
|:---:|---|---|:---:|:---:|---|
| 1.1 | **Deterministic Single-Turn Quick Capture** | Parser regex IDR (`35k`, `50rb`, `1.5jt`) dengan *sane defaults* akun dan kategori bawaan. | SUDAH ADA (M3) | `KEEP` | Cepat (<3.5 detik), 100% konsisten, nol token LLM. |
| 1.2 | **Interactive Safety Net Card** | Kartu konfirmasi Telegram interaktif dengan tombol `[❌ Batal]` 1-klik untuk menangkal typo nominal. | SUDAH ADA (M3) | `KEEP` | Terbukti menyelamatkan 1 insiden fatal typo (350k vs 35k) pada trial M9. |
| 1.3 | **Multi-Account Transfer Syntax** | Parser mengenali format transfer antar-rekening: `"trf 500k bca ke mandiri"`. | BELUM ADA | `EXTEND` | Kebutuhan nyata terbukti pada trial M9 (saat ini harus manual lewat Web Modal). |
| 1.4 | **AI Freeform Text Drafter (Assisted)** | LLM membantu memecah catatan panjang tidak berstruktur menjadi kartu konfirmasi draft. | BELUM ADA | `DEFER` | Ditunda hingga kebutuhan input kompleks terbukti mendesak. Tetap wajib konfirmasi 1-klik. |
| 1.5 | **Receipt OCR & Bank Email Auto-Scraping** | Parser otomatis membaca mutasi email atau foto struk belanja. | TIDAK ADA | `REJECT` | **DITOLAK KERAS**. Menambah titik gagal tinggi, lambat, dan memicu *premature automation* EAB. |
| 1.6 | **Autonomous Transaction Logging** | AI mencatat transaksi otomatis ke buku besar dari percakapan tanpa kartu konfirmasi. | TIDAK ADA | `REJECT` | **DITOLAK KERAS**. Melanggar *Zero Writes Rule* mutlak. |

---

### AREA 2: FINANCE MEMORY (Memori Finansial)
*Pertanyaan Utama: Apakah AI bisa menjawab "Apa yang terjadi dengan uang saya?"*

| No | Kapabilitas | Deskripsi Teknis | Status Saat Ini | Klasifikasi | Justifikasi Arsitektur |
|:---:|---|---|:---:|:---:|---|
| 2.1 | **Real-Time Account Balance Lookup** | Query saldo per rekening dan total kas likuid melalui endpoint `AccountOverview`. | SUDAH ADA (M6/M7) | `KEEP` | Latensi <1 detik, mencerminkan saldo fisik 100%. |
| 2.2 | **Current Month Cashflow Summary** | Ringkasan total pengeluaran, pemasukan, dan net cashflow bulan berjalan (`MonthlySummary`). | SUDAH ADA (M6/M7) | `KEEP` | Faktual 1:1 terhadap baris tabel SQLite. |
| 2.3 | **Recent Transaction Traceability** | Pelaporan histori 5-10 transaksi terakhir terurut kronologis dengan detail akun dan kategori. | SUDAH ADA (M6/M7) | `KEEP` | Memberikan audit instan saat Owner memeriksa transaksi baru. |
| 2.4 | **Multi-Month Comparative Memory** | Komparasi tren belanja bulan ini terhadap bulan-bulan sebelumnya (MoM / YoY). | PARSIAL (Data 1 bln) | `EXTEND` | Perlu memperluas `insights.py` saat akumulasi transaksi bertambah melintasi bulan. |
| 2.5 | **Merchant / Entity Historical Aggregation** | Menjawab total pengeluaran ke penerima tertentu ("Berapa total bayar ke PLN tahun ini?"). | BELUM ADA | `EXTEND` | Membutuhkan read model agregasi string catatan transaksi (`note`). |
| 2.6 | **External Account Auto-Sync (Open Banking)** | Sinkronisasi API otomatis dengan perbankan pihak ketiga. | TIDAK ADA | `REJECT` | **DITOLAK**. Risiko keamanan kredensial dan beban pemeliharaan scraper API tidak relevan. |

---

### AREA 3: FINANCIAL AWARENESS (Kesadaran Finansial)
*Pertanyaan Utama: Apakah AI membantu user sadar akan kondisi keuangannya?*

| No | Kapabilitas | Deskripsi Teknis | Status Saat Ini | Klasifikasi | Justifikasi Arsitektur |
|:---:|---|---|:---:|:---:|---|
| 3.1 | **Top Spending Category Breakdown** | Identifikasi kategori pengeluaran terbesar dan persentase dominasinya (`CategorySpendingReport`). | SUDAH ADA (M6/M7) | `KEEP` | Memberikan kesadaran langsung pos belanja yang paling menguras kas. |
| 3.2 | **Deterministic Anomaly Detection** | Mendeteksi transaksi tunggal $>2.5	imes$ rata-rata atau kategori mendominasi $>40\%$ pengeluaran. | SUDAH ADA (M6/M7) | `KEEP` | Aturan kaku Python, tidak membebani LLM dengan tebakan statistik. |
| 3.3 | **Budget Burn-Rate & Pacing Bar** | Menghitung rata-rata laju belanja harian vs kuota anggaran bulan berjalan. | SUDAH ADA (M2/M6) | `KEEP` | Visual bar di dashboard + angka pacing saat ditanya di chat. |
| 3.4 | **Weekly Spending Velocity Tracking** | Menghitung apakah belanja minggu tertentu mengalami lonjakan tajam dibanding awal bulan. | BELUM ADA | `EXTEND` | Dapat dihitung deterministik di Python sebagai sub-metrik `MonthlySummary`. |
| 3.5 | **Intrusive Nagging & Shaming Alerts** | AI secara agresif menegur dan menghakimi gaya hidup atau kebiasaan jajan Owner. | TIDAK ADA | `REJECT` | **DITOLAK**. Hermes adalah asisten pendukung yang tenang, bukan polisi finansial yang menjengkelkan. |

---

### AREA 4: FINANCIAL PLANNING SUPPORT (Dukungan Perencanaan & Pemikiran)
*Pertanyaan Utama: Apakah AI membantu user berpikir dan mensimulasikan pilihan finansial?*

| No | Kapabilitas | Deskripsi Teknis | Status Saat Ini | Klasifikasi | Justifikasi Arsitektur |
|:---:|---|---|:---:|:---:|---|
| 4.1 | **Envelope Budget Tracking** | Membandingkan pagu anggaran per kategori terhadap transaksi aktual (`budgets` table). | SUDAH ADA (M1/M6) | `KEEP` | Pondasi amplop anggaran bekerja dengan integritas ACID. |
| 4.2 | **Safe-to-Spend Calculator** | Formula deterministik: $	ext{Saldo Likuid} - 	ext{Komitmen Tetap} - 	ext{Safety Floor}$. | BELUM ADA (Gap M8.5) | `EXTEND` | Nilai guna sangat tinggi. Wajib diawali dengan penambahan model komitmen tetap. |
| 4.3 | **Payday Runway Estimation** | Menghitung estimasi ketahanan saldo hingga tanggal pemasukan/gajian berikutnya. | BELUM ADA (Gap M8.5) | `EXTEND` | Membutuhkan parameter konfigurasi tanggal gajian rutin. |
| 4.4 | **Trade-off & Purchase Impact Simulator** | Menjawab: *"Kalau saya beli barang X seharga RpY, dampak ke sisa runway dan safety buffer apa?"*. | BELUM ADA | `EXTEND` | Simulasi matematis murni (in-memory read calculation), nol mutasi ke buku besar. |
| 4.5 | **Prescriptive Financial Advice (Robo-Advisor)** | AI memutuskan *"Kamu boleh/tidak boleh beli mobil"* atau merekomendasikan alokasi saham/kripto. | TIDAK ADA | `REJECT` | **DITOLAK KERAS**. Melanggar batas Level 4. Keputusan hidup adalah hak mutlak Owner. |
| 4.6 | **Autonomous Budget Alteration** | AI mengubah plafon budget secara mandiri berdasarkan pengamatan pola. | TIDAK ADA | `REJECT` | **DITOLAK KERAS**. Mengubah anggaran tanpa izin Owner adalah cacat integritas fatal. |

---

### AREA 5: PROACTIVE ASSISTANCE (Bantuan Proaktif)
*Pertanyaan Utama: Apakah AI boleh memberi notifikasi tanpa ditanya?*

| No | Kapabilitas | Deskripsi Teknis | Status Saat Ini | Klasifikasi | Justifikasi Arsitektur |
|:---:|---|---|:---:|:---:|---|
| 5.1 | **Zero Background Schedulers (MVP Rule)** | Menjaga sistem tetap pasif tanpa cron background yang berjalan liar. | SUDAH ADA (M0-M9) | `KEEP` | Menghindarkan loop konsumsi CPU dan ketergantungan daemonic yang rapuh. |
| 5.2 | **Passive Sunday Weekly Recap** | Notifikasi ringkas rekap belanja mingguan setiap Minggu malam via Telegram (tanpa interogasi). | BELUM ADA (Req M9) | `EXTEND` | Diinginkan Owner pada trial M9. Harus dirancang sebagai cron pasif terisolasi. |
| 5.3 | **Real-Time Threshold Push Alerts** | Notifikasi instan saat saldo rekening menyentuh ambang batas minimum (*safety floor*). | BELUM ADA | `DEFER` | Ditunda hingga pola penggunaan stabil. Menghindari spamming pesan di ponsel. |
| 5.4 | **Conversational Proactive Interrogation** | Bot tiba-tiba memulai obrolan menanyakan kenapa ada pengeluaran besar kemarin. | TIDAK ADA | `REJECT` | **DITOLAK KERAS**. Menjebak user dalam interogasi dialog bergaya EAB yang dibenci. |
| 5.5 | **Autonomous Fund Rebalancing** | Memindahkan dana otomatis antar-rekening saat satu rekening menipis. | TIDAK ADA | `REJECT` | **DITOLAK MUTLAK**. Risiko kegagalan perbankan nyata dan pelanggaran batasan legal. |

---

## 3. Matriks Keputusan Master (*Classification Master Matrix*)

```text
+-----------------------------------------------------------------------------------------------+
| KEEP (Dipertahankan & Stabil)                                                                 |
| - 1.1 Single-turn regex parser (<3.5s)          - 2.1 Cek saldo akun real-time                |
| - 1.2 Interactive cancel card (1-klik)          - 2.2 Ringkasan arus kas bulanan              |
| - 3.1 Peringkat kategori belanja boros          - 2.3 Riwayat transaksi terakhir              |
| - 3.2 Deteksi anomali kaku (>2.5x mean)         - 4.1 Pelacakan amplop anggaran               |
| - 5.1 Zero background daemons (pasif)                                                         |
+-----------------------------------------------------------------------------------------------+
                                                │
                                                ▼
+-----------------------------------------------------------------------------------------------+
| EXTEND (Fokus Peningkatan Terukur)                                                            |
| - 1.3 Sintaks transfer chat ("trf 500k")        - 4.2 Safe-to-Spend Calculator deterministik  |
| - 2.4 Komparasi historis antar-bulan            - 4.3 Estimasi Runway s.d. tanggal gajian     |
| - 2.5 Pencarian riwayat per merchant/entitas     - 4.4 Simulator dampak belanja ("What-if")    |
| - 3.4 Analisis laju belanja mingguan            - 5.2 Rekap pasif Minggu malam                |
+-----------------------------------------------------------------------------------------------+
                                                │
                                                ▼
+-----------------------------------------------------------------------------------------------+
| DEFER (Ditunda untuk Fase Lanjutan)                                                           |
| - 1.4 AI draft parser untuk teks panjang        - 5.3 Push alert saldo minim real-time        |
+-----------------------------------------------------------------------------------------------+
                                                │
                                                ▼
+-----------------------------------------------------------------------------------------------+
| REJECT (Ditolak Mutlak / Anti-EAB Boundaries)                                                 |
| - 1.5 OCR struk & bank email scraping           - 4.5 Robo-advisor / saran hidup preskriptif  |
| - 1.6 AI ledger writes tanpa konfirmasi         - 4.6 Auto-ubah plafon budget sepihak         |
| - 2.6 Sinkronisasi open banking otomatis        - 5.4 Interogasi proaktif bot gaya EAB        |
| - 3.5 Nagging / shaming alert agresif           - 5.5 Auto-rebalancing kas / eksekusi otonom  |
+-----------------------------------------------------------------------------------------------+
```

---

## 4. Rangkuman Pertanyaan Strategis Success Criteria

### 1. AIRO Finance sebenarnya ingin menjadi apa?
Menjadi **Personal Finance Intelligence Assistant** yang berfungsi sebagai **Cermin Keuangan Obyektif** dan **Pengasah Kesadaran Finansial** yang cepat, terpercaya, dan bebas friksi di dalam persona AIRO Hermes.

### 2. Kemampuan apa yang sudah ada?
Pencatatan regex cepat (<3.5 detik), kartu pembatalan typo 1-klik, Web Dashboard cockpit, kueri fakta saldo dan transaksi real-time (M6), serta asisten tanya-jawab Hermes berbasis fakta bebas halusinasi (M7/M8).

### 3. Kemampuan apa yang kurang?
Kemampuan menangani transfer via chat, komparasi multi-bulan, dan kalkulasi interpretasi finansial Level 3 (*Safe-to-Spend*, *Payday Runway*, dan simulasi dampak belanja) akibat ketiadaan parameter tagihan rutin, tanggal gajian, dan batas cadangan aman.

### 4. Mana yang prioritas?
1. Sintaks transfer cepat di chat.
2. Resolusi 3 data gap deterministik (komitmen tetap, tanggal gajian, safety floor).
3. Penambahan read model deterministik untuk *Safe-to-Spend* dan simulasi pengeluaran.
4. Rekap pasif mingguan setiap Minggu malam.

### 5. Mana yang jangan dibuat?
Agen finansial baru terpisah, mutasi buku besar oleh AI, interogasi chat beruntun, scraper struk/email bank, dan penasihat keuangan preskriptif (*robo-advisor*).
