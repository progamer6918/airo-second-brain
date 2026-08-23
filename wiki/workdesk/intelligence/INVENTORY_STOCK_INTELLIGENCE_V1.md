---
title: "Inventory Stock Intelligence Layer v1"
component: "Inventory Stock Intelligence"
status: "APPROVED / CANONICAL"
version: "1.0"
parent_contract: "wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md"
source_authority: "STOCK_CURRENT_STATE.md, CURRENT_OPERATING_STATE.md, BUSINESS_PULSE.md"
last_updated: "2026-08-23"
---

# 📦 Inventory Stock Intelligence Layer v1

## 1. Purpose & Business Context

Inventory Stock Intelligence Layer v1 mentransformasikan data posisi stok fisik dealer (*Dealer Stock*) dan stok Main Dealer (*MD Stock*) periode **2024, 2025, dan 2026** di bawah arsitektur **Retail Intelligence Engine v2** menjadi inteligensi kesehatan pasokan dan risiko penumpukan stok (*Inventory Health & Aging Risk*).

Layer ini mengevaluasi apakah masalah penjualan di suatu dealer atau wilayah disebabkan oleh masalah permintaan (*demand issue*) atau keterbatasan stok (*supply bottleneck*), melacak hari kecukupan stok (*Stock Days*), mengidentifikasi unit stok menua (*Aging Stock $> 150$ Hari*), dan mengukur distribusi posisi stok (*Ready, Soft Booking, Unfill, Intransit*).

---

## 2. Parent Contract & Source Authority Relationship

Inventory Stock Intelligence Layer v1 beroperasi secara hirarkis sebagai *child capability* dari Retail Intelligence Engine v2 dan mengalirkan data dari Otoritas Stok Resmi yang telah disahkan:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Retail Intelligence Engine v2                      │
│                  (wiki/workdesk/intelligence/RETAIL_INTELLIGENCE_ENGINE_V2.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  Inventory Stock Intelligence Layer v1                  │
│             (wiki/workdesk/intelligence/INVENTORY_STOCK_INTELLIGENCE_V1.md) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│Stock Position & │         │Stock Days &     │         │Aging Risk &     │
│Status Breakdown │         │Health Ratio     │         │Demand-Supply    │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Otoritas Data Sumber:
1. **`STOCK_CURRENT_STATE.md`**: `wiki/workdesk/business-memory/operational/STOCK_CURRENT_STATE.md` (Total Dealer Stock: 5.239 unit; MD Stock: 3.496 unit; Aging $> 150$ hari: 323 unit / 6.17%; Derived Stock Days: 13.27 hari)
2. **`CURRENT_OPERATING_STATE.md`**: `wiki/workdesk/business-memory/operational/CURRENT_OPERATING_STATE.md`
3. **`BUSINESS_PULSE.md`**: `wiki/workdesk/views/BUSINESS_PULSE.md`

---

## 3. Privacy & Public Storage Boundary

Seluruh fakta posisi stok, status kecukupan stok, dan pengelompokan umur stok bersifat **Data Publik Terderivasi (Public Derived Aggregates)**.

Sistem tidak menampilkan sasis individu atau data sensitif internal operasional di luar fakta agregat tingkat dealer/kabupaten yang telah disetujui.

---

## 4. Core Metrics & Methodologies

Inventory Stock Intelligence mengukur 4 dimensi utama:

### 4.1 Stock Position Breakdown
Posisi fisik unit dikategorikan ke dalam 5 status operasional:
- **`READY_STOCK`**: Unit fisik yang siap dijual dan siap dikirim di gudang dealer.
- **`SOFT_BOOKING`**: Unit fisik yang sudah dialokasikan untuk SPK konsumen tetapi belum pelunasan/SSU.
- **`UNFILL_INDEN`**: Unit yang belum tersedia di gudang (*indent*) namun sudah ada pesanan konsumen.
- **`INTRANSIT`**: Unit dalam perjalanan pengiriman dari Main Dealer ke Dealer.
- **`MD_STOCK`**: Stok unit yang berada di gudang Main Dealer (RFS, Booking, NRFS).

### 4.2 Stock Days Formula
Indikator kecukupan stok dihitung berdasarkan selisih stok akhir dibanding rata-rata penjualan retail harian:
$$\text{Daily Retail Rate} = \frac{\text{Retail Units Sold in Current Month}}{\text{Days in Month}}$$
$$\text{Stock Days} = \frac{\text{Ending Dealer Stock}}{\text{Daily Retail Rate}}$$
*Contoh 2026*: Total Dealer Stock 5.239 unit / (Retail Juli 12.241 unit / 31 hari) = **13,27 Hari Stock Days**.

### 4.3 Aging Risk Standard ($> 150$ Hari)
- Unit stok dengan umur tinggal di gudang $> 150$ hari dikategorikan sebagai **`HIGH_AGING_RISK`**.
- *Batas Toleransi Batas Aman*: Presentase unit aging $> 150$ hari idealnya $< 5.0\%$ dari total stok dealer.

### 4.4 Inventory Stock Health Classification
Setiap dealer diklasifikasikan ke dalam 4 tingkatan kesehatan stok:

1. **`OPTIMAL_STOCK_HEALTH`**:
   - **Kriteria**: Stock Days berada dalam rentang ideal **10 – 15 hari** dan unit aging $> 150$ hari $< 5.0\%$.
   - **Diagnosis**: Pasokan dan laju penjualan retail seimbang.

2. **`UNDER_STOCKED_BOTTLENECK`**:
   - **Kriteria**: Stock Days $< 10$ hari dan volume `UNFILL_INDEN` tinggi.
   - **Diagnosis**: Potensi kehilangan penjualan (*lost sales*) karena keterbatasan pasokan unit dari MD.

3. **`OVER_STOCKED_SURPLUS`**:
   - **Kriteria**: Stock Days $> 20$ hari tetapi unit aging $> 150$ hari masih rendah ($< 5.0\%$).
   - **Diagnosis**: Penumpukan stok jangka pendek; perlu percepatan penyaluran retail (*sales push*).

4. **`CRITICAL_AGING_HAZARD`**:
   - **Kriteria**: Unit aging $> 150$ hari $\ge 5.0\%$ dari total stok dealer atau Stock Days $> 25$ hari.
   - **Diagnosis**: Penumpukan stok mati (*aging stock hazard*); wajib dilakukan program pembersihan stok (*stock clearance program*).

---

## 5. Demand vs Supply Diagnostic Matrix

| Symptom / Indicator | Stock Days | Aging > 150d | Root Cause Diagnosis | Action Required |
|---|---|---|---|---|
| Retail Sales Down + Stock Low | $< 10$ hari | $< 3.0\%$ | **Supply Bottleneck** (Keterbatasan Stok) | MD prioritaskan alokasi pengiriman tipe backbone |
| Retail Sales Down + Stock High | $> 20$ hari | $\ge 5.0\%$ | **Demand Problem** (Daya Serap Pasar Rendah / Aging) | Jalankan diskon program clearance & aksi promo lokal |
| High Unfill Inden + Ready Low | $< 8$ hari | $< 2.0\%$ | **High Popularity / Inden Backlog** | Dorong alokasi dari MD stock & percepat intransit |
| Ready High + Soft Booking Low | $> 18$ hari | $3.0\% - 4.9\%$ | **Conversion Bottleneck** | Dorong FLP follow-up prospek untuk konversi SPK |
