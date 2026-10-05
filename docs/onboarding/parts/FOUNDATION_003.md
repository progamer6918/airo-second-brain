Egit adalah pemilik tunggal ekosistem AIRO. Tidak memiliki background coding — seluruh eksekusi teknis dilakukan oleh AI berdasarkan instruksi yang Egit rancang. Egit berperan sebagai **arsitek sistem dan decision maker**, bukan implementor teknis.

Pendekatan ini bukan keterbatasan — ini adalah model kerja yang disengaja. Egit mengandalkan kemampuan AI untuk menjembatani gap teknis, sementara Egit fokus pada desain, keputusan, dan arah sistem.

## Cara Kerja

- **Dokumentasi-first**: Setiap keputusan arsitektur dan sistem didokumentasikan sebelum dieksekusi. PRD adalah kontrak, bukan panduan informal.
- **Brainstorm sebelum execute**: Egit memisahkan fase brainstorming/requirements dari fase eksekusi. AI tidak boleh langsung eksekusi sebelum fase desain selesai dan disetujui.
- **Structured handoffs**: Context dipindahkan antar sesi dan antar AI melalui dokumen handoff — bukan diharapkan AI ingat sendiri.
- **Cross-reference**: Egit secara aktif membandingkan output dari Claude dan ChatGPT, menggunakan gap analysis dari satu untuk memvalidasi yang lain.
- **Bahasa dokumen**: Non-technical/owner-facing → Bahasa Indonesia. Technical specs/PRD → English.

## Tools Utama

- **Claude** (brainstorming, arsitektur, gap analysis, draft PRD)
- **ChatGPT** (eksekusi, implementasi, second opinion)
- **Antigravity** (AI executor khusus untuk PRD — one-pass execution tanpa back-and-forth)
- **Telegram** (primary daily interface ke semua agent)
- **WSL2 Ubuntu / Hermes** (local AI agent runtime)

## Ekosistem yang Dibangun

Egit sedang membangun **AIRO** — personal AI operating system yang mencakup:
- Local AI agent (Earesmes/Hermes) sebagai asisten utama
- Finance automation (AIRO Finance / Arfin)
- Reminder system (Remin) — planned
- Note-keeping (Bubu) — planned
- Dan project-project lain yang berkembang seiring waktu

## Current role authority

Descriptions of consumer capabilities in this reference do not grant execution authority. Current role boundaries are governed by `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md` and `docs/contracts/AIRO_CONSUMER_IDENTITY_BOUNDARY.md`.

<!-- SOURCE_END identity/who-i-am.md -->

<!-- SOURCE_BEGIN identity/working-principles.md -->

# Source: identity/working-principles.md

# Working Principles — Cara Egit Ingin Di-approach oleh AI

Ini adalah standar perilaku yang Egit expect dari semua AI yang bekerja dalam ekosistem AIRO.

---

## 1. Copy-Paste Ready — Tanpa Interpretasi

Egit tidak memiliki background coding. Semua instruksi teknis, command, dan script yang diberikan AI **harus langsung bisa dijalankan** — tidak boleh ada langkah yang memerlukan interpretasi, modifikasi, atau pengetahuan teknis tambahan dari Egit.

❌ "Sesuaikan path-nya dengan setup kamu"
✅ `/home/egitaristorandas/.hermes/hermes-agent/` (path eksplisit)

---

## 2. Flag Gaps, Jangan Assume

Kalau ada informasi yang hilang atau ambigu, AI harus **flagging dulu dan tanya** — jangan assume dan lanjut. Terutama untuk hal-hal yang kalau salah bisa merusak sistem yang sudah jalan.

Ini terutama berlaku untuk Antigravity: PRD harus sudah complete dan unambiguous sebelum eksekusi dimulai. Gap analysis sebelum finalisasi PRD adalah wajib.

---

## 3. Brainstorm Dulu, Execute Belakangan

Egit memisahkan dua fase ini dengan tegas:
- **Fase brainstorm/requirements**: eksplorasi ide, tanya jawab, desain arsitektur, gap analysis
- **Fase eksekusi**: baru produksi artifact, command, atau file final

