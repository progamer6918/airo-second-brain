# AIRO Finance Lab — MVP Product Requirements Document (PRD) v1.0

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_LAB_MVP_PRD_V1`
- **Status**: `LOCKED_PHASE_0_CANONICAL`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_LAB_PHASE0_DOCUMENTATION_LOCK_V1`
- **Product Identity Lock**: **Personal Finance Intelligence Application**
  *(Bukan finance bot, bukan accounting enterprise, bukan autonomous finance agent, bukan automation platform)*
- **Architecture Triad**: Dashboard + Telegram Capture + Finance Core + AIRO Hermes Intelligence Layer

---

## 1. Product Objective

AIRO Finance Lab bertujuan memberikan visibilitas penuh, penguasaan arus kas, dan kenyamanan pencatatan keuangan pribadi harian untuk Owner (Egit) tanpa friksi kognitif.

Tujuan utama MVP adalah membuktikan bahwa Owner dapat:
1. **Mencatat transaksi harian dalam hitungan detik** melalui Telegram Quick Capture atau Dashboard Modal.
2. **Melihat status finansial yang jernih dan real-time** pada Web Dashboard yang cepat (<1 detik).
3. **Memahami kondisi finansial dan pacing anggaran** melalui ringkasan analitik visual serta interaksi tanya-jawab aman dengan AIRO Hermes.

---

## 2. User Problem & Historical Pitfalls

### 2.1 The Daily Friction Problem
Pencatatan keuangan manual sering gagal karena friksi antarmuka: form terlalu panjang, bot terlalu cerewet bertanya (arah -> rekening -> kategori -> subkategori), dan spreadsheet lambat dibuka di ponsel. Akibatnya, transaksi terlewat dan Owner mengalami kebutaan finansial (*financial blindness*).

### 2.2 Historical Failure Modes Avoided (Anti-EAB & Legacy Arfin)
1. **Opaque Apps Script Container Monolith**: Monolit 42.000 baris kode dengan bug *edge-container caching* (`AFPD-INC-012`) menyebabkan perbaikan kode tidak mempan di runtime produksi.
2. **Rigid 4-Turn State Traps**: State machine berbasis teks yang menjebak user dalam siklus pertanyaan berulang ("nomor + pilihan kategori") tanpa jalan keluar.
3. **Premature Automation**: Membangun jembatan lintas-bot (EAB HMAC) dan parser email bank sebelum alur pencatatan manual harian (`catat Rp1 makan`) terbukti stabil dan disukai Owner.
4. **AI-Ledger Entanglement**: AI diizinkan memiliki akses mutasi langsung ke buku besar, menciptakan risiko halusinasi data finansial.

---

## 3. Daily User Workflow

### A. Alur 1: On-The-Go Quick Capture (Telegram)
1. Owner membuka chat Telegram dengan bot mandiri AIRO Finance Lab.
2. Mengetik input natural 1 baris: `makan siang 35k bca`.
3. Engine Finance Core mem-parse teks secara deterministik, menerapkan *sane default* jika akun tidak disebutkan, dan mencatat transaksi.
4. Bot langsung mengembalikan struk konfirmasi ringkas dengan tombol interaktif `[🗑️ Batal (1-Klik)]` dan `[✏️ Ubah Rekening]`.
5. Waktu interaksi: **<5 detik**.

### B. Alur 2: Morning / Evening Financial Review (Dashboard Cockpit)
1. Owner membuka Web Dashboard dari browser laptop atau ponsel.
2. Dashboard memuat dalam <1 detik menampilkan:
   - Total Saldo Likuid & Saldo per Akun (BCA, Blu, Mandiri, Cash).
   - Progres pengeluaran bulan berjalan vs amplop anggaran bulanan (*budget pacing bar*).
   - Daftar 10 transaksi terakhir dengan indikator kategori yang rapi.
3. Owner dapat menambah transaksi manual melalui modal cepat atau memfilter transaksi berdasarkan bulan/kategori.

