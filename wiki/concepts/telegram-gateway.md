---
type: wiki-concept
title: "Telegram Gateway"
status: draft
canonical: false
last_reviewed: ""
tags: ["concept", "gateway", "telegram", "infra"]
sources:
  - path: "wiki/sources/earesmes-gateway-durability-50034df.md"
    commit: "50034df009ac7bc08455ef2ee7806c03891b4669"
    section: "Key evidence"
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
---

# Telegram Gateway

This note is derivative. Canonical AIRO sources remain authoritative.

## Definition
Telegram Gateway adalah infrastruktur penghubung komunikasi antara aplikasi Telegram pihak ketiga dengan agen kecerdasan buatan Hermes/Earesmes di mesin lokal. Gateway bertugas menerima pesan masuk secara persisten dan menyampaikannya ke antrean pekerja.

## Current understanding
- **Peran Gateway (Gateway Role)**: Bertindak sebagai front-door untuk menerima instruksi teks biasa dari pemilik sistem secara real-time (Status: implemented).
- **Perilaku Poller Tunggal (Single-Poller Behavior)**: Proses `telegram-gateway.py` dikonfigurasi sebagai satu-satunya pemilik polling (`getUpdates`). Hal ini penting untuk mencegah perebutan token Telegram oleh poller ganda (Status: validated).
- **Batasan Antrean/Pekerja (Queue/Worker Boundary)**: Gateway menulis pesan masuk ke antrean lokal, sementara Hermes worker memprosesnya secara asinkron. Kegagalan pada gateway tidak akan menghentikan worker yang sedang berjalan (Status: validated).
- **Bukti Ketahanan (Durability Evidence)**: Gateway diawasi oleh Windows Scheduled Task `AIRO Earesmes Telegram Listener` dengan pemicu logon dan penjadwalan berulang setiap 5 menit (PT5M). Opsi `MultipleInstances=IgnoreNew` and batas waktu tidak terbatas menjamin gateway segera dihidupkan ulang jika mati (Status: validated).
- **Perlindungan Duplikasi (Failure and Duplicate Protection)**: Mekanisme penanganan kegagalan terkendali membuktikan bahwa gateway yang dimatikan paksa dengan SIGTERM dapat pulih secara otomatis dalam 2 menit tanpa adanya pesan duplikat (Status: validated).

## Relationships
- `uses` [Earesmes](earesmes.md) — Meneruskan pesan masuk ke instansi agen Earesmes.
- `related_to` [Runtime Sync](runtime-sync.md) — Berjalan sebagai salah satu komponen latar belakang (background infra) di bawah pengawasan task scheduler.

## Evidence
Berdasarkan bukti pengujian kegagalan terkendali pada commit `50034df`, matinya PID gateway `18992` segera digantikan oleh PID `20505` tanpa menghentikan worker (PID `18482`).

## Contradictions or uncertainty
Gateway ini tidak menjamin latensi respons yang sangat rendah. Latensi pengiriman pesan saat ini tercatat sekitar 21 detik, yang masih memerlukan tracing end-to-end (Status: degraded).

## Canonical implications
Token API Telegram tidak boleh disimpan di repositori ini dan harus selalu dilindungi di luar workspace Git sesuai dengan kebijakan keamanan.

## Provenance
- `wiki/sources/earesmes-gateway-durability-50034df.md` (Commit: `50034df009ac7bc08455ef2ee7806c03891b4669`, Seksi: "Key evidence", "Remaining Open Item").
