# How to Use This Brain — Instruksi untuk AI

Dokumen ini untuk AI yang baru pertama kali mengakses repo `airo-second-brain`.

---

## Kamu Adalah Siapa?

Repo ini dikonsumsi oleh beberapa AI dengan cara berbeda:

| Consumer | Cara Akses | Yang Perlu Dibaca |
|----------|-----------|-------------------|
| **Hermes/Earesmes** | Clone lokal di `~/.hermes/brain/`, baca file via skill | `CONTEXT.md` dulu, lalu file relevan |
| **Claude** | Paste `CONTEXT.md` di awal conversation baru | `CONTEXT.md` + file sesuai topik sesi |
| **ChatGPT** | Upload file per sesi | File yang paling relevan dengan task |
| **Antigravity** | Paste sebagai opening context PRD | `CONTEXT.md` + `identity/working-principles.md` + file project yang akan dieksekusi |

---

## Prinsip Utama saat Bekerja dengan Egit

1. **Semua instruksi teknis harus copy-paste ready** — Egit tidak punya background coding
2. **Flag gaps sebelum mulai** — jangan assume dan lanjut kalau ada yang tidak jelas
3. **Brainstorm dulu, execute belakangan** — ini adalah dua fase terpisah
4. **Dokumen adalah source of truth** — kalau ada konflik antara memory AI dan dokumen, dokumen menang
5. **Bahasa Indonesia** untuk output owner-facing; **English** untuk technical specs

Baca [`identity/working-principles.md`](../identity/working-principles.md) untuk detail lengkap.

---

## Cara Membaca Repo Ini

### Kalau kamu baru pertama kali:
1. Baca `CONTEXT.md` (sudah kamu baca ini)
2. Baca `identity/who-i-am.md` untuk understand siapa Egit
3. Baca `identity/working-principles.md` untuk understand cara kerja yang diharapkan
4. Baca file relevan sesuai task yang sedang dikerjakan

### Kalau kamu diminta bekerja pada project tertentu:
1. Baca `projects/_index.md` untuk overview
2. Baca file project spesifik (misal `projects/airo-finance.md`)
3. Baca agent yang terlibat kalau relevan

### Kalau kamu adalah Antigravity dan mau eksekusi PRD:
1. Baca `CONTEXT.md`
2. Baca `identity/working-principles.md` — terutama bagian "Untuk Antigravity"
3. Baca file project yang relevan
4. Baru baca PRD yang akan dieksekusi

---

## Yang Tidak Ada di Repo Ini

- Detail sensitif atau private yang tidak perlu diketahui AI
- AIRO Finance detail teknis yang sangat spesifik ada di `projects/airo-finance.md` sebatas context — PRD asli ada di repo terpisah

---

## Maintenance

Repo ini diupdate secara manual oleh Egit atau atas permintaan Egit kepada AI. Kalau ada informasi yang terasa outdated, flag ke Egit — jangan assume dan lanjut dengan info yang mungkin stale.

Lihat [`changelog.md`](changelog.md) untuk history perubahan.
