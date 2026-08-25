# PRD — AIRO Knowledge Continuity Capability

**ID**: PRD_AIRO_KNOWLEDGE_CONTINUITY  
**Title**: AIRO Knowledge Continuity Capability  
**Status**: DRAFT / REVIEWED  
**Owner**: AIRO Ecosystem  
**Last Updated**: 2026-08-25  

---

## 1. Problem & Objectives

Important AIRO reasoning, owner requests, architecture decisions, troubleshooting insights, small ideas, and project evolution currently risk remaining trapped within ephemeral chat sessions. Knowledge persistence alone is insufficient; future AI sessions must also be capable of retrieving the correct information and accurately distinguishing active truth from superseded historical decisions.

The objective of this capability is to define a structured, lightweight, and deterministic knowledge capture, retrieval, and decision lifecycle framework within the canonical AIRO Second Brain (`airo-second-brain`) repository.

---

## 2. Core Artifact Model (v1)

The v1 model consists strictly of four conceptual artifact classes:

1. **CONTEXT** — Answers: *"What is the current state?"* (e.g. `CURRENT.md`, `state/active-context.md`).
2. **LOG** — Answers: *"What happened?"* (e.g. `events/raw/events.ndjson`, worklogs, session closeout notes).
3. **DECISION** — Answers: *"What decision/current operating truth applies, and why?"* (e.g. `decisions/decision-log.md`).
4. **CAPABILITY / PRD** — Answers: *"What sufficiently mature capability is intended to be built?"* (e.g. `docs/prd/*.md`).

*No additional artifact classes are introduced for v1.*

---

## 3. Explicit Non-Goals (v1)

The following are explicitly **out of scope** for v1:
- Raw chat transcript dumping as primary memory.
- Continuous background semantic capture engines.
- Vector databases or embeddings storage.
- Graph databases or knowledge graphs.
- Automatic semantic similarity / deduplication engines.
- PRD duplicate-search software.
- Enterprise knowledge management bureaucracy.

---

## 4. Checkpoint Triggers & Workflow

AI MUST NOT continuously pattern-match or automatically persist every perceived sentence. AI MAY proactively recommend a knowledge checkpoint under exactly four explicit triggers:

1. `TRIGGER_1=EXPLICIT_OWNER_REQUEST` — Owner explicitly requests session capture or checkpointing.
2. `TRIGGER_2=BEFORE_EXECUTOR_MUTATION` — Preceding discussion introduced a new decision, architecture rule, scope change, or reusable operating requirement prior to execution.
3. `TRIGGER_3=CLEAR_DECISION_FINALIZATION` — Owner and AI reach a clear, reusable decision that can be looked up independently in the future.
4. `TRIGGER_4=ARCHITECTURE_OR_SCOPE_CHANGE` — Material change to project boundary, system design, or operating workflow.

### Two-Stage Owner Approval Flow
```text
Conversation → Checkpoint Trigger → AI Recommends Capture → OWNER APPROVES CAPTURE 
  → AI Generates Exact Artifact Draft → OWNER REVIEWS/EDITS DRAFT → OWNER APPROVES PERSISTENCE 
  → Executor Writes/Commits/Pushes → Validated Receipt
```

---

## 5. Decision Lifecycle & Supersession

- **Format**: `DEC-YYYYMMDD-NN`
- **Required Fields**: `id`, `date`, `status`, `decision`, `reason`, `impact`, `supersedes`, `superseded_by`.
- **Allowed Status**: `ACTIVE`, `SUPERSEDED`.
- **Bidirectional Supersession Rule**: When a new decision supersedes an old decision, both the new decision (`status=ACTIVE`, `supersedes=<old-id>`) and the old decision (`status=SUPERSEDED`, `superseded_by=<new-id>`) MUST be updated in the same bounded mutation.

---

## 6. Retrieval Contract & Search Order

When querying historical or continuity context (e.g. *"pernah bahas X?"*, *"kenapa dulu pilih X?"*):
1. **Search Order**: `1. CONTEXT` → `2. DECISION` → `3. LOG` → `4. CAPABILITY/PRD`.
2. **Decision Status Check**: If `ACTIVE`, present as current truth. If `SUPERSEDED`, follow `superseded_by` link and present the active replacement (describing the old decision strictly as historical).
3. **Non-Negative Search Rule**: Never claim *"tidak pernah dibahas"* unless absolute evidence exists. Report the actual scope searched (e.g. *"Tidak ditemukan pada CONTEXT/DECISION/LOG/CAPABILITY yang diperiksa"*).

---

## 7. Bootstrap Dependency & Executor Framework

- Continuity behavior requires loading canonical bootstrap rules (`BOOT.md` & `AGENTS.md`) into context.
- **Executor Transport Status**: `VALIDATED` (WSL & Antigravity clipboard transport verified with `CLIPBOARD_READBACK=PASS`).
- **Executor Formal Contract**: Formally defined under `docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md` and `docs/contracts/AIRO_AGENT_ROLE_CONTRACT.md`.


## Current V1 Operational Policy (2026-08-25)
- **Operational Capture**: Automatic & lightweight at every meaningful execution.
- **Knowledge Promotion**: Selective (PRD / Decision).
- **Manual Trigger**: Override / failsafe.


## Current V1 Operational Policy (2026-08-25)
- **Operational Capture**: Automatic & lightweight at every meaningful execution.
- **Knowledge Promotion**: Selective (PRD / Decision).
- **Manual Trigger**: Override / failsafe.
