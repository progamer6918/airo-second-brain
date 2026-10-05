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

<!-- SOURCE_END systems/infrastructure.md -->

<!-- SOURCE_BEGIN systems/interfaces.md -->

# Source: systems/interfaces.md

# Interfaces — Cara Egit Berinteraksi dengan AIRO

## Primary Interface: Telegram

**Telegram adalah satu-satunya primary daily interface** untuk semua agent di ekosistem AIRO.

Kenapa Telegram:
- Mobile-first, selalu tersedia
- Bot API yang mature dan reliable
- Bisa handle text, file, command, inline buttons
- Satu tempat untuk semua agent (Earesmes, Arfin, dll. masing-masing punya bot/persona sendiri)

**Pattern penggunaan**:
- Daily interaction dengan Earesmes → via Telegram
- Finance commands ke Arfin → via Telegram
- Semua notifikasi dan output dari sistem → via Telegram

## Secondary Interface: WSL Terminal

Digunakan **hanya** untuk setup, debugging, dan maintenance sistem — bukan untuk daily use.

Akses: Windows Terminal → WSL2 Ubuntu

## Interface per Agent

| Agent | Interface | Keterangan |
|-------|-----------|------------|
| Earesmes | Telegram bot | Primary asisten, daily use |
| Arfin / AIRO Finance | Telegram bot | Finance commands & queries |
| Claude.ai | Web/mobile | Brainstorming, arsitektur, drafting |
| ChatGPT | Web/mobile | Eksekusi, second opinion |

## Owner-Facing vs Technical Layer

Semua output yang Egit lihat sehari-hari (via Telegram) ditulis dalam **Bahasa Indonesia**.
Semua dokumentasi teknis, PRD, dan konfigurasi sistem ditulis dalam **English**.

<!-- AIRO_TELEGRAM_IDENTITY_GUARD_BEGIN -->
## Telegram Identity Boundary

- Earesmes, Arfin, and EarnsAI use distinct existing Telegram bot identities.
- Earesmes is backed by Hermes/WSL.
- Arfin is the direct and independent AIRO Finance interface.
- A cross-project webhook binding is an incident, not intentional shared-bot
  architecture.
- Identity and evidence-scope rules are canonical in
  `telegram-agent-identity-contract.md`.
<!-- AIRO_TELEGRAM_IDENTITY_GUARD_END -->

## Current role authority

Descriptions of consumer capabilities in this reference do not grant execution authority. Current role boundaries are governed by `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md` and `docs/contracts/AIRO_CONSUMER_IDENTITY_BOUNDARY.md`.

<!-- SOURCE_END systems/interfaces.md -->

<!-- SOURCE_BEGIN systems/tools.md -->

# Source: systems/tools.md

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

## Current role authority

Descriptions of consumer capabilities in this reference do not grant execution authority. Current role boundaries are governed by `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md` and `docs/contracts/AIRO_CONSUMER_IDENTITY_BOUNDARY.md`.

<!-- SOURCE_END systems/tools.md -->

<!-- SOURCE_BEGIN systems/repository-registry.md -->

# Source: systems/repository-registry.md

---
last_updated: 2026-06-11
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
---

# Repository Registry

This file is the central registry for repositories and knowledge sources that belong to, support, or inform the AIRO ecosystem.

AIRO Second Brain is the canonical knowledge hub. Other repositories may contain implementation, experiments, tools, skills, automations, or reference material, but durable knowledge should be summarized or linked from this repo so future AIRO operators do not depend on scattered context.

## Core Rule

Do not treat external repositories, past chats, or model memory as canonical unless they are represented in AIRO Second Brain.

When important knowledge exists outside this repo, convert it into one of these forms:

- a project file under `projects/`
- a system file under `systems/`
- an agent/operator rule under `AGENTS.md`
- durable context under `CONTEXT.md`
- active status under `CURRENT.md`

## Core Hub

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/airo-second-brain` | Canonical AIRO knowledge hub | Active | Start from `BOOT.md`, then follow the startup sequence. |

## AIRO Ecosystem Repositories

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/airo-finance` | AIRO Finance implementation/project repo | Active / registered | AIRO Finance is one project inside the broader AIRO ecosystem, not the whole ecosystem. |
| `progamer6918/vortex-ai-skill-lab` | AI skills, experiments, and reusable capability lab | Registered | Important skills should be summarized into AIRO Second Brain before being treated as durable operator knowledge. |

