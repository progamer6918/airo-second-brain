# Obsidian Wiki Integration Record

Dokumen ini mencatat detail integrasi Obsidian Wiki (Ar9av) ke dalam ekosistem AIRO.

---

## Metadata Integrasi
- **Upstream Repository**: `https://github.com/Ar9av/obsidian-wiki.git`
- **Pinned Tag**: `v2026.06.6`
- **Full Pinned Commit**: `0dc9bfb9739d54f717b724df40ea16706f4f1bc8`
- **Installation Date**: 2026-06-19
- **Dependency Clone Path**: `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki`
- **Vault Path**: `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain`

---

## Selected Skills Installed
Hanya sembilan skill berikut yang diinstal:
1. `wiki-ingest` (Ingest documents/URLs/transcripts)
2. `wiki-query` (Graph-based and indexed semantic queries)
3. `wiki-status` (Wiki health, deltas and hub insights)
4. `wiki-lint` (Fix orphan links and taxonomy state)
5. `wiki-update` (Save current project context to wiki)
6. `wiki-synthesize` (Pair cluster concepts)
7. `cross-linker` (Weave links into graph)
8. `tag-taxonomy` (Controlled tagging)
9. `wiki-dashboard` (Dataview bases indexes)

*Keputusan Desain*: Tidak menjalankan script `setup.sh` bawaan upstream, tidak melakukan `pip install obsidian-wiki` secara global, and tidak menginstal semua skill bawaan untuk menjaga isolasi dan keamanan.

---

## Installation Targets & Method

### 1. Hermes (WSL Ubuntu)
- **Target Path**: `/home/egitaristorandas/.hermes/skills/`
- **Method**: Symbolic link ke folder `.skills/<skill>` di dalam `UPSTREAM_CLONE`.
- **Target Symlinks**:
  - `wiki-ingest` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-ingest`
  - `wiki-query` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-query`
  - `wiki-status` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-status`
  - `wiki-lint` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-lint`
  - `wiki-update` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-update`
  - `wiki-synthesize` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-synthesize`
  - `cross-linker` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/cross-linker`
  - `tag-taxonomy` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/tag-taxonomy`
  - `wiki-dashboard` -> `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki/.skills/wiki-dashboard`

### 2. Google Antigravity (Windows)
- **Target Path**: `C:\Users\Admin\.gemini\antigravity\skills`
- **Method**: Salinan direktori fisik (Copy) dikarenakan operasi lintas sistem berkas (cross-filesystem).
- **Target Folders**:
  - `wiki-ingest`
  - `wiki-query`
  - `wiki-status`
  - `wiki-lint`
  - `wiki-update`
  - `wiki-synthesize`
  - `cross-linker`
  - `tag-taxonomy`
  - `wiki-dashboard`

---

## Excluded Components & Automation
- **Excluded Skills**: `wiki-setup`, `wiki-history-ingest`, `hermes-history-ingest`, `claude-history-ingest`, `codex-history-ingest`, `copilot-history-ingest`, `pi-history-ingest`, `openclaw-history-ingest`, `daily-update`, `wiki-stage-commit`, `wiki-capture`, `wiki-rebuild`, `wiki-import`, `wiki-export`, `memory-bridge`, `wiki-agent`, `vault-skill-factory`, `skill-creator`, `graph-colorize`.
- **Automation Disabled**: Tidak ada auto-sync, cron daemon script, systemd timer daemon, atau plugin komunitas Obsidian yang diinstal.

---

## Maintenance Procedures

### Upgrade Procedure
1. Masuk ke folder `/home/egitaristorandas/.local/share/airo/dependencies/obsidian-wiki`.
2. Lakukan `git fetch --tags origin`.
3. Detach HEAD ke tag baru: `git checkout --detach <NEW_TAG>`.
4. Jalankan script audit untuk memverifikasi kecocokan tree hashes.

### Rollback Procedure
1. Hapus sembilan symlink Hermes di `/home/egitaristorandas/.hermes/skills/` jika masih menunjuk ke clone.
2. Hapus sembilan folder salinan Antigravity di `C:\Users\Admin\.gemini\antigravity\skills/` jika hashes-nya cocok dengan manifest instalasi.
3. Kembalikan cadangan berkas `~/.obsidian-wiki/config` jika ada.
4. Hapus folder `UPSTREAM_CLONE` jika dibuat baru dan belum dimodifikasi.

---

## Known Warnings & Contextual Notes

> [!WARNING]
> **M1B Warning**: Konfigurasi global Linux Obsidian `/home/egitaristorandas/.config/obsidian/obsidian.json` telah dimutasi secara sah selama closeout untuk menetapkan path repositori native Linux `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain` sebagai vault aktif.

> [!NOTE]
> **Runtime Health Status**: Kesehatan runtime sync ASB diamati berstatus `degraded` (pre-existing) dikarenakan keberadaan berkas terproteksi lokal yang kotor (`scripts/airo-manual-queue-process`, `scripts/airo-manual-queue-shortid`, `state/system-health.md`). Scheduler tetap operasional.
