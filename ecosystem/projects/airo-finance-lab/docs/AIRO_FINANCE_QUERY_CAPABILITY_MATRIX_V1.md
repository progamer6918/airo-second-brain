# AIRO Finance Lab — Query Capability Matrix (v1.0)

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_QUERY_CAPABILITY_MATRIX_V1`
- **Status**: `LOCKED_DESIGN_SPECIFICATION`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_LAB_M85_FINANCE_REASONING_GAP_ANALYSIS_V1`
- **Role**: `AIRO Executor Agent`
- **Mode**: `DESIGN_ONLY`
- **Source of Truth**: `AIRO_FINANCE_REASONING_BOUNDARY_V1`, M6-M8 Implementation Evidence

---

## 1. Overview & Evaluation Criteria

Matriks ini memetakan seluruh spektrum pertanyaan finansial yang mungkin diajukan oleh Owner kepada AIRO Hermes, status kesiapan teknis saat ini, data pendukung yang dibutuhkan, tingkat risiko, dan keputusan arsitekturalnya.

### Kriteria Status & Keputusan:
- **Current Support**:
  - `SUPPORTED`: Telah diimplementasikan dan terverifikasi pada M6/M7/M8.
  - `PARTIALLY_SUPPORTED`: Kerangka ada, namun membutuhkan data manual/asumsi eksplisit.
  - `NOT_SUPPORTED`: Belum dapat dilayani karena ketiadaan struktur data di Finance Core.
  - `PROHIBITED`: Dilarang secara arsitektural (melanggar batas AI).
- **Risk Level**:
  - `LOW`: Pertanyaan fakta numerik murni, risiko halusinasi minimal.
  - `MEDIUM`: Perhitungan komparatif yang membutuhkan integritas agregasi.
  - `HIGH`: Interpretasi kondisi keuangan yang jika salah hitung dapat menyesatkan alokasi kas Owner.
  - `CRITICAL`: Rekomendasi tindakan hidup / mutasi data yang dapat merusak kondisi finansial atau buku besar.
- **Decision**:
  - `MAINTAIN`: Pertahankan implementasi saat ini.
  - `ENHANCE_WITH_DETERMINISTIC_MODEL`: Kembangkan read model baru di Finance Core sebelum dibuka ke Hermes.
  - `REFUSE_WITH_OBJECTIVE_FACTS`: Tolak preskripsi, hanya kembalikan angka saldo obyektif.
  - `STRICT_REFUSAL_AND_REDIRECT`: Tolak mutlak dan arahkan ke kanal yang benar.

---

## 2. Query Capability Matrix Table

