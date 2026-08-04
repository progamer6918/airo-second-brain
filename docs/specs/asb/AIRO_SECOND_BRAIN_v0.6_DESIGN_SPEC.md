# AIRO Second Brain v0.6 Architecture & Design Specification

- **Status:** `OWNER_APPROVED_DESIGN_SPECIFICATION`
- **Owner:** Egit Aristo Randas
- **Approved Date:** 2026-08-04
- **Scope:** `ASB_GLOBAL`
- **Canonical PRD:** [AIRO Second Brain PRD v0.6.0](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md)
- **Roadmap:** [AIRO Second Brain v0.6 Roadmap](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md)
- **Approved Decision Record:** [Owner Architecture Approval 2026-08-04](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/decisions/approved/asb-v06-architecture-owner-approval-20260804.md)

---

## 1. Problem Statement & Real Use-Case Pain

### 1.1 The Reconstruction-Cost Problem
Previously, when the Owner or an AI consumer needed to resume work or verify status across sessions, information had to be laboriously reconstructed by searching across raw chat transcripts, terminal outputs, scattered git commits, status files, and old logs. This resulted in high context recovery overhead and lost momentum.

### 1.2 The False-PASS Problem
In past workflows (e.g. EAB / AIRO Finance tasks), a shell command returning exit code 0 (`RC=0`) was often falsely interpreted as task or milestone completion (`PASS`), even when the command only executed a simulation or dry-run. As a result, projects appeared to advance on paper, only to move backward later when live runtime failures occurred.

---

## 2. Core Design Principles

1. **ASB Scope:** This upgrade belongs to `ASB_GLOBAL` (`AIRO Second Brain v0.6`). It is NOT a separate "Obsidian project".
2. **Execution Assurance Invariant:** Shell execution success (`EXIT_CODE=0` / `SCRIPT_SUCCESS`) does NOT mean task completion (`BERHASIL`) or advancement permission (`CAN_ADVANCE=YES`).
3. **Baby-Friendly Human UX:** All human-facing UI, session notes, and status receipts use clean, simple Indonesian terminology without exposing technical enums, UUIDs, or raw logs.
4. **No Ad-Hoc Roadmap Gates:** Unapproved intermediate gates (e.g. M2.1A, Shadow Gate) are forbidden. Blockers produce a bounded diagnosis and an exact next action.
5. **Bounded Blocker Budget:** Blockers trigger 1 bounded diagnosis + 1 optional confirmation. If still unresolved, execution stops and records the blocker without infinite exploratory loops.
6. **Single Repository Cockpit:** Obsidian opens the existing `airo-second-brain` repository directly. No duplicate vaults are created.

---

## 3. Target Architecture Diagram

```text
CANONICAL PROJECT STATE
PRD / ROADMAP / DoD
          |
          v
EXECUTION ASSURANCE
"What must be proven?"
          |
          v
EXECUTION
          |
          v
VERIFIED EVIDENCE
          |
          v
AIRO STATUS RECEIPT
          |
   +------+-------+
   |      |       |
   v      v       v
 CHAT   SESSION  TRACKER
          |
          v
        DAILY
          |
          v
     OBSIDIAN HOME
          |
          v
 worth remembering?
          |
          v
       LLM WIKI
```

---

## 4. Human-Facing Status Receipt (`🧭 AIRO STATUS`)

All human-facing session status outputs and checkpoint receipts use the standard `🧭 AIRO STATUS` header and baby-friendly Indonesian fields:

```text
🧭 AIRO STATUS

📍 Project — <Nama Proyek>
📌 Lagi di — <Posisi Kanonis / Milestone>
📈 Progress — <Kemajuan berbasis bukti>

🧪 Bukti
Yang wajib ada — <Bukti yang disyaratkan>
Yang sudah ada — <Bukti aktual yang terkumpul>
Kesimpulan — BERHASIL | BERHASIL_DENGAN_BATASAN | BELUM_TERBUKTI | TERHAMBAT | GAGAL
Boleh lanjut — YA | TIDAK

⛔ Hambatan — <Hambatan eksplisit atau "Tidak ada">
➡️ Berikutnya — <Satu langkah konkret kanonis>
🏁 Selesai kalau — <Definisi Selesai / DoD>
```

### Human Wording Mapping
- `TASK_VERDICT` -> Kesimpulan
- `REQUIRED_PROOF` -> Bukti yang wajib ada
- `ACTUAL_PROOF` -> Bukti yang sudah ada
- `CAN_ADVANCE` -> Boleh lanjut?
- `REHEARSAL` -> Uji coba / simulasi
- `LIVE_RUNTIME` -> Bukti dari sistem nyata
- `NOT_YET_PROVEN` -> Belum terbukti selesai

---

## 5. Execution Assurance & Deterministic Validation

### 5.1 Deterministic Rules
`scripts/airo-task-verdict` computes task status deterministically using these fail-closed rules:
- `script_status != SCRIPT_SUCCESS` => `GAGAL` / `CAN_ADVANCE=NO`
- `blockers` non-empty => `TERHAMBAT` / `CAN_ADVANCE=NO`
- `required_evidence` missing or unsatisfied => `BELUM_TERBUKTI` / `CAN_ADVANCE=NO`
- `actual_evidence` satisfied with `limitations` => `BERHASIL_DENGAN_BATASAN` / `CAN_ADVANCE=NO`
- `required_evidence` satisfied, no blockers, no limitations => `BERHASIL` / `CAN_ADVANCE=YES`
- Unknown / conflicting evidence => `BELUM_TERBUKTI` / `CAN_ADVANCE=NO`

