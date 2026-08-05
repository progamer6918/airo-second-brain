# AIRO Second Brain PRD v0.6.0

## Execution Assurance, Human Work History & LLM Wiki Loop Specification

- **Status:** `OWNER_APPROVED_IMPLEMENTATION_TARGET`
- **Owner:** Egit Aristo Randas
- **Approved Date:** 2026-08-04
- **Scope:** `ASB_GLOBAL`
- **Target System:** AIRO Second Brain v0.6
- **Inherits From:** [AIRO Second Brain PRD v0.5.1](AIRO_SECOND_BRAIN_PRD_v0.5.1.md)
- **Primary Design Spec:** [AIRO Second Brain v0.6 Design Specification](../specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md)
- **Roadmap:** [AIRO Second Brain v0.6 Roadmap](../roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md)
- **Approved Decision Record:** [Owner Architecture Approval 2026-08-04](../../decisions/approved/asb-v06-architecture-owner-approval-20260804.md)

---

## 1. Executive Summary & Purpose

AIRO Second Brain v0.6 upgrades the ASB kernel from a passive shared-memory repository into an active **Execution Assurance**, **Human Work History**, **Obsidian Cockpit**, and **LLM Wiki Memory Loop** system.

### Core Problem Solved
Prior workflows allowed script execution success (`EXIT_CODE=0`) to be mistranslated as milestone or task completion, creating "false PASS" states where work appeared done but lacked verified live evidence. Additionally, human session work history was scattered across ephemeral chat transcripts.

### Key Architectural Deltas in v0.6
1. **Execution Assurance Invariant:** Script execution success (`SCRIPT_SUCCESS` / `EXIT_CODE=0`) does NOT equal task completion (`BERHASIL`) or milestone advancement permission (`CAN_ADVANCE=YES`).
2. **Deterministic Task Validator:** `scripts/airo-task-verdict` dynamically computes task status (`BERHASIL`, `BERHASIL_DENGAN_BATASAN`, `BELUM_TERBUKTI`, `TERHAMBAT`, `GAGAL`) based strictly on required vs actual evidence.
3. **Human-Facing Status Receipt (`🧭 AIRO STATUS`):** Standardizes all progress reporting into clear, baby-friendly Indonesian terms without exposing technical jargon or raw UUIDs.
4. **Project-Scoped Session Worklog Model:** 1 session = 1 project + 1 main work objective. Multiple checkpoints update the same active session draft. Project work push and session closeout push are conceptually separate.
5. **Multi-Layer Memory Architecture:** Clear separation between Raw Events, Session (episodic memory), Daily (generated navigation view), Canonical Project Docs (current truth), Decisions, and LLM Wiki (reusable semantic lessons).
6. **Obsidian Cockpit UX:** Obsidian opens the same ASB repository directly as a human navigation interface (`HOME.md`, `Hari Ini`, `Bases`).

---

## 2. Traceability & Acceptance Model

Every v0.6 milestone requirement follows strict acceptance traceability:

```text
REQUIREMENT -> IMPLEMENTATION -> REQUIRED EVIDENCE -> ACTUAL EVIDENCE -> COMPUTED VERDICT
```

If required live evidence is missing or simulated only:
- **Kesimpulan:** `BELUM_TERBUKTI`
- **Boleh lanjut:** `TIDAK`

---

## 3. Seven Canonical Milestones

The v0.6 upgrade is structured into exactly seven canonical milestones:
- **M0 — Reality Audit & Design Freeze** (DONE — M0B Evidence-Bound Accepted)
- **M1 — Governance & Execution Assurance** (DONE — Closeout Record Verified)
- **M2 — Session & Worklog** (DONE — Corrected Closeout Record Verified)
- **M3 — Obsidian Human Experience** (DONE — Human Cockpit Record Verified)
- **M4 — LLM Wiki Memory Loop** (DONE — Governed Memory Loop Record Verified)
- **M5 — Cross-Consumer & Failure Proof** (DONE — Cross-consumer safety & failure proof verified)
- **M6 — Owner Acceptance & Cutover** (NOT_YET_PROVEN — Next Active Target)

No ad-hoc roadmap gates (e.g. M2.1A, Shadow Gate) are allowed without explicit Owner approval.

---

## 4. Operational & Security Policies

1. **Repository Visibility:** The ASB repository is PUBLIC. All credentials, API tokens, OAuth secrets, private transcripts, and sensitive personal data are strictly forbidden.
2. **Runtime Sync Safety:** `ops/runtime/airo-runtime-runner.sh` remains DISABLED until its automatic rebase behavior is replaced with safe conflict-free handling.
3. **Finance Legacy Timer:** `airo-full-auto-sheets-sync.timer` is classified as `RETIRE_CANDIDATE` for the AIRO Finance project and recorded as a cleanup candidate only.

For detailed architecture, workflow diagrams, before/after comparisons, and complete design rationale, see the comprehensive [Design Specification](../specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md).
