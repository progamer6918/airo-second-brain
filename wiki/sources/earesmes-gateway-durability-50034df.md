---
type: wiki-source
title: "Earesmes Gateway Durability Evidence"
status: draft
canonical: false
source_kind: "git-validation-commit"
source_path: "git-commit:50034df009ac7bc08455ef2ee7806c03891b4669"
source_commit: "50034df009ac7bc08455ef2ee7806c03891b4669"
captured_at: "2026-06-18T21:52:54+07:00"
sensitivity: public
tags: ["durability", "gateway", "telegram", "validation"]
---

# Earesmes Gateway Durability Evidence

> [!WARNING]
> Do not paste secrets, tokens, full private conversations, credentials, or restricted raw source content into this note.

## Source identity
Dokumen ini merupakan laporan bukti validasi ketahanan gateway Earesmes yang terekam pada commit `50034df` di file `docs/validation/AIRO_EARESMES_GATEWAY_DURABILITY_20260618.md` serta perubahan di `projects/earesmes-hermes.md`.

## Safe summary
Laporan validasi ini membuktikan ketahanan runtime Telegram gateway yang digunakan oleh Earesmes. Gateway ini bertindak sebagai jembatan komunikasi alami dengan pemilik sistem lewat Telegram. Uji coba menunjukkan bahwa gateway mampu pulih secara otomatis dari kegagalan proses tanpa mengganggu Hermes worker.

## Key evidence
Bukti-bukti kunci dari pengujian ini mencakup:
- **Telegram Gateway**: Menggunakan skrip `telegram-gateway.py` sebagai penangan tunggal (`getUpdates`) untuk menerima pesan dari Telegram (Status: validated).
- **Hermes Worker**: Berjalan secara terisolasi sebagai service Linux systemd `airo-hermes-worker.service` tanpa dipengaruhi oleh hidup/matinya gateway (Status: validated).
- **Single Poller**: Terbukti tidak ada poller ganda (second poller) yang berjalan secara bersamaan (Status: validated).
- **Runtime Durability**: Menggunakan Windows Scheduled Task `AIRO Earesmes Telegram Listener` dengan pemicu logon dan pengulangan setiap 5 menit (PT5M) serta opsi `MultipleInstances=IgnoreNew` (Status: validated).
- **Controlled Failure Test**: Saat gateway ber-PID 18992 menerima sinyal SIGTERM, ia berhenti dengan bersih. Scheduler Windows mendeteksi berhentinya proses ini dan memicu kembali gateway baru dengan PID 20505 pada jadwal berikutnya, sementara Hermes worker (PID 18482) tetap aktif tanpa gangguan (Status: validated).
- **Startup/Context Hydration**: Proses hidrasi konteks dasar untuk ASB terbukti aktif dan berjalan pada commit `8959193` (Status: validated).

## Related concepts
- [[concepts/earesmes]] — Peran Earesmes sebagai agen depan Telegram.
- [[concepts/telegram-gateway]] — Detail teknis gateway ketahanan tinggi.
- [[concepts/runtime-sync]] — Sinkronisasi runtime yang berjalan di belakang layar.

## Contradictions or uncertainty
Meskipun ketahanan gateway terbukti pulih dengan baik, pengujian mencatat adanya masalah latensi respons Earesmes yang mencapai sekitar 21 detik. Penyebab latensi ini belum dilacak secara menyeluruh (Status: degraded).

## Provenance
Berdasarkan log validasi commit `50034df009ac7bc08455ef2ee7806c03891b4669` pada berkas `docs/validation/AIRO_EARESMES_GATEWAY_DURABILITY_20260618.md`.
