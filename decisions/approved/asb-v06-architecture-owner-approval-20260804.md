# Owner Decision Record — AIRO Second Brain v0.6 Architecture Approval

- **Decision ID:** `ASB-DEC-20260804-V06-ARCH`
- **Owner:** Egit Aristo Randas
- **Date:** 2026-08-04
- **Status:** `APPROVED_BY_OWNER`
- **Scope:** `ASB_GLOBAL`

---

## 1. Decision Summary

The Owner has explicitly approved the final architecture for **AIRO Second Brain v0.6**, focusing on **Execution Assurance**, **Human Work History**, **Obsidian Cockpit UX**, and **LLM Wiki Memory Loop**.

---

## 2. Approved Architecture Points

1. **Scope:** Belongs to `ASB_GLOBAL` (`AIRO Second Brain v0.6`). No separate "Obsidian project" shall be created.
2. **Execution Assurance Invariant:** Script execution success (`EXIT_CODE=0` / `SCRIPT_SUCCESS`) does NOT mean task completion (`BERHASIL`) or milestone advancement (`CAN_ADVANCE=YES`).
3. **Human Status Header:** Standardized to `🧭 AIRO STATUS` with simple Indonesian terminology.
4. **Deterministic Validation:** Task verdict computed by `scripts/airo-task-verdict` based strictly on required vs actual evidence.
5. **Project-Scoped Session Model:** 1 session = 1 project + 1 main objective. Checkpoints update the active session draft locally.
6. **Separate Pushes:** Project work push and session closeout push are separate.
7. **Obsidian Experience:** Same ASB repository opened directly in Obsidian with `HOME.md` cockpit.
8. **Selective Upstream Adoption:** Selective adoption from `obsidian-wiki`, `obsidian-skills`, `obsidian-second-brain`, and `Everything OpenAI Codex`.
9. **Component Status:** `airo-capture` kept/reused for M2; Runtime Sync kept DISABLED until repaired; Finance timer recorded as `RETIRE_CANDIDATE`.
10. **Milestones:** Exactly 7 canonical milestones (M0..M6). No ad-hoc roadmap gates allowed.

---

## 3. Canonical Pointers

- **PRD:** [docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/prd/AIRO_SECOND_BRAIN_PRD_v0.6.0.md)
- **Design Spec:** [docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/specs/asb/AIRO_SECOND_BRAIN_v0.6_DESIGN_SPEC.md)
- **Roadmap:** [docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md](file:///home/egitaristorandas/AI_WORKSPACES/airo-second-brain/docs/roadmap/AIRO_SECOND_BRAIN_v0.6_ROADMAP.md)