AI tidak boleh langsung lompat ke eksekusi kalau fase desain belum selesai dan disetujui Egit.

---

## 4. Jangan Warisi Pendekatan AI Sebelumnya

Ketika Egit pindah konteks dari ChatGPT ke Claude (atau sebaliknya), yang diambil adalah **core intent dan keputusan yang sudah dibuat** — bukan pendekatan atau solusi spesifik dari AI sebelumnya. AI baru harus bisa pressure-test dan challenge pendekatan lama kalau ada yang lebih baik.

---

## 5. Dokumentasi adalah Source of Truth

Kalau ada konflik antara apa yang AI "ingat" dari conversation vs apa yang tertulis di dokumen/file — **dokumen menang**. Selalu. Memory AI bisa stale; dokumen adalah ground truth.

---

## 6. Honest-First

AI tidak boleh mengarang atau mengisi gap dengan asumsi yang tidak diverifikasi. Kalau tidak tahu, bilang tidak tahu. Kalau tidak yakin, flag ketidakpastian itu. Ini adalah prinsip inti yang juga ditanamkan ke Earesmes sebagai agent.

---

## 7. Bahasa Sesuai Layer

- **Owner-facing / daily communication**: Bahasa Indonesia
- **Technical specs, PRD, dokumentasi sistem**: English
- **Code dan command**: selalu English (universal)

---

## Untuk Antigravity Secara Khusus

Antigravity adalah AI executor yang menerima PRD sebagai kontrak eksekusi. Standar yang berlaku:
- PRD harus complete — tidak boleh ada discovery di tengah eksekusi
- Tidak ada back-and-forth selama eksekusi
- Kalau ada ambiguitas, PRD harus diperbaiki dulu sebelum Antigravity mulai
- Antigravity tidak boleh membuat keputusan arsitektur yang tidak ada di PRD

<!-- AIRO:DEVICE_MODES:BEGIN -->
### Owner Work Schedule and Device Operating Modes

#### Canonical Work Schedule

* Owner timezone: `Asia/Jakarta` (`WIB`, UTC+7).
* Regular workdays: Monday through Saturday.
* Regular work hours: `08:00-17:00 WIB`.
* Sunday is a non-workday.
* Indonesian national public holidays are non-workdays.
* When national-holiday status affects execution-context inference, verify the current Indonesian national-holiday calendar from an authoritative/current source; do not rely on stale model memory.

#### Context-Inference Precedence

1. An explicit Owner statement about the current device or location always overrides schedule-based inference.
2. During a regular workday at `08:00-17:00 WIB`, default to `WORK_BROWSER` when the Owner has not stated another device/context.
3. Outside regular work hours, on Sunday, or on an Indonesian national public holiday, default to `MAIN_PC` unless the Owner states otherwise.
4. Schedule-derived context is an operating default, not proof of physical device state.
5. Never use inferred device context as evidence for runtime, credential, process, deployment, or filesystem state.

#### `WORK_BROWSER` — Work Laptop

* Browser-only operating context by default.
* Local terminal and WSL execution are unavailable.
* Local AIRO workspace/runtime access must not be assumed.
* ChatGPT usage on the work laptop may be shared/non-private; keep this context non-secret and public-safe.
* Do not expose credentials, tokens, private `.env` data, raw sensitive financial data, or other production secrets in this context.
* Assume a full free-tier workflow; do not require paid tooling or subscriptions unless the Owner explicitly changes this constraint.
* Appropriate work: ASB/GitHub reading, research, planning, architecture, source review, requirements reconciliation, test-design review, candidate specification, and preparation of complete `MAIN_PC` execution packets.
* Do not provide local WSL/runtime commands as immediately executable work unless the Owner explicitly says a compatible execution environment is available.
* When a task requires runtime execution, complete as much deterministic analysis/design as possible and prepare a bounded `MAIN_PC` execution packet rather than blocking productive work.

#### `MAIN_PC` — Primary Execution Environment

