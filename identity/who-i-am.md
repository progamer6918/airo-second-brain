# Who I Am — Egit

## Identitas Dasar

- **Nama**: Egit (Egit Aristorandas)
- **Lokasi**: Jambi, Indonesia
- **Bahasa**: Bahasa Indonesia (komunikasi sehari-hari dan owner-facing docs), English (technical specs dan PRD)

## Background

Egit adalah pemilik tunggal ekosistem AIRO. Tidak memiliki background coding — seluruh eksekusi teknis dilakukan oleh AI berdasarkan instruksi yang Egit rancang. Egit berperan sebagai **arsitek sistem dan decision maker**, bukan implementor teknis.

Pendekatan ini bukan keterbatasan — ini adalah model kerja yang disengaja. Egit mengandalkan kemampuan AI untuk menjembatani gap teknis, sementara Egit fokus pada desain, keputusan, dan arah sistem.

## Cara Kerja

- **Dokumentasi-first**: Setiap keputusan arsitektur dan sistem didokumentasikan sebelum dieksekusi. PRD adalah kontrak, bukan panduan informal.
- **Brainstorm sebelum execute**: Egit memisahkan fase brainstorming/requirements dari fase eksekusi. AI tidak boleh langsung eksekusi sebelum fase desain selesai dan disetujui.
- **Structured handoffs**: Context dipindahkan antar sesi dan antar AI melalui dokumen handoff — bukan diharapkan AI ingat sendiri.
- **Cross-reference**: Egit secara aktif membandingkan output dari Claude dan ChatGPT, menggunakan gap analysis dari satu untuk memvalidasi yang lain.
- **Bahasa dokumen**: Non-technical/owner-facing → Bahasa Indonesia. Technical specs/PRD → English.

## Tools Utama

- **Claude** (brainstorming, arsitektur, gap analysis, draft PRD)
- **ChatGPT** (eksekusi, implementasi, second opinion)
- **Antigravity** (AI executor khusus untuk PRD — one-pass execution tanpa back-and-forth)
- **Telegram** (primary daily interface ke semua agent)
- **WSL2 Ubuntu / Hermes** (local AI agent runtime)

## Ekosistem yang Dibangun

Egit sedang membangun **AIRO** — personal AI operating system yang mencakup:
- Local AI agent (Earesmes/Hermes) sebagai asisten utama
- Finance automation (AIRO Finance / Arfin)
- Reminder system (Remin) — planned
- Note-keeping (Bubu) — planned
- Dan project-project lain yang berkembang seiring waktu
