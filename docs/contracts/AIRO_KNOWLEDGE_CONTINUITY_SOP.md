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
