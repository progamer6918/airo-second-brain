1. **Classify** the command as Tier 2 per §2 and §4.
2. **Derive task slug**: `<project-short>_<verb>_<object>` — safe characters only.
3. **Confirm working directory** or use absolute wrapper path.
4. **Invoke wrapper**: `scripts/airo-vps-exec --task <slug> -- <command>`.
5. **Verify receipt fields** in output: `RESULT=`, `EXIT_CODE=`, `COPIED_TO_CLIPBOARD=`.
6. **Report receipt** in AGY response (do not fabricate fields not present in output).

---

## 6. Compliance & Enforcement

- Violation: AGY running a Tier 2 command without `airo-vps-exec` constitutes a
  **governance breach** under `AIRO_AGENT_ROLE_CONTRACT §4` and invalidates the session receipt.
- Tier 1 misclassification of a Tier 2 command: treated as governance breach.
- Wrapper failure (non-zero exit from wrapper itself, not from the wrapped command):
  AGY must stop, report the wrapper error, and not proceed as if delivery succeeded.
- Clipboard FAIL is NOT a Tier 2 blocker — wrapper exit code follows the underlying command.
  But `COPIED_TO_CLIPBOARD=NO` must be faithfully reported in the AGY receipt.

---

## 7. Relationship to Existing Contracts

| Contract | Relationship |
|---|---|
| `AIRO_AGENT_ROLE_CONTRACT.md §2.2` | This contract operationalizes Antigravity's "Evidence Collection" responsibility. |
| `AIRO_DIRECT_WSL_EXECUTION_CONTRACT §9–10` | This contract names the binding mechanism (airo-vps-exec) that satisfies those rules. |
| `AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT` | Tier 2 flow is the enforcement mechanism for AUTO_COPY_REQUIRED=true. |
| `AIRO_EXECUTION_EVIDENCE_CONTRACT §8` | Tier 2 receipt provides the verifiable clipboard evidence chain. |
| `AIRO_CODE_CHANGE_CONTRACT` | Applies when implementing changes approved under this contract. |
| `scripts/airo-vps-exec` | Canonical Tier 2 entry point. Must not be modified to satisfy this contract. |

---

## 8. Scope Exclusions

This contract governs AGY (Antigravity) terminal execution only.

- **Earesmes / Hermes**: Not governed by this contract. Earesmes uses its own adapter chain.
- **ChatGPT direct WSL**: Governed by `AIRO_DIRECT_WSL_EXECUTION_CONTRACT` directly.
- **Automated background services** (telegram-gateway, etc.): Not governed by this contract.
- **airo-vps-exec internal logic**: This contract does not modify or extend the wrapper script.

<!-- SOURCE_END docs/contracts/AIRO_AGY_EXECUTION_GATEWAY_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md -->

# Source: docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md

# AIRO Direct WSL Execution Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-11
**Authority**: OWNER_APPROVED

1. When Owner says `via WSL`, use direct WSL; do not redirect to Antigravity or a manual file-download workflow.
2. Prefer one copy-paste-ready bounded execution packet per Owner interaction.
3. A packet may contain multiple deterministic sub-steps when no new Owner decision is required.
4. Optimize for the fewest safe Owner interaction cycles, not one technical sub-step per turn.
5. Antigravity low-limit one-small-gate behavior is a separate execution mode.
6. Stop at genuine boundaries: new Owner approval, unresolved identity/ambiguity, owner-work conflict, remote divergence, remote-runtime authorization, or required Owner visual/live acceptance.
7. The Owner interactive parent WSL shell MUST survive every outcome. Never apply `set -e`, `set -u`, or `exit` to the parent shell.
8. Run strict execution inside an isolated child shell or subshell.
9. Capture stdout+stderr to a timestamped `/tmp` receipt through `tee`.
10. Finish Owner delivery with `scripts/airo-clipboard-receipt`; verified clipboard readback and content-hash match are mandatory.
11. Owner-facing commands must be chat-formatting-safe; literal nested Markdown fences inside an outer command fence are forbidden.
12. Every meaningful execution starts or continues `bin/airo-session`, records semantic terminal outcomes, and closes with a structured worklog at an objective or explicit pause boundary.
13. Session closeout writes permanent `worklog/sessions/...` and regenerates `worklog/daily/...` for Obsidian continuity.
14. Git push is never implied. Bundle it only with explicit Owner authorization, verified remote parity, exact-path staging, public-safety checks, and never force push.
15. Never reset, stash, rebase, clean, overwrite, or stage unrelated Owner work.
16. Script success is not task success; completion remains evidence-driven.
17. Acceptance evidence follows `AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`; direct WSL should automate backend acceptance when it can prove the required behavior without Owner manual review.


## Mandatory Operational Execution Continuity (KCC v1)

Every meaningful AIRO execution MUST automatically record semantic operational state:

