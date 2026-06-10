---
last_updated: 2026-06-10
updated_by: local-wsl-script
status: current
confidence: repo-derived
source: local-wsl-metadata-and-safe-doc-excerpts
---

# WSL Full Safe Knowledge Ingest — 2026-06-10 23:19 +0700

## Scope

- Consumer: local WSL script
- Target: all detected git repositories under approved WSL workspace roots
- Purpose: populate AIRO Second Brain with safe workspace knowledge beyond AIRO Finance

## Approved Roots

- /home/egitaristorandas/AI_WORKSPACES
- /home/egitaristorandas/vortex-ai-skill-lab

## Safety Policy

- No raw full workspace dump
- No token/credential/secret files
- No .env
- No OAuth/client secret files
- No cookie/auth files
- No full email bodies
- Only repo metadata and safe documentation excerpts

## Repositories Found


### airo-second-brain

- Path: `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain`
- Branch: `main`
- Latest commit: `5efcf92 docs: capture WSL workspace scan`
- Status short:
```text
?? inbox/wsl-full-safe-ingest-2026-06-10-2319.md
```
- Remotes:
```text
origin	https://github.com/progamer6918/airo-second-brain.git (fetch)
origin	https://github.com/progamer6918/airo-second-brain.git (push)
```

#### Key files detected
```text
AGENTS.md
BOOT.md
CONTEXT.md
CURRENT.md
README.md
```

#### Safe documentation excerpts

##### AGENTS.md

```text

last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Agents Operating Rules

All consumers are interface-specific operators of the same AIRO ecosystem.

Consumers include ChatGPT, Claude, Claude Code, Hermes/Earesmes, Antigravity, OpenClaw, local WSL agents, and future AIRO workers.

Do not behave as a new independent assistant.

Session Start

At the start of every meaningful session:

Read BOOT.md.
Read CURRENT.md.
Read CONTEXT.md.
Read AGENTS.md.
Read SECURITY.md.
Read the relevant project file under projects/.

Do not read inbox/ or archive/ unless the owner explicitly asks for history/forensic review.

Source Priority

If context conflicts, follow this priority:

Live runtime evidence
Canonical project repo
state/active-context.md
decisions/decision-log.md
projects/*.md
CURRENT.md
inbox/
Chat summaries
Model memory

Never let model memory override project reality.

During Session
Use Bahasa Indonesia for owner-facing communication.
Be direct, practical, and evidence-driven.
Never claim a task is done without evidence.
Never claim deployment/test/readback PASS unless actually verified.
Never overwrite local files without approval.
Never inspect or expose credentials.
Never introduce a new roadmap when an official roadmap exists.
Distinguish facts, assumptions, recommendations, and next actions.
Use safe commands and explain destructive risk before execution.
For project execution, read the project canonical repo before patching.
Session End

At the end of every meaningful session, produce a session closeout.

If the consumer has safe local repo write access, it may write:

inbox/[consumer]-[YYYY-MM-DD]-[HHMM].md

and append to:

state/active-context.md
meta/changelog.md

Auto-write is allowed for inbox/state/changelog when configured.

Auto-commit is allowed only for configured local consumers with git access and only for non-canonical append-only updates.

Canonical files require owner approval before modification.

Canonical files include:

CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
identity/*
projects/*
decisions/decision-log.md
meta/update-protocol.md
meta/staleness-policy.md
Session Closeout Template
# Session Closeout — [Consumer] — [YYYY-MM-DD HH:mm]

## Project / Topic
-

## Summary
-

## Decisions
-

## Pending Decisions
-

## Files / Repos Touched
-

## Evidence / Tests / Readbacks
-

## Blockers / Risks
-

## Next Action
-
Never Store

Never store or commit tokens, API keys, OAuth credentials, Telegram bot tokens, OTP/2FA/security codes, full email bodies, raw chat transcripts, local auth files, cookie files, .env, .clasp.json, .clasprc.json, credentials*.json, or token*.json.
```

##### BOOT.md

```text
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
```

##### CONTEXT.md

```text
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

```

##### CURRENT.md