| No | Question Type (Contoh Pertanyaan) | Level | Current Support | Required Data (Sumber Kebenaran) | Risk Level | Architectural Decision |
|:---:|---|:---:|:---:|---|:---:|---|
| **1** | **Cek Saldo Akun / Total Kas**<br>*(Berapa saldo BCA saya? Berapa total uang saya?)* | Level 1 | `SUPPORTED` | `accounts` table (`AccountOverview` API) | `LOW` | **MAINTAIN**<br>Layanan fakta stabil, 0ms halusinasi. |
| **2** | **Total Pengeluaran / Pemasukan Periode**<br>*(Berapa pengeluaran bulan ini? Berapa pemasukan September?)* | Level 1 | `SUPPORTED` | `transactions` table (`MonthlySummary` API) | `LOW` | **MAINTAIN**<br>Agregasi SQL teruji 100% presisi. |
| **3** | **Histori Transaksi Terakhir**<br>*(Apa 5 transaksi terakhir saya? Tadi pagi catat apa?)* | Level 1 | `SUPPORTED` | `transactions` JOIN `categories` (`RecentActivityItem` API) | `LOW` | **MAINTAIN**<br>Riwayat terurut kronologis akurat. |
| **4** | **Sisa Plafon Anggaran Bulanan**<br>*(Berapa sisa budget makan bulan ini?)* | Level 1 | `SUPPORTED` | `budgets` & `transactions` (`CategorySpendingReport`) | `LOW` | **MAINTAIN**<br>Pacing dan limit anggaran terbaca jelas. |
| **5** | **Kategori Belanja Paling Boros**<br>*(Kategori mana yang paling banyak makan biaya?)* | Level 2 | `SUPPORTED` | `CategorySpendingReport` (Sorting + persentase kalkulatif) | `MEDIUM` | **MAINTAIN**<br>Diolah deterministik oleh Python M6. |
| **6** | **Deteksi Anomali & Transaksi Besar**<br>*(Ada transaksi mencurigakan atau boros tidak?)* | Level 2 | `SUPPORTED` | `SpendingAnomaly` (Aturan $>2.5	imes$ rata-rata, dominasi $>40\%$) | `MEDIUM` | **MAINTAIN**<br>Deteksi berbasis aturan matematis kaku. |
| **7** | **Laju Belanja Harian (Daily Burn Rate)**<br>*(Berapa rata-rata pengeluaran saya per hari?)* | Level 2 | `SUPPORTED` | `MonthlySummary` ($	ext{Total Expense} / 	ext{Day of Month}$) | `MEDIUM` | **MAINTAIN**<br>Kalkulasi in-context terbukti stabil di M8. |
| **8** | **Komparasi Antar-Bulan / Antar-Minggu**<br>*(Apakah bulan ini lebih boros dari bulan lalu?)* | Level 2 | `PARTIALLY_SUPPORTED` | Multi-month transaction dataset (saat ini baru 1 bulan di uji coba) | `MEDIUM` | **ENHANCE_WITH_DETERMINISTIC_MODEL**<br>Perluas `insights.py` untuk mendukung multi-month query saat data bertambah. |
| **9** | **Uang Aman Belanja (Safe-to-Spend)**<br>*(Berapa uang aman saya untuk jajan minggu ini?)* | Level 3 | `NOT_SUPPORTED` | Saldo likuid + Komitmen tagihan rutin + Ambang batas cadangan aman (*safety floor*) | `HIGH` | **ENHANCE_WITH_DETERMINISTIC_MODEL**<br>Dilarang dijawab sebelum ada modul komitmen tetap di Finance Core. |
| **10** | **Kecukupan Saldo Sampai Gajian**<br>*(Apakah saldo saya cukup sampai tanggal gajian?)* | Level 3 | `NOT_SUPPORTED` | Saldo likuid + Tanggal gajian berikutnya + Rata-rata burn rate harian | `HIGH` | **ENHANCE_WITH_DETERMINISTIC_MODEL**<br>Butuh parameter tanggal gajian di sistem sebelum diaktifkan. |
| **11** | **Estimasi Runway Dana Darurat**<br>*(Kalau tidak ada pemasukan, uang saya tahan berapa bulan?)* | Level 3 | `PARTIALLY_SUPPORTED` | Saldo likuid aktif $\div$ rata-rata pengeluaran bulanan minimum | `HIGH` | **ENHANCE_WITH_DETERMINISTIC_MODEL**<br>Dukungan kondisional dengan kewajiban menyatakan batasan asumsi secara eksplisit. |
| **12** | **Simulasi Pengeluaran Tambahan**<br>*(Kalau beli barang 1,5 juta sekarang, sisa saldo aman berapa?)* | Level 3 | `NOT_SUPPORTED` | Saldo likuid saat ini $-$ Pengeluaran simulasi $-$ Safety buffer | `HIGH` | **ENHANCE_WITH_DETERMINISTIC_MODEL**<br>Memerlukan model kalkulator matematis murni di endpoint API insights. |
| **13** | **Kelayakan Pembelian Aset Besar**<br>*(Boleh tidak saya beli mobil / laptop baru bulan ini?)* | Level 4 | `PROHIBITED` | Variabel eksternal subjektif, risiko karier, prioritas hidup non-buku besar | `CRITICAL` | **REFUSE_WITH_OBJECTIVE_FACTS**<br>Tolak keputusan preskriptif; hanya sajikan dampak saldo numerik obyektif. |
| **14** | **Rekomendasi Penempatan Investasi**<br>*(Sisa uang sebaiknya ditaruh di saham mana?)* | Level 4 | `PROHIBITED` | Profil risiko, tren pasar eksternal, regulasi kepatuhan finansial | `CRITICAL` | **STRICT_REFUSAL_AND_REDIRECT**<br>Tolak secara tegas. AIRO Finance bukan manajer investasi. |
| **15** | **Kelayakan Mengambil Utang / Cicilan Baru**<br>*(Apakah saya sanggup cicil rumah 5 juta per bulan?)* | Level 4 | `PROHIBITED` | Analisis solvabilitas jangka panjang & komitmen hidup tak tercatat | `CRITICAL` | **REFUSE_WITH_OBJECTIVE_FACTS**<br>Tolak putusan; tampilkan data cashflow historis murni. |
| **16** | **Perintah Mutasi Tulis via Chat AI**<br>*(Hermes, catatkan pengeluaran makan 40k / transfer uang)* | Out-of-Scope | `PROHIBITED` | Akses mutasi database (DILARANG UNTUK AI) | `CRITICAL` | **STRICT_REFUSAL_AND_REDIRECT**<br>Tolak mutlak (*Zero Writes Rule*); arahkan ke Telegram Quick Capture. |
| **17** | **Pertanyaan Umum Non-Finansial**<br>*(Bagaimana cuaca hari ini? Buatkan resep masakan)* | Out-of-Scope | `NOT_SUPPORTED` | Pengetahuan umum non-domain | `LOW` | **STRICT_REFUSAL_AND_REDIRECT**<br>Tolak secara sopan; arahkan fokus percakapan ke domain keuangan pribadi. |

