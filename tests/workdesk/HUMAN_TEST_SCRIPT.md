---
type: workdesk-test-script
project: AIRO_WORKDESK
audience: human-tester
duration_minutes: 10
---

# 🧪 Zero-Context Human Test Script (Obsidian UX)

## Tujuan
Menguji apakah pengguna manusia tanpa konteks awal (zero-context human) dapat menemukan informasi, memahami peran Area Sales Supervisor, mendiagnosis masalah bisnis, dan menghasilkan output deliverable menggunakan Obsidian AIRO WorkDesk dalam waktu <= 10 menit tanpa perlu diajari istilah teknis.

## 📋 Instruksi Bagi Penguji (Tester)
- Jangan membuka folder explorer di sidebar kiri jika tidak diminta.
- Gunakan hanya link interaktif di dalam halaman atau fitur pencarian Obsidian (`Ctrl + O` / `Ctrl + Shift + F`).
- Jangan melihat kunci jawaban atau file TSV di folder `evidence/`.

---

## 🎯 Tugas 1: Onboarding & Peran (2 Menit)
1. Buka halaman utama `HOME.md`.
2. Klik jalur **Belajar dari nol** (`START_HERE.md`).
3. Cari penjelasan 10-detik mengenai apa itu peran **Area Sales Supervisor (ASS)**.
4. *Pertanyaan Verifikasi*: Apakah ASS hanya mengawasi sales orang, atau mengelola performance bisnis area secara menyeluruh?

## 🎯 Tugas 2: Diagnosis Masalah Bisnis (3 Menit)
1. Kembali ke `HOME.md`.
2. Skenario: *"Penjualan sepeda motor segmen AT High di area Anda mengalami penurunan selama 2 bulan berturut-turut."*
3. Pilih rute **Selesaikan masalah** atau jalan pintas **AT High underperform**.
4. *Pertanyaan Verifikasi*: Sebutkan 3 hal pertama yang wajib diverifikasi sebelum mengusulkan program promo/diskon.

## 🎯 Tugas 3: Pembuatan Output Kerja / Deliverable (3 Menit)
1. Dari `HOME.md`, klik rute **Pilih output kerja** (`DELIVERABLE_INDEX.md`).
2. Pilih deliverable **Formulir PICA**.
3. *Pertanyaan Verifikasi*: Sebutkan 4 komponen utama yang wajib ada dalam tabel PICA (Problem Identification & Corrective Action).

## 🎯 Tugas 4: Peta Dunia Kerja & Sistem (2 Menit)
1. Buka halaman `WORK_WORLD_MAP.md` (atau visual canvas `WORK_WORLD_MAP.canvas`).
2. Temukan bagaimana peran ASS menghubungkan domain **Market**, **Dealer**, **Commercial**, dan **Leadership**.
3. *Pertanyaan Verifikasi*: Jika skor NOS dealer rendah tetapi penjualan tinggi, domain mana yang perlu dicek untuk kepatuhan jangka panjang?

---

## 📝 Lembar Evaluasi Penguji (Scoring Sheet)

| Tugas | Waktu Tempuh | Berhasil Tanpa Bantuan? (Ya/Tidak) | Tingkat Kemudahan (1-5) | Catatan Masukan |
|---|---|---|---|---|
| 1. Onboarding & Peran | ___ menit | [ ] Ya  [ ] Tidak | ___ / 5 | |
| 2. Diagnosis Masalah | ___ menit | [ ] Ya  [ ] Tidak | ___ / 5 | |
| 3. Output / PICA | ___ menit | [ ] Ya  [ ] Tidak | ___ / 5 | |
| 4. Peta Dunia Kerja | ___ menit | [ ] Ya  [ ] Tidak | ___ / 5 | |

**Status Penerimaan Pengguna Manusia**:
- [ ] `ZERO_CONTEXT_HUMAN_ACCEPTANCE=PASS` (Jika seluruh tugas completed <= 10 menit tanpa kendala navigasi)
- [x] `ZERO_CONTEXT_HUMAN_ACCEPTANCE=NOT_YET` (Status default sebelum sesi pengujian manusia aktual dilaksanakan oleh Owner)
