---
last_updated: 2026-06-10
updated_by: local-wsl-script
status: current
confidence: repo-derived
source: local-wsl-scan
---

# WSL Local Workspace Map

## Approved Scan Roots

- `/home/egitaristorandas/AI_WORKSPACES`
- `/home/egitaristorandas/vortex-ai-skill-lab`

## Scan Policy

- Git repositories are discovered by locating `.git` directories.
- Secret-like file contents are never read.
- Safe documentation excerpts may be captured from README/PRD/AGENTS/CLAUDE/BOOT/CONTEXT style markdown files.
- Large docs are skipped from excerpts.
- Runtime folders such as node_modules, venv, .venv, cache, and .git are excluded.

## Latest Ingest

- Inbox report: `inbox/wsl-full-safe-ingest-2026-06-10-2319.md`
- Workspace index: `projects/wsl-workspace-index.md`
