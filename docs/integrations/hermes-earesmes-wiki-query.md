# Hermes & Earesmes Read-Only Wiki Query Contract

Dokumen ini mendefinisikan kontrak operasional dan tata kelola integrasi kueri baca-saja (*read-only query*) pada AIRO Second Brain (ASB) untuk agen **Earesmes** (antarmuka Telegram) dan runner **Hermes** (WSL runtime).

## 1. Peran dan Tanggung Jawab

- **Earesmes (Telegram Front Door)**: Bertindak sebagai gerbang komunikasi depan dan router kueri. Earesmes menerima permintaan kueri dari pemilik di Telegram, memvalidasinya, dan meneruskannya ke mesin kueri Hermes. Earesmes **tidak memiliki** wewenang untuk menulis berkas kanonik atau melakukan mutasi data secara mandiri.
- **Hermes (Query Executor)**: Bertindak sebagai pelaksana kueri pada lingkungan lokal WSL Ubuntu. Hermes memproses kueri pembacaan pengetahuan derivatif pada direktori `wiki/` dan dokumen penjelas di bawah `docs/`.

## 2. Hierarki Sumber dan Otoritas Kebenaran

- **Otoritas Kanonik (Source of Truth)**: Berkas-berkas di root repositori (`BOOT.md`, `CURRENT.md`, `CONTEXT.md`, `AGENTS.md`, `SECURITY.md`) serta folder penentu kebijakan (`decisions/`, `projects/`, `state/`, `identity/`, `systems/`, `agents/`, `personas/`) adalah sumber kebenaran tertinggi yang **bersifat mutlak**.
- **Pengetahuan Derivatif (Derivative Knowledge)**: Direktori `wiki/` (`wiki/concepts/`, `wiki/sources/`, `wiki/syntheses/`) adalah representasi pengetahuan sekunder yang disaring secara berkala dari sumber kanonik oleh asisten AI.
- **Aturan Pembedaan Sumber**: Earesmes/Hermes wajib secara eksplisit memberitahukan kepada pemilik di Telegram apakah jawaban yang diberikan bersumber dari **Dokumen Kanonik Asli** (Halaman Utama) atau dari **Wiki Derivatif** (lapisan sekunder).

## 3. Batasan Akses Berkas (Read/Write Boundaries)

### Jalur Baca yang Diizinkan (Allowed Read Paths)
- `wiki/` (seluruh folder konsep, sumber, dan sintesis)
- `docs/` (seluruh dokumentasi sistem dan integrasi)
- Dokumen kanonik root (hanya untuk referensi pembacaan data)

### Jalur Tulis yang Dilarang (Forbidden Write Paths)
- Dilarang keras memodifikasi atau menulis file di root: `BOOT.md`, `CURRENT.md`, `CONTEXT.md`, `AGENTS.md`, `SECURITY.md`.
- Dilarang keras melakukan penulisan berkas kanonik di: `projects/`, `decisions/`, `state/`, `identity/`, `systems/`, `agents/`, `personas/`, `registry/`, `ops/`, `scripts/` (kecuali skrip pembungkus yang disetujui).
- Mutasi berkas kanonik hanya boleh dilakukan melalui gerbang promosi otonom yang disetujui langsung oleh pemilik (*owner-approved promotion gate*).

## 4. Kebijakan Kliping Percakapan (Conversation Clip Policy)

Sesuai dengan `APPROVED_CONVERSATION_CLIP_POLICY`:
1. Kliping percakapan mentah (*raw conversation transcript*) dari ChatGPT/Claude Brave Windows disimpan di folder transisi: `C:\Users\Admin\AIRO_CLIP_INBOX\Clippings`.
2. Skrip importir otomatis wajib melewati (*skip*) kliping percakapan mentah secara default dari proses komit repositori ASB.
3. Hermes/Earesmes hanya boleh mengakses berkas kliping percakapan mentah di Windows staging untuk tugas penyulingan (*distillation task*) yang diperintahkan secara eksplisit oleh pemilik di Telegram.
4. Hasil penyulingan yang diperbolehkan masuk ke ASB: ringkasan aman (*safe summary*), catatan akhir sesi (*session closeout*), kandidat keputusan (*decision candidate*), metadata asal sumber (*source metadata*), dan tugas lanjutan (*task carry-over*). Semua file hasil penyulingan ini harus diklasifikasikan dengan status awal `status: draft` atau `status: proposal`.

## 5. Protokol Disposisi dan Contoh Perintah (Dispatch & Command Shapes)

Earesmes menerima perintah Telegram dengan format berikut:

- `/wiki query <pertanyaan>`: Melakukan kueri baca-saja pada wiki dan dokumen kanonik untuk menjawab pertanyaan pemilik.
- `/wiki status`: Menampilkan status kesehatan, jumlah indeks berkas di dalam wiki (Concepts, Sources, Syntheses), serta status validasi tautan terbaru.
- `/wiki sources <topik>`: Menampilkan daftar dokumen sumber (*source notes*) yang relevan dengan topik yang dicari.
- `/clip status`: Menampilkan status berkas kliping baru yang sedang menunggu di Windows staging inbox.
- `/clip distill <nama-berkas>`: [GATED/DEFERRED] Menjalankan perintah penyulingan terhadap berkas kliping percakapan secara terisolasi. Perintah ini dinonaktifkan di M6 dan memerlukan persetujuan pemilik serta promote gate di masa mendatang.

## 6. Aturan Penolakan Mutasi (Refusal & Guard Rules)

Jika Earesmes/Hermes menerima instruksi dari Telegram atau eksternal yang meminta mutasi file kanonik, modifikasi scheduler, penulisan otonom, atau promosi otomatis, Hermes **wajib menolak** dengan pesan terstandarisasi:

> "Maaf, permintaan modifikasi ditolak. Earesmes/Hermes saat ini beroperasi di bawah mode READ-ONLY pada repositori AIRO Second Brain. Mutasi berkas kanonik dan pembaruan struktur memerlukan persetujuan tugas eksplisit dari pemilik."

## 7. Ekspektasi Audit dan Pembacaan Balik (Audit/Readback)

Setiap kueri yang dijalankan oleh Hermes harus mencatat bukti pembacaan balik (*readback evidence*) dari file wiki yang digunakan sebagai referensi (misalnya dengan mencantumkan tag commit berkas, jalur berkas relatif, atau kutipan seksi berkas).

## 8. Daftar Periksa Adopsi M7 (M7 Adoption Checklist)

Sebelum integrasi dideploy sepenuhnya untuk operasional harian di M7, verifikasi hal-hal berikut:
- [ ] Proses Linux Obsidian WSLg berjalan lancar berdampingan dengan Earesmes.
- [ ] Skrip importir kliping web berjalan secara otomatis tanpa bentrokan kunci *writer lock*.
- [ ] Seluruh kueri baca-saja Telegram tidak mengirimkan spam ke log internal.
- [ ] Pengiriman Telegram aman dari paparan rahasia/token.