### C. Alur 3: Ad-Hoc Reasoning & Financial Inquiry (AIRO Hermes)
1. Owner bertanya kepada AIRO Hermes di Telegram: *"Hermes, sisa budget makan bulan ini berapa?"* atau *"Pengeluaran terbesar minggu ini di mana?"*.
2. Hermes memanggil tool read-only ke Finance Core API, mengambil data agregat yang terverifikasi, dan menyusun jawaban cerdas dalam bahasa natural yang santai dan presisi.
3. Hermes **tidak memiliki izin tulis** ke database; semua angka murni berasal dari data riil.

---

## 4. MVP Feature Scope (Strictly Locked)

| Komponen | Fitur In-Scope MVP | Rincian Fungsional |
|---|---|---|
| **1. Web Dashboard** | Overview Cockpit | Saldo per akun aktif, pengeluaran bulan ini, visualisasi budget pacing. |
| | Transaction Explorer | Tabel histori transaksi paginasi, filter bulan/tahun, pencarian catatan. |
| | Quick Manual Entry | Modal web cepat untuk mencatat transaksi manual dari PC/browser. |
| **2. Telegram Capture** | Single-Turn Parser | Regex deterministik angka IDR (`35k`, `50rb`, `1.5jt`, `1250000`) & alias akun/kategori. |
| | Sane Defaults | Otomatis menetapkan akun default (Cash/BCA) jika tidak disebutkan; tidak ada kuis interogasi. |
| | Instant Receipt Card | Struk rapi dengan tombol inline `[Batal / Undo]` untuk pembatalan instan. |
| **3. Finance Core** | Relational Ledger | Engine Python mandiri pengelola mutasi akun dan integritas transaksi. |
| | Soft Invalidation | Pembatalan transaksi menggunakan `status='VOIDED'` untuk integritas jejak audit. |
| **4. Hermes Intelligence** | Read-Only Tools | Tool `get_finance_summary()` dan `get_account_balances()` untuk penalaran AI bebas halusinasi. |

---

## 5. Non-Goals (Explicitly Forbidden in MVP)

Fitur-fitur berikut **DIKUNCI DI LUAR LINGKUP MVP** dan dilarang dikembangkan pada Phase 0–M3:
- ❌ **NO Email Bank Scraping**: Tidak ada parser notifikasi Gmail / mutasi bank otomatis.
- ❌ **NO Multi-Tenant / Enterprise Accounting**: Tidak ada sistem jurnal ganda berbelit-belit atau multi-organisasi.
- ❌ **NO Investment / Gold Scraping**: Tidak ada live ticker saham/kripto atau harga emas harian.
- ❌ **NO Amortization / Debt Engine**: Modul cicilan rumah (KPR) dan kartu kredit bertingkat ditunda.
- ❌ **NO Autonomous AI Writes**: Hermes atau LLM dilarang keras memicu mutasi tulis ke database.
- ❌ **NO Background Schedulers**: Tidak ada cron background otomatis yang berjalan tanpa intervensi.

---

## 6. Definition of Done & Acceptance Criteria

MVP dinyatakan **LULUS (DONE)** jika memenuhi kriteria penerimaan inti:
1. **Pencatatan Cepat Terbukti**: Owner dapat mencatat transaksi via Telegram dalam waktu <5 detik tanpa terjebak *prompt loop*.
2. **Dashboard Real-Time Terbukti**: Dashboard memuat saldo riil dan histori transaksi dengan latensi <1 detik secara konsisten.
3. **Pemahaman Finansial Terbukti**: Owner mendapatkan kejelasan posisi saldo kas dan laju pengeluaran bulanan melalui visual cockpit dan penjelasan Hermes.
4. **Mandatory 7-Day Live Trial**: Owner berhasil menggunakan sistem pencatatan manual ini selama 7 hari berturut-turut tanpa laporan *state deadlocks* atau data korup.