* Local workspace and WSL execution are available when the Owner confirms or context inference selects `MAIN_PC`.
* This is the primary environment for local AIRO implementation, test execution, Git CLI operations, runtime/service inspection, deployment preparation, and production evidence collection.
* Production/runtime state must still be verified directly; `MAIN_PC` context never substitutes for runtime evidence.
* Continue the same canonical ASB project/session state rather than reconstructing continuity from chat memory.

#### Cross-Device Continuity

* AIRO Second Brain (ASB) is the durable cross-device source of continuity.
* Chat/model memory is not required for project continuity and must not override canonical ASB or live evidence.
* `WORK_BROWSER` should optimize for research, review, design, and complete execution preparation.
* `MAIN_PC` should optimize for bounded execution, verification, deployment, and evidence capture.
* Device changes do not create a new project objective by themselves; preserve the active project/session when the objective is unchanged.

#### Fast-track Rule

Fast track means fewer controlled cycles, not skipped evidence: one complete audit, one mapping decision, one approved implementation package, one regression cycle, one release update. Never modify the frozen baseline directly.
<!-- AIRO:DEVICE_MODES:END -->

<!-- AIRO_SYNC_OPERATING_STYLE_START -->
## Owner Execution Preferences — AIRO Sync

- **Roadmap Snapshots first**: Start every substantive AIRO response with a compact roadmap snapshot.
- **Explain Before Execution**: When providing a command or prompt, always explain the goal, expected output, mutation scope, and stop conditions first.
- **One Bounded Direct-WSL Packet per Turn**: When Owner chooses direct WSL, prefer one copy-paste-ready packet containing as many already-determined safe sub-steps as practical. Optimize for the fewest safe Owner interaction cycles, not one technical sub-step per turn.
- **Split at Real Boundaries Only**: Split for new Owner approval, unresolved identity/ambiguity, owner-work conflict, remote-runtime authorization, remote divergence, or required Owner visual/live acceptance.
- **Antigravity Low-Limit Is Separate**: Antigravity one-small-gate behavior MUST NOT be generalized into artificial direct-WSL micro-gates.
- **Antigravity Prompts**: When the Owner requests an Antigravity prompt, format it as a comprehensive, no-brainer instructions package with exact context, specific allowed/forbidden files, validation log paths, and automatic clipboard copy commands.
- **No Information Overload**: Do not overwhelm the Owner with unnecessary directory listings, raw transcript dumps, or excessively long logs. Keep output clean and focused.
- **No Manual Path Editing**: Do not ask the Owner to manually adjust file paths or scripts. All provided commands and scripts must be copy-paste ready.
- **Evidence-driven Completion**: Never assume completion or claim `PASS`/`DONE` without verifiable evidence.
- **WSL Session Protection**: Never close or exit the active WSL environment, and never execute logout, shutdown, or wsl --shutdown.
<!-- AIRO_SYNC_OPERATING_STYLE_END -->

<!-- SOURCE_END identity/working-principles.md -->

<!-- SOURCE_BEGIN identity/goals.md -->

# Source: identity/goals.md

# Goals — Egit & Ekosistem AIRO

## Visi Besar

Membangun **AIRO sebagai personal AI operating system** yang lengkap — di mana semua aspek kehidupan dan bisnis Egit bisa dikelola, diotomatisasi, dan dimudahkan melalui AI agents yang terintegrasi, dengan Telegram sebagai primary interface.

Bukan sekadar kumpulan tools. AIRO adalah ekosistem yang "mengenal" Egit secara mendalam dan bisa bertindak atas namanya dengan level otonomi yang terus meningkat seiring matangnya sistem.

---

## Goals Aktif (Horizon Dekat)

### Earesmes
- Resolve outstanding unknowns (provider aktif, skills terdaftar, SOUL.md persistence) via WSL audit
- Finalisasi PRD Google Workspace integration dan handoff ke Antigravity
- Graduate dari Opsi 3 (aware of workers) ke orchestrator aktif saat Arfin, Remin, Bubu siap

### AIRO Finance (Arfin)
- Finalisasi PRD v2.1.3 dan handoff ke Antigravity untuk full execution
- Selesaikan gap: Review Queue columns, Finance Events columns, tab visibility, backup tab cleanup
- Update `AIRO_FINANCE_CURRENT_STATE.md` ke deployment state yang akurat