---

## 6. Worklog Session Lifecycle & Per-Run Append Flow

### 6.1 Human Session Definition
- **1 Session = 1 Project + 1 Main Objective.**
- The ChatGPT conversation is NOT the session boundary. One chat may contain multiple sessions if projects or objectives change.
- Same project + same objective = continue updating the SAME active session draft.
- Switch project or new objective = close current session and start a new session.

### 6.2 Session Filename & Folder UX (Target M2 Scope)
- Path pattern: `worklog/sessions/YYYY-MM-DD/<Project>/<Number> - <Objective>.md`
- Example: `worklog/sessions/2026-08-04/ASB/01 - Upgrade Workflow ASB.md`
- Raw UUIDs are forbidden in human filenames.

### 6.3 Per-Run Append vs Closeout Push
- During an active session, Antigravity appends safe checkpoints to the active session draft locally.
- Project work pushes and session closeout pushes are conceptually separate.
- Closeout push occurs only at explicit session close after final sanitization, secret scanning, and evidence verification.

---

## 7. Multi-Layer Memory Architecture

| Layer | Primary Role | Storage Location / Interface |
|---|---|---|
| **Raw Events** | Machine telemetry & event ledger | `events/raw/events.ndjson` |
| **Session** | Episodic work memory ("what happened in this segment?") | `worklog/sessions/` (M2) |
| **Daily** | Generated human navigation view ("what happened today?") | `worklog/daily/` (M2) |
| **Canonical Project Docs** | Current project truth ("where is the project now?") | `projects/`, `docs/`, `CURRENT.md` |
| **Decisions** | Durable Owner decision records | `decisions/approved/` |
| **LLM Wiki** | Reusable semantic knowledge & lessons learned | `wiki/` |

---

## 8. Multi-Project Real Use-Case Walkthrough

```text
09:00 - 11:30: EAB session (Objective: Canary Fix) -> Session 01
13:00 - 15:00: AIRO Finance session (Objective: Email Parsing) -> Session 01
19:00 - 22:00: ASB_GLOBAL session (Objective: v0.6 Upgrade) -> Session 01

Daily Navigation View (4 August 2026):
  EAB: Session 01 (Canary Fix) — BERHASIL (CAN_ADVANCE=YES)
  AIRO Finance: Session 01 (Email Parsing) — BERHASIL_DENGAN_BATASAN
  ASB: Session 01 (v0.6 Upgrade) — BERHASIL (CAN_ADVANCE=YES)
```

---

## 9. Selective Upstream Adoption Decisions

1. **`Ar9av/obsidian-wiki`**: Selected as primary upstream for LLM Wiki capabilities, capture/query patterns, and metadata/Bases filtering.
2. **`kepano/obsidian-skills`**: Selected for Obsidian-native authoring, Bases, Canvas, and CLI skills.
3. **`eugeniughelbur/obsidian-second-brain`**: Selected as UX/workflow pattern donor for worklog, daily recap, and project views.
4. **`Everything OpenAI Codex`**: Selected as execution-pattern donor (Intake -> Route -> Plan -> Execute -> Verify -> Capture -> Resume).

*Strategy: Selective adoption only. No wholesale replacement of ASB governance.*

---

## 10. System Component Roles & Status

- **`airo-capture`**: KEEP / REUSE concept and NDJSON ledger. Will be integrated into session lifecycle in M2.
- **Runtime Sync (`ops/runtime/airo-runtime-runner.sh`)**: KEEP DISABLED until automatic rebase is replaced with safe conflict-free sync.
- **Finance Legacy Timer (`airo-full-auto-sheets-sync.timer`)**: Recorded as `RETIRE_CANDIDATE` for AIRO Finance. Do not mutate in M1.
- **Earesmes Telegram Gateway**: Active running background process (`telegram-gateway.py`). E2E health remains `NOT_YET_PROVEN` until live test.

---

## 11. Before vs After Summary

| Dimension | BEFORE (v0.5.1) | AFTER (v0.6.0) |
|---|---|---|
| **Execution Truth** | `RC=0` / Script success often mistranslated as Milestone PASS | Script success != Task PASS; `airo-task-verdict` requires verified evidence |
| **Context Recovery** | Search across raw chats, terminal logs, git history | Instantly navigable via `🧭 AIRO STATUS`, Session worklogs, and Daily view |
| **Human UX** | Exposed technical enums, raw UUIDs, and dry logs | Simple, baby-friendly Indonesian status receipts and Obsidian cockpit |
| **Memory Loop** | Passive LLM Wiki with incomplete daily integration | Multi-layer memory architecture (Raw -> Session -> Daily -> Canonical -> Wiki) |

---

## 12. Known Limitations & Out of Scope for M1

- **Out of Scope for M1:** `worklog/sessions/` directory creation, `HOME.md` cockpit UI build, LLM Wiki capture automation, Runtime Sync repair, Finance timer retirement. These belong to M2..M6.
