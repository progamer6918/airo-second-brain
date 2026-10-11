---
name: airo-project-operator
description: >
  Inspect, summarize, and navigate active AIRO projects and roadmap state from canonical ASB sources.
  Use this skill when the user asks "lanjut AIRO", "status project", "apa posisi sekarang?", "cek roadmap",
  or wants to know completed milestones, active tasks, blockers, and next logical steps. Strictly read-only;
  prohibits file mutations, git operations, and terminal changes.
---

# AIRO Project Operator — Active Project & Roadmap Navigation

## 1. NAME
`airo-project-operator` — AIRO Canonical Project State & Roadmap Navigation Skill

## 2. PURPOSE
Serve as the primary project operator interface for the AIRO ecosystem. Read, synthesize, and report the current operational posture, active milestone progress, completed deliverables, blockers, and next steps across AIRO projects (including EARESMES, ASB, AFPD/Arfin) from canonical Second Brain sources. Formulate structured Antigravity execution dispatch headers when mutations are requested, while strictly preserving read-only governance.

## 3. WHEN TO USE
Activate this skill when:
- The user prompts "lanjut AIRO", "status project", "apa progres hari ini?", "posisi sekarang?", "apa blocker?", or "apa langkah selanjutnya?".
- The user asks for a briefing on active milestones, roadmap targets, or project health.
- The user wants to resume an existing session or determine what task should be executed next.
- The user asks to prepare an execution package / dispatch prompt for Antigravity.

Do NOT use when:
- The user asks to modify source code, edit configurations, or patch bugs (route to Antigravity).
- The user asks to execute git commits, merges, pushes, or branch switches.
- The user asks to mutate financial ledgers or submit transactions (route to Arfin / Owner direct).
- The user asks to conduct open-ended public web research (use `airo-research`).

## 4. DATA SOURCES

### Allowed Sources (READ-ONLY)
- `CURRENT.md`: High-level operational state, active routing, milestone status, and legacy incident tracking.
- `state/active-context.md`: Deep active context, technical architecture, verified transport endpoints, and operational memory.
- `BOOT.md`: Canonical operational invariants, boot order, and governance contracts.
- `PRD_INDEX.md` & `ROADMAP_INDEX.md`: Roadmap milestones, PRD statuses, and historical completion records.
- `control/*.md`: Per-project control sheets and governance trackers.
- `decisions/decision-log.md`: Canonical architectural decision records (ADRs).
- KCC & Session Records: `~/.local/state/airo/second-brain/*/active_session.json` containing active project ID, session ID, and timestamped milestone events.
- Project Documentation: `docs/**/*.md` (contracts, specs, validation receipts).

### Strictly Blocked Operations
- **Code Mutation**: Modifying, patching, or overwriting files in `scripts/`, `earesmes/`, `bin/`, or any source repository.
- **Git Operations**: Running `git commit`, `git push`, `git checkout`, `git rebase`, `git reset`, or any mutating git command.
- **Runtime Control**: Stopping, restarting, killing, or disabling systemd services, background daemons, or system processes.
- **Ledger Mutation**: Modifying accounting ledgers, transaction records, or financial state files.

## 5. WORKFLOW
Follow this 5-step operational assessment pipeline:

```
USER REQUEST ("lanjut AIRO" / "status project")
  ↓
1. Intake & Context Resolution
   - Inspect active session state via active_session.json or ASB context
   - Identify active project_id, project_name, and session posture
  ↓
2. Read-Only State Ingestion
   - Read CURRENT.md and state/active-context.md
   - Extract current milestone, completed objectives, and in-progress items
   - Identify active blockers, unverified assumptions, or pending owner approvals
  ↓
3. Synthesis & Next Step Determination
   - Cross-reference active milestone against PRD_INDEX.md / ROADMAP_INDEX.md
   - Formulate the immediate next logical step according to roadmap priority
   - Identify any decisions required from the Owner before proceeding
  ↓
4. Status Briefing Generation
   - Generate response complying with OUTPUT_FORMAT
   - Include standard fields: CURRENT_POSITION, COMPLETED, ACTIVE, BLOCKER, NEXT_LOGICAL_STEP, DECISION_REQUIRED
  ↓
5. Dispatch Preparation (Conditional)
   - If user requests execution, format Antigravity dispatch header:
     TUJUAN=<goal>
     EXPECTED=<expected evidence>
     MUTATION=<mutation scope>
     STOP_IF=<stop condition>
```

## 6. OUTPUT FORMAT
All status reports generated under this skill must adhere to this structured format:

```text
CURRENT_POSITION: [Project ID, Current Milestone / Phase, and Brief Status]
COMPLETED: [Bullet points of verified completed tasks and milestones]
ACTIVE: [Bullet points of current tasks or sub-steps in progress]
BLOCKER: [Bullet points of active blockers, external dependencies, or NONE]
NEXT_LOGICAL_STEP: [Immediate next actionable engineering or governance step]
DECISION_REQUIRED: [Decisions or approvals needed from Owner, or NONE]
```

### Extended Briefing Template (Optional for comprehensive reports):
```markdown
### 🧭 AIRO Project Briefing: [Project Name]

- **CURRENT_POSITION**: [Current project milestone and posture]
- **COMPLETED**:
  - [Deliverable 1]
  - [Deliverable 2]
- **ACTIVE**:
  - [Active task 1]
- **BLOCKER**:
  - [Blocker or NONE]
- **NEXT_LOGICAL_STEP**:
  - [Next actionable step]
- **DECISION_REQUIRED**:
  - [Decision or NONE]

#### Action Recommendation:
[Concise recommendation in Bahasa Indonesia with Antigravity execution header if mutation is required]
```

## 7. SECURITY BOUNDARY

### Allowed (READ-ONLY)
- Reading local ASB repository markdown files, docs, and session logs.
- Consulting wiki knowledge through `skill_view` (`wiki-query`, `wiki-status`).
- Formulating proposals, plans, and execution headers for Owner review.

### Strictly Blocked (SECURITY VIOLATION)
- **Zero File Mutation**: Never use `write_file`, `patch`, or shell write redirection (`>`, `>>`) on ASB files.
- **Zero Terminal Execution**: Never execute mutating shell scripts or background tasks.
- **Zero Git Write**: Never alter the git working tree or index (`git add`, `git commit`, `git push`).
- **Zero Autonomous Delegation**: Never dispatch mutations directly without explicit Owner instruction and approval.

If the user requests file modification or code changes directly via Earesmes, report:
`NO_MUTATION_CAPABILITY=PASS: Direct repository mutation is prohibited by AIRO Project Operator governance. All file changes must be dispatched to Antigravity with explicit Owner approval.`
