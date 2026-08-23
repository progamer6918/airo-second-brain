---
title: "Financing Intelligence Layer v1"
component: "Financing Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
source_authority: "Retail Sales Authority (SSU 2024, WD-SRC-057 FY2025, SSU.2026.xlsx)"
last_updated: "2026-08-23"
---

# 💳 Financing Intelligence Layer v1

## 1. Purpose & Business Context

Financing Intelligence Layer v1 mentransformasikan data transaksi penjualan retail (Sales & Stock Unit / SSU) periode **2024, 2025, dan 2026** di bawah pengayoman **Retail Intelligence Engine v2** menjadi inteligensi pembiayaan terstruktur.

Layer ini mengukur rasio skema pembayaran konsumen (**Cash vs Credit**), pangsa pasar Lembaga Pembiayaan (**Finco/Leasing**), rataan Uang Muka Real (**DP Real %**), dan distribusi jangka waktu angsuran (**Tenor**) untuk mendukung keputusan bisnis komersial, penetrasi pasar, dan manajemen risiko kredit dealer.

---

## 2. Parent Contract & Source Authority Relationship

Financing Intelligence Layer v1 beroperasi secara hirarkis sebagai *child capability* dari Retail Intelligence Engine v2 dan tidak membuat otoritas sumber data baru:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Financing Intelligence Layer v1                   │
│                  (wiki/workdesk/intelligence/FINANCING_INTELLIGENCE_V1.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│Cash vs Credit   │         │Finco Market     │         │DP & Tenor       │
│Ratio Analysis   │         │Share & Matrix   │         │Distribution     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Otoritas Data Sumber:
1. **SSU 2024**: `Retail Sales/SSU 2024.xlsx` (SHA256: `31af415f9137dc59c6a22c9dfea0a6869610d53f1de45b33d14162b3912ea380`)
2. **SSU 2025**: `WD-SRC-057__SSU_2025_FULL_YEAR.md` & `Retail Sales/SSU 2025.xlsx` (SHA256: `38e05002d23a6b275b6380bd78e991b8152b70e790c46e7ee543d5bae3891450`)
3. **SSU 2026**: `RETAIL_CURRENT_STATE.md` & `Retail Sales/SSU.2026.xlsx` (SHA256: `a9ff25cd2286e285865cf5d79d9d0e77f6f3dd81d874dfd3a61554a04c99f0c3`)

---

## 3. Data Protection & PII Boundary

Sesuai dengan Aturan Privasi Data (`DATA_USE_RULES.md`) dan Kontrak Eksekusi ASB:
- **100% PII-Sanitized**: Seluruh identitas pribadi konsumen (Nama Konsumen, NIK, No Telepon, Alamat Rumah) dieksklusi sepenuhnya dari memori publik ASB.
- **Sanitized Aggregates Only**: Memori publik ASB hanya menyimpan agregasi persentase skema bayar, pangsa volume Finco, rataan DP %, dan kelompok tenor tanpa mengidentifikasi individu pembeli.

---

## 4. Methodology & Core Metrics

Financing Intelligence mengukur 4 indikator utama:

### 4.1 Credit Ratio
$$\text{Credit Ratio (\%)} = \left( \frac{\text{Volume SSU Kredit}}{\text{Total Volume SSU}} \right) \times 100$$

### 4.2 Finco Market Share
$$\text{Finco Share (\%)} = \left( \frac{\text{Volume SSU Finco tertentu}}{\text{Total Volume SSU Kredit}} \right) \times 100$$

### 4.3 Average Down Payment Real (DP Real %)
$$\text{Avg DP Real (\%)} = \left( \frac{\text{Total Nominal DP Real}}{\text{Total Harga OTR SSU Kredit}} \right) \times 100$$

### 4.4 Tenor Distribution Buckets
Transaksi kredit dikelompokkan ke dalam 4 durasi tenor angsuran:
- `< 12 Bulan`: Tenor pendek (Low risk / High installment)
- `12 - 23 Bulan`: Tenor menengah-pendek
- `24 - 35 Bulan`: Tenor standar umum (Mainstream)
- `> 35 Bulan`: Tenor panjang (High affordability / Extended credit)

---

## 5. Outlet Financing Classification Taxonomy

Setiap Dealer dan POS diklasifikasikan ke dalam salah satu dari 4 kategori inteligensi pembiayaan:

1. **`CASH_DOMINANT`**:
   - **Kriteria**: Rasio penjualan Tunai (Cash) $\ge 50\%$ dari total retail SSU.
   - **Fokus Keputusan**: *Maintain Cash Flow & Up-sell* — Tawarkan paket aksesoris premium, asuransi tambahan, dan program loyalti konsumen tunai.

2. **`BALANCED_FINANCING`**:
   - **Kriteria**: Rasio Kredit $50\% - 79\%$, dengan distribusi pangsa pasar Finco yang sehat (tidak ada Finco tunggal yang menguasai $> 60\%$).
   - **Fokus Keputusan**: *Optimize Partnership* — Pertahankan kerjasama multi-Finco (Tier-1 & Tier-2) dan tingkatkan kelancaran proses approval credit.

3. **`CREDIT_EXPANSION_OPPORTUNITY`**:
   - **Kriteria**: Rasio Kredit $\ge 80\%$, didominasi tenor panjang (35m+), beroperasi di wilayah potensial namun Finco Tier-1 masih belum optimal.
   - **Fokus Keputusan**: *Expand Finco Tier-2 & Joint Promo* — Dorong program subsidi DP ringan dan joint promotion bersama Finco mitra lokal.

4. **`HIGH_RISK_FINANCING_GAP`**:
   - **Kriteria**: Ketergantungan ekstrem pada 1 Finco ($> 70\%$ share) ATAU rataan DP Real sangat rendah ($< 8\%$) dengan rasio penolakan aplikasi kredit tinggi.
   - **Fokus Keputusan**: *Diversify & Audit Credit Hygiene* — Lakukan diversifikasi ke Finco alternatif, audit kecukupan DP, dan evaluasi PICA pembiayaan dealer.

---

## 6. Finco Text Normalization & Alias Mapping Rules

Data mentah SSU mengandung variasi penulisan nama Finco dari berbagai dealer. Financing Intelligence Engine menyatukan variasi tersebut ke dalam Kode Standar Finco:

| Raw Alias Examples in SSU | Normalized Finco Code | Standard Canonical Name |
|---|---|---|
| `FIF`, `PT FIF`, `PT. FIF`, `FIFGROUP`, `FIF GROUP` | `FIFGROUP` | PT Astra Sedaya Finance / FIFGROUP |
| `ADIRA`, `ADIRA FINANCE`, `PT ADIRA`, `PT. ADIRA DINAMIKA` | `ADIRA_FINANCE` | PT Adira Dinamika Multi Finance Tbk |
| `OTO`, `OTO KREDIT MOTOR`, `PT OTO MULTIARTHA` | `OTO_FINANCE` | PT Oto Multiartha |
| `SOF`, `SUMMIT`, `SUMMIT OTO`, `PT SUMMIT OTO FINANCE` | `SUMMIT_AUTO_FINANCE` | PT Summit Oto Finance |
| `BAF`, `BUSSAN`, `PT BUSSAN AUTO FINANCE` | `BAF` | PT Bussan Auto Finance |
| `WOM`, `WOM FINANCE`, `PT WOM FINANCE` | `WOM_FINANCE` | PT Wahana Ottomitra Multiartha Tbk |
| `MTF`, `MANDIRI TUNAS`, `PT MANDIRI TUNAS FINANCE` | `MANDIRI_TUNAS_FINANCE` | PT Mandiri Tunas Finance |
| `BCA FINANCE`, `CSUL FINANCE`, `IMFI`, `OTHER`, `LAINNYA` | `OTHER_FINCO` | Other Regional Financing Partners |