```text

last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Current State
Active Focus
AIRO Second Brain: being upgraded into a shared canonical knowledge base / AIRO Kernel.
Earesmes/Hermes: local WSL AI agent via Telegram, intended as the main local operator node.
AIRO Finance: active project, but canonical status lives in the vortex-ai-skill-lab repo.
Owner Preferences Quick Reference
Owner-facing communication: Bahasa Indonesia.
Preferred execution style: safe, explicit, no hallucinated status.
Coding skill assumption: owner is beginner; commands must be copy-paste friendly.
Do not overwrite local changes without approval.
Do not claim PASS or DONE without evidence.
Distill knowledge; do not dump raw chat into canonical files.
Different consumers should behave as one AIRO operator across tools.
Current Architecture Decision

AIRO Second Brain is not a raw transcript dump.

Use this layer model:

inbox/ = session closeout capture.
state/ = current active context.
decisions/ = final and pending decisions.
projects/ = project pointers and summaries.
identity/, systems/, agents/, meta/ = stable operating knowledge.
Read Next
For owner preferences: identity/working-principles.md
For project list: projects/_index.md
For execution rules: AGENTS.md
For safety rules: SECURITY.md
For AIRO Finance: projects/airo-finance.md, then canonical repo docs

For Earesmes/Hermes: projects/earesmes-hermes.md
```

##### README.md

```text

Quick Start for AI Consumers

Start here:

Read BOOT.md, then follow its instructions.

If this repo is private, the consumer must have repository access, local clone access, or the owner must paste/upload the relevant bootstrap files.

Default read order:

BOOT.md
CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
Relevant project file under projects/
# AIRO Second Brain

Repository ini adalah **knowledge base pribadi ekosistem AIRO** — milik Egit.

Berisi konteks tentang identitas, sistem, agent, dan project yang membentuk AIRO sebagai personal AI operating system.

## Untuk AI yang Baru Pertama Kali Masuk

Baca [`CONTEXT.md`](CONTEXT.md) terlebih dahulu. File itu adalah router ke semua knowledge yang relevan.

## Untuk Manusia

Repo ini private. Strukturnya dirancang agar AI (Hermes, Claude, ChatGPT, Antigravity, dll.) bisa mengkonsumsi knowledge ini dengan cara yang paling efisien sesuai kebutuhan mereka.

## Struktur

```
airo-second-brain/
├── CONTEXT.md                  ← Router utama (baca ini dulu)
├── identity/                   ← Siapa Egit, cara kerja, goals
├── systems/                    ← Infrastruktur, tools, interfaces
├── agents/                     ← Earesmes dan agent family lainnya
├── projects/                   ← Semua project di ekosistem AIRO
└── meta/                       ← Instruksi penggunaan repo ini
```
```

### vortex-ai-skill-lab

- Path: `/home/egitaristorandas/vortex-ai-skill-lab`
- Branch: `main`
- Latest commit: `d9a3e46 fix(airo-finance): route debt approval to hutang projection`
- Status short:
```text
 M docs/airo-finance/sprint7d/real_email_source_setup_config_20260527.json
 M docs/personal-workflow/handoff/AIRO_FINANCE_ACCOUNT_LEDGER_PARITY_DELTA_CARRYOVER.md
?? scripts/personal-workflow/birthday_reminder.py
?? scripts/personal-workflow/birthday_reminder_simple.py
?? scripts/personal-workflow/run_birthday_reminder
?? scripts/personal-workflow/ultah_sederhana.csv
```
- Remotes:
```text
origin	git@github.com:progamer6918/vortex-ai-skill-lab.git (fetch)
origin	git@github.com:progamer6918/vortex-ai-skill-lab.git (push)
```

#### Key files detected
```text
.pytest_cache/README.md
README.md
_ops_backups/apps_script_rotation_20260525_230039/README.md
airo_personal_workflow/README.md
docs/AIRO_FINANCE_PRD_LIVING.md
docs/personal-workflow/README.md
tests/personal-workflow/.pytest_cache/README.md
```

#### Safe documentation excerpts

##### .pytest_cache/README.md

```text
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
```

##### README.md

```text
# Vortex AI Skill Lab

This repo is a personal AI skill library.

It converts useful public GitHub repositories into practical skill cards, playbooks, templates, and workflows that can be reused across projects.

## Initial Skill Sources

- build-your-own-x
- developer-roadmap
- the-art-of-command-line

## Main Skill Areas

- Roadmap planning
- Project building
- Command-line operation
- Safe terminal workflow
- GitHub project handover
- AI agent workflow design
```

##### _ops_backups/apps_script_rotation_20260525_230039/README.md

```text
# AIRO Apps Script Project Rotation Backup

- Timestamp: 2026-05-25T23:00:49+07:00
- Repo: /home/egitaristorandas/vortex-ai-skill-lab
- Old clasp dir: apps-script-live
- New clasp dir prepared: apps-script-prod-v2
- Backup root: /home/egitaristorandas/vortex-ai-skill-lab/_ops_backups/apps_script_rotation_20260525_230039
- Reason: old Apps Script project reached 200 immutable versions
- Sprint: Sprint 4 Finance Events remains active
- Important: this rotates Apps Script project/version container only, not repo architecture and not Google Sheet

## Current git head
c0d57f2 fix(airo-finance): surface Finance Events emission failures
1a1e1ed docs(airo-finance): record Sprint 4 post-deploy live blockers
72afd38 docs(airo-finance): record Sprint 4 cash Finance Events production update
86ca693 fix(airo-finance): emit Finance Events for cash Account Ledger writes
af13a70 docs(airo-finance): correct Sprint 4 schema verify status

## Next manual-sensitive items
- Create new Apps Script project with clasp in apps-script-prod-v2
- Set Script Properties in new project: BOT_TOKEN and SPREADSHEET_ID
- Deploy new Web App
- Update Cloudflare Worker APPS_SCRIPT_URL to new Web App URL
- Keep old project until new smoke passes
```

