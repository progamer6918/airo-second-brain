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
