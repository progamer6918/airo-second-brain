---
project_id: AIRO_FINANCE_LAB
project_name: AIRO Finance Lab
status: ACTIVE_DESIGN_FOUNDATION
current_milestone: M0
aliases:
  - AIRO Finance Lab
  - Finance Lab
  - finance-lab
---

# 🧪 AIRO Finance Lab (Clean-Slate Personal Finance)

**Status**: Aktif (ACTIVE_DESIGN_FOUNDATION)  
**Parent System**: AIRO Ecosystem  
**Tujuan Utama**: Membangun personal finance tracking yang ultra-ringan, minim friksi, dan membuktikan daily value sebelum otomasi, kebal terhadap pola kegagalan EAB.

---

## 🧭 Dokumen Fondasi (Canonical Specs)

- 📄 **MVP PRD V1 (LOCKED)**: [[ecosystem/projects/airo-finance-lab/docs/AIRO_FINANCE_LAB_MVP_PRD_V1.md|AIRO Finance Lab MVP PRD V1]] — Personal Finance Intelligence App identity, 3 daily workflows, strictly locked MVP scope.
- 🏛️ **MVP Architecture V1 (LOCKED)**: [[ecosystem/projects/airo-finance-lab/docs/AIRO_FINANCE_LAB_MVP_ARCHITECTURE_V1.md|MVP Architecture V1]] — Unidirectional data flow, strictly 5 tables (accounts, transactions, categories, budgets, audit_logs), decoupled boundaries.
- 🛡️ **Execution Rules V1 (LOCKED)**: [[ecosystem/projects/airo-finance-lab/docs/AIRO_FINANCE_LAB_EXECUTION_RULES_V1.md|Execution Rules V1]] — Anti-EAB guardrails, small reversible steps, 7-day manual rule, zero AI ledger write access.
- 🗄️ **Schema Decision V1**: [[ecosystem/projects/airo-finance-lab/docs/AIRO_FINANCE_LAB_DATABASE_SCHEMA_DECISION_V1.md|Database Schema Decision V1]] — Supabase PostgreSQL trade-off analysis, migration mapping from legacy sheets.
- 🗺️ **Implementation Plan V1**: [[ecosystem/projects/airo-finance-lab/docs/AIRO_FINANCE_LAB_IMPLEMENTATION_PLAN_V1.md|Implementation Plan V1]] — 5-phase linear roadmap (M1 Foundation, M2 Dashboard, M3 Capture, M4 Hermes, M5 Automation).

---

## 📈 Roadmap & Milestone Ringkas

- **M0**: Architecture & Contracts (PRD, ADR, Rules) — DONE
- **M1**: Core Local Parser & Append-Only Ledger Engine — PLANNED
- **M2**: Standalone Telegram Bot Pilot — PLANNED
- **M3**: 7-Day Live Owner Value Proof — PLANNED
- **M4**: Lightweight Reporting & Balance Queries — PLANNED
- **Phase 2**: Optional Automations & Sync (Hanya setelah M3+M4 PASS)

---

⬅️ [[control/_index|Kembali ke Project Index]]
