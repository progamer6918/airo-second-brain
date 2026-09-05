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
3. **Completed Implementation Records**: Full execution sessions containing reproducible steps, validation proofs, and terminal receipts.
4. **Validated Investigation Results**: Root-cause diagnostic findings, architecture audits, security assessments, and environment verifications.

### 4.2 Artifacts to REJECT (`DO NOT PROMOTE`)
1. **Temporary Debugging**: Scratch scripts (`run_test.py`), intermediate log dumps, raw stdout tracebacks without a distilled closeout.
2. **Failed Experiments**: Abandoned proof-of-concepts or errored runs that produced no reusable system learning or architectural value.
3. **Secrets & Credentials**: Private tokens, OAuth credentials, bot tokens, API keys, passwords, private configuration files (`.env`, `credentials*.json`).
4. **Runtime Plumbing Artifacts**: Process PID files, IPC sockets, temporary lock files, OS cache (`.DS_Store`, `Thumbs.db`).

---

## 5. Responsibility Matrix

All AIRO ecosystem participants must adhere to their contractual role boundaries during promotion:

```text
┌────────────────────────────────────────────────────────┐
│                        ChatGPT                         │
│  - Evaluates session significance against PRD/Roadmap  │
│  - Plans bounded promotion execution packets           │
└──────────────────────────┬─────────────────────────────┘
                           │ Directs
                           ▼
┌────────────────────────────────────────────────────────┐
│                      Antigravity                       │
│  - Executes file copy & directory generation           │
│  - Computes & verifies SHA256 checksum parity          │
│  - Performs exact-path git staging & commits           │
│  - Delivers verified clipboard receipt (clip.exe)      │
└──────────────────────────┬─────────────────────────────┘
                           │ Requests Gate Approval
                           ▼
┌────────────────────────────────────────────────────────┐
│                         Owner                          │
│  - Exercises sole authority to approve canonical state │
│  - Authorizes remote git push to origin main           │
└────────────────────────────────────────────────────────┘
```

- **AIRO Session Engine (`bin/airo-session`)**: Generates deterministic, sanitized, 10-section session markdown notes and executes daily roll-up.
- **ChatGPT (Intelligence & Planning Layer)**: Identifies historical gaps, evaluates session importance, and generates detail-guarded execution packets.
- **Antigravity (Executor-Only Layer)**: Carries out terminal automation, performs file copy, checks checksum parity, enforces exact-path staging, and generates verifiable receipts.
- **Owner (Ultimate Governance Authority)**: Approves promotion packets and authorizes remote repository pushes.

---

## 6. Failure Handling & Recovery Protocols

### Failure Case 1: Artifact Exists Only in Scratch
- **Symptom**: Session was closed successfully, but is missing from the canonical vault and Obsidian.
- **Root Cause**: Session close was executed locally without a subsequent promotion packet.
- **Resolution**:
  1. Inspect `worklog/sessions/` in the scratch workspace to locate the note.
  2. Verify that `bin/airo-session status` indicates the session is closed.
  3. Execute an approved Historical Recovery Packet specifying source and target paths with SHA256 verification.

### Failure Case 2: Checksum Mismatch
- **Symptom**: Source SHA256 does not match canonical destination SHA256 after copy.
- **Root Cause**: Incomplete file write, transmission truncation, or line-ending conversion (`CRLF`/`LF` divergence).
- **Resolution**:
  1. Abort staging immediately (`DO NOT GIT ADD`).
  2. Perform clean binary copy (`shutil.copy2` or `cp -p`).
  3. Re-verify SHA256 hashes. Do not commit until checksum parity is 100%.

### Failure Case 3: Git Staging Index Contamination
- **Symptom**: `git status` reports modified files or untracked directories outside the target session notes (e.g. `.obsidian/*`, `events.ndjson`).
- **Root Cause**: Overly broad `git add` command executed without path restriction.
- **Resolution**:
  1. Immediately unstage all files using `git restore --staged .`.
  2. Re-stage strictly using explicit, exact file paths:
     ```bash
     git add "worklog/sessions/YYYY-MM-DD/<Project>/<File>.md"
     ```
  3. Re-verify with `git diff --cached --name-only` before committing.

### Failure Case 4: Canonical Vault Desynchronization
- **Symptom**: Remote `origin/main` has been updated with promoted sessions, but local Obsidian fails to display them.
- **Root Cause**: The physical repository backing Obsidian (`C:\Users\Admin\AI_WORKSPACES\airo-second-brain`) has not pulled the latest remote commits.
- **Resolution**:
  1. Check for uncommitted working tree conflicts in the canonical repo.
  2. Execute fast-forward pull:
     ```bash
     git -C /mnt/c/Users/Admin/AI_WORKSPACES/airo-second-brain pull --ff-only origin main
     ```
  3. Confirm Obsidian indices refresh and display the session under `AIRO Worklog.base`.

---

## 7. Delivery & Receipt Contract

Every execution of this SOP must conclude with a verified clipboard receipt generated via `scripts/airo-clipboard-receipt`:

```text
COPIED_TO_CLIPBOARD=YES
CLIPBOARD_METHOD=/mnt/c/Windows/System32/clip.exe
CLIPBOARD_ERROR=NONE
CLIPBOARD_READBACK=PASS
CLIPBOARD_CONTENT_HASH=PASS
```
