# SOP — AIRO Knowledge Continuity Operating Standard

**ID**: SOP_AIRO_KNOWLEDGE_CONTINUITY  
**Status**: CURRENT / APPROVED  
**Applies To**: All AIRO Consumers & Executors (ChatGPT, Antigravity, WSL, Hermes)  
**Last Updated**: 2026-08-25  

---

## 1. Operating Rules for Knowledge Capture

1. **Trigger Identification**: Checkpoint recommendations MUST evaluate against the 4 explicit triggers (`EXPLICIT_OWNER_REQUEST`, `BEFORE_EXECUTOR_MUTATION`, `CLEAR_DECISION_FINALIZATION`, `ARCHITECTURE_OR_SCOPE_CHANGE`). Generic trigger evaluation is forbidden.
2. **Two-Stage Approval**:
   - Stage 1: Owner approves knowledge capture proposal.
   - Stage 2: Owner reviews and approves the exact draft artifact prior to canonical persistence.
3. **Atomic Supersession**: Any decision mutation MUST enforce bidirectional status updates (`ACTIVE` vs `SUPERSEDED`) across both superseded and superseding decision entries in a single commit.

---

## 2. Operating Rules for Retrieval & Answers

1. Read canonical context (`CURRENT.md` / `decisions/decision-log.md`) before relying on model memory.
2. Filter decisions by `status=ACTIVE` for current operating rules.
3. Apply exact negative search phrasing when queries return zero matches.

---

## 3. Executor Transport & Clipboard Protocol

All session closeouts and knowledge persistence runs MUST execute via `scripts/airo-clipboard-receipt` and verify:
- `COPIED_TO_CLIPBOARD=YES`
- `CLIPBOARD_READBACK=PASS`
- `CLIPBOARD_CONTENT_HASH=PASS`


## Current V1 Operational SOP (2026-08-25)
- **Cadence**: Operational capture runs automatically at `EVERY_MEANINGFUL_EXECUTION`.
- **Live Markdown**: Running session state is continuously updated in Obsidian.
---

## 4. Closeout Semantic Carry-Forward Contract

1. **Active Semantic Envelope Snapshot**: Before `bin/airo-session close` clears runtime active state, a final semantic envelope (containing `owner_request`, `objective`, `position`, `progress`, `blocker`, `next_action`, and recorded decisions) MUST be snapshotted.
2. **Durable Historical Session Representation**: The permanent historical session Markdown artifact (`worklog/sessions/.../SESSION_<sid>.md`) MUST carry forward the active semantic context when available.
3. **Owner Request Priority**: The closeout renderer MUST use the semantic `owner_request` when available. Absence of raw chat/prompt transcript MUST NEVER be rendered as absence of Owner Request when a semantic `owner_request` is recorded.
4. **Deterministic Background Context**: When an explicit background is not provided in closeout JSON, background context MUST be deterministically derived from the session `objective` and semantic `owner_request`. Generic fallback ("Latar belakang tambahan belum dicatat") is forbidden when objective or owner request exist.
5. **Fresh-AI Reconstructability**: Closeout success requires that a fresh AI reader, reading ONLY the durable repository artifact, can fully reconstruct the session's background, Owner intent, objective, implemented outcomes, decisions, and next operating posture.
---

## 5. Session Materiality & Isolation Contract

1. **ONE OWNER OBJECTIVE = ONE PRODUCTION AIRO SESSION**: The lifetime of a production AIRO session maps 1-to-1 with a single main Owner objective.
2. **Sub-Executions Do Not Create Sessions**: A new Antigravity prompt, WSL command, executor packet, retry, verifier, regression test, debugging step, or evidence check does NOT by itself create a production session.
3. **Same Objective Continuation**: If `project_id` + main Owner objective remain unchanged, invocation MUST return `SESSION_ACTION=CONTINUE_EXISTING`. Record semantic events/checkpoints inside the owning session.
4. **Read-Only Verifier Sub-Execution**: A read-only verifier is a sub-execution of the owning objective. It MUST NOT start another production session.
5. **Retry Sub-Execution**: A retry after failed execution stays inside the same owning production session.
6. **Synthetic Test Isolation**: Synthetic tests, fixtures, simulated sessions, test harnesses, and regression-only sessions MUST use isolated repository/state/worklog roots (`AIRO_TEST_MODE=1` / `AIRO_SESSION_STATE_DIR`). They MUST NOT create production artifacts under canonical `worklog/sessions/`.
7. **Close Eligibility**: Production session close is allowed only when Owner objective DoD is satisfied, required acceptance verification has completed, no known directly-related blocker remains, and no directly-required repair is already known.
8. **New Maintenance Objective Boundary**: If a concrete defect is discovered AFTER the original objective was legitimately completed and closed, one NEW maintenance objective/session may be opened. All diagnosis, repair, regression, and verifier work for THAT defect remains inside that single maintenance session.
9. **Synthetic Test Event Promotion**: Synthetic/test outcomes are evidence/events belonging to the owning production session. Synthetic session notes are not promoted into human worklogs.
10. **Non-Session Boundaries**: Chat boundary, command boundary, executor boundary, and verifier boundary are NOT production session boundaries.
---

