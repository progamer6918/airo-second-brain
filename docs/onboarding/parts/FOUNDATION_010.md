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

<!-- SOURCE_END docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/operations/AIRO_SESSION_WORKLOG_PROMOTION_SOP.md -->

# Source: docs/operations/AIRO_SESSION_WORKLOG_PROMOTION_SOP.md

---
type: standard_operating_procedure
project: GLOBAL
status: CANONICAL
authority: OWNER_APPROVED
date: 2026-09-05
audience: all_airo_operators
---

# 📜 AIRO Session Worklog Promotion SOP

**Document ID:** `AIRO_SOP_SESSION_PROMOTION_V1`  
**Effective Date:** 2026-09-05  
**Canonical Path:** `docs/operations/AIRO_SESSION_WORKLOG_PROMOTION_SOP.md`  
**Governing Contracts:**  
- `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`
- `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`
- `docs/contracts/WORKDESK_HOME_OPERATING_SURFACE_CONTRACT.md`
- `docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`

---

## 1. Purpose

### 1.1 Background: Why Session Artifacts Exist Outside Canonical ASB
In the AIRO ecosystem, automated agents (such as Antigravity and automated WSL scripts) execute tasks inside isolated sandbox or scratch workspaces (e.g., `C:\Users\Admin\.gemini\antigravity\scratch\airo-second-brain` or temporary runtime subshells). This containment boundary prevents experimental trials, unverified script outputs, and incomplete mutations from contaminating the production repository.

When an execution session completes via `bin/airo-session close`, it intentionally writes the permanent session note only to the **local filesystem** of the current execution workspace (`repo_root/worklog/sessions/...`). It deliberately does not perform automated git staging, commit, or remote push.

### 1.2 Why Promotion is Required
Session artifacts left exclusively in scratch workspaces become orphaned from the canonical source of truth. Consequently, human operating cockpits—most notably Obsidian—cannot discover, display, or link these execution records.

**Session Promotion** is the formal, deterministic procedure that bridges verified execution records from the scratch execution workspace into the canonical AIRO Second Brain repository.

### 1.3 Architectural Relationship
The system operates across three distinct operational layers:

```text
┌────────────────────────────────────────────────────────┐
│             Execution Workspace (Scratch)              │
│  - Sandbox environment (Antigravity / WSL Runtime)     │
│  - Local testbench & temporary session write target    │
└──────────────────────────┬─────────────────────────────┘
                           │ 1. Verify & Promote Artifacts
                           ▼
┌────────────────────────────────────────────────────────┐
│             Canonical ASB Repository (Git)             │
│  - Canonical Git Source of Truth (origin/main)         │
│  - Controlled mutations, exact-path staging & history   │
└──────────────────────────┬─────────────────────────────┘
                           │ 2. Filesystem / Git Sync
                           ▼
┌────────────────────────────────────────────────────────┐
│              Obsidian Cockpit (Vault Surface)          │
│  - Human-friendly operational viewing & review surface  │
│  - Queries canonical worklog/sessions & daily notes    │
└────────────────────────────────────────────────────────┘
```

---

## 2. Standard Promotion Workflow

Following the close of any meaningful execution session, operators must follow this five-step workflow:

```text
[bin/airo-session close]
       ↓
[Step 1: AIRO Creates Session Artifact]
       ↓
[Step 2: Owner Reviews Session Permanence]
       ↓
[Step 3: Promote Approved Artifact to Canonical ASB]
       ↓
[Step 4: Verify Presence, Checksum & Git Index]
       ↓
[Step 5: Exact-Path Commit & Owner-Approved Push]
```

### Step 1: AIRO Creates Session Artifact
- **Action**: The executor executes `bin/airo-session close` with required parameters and verified evidence.
- **Location**: The engine writes a standardized 10-section Markdown note at:
  ```text
  worklog/sessions/YYYY-MM-DD/<Project_Name>/<NN> - <Session_Title>.md
  ```
  and automatically executes `scripts/airo-daily <YYYY-MM-DD>` to generate or update `worklog/daily/YYYY-MM-DD.md`.
