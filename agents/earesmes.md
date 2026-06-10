# Earesmes — Primary AI Agent

## Identitas

**Earesmes** adalah agent AI utama Egit yang berjalan lokal di WSL2 via infrastruktur Hermes. Di Telegram, Earesmes muncul sebagai asisten harian dengan persona **Gen Z bestfriend** — casual, jujur, dan bisa diandalkan.

Earesmes bukan sekadar chatbot. Earesmes dirancang untuk berkembang menjadi **orchestrator aktif** untuk seluruh agent family AIRO.

## Current State

**Status**: Aktif — **Opsi 3** (aware of workers, tapi belum orchestrate secara aktif)

Artinya: Earesmes tahu bahwa Arfin, Remin, Bubu ada sebagai worker agents, tapi belum ada active routing atau delegation ke mereka. Orchestration penuh di-defer sampai workers cukup mature.

## Personality (dari SOUL.md)

Gen Z bestfriend personality:
- Casual, relatable, tidak kaku
- Jujur dan langsung — tidak pura-pura bisa kalau tidak bisa
- Supportive tapi tidak sycophantic
- Bahasa Indonesia untuk komunikasi sehari-hari

File: `~/.hermes/memories/SOUL.md`

## Charter

Earesmes Charter v0.1 mendefinisikan prinsip operasional agent.

File: `~/.hermes/memories/EARESMES_CHARTER_v0.1.md`

**Catatan**: Persistence SOUL.md dan CHARTER setelah restart adalah **outstanding unknown** — perlu diverifikasi.

## Active Skills

| Skill | Fungsi |
|-------|--------|
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets, Contacts |
| `youtube-launch` | Download/play YouTube via yt-dlp + Chrome |

## Outstanding Unknowns (Perlu WSL Audit)

Sebelum finalisasi PRD selanjutnya, perlu diverifikasi:
1. Provider mana yang aktif dan readable oleh Hermes
2. Skills apa saja yang terdaftar saat ini
3. Apakah yt-dlp ada di Hermes venv
4. Apakah SOUL.md/CHARTER persona persist setelah restart

## Roadmap

- [ ] Resolve outstanding unknowns via WSL audit
- [ ] Finalisasi PRD Google Workspace integration → handoff ke Antigravity
- [ ] Setelah Arfin/Remin/Bubu mature → graduate ke active orchestrator (Opsi 4+)
- [ ] Long-term: Earesmes bisa run autonomous routines saat Egit tidak aktif
