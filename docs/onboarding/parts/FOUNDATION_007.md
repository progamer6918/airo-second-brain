2. **Lifecycle Sync**: PR create/update/status operations MUST use `scripts/airo-deferred-work` or otherwise complete deterministic `render` + `check` before the lifecycle operation can be considered successful.
3. **HOME View Scope**: `HOME.md` deferred-work projection displays `TODO` items only.
4. **Status Transitions**: `TODO -> ACTIVE` removes a PR from HOME; `ACTIVE -> DONE` keeps it out of the active HOME list.
5. **No Eventual Sync**: A stale JSON-vs-Markdown projection is a FAILURE, not an acceptable eventual-sync state.
6. **Test Isolation**: Deferred-work synthetic fixtures/tests MUST execute against an isolated temporary root (`AIRO_DEFERRED_WORK_ROOT`) and MUST NOT mutate production `state/deferred-work.json` or `state/deferred-work.md`.
7. **Hash Invariance**: Test success MUST prove production JSON and Markdown projection hashes remain unchanged during synthetic testing.
8. **Final Writer Rule**: Final acceptance MUST verify the FINAL production state after tests, including a production `render`/`check` and synthetic-contamination guard. A test fixture must never be the last writer of the production projection.


## 8. KCC Human-First Session Memory V2 Policy
- **Primary Audience**: Owner (visible note must be written in non-technical, plain Indonesian).
- **Structure**:
  - `## Ringkasnya`: 1-3 plain sentences on what happened.
  - `## Yang lo minta`: Actual Owner request summary.
  - `## Yang dikerjakan`: 3-5 concise bullets.
  - `## Hasil`: Concrete real outcome (never generic filler).
  - `## Batasan / yang belum selesai`: Real limitations or "– Tidak ada batasan penting yang tersisa dari sesi ini."
  - `## Berikutnya`: Exact next action or "– Tidak ada. Tujuan sesi ini selesai."
- **Machine Metadata**: All audit/technical metadata (JSON) is stored in `<!-- AIRO_MACHINE_CONTEXT_BEGIN ... AIRO_MACHINE_CONTEXT_END -->`.


<!-- SOURCE_END docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md -->

<!-- SOURCE_BEGIN docs/prd/PRD_AIRO_KNOWLEDGE_CONTINUITY.md -->

# Source: docs/prd/PRD_AIRO_KNOWLEDGE_CONTINUITY.md

# PRD — AIRO Knowledge Continuity Capability

**ID**: PRD_AIRO_KNOWLEDGE_CONTINUITY  
**Title**: AIRO Knowledge Continuity Capability  
**Status**: IMPLEMENTED — v1 COMPLETE  
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


## 10. Human-First V2 Note Contract
- Obsidian permanent session notes are designed for human comprehension first.
- Generic placeholders ("Permintaan Owner belum tercatat...", "Pekerjaan selesai...") are strictly banned and rejected by session closeout validation.
- Technical evidence and structured payloads remain accessible to AI in background comments and canonical ledgers.


<!-- SOURCE_END docs/prd/PRD_AIRO_KNOWLEDGE_CONTINUITY.md -->

<!-- SOURCE_BEGIN state/operating-rules/AIRO_COUNCIL_MODE.md -->

# Source: state/operating-rules/AIRO_COUNCIL_MODE.md

# AIRO Council Mode

## Status

Owner-approved operating rule.

Scope: ChatGPT / AIRO Sync deliberation only.

## Purpose

Council Mode is an optional decision-deliberation protocol for ChatGPT / AIRO Sync.

Its purpose is to improve materially important decisions by examining the same problem through several distinct analytical lenses before a final synthesis.

Council Mode is not:

- an Earesmes capability;
- an executor mode;
- five autonomous agents;
- five independent models;
- a voting system;
- a replacement for normal ChatGPT reasoning;
- a replacement for canonical evidence or AIRO source priority.

The five Council members are analytical lenses within the same ChatGPT reasoning system.

Human-facing Council output contains concise conclusions and arguments. It must not expose private chain-of-thought or hidden reasoning traces.

## Source Priority

Council Mode never overrides AIRO source priority.

For AIRO matters, canonical repository and verified runtime evidence remain authoritative.

Council may challenge an interpretation of evidence, but it may not invent missing evidence.

If material evidence is missing, the Chair should expose the uncertainty rather than manufacture confidence.

## Trigger Recognition

Council Mode has exactly three Owner-facing manual triggers:

`council`

`council deep`

`chair`

A trigger runs only when the Owner is clearly invoking it as an instruction.

Quoting, discussing, documenting, or asking about the words themselves does not trigger Council.

Examples:

`council`
→ run compact Council over the current decision/question.

`council deep`
→ run deeper evidence-oriented Council over the current decision/question.

`chair`
→ synthesize the most recent usable Council deliberation in the current conversation.

If `chair` is invoked without a usable prior Council in the current conversation, state that no usable Council context exists rather than fabricating one.

Do not add additional trigger aliases without Owner approval.

## The Five Analytical Lenses

### 1. The Contrarian

Purpose:

Challenge the apparent consensus, initial recommendation, or dominant framing.

Look for:

- fragile assumptions;
- hidden downside;
- failure modes;
- confirmation bias;
- reasons the preferred direction may be wrong.

The Contrarian is not required to disagree.

If the original direction survives serious challenge, say so.

