---
type: wiki-concept
title: "Canonical Knowledge"
status: draft
canonical: false
last_reviewed: ""
tags: ["concept", "governance", "truth"]
sources:
  - path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
    commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
    section: "3. Truth Hierarchy"
  - path: "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md"
    commit: "9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc"
    section: "2.6 Promotion"
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
---

# Canonical Knowledge

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
Canonical Knowledge adalah informasi resmi, sahih, dan bersertifikat pemilik di dalam ekosistem AIRO. Konsep ini memisahkan antara data mentah yang tidak tepercaya (derivative/raw) dengan kebenaran sistem yang telah divalidasi.

## Current understanding
- **Distingsi Kanonik vs Derivatif (Canonical vs Derivative Distinction)**: Berkas kanonik (seperti PRD, keputusan tertulis pemilik, dan arsitektur stabil) bersifat otoritatif. Sebaliknya, proposal distilasi, catatan hasil penalaran AI, dan isi folder wiki di bawah namespace `wiki/` bersifat derivatif dan tidak boleh mengubah berkas kanonik tanpa persetujuan eksplisit (Status: implemented).
- **Hierarki Kebenaran (Truth Hierarchy)**: Jika terjadi pertentangan informasi, bukti runtime langsung dan bukti Git menempati prioritas tertinggi, disusul berkas kanonik ASB, sementara ingatan obrolan model AI menempati posisi terendah (Status: implemented).
- **Persyaratan Provenance (Provenance Requirements)**: Setiap klaim faktual harus merujuk pada bukti sumber nyata yang mencantumkan path dokumen, commit, dan seksi spesifik (Status: implemented).
- **Penanganan Konflik (Conflict Behavior)**: Jika terjadi konflik informasi semantik atau divergensi kode, sistem otomatisasi harus dihentikan (`GIT_CONFLICT_PAUSED`) dan dialihkan ke resolusi manual (Status: implemented).
- **Promosi ke Status Kanonik (Promotion into Canonical State)**: Fakta mesin dan operasional dipromosikan otomatis dengan bukti, sedangkan pengetahuan semantik memerlukan persetujuan pemilik lewat rekaman persetujuan formal (Status: implemented).

## Relationships
- `related_to` [AIRO Second Brain](airo-second-brain.md) — Mengatur standar kebenaran isi Second Brain.
- `related_to` [Earesmes](earesmes.md) — Earesmes dilarang melakukan promosi pengetahuan semantik secara mandiri.

## Evidence
Aturan Hierarki Kebenaran didefinisikan pada Seksi 3 PRD v0.5.1, yang mengikat semua AI consumers untuk mendahulukan bukti runtime dibanding memori model.

## Contradictions or uncertainty
Konflik antara dokumentasi yang tertulis lama dengan kenyataan runtime sering kali terjadi. Di bawah aturan ini, ketidaksesuaian diselesaikan dengan memprioritaskan bukti runtime sebagai fakta yang benar.

## Canonical implications
Perubahan pada berkas-berkas kanonik (seperti `AGENTS.md` atau `SECURITY.md`) harus melalui persetujuan pemilik dan tidak boleh dilakukan secara otomatis oleh skrip.

## Provenance
- `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md` (Commit: `9cca18b0bcbdbaf6d69e54a5cc44169534e1edcc`, Seksi: "3. Truth Hierarchy", "12. Owner Approval Protocol", "22. Hybrid Promotion").
