No secret files are staged.
Only allowed append-only files are staged.
Owner has approved that consumer for auto-commit.

Default for ChatGPT/Claude web:

produce closeout text only
do not claim repo write

Default for Hermes/Earesmes local:

may write closeout locally if configured
may commit only after owner allows auto-commit

Default for Antigravity:

may patch requested files during explicit execution task
must report changed files and validation

must not push unless owner asks

<!-- SOURCE_END meta/update-protocol.md -->

<!-- SOURCE_BEGIN meta/staleness-policy.md -->

# Source: meta/staleness-policy.md


last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Second Brain Staleness Policy

Every canonical file should include metadata:

---
last_updated: YYYY-MM-DD
updated_by: owner | agent | owner-confirmed-design
status: current | stale-risk | planned | archived
confidence: verified | owner-confirmed | assumed | unknown
source: repo-derived | live-verified | chat-derived | owner-confirmed | mixed
---
Stale Thresholds
File / Folder	Stale After
CURRENT.md	14 days
state/active-context.md	7 days
projects/*.md	30 days
systems/*.md	60 days
agents/*.md	60 days
identity/*	never auto-stale
decisions/decision-log.md	never auto-stale
SECURITY.md	90 days or whenever tooling changes
AGENTS.md	60 days or whenever workflow changes
Agent Rule

If a file is stale:

Flag it to owner.
Do not silently trust it as current.
Prefer canonical project repo or live evidence when available.
Ask for or perform a current-state refresh if execution depends on it.
Confidence Meaning
verified

Use only when supported by live runtime proof, repo state, commit evidence, readback, or direct source evidence.

owner-confirmed

Use when the owner explicitly confirmed the concept/decision in conversation.

assumed

Use when inferred but not directly verified.

unknown

Use when the agent cannot establish confidence.

<!-- SOURCE_END meta/staleness-policy.md -->

<!-- SOURCE_BEGIN meta/how-to-use-this-brain.md -->

# Source: meta/how-to-use-this-brain.md

# Current startup authority

Begin with `BOOT.md` and follow its startup order. The guidance below is a usage reference; it does not override BOOT startup order or consumer-specific contracts.

# How to Use This Brain — Instruksi untuk AI

Dokumen ini untuk AI yang baru pertama kali mengakses repo `airo-second-brain`.

---

## Kamu Adalah Siapa?

Repo ini dikonsumsi oleh beberapa AI dengan cara berbeda:

| Consumer | Cara Akses | Yang Perlu Dibaca |
|----------|-----------|-------------------|
| **Hermes/Earesmes** | Clone lokal di `~/.hermes/brain/`, baca file via skill | `CONTEXT.md` dulu, lalu file relevan |
| **Claude** | Paste `CONTEXT.md` di awal conversation baru | `CONTEXT.md` + file sesuai topik sesi |
| **ChatGPT** | Upload file per sesi | File yang paling relevan dengan task |
| **Antigravity** | Paste sebagai opening context PRD | `CONTEXT.md` + `identity/working-principles.md` + file project yang akan dieksekusi |

---

## Prinsip Utama saat Bekerja dengan Egit

1. **Semua instruksi teknis harus copy-paste ready** — Egit tidak punya background coding
2. **Flag gaps sebelum mulai** — jangan assume dan lanjut kalau ada yang tidak jelas
3. **Brainstorm dulu, execute belakangan** — ini adalah dua fase terpisah
4. **Dokumen adalah source of truth** — kalau ada konflik antara memory AI dan dokumen, dokumen menang
5. **Bahasa Indonesia** untuk output owner-facing; **English** untuk technical specs

Baca [`identity/working-principles.md`](../identity/working-principles.md) untuk detail lengkap.

---

## Cara Membaca Repo Ini

### Kalau kamu baru pertama kali:
1. Baca `CONTEXT.md` (sudah kamu baca ini)
2. Baca `identity/who-i-am.md` untuk understand siapa Egit
3. Baca `identity/working-principles.md` untuk understand cara kerja yang diharapkan
4. Baca file relevan sesuai task yang sedang dikerjakan

### Kalau kamu diminta bekerja pada project tertentu:
1. Baca `projects/_index.md` untuk overview
2. Baca file project spesifik (misal `projects/airo-finance.md`)
3. Baca agent yang terlibat kalau relevan

### Kalau kamu adalah Antigravity dan mau eksekusi PRD:
1. Baca `CONTEXT.md`
2. Baca `identity/working-principles.md` — terutama bagian "Untuk Antigravity"
3. Baca file project yang relevan
4. Baru baca PRD yang akan dieksekusi

---

## Yang Tidak Ada di Repo Ini

- Detail sensitif atau private yang tidak perlu diketahui AI
- AIRO Finance detail teknis yang sangat spesifik ada di `projects/airo-finance.md` sebatas context — PRD asli ada di repo terpisah

---

## Maintenance

Repo ini diupdate secara manual oleh Egit atau atas permintaan Egit kepada AI. Kalau ada informasi yang terasa outdated, flag ke Egit — jangan assume dan lanjut dengan info yang mungkin stale.

Lihat [`changelog.md`](changelog.md) untuk history perubahan.

<!-- SOURCE_END meta/how-to-use-this-brain.md -->

<!-- SOURCE_BEGIN docs/contracts/ASB_HUMAN_NAVIGATION_CONTRACT.md -->

# Source: docs/contracts/ASB_HUMAN_NAVIGATION_CONTRACT.md

# ASB Human Navigation Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-25
**Authority**: OWNER_APPROVED_UX_CORRECTION

---

## 🧭 Rules of Human Navigation

1. **Intent-First Design**: Human users start from intent ("Mau ngapain?"), not filesystem structures.
2. **Canonical Front Door**: `HOME.md` is the single canonical human launchpad for AIRO Second Brain.
3. **Strict Hierarchy**:
   - `AIRO Home` is Level 0.
   - `AIRO WorkDesk` & `AIRO Finance` are Level 1 worlds.
   - `D-READY` is explicitly a Level 2 child of `AIRO WorkDesk` (`AIRO → WorkDesk → D-READY`).
4. **No Peer Elevation**: Child projects (like D-READY) MUST NOT be elevated to top-level peers of WorkDesk.
5. **Knowledge Discovery Routing**: "Cari Tahu Sesuatu" MUST route to actual professional knowledge topics (`wiki/workdesk/KNOWLEDGE_MAP.md`), NOT architectural planning pages.
6. **No Continuity Duplication**: "Lanjut Kerja" MUST NOT duplicate the main WorkDesk entrypoint or show technical maintenance status. If no specific resumable work item exists, it must state so truthfully.
7. **Rich Work History**: Root Home embeds dynamic Obsidian Base `![[worklog/views/AIRO Worklog.base#Hari Ini]]`; `RIWAYAT_KERJA.md` exposes `Hari Ini`, `Sesi Terbaru`, and full `Riwayat Sesi`.
8. **Global Inventory**: `wiki/AREAS_AND_PROJECTS.md` is the global ASB inventory covering all systems, worlds, bridges, and child projects.
9. **Technical Plumbing Isolation**: Raw Session UUIDs, Git hashes, evidence paths, and governance jargon are hidden from primary human viewports into Obsidian-compatible collapsed sections.
10. **Obsidian Compatibility**: All primary human pages MUST use clean Markdown wikilinks and standard frontmatter `aliases` for Quick Switcher discoverability without requiring third-party plugins.

11. **Root Presentation Placement**: WorkDesk and AIRO Finance remain Level-1 worlds even when their entry links are visually grouped under root `Cari & Jelajah`.
12. **Acceptance Evidence**: Functional HOME acceptance may be established by verified backend evidence covering hierarchy, wikilinks, Base views, session/worklog continuity, vault/source parity, and regression tests. Pixel-level visual evidence is required only when visual appearance/render fidelity is an explicit acceptance objective.
13. **Deferred Work HOME Presentation**:
    - `HOME.md` is the canonical human launchpad and embeds the generated deferred-work projection (`![[state/deferred-work]]`) rather than duplicating PR data.
    - `TODO` PRs use compact, Owner-scannable presentation collapsed by default.
    - Current implementation uses Obsidian-native collapsed callouts (`> [!todo]-`), without third-party plugin dependency.
    - Collapsed summary shows only priority icon + familiar title + project + PR ID + creation date.
    - Expanded content prioritizes human-readable WHY (`context`), WHAT (`detail`), and bounded Owner origin (`origin_text`) when available.
    - Technical metadata (Git SHA, session UUID, evidence paths, schema plumbing, governance jargon) stays out of the primary PR card.
    - Large supporting material should live in a valid canonical reference rather than bloating HOME.

<!-- SOURCE_END docs/contracts/ASB_HUMAN_NAVIGATION_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md -->

# Source: docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md

# WorkDesk Home Operating Surface Contract

**Project:** AIRO_WORKDESK
**Status:** ACCEPTED — CANONICAL
**Date:** 2026-08-11

## Purpose

WorkDesk Home adalah **expert-first operational cockpit dengan beginner-proof navigation**.

Home bukan generic KPI dashboard, training portal, raw repository index, atau static report.

## Information Classes

1. **Business Pulse** = latest supplied operating facts.
2. **Signals** = evidence-backed concern, opportunity, atau decision boundary.
3. **My Commitments** = explicit Owner commitment / confirmed assignment.
4. **Quick Work** = job-to-be-done routing.
5. **Knowledge Updates** = perubahan meaningful pada kemampuan brain.
6. **Explore Brain** = deep professional knowledge.
7. **Work History** = canonical closed WorkDesk sessions.

## Truth Rules

- State ≠ Signal.
- Signal ≠ Commitment.
- Program/meeting date ≠ personal Owner deadline tanpa assignment evidence.
- Semua angka/signal mempertahankan `as-of` / currentness.
- Asynchronous datasets tidak boleh dipresentasikan sebagai same-date snapshot.
- Missing evidence harus tetap visible.
- Market event tidak boleh otomatis menjadi causal proof.
- Derived priority harus dire-evaluate ketika authority/data lebih baru masuk.
- Fake/stale continuation dilarang.

## Live Session Boundary

`airo-session` active state hidup pada external runtime state.

Sampai ada deterministic sanitized session-to-Obsidian bridge, Home tidak menampilkan live-session continuation card yang dibuat manual.

## Case-Driven Delta Refresh

Setiap accepted WorkDesk delta wajib mengevaluasi apakah perlu mengubah:

- `wiki/workdesk/views/BUSINESS_PULSE.md`
- `wiki/workdesk/views/SIGNALS.md`
- `wiki/workdesk/MY_COMMITMENTS.md`
- `wiki/workdesk/updates/`

RAW_INPUT tetap harus melewati canonical input/source-authority rules sebelum dipromosikan ke Home.

## Acceptance

Backend and render acceptance have established:

- content/currentness integrity: PASS;
- semantic and downstream routing: PASS;
- commitment truth guard: PASS;
- no fabricated live continuation: PASS;
- Home information hierarchy and density: PASS;
- knowledge-update runtime surface: PASS;
- existing-vault presentation: PASS.

`HOME_V2_ACCEPTED=YES`

Canonical Git integration is complete. No additional Owner content or visual QA gate remains for Home v2.

## Implemented session projection bridge

The session bridge is governed by `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`. Current-work and active-session presentation remain deterministic derived projections; they do not replace canonical session authority or independently prove live runtime state.

<!-- SOURCE_END docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md -->

<!-- SOURCE_BEGIN registry/consumer-policy.yaml -->

# Source: registry/consumer-policy.yaml

# consumer-policy.yaml
consumers:
  chatgpt:
    allowed_reads:
      - BOOT.md
      - CURRENT.md
      - CONTEXT.md
      - AGENTS.md
      - SECURITY.md
      - state/system-health.md
      - projects/
      - decisions/pending-decisions.md
      - docs/onboarding/
      - docs/contracts/
      - docs/architecture/
      - docs/prd/PRD_AIRO_KNOWLEDGE_CONTINUITY.md
      - docs/operations/AIRO_SESSION_WORKLOG_PROMOTION_SOP.md
      - identity/
      - systems/
      - agents/
      - meta/
      - state/operating-rules/AIRO_COUNCIL_MODE.md
      - registry/consumer-policy.yaml
      - PRD_INDEX.md
      - ROADMAP_INDEX.md
      - AIRO_BOOTSTRAP_INDEX.md
      - control/
      - wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY.md
    allowed_writes:
      - inbox/session-closeouts/
      - distill/proposals/
    promote_allowed: false
  claude:
    allowed_reads:
      - BOOT.md
      - CURRENT.md
      - CONTEXT.md
      - AGENTS.md
      - SECURITY.md
      - state/system-health.md
      - projects/
      - decisions/pending-decisions.md
      - docs/onboarding/
      - docs/contracts/
      - docs/architecture/
      - docs/prd/PRD_AIRO_KNOWLEDGE_CONTINUITY.md
      - docs/operations/AIRO_SESSION_WORKLOG_PROMOTION_SOP.md
      - identity/
      - systems/
      - agents/
      - meta/
      - state/operating-rules/AIRO_COUNCIL_MODE.md
      - registry/consumer-policy.yaml
      - PRD_INDEX.md
      - ROADMAP_INDEX.md
      - AIRO_BOOTSTRAP_INDEX.md
      - control/
      - wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY.md
    allowed_writes:
      - inbox/session-closeouts/
      - distill/proposals/
    promote_allowed: false
  antigravity:
    allowed_reads:
      - "*"
    allowed_writes:
      - scripts/
      - registry/
      - events/
      - logs/
      - distill/proposals/
      - docs/
    promote_allowed: true
    require_owner_review_for_semantic: true
  earesmes:
    allowed_reads:
      - "*"
    allowed_writes:
      - logs/
      - events/raw/
      - state/active-sessions.md
      - state/system-health.md
    promote_allowed: false

  codex:
    # Owner-approved role, 2026-10-05; paths are not blanket mutation consent.
    allowed_reads:
      - "*"
    allowed_writes: []
    # No blanket static write grant; resolve exact task paths from Owner authorization.
    task_scoped_writes_require_owner_authorization: true
    execution_allowed: true
    require_owner_authorized_scope: true
    require_session_evidence_git_guards: true
    promote_allowed: false
    require_owner_review_for_semantic: true

<!-- SOURCE_END registry/consumer-policy.yaml -->

<!-- SOURCE_BEGIN AIRO_BOOTSTRAP_INDEX.md -->

# Source: AIRO_BOOTSTRAP_INDEX.md

# AIRO Bootstrap Index

## Purpose

Canonical navigation entrypoint for fresh AIRO Sync sessions.

This file does not replace BOOT.md.

It provides deterministic routing into the AIRO Second Brain.

---

# Canonical Source

Repository:

https://github.com/progamer6918/airo-second-brain


# First Read

Always start from:

BOOT.md


Then follow:

- ASB read order
- source priority
- contracts
- guards
- operating rules


# AIRO WorkDesk Routing

For business intelligence queries:

Default project:

AIRO_WORKDESK


Business query examples:

- Retail Sales
- Market Share
- Dealer Performance
- Territory
- Ring
- POLREG
- FLP Productivity
- Customer
- RO
- FINCO


Resolve:

wiki/workdesk/reference/AWD_CAPABILITY_REGISTRY.md


# Operational Authority Discovery

Before requesting user data, check:

1. AWD Capability Registry
2. Operational Data Inventory
3. Source Authority


Expected authorities:

- Retail Sales Authority
- Market Share Authority
- POLREG/Territory Authority
- Dealer Network Authority
- FLP Authority
- Customer/RO/FINCO Authority


# Failure Rule

Do not conclude:

"I don't have data"

until canonical discovery has been attempted.


If source retrieval is unavailable:

request:

- BOOT.md
- CURRENT.md
- state/active-context.md


# Expected Fresh Session Flow

Fresh Session

↓

AIRO Bootstrap Index

↓

BOOT.md

↓

ASB Rules

↓

AWD Capability Registry

↓

Authority Source

↓

Business Analysis

<!-- SOURCE_END AIRO_BOOTSTRAP_INDEX.md -->

<!-- SOURCE_BEGIN systems/infrastructure.md -->

# Source: systems/infrastructure.md

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