---

## 3. Identifikasi Kesenjangan Utama (*Key Capability Gaps*)

Berdasarkan matriks di atas, terdapat 3 kesenjangan kritis (*critical gaps*) yang harus dibangun di Finance Core sebelum Hermes diizinkan menjawab pertanyaan Level 3:

```text
1. DATA GAP: COMMITTED EXPENSES (Tagihan Rutin & Kewajiban Tetap)
   - Status Saat Ini: Semua transaksi diperlakukan sama dalam tabel transactions.
   - Solusi Dibutuhkan: Menambahkan penanda transaksi berulang (is_recurring) atau tabel fixed_obligations
     agar sistem tahu uang yang "sudah terkunci" untuk bayar kos/kontrakan, listrik, dan asuransi.

2. PARAMETER GAP: INCOME CADENCE (Siklus Gajian / Payroll Date)
   - Status Saat Ini: Pemasukan hanya tercatat saat transaksi terjadi secara manual.
   - Solusi Dibutuhkan: Menyimpan parameter tanggal gajian rutin (misal: tanggal 25)
     agar formula kecukupan saldo s.d. gajian dapat dihitung secara deterministik.

3. CONFIGURATION GAP: SAFETY FLOOR (Batas Bawah Dana Pengaman)
   - Status Saat Ini: Belum ada konfigurasi nominal saldo minimal yang tidak boleh disentuh.
   - Solusi Dibutuhkan: Parameter batas saldo cadangan aman (misal: Rp2.000.000)
     agar kalkulasi "Safe-to-Spend" tidak mengizinkan saldo terkuras sampai nol rupiah.
```

---

## 4. Lingkup Implementasi Fase Berikutnya (*Next Scope Definition*)

Agar roadmap pengembangan tetap terarah dan tidak mengulang pola overengineering EAB:

1. **JANGAN MEMBUAT AI AGENT BARU**:
   - Hermes tetap sebagai asisten tunggal dengan persona terpadu.
   - Penambahan penalaran dilakukan melalui ekspansi tool/read model, BUKAN menambah agen perantara.
2. **PRIORITAS TAHAP IMPLEMENTASI BERIKUTNYA**:
   - **Fase A (Data Enrichment di Finance Core)**: Tambahkan flag `is_recurring` pada transaksi dan tabel konfigurasi profil pengguna sederhana (`user_finance_profile` untuk `payday_date` dan `safety_floor`).
   - **Fase B (Read Model Baru di `insights.py`)**: Bangun fungsi deterministik `calculate_safe_to_spend()` dan `calculate_payday_runway()`.
   - **Fase C (Adapter Query Mapping di `hermes_adapter.py`)**: Petakan pertanyaan Level 3 ke tool baru tersebut dengan menyertakan aturan penolakan Level 4 yang kaku.
