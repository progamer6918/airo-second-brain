# Tools — Arsenal Teknis Ekosistem AIRO

## CLI & Development Tools

| Tool | Fungsi | Catatan |
|------|--------|---------|
| `clasp` | Google Apps Script CLI — push/deploy kode ke Apps Script | Harus eksplisit push setelah perubahan |
| `clip.exe` | Copy ke clipboard di WSL2 | Gunakan ini, BUKAN `xclip` |
| `yt-dlp` | Download YouTube audio/video | Dipakai oleh youtube-launch skill di Hermes |
| `systemctl` | Manage Hermes sebagai systemd service | Start, stop, restart, status |

## Google Workspace Integration

Diakses oleh Earesmes/Hermes melalui Google OAuth tokens yang sudah ada.

**Authorized services:**
- **Gmail** — read, modify, send
- **Google Calendar** — full access
- **Google Drive** — full access
- **Google Docs** — full access
- **Google Sheets** — full access (dipakai AIRO Finance sebagai source of truth)
- **Google Contacts** — readonly

## Infrastructure Tools

| Tool | Fungsi |
|------|--------|
| **Cloudflare Worker** | Proxy untuk AIRO Finance Apps Script |
| **Google Apps Script** | Backend runtime untuk AIRO Finance |
| **Google Sheets** | Source of truth untuk AIRO Finance data |
| **GitHub** | Version control untuk `vortex-ai-skill-lab` (AIRO Finance repo) |
| **Python venv** | Isolated environment untuk Hermes agent |

## Active Skills di Hermes

| Skill | Status | Fungsi |
|-------|--------|--------|
| `google-workspace` | Aktif | Gmail, Calendar, Drive, Sheets, Docs, Contacts |
| `youtube-launch` | Aktif | yt-dlp + Chrome EXE di Windows |

**Outstanding unknowns** (perlu diverifikasi via WSL audit):
- Provider mana yang aktif/readable oleh Hermes
- Skills apa saja yang terdaftar saat ini
- Apakah yt-dlp ada di Hermes venv

## AI Tools

| Tool | Peran dalam AIRO |
|------|-----------------|
| **Claude** | Brainstorming, arsitektur, gap analysis, draft PRD |
| **ChatGPT** | Eksekusi teknis, second opinion, implementasi |
| **Antigravity** | AI executor — menerima PRD sebagai kontrak, one-pass execution |
| **Earesmes** | Daily assistant via Telegram, future orchestrator |
