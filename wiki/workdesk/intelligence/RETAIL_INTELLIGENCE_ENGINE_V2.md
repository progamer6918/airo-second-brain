---
title: "Retail Intelligence Engine v2 Foundation Contract"
component: "Retail Intelligence Engine"
status: "APPROVED / CANONICAL"
version: "2.0"
source_authority: "Retail Sales Authority (SSU 2024, WD-SRC-057 FY2025, SSU.2026.xlsx)"
last_updated: "2026-08-23"
---

# 🛒 Retail Intelligence Engine v2 Foundation Contract

## 1. Purpose & Overview

Retail Intelligence Engine v2 adalah arsitektur inteligensi bisnis retail terpadu di dalam ekosistem **AIRO WorkDesk (AWD)**. Arsitektur ini menyatukan data penjualan retail (Sales & Stock Unit / SSU) periode **2024, 2025, dan 2026** ke dalam satu struktur inteligensi keputusan multidimensi tanpa melanggar batasan privasi data (PII) maupun hak cipta/otoritas data sumber.

Engine ini berfungsi sebagai pusat penghubung (hub) yang mentransformasikan data transaksi mentah menjadi 7 domain inteligensi keputusan yang dapat digunakan oleh seluruh operator AIRO Sync dan sistem analitik WorkDesk.

---

## 2. Source Authority Relationship

Retail Intelligence Engine v2 **TIDAK** membuat otoritas data baru, melainkan mengalirkan dan menstrukturkan data dari Otoritas Data Sumber (Source Authorities) yang telah disahkan:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        Retail Sales Authorities                         │
│  - 2024: Retail Sales/SSU 2024.xlsx (Historical Comparable)             │
│  - 2025: WD-SRC-057 SSU 2025 Full Year Baseline (107,108 units)           │
│  - 2026: Retail Sales/SSU.2026.xlsx YTD Jan-Jul (73,968 units)          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│Sales Intel      │         │Dealer Intel     │         │Territory Intel  │
└─────────────────┘         └─────────────────┘         └─────────────────┘
         │                           │                           │
         ▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│Product Intel    │         │Financing Intel  │         │Customer Seg.    │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │FLP Intel        │
                            └─────────────────┘
