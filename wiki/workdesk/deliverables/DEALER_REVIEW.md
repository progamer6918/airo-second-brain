---
type: workdesk-blueprint
project: AIRO_WORKDESK
domain: deliverable
workdesk_status: ACTIVE
audience: human-ai
---

# 📄 Blueprint — Dealer Review

## 🍼 10 detik
Blueprint standar untuk menyusun dokumen laporan atau lembar kerja evaluasi bulanan/kuartalan outlet dealer Honda (H1/H2/H3/AHASS/Wing/BigWing).

## 📥 Input Requirements

| Kategori | Item | Tipe Input |
|---|---|---|
| **REQUIRED** | Kode & Nama Dealer, Periode Review, Target vs Penjualan Aktual | AUTO_RESOLVE_FIRST |
| **REQUIRED** | Data Days of Inventory (DOI) Stock & Manpower Count | AUTO_RESOLVE_FIRST |
| **OPTIONAL** | Hasil audit NOS 2026 terbaru | AUTO_RESOLVE_FIRST |
| **OPTIONAL_OWNER_CONTEXT** | Catatan khusus kesepakatan owner dealer sebelumnya | OWNER_REQUIRED |

## 🏗 Struktur Blueprint Deliverable

1. **Executive Summary**: Ringkasan performa dealer (Green / Yellow / Red status).
2. **Key Performance Indicators (KPI)**: Target vs Retail sales, Market share wilayah, DOI stock.
3. **Kontekstual Pasar & Area**: Isu ekonomi lokal, pergerakan kompetitor di area dealer.
4. **Evaluasi Manpower & Produktivitas**: Jumlah FLP, produktivitas per head, conversion rate sales funnel.
5. **Aktivitas BTL & Event**: Frekuensi acara, jumlah prospek terkumpul, tingkat konversi.
6. **Komersial & Pembiayaan**: Rasio Cash vs Credit, approval rate fincoy, komposisi DP.
7. **Standar Eksekusi Jaringan (NOS)**: Evaluasi Premises, Process, dan People.
8. **Akar Masalah (RCA)**: Pemisahan antara gejala umum dengan akar masalah operasional.
9. **Formulir PICA**: Tabel perbaikan terkuantifikasi (Issue → Root Cause → PI → CA → PIC → Timeline → Control).

## 🚦 Quality Gate (Syarat Siap Pakai)
- [x] Rasio penjualan dan perbandingan target menggunakan periode yang konsisten.
- [x] Penyebab utama tidak didasarkan pada asumsi tanpa data pendukung.
- [x] Setiap item aksi memiliki penanggung jawab (PIC) dan batas waktu (due date).

## 🔗 Evidence & Source
- `WD-SRC-027` slides 20–24; `WD-SRC-004` slide 4; `WD-SRC-056` Form Dealer Review.
