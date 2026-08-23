---
title: "Promotion & Sales Program Intelligence Layer v1"
component: "Promotion Program Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
source_authority: "Commercial Program Intelligence (COMMERCIAL_PROGRAM_INTELLIGENCE.md, MSW Price Lists 2026, NMS Claim Monitoring, SSU 2024-2026)"
last_updated: "2026-08-23"
---

# 🏷️ Promotion & Sales Program Intelligence Layer v1

## 1. Purpose & Business Context

Promotion & Sales Program Intelligence Layer v1 mentransformasikan data program promosi penjualan retail (*Commercial Sales Program & Discounts*) jaringan dealer Honda periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi efektivitas promosi, tingkat adopsi diler, respon model produk, dan dampak terhadap peningkatan penjualan retail (*Sales Uplift & Incremental Units*).

Layer ini mengevaluasi dampak finansial dan daya tarik program promosi tanpa menggantikan fungsi operasional klaim NMS maupun mengekspos pembagian subsidi internal antara AHM, Main Dealer, dan Dealer.

---

## 2. Parent Contract & Source Authority Relationship

Promotion & Sales Program Intelligence Layer v1 beroperasi secara hirarkis sebagai *child capability* dari Retail Intelligence Engine v2 dan mengintegrasikan 5 dimensi inteligensi retail:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            Promotion & Sales Program Intelligence Layer v1              │
│          (wiki/workdesk/intelligence/PROMOTION_PROGRAM_INTELLIGENCE_V1.md)    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
   ┌───────────────┬─────────────────┼─────────────────┬───────────────┐
   ▼               ▼                 ▼                 ▼               ▼
┌──────────────┐┌──────────────┐  ┌──────────────┐   ┌──────────────┐┌──────────────┐
│Promotion Offer││Sales Activity│  │ Financing    │   │ Product Mix  ││ Retail SSU   │
│(Discounts)   ││(Lead Funnel) │  │ (DP & Tenor) │   │ (Model Code) ││ (Unit Output)│
└──────────────┘└──────────────┘  └──────────────┘   └──────────────┘└──────────────┘
```

### Otoritas Data Sumber:
1. **`COMMERCIAL_PROGRAM_INTELLIGENCE.md`**: `wiki/workdesk/domains/pricing-financing/COMMERCIAL_PROGRAM_INTELLIGENCE.md`
2. **`MSW Price Lists`**: `MSW_CURRENTNESS_RETRIEVAL.md` (Brosur & Price List Resmi Honda SMH 2026)
3. **`NMS Claim Monitoring`**: `NOS_2026_ROW_LEVEL_CANONICAL.tsv` (Monitoring Klaim & Diskon Tambahan Sistem NMS)
4. **`SSU Retail Sales`**: `Retail Sales/SSU 2024.xlsx`, `SSU 2025.xlsx`, `SSU.2026.xlsx`

---

## 3. Privacy Boundary & Public Storage Boundary

### 3.1 Strict Private Raw Exclusion:
Informasi sensitif internal operasional berikut **100% EXCLUDED** dari repositori publik ASB memory:
- Pembagian porsi beban subsidi internal (*Subsidy Margin Split AHM / Main Dealer / Dealer*)
- Identitas pribadi konsumen (`NIK`, Nama Konsumen)
- Rincian ID transaksi klaim individual

### 3.2 Public Derived Intelligence:
Repositori publik ASB hanya menyimpan **fakta agregat terderivasi**:
- Tipe Taksonomi Program Promosi (*Program Type Classification*)
- Masa Berlaku Program (*Program Period / Time-bound Duration*)
- Tingkat Adopsi Diler (*Dealer Program Adoption Rate*)
- Respon Model Produk (*Model Sales Response*)
- Persentase Peningkatan Penjualan (*Sales Uplift % & Incremental Units*)

---

## 4. Canonical Program Classification Taxonomy

Sesuai dengan bukti data promosi resmi, jenis program penjualan diklasifikasikan ke dalam 6 taksonomi kanonis:

1. **`VOUCHER_DISCOUNT`**: Program potongan harga tunai/kredit berbentuk voucher langsung (misal: Voucher Diskon Rp 600.000,-).
2. **`POTONGAN_ANGSURAN`**: Program pemotongan durasi tenor kredit (misal: Potongan Angsuran 1 Bulan untuk Tenor 35 Bulan).
3. **`POTONGAN_DP`**: Program subsidi atau keringanan Uang Muka / Down Payment kredit.
4. **`DIRECT_GIFT_APPAREL`**: Hadiah langsung barang/apparel pendukung unit (misal: Helm/Jaket Spesial CRF, Apparel Touring).
5. **`FINCOY_SUPPORT`**: Program promosi bersama (*joint promo*) dengan perusahaan pembiayaan (*Finco*).
6. **`LOYALTY_RETENTION_PROGRAM`**: Program khusus konsumen setia / tukar-tambah (*Trade-in & Repeat Order Retention*).

---

## 5. Core Metrics & Methodologies

Promotion Program Intelligence mengukur 4 indikator utama:

### 5.1 Program Adoption Rate (Tingkat Adopsi Diler)
Persentase diler aktif yang mengimplementasikan dan mengajukan klaim program promosi:
$$\text{Program Adoption Rate (\%)} = \left( \frac{\text{Jumlah Dealer Berpartisipasi Klaim}}{\text{Total Dealer Aktif}} \right) \times 100$$

### 5.2 Sales Uplift Percentage (Persentase Peningkatan Penjualan)
Mengukur lonjakan laju penjualan retail bulanan selama masa program dibanding garis dasar sebelum program (*Baseline Sales*):
$$\text{Baseline Sales} = \text{Rata-rata Penjualan Retail Daily 3 Bulan Sebelum Program} \times \text{Hari Periode Program}$$
$$\text{Sales Uplift (\%)} = \left( \frac{\text{Actual Sales During Program} - \text{Baseline Sales}}{\text{Baseline Sales}} \right) \times 100$$

### 5.3 Incremental Unit (Penambahan Unit Retail Tambahan)
Jumlah fisik unit motor tambahan yang berhasil dijual sebagai dampak langsung dari program promosi:
$$\text{Incremental Unit} = \text{Actual Sales During Program} - \text{Baseline Sales}$$

### 5.4 Program Conversion Rate (Tingkat Konversi Prospek Program)
Persentase prospek konsumen yang masuk melalui kampanye promosi dan berhasil dikonversi menjadi transaksi SSU yang diklaim:
$$\text{Program Conversion Rate (\%)} = \left( \frac{\text{Claimed Retail Deals SSU}}{\text{Total Program Leads}} \right) \times 100$$