## 6. DEFERRED WORK / PR LIFECYCLE CONTRACT

1. **PR Definition**: A PR (Pekerjaan Rumah) is an actionable piece of work intentionally deferred for future execution.
2. **Exclusions**: A PR is NOT an idea, brainstorming possibility, generic recommendation, informational observation, or vague someday thought.
3. **Owner Explicit Deferral**: Direct Owner explicit deferrals or commitments ("nanti kerjain ini", "masukin PR", "next aja", "ini jangan lupa", "buat todo") MUST generate a PR.
4. **Conservative AI Capture**: AI may capture a PR without explicit user prompt ONLY when current discussion establishes a concrete future work commitment or explicit deferral. AI wording must be conservative and factual.
5. **Ambiguity Guard**: If intent is ambiguous or speculative, do NOT create a PR automatically. Ask Owner if clarification is needed.
6. **Deduplication Check**: Before creating a PR, inspect current open PRs in `state/deferred-work.json` to prevent obvious duplicate entries.
7. **Creation Timestamp**: Every PR MUST record a single `created_at` date (ISO YYYY-MM-DD) which is set once at creation and never reset upon priority or text updates.
8. **No Silent Session Creation**: A PR does NOT create a production session merely by existing.
9. **Start-Work Transition**: When work on a PR begins, its status transitions `TODO` → `ACTIVE`. It disappears from the HOME PR projection (which displays `TODO` items only) as the owning production session starts/continues.
10. **Completion**: Upon successful objective completion, the PR is marked `DONE` and removed from the active view as durable session history records its completion.
11. **Selective Closeout Promotion**: Session closeout creates a new PR only selectively when `next_action` describes concrete, actionable deferred work. Generic operational postures ("Use normally", "Monitor", "No further action") MUST NOT generate a PR.
12. **Git Policy**: PR register updates follow normal ASB checkpoint Git policy. No dedicated auto-push-per-PR behavior is required.
### 6.1 Owner Origin & Provenance Contracts

1. **Owner Origin Preservation**: A PR should preserve enough original Owner language for later recognition. When direct Owner wording is available and relevant, store a bounded exact excerpt in `origin_text` (up to 2 short utterances or equivalent).
2. **No Raw-Chat Archive**: `origin_text` is NOT a raw-chat archive; store only the minimum excerpt necessary for recognition. Never paraphrase and label it as exact Owner wording. If exact wording is unavailable, `origin_text` may be omitted.
3. **Owner vs AI_CAPTURED Source**: If the Owner explicitly requests a to-do/PR ("masukin PR", "buat todo", "next aja", "nanti kerjain ini"), `source` MUST be `OWNER`. `AI_CAPTURED` is reserved only for conservative AI identification without explicit Owner registration commands.
4. **Human-Familiar Title**: Owner-facing PR `summary` should prefer terminology recognizable from the Owner discussion. Avoid transforming familiar Owner language into abstract technical jargon in the primary title. Technical normalization belongs in `detail` and `context`.
5. **Sufficient Context**: A PR is not sufficiently captured by title alone. Authority data must allow an Owner or fresh AI to answer:
   - **WHAT**: Concrete work required (`detail`)
   - **WHY**: Why the work exists (`context`)
   - **OWNER_ORIGIN**: Bounded exact Owner utterances (`origin_text`)
   - **PROJECT**: Project / context mapping (`project` / `project_ref`)
   - **WHEN**: Creation date (`created_at`)
   - **SOURCE**: Durable reference link if available (`source_ref`)
