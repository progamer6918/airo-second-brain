# Projects Index — Ekosistem AIRO

Semua project aktif dan planned di bawah brand AIRO.

---

## Aktif

### AIRO Finance (Arfin)
- **Status**: Aktif, in development
- **Deskripsi**: Sistem otomatisasi keuangan pribadi. Google Sheets sebagai source of truth, Google Apps Script sebagai backend, Cloudflare Worker sebagai proxy, Telegram sebagai interface.
- **Repo**: `progamer6918/vortex-ai-skill-lab`
- **Current milestone**: PRD v2.1.3 finalization → Antigravity execution
- **File detail**: `projects/airo-finance.md`

### Earesmes / Hermes Agent
- **Status**: Aktif, in development
- **Deskripsi**: Local AI agent yang berjalan di WSL2. Primary daily assistant via Telegram.
- **Current milestone**: WSL audit → Google Workspace PRD → Antigravity execution
- **File detail**: Lihat [`agents/earesmes.md`](../agents/earesmes.md)

### AIRO Second Brain (Repo Ini)
- **Status**: Aktif
- **Deskripsi**: Knowledge base terpusat untuk seluruh ekosistem AIRO. Dikonsumsi oleh Hermes, Claude, ChatGPT, Antigravity.
- **Current milestone**: Initial population ✓ → Maintain & update ongoing

---

## Planned

### Remin
- **Status**: Planned
- **Deskripsi**: Reminder system yang terintegrasi dengan Earesmes sebagai orchestrator
- **Dependency**: Earesmes mature dulu

### Bubu
- **Status**: Planned
- **Deskripsi**: Note-keeping system
- **Dependency**: Earesmes mature dulu

### Notion Integration
- **Status**: Deferred
- **Deskripsi**: Integrasi Notion ke ekosistem AIRO untuk knowledge management yang lebih mature
- **Catatan**: Di-defer secara eksplisit. Local file records di `~/.hermes/records/` adalah interim solution.