## EarnsAI / Trading Repositories

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/earnai-pulse-trading` | Trading system / pulse trading workstream | Registered | Needs project context capture before future operators rely on it. |
| `progamer6918/earnai-telegram-gateway` | Telegram gateway / integration workstream | Registered | Needs architecture and operational notes captured if active. |
| `progamer6918/earnai-trading-research-lab` | Trading research and experimentation workstream | Registered | Research conclusions should be distilled into AIRO Second Brain. |
| `progamer6918/earnai-notion-agent-os` | Notion agent operating system / workflow automation | Registered | Needs workflow and agent behavior mapping if still active. |

## Reference / Learning Repositories

These repositories are useful as learning or reference sources, but they are not canonical AIRO memory by themselves.

| Repository | Role | Status | Notes |
|---|---|---|---|
| `progamer6918/the-art-of-command-line` | Command line learning/reference | Reference | Use as supporting material only. |
| `progamer6918/developer-roadmap` | Developer learning roadmap/reference | Reference | Use as supporting material only. |
| `progamer6918/build-your-own-x` | Engineering learning/reference | Reference | Use as supporting material only. |

## Knowledge Capture Policy

For every active repository, AIRO Second Brain should eventually contain:

- what the repository is for
- whether it is active, paused, archived, or reference-only
- where its canonical project context lives
- the current next step
- constraints, risks, and important decisions
- how a new AI operator should continue the work without guessing

## Recommended Mapping

Current recommended mapping:

| Workstream | Canonical AIRO file |
|---|---|
| AIRO ecosystem overview | `CURRENT.md`, `CONTEXT.md`, `AGENTS.md`, `systems/repository-registry.md` |
| Report Automation VBA | `projects/report-automation-vba.md` |
| AIRO Finance | `projects/airo-finance.md` or existing finance project file |
| Vortex AI Skill Lab | `projects/vortex-ai-skill-lab.md` or `systems/skills-registry.md` |
| EarnsAI / trading workstreams | dedicated project files under `projects/` after owner confirmation |

## Cleanup Rule

Do not create one project file per chat, one per bug, or one per small experiment.

Create one project file per durable workstream.

When a workstream grows too large for one file, promote it from:

```text
projects/example-workstream.md
to:

projects/example-workstream/
├── README.md
├── decisions.md
├── runbook.md
└── session-closeouts.md
Current Next Step

Capture the active Report Automation VBA project in:

projects/report-automation-vba.md

Then add a short pointer in:

CURRENT.md

<!-- SOURCE_END systems/repository-registry.md -->

<!-- SOURCE_BEGIN systems/wsl-local-workspace-map.md -->

# Source: systems/wsl-local-workspace-map.md

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

<!-- SOURCE_END systems/wsl-local-workspace-map.md -->

<!-- SOURCE_BEGIN systems/wsl-home-safe-discovery.md -->

# Source: systems/wsl-home-safe-discovery.md

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

<!-- SOURCE_END systems/wsl-home-safe-discovery.md -->

<!-- SOURCE_BEGIN systems/telegram-agent-identity-contract.md -->

# Source: systems/telegram-agent-identity-contract.md

# Telegram Agent Identity and Evidence-Scope Contract

status: current
authority: owner-confirmed
scope: Telegram bot identity, ownership, intake topology, and AI reasoning

## Canonical identity ownership

### Earesmes

- Earesmes is the primary AIRO assistant and orchestrator persona.
- Hermes is the local WSL runtime underneath Earesmes.
- Earesmes uses its existing dedicated Earesmes Telegram bot.
- The Earesmes bot is not the Arfin bot.
- Its canonical intake is the local persistent gateway acting as the sole
  getUpdates consumer for the Earesmes token.

### Arfin / AIRO Finance

- Arfin is the dedicated AIRO Finance persona.
- Arfin uses its existing dedicated Arfin Telegram bot.
- The Arfin bot is not the Earesmes bot.
- Arfin remains direct and independent until the Owner activates a different
  orchestration model.
- Its credentials may reside in Apps Script Script Properties, Cloudflare
  Worker secrets, or another approved production secret store.

### EarnsAI

- EarnsAI uses its existing dedicated EarnsAI Telegram bot.
- Its bot identity and runtime are independent from Earesmes and Arfin.

## Evidence-scope rule

Every bot, token, webhook, process, and configuration audit must declare the
scope it actually inspected.

A local WSL filesystem scan proves only what was found in the scanned local
paths. It does not prove the presence or absence of credentials in production
secret stores, Apps Script, Cloudflare, BotFather, another machine, or any
unscanned location.

Forbidden inference:

not found in local WSL files -> does not exist in the AIRO ecosystem

Permitted conclusion:

not found within the declared local WSL scan scope

## Fail-closed identity rule

Before recommending any bot creation, token rotation, webhook deletion,
webhook reassignment, polling change, or cross-agent routing change, the AI
operator must truthfully establish:

- the identity contract was read;
- Earesmes and Arfin ownership were resolved;
- the evidence scope was declared;
- local absence was not treated as global absence;
- production secret scope is verified or explicitly unknown;
- the Owner architecture decision was read.
- explicit Owner approval is required for every bot-identity architecture change.

If these conditions are incomplete:

- mutation is not allowed;
- new-bot recommendations are not allowed;
- token-rotation recommendations are not allowed;
- webhook mutation recommendations are not allowed;
- the next action is read-only attribution.

## Mandatory visible response receipt

Every substantive Telegram architecture response must emit one of the following
receipts before giving a technical conclusion, recommendation, command, or
mutation plan.

PASS receipt:

AIRO_AGENT_IDENTITY_GUARD=PASS
IDENTITY_CONTRACT_READ=YES
EARESMES_BOT_OWNERSHIP=RESOLVED
ARFIN_BOT_OWNERSHIP=RESOLVED
EARNSAI_BOT_OWNERSHIP=RESOLVED_OR_NOT_RELEVANT
EVIDENCE_SCOPE_DECLARED=YES
LOCAL_ABSENCE_USED_AS_GLOBAL_ABSENCE=NO
PRODUCTION_SECRET_SCOPE_STATUS=VERIFIED_OR_EXPLICITLY_UNKNOWN
OWNER_ARCHITECTURE_DECISION_READ=YES
NEW_BOT_RECOMMENDATION_ALLOWED=NO
TOKEN_ROTATION_RECOMMENDATION_ALLOWED=NO
WEBHOOK_MUTATION_ALLOWED=NO
MUTATION_ALLOWED=ONLY_WITH_SEPARATE_OWNER_APPROVAL

FAIL receipt:

