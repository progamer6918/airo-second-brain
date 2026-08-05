---
type: wiki-concept
title: "Execution Assurance"
status: draft
canonical: false
last_reviewed: "2026-08-05"
tags: ["concept", "governance", "execution-assurance", "fail-closed"]
sources:
  - path: "worklog/sessions/2026-08-04/ASB/02 - M2 Session & Worklog Implementation.md"
    commit: "65ebc858ce042912616dd427c0fdd0ff66a8f053"
    section: "## 🛠 Yang dilakukan"
provenance:
  extracted: 1.0
  inferred: 0.0
  ambiguous: 0.0
---

# Execution Assurance

This note is derivative. Canonical ASB sources remain authoritative.

## Definition
Execution Assurance adalah mekanisme penjaminan eksekusi di ekosistem AIRO yang mengevaluasi secara deterministik apakah suatu tugas benar-benar selesai (`BERHASIL`) berdasarkan kesesuaian bukti wajib (*required evidence*) dan bukti aktual (*actual evidence*).

## Key Rules & Learnings
- **Script Success Is Not Task Success**: Keberhasilan skrip atau perintah shell (`EXIT_CODE=0` / `SCRIPT_SUCCESS`) tidak sama dengan selesainya tugas (`BERHASIL` / `CAN_ADVANCE=YES`).
- **Fail-Closed Evidence Evaluation**: Jika bukti wajib yang dipersyaratkan tidak terpenuhi atau tidak dilampirkan, validator tugas harus gagal-tutup (*fail closed*) dengan hasil `BELUM_TERBUKTI` dan `CAN_ADVANCE=NO`.
- **Preservasi Status Sesi Aktif**: Kegagalan validator atau generator harian tidak boleh menghapus atau merusak status sesi yang sedang aktif.

## Relationships
- `related_to` [Canonical Knowledge](canonical-knowledge.md) — Menjamin bahwa klaim keberhasilan tugas didasarkan pada bukti sahih.
- `related_to` [AIRO Second Brain](airo-second-brain.md) — Mengatur standar validasi tugas pada seluruh milestone ASB.

## Evidence
- `worklog/sessions/2026-08-04/ASB/02 - M2 Session & Worklog Implementation.md` (Commit: `65ebc858ce042912616dd427c0fdd0ff66a8f053`, Seksi: "## 🛠 Yang dilakukan").

## Provenance
- `worklog/sessions/2026-08-04/ASB/02 - M2 Session & Worklog Implementation.md` (Commit: `65ebc858ce042912616dd427c0fdd0ff66a8f053`, Seksi: "## 🛠 Yang dilakukan").