```

### Otoritas Sumber Resmi per Periode:
1. **SSU 2024**: `Retail Sales/SSU 2024.xlsx` (SHA256: `31af415f9137dc59c6a22c9dfea0a6869610d53f1de45b33d14162b3912ea380`) — Otoritas historis pembanding FY2024.
2. **SSU 2025**: `WD-SRC-057__SSU_2025_FULL_YEAR.md` & `Retail Sales/SSU 2025.xlsx` (SHA256: `38e05002d23a6b275b6380bd78e991b8152b70e790c46e7ee543d5bae3891450`) — Otoritas historis pembanding penuh FY2025 (107,108 unit).
3. **SSU 2026**: `RETAIL_CURRENT_STATE.md` & `Retail Sales/SSU.2026.xlsx` (SHA256: `a9ff25cd2286e285865cf5d79d9d0e77f6f3dd81d874dfd3a61554a04c99f0c3`) — Otoritas operasional berjalan 2026 (YTD Jan–Jul: 73,968 unit).

---

## 3. Raw Data vs Sanitized Public Memory Boundary

Untuk mematuhi Aturan Privasi Data (`DATA_USE_RULES.md`) dan Kebijakan Repositori Publik ASB (`BOOT.md`), Retail Intelligence Engine v2 menerapkan pemisahan ketat antara data mentah (Private Raw) dan memori publik (Public Business Memory):

1. **Private Raw Layer (Sidecar / Local Registry)**:
   - Menyimpan berkas mentah `.xlsx` yang berisi identitas pribadi konsumen (Nama, NIK, No Telepon, Alamat Lengkap) serta nomor unik aset (`No Mesin`, `No Rangka`).
   - Berkas mentah dilarang keras di-commit ke dalam repositori publik ASB.
2. **Sanitized Public Memory Layer (ASB Markdown / TSV)**:
   - Menyimpan hasil ekstrak agregasi faktual (Volume per Dealer/POS, Volume per Kabupaten/Kecamatan, Volume per Tipe/Segment, Rasio Cash/Credit, Distribusi Tenor).
   - Data demografis konsumen dikonversi menjadi kategori anonim (misal: Kelompok Umur, Kategori Pekerjaan) tanpa identitas individu.

---

## 4. Intelligence Layer Hierarchy & Domain Breakdown

Retail Intelligence Engine v2 mengorganisir 7 sub-domain inteligensi bisnis:

### 4.1 Sales Intelligence
- **Fokus**: Tren volume retail bulanan, pola musiman (peak months), pertumbuhan YoY/MoM, serta pencapaian target penjualan regional.
- **Keluaran**: Volume total regional, rataan penjualan bulanan, dan indeks pertumbuhan retail.

### 4.2 Dealer Intelligence (`RETAIL_DEALER_INTELLIGENCE_V1.md`)
- **Fokus**: Distribusi penjualan tingkat outlet (`Group` ➔ `Dealer` ➔ `POS`), kontribusi retail terhadap total regional, dan klasifikasi kinerja outlet.
- **Taksonomi Klasifikasi**:
  - `BACKBONE`: Kontribusi retail $\ge 10\%$ regional, kinerja stabil.
  - `GROWTH_OPPORTUNITY`: Beroperasi di wilayah potensial, kontribusi $5\% - 9.9\%$.
  - `ATTENTION`: Kontribusi $< 5\%$ atau mengalami penurunan volume MoM tajam.

### 4.3 Territory Intelligence (`TERRITORY_INTELLIGENCE_V1.md`)
- **Fokus**: Atribusi geografis retail ke dalam struktur 9 Kabupaten/Kota, 118 Kecamatan, dan 1,223 Kelurahan-Desa serta penetrasi Ring wilayah.
- **Taksonomi Klasifikasi**:
  - `BACKBONE`: Market share Honda $\ge 70\%$ (Ring 1 Core).
  - `GROWTH_OPPORTUNITY`: Market share Honda $45\% - 69\%$ (Ring 2 POS).
  - `ATTENTION`: Market share Honda $< 45\%$ (Ring 3 White-space).

### 4.4 Product Intelligence
- **Fokus**: Performa penjualan berdasarkan Tipe Motor (`Model Code`), Nama Komersial, Warna, dan Segmen Produk (Matik, Sport, Cub, EV).
- **Keluaran**: Product mix ratio, analisis tipe backbone (misal: MM1, MJ1, GD4), dan evaluasi transisi produk.

### 4.5 Financing Intelligence
- **Fokus**: Komposisi skema pembayar retail (Cash vs Credit), pangsa pasar lembaga pembiayaan (Finco/Leasing), rasio Down Payment Real (DP %), dan distribusi tenor angsuran.
- **Keluaran**: Indeks kesehatan kredit dealer, Finco share per wilayah, dan kesesuaian program pembiayaan.

### 4.6 Customer Segment Intelligence
- **Fokus**: Profil demografis konsumen ter-anonimisasi (Kelompok Umur, Pekerjaan, Kategori Pembeli Repeat Customer / First-time Buyer).
- **Keluaran**: Pemetaan target segmen pembeli per tipe produk dan wilayah.

### 4.7 FLP Intelligence
- **Fokus**: Produktivitas tenaga penjual Front Line People (FLP), rataan unit terjual per FLP, dan efisiensi konversi lead sales ke retail SSU.
- **Keluaran**: Indeks Produktivitas FLP per dealer/POS dan evaluasi kebutuhan pengembangan tim sales.

---

## 5. Cross-Year Comparability & Normalization Rules (2024 - 2026)

Untuk memastikan perbandingan antar-tahun yang valid dan bebas dari bias data:

1. **Unit Grain Standard**:
   - 1 Unit SSU disetarakan secara ketat dengan **1 No Mesin terverifikasi** yang telah mencapai serah terima retail.
2. **Comparable Period Alignment**:
   - Analisis YTD 2026 vs 2025 wajib membandingkan rentang bulan yang identik (misal: YTD Jan–Jul 2026 vs YTD Jan–Jul 2025).
   - Penggunaan data pembanding 2025 wajib mengacu pada `WD-SRC-057` (107,108 unit baseline) untuk level full-year, atau `RETAIL_2025_YTD_JUL_DEALER_HISTORICAL.tsv` untuk YTD Jul.
3. **POS Standardization Adjustment**:
   - Perubahan pengkodean dan penyatuan POS tahun 2026 (per `Pengkodean POS_Sinsen_Aug 2026.xlsx`) dirujuk balik ke Dealer Main Outlet induknya saat membandingkan histori 2024/2025.
4. **Target Context Guard**:
   - Jika target bulanan/tahunan tidak tersedia pada berkas sumber mentah tertentu, analisis wajib mencantumkan status `TARGET_NOT_SUPPLIED` dan dilarang mengasumsikan angka target buatan.

---

## 6. Data Integrity & Validation Safeguards

1. **Zero Duplicate Rule**: Tidak boleh ada 2 sumber retail yang saling mengeklaim sebagai Otoritas Utama untuk periode yang sama.
2. **No Memory Drift**: Hasil agregasi publik ASB harus selalu dapat ditelusuri ke checksum SHA256 berkas sumber mentah di `OPERATIONAL_DATA_INVENTORY.tsv`.
3. **Strict Path Execution**: Seluruh pembacaan data dan pengoperasian engine wajib mematuhi aturan penulisan repositori ASB.

---

## 7. Permanent Dealer Entity Resolution Governance & Scope Safeguards

Seluruh child capability dan mesin penalaran diagnostik yang beroperasi di bawah Retail Intelligence Engine v2 **WAJIB MENENTUKAN DILER & AREA BERDASARKAN DEALER MASTER SAH**:

1. **`Dealer Group Resolution`**: Keanggotaan diler di dalam suatu grup (*Dealer Group*) **WAJIB MENGGUNAKAN** `Dealer_Master.Group`.
2. **`Area Administrative Validation`**: Penentuan wilayah (*Area*) **WAJIB MENGGUNAKAN** `Dealer_Master.Area` administratif resmi.
3. **`Forbidden Inference Boundary`**:
   - Dilarang keras melakukan inferensi dari nama perusahaan (PT/CV), nama diler, kepemilikan saham (*ownership*), perusahaan sister/induk, maupun lokasi geografis.
   - Dilarang membuat pengelompokan wilayah manual (misal: Jambi 1/Jambi 2) yang tidak bersumber dari `Dealer_Master.Area`.
4. **`Scope Validation Requirement`**:
   `ENTITY_SCOPE_VALIDATION_REQUIRED=YES`