1. **Resolve/Start/Continue Session**: Before execution, verify active session context (`bin/airo-session start`).
2. **Semantic PRE-EXECUTION Checkpoint**: Record action intent, active owner request, current position, and next action (`scripts/airo-capture --phase PRE_EXECUTION ...`).
3. **Bounded Execution**: Execute approved task.
4. **Semantic POST-EXECUTION Checkpoint**: Record factual outcome, evidence pointer, updated position, and next action (`scripts/airo-capture --phase POST_EXECUTION ...`).
5. **Live Obsidian Artifact**: Automatically refreshed at `worklog/sessions/<date>/<project>/SESSION_<id>.md` during the running session.

> **CRITICAL RULE**: `RAW COMMAND != KNOWLEDGE RECORD`. Do NOT store raw terminal command strings or raw prompt dumps as knowledge records. Record the semantic state around the execution.

<!-- SOURCE_END docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md -->

# Source: docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md

# AIRO Acceptance Evidence Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-11
**Authority**: OWNER_APPROVED

1. Acceptance evidence MUST match the actual objective and definition of done.
2. Script success, commit success, or push success alone never proves task success.
3. Functional, navigation, data, workflow, link, state, and semantic correctness MAY be accepted from verified backend evidence when those properties are deterministically measurable.
4. Pixel-level screenshots or GUI inspection are mandatory only when visual appearance, layout, theme behavior, clipping, rendering fidelity, or another inherently visual property is an explicit objective/DoD, or when backend evidence cannot prove the required behavior.
5. Do not force Owner screenshot/manual review for behavior already proven by trustworthy backend/runtime evidence.
6. When a task has both functional and cosmetic goals, classify them separately. Functional PASS may coexist with a non-blocking note that cosmetic pixel review was not performed.
7. Live/runtime evidence remains mandatory when the objective depends on actual runtime state that static/backend evidence cannot establish.
8. Acceptance requirements MUST be declared before closeout and must not be inflated after implementation merely because additional evidence is possible.
9. Owner may explicitly require visual/live acceptance even when backend evidence would otherwise suffice.
10. Every final verdict remains governed by required-vs-actual evidence and source priority.

<!-- SOURCE_END docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_EXECUTION_EVIDENCE_CONTRACT.md -->

# Source: docs/contracts/AIRO_EXECUTION_EVIDENCE_CONTRACT.md

# AIRO Execution Evidence Contract

- **Status:** `ACTIVE_CONTRACT`
- **Version:** `1.0.0`
- **Scope:** `ASB_GLOBAL`

---

## 1. Purpose

This contract defines evidence classification, required evidence matching, and execution assurance rules for AIRO Second Brain v0.6.

---

## 2. Evidence Classes

1. `LIVE_RUNTIME`: Verified execution on real live infrastructure (e.g. HTTP 200 JSON from live Apps Script, verified process state).
2. `SIMULATION`: Execution in dry-run, mock, or local test harness.
3. `VERIFIED_COMMIT`: Git commit object verified in local repository.
4. `VERIFIED_REMOTE_PARITY`: Verification that local commit SHA matches remote HEAD.
5. `MACHINE_TELEMETRY`: Raw event recorded in `events/raw/events.ndjson`.

---

## 3. Invariant Matching Rules

- A `SIMULATION` evidence item MUST NEVER satisfy a requirement specifying `LIVE_RUNTIME` evidence.
- If required evidence is `LIVE_RUNTIME` and actual evidence is `SIMULATION`, the validator MUST compute `BELUM_TERBUKTI` and `can_advance: NO`.

## 8. Output Transport Evidence Invariant

- Clipboard delivery is output transport evidence, NOT task-completion evidence.
- Command exit code 0 does not prove receipt delivery.
- Verified read-back (`CLIPBOARD_READBACK=PASS`) and complete content match (`CLIPBOARD_CONTENT_HASH=PASS`) are mandatory **unless the OSC52 terminal delivery exception applies** (see § 8.1 below).
- Do not confuse clipboard delivery success with task verdict BERHASIL or CAN_ADVANCE.

### 8.1 OSC52 Terminal Delivery Exception

> `OSC52_SEND_SUCCESS_DOES_NOT_REQUIRE_READBACK=true`

**Applies to**: VPS Terminal OSC52 adapter; AGY VPS parent TTY OSC52 adapter.

For **OSC52-based delivery paths**, clipboard readback is structurally unavailable — the terminal emulator absorbs the escape sequence and no in-process read path exists. The following substitutions are accepted:

| Field | Standard Requirement | OSC52 Accepted Value |
|---|---|---|
| `CLIPBOARD_READBACK` | `PASS` | `NOT_AVAILABLE` |
| `CLIPBOARD_CONTENT_HASH` | `PASS` | `NOT_AVAILABLE` |
| `COPIED_TO_CLIPBOARD` | `YES` (via readback) | `YES` (via confirmed OSC52 WRITE exit 0) |
| `DELIVERY_STATUS` | verified match | `OSC52_WRITE_SUCCESS_READBACK_NOT_AVAILABLE` |

This exception does **NOT** relax evidence requirements for the LOCAL PC/WSL clipboard adapter.

**Cross-reference**: [`AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT`](./AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT.md) — canonical authority for OSC52 delivery rules and the `OSC52_SEND_SUCCESS_DOES_NOT_REQUIRE_READBACK` flag.  
**KCC SOP cross-reference**: [`AIRO_KNOWLEDGE_CONTINUITY_SOP`](./AIRO_KNOWLEDGE_CONTINUITY_SOP.md) § 3.1 — mirrors this exception for session closeout transport.


