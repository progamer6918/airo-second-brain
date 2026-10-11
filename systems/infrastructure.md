# Infrastructure — Setup Teknis AIRO


## Snapshot akses operasional saat ini (Owner-confirmed, 2026-10-11)

- **PC utama:** Windows; WSL telah dihapus. **Jangan otomatis memberikan perintah `wsl`, mengasumsikan distro Linux lokal, atau memakai path home WSL lama pada PC ini.**
- **Jalur SSH yang tersedia untuk Owner:** **Termius pada PC Windows** untuk masuk secara interaktif ke AIRO Tencent VPS. Bukti terminal Owner (2026-10-11): `whoami` menghasilkan `ubuntu`; `hostname` menghasilkan `VM-0-9-ubuntu`.
- **Batas bukti:** output terminal tersebut membuktikan user dan hostname sesi shell, **bukan** secara mandiri fingerprint host, alamat IP publik, izin Codex Cloud, maupun status service Hermes. Sebelum deployment, verifikasi ulang target dan runtime live melalui akses yang sudah diautentikasi.
- **Pemisahan executor:** Termius adalah terminal lokal terautentikasi milik Owner. **Codex Work Cloud tidak otomatis mewarisi koneksi/SSH key Termius.** Jika koneksi Codex Cloud ke VPS gagal dengan `Permission denied (publickey)`, jangan menyimpulkan VPS offline dan jangan memaksa WSL. Gunakan jalur eksekusi yang memang memiliki autentikasi (mis. satu batch perintah yang disiapkan executor dan dijalankan Owner lewat Termius), atau provision akses sementara terpisah secara aman bila disetujui.
- **Keamanan:** repository ASB bersifat publik. Jangan commit kredensial Termius, private key, password, token, screenshot sensitif, `authorized_keys`, atau isi file environment.
- **Batas scope:** status di atas menggambarkan **cara Owner mengakses VPS**, bukan bukti bahwa laptop lain sudah onboard, bahwa Codex memperoleh akses SSH, atau bahwa Hermes sedang sehat.

**Dokumentasi WSL di bawah adalah catatan environment lama, bukan instruksi untuk kondisi PC utama pada 2026-10-11.** Komponen historis mungkin masih relevan untuk arsip atau lingkungan lain, tetapi harus dikonfirmasi dengan bukti runtime sebelum dipakai.


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
