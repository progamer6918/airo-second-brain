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

## Current session format and capture scope

For current human-facing session memory, use the six headings and hidden machine context defined by `docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md` §8. Legacy section-count examples below/above are not a second current formatting requirement. Operational event/session capture and semantic canonical promotion are distinct activities; this promotion SOP does not authorize bypassing KCC semantic approval or lifecycle guards.

<!-- SOURCE_END docs/operations/AIRO_SESSION_WORKLOG_PROMOTION_SOP.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md -->

# Source: docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md

---
type: contract
project: GLOBAL
status: APPROVED
audience: human-ai
---

# 📜 AIRO Input Processing Contract

Contract for receiving, classifying, digesting, reconciling, routing, and canonicalizing all Owner-supplied inputs into AIRO Second Brain (ASB).

## Core Principle

> [!IMPORTANT]
> `RAW_INPUT -> DIRECT_CANONICAL_TRUTH` is STRICTLY FORBIDDEN.
> `RAW_INPUT -> AUTOMATIC_NEW_WIKI_NOTE` is STRICTLY FORBIDDEN.
> Owner-supplied files, messages, or notes do NOT automatically become canonical system truth. Every input must pass through the canonical processing pipeline.

---

## 🔄 Processing Pipeline

```text
OWNER INPUT 
  ↓
1. RECEIVE
  ↓
2. CLASSIFY (Identify Input Type & Sensitivity)
  ↓
3. REGISTER (If durable provenance tracking is needed)
  ↓
4. DIGEST (Extract meaningful units, facts, claims)
  ↓
5. RECONCILE WITH CANONICAL STATE (Compare against ASB truth)
  ↓
6. ROUTE (Direct to appropriate memory/project layer)
  ↓
7. VALIDATE (Run tests, secret scans, link integrity)
  ↓
8. CANONICALIZE (Commit to canonical repo)
```

---

## 🏷️ Input Classification (Input Types)

Every input received from the Owner or external environment must be classified into one of the following 12 types:

1. `OWNER_FACT` — Factual statements supplied by the Owner regarding business, project, or personal domain.
2. `OWNER_DECISION` — Authoritative Owner decisions overriding or establishing policy, scope, or architecture.
3. `OWNER_CORRECTION` — Explicit corrections to existing ASB knowledge, claims, or data.
4. `NEW_SOURCE_DOCUMENT` — New training materials, presentation decks, PDFs, spreadsheets, or formal guidelines.
5. `CURRENT_BUSINESS_DATA` — Operational metrics, monthly sales numbers, tracking sheets, active logs.
6. `PROJECT_ARTIFACT` — Deliverable templates, codebase modules, scripts, schemas, or design blueprints.
7. `EXTERNAL_RESEARCH` — Market benchmarks, competitor data, industry research from external web/sources.
8. `NEW_TERMINOLOGY` — Business acronyms, technical glossaries, role definitions.
9. `HISTORICAL_CONTEXT` — Background history or past context explaining prior decisions or legacy systems.
10. `UNVERIFIED_INFORMATION` — Hypotheses, unconfirmed rumors, draft proposals needing validation.
11. `EPISODIC_INPUT` — Transient schedule reminders, meeting times, one-off chat banter, immediate task commands.
12. `SECRET_OR_SENSITIVE` — Credentials, API tokens, passwords, private personal identification, raw unredacted chats.

---

## ⚖️ Reconciliation Outcomes

Comparing new input against current ASB state must yield exactly one of the following 10 outcomes:

- `NEW` — Factual meaning not previously captured in ASB.
- `SUPPORTING` — Corroborates existing ASB knowledge; adds provenance weight.
- `DUPLICATE` — Identical to existing knowledge; no new note required.
- `UPDATE` — Refines existing ASB knowledge with newer/more accurate details.
- `CORRECTION` — Corrects erroneous ASB state; supersedes older claim with explicit provenance.
- `CONFLICT` — Contradicts existing ASB knowledge without clear resolution; logged in Conflict Register.
- `SUPERSEDED` — Newer authoritative source replaces older source; older source marked historical.
- `HISTORICAL_ONLY` — Relevant only as historical record; does not alter current operating state.
- `UNRESOLVED` — Requires further clarification before canonicalization.
- `EXCLUDED` — Rejected due to security, privacy, out-of-scope, or zero-utility rules.

---

## 🗺️ Canonical Routing Targets

Target memory/repository layers for reconciled meaning:

- `PROJECT_TRUTH` — `projects/*.md` (Project scope, milestone, current status)
- `DECISION` — `decisions/decision-log.md` or `decisions/approved/*.md`
- `SEMANTIC_KNOWLEDGE` — `wiki/<domain>/...` (Structured, provenance-backed knowledge)
- `PLAYBOOK` — `wiki/<domain>/playbooks/*.md` (Operating procedures & diagnosis flow)
- `DELIVERABLE` — `wiki/<domain>/deliverables/*.md` (Output blueprints & quality gates)
- `GLOSSARY` — `wiki/<domain>/glossary/*.md` (Domain terms & definitions)
- `SOURCE_EVIDENCE` — `evidence/<domain>/...` (Ledgers, manifests, coverage matrices)
- `CURRENT_DATA` — `worklog/daily/` or active task workspace (Transient operational data)
- `SESSION_ONLY` — Active session context / temporary scratch (Not persisted to Wiki)
- `MACHINE_EVENT` — `events/raw/events.ndjson` (Automated session & system log events)
- `EXCLUDED` — Discarded safely without repository footprint