<!-- SOURCE_END docs/contracts/AIRO_EXECUTION_EVIDENCE_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_STATUS_CONTRACT.md -->

# Source: docs/contracts/AIRO_STATUS_CONTRACT.md

# AIRO Status Receipt Contract

- **Status:** `ACTIVE_CONTRACT`
- **Version:** `1.1.0`
- **Scope:** `ASB_GLOBAL`
- **Owner Approved Date:** 2026-08-04

---

## 1. Purpose & Core Invariant

This contract defines the standard human-facing receipt (`🧭 AIRO STATUS`), the machine-facing structured JSON receipt, and the deterministic mapping between them.

### Critical Invariant
Chat responses, Session worklogs, and Daily navigation views **MUST NOT** independently re-infer or recalculate current task outcomes. All interfaces MUST render their status directly from the same single structured machine receipt computed by `scripts/airo-task-verdict`.

---

## 2. Section A — Human-Facing Receipt Specification (`🧭 AIRO STATUS`)

All human-facing status outputs produced by AI consumers or tools MUST conform to this exact structure:

```text
🧭 AIRO STATUS

📍 Project — <Project Name>
📌 Lagi di — <Milestone / Position Name>
📈 Progress — <Evidence-based progress summary>

🧪 Bukti
Yang wajib ada — <Required evidence items>
Yang sudah ada — <Actual evidence items>
Kesimpulan — BERHASIL | BERHASIL_DENGAN_BATASAN | BELUM_TERBUKTI | TERHAMBAT | GAGAL
Boleh lanjut — YA | TIDAK

⛔ Hambatan — <Blocker description or "Tidak ada">
➡️ Berikutnya — <Canonical next action>
🏁 Selesai kalau — <Definition of Done / DoD>
```

---

## 3. Section B — Machine-Facing Receipt Specification (JSON Schema)

Every execution task MUST generate or evaluate a structured JSON receipt with these minimum fields:

*(ILLUSTRATIVE EXAMPLE ONLY — NOT CURRENT PROJECT STATE)*

```json
{
  "project_id": "ASB_GLOBAL",
  "position_id": "M1",
  "position_name": "Governance & Execution Assurance",
  "script_status": "SCRIPT_SUCCESS",
  "required_evidence": ["PRD_v06_DesignSpec_Contracts_Validator"],
  "actual_evidence": ["Validator_Tests_Passed"],
  "limitations": [],
  "blockers": [],
  "task_status": "BERHASIL",
  "can_advance": "YES",
  "next_exact_action": "START_M2_SESSION_AND_WORKLOG_IMPLEMENTATION",
  "done_when": "ASB v0.6 M1 closeout complete and M2 ready to begin",
  "evidence_references": [
    "docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md",
    "docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md"
  ]
}
```

---

## 4. Section C — Deterministic Mapping Rules

1. `project_id` -> `📍 Project`
2. `position_id` / `position_name` -> `📌 Lagi di`
3. `script_status` + `actual_evidence` -> `📈 Progress`
4. `required_evidence` -> `Yang wajib ada`
5. `actual_evidence` -> `Yang sudah ada`
6. `task_status` -> `Kesimpulan` (`BERHASIL`, `BERHASIL_DENGAN_BATASAN`, `BELUM_TERBUKTI`, `TERHAMBAT`, `GAGAL`)
7. `can_advance` -> `Boleh lanjut` (`YES` -> `YA`, `NO` -> `TIDAK`)
8. `blockers` -> `⛔ Hambatan` (If empty -> `Tidak ada`)
9. `next_exact_action` -> `➡️ Berikutnya`
10. `done_when` -> `🏁 Selesai kalau`

### Validation Enforcement Rules
- `script_status != SCRIPT_SUCCESS` => `Kesimpulan = GAGAL`, `can_advance = NO`.
- `blockers` non-empty => `Kesimpulan = TERHAMBAT`, `can_advance = NO`.
- `required_evidence` missing or unsatisfied => `Kesimpulan = BELUM_TERBUKTI`, `can_advance = NO`.
- `limitations` non-empty => `Kesimpulan = BERHASIL_DENGAN_BATASAN`, `can_advance = NO`.
- All `required_evidence` satisfied, no blockers, no limitations => `Kesimpulan = BERHASIL`, `can_advance = YES`.

<!-- SOURCE_END docs/contracts/AIRO_STATUS_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT.md -->

# Source: docs/contracts/AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT.md

# AIRO Terminal Receipt Delivery Contract

AUTO_COPY_REQUIRED=true
PRIMARY_METHOD=OSC52
MANUAL_COPY=DISALLOWED
OSC52_SEND_SUCCESS_DOES_NOT_REQUIRE_READBACK=true
RECEIPT_FLOW=COMMAND -> RECEIPT -> CLIPBOARD -> PASTE

<!-- SOURCE_END docs/contracts/AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md -->

# Source: docs/contracts/AIRO_SESSION_PROJECTION_SYNC_CONTRACT.md

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
