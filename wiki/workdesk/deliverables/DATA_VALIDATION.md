---
type: workdesk-blueprint
project: AIRO_WORKDESK
domain: deliverable
workdesk_status: ACTIVE
audience: human-ai
---

# 📄 Blueprint — Data Validation Before Presentation

## 🍼 10 detik
Daftar periksa (checklist) validasi kualitas data sebelum menyajikan laporan atau presentasi ke manajemen.

## 📋 Validation Checklist (10 Langkah)

1. **Cek Konsistensi Scope**: Wilayah dan segmen produk sama di seluruh lembar kerja.
2. **Cek Denominator**: Pembagi perhitungan Market Share (Total Market) menggunakan angka yang terverifikasi.
3. **Cek Rekonsiliasi Total**: Jumlah total segmen/dealer sama dengan angka total area.
4. **Cek Periode**: Tanggal rilis data aktual vs target berada dalam horizon waktu yang sama.
5. **Cek Formula Pencapaian**: `Achievement % = (Aktual / Target) * 100`.
6. **Cek Rumus Growth**: `Growth % = ((Periode Ini - Periode Lalu) / Periode Lalu) * 100`.
7. **Cek Kebocoran Data Kosong**: Tidak ada sel bernilai NULL/N/A yang menyebabkan rumus error (`#DIV/0!`).
8. **Cek Konsistensi Tabel & Grafik**: Angka di tabel persis sama dengan grafik visual.
9. **Cek Perbandingan Angka Presentasi vs File Excel**: Angka di slide PPT cocok 100% dengan lembar analisis Excel.
10. **Cek Timestamp Source**: Sumber data dicantumkan dengan jelas di bagian bawah laporan.

## 🔗 Evidence & Source
- `WD-SRC-084` Data Analytics; `WD-SRC-096` Power BI Sales Dashboard.
