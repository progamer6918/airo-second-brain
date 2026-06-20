---
type: wiki-concept
title: "Obsidian"
status: draft
canonical: false
last_reviewed: ""
tags:
  - obsidian
  - knowledge-interface
sources:
  - path: ".obsidian/app.json"
    commit: "9f32d6b3b530fe5d3ba8d958ac5149444f9473ee"
    section: "Tracked vault configuration"
  - path: "docs/integrations/obsidian-wiki.md"
    commit: "b58159559edfd1ebbfad6d29577f31b288ed70d4"
    section: "Vault and selected-skill integration"
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
---

# Obsidian

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
Obsidian adalah antarmuka visual utama bagi pemilik sistem (manusia) untuk membaca, mengedit catatan Markdown, dan memvisualisasikan grafik keterkaitan antar konsep dalam ekosistem AIRO Second Brain (Status: implemented).

## Current understanding
- **Visual Cockpit untuk Manusia**: Obsidian bertindak sebagai kokpit navigasi dan antarmuka peninjauan (review interface) bagi pemilik untuk mengelola tugas dan pengetahuan (Status: implemented).
- **Repositori yang Sama sebagai Vault**: Obsidian membuka direktori repositori Git lokal (ASB_REPO) secara langsung sebagai vault tunggal. Tidak ada repositori kedua atau cermin (mirror) yang dibuat untuk menghindari redundansi data (Status: implemented).
- **Aplikasi Linux Melalui WSLg**: Obsidian dijalankan sebagai aplikasi Linux asli (native) di dalam lingkungan Ubuntu WSL menggunakan WSLg (Windows Subsystem for Linux GUI) untuk mengakses sistem berkas Linux secara native (Status: implemented). Arsitektur Windows UNC sebelumnya yang mencoba membuka vault lewat jalur UNC jaringan Windows (wsl.localhost) ditinggalkan karena masalah kompatibilitas pengawasan file (Status: deferred).
- **Bukan Otoritas Kebenaran**: Obsidian tidak memiliki otoritas kanonik untuk memvalidasi atau mempromosikan keputusan secara otomatis. Berkas kanonik asli di dalam repositori tetap menjadi sumber kebenaran tertinggi (Truth Hierarchy) (Status: implemented).
- **Fitur Awan Dinonaktifkan**: Layanan Obsidian Sync dan Obsidian Publish dinonaktifkan sepenuhnya untuk menjamin bahwa seluruh data tetap bersifat lokal, privat, dan sinkronisasi hanya dilakukan melalui skrip kontrol Git internal (Status: implemented).

## Relationships
- `related_to` [AIRO Second Brain](airo-second-brain.md) — Obsidian bertindak sebagai antarmuka tampilan untuk isi Second Brain.
- `related_to` [Canonical Knowledge](canonical-knowledge.md) — Mengikuti tata kelola kebenaran di mana berkas kanonik tidak boleh dimutasi tanpa izin pemilik.

## Evidence
Penginstalan dan peluncuran Obsidian Linux asli melalui WSLg dikonfirmasi pada Milestone M1B dengan versi paket 1.12.7 amd64 yang berjalan di bawah pengguna normal, bukan root.

## Contradictions or uncertainty
Kondisi tampilan WSLg bergantung pada kesiapan grafis host Windows. Apabila terjadi kegagalan GPU Viz pada WSLg, proses Obsidian Linux dapat terhenti secara tidak terduga, namun tidak memengaruhi keandalan sinkronisasi data Git di latar belakang.

## Canonical implications
Penyuntingan catatan secara manual di Obsidian oleh pengguna harus mematuhi format penautan Markdown relatif agar tidak memicu kesalahan tautan rusak pada proses otomatisasi wiki-lint.

## Provenance
- `.obsidian/app.json` (Commit: `9f32d6b3b530fe5d3ba8d958ac5149444f9473ee`, Seksi: "Tracked vault configuration").
- `docs/integrations/obsidian-wiki.md` (Commit: `b58159559edfd1ebbfad6d29577f31b288ed70d4`, Seksi: "Vault and selected-skill integration").