---

## ❓ The 10 Core Reconciliation Questions

Before committing any input to canonical memory, answer:

1. **What is this input?** (Classify input type)
2. **Who/what is the source?** (Trace origin & authority level)
3. **How authoritative and current is it?** (Compare against current formal baseline)
4. **Which project or domain does it affect?** (Identify target project/child project)
5. **What does ASB already know about this topic?** (Inspect canonical knowledge/ledgers first)
6. **What is the reconciliation outcome?** (New, supporting, duplicate, update, correction, conflict, etc.)
7. **What durable meaning is worth retaining?** (Distill core facts/claims from raw text)
8. **Where does that meaning belong?** (Select canonical routing target)
9. **What provenance must remain?** (Record source, date, authority, and confirmed status)
10. **What must NOT be retained?** (Filter secrets, raw transcripts, redundant clutter)

<!-- SOURCE_END docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_MANUAL_SYNC_QUEUE_POLICY.md -->

# Source: docs/contracts/AIRO_MANUAL_SYNC_QUEUE_POLICY.md

# AIRO Manual Sync Queue Policy

`inbox/manual-sync-queue.md` is staging, not canonical. Operator AIRO Sync / Antigravity must follow this lifecycle policy.

## Lifecycle States

- **PENDING**: Staged capture that has not been processed.
- **SUMMARIZED**: A short, operator-friendly summary has been generated.
- **OWNER_ACTION_REQUESTED**: Action card sent to owner on Telegram.
- **OWNER_APPROVED_ACTION**: Owner has clicked approval in Telegram.
- **PROCESSING**: The operator is currently executing the promotion/processing action.
- **CANONICALIZED**: Content has been written to canonical project files.
- **READBACK_VERIFIED**: The changes have passed canonical verification / readback.
- **PROCESSED**: The staged block has been marked as resolved.
- **ARCHIVED**: Staged block is moved to the archives.
- **QUEUE_COMPACTED**: Staging file has been cleaned of processed entries.
- **PUSHED**: Changes have been pushed to origin main.

Other valid states:
- **DEFERRED**: Deferred project backlog.
- **ARCHIVED_OBSOLETE**: Obsolete capture archived.
- **BLOCKED_NEEDS_OWNER**: Blocked due to unresolved business choices.
- **BLOCKED_CONFLICT**: Blocked due to merge conflicts.
- **BLOCKED_SECRET**: Blocked by secret guard.

## Core Rules

1. **Staging Status Only**: `inbox/manual-sync-queue.md` is a temporary staging file. Do not trust or promote blocks unless requested by the owner or approved via Telegram actions.
2. **Latest Detection**: The latest capture is defined as the last valid heading matching `## YYYY-MM-DD — ...` at the bottom of the active queue.
3. **Archiving processed blocks**: Processed captures must move to `archive/manual-sync-queue/YYYY-MM-DD/<capture-id>.md`. Never delete capture history.
4. **Archiving deferred captures**: Deferred captures must move to `inbox/deferred/` or `decisions/deferred/`.
5. **Compaction**: The active staging queue `inbox/manual-sync-queue.md` must be compacted after processing.
6. **Readback Safeguard**: Never mark a capture block as processed or archive it unless the canonical readback check passes.

<!-- SOURCE_END docs/contracts/AIRO_MANUAL_SYNC_QUEUE_POLICY.md -->

<!-- SOURCE_BEGIN meta/update-protocol.md -->

# Source: meta/update-protocol.md


last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Second Brain Update Protocol

This protocol controls how AIRO Second Brain is updated.

Update Layers
Layer 1 — Auto-capturable

May be written automatically by configured local consumers:

inbox/[consumer]-[YYYY-MM-DD]-[HHMM].md

May be appended automatically:

state/active-context.md
meta/changelog.md
decisions/pending-decisions.md

Rules:

Append-only preferred.
No secrets.
No raw transcripts.
No full email bodies.
No credential/token contents.
No canonical rewrite.
Layer 2 — Approval-gated canonical files

Require owner approval before modification:

CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
identity/*
systems/*
agents/*
projects/*
decisions/decision-log.md
meta/update-protocol.md
meta/staleness-policy.md

Rules:

Agent may propose updates.
Owner approves before write/commit.
Do not silently rewrite.
Layer 3 — Project canonical repos

Project-specific execution truth remains in the relevant project repo.

Example:

AIRO Finance canonical status lives in:

vortex-ai-skill-lab/docs/AIRO_FINANCE_PRD_LIVING.md
vortex-ai-skill-lab/docs/AIRO_FINANCE_CURRENT_STATE.md
vortex-ai-skill-lab/docs/airo-finance/records/

AIRO Second Brain may point to project truth, but must not replace it.

Distillation Trigger

Run distillation when:

14+ days since last CURRENT.md update; or
a major milestone is completed; or
inbox grows too large; or
owner explicitly asks for "distill Second Brain"; or
a consumer notices stale context.

Distillation means:

Read relevant inbox/session closeouts.
Summarize important changes.
Propose updates to canonical files.
Owner approves.
Apply canonical updates.
Append meta/changelog.md.
Session Closeout Requirement

Every meaningful session should end with a closeout containing project/topic, summary, decisions, pending decisions, files/repos touched, evidence/tests/readbacks, blockers/risks, and next action.

Auto-Commit Policy

Auto-commit is not universal.

Allowed only when:

Consumer runs in a configured local environment.
Git identity is configured.
