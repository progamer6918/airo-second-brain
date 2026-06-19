---
type: wiki-concept
title: "Earesmes"
status: draft
canonical: false
last_reviewed: ""
tags: ["concept", "agent", "earesmes", "hermes"]
sources:
  - path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
    commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
    section: "4.4 Earesmes / Hermes"
  - path: "wiki/sources/earesmes-gateway-durability-50034df.md"
    commit: "50034df009ac7bc08455ef2ee7806c03891b4669"
    section: "Key evidence"
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
---

# Earesmes

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
Earesmes adalah persona asisten AI utama dan Resident Orchestrator lokal dalam ekosistem AIRO. Ia bertindak sebagai "Chief of Staff" bagi pemilik sistem dan berjalan di atas infrastruktur runtime lokal bernama Hermes.

## Current understanding
- **Peran Gateway Telegram (Role as Telegram/Front-Door Agent)**: Earesmes melayani interaksi sehari-hari dengan pemilik sistem melalui Telegram natural-language bridge (Status: implemented).
- **Hubungan dengan Hermes Worker (Relationship to Hermes Worker)**: Earesmes berjalan sebagai agen logika di atas Hermes worker (`airo-hermes-worker.service`) yang terisolasi dari proses Telegram gateway (Status: implemented).
- **Hubungan dengan Konteks ASB (Relationship to ASB Context)**: Earesmes menggunakan catatan di ASB untuk melakukan hidrasi konteks saat memulai sesi operasional (Status: specified).
- **Otoritas Pembacaan dan Rute (Read/Query/Routing Authority)**: Earesmes memiliki wewenang untuk membaca status sistem, menghitung jumlah pekerjaan tertunda, dan mengarahkan pekerjaan sederhana ke model gratis (Status: implemented).
- **Batasan Mutasi (Mutation Limitations)**: Earesmes dilarang keras memodifikasi berkas kanonik atau melakukan promosi pengetahuan semantik tanpa persetujuan eksplisit pemilik (Status: implemented). Integrasi otomatisasi penuh (seperti sinkronisasi penuh di Fase 6/10) belum diimplementasikan (Status: deferred).

## Relationships
- `uses` [[concepts/telegram-gateway]] — Bergantung pada gateway untuk menerima pesan.
- `uses` [[concepts/runtime-sync]] — Memonitor liveness sinkronisasi untuk pelaporan kesehatan.

## Evidence
Pemisahan peran antara Earesmes (persona) dan Hermes (runtime lokal) divalidasi pada pengujian ketahanan gateway di commit `50034df`, di mana kegagalan gateway tidak mematikan worker Hermes.

## Contradictions or uncertainty
Kapasitas penalaran lokal Earesmes dibatasi oleh model gratis yang terpasang di WSL. Pekerjaan penalaran yang rumit harus dieskalasi ke ChatGPT atau Claude melalui mekanisme pending jobs (Status: degraded).

## Canonical implications
Pesan Telegram yang dikirim oleh pemilik tidak boleh disimpan mentah-mentah ke dalam repositori pengetahuan guna melindungi keamanan data pribadi (pii).

## Provenance
- `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md` (Commit: `9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc`, Seksi: "4.4 Earesmes / Hermes", "9. Deterministic Work Classification").
- `wiki/sources/earesmes-gateway-durability-50034df.md` (Commit: `50034df009ac7bc08455ef2ee7806c03891b4669`, Seksi: "Key evidence").
