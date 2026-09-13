# ASB Human Navigation Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-10
**Authority**: OWNER_APPROVED_UX_CORRECTION

---

## 🧭 Rules of Human Navigation

1. **Intent-First Design**: Human users start from intent ("Mau ngapain?"), not filesystem structures.
2. **Canonical Front Door**: `HOME.md` is the single canonical human launchpad for AIRO Second Brain.
3. **Strict Hierarchy**:
   - `AIRO Home` is Level 0.
   - `AIRO WorkDesk` & `AIRO Finance` are Level 1 worlds.
   - `D-READY` is explicitly a Level 2 child of `AIRO WorkDesk` (`AIRO → WorkDesk → D-READY`).
4. **No Peer Elevation**: Child projects (like D-READY) MUST NOT be elevated to top-level peers of WorkDesk.
5. **Knowledge Discovery Routing**: "Cari Tahu Sesuatu" MUST route to actual professional knowledge topics (`wiki/workdesk/KNOWLEDGE_MAP.md`), NOT architectural planning pages.
6. **No Continuity Duplication**: "Lanjut Kerja" MUST NOT duplicate the main WorkDesk entrypoint or show technical maintenance status. If no specific resumable work item exists, it must state so truthfully.
7. **Rich Work History**: Root Home embeds dynamic Obsidian Base `![[worklog/views/AIRO Worklog.base#Hari Ini]]`; `RIWAYAT_KERJA.md` exposes `Hari Ini`, `Sesi Terbaru`, and full `Riwayat Sesi`.
8. **Global Inventory**: `wiki/AREAS_AND_PROJECTS.md` is the global ASB inventory covering all systems, worlds, bridges, and child projects.
9. **Technical Plumbing Isolation**: Raw Session UUIDs, Git hashes, evidence paths, and governance jargon are hidden from primary human viewports into collapsed `<details>` sections.
10. **Obsidian Compatibility**: All primary human pages MUST use clean Markdown wikilinks and standard frontmatter `aliases` for Quick Switcher discoverability without requiring third-party plugins.

11. **Root Presentation Placement**: WorkDesk and AIRO Finance remain Level-1 worlds even when their entry links are visually grouped under root `Cari & Jelajah`.
12. **Acceptance Evidence**: Functional HOME acceptance may be established by verified backend evidence covering hierarchy, wikilinks, Base views, session/worklog continuity, vault/source parity, and regression tests. Pixel-level visual evidence is required only when visual appearance/render fidelity is an explicit acceptance objective.
