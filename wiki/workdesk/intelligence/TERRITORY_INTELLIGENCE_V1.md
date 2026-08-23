---
title: "Territory Intelligence Layer v1"
component: "Territory Intelligence"
source_authority: "POLREG 2026 & SINSEN_EVALPOLREG & WD-SRC-057"
---

# 🗺️ Territory Intelligence Layer v1

## 1. Purpose
Territory Intelligence Layer v1 menghubungkan struktur geografis wilayah operasi PT Sinar Sentosa Primatama (9 Kabupaten/Kota, 118 Kecamatan, 1,223 Kelurahan-Desa) dengan atribuisi tanggung jawab dealer (`Group` ➔ `Dealer` ➔ `POS`) dan hasil kontribusi penjualan retail.

Dokumen ini mendefinisikan klasifikasi daya serap pasar per wilayah (Ring 1/2/3) dan matriks penetrasi pasar untuk mendukung pengambilan keputusan strategis.

---

## 2. Source Authority References
- **Geographic Filter Authority**: `POLREG PER KECAMATAN PER KELURAHAN PER SEGMENT 2026.xlsx` (118 Kecamatan / 1,223 Kelurahan)
- **Market Share Authority**: `SINSEN_EVALPOLREG+MSPERKAB_JUN 2026.xlsx` (9 Kabupaten)
- **Retail Volume Baseline**: `WD-SRC-057__SSU_2025_FULL_YEAR.md` (FY2025 107,108 unit) & `RETAIL_CURRENT_STATE.md`
- **PII Boundary**: Data ter-sanitasi penuh (agregasi wilayah, kecamatan, dealer, dan status kualitatif tanpa PII).

---

## 3. Territory Hierarchy & Data Relationship Model

```text
Kabupaten (9 Kabupaten/Kota)
  ↓
Kecamatan (118 Kecamatan)
  ↓
Kelurahan / Desa (1,223 Mapped Rows)
  ↓
Dealer Coverage (Ring 1 Core / Ring 2 POS / Ring 3 White-space)
  ↓
Retail Contribution & Market Share Penetration (%)
```

---

## 4. Territory Classification Logic

1. **`BACKBONE`** (High Volume & Dominant Share Territory):
   - **Kriteria**: Kecamatan/Wilayah di Ring 1 dengan pangsa pasar Honda $\ge 70\%$ DAN menyumbang kontribusi retail signifikan bagi dealer utama.
   - **Fokus Keputusan**: *Defend Market Leadership* — Jaga ketersediaan unit H123, efisiensi layanan AHASS, dan kepuasan pelanggan.

2. **`GROWTH_OPPORTUNITY`** (High Potential / Upside Territory):
   - **Kriteria**: Kecamatan/Wilayah di Ring 2 atau Ring 3 dengan total pasar besar namun pangsa pasar Honda masih di kisaran $45\% - 69\%$.
   - **Fokus Keputusan**: *Expand Coverage & Penetration* — Tambah jaringan POS/kanvasing, tingkatkan BTL event, dan optimalkan produktivitas FLP.

3. **`ATTENTION`** (Low Penetration / Underperforming Territory):
   - **Kriteria**: Kecamatan/Wilayah di mana pangsa pasar Honda $< 45\%$ ATAU mengalami penurunan kontribusiMoM yang tajam.
   - **Fokus Keputusan**: *Investigate & Correct* — Lakukan audit pemetaan kompetitor, evaluasi kesesuaian lokasi POS, dan siapkan rekomendasi PICA.

---

## 5. Usage & Decision Support Examples

- **Kueri**: *"Kecamatan mana di Kabupaten Sarolangun yang menjadi backbone?"*
  - **Jawaban AIRO Sync**: Menampilkan Kecamatan Sarolangun Kota (Ring 1) sebagai *BACKBONE* territory.
- **Kueri**: *"Wilayah mana yang memiliki opportunity pertumbuhan terbanyak?"*
  - **Jawaban AIRO Sync**: Menyajikan Kecamatan Singkut dan Pelawan (Ring 2) sebagai *GROWTH_OPPORTUNITY* territory.
- **Kueri**: *"Kecamatan mana yang memerlukan attention/perbaikan pasar?"*
  - **Jawaban AIRO Sync**: Menyajikan daftar kecamatan dengan penetrasi di bawah target beserta indikasi gap jaringan/FLP.