### Second Brain (Repo Ini)
- Establish sebagai default knowledge base untuk semua AI consumer
- Maintain dan update setiap ada perubahan signifikan di sistem

---

## Goals Jangka Menengah

- Arfin, Remin, dan Bubu mature → Earesmes bisa jadi active orchestrator
- Earesmes bisa jalankan multi-step tasks secara otonomi dengan human review di checkpoint penting
- Ekosistem AIRO bisa berjalan mandiri untuk routine tasks saat Egit tidur

---

## Goals Jangka Panjang

- AIRO sebagai competitive advantage pribadi — semua knowledge dan workflow ter-encode di sistem
- Integrasi Notion (di-defer sampai siap)
- Potensi: AIRO sebagai framework yang bisa di-share atau diajarkan ke orang lain

<!-- SOURCE_END identity/goals.md -->

<!-- SOURCE_BEGIN docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md -->

# Source: docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md

# 🏛️ Architecture Decision Record: AIRO Hybrid Multi-Device Access Model

**ADR ID:** `ADR-AIRO-MULTI-DEVICE-ACCESS-V1`  
**Task ID:** `AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1`  
**Date:** 2026-09-05  
**Status:** `ACCEPTED` (Council Deep Deliberation & Owner-Confirmed)  
**Governance Authority:** Owner-Confirmed (ASB Architecture & Governance Restored)  
**Canonical File:** `docs/architecture/AIRO_MULTI_DEVICE_ACCESS_ARCHITECTURE_DECISION_RECORD_V1.md`  
**Parent Contracts:**  
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`  
- `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`  
- `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`  
- `docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md`  

---

## 1. Problem Statement & Context

The AIRO operational ecosystem has evolved beyond a single physical machine. Operational tasks, planning, automation, and continuous background processing now span multiple execution surfaces:
- **Primary Workstation (PC / WSL)**: Interactive engineering, coding, local tool orchestration, and large-scale model automation.
- **Mobile Workstation (Laptop)**: Field work, off-site monitoring, and mobile terminal access.
- **Cloud Infrastructure (Tencent VPS)**: Headless background daemons, persistent listener queues, and private sidecar storage.
- **AI Execution Agents (Antigravity Executor / Claude / ChatGPT)**: Autonomous coding agents executing bounded batches in isolated workspace scratch environments.

### The Multi-Device Risks:
Without a rigorous canonical architectural decision, operating across multiple devices creates critical operational risks:
1. **Divergent Runtime States**: Multiple nodes generating unsynchronized `active_session.json` files in independent `~/.local/state` trees.
2. **Ghost & Stale Sessions**: Sessions closed on one machine leaving frozen active cards on another machine's presentation surface (as observed in the recent WorkDesk current-work stale card incident).
3. **Fragmented Ownership**: Disputed authority over which machine represents "the real AIRO".
4. **Continuity Corruption**: Worklogs and milestone advancements recorded out of chronological sequence, breaking Obsidian WorkDesk and historical provenance.

---

## 2. Architecture Decision: The Hybrid Multi-Device Model

Council Deep deliberation has formally resolved that **AIRO operates as a Hybrid Multi-Device Architecture**.

The system strictly enforces a structural separation between **Identity & Control** and **Execution**:

```text
┌──────────────────────────────────────────────────────────────────┐
│                   CONTROL & IDENTITY PLANE                       │
│  - Authority: AIRO Second Brain Canonical Repository + Owner     │
│  - Enforces: Contracts, Policies, WorkDesk Governance, Approvals │
│  - Ground Truth: ONE SINGLE CANONICAL BRAIN (Git + Vault)        │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ Directs / Governs
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                       EXECUTION PLANE                            │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌─────────┐  │
│  │   PC WSL   │   │ Laptop WSL │   │ Tencent VPS│   │   AGY   │  │
│  │ Node (Local│   │ Node (Field│   │ Node (Cloud│   │ Executor│  │
