# ASB Human Navigation Contract

**Status**: CANONICAL_CONTRACT
**Date**: 2026-08-10
**Authority**: OWNER_APPROVED_V1_PRODUCTIZATION

---

## 🧭 Rules of Human Navigation

1. **Intent-First Design**: Human users start from intent ("Mau ngapain?"), not filesystem structures.
2. **Canonical Front Door**: `HOME.md` is the single canonical human launchpad for AIRO Second Brain.
3. **Strict Hierarchy**:
   - `AIRO Home` is Level 0.
   - `AIRO WorkDesk` & `AIRO Finance` are Level 1 worlds.
   - `D-READY` is explicitly a Level 2 child of `AIRO WorkDesk` (`AIRO → WorkDesk → D-READY`).
4. **No Peer Elevation**: Child projects (like D-READY) MUST NOT be elevated to top-level peers of WorkDesk.
5. **Human Projections**: "Lanjut Kerja", "Aktivitas Terakhir", and "Riwayat Kerja" are human-friendly projections of underlying canonical Session/worklog truth.
6. **Technical Plumbing Isolation**: Raw Session UUIDs, Git hashes, evidence paths, and governance jargon are hidden from primary human viewports into collapsed `<details>` sections.
7. **Obsidian Compatibility**: All primary human pages MUST use clean Markdown wikilinks and standard frontmatter `aliases` for Quick Switcher discoverability without requiring third-party plugins.
8. **Breadcrumb Standard**:
   - WorkDesk: `🏠 AIRO → 💼 WorkDesk`
   - D-READY: `🏠 AIRO → 💼 WorkDesk → D-READY`
   - All Areas: `🏠 AIRO → 🗂 Semua Area & Project`
