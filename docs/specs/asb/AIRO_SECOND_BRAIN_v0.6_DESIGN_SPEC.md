# AIRO Second Brain v0.6 Architecture & Design Specification

- **Status:** `OWNER_APPROVED_DESIGN_SPECIFICATION`
- **Owner:** Egit Aristo Randas
- **Approved Date:** 2026-08-04
- **Scope:** `ASB_GLOBAL`
- **Canonical PRD:** [AIRO Second Brain PRD v0.6.0](../prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md)
- **Roadmap:** [AIRO Second Brain v0.6 Roadmap](../roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md)
- **Approved Decision Record:** [Owner Architecture Approval 2026-08-04](../../decisions/approved/asb-v06-architecture-owner-approval-20260804.md)

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

## 4. Exact Real Per-Run Workflow

1. **ChatGPT Guarded Prompt**: Owner provides task request with explicit boundaries.
2. **Owner Copy**: Request copied to workspace/Antigravity.
3. **Antigravity Preflight**: Preflight inspection of repo status and environment.
4. **Execute**: Execution in bounded temporary environment or script.
5. **Full /tmp Log**: Output captured via `tee` to `/tmp/airo_<task>_<timestamp>.txt`.
6. **Validation**: Deterministic validation via `scripts/airo-task-verdict`.
7. **Project Commit**: Commit in git repository when authorized.
8. **Project Push**: Push to GitHub main when authorized.
9. **Verify Remote**: Remote parity check (`REMOTE_COMMIT_PARITY` and `REMOTE_TREE_PARITY`).
10. **Append Safe Checkpoint**: Safe checkpoint appended to the SAME active session draft.
11. **Record Safe Machine Event**: Telemetry event recorded to event ledger.
12. **Compact Result**: Final machine receipt generated.
13. **Clipboard Copy**: Log and summary copied to Windows clipboard (`clip.exe`).
14. **Owner Paste to ChatGPT**: Summary pasted back to ChatGPT with `🧭 AIRO STATUS`.

---

## 5. Human-Facing Status Receipt (`🧭 AIRO STATUS`)

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

---

## 6. Worklog Session Lifecycle & Per-Run Append Flow

### 6.1 Human Session Definition
- **1 Session = 1 Project + 1 Main Objective.**
- The ChatGPT conversation is NOT the session boundary. One chat may contain multiple sessions if projects or objectives change.
- Same project + same objective = continue updating the SAME active session draft.
- Switch project or new objective = close current session and start a new session.

### 6.2 Target Human Session Note Sections (10 Sections)
Every completed session note in Obsidian contains these 10 target sections:
1. `🧭 AIRO STATUS`
2. `🎯 Tujuan sesi`
3. `🛠 Yang dilakukan`
4. `📌 Hasil`
5. `🧪 Bukti`
6. `⛔ Masalah / hambatan`
7. `✅ Keputusan`
8. `📁 Yang berubah`
9. `📝 Yang belum selesai`
10. `➡️ Berikutnya`

### 6.3 Special Session Handling Rules
- **Failed / Blocked Sessions**: Must still be recorded truthfully in session history with exact blocker details.
- **Unknown Root Cause**: Must explicitly state `"Penyebab belum diketahui"` rather than guessing or swallowing exceptions.
- **Interrupted / Inactive Sessions**: Remain in draft/resumable state; never falsely mark as finalized or complete.

---

## 7. Multi-Layer Memory Architecture & Daily Generator

### 7.1 Memory Layers Table
| Layer | Primary Role | Storage Location / Interface |
|---|---|---|
| **Raw Events** | Machine telemetry & event ledger | `events/raw/events.ndjson` |
| **Session** | Episodic work memory ("what happened in this segment?") | `worklog/sessions/` (M2 target) |
| **Daily** | Generated human navigation view ("what happened today?") | `worklog/daily/` (M2 target) |
| **Canonical Project Docs** | Current project truth ("where is the project now?") | `projects/`, `docs/`, `CURRENT.md` |
| **Decisions** | Durable Owner decision records | `decisions/approved/` |
| **LLM Wiki** | Reusable semantic knowledge & lessons learned | `wiki/` |

### 7.2 Daily Navigation View Rules
- Generated automatically from recorded session files.
- Serves as a human navigation view only; it is NOT the current project source of truth.
- Completely regenerable from session notes.
- Avoid concurrent manual appends from multiple devices.

---

## 8. Multi-Device Design & Raw Chat Policy

### 8.1 Multi-Device Design Considerations
- Obsidian may synchronize working-copy notes through an approved vault sync layer.
- Git / GitHub remains the canonical version and audit layer.
- Never perform filesystem synchronization on the `.git` folder across devices.
- Avoid competing automatic Git and vault-sync writers.
- Note: Remotely Save plugin implementation is not declared active in M1.

### 8.2 Raw Chat Transcript Policy
- Raw downloaded chat transcripts are NEVER canonical repository documentation.
- Raw transcripts remain local-only evidence or reference material.
- Only distilled specs, approved decision records, and clean session summaries are committed to the canonical repository.

---

## 9. Selective Upstream Adoption Decisions & Research Appendix

### 9.1 Upstream Decisions
1. **`Ar9av/obsidian-wiki`**: Selected as primary upstream for LLM Wiki capabilities, capture/query patterns, and metadata/Bases filtering.
2. **`kepano/obsidian-skills`**: Selected for Obsidian-native authoring, Bases, Canvas, and CLI skills.
3. **`eugeniughelbur/obsidian-second-brain`**: Selected as UX/workflow pattern donor for worklog, daily recap, and project views.
4. **`Everything OpenAI Codex`**: Selected as execution-pattern donor (Intake -> Route -> Plan -> Execute -> Verify -> Capture -> Resume).

### 9.2 Deferred / Rejected Options
- **Whole Vault Replacement**: Deferred/Rejected. ASB governance and execution assurance must remain canonical.
- **Session Brain as Source of Truth**: Deferred/Rejected. Session Brain remains an optional local helper script, NOT the ASB source of truth.

---

## 10. Known Limitations & Out of Scope for M1

- Out of scope for M1: `worklog/sessions/` directory creation, `HOME.md` cockpit UI build, LLM Wiki capture automation, Runtime Sync repair, Finance timer retirement. These belong to M2..M6.
