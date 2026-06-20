---
type: wiki-concept
title: "Runtime Sync"
status: draft
canonical: false
last_reviewed: ""
tags: ["concept", "sync", "runtime", "infra"]
sources:
  - path: "wiki/sources/runtime-sync-repair-19f3bd5.md"
    commit: "19f3bd5c12be8c61726a111b05fc698504f7c191"
    section: "Key evidence"
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
---

# Runtime Sync

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
Runtime Sync adalah mekanisme sinkronisasi latar belakang yang berjalan secara periodik untuk memastikan perubahan pada repositori lokal (ASB) terkirim ke remote repository Git (GitHub) secara aman dan konsisten.

## Current understanding
- **Kepemilikan Scheduled Task (Windows Scheduled Task Ownership)**: Proses sinkronisasi dipicu secara berkala oleh Windows Task Scheduler melalui berkas pembungkus `AIRO-SecondBrain-Sync.vbs` yang menjalankan skrip WSL (Status: implemented).
- **WSL Runtime Runner**: Skrip runner utama (`airo-runtime-runner.sh`) mengelola alur Git fetch, deteksi konflik, polling Telegram gateway, pemeriksaan kesehatan, dan sinkronisasi perubahan aman (Status: implemented).
- **Penanganan Worktree Kotor (Safe Handling of Dirty Worktrees)**:
  - Jika repositori lokal kotor tetapi setara dengan remote, rebase diabaikan dengan kode `SAFE_REBASE_SKIPPED_DIRTY_WORKTREE` dan proses tetap berlanjut (Status: implemented).
  - Jika remote memiliki pembaruan baru sementara worktree lokal kotor, sinkronisasi otomatis dinonaktifkan (`degraded_sync_disabled`) dengan status `DEGRADED_REMOTE_SYNC_BLOCKED` untuk mencegah konflik (Status: implemented).
- **Peran Lock dan Guard (Writer-Lock and Secret-Guard Role)**:
  - Writer lock `/tmp/airo-second-brain-runtime.lock` mencegah eksekusi runner ganda yang saling bertabrakan (Status: implemented).
  - File sensitif lokal yang kotor (seperti skrip antrean manual) dilindungi dari Git cleanup otomatis (Status: implemented).
- **Bukti Kesiapan Runtime Terdegradasi (Current Degraded Health Evidence)**: Status Second Brain saat ini diklasifikasikan sebagai terdegradasi (`degraded`) karena adanya berkas modifikasi lokal yang belum dilakukan commit, meskipun infrastruktur runtime tetap berjalan aktif (Status: degraded).

## Relationships
- `uses` [Canonical Knowledge](canonical-knowledge.md) — Melindungi integritas berkas kanonik selama sinkronisasi.
- `uses` [Telegram Gateway](telegram-gateway.md) — Berjalan beriringan dengan gateway Telegram di bawah pemicu scheduler yang sama.

## Evidence
Pengujian statis di skrip `airo-runtime-runner-static-test.py` memverifikasi bahwa enam berkas terlarang dilindungi dari pembersihan Git yang tidak aman, dan VBS mengembalikan kode keluar yang benar.

## Contradictions or uncertainty
Penanganan divergensi Git tingkat lanjut tidak diotomatiskan dan akan memblokir sinkronisasi secara permanen hingga dilakukan penggabungan (merge) manual oleh operator.

## Canonical implications
Proses sinkronisasi otomatis tidak boleh menggunakan perintah sapu bersih (`git add .`) untuk mencegah terstagenya berkas sensitif atau berkas lokal yang tidak disetujui.

## Provenance
- `wiki/sources/runtime-sync-repair-19f3bd5.md` (Commit: `19f3bd5c12be8c61726a111b05fc698504f7c191`, Seksi: "Key evidence").
