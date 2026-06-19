---
type: wiki-source
title: "AIRO Second Brain PRD v0.5.1"
status: draft
canonical: false
source_kind: "canonical-prd"
source_path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
source_commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
captured_at: "2026-06-17T23:15:00+07:00"
sensitivity: public
tags: ["prd", "airo-second-brain", "governance"]
---

# AIRO Second Brain PRD v0.5.1

> [!WARNING]
> Do not paste secrets, tokens, full private conversations, credentials, or restricted raw source content into this note.

## Source identity
Dokumen ini merupakan spesifikasi produk resmi (PRD) versi 0.5.1 untuk proyek AIRO Second Brain. Dokumen ini disetujui oleh pemilik sistem (Egit Aristo Randas) sebagai acuan teknis operasional.

## Safe summary
PRD ini mendefinisikan struktur repositori, aturan orkestrasi sistem, aliran data, dan integrasi dengan Obsidian. Tujuan utamanya adalah meningkatkan repositori pengetahuan bersama (Second Brain) menjadi sistem memori aktif yang menghubungkan pengguna dengan asisten AI (Earesmes/Hermes) dan pelaksana teknis (Antigravity).

## Key evidence
Beberapa poin bukti kunci dari dokumen ini meliputi:
- **Tujuan AIRO Second Brain**: Menyediakan platform memori bersama antar AI consumers (ChatGPT, Claude, Antigravity) tanpa membuat replika repositori pengetahuan baru (Status: implemented).
- **Hierarki Kebenaran (Truth Hierarchy)**: Menetapkan prioritas pembacaan di mana bukti runtime langsung menempati prioritas tertinggi di atas kesimpulan model AI (Status: implemented).
- **Peran Earesmes**: Agen asisten lokal di Telegram yang bertindak sebagai resident orchestrator / Chief of Staff / resident AIRO Sync (Status: implemented).
- **Arsitektur Sinkronisasi (Runtime Sync)**: Target sinkronisasi berkala setiap 10 menit saat WSL aktif dan proses nightly pada pukul 22.00 (Status: specified).
- **Obsidian Phase (Fase 8)**: Membuka repositori existing secara langsung sebagai vault tanpa copy/mirror (Status: validated).
- **LLM Wiki Phase (Fase 9)**: Mengolah sumber mentah di staging menjadi proposal, konsep, dan wiki terstruktur (Status: implemented).
- **North-Star Orchestration (Fase 10)**: Aliran orkestrasi ujung-ke-ujung (end-to-end loop) otomatis dari input Telegram ke aksi Antigravity dan kembali ke Obsidian (Status: specified).

## Related concepts
- [[concepts/airo-second-brain]] — Menjelaskan peran repositori ini.
- [[concepts/canonical-knowledge]] — Dasar tata kelola kebenaran (truth hierarchy).
- [[concepts/earesmes]] — Peran dan batas asisten lokal Earesmes.
- [[concepts/runtime-sync]] — Sinkronisasi otomatis dan penanganan repositori kotor.

## Contradictions or uncertainty
Fase 10 (North-star orchestration) masih berupa spesifikasi masa depan dan belum diimplementasikan sepenuhnya. Keterbatasan API gratis membatasi kapabilitas penalaran langsung Earesmes pada mesin lokal.

## Provenance
Distilasi dari `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md` pada commit `9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc`.
