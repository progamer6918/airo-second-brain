# AIRO Second Brain v0.6 M3 HOME Base Runtime Correction Record

- **Date:** 2026-08-05
- **Task:** `asb_v06_m3_home_base_runtime_correction`
- **Scope:** `ASB_GLOBAL`
- **Owner Visual Confirmation:** `OWNER_REAL_OBSIDIAN_VISUAL_CONFIRMATION=PENDING`

---

## 🧭 AIRO STATUS

📍 Project — ASB_GLOBAL  
📌 Lagi di — M3 HOME Base Runtime Correction Selesai; Siap verifikasi visual Owner  
📈 Progress — Memperbaiki skema berkas `AIRO Worklog.base` ke format resmi native Obsidian Bases YAML

🧪 Bukti  
Yang wajib ada — Perbaikan skema `filters`/`displayName`/`order` pada `AIRO Worklog.base`, pengujian negatif skema lama, pemindaian dataset independen (berkas `.pyc` dan non-sesi 0 match), pengujian 20 skenario `scripts/airo-obsidian-test.py` (20/20 PASS), regresi M1-M4 (100% PASS), preservasi 29 berkas Owner  
Yang sudah ada — Seluruh pengujian deterministik PASS, visual confirmation PENDING menunggu Owner membuka `HOME.md` di Obsidian  
Kesimpulan — BERHASIL  
Boleh lanjut — YA (Menunggu verifikasi visual Owner sebelum M5)  

⛔ Hambatan — Tidak ada  
➡️ Berikutnya — Owner membuka `HOME.md` di Obsidian untuk verifikasi rendering  
🏁 Selesai meyakinkan — Skema Base diperbaiki deterministik dan terverifikasi secara statis  

---

## Root Cause Analysis & Incident Record

- **Problem:** When Owner opened `HOME.md` in the real Obsidian vault, the "Hari Ini" Base view rendered approximately 6,998 unrelated vault files (including `.pyc` compiled Python files).
- **Root Cause:** The `AIRO Worklog.base` file previously used invalid/outdated top-level keys (`filter:`, `label:`, `fields:`) instead of the official native Obsidian Bases YAML schema (`filters:`, `displayName:`, `order:`). Obsidian ignored the invalid filter keys and displayed an unfiltered vault-wide dataset by default.
- **Correction:** 
  1. Updated `worklog/views/AIRO Worklog.base` to use exact official native Obsidian Bases YAML syntax (`file.inFolder("worklog/sessions")`, `file.ext == "md"`, `type == "airo-session"`, `displayName`, `order`).
  2. Strengthened `scripts/airo-obsidian-test.py` to reject legacy invalid keys (`filter`, `label`, `fields`) and verify strict native schema compliance (`BASE_NATIVE_SCHEMA_KEYS=PASS`).
  3. Added an independent dataset scan verifying that only valid `airo-session` notes under `worklog/sessions` match (`UNEXPECTED_PYC_MATCH_COUNT=0`, `UNEXPECTED_NON_SESSION_MATCH_COUNT=0`).
  4. Added a negative fixture test proving that `.pyc` files and arbitrary markdown files outside `worklog/sessions` are excluded.
