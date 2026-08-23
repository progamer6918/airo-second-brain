---
title: "Product Intelligence Layer v1"
component: "Product Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
source_authority: "Retail Sales Authority (SSU 2024, WD-SRC-057 FY2025, SSU.2026.xlsx)"
last_updated: "2026-08-23"
---

# 🛵 Product Intelligence Layer v1

## 1. Purpose & Business Context

Product Intelligence Layer v1 mentransformasikan data penjualan retail per unit (Sales & Stock Unit / SSU) periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi produk terstruktur.

Layer ini menganalisis kontribusi volume per Tipe Motor (`Model Code`), dinamika pergeseran segmen produk (Matik, Cub, Sport, EV), evolusi siklus hidup produk (peluncuran tipe baru vs transisi model lama), serta pengelompokan rentang harga OTR.

---

## 2. Parent Contract & Source Authority Relationship

Product Intelligence Layer v1 beroperasi sebagai *child capability* dari Retail Intelligence Engine v2 dan mengalirkan data dari Otoritas Sumber Resmi yang telah disahkan:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Product Intelligence Layer v1                    │
│                  (wiki/workdesk/intelligence/PRODUCT_INTELLIGENCE_V1.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│Model Share &    │         │Segment Portfolio│         │Lifecycle &      │
│Volume Ranking   │         │& Price Bands    │         │Transition Rules │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Otoritas Data Sumber:
1. **SSU 2024**: `Retail Sales/SSU 2024.xlsx` (SHA256: `31af415f9137dc59c6a22c9dfea0a6869610d53f1de45b33d14162b3912ea380`)
2. **SSU 2025**: `WD-SRC-057__SSU_2025_FULL_YEAR.md` & `Retail Sales/SSU 2025.xlsx` (SHA256: `38e05002d23a6b275b6380bd78e991b8152b70e790c46e7ee543d5bae3891450`)
3. **SSU 2026**: `RETAIL_CURRENT_STATE.md`, `RETAIL_2026_YTD_JUL_TYPE.tsv`, & `Retail Sales/SSU.2026.xlsx` (SHA256: `a9ff25cd2286e285865cf5d79d9d0e77f6f3dd81d874dfd3a61554a04c99f0c3`)

---

## 3. Non-PII Asset Classification Boundary

Seluruh atribut produk (Tipe Motor, Kode Tipe, Deskripsi Komersial, Kode Warna, Segmen, dan Harga OTR) diklasifikasikan sebagai **Non-PII / Public Business Data**.

Atribut produk dapat disimpan, dianalisis, dan ditampilkan secara utuh dalam repositori publik ASB tanpa memerlukan proses anonimisasi atau pengkaburan data.

---

## 4. Methodology & Core Metrics

Product Intelligence mengukur 4 indikator kinerja produk:

### 4.1 Model Volume Contribution
$$\text{Model Contribution (\%)} = \left( \frac{\text{Volume SSU Tipe Motor tertentu}}{\text{Total Volume SSU Regional}} \right) \times 100$$

### 4.2 Segment Share
$$\text{Segment Share (\%)} = \left( \frac{\text{Volume SSU Segmen (Matik/Cub/Sport/EV)}}{\text{Total Volume SSU Regional}} \right) \times 100$$

### 4.3 Price Band Classification
Tipe motor dikelompokkan ke dalam 4 rentang harga OTR (On-The-Road):
- `ENTRY_BAND` ($< \text{Rp 20.000.000}$): Revo Fit, Revo X, Supra X 125, Beat Sporty CBS.
- `MID_BAND` ($\text{Rp 20.000.000} - \text{Rp 25.000.000}$): Beat Street, Scoopy, Genio, Vario 125, CB150 Verza.
- `UPPER_MID_BAND` ($\text{Rp 25.000.000} - \text{Rp 35.000.000}$): Vario 160, Stylo 160, PCX 160, ADV 160, CRF150L.
- `PREMIUM_BAND` ($> \text{Rp 35.000.000}$): CBR150R, CB150R, CBR250RR, CRF250L, EV EM1 e: / CUV e:.

### 4.4 Segment Mapping Standard
- `MATIK_LOW`: Beat Series, Genio Series.
- `MATIK_MID`: Scoopy Series, Vario 125 Series.
- `MATIK_HIGH`: Vario 160 Series, Stylo 160 Series, PCX 160 Series, ADV 160 Series.
- `CUB_LOW`: Revo Series.
- `CUB_MID`: Supra X 125 Series, Supra GTR 150 Series.
- `SPORT_LOW`: CB150 Verza Series.
- `SPORT_MID`: CB150R StreetFire, CB150X, CBR150R, CRF150L.
- `SPORT_HIGH`: CBR250RR, CRF250L.
- `EV_ELECTRIC`: EM1 e:, EM1 e: Plus, ICON e:, CUV e:.

---

## 5. Product Portfolio Classification Taxonomy

Setiap Tipe Motor diklasifikasikan ke dalam 4 kategori portofolio produk:

1. **`BACKBONE_VOLUME_LEADER`**:
   - **Kriteria**: Tipe motor dengan kontribusi volume retail tinggi ($\ge 4\%$ dari total regional) dan menjadi pilar utama pendapatan jaringan dealer.
   - **Contoh**: Beat Street (`MM1`), Beat Sporty CBS (`MJ1`), Revo X (`GD4`), Scoopy Fashion (`MRB`), Scoopy Prestige (`MS1`), Scoopy Stylish (`MSB`), Vario 125 ISS (`NE0`), CRF150L (`ESL`).
   - **Fokus Keputusan**: *Secure Supply & Maintain Stock Days* — Pastikan ketersediaan stok fisik terjaga di angka 10–14 hari.

2. **`GROWTH_LAUNCH_MODEL`**:
   - **Kriteria**: Tipe motor baru atau varian facelift yang menunjukkan pertumbuhan volume MoM yang pesat pasca peluncuran komersial.
   - **Contoh**: Stylo 160 CBS/ABS (`MF1`, `MG1`, `MGA`), PCX 160 CBS/ABS/RoadSync (`MT1`, `MV1`, `MW1`), Beat Facelift 2026 (`MJ2`, `MM2`, `ML2`, `MK2`).
   - **Fokus Keputusan**: *Accelerate Display & Test Ride* — Perluas unit test ride di dealer utama dan prioritaskan alokasi pasokan pengiriman.

3. **`NICHE_SPECIALTY_MODEL`**:
   - **Kriteria**: Tipe motor segmen hobibis/spesialis dengan volume penjualan sedang ($0.2\% - 3.9\%$) namun memiliki citra merek atau margin tinggi.
   - **Contoh**: CB150 Verza (`KG0`), Supra X 125 CW (`GF5`), ADV160 CBS (`NA0`), CBR150R ABS (`KEA`), EV EM1 e: (`ME0`), CUV e: (`MN0`).
   - **Fokus Keputusan**: *Targeted Marketing & Community Activation* — Jalankan event komunitas (HOCI/Club), pameran khusus BTL, dan edukasi konsumen.

4. **`PHASING_OUT_LEGACY`**:
   - **Kriteria**: Tipe motor generasi sebelumnya yang mengalami penurunan volume tajam karena digantikan oleh kode tipe generasi baru (model transition).
   - **Contoh**: Beat rlis awal (`MJ1`, `MM1` pasca rilis `MJ2`/`MM2`), Stylo rilis awal (`MF0`, `MG0`), PCX rilis awal (`MT0`, `MV0`, `MW0`), Vario 160 awal (`LV1`, `LW1`).
   - **Fokus Keputusan**: *Run-out Stock Control & Program Clearance* — Monitor sisa stok dealer untuk mencegah aging stock $> 30$ hari dan terapkan diskon pembersihan unit.

---

## 6. Model Code Generational Transition Rules

Untuk mencegah duplikasi atau distorsi analisis histori saat terjadi pergantian kode tipe AHM:

| Legacy Model Code | New Model Code | Commercial Model Name | Transition Effective | Handling Rule |
|---|---|---|---|---|
| `MJ1` | `MJ2` | Beat Sporty CBS | July 2026 | Gabungkan volume untuk analisis YoY; pisahkan untuk analisis akselerasi facelift |
| `MM1` | `MM2` | Beat Street | July 2026 | Gabungkan volume untuk analisis YoY; pisahkan untuk analisis akselerasi facelift |
| `ML1` | `ML2` | Beat Deluxe Smart Key | July 2026 | Gabungkan volume untuk analisis YoY; pisahkan untuk analisis akselerasi facelift |
| `MK1` | `MK2` | Beat Deluxe ISS | July 2026 | Gabungkan volume untuk analisis YoY; pisahkan untuk analisis akselerasi facelift |
| `MF0` | `MF1` | Stylo 160 CBS | April 2026 | MF0 dianggap phasing-out; MF1 dianggap active growth authority |
| `MG0` | `MG1` / `MGA` | Stylo 160 ABS / Special | April 2026 | MG0 dianggap phasing-out; MG1/MGA dianggap active growth authority |
| `MT0` | `MT1` | PCX 160 CBS | March 2026 | MT0 dianggap phasing-out; MT1 dianggap active growth authority |
| `MV0` | `MV1` | PCX 160 ABS | March 2026 | MV0 dianggap phasing-out; MV1 dianggap active growth authority |
| `MW0` | `MW1` | PCX 160 RoadSync | March 2026 | MW0 dianggap phasing-out; MW1 dianggap active growth authority |
