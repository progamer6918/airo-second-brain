---
type: wiki-concept
title: "LLM Wiki"
status: draft
canonical: false
last_reviewed: ""
tags:
  - llm-wiki
  - knowledge-synthesis
sources:
  - path: "docs/integrations/obsidian-wiki.md"
    commit: "b58159559edfd1ebbfad6d29577f31b288ed70d4"
    section: "Pinned selected skills"
  - path: "docs/integrations/obsidian-wiki-knowledge-contract.md"
    commit: "a2747bb3b8f7f4fde421c5265e2c6b9f881c8c34"
    section: "Derivative authority and provenance contract"
  - path: "wiki/dashboards/status.md"
    commit: "ceab25431189ff9aecf5b2b7bc27430330b390cb"
    section: "Initial governed ingestion status"
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
---

# LLM Wiki

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
LLM Wiki adalah lapisan pengetahuan derivatif (derivative knowledge layer) dalam ekosistem AIRO yang diatur untuk melakukan distilasi dan integrasi informasi dari berbagai sumber menjadi struktur pengetahuan yang terhubung dan dapat ditelusuri (Status: implemented).

## Current understanding
- **Status Penerimaan Governed Ingest**: Lapisan LLM Wiki telah berhasil mengimplementasikan proses pencatatan sumber (ingestion) awal yang terkelola dengan menerjemahkan tiga paket bukti nyata (S1, S2, S3) menjadi catatan sumber (source notes) dan catatan konsep (concept notes) (Status: implemented).
- **Kewajiban Provenance**: Setiap klaim pengetahuan faktual yang tercantum di dalam wiki wajib merujuk secara eksplisit ke berkas asli, nomor commit Git, dan seksi dokumen sumber untuk menjamin ketertelusuran (Status: implemented).
- **Otoritas Kebenaran**: LLM Wiki bersifat sekunder dan derivatif. Berkas kanonik utama (seperti PRD di `docs/prd/`, keputusan pemilik di `decisions/`, dan `AGENTS.md`) tetap memegang kebenaran mutlak (Truth Hierarchy) (Status: implemented).
- **Penyematan Skill Terpilih**: Sistem meminjam repositori upstream `Ar9av/obsidian-wiki` (tag `v2026.06.6`) dan menyematkan skill-skill tertentu untuk orkestrasi pengetahuan (seperti `wiki-query`, `wiki-synthesize`, `cross-linker`, `wiki-lint`, `wiki-dashboard`, dan `wiki-status`) (Status: implemented).
- **Pencegahan Mutasi Berlebih**: LLM Wiki dilarang melakukan Git sync mandiri secara bebas, dilarang melakukan promosi kanonik otomatis tanpa persetujuan pemilik, dan mutasi asisten Hermes penuh ditangguhkan hingga Milestone M6 (Status: deferred).

## Relationships
- `uses` [Canonical Knowledge](canonical-knowledge.md) — Bergantung pada tata kelola kebenaran kanonik untuk validasi klaim.
- `uses` [Obsidian](obsidian.md) — Memanfaatkan Obsidian sebagai antarmuka tampilan grafis dan navigasi.

## Evidence
Kontrak tata kelola LLM Wiki diatur secara formal di dalam `docs/integrations/obsidian-wiki-knowledge-contract.md` pada commit M3 (`a2747bb`), sementara status ingesti awal Milestone M4 terekam pada commit `ceab254`.

## Contradictions or uncertainty
Hambatan saat ini adalah ketergantungan penuh proses pembaruan data pada eksekusi manual Antigravity, karena orkestrasi mutasi asisten otonom Hermes masih ditunda.

## Canonical implications
Penerapan aturan wiki-lint secara berkala diperlukan untuk menjamin tidak ada inkonsistensi metadata di bawah folder `wiki/` sebelum data tersebut dikonsumsi oleh agen eksternal.

## Provenance
- `docs/integrations/obsidian-wiki.md` (Commit: `b58159559edfd1ebbfad6d29577f31b288ed70d4`, Seksi: "Pinned selected skills").
- `docs/integrations/obsidian-wiki-knowledge-contract.md` (Commit: `a2747bb3b8f7f4fde421c5265e2c6b9f881c8c34`, Seksi: "Derivative authority and provenance contract").
- `wiki/dashboards/status.md` (Commit: `ceab25431189ff9aecf5b2b7bc27430330b390cb`, Seksi: "Initial governed ingestion status").
