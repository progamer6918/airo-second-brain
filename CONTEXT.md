# AIRO — Owner Context Router

> **Baca file ini dulu sebelum apapun.** Ini adalah router utama ekosistem AIRO.
> Semua pointer ke knowledge spesifik ada di sini.

---

## Siapa yang Membangun Ini

Egit adalah pemilik tunggal ekosistem **AIRO** — sebuah personal AI operating system yang sedang dibangun secara bertahap. Egit tidak memiliki background coding dan sepenuhnya mengandalkan AI untuk eksekusi teknis. Semua instruksi yang diberikan kepada AI harus **copy-paste ready** — tidak boleh ada ambiguitas atau interpretasi yang diperlukan.

→ Detail lengkap: [`identity/who-i-am.md`](identity/who-i-am.md)
→ Cara Egit ingin di-approach oleh AI: [`identity/working-principles.md`](identity/working-principles.md)
→ Goals: [`identity/goals.md`](identity/goals.md)

---

## Apa Itu AIRO

**AIRO** adalah nama brand ekosistem AI pribadi Egit. Bukan hanya satu tool — ini adalah seluruh lapisan sistem yang mencakup:

- Agen AI dengan persona berbeda (Earesmes, Arfin, Remin, Bubu)
- Infrastruktur lokal (Hermes, WSL2, Telegram)
- Project-project spesifik (finance automation, YouTube skill, dll.)
- Dokumen-dokumen knowledge dan PRD yang jadi "source of truth"

AIRO Finance (otomatisasi keuangan dengan Google Sheets) adalah **salah satu project** di dalam ekosistem ini, bukan keseluruhan AIRO.

---

## Infrastruktur & Tools

→ Setup WSL, Hermes, systemd: [`systems/infrastructure.md`](systems/infrastructure.md)
→ Telegram sebagai primary interface: [`systems/interfaces.md`](systems/interfaces.md)
→ Tools yang dipakai (clasp, clip.exe, yt-dlp, dll.): [`systems/tools.md`](systems/tools.md)

---

## Agent Family

| Agent | Peran | Status |
|-------|-------|--------|
| **Earesmes** | Orchestrator / asisten utama, persona di Telegram | Aktif (Opsi 3) |
| **Arfin / AIRO Finance** | Finance interface, Google Sheets automation | Aktif, in development |
| **Remin** | Reminders | Planned |
| **Bubu** | Note-keeping | Planned |

→ Detail Earesmes: [`agents/earesmes.md`](agents/earesmes.md)
→ Relasi antar agent: [`agents/agent-family.md`](agents/agent-family.md)
→ Prinsip desain agent: [`agents/design-principles.md`](agents/design-principles.md)

---

## Projects

→ Index semua project: [`projects/_index.md`](projects/_index.md)

---

## Meta

→ Cara pakai repo ini (untuk AI): [`meta/how-to-use-this-brain.md`](meta/how-to-use-this-brain.md)
→ Changelog: [`meta/changelog.md`](meta/changelog.md)

Routing Rules

Use these routing rules before answering or executing.

AIRO Finance

If task is about AIRO Finance:

Read projects/airo-finance.md.
Then read canonical AIRO Finance repo docs.
Do not trust status copied into Second Brain for execution.
The canonical AIRO Finance repo is the source of current implementation truth.
Earesmes / Hermes

If task is about Earesmes or Hermes:

Read projects/earesmes-hermes.md.
Read systems/infrastructure.md.
Read agents/earesmes.md.
Read SECURITY.md before any local execution.
Owner Preferences

If task is about owner preferences, communication style, or working style:

Read identity/working-principles.md.
Read identity/who-i-am.md if relevant.
Execution Tasks

If task involves repo changes, commands, deployment, local files, Google Workspace, or automation:

Read AGENTS.md.
Read SECURITY.md.
Read the relevant project file.
Verify canonical project repo before patching.
History / Forensic Review

If task needs old chat history, prior sessions, or forensic investigation:

Ask owner before reading inbox/ or any archive.
Prefer distilled summaries over raw transcript.
Never import raw chat into canonical files without distillation.
Default

Default read set for most sessions:

BOOT.md
CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
Relevant project file

Routing Rules

Use these routing rules before answering or executing.

AIRO Finance

If task is about AIRO Finance:

Read projects/airo-finance.md.
Then read canonical AIRO Finance repo docs.
Do not trust status copied into Second Brain for execution.
The canonical AIRO Finance repo is the source of current implementation truth.
Earesmes / Hermes

If task is about Earesmes or Hermes:

Read projects/earesmes-hermes.md.
Read systems/infrastructure.md.
Read agents/earesmes.md.
Read SECURITY.md before any local execution.
Owner Preferences

If task is about owner preferences, communication style, or working style:

Read identity/working-principles.md.
Read identity/who-i-am.md if relevant.
Execution Tasks

If task involves repo changes, commands, deployment, local files, Google Workspace, or automation:

Read AGENTS.md.
Read SECURITY.md.
Read the relevant project file.
Verify canonical project repo before patching.
History / Forensic Review

If task needs old chat history, prior sessions, or forensic investigation:

Ask owner before reading inbox/ or any archive.
Prefer distilled summaries over raw transcript.
Never import raw chat into canonical files without distillation.
Default

Default read set for most sessions:

BOOT.md
CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
Relevant project file
