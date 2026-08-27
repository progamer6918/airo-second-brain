---
type: awd-owner-domain-hub
domain: Customer Lifecycle & Repeat Order
date: 2026-08-27
---

# Customer Lifecycle & Repeat Order

> **Program retensi, analisis repeat order, dan pola migrasi model antar-pembelian.**

[[wiki/workdesk/AWD_INDEX|⬅️ AWD — Daftar Isi]] · [[wiki/workdesk/STATUS_DATA#Customer Lifecycle & Repeat Order|🩺 Cek Status Data & Kesehatan Layer]]

---

## 📊 Ringkasan Saat Ini
**Pertanyaan Utama Owner**: *"Seberapa tinggi repeat order konsumen dan bagaimana pola migrasi modelnya?"*

- **Periode Data**: **YTD Jan–Jul 2026** (Sumber sah `CUSTOMER_LIFECYCLE_2026_CURRENT_SUMMARY.tsv`)
- **Total Retail SSU**: **73.968 unit**
- **Jumlah Repeat Order**: **27.738 unit**
- **Tingkat Repeat Order (Overall)**: **37,50%**
- **First-Time Buyer**: **46.230 unit (62,50%)**

---

## 🎯 KPI & Status Domain
- **Repeat Order per Kategori**:
  - Perorangan RO: **37,2%**
  - Perusahaan RO: **52,8%**
- **Jeda Repeat Order (Repeat Gap)**:
  - 18 – 36 Bulan: **68,5%** (Masa pergantian favorit)
  - < 18 Bulan: **14,2%**
  - > 36 Bulan: **17,3%**
- **Perilaku Penggantian**:
  - Maturity Replacement: **58,2%**
  - Segment Upgrade: **54,2%**
  - Retensi Dealer (Dealer Retained): **88,6%** (Konsumen kembali ke dealer yang sama)

---

## 👁️ Apa yang Terlihat
Tabel Perilaku Lifecycle & Repeat Order (YTD Jan–Jul 2026):

| Indikator Lifecycle | Nilai (%) | Catatan Perilaku |
|---|---:|---|
| Rasio Repeat Order | 37,50% | 27.738 unit dari total 73.968 retail |
| Jeda Repeat 18–36 Bulan | 68,5% | Mayoritas konsumen ganti motor di usia 1,5–3 tahun |
| Retensi Dealer | 88,6% | 88,6% konsumen repeat order di dealer yang sama |
| Segment Upgrade | 54,2% | 54,2% konsumen naik kelas segmen kendaraan |
| Same Model Refresh | 32,5% | 32,5% konsumen membeli tipe model yang sama |

---

## 🔍 Rincian & Eksplorasi
Kemampuan eksplorasi lifecycle sah:
1. **Dealer Retention Rate**: Retensi dealer mencapai 88,6%, menunjukkan loyalitas tinggi terhadap outlet awal.
2. **Upgrade Pattern**: 54,2% melakukan segment upgrade (misal: BeAT → Vario/PCX).

---

## 💡 Analisis yang Bisa Diminta
- Analisis peluang program CRM trade-in dan penyapaan kembali konsumen usia kendaraan 2-3 tahun.

---

## 🕘 Riwayat & Tren
### 📊 Rincian Historis Customer Lifecycle

- **⚪ Kapabilitas Historis Lifecycle**: Database mengelola pelacakan repeat order, jeda penggantian (repeat gap 18–36 bulan), serta rasio retensi dealer.
- **Limitation Period-Specific**: Angka rasio historis per tahun terdahulu dikelola secara terpisah dalam basis data transaksi repeat order.

---

## ⚠️ Status & Batasan Data
- Pola dihitung dari agregat nomor rangka/transaksi tanpa mengekspos identitas pribadi individu.

---

## 📚 Referensi Utama
- [[wiki/workdesk/STATUS_DATA#Customer Lifecycle & Repeat Order|Status Data Customer Lifecycle]]
- [[wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY|Registry Customer Lifecycle]]

---

## 🧭 Navigasi Terkait
- [[wiki/workdesk/AWD_INDEX|AWD — Daftar Isi WorkDesk]]
- [[wiki/workdesk/STATUS_DATA|🩺 Status Data WorkDesk]]
