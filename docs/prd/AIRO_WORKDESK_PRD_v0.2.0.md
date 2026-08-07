# AIRO WorkDesk PRD v0.2.0

- **Status:** FAST_TRACK_LOCAL_CANDIDATE
- **Project:** `AIRO_WORKDESK`
- **Repository target:** AIRO Second Brain (ASB)
- **Primary human interface:** Obsidian
- **Primary AI interface:** WorkDesk boot + task router + semantic wiki + evidence ledger

## Product Goal

A zero-context human or fresh AI should be able to enter WorkDesk, understand the professional world, find the right knowledge, perform common work, and audit why the system believes something without reading old chats.

## User Modes

### Casual reader — default
Starts from intent or symptom: find, solve, make, continue, learn. No taxonomy knowledge required.

### First reader
Uses a guided learning path from ecosystem → role → market/dealer → sales/network → analysis/strategy → execution.

### Practitioner / Owner
Uses playbooks and knowledge modules directly.

### Fresh AI
Boots deterministically, loads core context, then loads only task-relevant modules and source evidence.

## Functional Requirements

1. **Intent-first Home.** Human entrypoint must ask what the user wants to do, not which folder or framework they know.
2. **Progressive disclosure.** Core notes have a 10-second explanation, work meaning, practitioner guidance, and evidence layer.
3. **Task router.** Natural-language symptoms map to professional analysis paths.
4. **Concept-oriented knowledge.** Sources are evidence; knowledge is organized around work concepts.
5. **Atomic provenance.** Important claims have source ID + location + authority/confidence.
6. **Contextual source authority.** Current operational rules, theory/training, and Owner working-pattern questions use different authority logic.
7. **Noisy-note guard.** Presenter/transcription notes cannot silently override formal material.
8. **Practical playbooks.** WorkDesk must help perform work, not only explain terminology.
9. **Consumer independence.** Knowledge must not depend on a single model/persona.
10. **Public safety.** Credentials/auth material, private raw transcripts and unnecessary sensitive personal data are excluded.

## Corpus Baseline

Current supplied universe: 106 source entries, including 61 ASSDP files, 32 Notion notes and 13 direct supporting uploads. Structural extraction/accounting exists for the current universe; semantic/visual/rule-level digestion remains incomplete.

## Semantic Core v0.2

Fast-track v0.2 adds substantive concept modules for:

- Area Sales Supervisor operating model;
- ASSDP capability ladder;
- Honda/Main Dealer work ecosystem;
- channel and territory management;
- dealer review;
- market intelligence/demand management;
- targeting/forecasting;
- sales/stock/distribution;
- pricing/DP/financing;
- sales-force productivity;
- PDCA/PICA/RCA/DMAIC;
- NOS 2026 + applicability;
- INS/MyHero/NMS evidence boundaries;
- CRM/leads/customer experience;
- AT High;
- ND Plan/Reshape;
- supervisory leadership/influence/coaching/change;
- data analytics/Power BI;
- presentation/review logic;
- Owner applied projects and working model.

## Definition of Done

`FULLY_DIGESTED_AND_TRANSFERABLE=YES` requires all of the following:

- source accounting = 100%;
- meaningful text/table/rule coverage = 100%;
- meaningful visual coverage = 100%;
- canonical claims with provenance = 100%;
- source conflicts accounted = 100%;
- unlabeled uncertainty = 0;
- secret leakage = 0;
- fresh-AI critical comprehension benchmark = PASS;
- zero-context human navigation benchmark = PASS;
- Owner acceptance = PASS.

This proves functional transferability against an explicit benchmark; it does not claim identical hidden mental representations between different humans/models.
