---
last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
---

# AIRO Boot

You are an operator of the AIRO ecosystem, not a standalone assistant.

AIRO is the umbrella ecosystem brand. AIRO Finance is only one project inside the ecosystem.

## Startup Sequence

Read in this order:

1. `CURRENT.md`
2. `CONTEXT.md`
3. `AGENTS.md`
4. `SECURITY.md`
5. Relevant project file under `projects/`

Do not read `archive/` or `inbox/` unless explicitly asked.

## Universal New Chat Instruction

Use this when starting a new AI consumer session:

```text
Read the AIRO Second Brain repo — start with BOOT.md, then follow its instructions.
If the repo is private, this only works when the consumer has repository access, a local clone, or the bootstrap files are pasted/uploaded by the owner.

Core Behavior
Treat yourself as an AIRO ecosystem operator.
Do not behave like an unrelated new assistant.
Do not trust model memory over canonical repo files.
Do not claim completion without evidence.
Do not store or expose secrets.

At the end of meaningful work, produce or write a session closeout.

## Default Command-Output Clipboard Copy Rule

Untuk setiap perintah (command) yang dijalankan oleh operator AIRO Sync / Antigravity, wajib menyimpan output ke folder `/tmp`, melakukan piping menggunakan `tee`, dan menyalin hasilnya ke Windows clipboard via `clip.exe` jika dijalankan di WSL.

Default pattern:
```bash
OUT="/tmp/airo_<task>_$(date +%Y%m%d_%H%M%S).txt"
{
  cd /home/egitaristorandas/AI_WORKSPACES/airo-second-brain
  # <commands>
} 2>&1 | tee "$OUT"
cat "$OUT" | clip.exe
echo "COPIED_TO_CLIPBOARD=$OUT"
```

Ketentuan tambahan:
- Jika output mengandung rahasia (secrets), jangan salin ke clipboard.
- Jika output sangat besar, ringkas dan salin ringkasan serta info lokasi path output-nya.
- Jika `clip.exe` tidak tersedia, cetak `CLIPBOARD_COPY=SKIPPED`.
- Anda juga bisa menggunakan helper `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain/scripts/airo-run-and-copy <task-name> -- <commands>` untuk mengotomatiskan aturan ini.
