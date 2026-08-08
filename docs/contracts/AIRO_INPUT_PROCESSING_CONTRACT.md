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