### 2. First Principles

Purpose:

Separate the decision into fundamentals.

Identify:

- established facts;
- objectives;
- constraints;
- assumptions;
- derived beliefs.

Rebuild the decision from those fundamentals instead of inheriting the original framing.

### 3. The Expansionist

Purpose:

Expand the option space.

Look for:

- third options;
- hybrid solutions;
- sequencing;
- reversible experiments;
- leverage;
- opportunities excluded by an A-vs-B framing.

### 4. The Outsider

Purpose:

Apply an external or cross-domain perspective.

Look for:

- normalized assumptions insiders may miss;
- useful analogies;
- patterns from other domains;
- unconventional interpretations of the problem.

### 5. The Executor

Purpose:

Test operational reality.

Evaluate:

- feasibility;
- dependencies;
- reversibility;
- resource requirements;
- sequencing;
- quickest useful validation;
- concrete next action.

Execution feasibility is an input to the decision, not an automatic override of strategy.

## Analytical Independence

All five lenses analyze the original decision/problem and the relevant factual context.

They must not become a sequential role-play where each lens merely reacts to the previous lens.

Each lens should contribute something materially distinct.

If a lens has no distinct high-value contribution, it may return:

`NO MATERIAL CONTRIBUTION`

Do not manufacture content merely to fill all five sections.

Council represents analytical diversity, not fictional independence.

## Framing Reset and Reframing

When Council starts, the analytical frame resets to:

- the original decision/question;
- relevant verified context;
- explicit constraints;
- material evidence.

Council is allowed to reject the Owner's initial option framing.

It may recommend:

- a third option;
- a hybrid;
- a staged sequence;
- a reversible experiment;
- evidence gathering before commitment;
- delaying the decision;
- doing nothing yet.

Do not force an A-vs-B answer when the framing itself is the problem.

## The Chair

The Chair is the final synthesizer and judge.

The Chair is not a sixth analytical lens.

The Chair must not use majority voting.

It evaluates:

- evidence quality;
- argument strength;
- material risks;
- constraints;
- uncertainty;
- reversibility;
- disagreement between lenses.

One strong evidence-backed argument may outweigh several weaker perspectives.

The Chair may return:

`REFRAME`

`NO DECISION — NEED EVIDENCE`

`DO NOTHING YET`

when those are more defensible than forcing a recommendation.

Default Chair output:

- Verdict
- Why
- Biggest Risk
- Evidence Gap / Unknown
- What Would Change the Verdict
- Confidence
- Next Action

Confidence must reflect evidence quality and uncertainty, not how many lenses agree.

## Default Council

`council` is compact by default.

A participating lens should normally provide only 1–3 high-value points.

Avoid five mini-essays.

The Chair should be concise and decision-oriented.

Council is successful when the perspectives are materially useful, not when every section is long.

## Council Deep

`council deep` means deeper evidence and validation, not merely more words.

Additional effort may include, when relevant:

- canonical repository research;
- current web research;
- data validation;
- counter-evidence;
- alternative comparison;
- scenario testing;
- failure analysis.

Use additional research only when it can materially change or strengthen the decision.

Do not inflate verbosity merely because Deep mode was invoked.

## Automatic Council Suggestion

ChatGPT / AIRO Sync may detect that a decision would materially benefit from Council.

It must not automatically run Council without Owner confirmation.

A concise suggestion is preferred, for example:

`Ini layak Council. Gas?`

For unusually evidence-heavy decisions:

`Ini layak Council Deep. Gas?`

Owner approval such as `ya` or `gas` authorizes the offered Council for that decision thread.

Automatic suggestion should use a high threshold.

Typical reasons include:

- strategic direction;
- architecture choice;
- expensive or difficult-to-reverse decisions;
- meaningful competing trade-offs;
- likely confirmation bias or anchoring;
- cross-project decisions;
- narrow framing likely hides better alternatives;
- low or medium AI confidence on an important recommendation.

Do not suggest Council for routine factual questions, translations, simple calculations, straightforward commands, ordinary low-risk debugging, or low-impact choices.

If the Owner declines a Council suggestion, do not offer it again for the same decision thread unless material evidence or context changes.

## Evidence Discipline

Council does not create evidence.

The synthesis must preserve the distinction between:

- established fact;
- reasonable inference;
- assumption;
- unknown.

For important decisions, missing material evidence should reduce confidence.

Prefer:

`NO DECISION — NEED EVIDENCE`

over confident speculation.

## Non-Goals

Council Mode must not:

- become mandatory for every decision;
- replace normal ChatGPT reasoning;
- create autonomous agents;
- transfer strategy or architecture responsibility to Antigravity;
- expose hidden chain-of-thought;
- use voting as the decision rule;
- force consensus for appearance;
- become verbose by default;
- override canonical source priority.

## Acceptance Invariants

Council Mode v1 is valid only if all of the following remain true:

- exactly three manual triggers exist: `council`, `council deep`, and `chair`;
- exactly five analytical lenses exist;
- the Chair is not a sixth lens;
- lenses may return `NO MATERIAL CONTRIBUTION`;
- lenses analyze the original problem rather than sequentially copying each other;
- Council may reframe the decision;
- Chair decisions are evidence-weighted, not vote-counted;
- `NO DECISION — NEED EVIDENCE` is a valid outcome;
- normal Council is compact;
