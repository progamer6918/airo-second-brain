---
type: wiki-synthesis
title: "AIRO Second Brain Operational Architecture"
status: draft
canonical: false
created_at: "2026-06-20T17:17:00+07:00"
last_reviewed: ""
tags:
  - synthesis
  - architecture
  - acceptance-test
sources:
  - path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
    commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
    section: "1. Purpose"
  - path: "docs/validation/AIRO_EARESMES_GATEWAY_DURABILITY_20260618.md"
    commit: "50034df009ac7bc08455ef2ee7806c03891b4669"
    section: "Key evidence"
  - path: "ops/runtime/airo-runtime-runner.sh"
    commit: "19f3bd5ac93edd273989f8681a498e1b42e9c2f5"
    section: "Key evidence"
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
---

# AIRO Second Brain Operational Architecture

This note is derivative. Canonical AIRO sources remain authoritative.

## Question
Bagaimana arsitektur operasional, hubungan agen, dan ketahanan runtime sistem AIRO Second Brain berjalan saat ini berdasarkan bukti validasi nyata?

## Executive synthesis
Dokumen ini menyintesis arsitektur operasional AIRO Second Brain (ASB) dengan menyelaraskan dokumen PRD v0.5.1, bukti ketahanan gateway Earesmes, dan perbaikan runtime sinkronisasi. Sistem ini berhasil menggabungkan visualisasi lokal [Obsidian](../concepts/obsidian.md) dengan distilasi pengetahuan semi-otomatis [LLM Wiki](../concepts/llm-wiki.md) di bawah aturan Truth Hierarchy yang ketat.

## Current implemented architecture
Arsitektur operasional ASB yang aktif saat ini dirancang sebagai repositori memori bersama (shared-memory) berbasis Git yang berlokasi lokal di WSL (ASB_REPO) (Status: implemented). Antarmuka visual yang digunakan adalah [Obsidian](../concepts/obsidian.md), yang membuka repositori Git ini langsung dari Linux/WSL (Status: implemented). Di latar belakang, terdapat runtime sinkronisasi (`airo-runtime-runner.sh`) yang dijalankan oleh Windows Scheduled Task melalui `AIRO-SecondBrain-Sync.vbs` untuk memicu sinkronisasi otomatis ke remote GitHub (`origin main`) (Status: implemented).

## Agent and runtime relationships
Hubungan antar-komponen didefinisikan sebagai berikut:
- [Earesmes](../concepts/earesmes.md) bertindak sebagai persona asisten utama, "Chief of Staff", dan Resident Orchestrator lokal dalam ekosistem AIRO yang melayani interaksi alami dengan pemilik (owner) lewat Telegram (Status: implemented).
- [Telegram Gateway](../concepts/telegram-gateway.md) (`telegram-gateway.py`) adalah gerbang depan penerima pesan Telegram dengan metode polling tunggal (`getUpdates`) (Status: validated). Ia memindahkan pesan ke antrean lokal dan mengirimkan balasan kembali.
- Hermes Worker (`airo-hermes-worker.service`) adalah layanan Linux latar belakang yang memproses antrean pesan secara asinkron menggunakan model AI lokal, sepenuhnya terisolasi dari kegagalan Telegram Gateway (Status: validated).
- [AIRO Second Brain](../concepts/airo-second-brain.md) (ASB) adalah repositori pengetahuan bersama (shared-memory) terpusat tempat Earesmes menggunakannya untuk hidrasi konteks di awal sesi dan mendaftarkan closeout sesi untuk menjaga kontinuitas memori (Status: implemented).

## Implemented, validated, specified, deferred, and degraded
Status komponen di ekosistem AIRO Second Brain saat ini didefinisikan secara tegas sebagai berikut:
- **Implemented:**
  - Repositori bersama Git lokal di WSL (Status: implemented).
  - Struktur repositori pengetahuan dan skrip runner sinkronisasi `airo-runtime-runner.sh` (Status: implemented).
  - Persona Earesmes sebagai Resident Orchestrator (Status: implemented).
- **Validated:**
  - Ketahanan Telegram Gateway (`telegram-gateway.py`) dengan pemicu otomatis Windows Scheduled Task setiap 5 menit (Status: validated).
  - Isolasi Hermes Worker latar belakang sebagai systemd service (Status: validated).
  - Penanganan repositori kotor (dirty worktree) pada sinkronisasi dengan logic `SAFE_REBASE_SKIPPED_DIRTY_WORKTREE` (Status: validated).
- **Specified:**
  - Proses organisasi malam (nightly processing) pada jam 22.00 local time (Status: specified).
  - Aliran orkestrasi ujung-ke-ujung otomatis (end-to-end loop) (Status: specified).
- **Deferred:**
  - Mutasi asisten Earesmes penuh (ditunda hingga Milestone M6) (Status: deferred).
  - Integrasi sinkronisasi data Notion (Status: deferred).
- **Degraded:**
  - Kesehatan runtime Second Brain saat ini diklasifikasikan terdegradasi (`degraded`) karena adanya modifikasi file lokal yang belum staged/committed (Status: degraded).
  - Kinerja waktu respons Earesmes yang memakan waktu sekitar 21 detik (Status: degraded).

