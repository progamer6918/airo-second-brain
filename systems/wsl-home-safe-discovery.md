---
last_updated: 2026-06-10
updated_by: local-wsl-script
status: current
confidence: repo-derived
source: local-wsl-home-safe-discovery
---

# WSL Home Safe Discovery

## Latest Report

- Inbox: `inbox/wsl-home-broad-safe-discovery-2026-06-10-2322.md`
- Candidates: `projects/wsl-home-project-candidates.md`

## Scan Root

- `/home/egitaristorandas`

## Excluded Areas

- .config
- .cache
- .local
- .ssh
- .gnupg
- .npm
- .cargo
- .rustup
- .vscode-server
- node_modules
- venv / .venv
- .git internals

## Policy

- This process captures metadata and safe docs only.
- It must not capture credentials, tokens, private keys, OAuth material, cookies, or raw transcripts.
- Future project-specific execution must inspect the actual project repo before changes.
