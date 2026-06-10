# Infrastructure — Setup Teknis AIRO

## Environment

| Komponen | Detail |
|----------|--------|
| **OS** | WSL2 Ubuntu 24 (berjalan di Windows) |
| **WSL Username** | `egitaristorandas` |
| **Home directory** | `/home/egitaristorandas/` |
| **Agent runtime** | Hermes (`~/.hermes/hermes-agent/`) |
| **Process manager** | systemd (Hermes dikelola sebagai systemd service) |
| **Python** | venv di dalam Hermes agent directory |

## Hermes / Earesmes

Hermes adalah nama infrastruktur lokal. Earesmes adalah persona/nama agent yang berjalan di atas Hermes.

```
~/.hermes/
├── hermes-agent/       ← Core agent (Python, systemd-managed)
├── memories/           ← Memory files termasuk SOUL.md, CHARTER
└── records/            ← Local file records (interim solution sebelum Notion)
```

**Key files:**
- `~/.hermes/memories/SOUL.md` — Persona Earesmes (Gen Z bestfriend personality)
- `~/.hermes/memories/EARESMES_CHARTER_v0.1.md` — Charter agent
- SOUL.md/CHARTER persistence setelah restart adalah **outstanding unknown** — perlu diverifikasi

## AIRO Finance Repository

- **Path lokal**: `/home/egitaristorandas/vortex-ai-skill-lab`
- **GitHub**: `progamer6918/vortex-ai-skill-lab`
- **Apps Script project aktif**: `apps-script-live`
  - Script ID: `1JVKcn7cR8K3VNDCP2vxKoJl45aS2u2O9I_TU_hWuNRRbFsuz_e6y3Uf0`
  - Deployment ID: `AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA`

## Google OAuth

Token sudah ada dengan 8 authorized scopes:
- Gmail: read, modify, send
- Google Calendar
- Google Drive
- Google Docs
- Google Sheets
- Contacts (readonly)

## Clipboard di WSL

**PENTING**: `xclip` tidak bekerja di WSL2. Gunakan selalu:
```bash
echo "text" | clip.exe
```
`clip.exe` adalah binary Windows native, tidak perlu instalasi.

## Deployment Pattern

Risiko yang diketahui: **deployment mismatch** — kode di repo belum tentu tercermin di behavior live. Selalu verifikasi Apps Script project mana yang live dan push/deploy secara eksplisit setelah perubahan.
