---
type: wiki-concept
title: "AIRO Second Brain"
status: draft
canonical: false
last_reviewed: ""
tags: ["concept", "airo-second-brain", "architecture"]
sources:
  - path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
    commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
    section: "1. Purpose"
  - path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
    commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
    section: "5. Required Logical Repository Structure"
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
---

# AIRO Second Brain

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
AIRO Second Brain (ASB) adalah repositori pengetahuan bersama (shared-memory) terpusat yang dirancang untuk menjaga kontinuitas informasi dan memori operasional di seluruh ekosistem AIRO. ASB bertindak sebagai jembatan durabel antara pemilik sistem (manusia) dengan berbagai konsumen kecerdasan buatan (seperti ChatGPT, Claude, dan Antigravity).

## Current understanding
- **Peran Repositori Utama (Canonical Repository Role)**: ASB menyimpan semua catatan tata kelola, dokumentasi proyek, riwayat keputusan pemilik, dan proposal distilasi dalam satu repositori Git tunggal yang diakses langsung melalui antarmuka Obsidian (Status: implemented).
- **Tujuan Kontinuitas (Knowledge Continuity)**: Menjamin agar AI yang berbeda dapat berbagi konteks yang konsisten tanpa kehilangan memori antar sesi obrolan (Status: implemented).
- **Hubungan dengan Agen (Relationship to Agents)**:
  - Earesmes menggunakannya untuk hidrasi konteks di awal sesi dan merekam closeout sesi (Status: specified).
  - Antigravity membaca berkas-berkas ASB untuk memvalidasi batasan keamanan sebelum melakukan modifikasi kode (Status: implemented).
- **Batasan Terimplementasi vs Ditunda (Implemented vs Deferred Boundaries)**:
  - Struktur repositori, manajemen pekerjaan (jobs), kontrol keamanan dasar, dan visualisasi Obsidian telah diimplementasikan (Status: implemented).
  - Otomatisasi ujung-ke-ujung (end-to-end loop) dan integrasi promosi pengetahuan penuh masih berada dalam fase spesifikasi dan ditunda untuk pengembangan masa depan (Status: deferred).

## Relationships
- `extends` [Canonical Knowledge](canonical-knowledge.md) — ASB menerapkan model pengetahuan kanonik untuk menjaga kebenaran.
- `uses` [Runtime Sync](runtime-sync.md) — Bergantung pada sinkronisasi otomatis untuk mendistribusikan perubahan.

## Evidence
Desain logical struktur repositori didefinisikan secara eksplisit di Seksi 5 PRD v0.5.1, yang melarang keras pembuatan vault duplikat atau modifikasi struktur di luar namespace `wiki/`.

## Contradictions or uncertainty
Ketergantungan pada editor manusia (owner) untuk promosi pengetahuan semantik berarti bahwa sebagian konten di ASB akan tetap berada dalam status draft untuk waktu lama jika pemilik tidak melakukan review secara rutin.

## Canonical implications
Setiap data yang dimasukkan ke ASB harus melalui distilasi ketat agar tidak mengotori repositori dengan transkrip mentah yang berukuran besar.

## Provenance
- `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md` (Commit: `9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc`, Seksi: "1. Purpose", "2.5 Obsidian", "5. Required Logical Repository Structure").