##### airo_personal_workflow/README.md

```text
# Airo Personal Workflow Core

Local-first personal workflow core for Airo.

## MVP Capability

- SQLite database schema
- personal finance tracking
- installment tracking
- attachment index
- audit log
- approval queue
- basic transaction parser

## Not Included Yet

- OAuth credentials
- Google API live write
- Telegram live bot hook
- OCR
- Gmail automation
```

##### docs/AIRO_FINANCE_PRD_LIVING.md

```text
# AIRO FINANCE — FINAL LIVING PRD v2.1.3

Execution Contract after Architecture Freeze Audit

PRD Version      : 2.1.3
Status           : CANONICAL EXECUTION CONTRACT — READY FOR OWNER-APPROVED REPO REPLACEMENT
Last verified    : 2026-06-03 19:40 WIB
Repo baseline    : bd6815e
Feature baseline : a4fd0ac — Phase 6H-G3 category registry fix
Apps Script      : apps-script-live @241
Deployment ID    : AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA
Worker           : airo-finance-telegram-proxy → env.APPS_SCRIPT_URL unchanged
Gmail trigger    : NOT INSTALLED
Email ingestion  : DISABLED
Alert Engine     : SAFE MODE, trigger installed, proactive send OFF
E-path layer 1   : LIVE PASS @241
Audit basis      : Architecture Freeze Audit Pack 1, Pack 1B, Pack 2

---

## 0. Status Claim

This PRD is execution-ready after repo, active source, deployment, workbook schema, and dashboard contract audit.

Allowed claim:

```text
No known architecture-level blocker remains undocumented after Architecture Freeze Audit.
Antigravity may execute in task-contract mode with no roadmap discovery expected.
```

Forbidden claim:

```text
zero bug
zero mistake
zero implementation issue
project already ready-to-use
```

This document removes known architecture ambiguity. It does not remove the need for task-level tests, deployment verification, Telegram live smoke, and workbook readback.

---

## 1. Purpose

This document is the execution contract for completing AIRO Personal Finance Command Center.

Antigravity must not use this document as passive documentation. It must execute tasks in order, respect stop gates, avoid speculative redesign, and report evidence after every task.

A task is done only when all layers align:

```text
repo source
→ Apps Script editor synced
→ Apps Script deployed using existing deployment ID
→ Cloudflare Worker target unchanged or explicitly approved
→ Telegram live behavior matches expected
→ Google Sheet write/readback verified
→ PRD/current-state evidence updated
→ committed and pushed
```

Feature existence in repo is not sufficient.

---

## 2. Non-Negotiable Architecture

Do not redesign the system unless the owner explicitly approves a breaking change.

### 2.1 Platform

Google Spreadsheet remains the operational workspace and source-of-truth for current v1.

No web app, localhost backend, SaaS migration, or external database migration is in current scope.

### 2.2 Interface

Telegram is the primary owner-facing interface for:

```text
manual transaction input
cash transaction input
clarification replies
admin commands
approval actions
Review Queue actions
alert acknowledgement
email clarification replies
```

Email never replaces Telegram manual input.

### 2.3 Runtime

```text
Google Apps Script = main backend runtime
Cloudflare Worker = Telegram proxy / async_ack bridge
Gmail = optional passive input only
GitHub repo = canonical docs and source control
```

### 2.4 Data Layers

```text
Account Ledger = wallet/account movement only
Finance Events = central event index, not balance ledger
Credit Card = credit card domain truth
Hutang = debt/liability/receivable domain truth
Aset = asset/gold/domain truth
Cicilan Rumah = home installment domain truth
Review Queue = unresolved exception fallback + email staging gate
Audit Log = script/admin/reconciliation trail
Dashboard = intelligence cockpit, not source-of-truth
Monthly Review = legacy/partial until rewired
Transactions = visible but forbidden as v1 master
Cash Ledger = hidden legacy/transitional
```

```

## Distillation Notes

- This is a safe ingest layer, not final canonical truth for every project.
- Future distillation should promote stable findings into project-specific files only after review.
- Repositories with dirty git status may need separate cleanup before execution.
