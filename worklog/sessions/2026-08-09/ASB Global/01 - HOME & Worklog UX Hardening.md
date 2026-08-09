---
type: airo-session
date: 2026-08-09
project: "ASB Global"
objective: "Harden HOME and Worklog human experience, rename the root control-plane from projects to control, and normalize chronology/navigation without losing permanent history."
position: "Post-v0.6 Human Navigation & Worklog Hardening"
status: BELUM_TERBUKTI
can_advance: NO
---

# HOME & Worklog UX Hardening

## 🧭 AIRO STATUS

📍 Project — ASB Global
📌 Lagi di — Post-v0.6 Human Navigation & Worklog Hardening
📈 Progress — Sesi selesai dengan status BELUM_TERBUKTI

🧪 Bukti
Yang wajib ada — Evaluasi bukti kanonis
Yang sudah ada — control/_index.md, control/PROJECT_REGISTRY.tsv, HOME.md, worklog/views/AIRO Worklog.base, worklog/daily/2026-08-09.md
Kesimpulan — BELUM_TERBUKTI
Boleh lanjut — TIDAK

⛔ Hambatan — Tidak ada
➡️ Berikutnya — WAIT_OWNER_POST_IMPLEMENTATION_REVIEW_AND_COMMIT_PUSH_APPROVAL
🏁 Selesai kalau — Definition of Done satisfied

## 🎯 Tujuan sesi
Harden HOME and Worklog human experience, rename the root control-plane from projects to control, and normalize chronology/navigation without losing permanent history.

## 🛠 Yang dilakukan
- Renamed root control-plane projects/ -> control/ (filesystem move, no git mv)
- Migrated canonical references in BOOT/AGENTS/CURRENT/ROADMAP_INDEX/HOME/worklog/scripts/tests
- HOME hardened: Hari Ini / Sesi Terbaru (14d bounded newest-first) / Riwayat Sesi / Control / Keputusan / Pengetahuan
- Updated airo-obsidian-test.py T4/T9/T10 for new view names
- Updated tests/workdesk/test_global_session_project_nav.py for dual-format session schema
- All 5 test suites PASS: 20/20 + 36/36 + 8/8 + 32/32 + 22/22
- Daily regenerated deterministically
- Owner dirty bin/airo-session and ROADMAP_INDEX.md byte-preserved

## 📌 Hasil
- control/ is canonical root control-plane; ecosystem/projects/ unchanged
- HOME no longer dumps unbounded history as primary view
- Sesi Terbaru: 14-day bounded, newest-first, human title as label
- Riwayat Sesi: full permanent history, newest-first
- Internal 01/02 prefix preserved for deterministic ordering
- No HOME section named Project
- stale_wikilinks_after_migration=0

## 🧪 Bukti
- control/_index.md
- control/PROJECT_REGISTRY.tsv
- HOME.md
- worklog/views/AIRO Worklog.base
- worklog/daily/2026-08-09.md

## ⛔ Masalah / hambatan
Tidak ada

## ✅ Keputusan
- control/ is canonical root control-plane name
- ecosystem/projects/ remains unchanged as code/payload workspace
- Dual-format session schema: legacy (project_id+wikilink) and new (plain project string) both accepted
- closed_at deferred to future Owner-approved bin/airo-session update
- archive/inbox/ historical mentions of projects/ preserved as historical record

## 📁 Yang berubah
- `control/`
- `BOOT.md`
- `AGENTS.md`
- `CURRENT.md`
- `HOME.md`
- `ROADMAP_INDEX.md`
- `worklog/README.md`
- `worklog/views/AIRO Worklog.base`
- `worklog/daily/2026-08-09.md`
- `scripts/airo-daily`
- `scripts/airo-promote`
- `scripts/airo-inventory`
- `scripts/airo-manual-queue-status`
- `scripts/airo-obsidian-test.py`
- `tests/workdesk/test_global_session_project_nav.py`

## 📝 Yang belum selesai
- Commit/push pending explicit Owner approval
- Legacy sessions lack provable closed_at — date+sequence DESC fallback used

## ➡️ Berikutnya
WAIT_OWNER_POST_IMPLEMENTATION_REVIEW_AND_COMMIT_PUSH_APPROVAL