- **Precondition**: The task verdict computed by `scripts/airo-task-verdict` must evaluate to `BERHASIL` or `BERHASIL_DENGAN_BATASAN`.

### Step 2: Owner Reviews Session Permanence
- **Action**: The Owner (or ChatGPT Intelligence Layer representing Owner policy) reviews whether the closed session contains durable project facts, decisions, or verified evidence.
- **Decision Gate**:
  - `PERMANENT_RECORD` → Proceed to Step 3 for promotion.
  - `TRANSIENT_SCRATCH` → Retain in scratch workspace without canonical promotion.

### Step 3: Promote Approved Artifact to Canonical ASB
- **Action**: Copy the verified session artifact(s) and updated daily note from the scratch workspace to the canonical ASB directory (`C:\Users\Admin\AI_WORKSPACES\airo-second-brain`).
- **Rules**:
  - Automatically create missing project subdirectories if they do not yet exist in the canonical path.
  - Retain original filenames, markdown frontmatter, and timestamps.
  - Do not delete original files in scratch.

### Step 4: Verification (Three-Point Parity Check)
Before staging or committing, execute the following three verifications:
1. **File Presence**: Confirm all target files exist at the canonical destination path.
2. **Content Integrity (SHA256 Match)**: Compute SHA256 checksums of source and destination files. Promotion is invalid unless:
   $$\text{Hash}_{\text{scratch}} \equiv \text{Hash}_{\text{canonical}}$$
3. **Git Index Isolation**: Run `git status` / `git diff --cached --name-only`. Verify that **only** the intended recovered markdown files are staged in the git index. Any untracked or modified files outside the approved list must remain completely unstaged.

### Step 5: Commit & Push via Explicit Owner-Approved Action
- **Action**:
  1. Stage exact files:
     ```bash
     git add "worklog/sessions/YYYY-MM-DD/<Project>/<File>.md" "worklog/daily/YYYY-MM-DD.md"
     ```
  2. Commit using the canonical message format:
     ```bash
     git commit -m "feat(worklog): promote verified session artifacts YYYY-MM-DD"
     ```
  3. Push to remote origin:
     ```bash
     git push origin main
     ```
- **Constraint**: Under Rule 14 of `AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`, `git push` is never implied. Remote pushes must be explicitly commanded by an Owner-approved execution packet or Telegram action callback.

---

## 3. Workspace Boundary & Role Definitions

| Operational Layer | Physical Path / Environment | Primary Function | Mutation Policy |
|---|---|---|---|
| **Execution Workspace** | `C:\Users\Admin\.gemini\antigravity\scratch\airo-second-brain`<br>*(WSL: `/mnt/c/.../scratch/...`)* | Scratch execution, terminal automation, build tests, raw script execution. | Highly mutable; local scratch writes allowed; automated remote push strictly prohibited. |
| **Canonical ASB** | `C:\Users\Admin\AI_WORKSPACES\airo-second-brain`<br>*(Git: `origin/main`)* | Canonical source of truth, persistent system memory, project governance. | Strictly controlled; exact-path commits only; requires Owner or explicit packet authority. |
| **Obsidian Surface** | `C:\Users\Admin\AI_WORKSPACES\airo-second-brain` | Human-facing operational cockpit, wikilinks, Base views (`AIRO Worklog.base`). | Read/viewing interface; reflects Canonical ASB filesystem state. |

---

## 4. Promotion Rules & Filtering Criteria

### 4.1 Artifacts to PROMOTE (`PROMOTE=YES`)
1. **Meaningful Project Progress**: Verifiable progress against active milestones, roadmap objectives, or deliverables.
2. **Architecture & Governance Decisions**: Changes recorded in decision logs, contract ratifications, or PRD updates.
