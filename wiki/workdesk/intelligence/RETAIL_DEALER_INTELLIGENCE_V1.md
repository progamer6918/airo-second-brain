---
title: "Retail Dealer Intelligence Layer v1"
component: "Dealer Intelligence"
source_authority: "WD-SRC-057__SSU_2025_FULL_YEAR.md"
---

# 🏢 Retail Dealer Intelligence Layer v1

## 1. Purpose
Retail Dealer Intelligence Layer v1 menstimulasi dan mentransformasi data Retail Sales Authority (`WD-SRC-057` / FY2025 107,108 unit baseline) menjadi inteligensi keputusan tingkat dealer (`Group` ➔ `Dealer` ➔ `POS`).

Dokumen ini mendefinisikan metode analisis kontribusi penjualan retail, atribusi wilayah, dan logika klasifikasi status kinerja dealer/POS.

---

## 2. Source Authority Reference
- **Primary Source**: `WD-SRC-057__SSU_2025_FULL_YEAR.md`
- **Business Memory**: `RETAIL_SALES_2025_FULL_YEAR_SUMMARY.md`
- **Operating Currentness**: `RETAIL_CURRENT_STATE.md` & `SSU.2026.xlsx`
- **PII Boundary**: Data ter-sanitasi penuh. HANYA agregasi volume retail, pangsa kontribusi, dan status kualitatif yang disimpan di public ASB.

---

## 3. Methodology & Dealer Contribution Model

### 3.1 Contribution Calculation
$$	ext{Retail Share Pct (\%)} = \left( rac{	ext{Dealer FY2025 Retail Volume}}{	ext{Total Regional Retail Volume (107,108)}} ight) 	imes 100$$

### 3.2 Classification Logic

1. **`BACKBONE`** (Strategic Pillar Dealer):
   - **Kriteria**: Menyumbang kontribusi penjualan retail tinggi ($\ge 10\%$ dari total volume regional) DAN menjaga kestabilan kinerja pencapaian target.
   - **Fokus Keputusan**: *Defend & Maintain* — Pastikan ketersediaan pasokan stok utama dan dukungan aktivitas komersial reguler.

2. **`GROWTH_OPPORTUNITY`** (Upside Potential Dealer/POS):
   - **Kriteria**: Beroperasi di territory/kecamatan dengan potensi pasar besar (Ring 2/3), namun kontribusi retail masih sedang ($5\% - 9.9\%$).
   - **Fokus Keputusan**: *Expand & Invest* — Alokasikan program promosi khusus (BTL), penambahan armada kanvasing FLP, dan penetrasi wilayah.

3. **`ATTENTION`** (Performance/Productivity Gap Dealer/POS):
   - **Kriteria**: Kontribusi retail rendah ($< 5\%$) ATAU mengalami penurunan MoM volume penjualan dan gap Indeks Produktivitas FLP ($< 70\%$).
   - **Fokus Keputusan**: *Investigate & Correct* — Jalankan audit operasional NOS 2026, siapkan tindakan korektif PICA, dan jadwalkan supervisory review.

---

## 4. Decision Support Usage Examples

- **Kueri**: *"Dealer mana yang menjadi backbone penjualan retail?"*
  - **Jawaban AIRO Sync**: Merekap dealer dengan status `BACKBONE` (misal: Sinsen Sarolangun Main Outlet, Sinsen Jambi Main Outlet).
- **Kueri**: *"Dealer atau POS mana yang punya opportunity pertumbuhan?"*
  - **Jawaban AIRO Sync**: Menampilkan outlet `GROWTH_OPPORTUNITY` beserta territory target (misal: POS Singkut, POS Pelawan).
- **Kueri**: *"Outlet mana yang memerlukan attention?"*
  - **Jawaban AIRO Sync**: Menyajikan daftar outlet `ATTENTION` beserta indikasi root cause (gap produktivitas FLP / BTL).

---

## 5. Permanent Dealer Entity Resolution Rule & Scope Validation

Setiap proses analitik, diagnostik, dan agregasi inteligensi diler **WAJIB OBEY** aturan tata kelola entitas (*Permanent Entity Resolution Rule*):

1. **`Dealer Group Matching Rule`**: Keanggotaan diler di dalam suatu grup (*Dealer Group*) **WAJIB HANYA ACU** ke field `Dealer_Master.Group`. Dilarang keras melakukan inferensi dari nama PT, nama diler, pola kepemilikan (*ownership*), perusahaan induk (*parent company*), atau sister company.
2. **`Area Definition Rule`**: Penentuan wilayah diler (*Area*) **WAJIB HANYA ACU** ke field `Dealer_Master.Area` administratif resmi (misal: `KOTA JAMBI`, `KAB. MUARO JAMBI`, `KAB. BATANG HARI`, `KAB. TANJUNG JABUNG BARAT`). Dilarang membuat penamaan area manual (misal: Jambi 1/Jambi 2) atau menginferensi dari lokasi kecamatan.
3. **`Forbidden Inference Boundary`**:
   - Dilarang memperluas keanggotaan diler berdasarkan kesamaan merek/lokasi.
   - Dilarang menggabungkan entitas independen ke dalam grup utama tanpa basis `Dealer_Master.Group`.
4. **`Scope Validation Flag`**:
   `ENTITY_SCOPE_VALIDATION_REQUIRED=YES`

