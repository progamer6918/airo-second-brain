---
type: awd-owner-domain-hub
domain: Dealer & POS
date: 2026-08-27
---

# Dealer & POS

> **Penilaian kapasitas, kontribusi, dan jangkauan jaringan penjualan Dealer, POS, dan FLP.**

[[wiki/workdesk/AWD_INDEX|⬅️ AWD — Daftar Isi]] · [[wiki/workdesk/STATUS_DATA#Dealer & POS|🩺 Cek Status Data & Kesehatan Layer]]

---

## 📊 Ringkasan Saat Ini
**Pertanyaan Utama Owner**: *"Dealer/POS mana perform, bermasalah, dan kenapa?"*

- **Status Domain**: **🟠 Sebagian** (Hierarki Dealer → POS → FLP tersedia; total jaringan acuan terkini belum terkonfirmasi)
- **Batas Periode Asinkron (Multi-domain)**:
  - Retail: Juli 2026 (`RETAIL_2026_YTD_JUL_DEALER.tsv`)
  - Market Share: Juni 2026
  - Stock Kendaraan: 6 Agustus 2026

---

## 🎯 KPI & Status Domain
- **Hierarki Jaringan**: Dealer Group → Main Dealer → POS → Sales Force
- **Jumlah Dealer Dipantau (SSU)**: 28 Jaringan Dealer
- **Integrasi Domain**: Penjualan, Stok, Manpower, dan Activity terikat pada kode Dealer/POS

---

## 👁️ Apa yang Terlihat
Struktur Jaringan Penjualan:
- **Dealer Group**: Kelompok dealer utama
- **POS (Point of Sales)**: Pos jualan cabang bawahan
- **FLP Roster**: Alokasi 384 headcount sales force per POS (`FLP_2026_CURRENT_SUMMARY.tsv`)

---

## 🔍 Rincian & Eksplorasi
Kemampuan eksplorasi jaringan yang tersedia:
1. **Performa Retail per Dealer**: Volume kontribusi retail per dealer dari 28 dealer terdaftar.
2. **Evaluasi Stok per POS**: Identifikasi POS dengan stok berlebih atau kritis (`DEALER_STOCK_DAYS_2026-08-06_DERIVED.tsv`).

---

## 💡 Analisis yang Bisa Diminta
- Diagnosa outlet dengan produktivitas rendah.
- Analisis kecukupan man power FLP per dealer group.

---

## 🕘 Riwayat & Tren
### 📊 Rincian Historis Jaringan Dealer (2025)

- **Rekam Jaringan 2025**: Jaringan 28 dealer terdaftar aktif (`RETAIL_2025_YTD_JUL_DEALER_HISTORICAL.tsv`).
- **Top 3 Dealer Kontributor 2025 (YTD Jul)**:
  1. **PT PATRIA ANUGRAH SENTOSA - JAMBI**: **3.125 unit**
  2. **PT ASTRA INTERNATIONAL TBK - HONDA**: **2.964 unit**
  3. **PT DAYA ANUGRAH MANDIRI - JAMBI**: **1.944 unit**

---

## ⚠️ Status & Batasan Data
- Status domain 🟠 Sebagian. Total semesta Dealer/POS terkini tidak boleh direkayasa sebelum konfirmasi data acuan induk final.

---

## 📚 Referensi Utama
- [[wiki/workdesk/STATUS_DATA#Dealer & POS|Status Data Dealer]]
- [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Registry Dealer]]

---

## 🧭 Navigasi Terkait
- [[wiki/workdesk/AWD_INDEX|AWD — Daftar Isi WorkDesk]]
- [[wiki/workdesk/STATUS_DATA|🩺 Status Data WorkDesk]]
