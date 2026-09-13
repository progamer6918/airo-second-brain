---
type: contract
project: GLOBAL
status: CANONICAL
authority: OWNER_APPROVED
date: 2026-09-05
audience: all_airo_operators
---

# 📜 AIRO Session Projection Synchronization Contract

**Contract ID:** `AIRO_CONTRACT_SESSION_PROJECTION_SYNC_V1`  
**Effective Date:** 2026-09-05  
**Canonical Path:** `docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md`  
**Parent Contracts:**  
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`  
- `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`  
- `docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md`  
- `docs/contracts/ASB_HUMAN_NAVIGATION_CONTRACT.md`  

---

## 1. Purpose & Core Principles

### 1.1 Architectural Rationale
In the AIRO Second Brain (ASB) ecosystem, session execution operates across two distinct planes:
1. **The Runtime Execution Plane (`Runtime State`)**: Headless, low-latency, machine-parsable JSON state managed by `bin/airo-session` inside user-space runtime storage (`~/.local/state/airo/second-brain/<repo_hash>/active_session.json`).
2. **The Human Operational Surface (`Obsidian Projection`)**: Visual, human-friendly Markdown notes embedded within Obsidian cockpits:
   - `state/active-session.md`: Card-formatted session view for project/PRD linkages.
   - `runtime/workdesk/current-work.md`: Table-formatted operational current-work surface transcluded by `HOME.md` (`### ▶️ Lanjut Kerja`) and `wiki/workdesk/WORKDESK.md`.

### 1.2 Core Invariant
> [!IMPORTANT]
> **Projection notes (`state/active-session.md` and `runtime/workdesk/current-work.md`) are DERIVED OPERATIONAL VIEWS, NEVER THE SOURCE OF TRUTH.**  
> Under no circumstances may an agent, script, or operator treat projection files as authoritative session state. Live session truth is defined solely by the active runtime execution engine (`bin/airo-session`).

---

## 2. Source of Truth Hierarchy

When resolving active session identity, status, or lifecycle stage, all AIRO consumers and executors MUST obey the following strict priority:

```text
┌────────────────────────────────────────────────────────┐
│               1. PRIMARY: Runtime State                │
│  - ~/.local/state/airo/second-brain/.../active_session │
│  - Queried via: python3 bin/airo-session status        │
│  - Authority: ABSOLUTE LIVE TRUTH                      │
└──────────────────────────┬─────────────────────────────┘
                           │ Projects to
                           ▼
┌────────────────────────────────────────────────────────┐
│            2. SECONDARY: Markdown Projection           │
│  - Surface A: state/active-session.md                  │
│  - Surface B: runtime/workdesk/current-work.md         │
│  - Authority: DERIVED READ-ONLY MIRRORS                │
│  - Stale when desynchronized from Primary              │
└──────────────────────────┬─────────────────────────────┘
                           │ Transcludes into
                           ▼
┌────────────────────────────────────────────────────────┐
│            3. VIEWER: Obsidian WorkDesk Cockpit        │
│  - Human surface: HOME.md, wiki/workdesk/WORKDESK.md   │
│  - Authority: PRESENTATION LAYER ONLY                  │
└────────────────────────────────────────────────────────┘
```

1. **Primary (Runtime Session State)**:
   - File: `~/.local/state/airo/second-brain/<repo_hash>/active_session.json`
   - Authority: Absolute runtime truth. Contains active UUID, project ID, title, position, start timestamp, and raw ledger events.
2. **Secondary (Projection Notes)**:
   - Surface A: `state/active-session.md` (Rich card format).
   - Surface B: `runtime/workdesk/current-work.md` (Operational table format transcluded by `HOME.md` and `WORKDESK.md`).
   - Authority: Derived representation formatted for Obsidian readability. Atomically updated by `scripts/airo-session-projection-sync`.
3. **Viewer (Obsidian Cockpit)**:
   - Interface: Desktop / Mobile Obsidian rendering `HOME.md`.
   - Authority: Display only. Never dictates system state.

---

## 3. Lifecycle Synchronization Rules

### 3.1 Session Start (`bin/airo-session start`)
- **Runtime Transition**: Generates new session UUID, writes `active_session.json`, and records `started_at` timestamp.
- **Required Projection Action**:
  - The projection file `state/active-session.md` MUST transition from idle state to the active session card format:
    ```markdown
    ### 🟢 <Project_Name>

    **Lagi di**
    <Position_Description>

    **Yang Saya Minta**
    <Objective_Or_Request>

    **Progress Terakhir**
    <Current_Progress_Summary>

    **Hambatan**
    <Blockers_Or_None>

    **Berikutnya**
    <Next_Action>

    → [[<PRD_Or_Project_Link>|Buka Project / PRD]]
    ```
- **Atomicity**: If runtime session starts successfully, projection MUST reflect the active card.

