# AIRO Finance Lab — Execution Rules & Governance v1.0

- **Project**: `AIRO_FINANCE_LAB`
- **Document ID**: `AIRO_FINANCE_LAB_EXECUTION_RULES_V1`
- **Status**: `LOCKED_PHASE_0_CANONICAL`
- **Date**: `2026-09-11`
- **Task**: `AIRO_FINANCE_LAB_PHASE0_DOCUMENTATION_LOCK_V1`
- **Product Identity Lock**: **Personal Finance Intelligence Application**
- **Authority**: Governance & Anti-EAB Safeguard Policy

---

## 1. Mandatory Implementation Principles

Setiap prompt eksekusi, agen AI, dan engineer yang bekerja di AIRO Finance Lab wajib mematuhi 5 aturan mutlak berikut:

### Rule 1: Small Reversible Steps
- Setiap task harus dipecah menjadi unit kerja terkecil yang independen dan dapat diverifikasi (*bounded slice*).
- Setiap langkah harus memiliki prosedur *rollback* yang jelas sebelum perubahan diaplikasikan.
- Hindari *big-bang releases* atau refactor skala besar sekaligus.

### Rule 2: Evidence Before Completion
- Status `EXIT_CODE=0` atau unit test hijau saja **BUKAN BUKTI PENYELESAIAN TUGAS**.
- Penyelesaian tugas (*verdict BERHASIL*) wajib dibuktikan dengan runtime readback riil, hash kecocokan data, dan penerimaan langsung oleh Owner (*Owner smoke test*).
- Dilarang mengklaim fitur selesai jika belum diuji pada lingkungan live pengguna.

### Rule 3: No Scope Expansion (Scope Firewall)
- Ruang lingkup MVP dibatasi secara ketat hanya pada apa yang tercantum di `AIRO_FINANCE_LAB_MVP_PRD_V1.md`.
- Setiap ide baru, perbaikan estetika non-esensial, atau fitur "bagus kalau ada" yang muncul di tengah sprint wajib dialirkan ke `inbox/backlog` dan ditandai `DEFERRED`.
- Dilarang keras menyisipkan fitur baru ke milestone yang sedang berjalan.

### Rule 4: No Automation Before Validation (The 7-Day Rule)
- Dilarang membuat otomatisasi latar belakang (email bank scraper, cron triggers, sinkronisasi otomatis) sebelum alur pencatatan manual divalidasi oleh Owner.
- Alur pencatatan manual (Telegram capture & Dashboard modal) wajib digunakan dan disukai oleh Owner selama **7 hari berturut-turut** sebelum otomatisasi Phase M5 diizinkan.

### Rule 5: No AI Write Access to Ledger
- AIRO Hermes dan model LLM lainnya **DILARANG KERAS MEMILIKI AKSES MUTASI TULIS LANGSUNG KE BUKU BESAR**.
- Hermes adalah *intelligence and reasoning layer*, bukan juru tulis database.
- Hermes hanya boleh memanggil endpoint Read-Only untuk mengambil context ringkasan finansial.
- Semua mutasi transaksi wajib diinisiasi langsung oleh manusia (Owner) atau parser deterministik berbasis aturan pasti.

---

## 2. Anti-EAB Pattern Prevention Safeguards

Pola-pola kegagalan historis pada proyek pendahulu dilarang keras diulang:

| Pola Kegagalan EAB / Legacy Arfin | Larangan Mutlak di Finance Lab | Mekanisme Pencegahan |
|---|---|---|
| **Giant Monolith** | Dilarang menggabungkan webhook, parser, HTML, formatting cell, dan query dalam 1 file raksasa (seperti 42k baris Apps Script). | Modular Python architecture: pisahkan router API, engine validasi, dan data models ke file terpisah (<200 baris per modul). |
| **State Machine Panjang** | Dilarang membuat percakapan bertingkat kaku (tanya arah -> tanya akun -> tanya kategori -> tanya subkategori). | Alur atomik Single-Turn Parse-and-Confirm. Terapkan *sane defaults* cerdas dan sediakan tombol 1-klik undo. |
| **Hidden Automation** | Dilarang menyalakan trigger/scheduler tersembunyi yang beroperasi tanpa sepengetahuan Owner. | Semua eksekusi harus eksplisit, transparan, dan tercatat di `audit_logs`. |
| **Feature Creep** | Dilarang menambahkan integrasi cross-bot, scraper investasi, atau cicilan kompleks pada tahap awal. | MVP dikunci strictly hanya pada 5 tabel dan 3 alur utama (Dashboard, Telegram Capture, Hermes Read-Only). |

---

## 3. Stop-Loss & Single Retest Failure Rule

Untuk mencegah pemborosan token dan waktu debug berulang-ulang:
1. **Batas 1 Siklus Perbaikan**: Jika terjadi *bug* atau kegagalan tes pada tahap implementasi, tim eksekutor hanya diizinkan melakukan **tepat 1 siklus perbaikan kausal**.
2. **Kriteria Henti (STOP & REPLAN)**: Jika pengujian ulang kedua (*second retest*) masih gagal, eksekusi **WAJIB SEGERA DIHENTIKAN**.
3. Dilarang melakukan *looping trial-and-error* tanpa bukti kausal baru. Masalah harus dilaporkan ke Owner untuk peninjauan arsitektur ulang.

---

## 4. Format Laporan & Penerimaan Harian

- Komunikasi kepada Owner menggunakan **Bahasa Indonesia**.
- Kode, dokumentasi teknis, dan PRD menggunakan **Bahasa Inggris**.
- Setiap laporan substantif wajib menggunakan header tanda terima resmi:
  ```text
  🧭 EXECUTOR RECEIPT
  ```
- Pelaporan output eksekusi wajib menyertakan verifikasi bukti clipboard melalui helper kanonis `scripts/airo-clipboard-receipt`.