## Durability evidence
Bukti ketahanan (durability) dan keunikan poller Telegram Gateway divalidasi melalui pengujian kegagalan terkendali pada 18 Juni 2026 (Status: validated):
- **Single Poller:** Proses `telegram-gateway.py` dikonfirmasi sebagai satu-satunya penangan polling `getUpdates` (GATEWAY_COUNT=1, legacy poller count=0). Tidak ada poller sekunder yang aktif untuk menghindari perebutan token Telegram (Status: validated).
- **Durability & Auto Recovery:** Windows Scheduled Task `AIRO Earesmes Telegram Listener` dikonfigurasi dengan pemicu logon dan pengulangan setiap 5 menit (PT5M), serta opsi `MultipleInstances=IgnoreNew` dan batas waktu eksekusi tidak terbatas.
- **Uji Kegagalan:** Ketika gateway ber-PID 18992 dimatikan dengan sinyal SIGTERM, ia mati secara bersih. Pada jadwal Scheduled Task berikutnya, gateway baru otomatis dipicu dengan PID 20505, sementara Hermes worker (PID 18482) tetap aktif tanpa terputus (Status: validated).

## Runtime sync and current health
- **Cara Kerja Runtime Sync:** Proses sinkronisasi dipicu secara periodik oleh Windows Scheduled Task melalui `AIRO-SecondBrain-Sync.vbs` yang memanggil skrip WSL `airo-runtime-runner.sh` (Status: implemented). Runner ini melakukan Git fetch, polling pesan, memeriksa antrean manual, memperbarui status kesehatan (`airo-health`), dan melakukan sinkronisasi aman (`airo-sync`) ke remote GitHub.
- **Penanganan Worktree Kotor:** Skrip runner mencegah kegagalan fatal akibat file kotor lokal:
  - Jika repositori lokal kotor tetapi setara dengan remote, rebase dilewati secara aman (`SAFE_REBASE_SKIPPED_DIRTY_WORKTREE`) (Status: implemented).
  - Jika remote ahead dan repositori lokal kotor, sinkronisasi dinonaktifkan (`degraded_sync_disabled`) dengan peringatan `DEGRADED_REMOTE_SYNC_BLOCKED` (Status: implemented).
- **Penyebab Status Degraded:** Status kesehatan terkini di `state/system-health.md` bernilai terdegradasi (`degraded`) karena repositori `airo-second-brain` ditandai kotor (`truth_status: dirty`) akibat adanya modifikasi berkas konfigurasi lokal (seperti `.obsidian/` dan skrip antrean manual) yang belum dimasukkan ke area pementasan Git (Status: degraded).

## Obsidian and LLM Wiki authority
- **Obsidian:** Bertindak sebagai antarmuka membaca bagi manusia, Markdown editor, visualisasi grafik tautan, dan kokpit navigasi (Status: implemented). Obsidian membuka repositori Git lokal (ASB_REPO) secara langsung dari WSLg Linux filesystem (Status: implemented).
- **LLM Wiki:** Bertindak sebagai lapisan pengetahuan derivatif yang bertugas mendistilasi dan mengintegrasikan informasi dari berbagai sumber menjadi catatan terstruktur melalui skill seperti `wiki-ingest` dan `wiki-query` (Status: implemented).
- **Batasan Otoritas (Authority Boundaries):**
  - [Obsidian](../concepts/obsidian.md) maupun [LLM Wiki](../concepts/llm-wiki.md) **bukan otoritas kanonik utama**. Berkas kanonik (seperti PRD, keputusan pemilik, `SECURITY.md`) tetap menjadi sumber kebenaran tertinggi (Truth Hierarchy) (Status: implemented).
  - Obsidian Sync dan Publish dinonaktifkan sepenuhnya.
  - LLM Wiki dilarang melakukan komit Git otomatis, pembersihan repositori yang merusak, promosi kanonik secara otomatis, atau memodifikasi file kanonik tanpa otorisasi formal pemilik (Status: implemented).

## Supporting evidence
- [PRD v0.5.1](../sources/airo-second-brain-prd-v0-5-1.md) — Spesifikasi kanonik orkestrasi dan repositori memori bersama.
- [Gateway Durability](../sources/earesmes-gateway-durability-50034df.md) — Laporan uji kegagalan terkendali Telegram gateway.
- [Runtime Sync Repair](../sources/runtime-sync-repair-19f3bd5.md) — Skrip perbaikan runtime runner dan data static-test.
- [Canonical Knowledge](../concepts/canonical-knowledge.md) — Hub utama model kebenaran kanonik.
- [Runtime Sync](../concepts/runtime-sync.md) — Konsep sinkronisasi latar belakang yang terkelola.

## Conflicting evidence
Tidak ditemukan bukti konflik fungsional yang signifikan, namun latensi respons Earesmes (~21 detik) menunjukkan ketidaksesuaian dengan ekspektasi akses real-time cepat ^[inferred].

## Inferences
Mekanisme Windows Scheduled Task yang memicu ulang gateway setiap 5 menit dianggap cukup memadai untuk menjaga ketahanan sistem dalam skenario kegagalan biasa ^[inferred].

## Open questions
Bagaimana cara menekan latensi waktu respons Earesmes dari ~21 detik menjadi di bawah 5 detik tanpa mengubah arsitektur worker Hermes secara drastis?

## Canonical implications
Semua hasil olahan LLM Wiki di bawah folder `wiki/` bersifat derivatif, sehingga kebenaran mutlak selalu mengacu pada berkas kanonik asli repositori Git.

## Provenance
- `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md` (Commit: `9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc`).
- `docs/validation/AIRO_EARESMES_GATEWAY_DURABILITY_20260618.md` (Commit: `50034df009ac7bc08455ef2ee7806c03891b4669`).
- `ops/runtime/airo-runtime-runner.sh` (Commit: `19f3bd5ac93edd273989f8681a498e1b42e9c2f5`).