### 3.2 Session Events (`bin/airo-session event`)
- **Runtime Transition**: Appends event to `events` array in `active_session.json` and records to `events/raw/events.ndjson`.
- **Projection Action**:
  - Intermediate checkpoints SHOULD update `**Lagi di**` and `**Progress Terakhir**` if the event represents a major milestone or state change.
  - Minor terminal commands or transient diagnostics MUST NOT trigger file-write churn in `state/active-session.md`.

### 3.3 Session Close (`bin/airo-session close`)
- **Runtime Transition**:
  - Evaluates required evidence via `scripts/airo-task-verdict`.
  - Writes permanent note to `worklog/sessions/YYYY-MM-DD/<Project>/`.
  - Generates/updates `worklog/daily/YYYY-MM-DD.md`.
  - Unlinks `active_session.json` (`ACTIVE_SESSION=NONE`).
- **Required Projection Action**:
  - `state/active-session.md` MUST immediately reset to the canonical idle card:
    ```markdown
    # ⚪ Tidak Ada Sesi Aktif

    Belum ada pekerjaan aktif yang perlu dilanjutkan.
    ```
- **Prohibition**: An unlinked or closed runtime session MUST NEVER leave an active `🟢` card in `state/active-session.md`.

---

## 4. Failure States & Automated Resolution

| Failure Scenario | Manifestation | Root Cause | Deterministic Resolution |
|---|---|---|---|
| **State 1: Runtime Active, Projection Missing/Idle** | `bin/airo-session status` shows active session, but `state/active-session.md` displays `⚪ Tidak Ada Sesi Aktif` or is empty. | Projection writer was bypassed during headless or script execution. | Re-project active session card from `active_session.json` into `state/active-session.md` without restarting session. |
| **State 2: Runtime Closed, Projection Stale (Frozen Green Card)** | `bin/airo-session status` shows `ACTIVE_SESSION=NONE`, but `state/active-session.md` displays a stale `🟢 <Project>` card. | Session was closed via legacy CLI, process kill, or decoupling defect. | Force-reset `state/active-session.md` immediately to canonical idle state (`# ⚪ Tidak Ada Sesi Aktif`). |
| **State 3: Multi-Workspace / Conflicting Sessions** | Different repositories or clones have divergent `active_session.json` files. | Simultaneous execution across scratch and canonical directories. | Obey Source Priority per `AGENTS.md`. Execution workspace (`scratch`) holds execution authority; canonical holds storage authority. Reconcile to single active session; close stale orphans. |

---

## 5. Ownership & Boundary Separation

Under the [`AIRO Agent Role Contract`](docs/governance/AIRO_AGENT_ROLE_CONTRACT.md), role boundaries during projection synchronization are strictly enforced:

1. **ChatGPT (Intelligence & Planning Layer)**:
   - Evaluates session state.
   - Diagnoses projection mismatches.
   - Generates bounded remediation instructions.
   - Does NOT directly mutate local files.
2. **Antigravity (Executor-Only Layer)**:
   - Executes synchronization instructions and terminal scripts.
   - Verifies file contents and hash parity.
   - Enforces exact-path changes.
   - Returns standardized `🧭 AIRO STATUS` receipts.
3. **Owner (Governance Authority)**:
   - Approves architectural changes.
   - Authorizes Git commits and pushes.

---

## 6. Git Synchronization Policy

1. **Runtime Operational Classification**:
   - Updates to `state/active-session.md` represent transient runtime operational states.
   - Intermediate transitions (`🟢 Active` ↔ `⚪ Idle`) during normal working sessions SHOULD NOT generate standalone git commits unless part of a structured session closeout or checkpoint commit.
2. **No Automatic Push Implied**:
   - Per Rule 14 of `AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`, `git push` is never implied.
   - Resetting or updating `state/active-session.md` locally in the Obsidian vault does NOT require immediate remote git push.
3. **Controlled Promotion**:
   - When session worklogs and state checkpoints are promoted, they must be staged via exact paths and pushed only with explicit Owner authority.

---

## 7. Validation & Verification Requirements

Any procedure claiming projection synchronization MUST satisfy the following four validation checks:

1. **Runtime Parity Check**:
   ```bash
   python3 bin/airo-session status
   ```
   Must match the intended state (`ACTIVE_SESSION=NONE` for idle, or active project details).
2. **Projection Content Check**:
   Inspect `state/active-session.md`. Confirm exact text match with either the active card template or the canonical idle template.
3. **Stale Session Detection**:
   Assert that no orphaned links to closed sessions exist in `state/active-session.md`.
4. **Verified Receipt Delivery**:
   Every synchronization or repair action MUST conclude with a verified clipboard receipt generated by `scripts/airo-clipboard-receipt`:
   ```text
   COPIED_TO_CLIPBOARD=YES
   CLIPBOARD_READBACK=PASS
   CLIPBOARD_CONTENT_HASH=PASS
   ```
