---
type: awd-owner-domain-hub
domain: Stock Kendaraan
date: 2026-08-27
---

# Stock Kendaraan

> **Monitoring ketersediaan stok, keseimbangan supply-demand, dan aging.**

[[wiki/workdesk/AWD_INDEX|⬅️ AWD — Daftar Isi]] · [[wiki/workdesk/STATUS_DATA#Stock Kendaraan|🩺 Cek Status Data & Kesehatan Layer]]

---

## 📊 Ringkasan Saat Ini
**Pertanyaan Utama Owner**: *"Berapa stok kendaraan yang ada dan bagaimana keseimbangannya?"*

- **Tanggal Snapshot**: **6 Agustus 2026 (08:03 WIB)**
- **Total Stok Dealer**: **5.239 unit**
- **Total Stok Main Dealer (MD)**: **3.496 unit**
- **Estimasi Stock Days Dealer (DERIVED)**: **13,27 hari** *(Formula: `Dealer Stock / (Jul Retail / 31)` = `5.239 / (12.241 / 31)`)*

---

## 🎯 KPI & Status Domain
- **Komposisi Stok Dealer (5.239 unit)**:
  - Ready: **3.495 unit** (66,71%)
  - Soft Booking: **803 unit** (15,33%)
  - Unfill: **593 unit** (11,32%)
  - Intransit: **348 unit** (6,64%)
- **Stok Old Aging Dealer (>150 hari)**: **323 unit** (6,17% dari total stok)
- **Komposisi Stok MD (3.496 unit)**:
  - RFS (Ready for Sale): **3.362 unit**
  - Booking: **105 unit**
  - NRFS (Not Ready for Sale): **29 unit**
  - Rakitan: 2026 = 3.446 unit / 2025 = 50 unit

---

## 👁️ Apa yang Terlihat
Tabel Distribusi Aging Stok Dealer (Snapshot 6 Aug 2026):

| Rentang Aging (Hari) | Jumlah Stok (Unit) | Persentase (%) | Status Kesehatan |
|---|---:|---:|---|
| 0 – 30 hari | 3.862 | 73,72% | 🟢 Fresh Stock |
| 31 – 60 hari | 526 | 10,04% | 🟢 Normal |
| 61 – 90 hari | 252 | 4,81% | 🟡 Perlu Perhatian |
| 91 – 120 hari | 162 | 3,09% | 🟡 Slow Moving |
| 121 – 150 hari | 114 | 2,18% | 🟠 Warning |
| > 150 hari | 323 | 6,17% | 🔴 Critical Aging |
| **Total Stok Dealer** | **5.239** | **100,00%** | |

*Daftar Outlet/POS dengan Stock-Days Tertinggi (Perhatian Khusus)*:
1. **POS PATRIA - SIJENJANG**: Stock Days **29,11 hari** (Stok 77 / Jul retail 82 / >90: 10 / >150: 5)
2. **POS PATRIA - PAUH**: Stock Days **28,56 hari** (Stok 82 / Jul retail 89 / >90: 2 / >150: 0)
3. **POS TUNAS JAMBI - BULURAN**: Stock Days **28,53 hari** (Stok 81 / Jul retail 88 / >90: 21 / >150: 7)
4. **POS PATRIA - BUNGO**: Stock Days **27,90 hari** (Stok 81 / Jul retail 90 / >90: 8 / >150: 2)
5. **PT. DAYA ANUGRAH MANDIRI - BAHAR**: Stock Days **25,61 hari** (Stok 114 / Jul retail 138 / >90: 27 / >150: 20)

---

## 🔍 Rincian & Eksplorasi
Kemampuan eksplorasi stok kendaraan sah:
1. **Dealer Stock Detail**: Breakdown per dealer & POS (`DEALER_STOCK_2026-08-06_AGGREGATE.tsv`).
2. **Derived Stock Days**: Rasio kecukupan stok per outlet (`DEALER_STOCK_DAYS_2026-08-06_DERIVED.tsv`).
3. **MD Stock Aggregate**: RFS, Booking, NRFS (`MD_STOCK_2026-08-06_AGGREGATE.tsv`).

---

## 💡 Analisis yang Bisa Diminta
- Diagnosa stok penumpukan (>150 hari) per dealer dan varian warna.
- Analisis keseimbangan pasokan MD vs kebutuhan retail dealer.

---

## 🕘 Riwayat & Tren
### 📊 Riwayat Snapshot Stok Kendaraan

- **Snapshot Mode**: Stok kendaraan dikelola berbasis snapshot point-in-time operasional (`DEALER_STOCK_2026-08-06_SUMMARY.tsv` & `INVENTORY_STOCK_2026_CURRENT_SUMMARY.tsv`).
- **Snapshot Point-in-Time 6 Aug 2026**: 5.239 unit Dealer / 3.496 unit MD. Snapshot historis sebelumnya diarsipkan sebagai pembanding per tanggal pengunduhan tanpa merekayasa tren tahunan buatan.

---

## ⚠️ Status & Batasan Data
- Rincian aging stok MD **TIDAK TERSEDIA (NOT_AVAILABLE)** dalam data sumber MD. Dilarang menggunakan tahun rakitan sebagai proxy aging stok MD.
- Angka Stock Days (13,27 hari) adalah hasil kalkulasi turunan (DERIVED) menggunakan retail Juli 2026.

---

## 📚 Referensi Utama
- [[wiki/workdesk/STATUS_DATA#Stock Kendaraan|Status Data Stock]]
- [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Registry Stock]]

---

## 🧭 Navigasi Terkait
- [[wiki/workdesk/AWD_INDEX|AWD — Daftar Isi WorkDesk]]
- [[wiki/workdesk/STATUS_DATA|🩺 Status Data WorkDesk]]
