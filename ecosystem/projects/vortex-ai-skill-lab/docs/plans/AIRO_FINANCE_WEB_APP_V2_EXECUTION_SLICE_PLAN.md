# AIRO Finance Web App V2 Execution Slice Plan

- **Status:** OWNER_APPROVED_PLAN
- **Date:** 2026-07-23
- **Estimates Note:** All time estimates are planning estimates, NOT SLA or delivery guarantees.

---

## 1. Executive Summary
This document outlines the phased vertical-slice execution plan for building and deploying AIRO Finance Web App V2. Each phase represents an independently deployable vertical slice from schema/contract through backend adapter, test harness, frontend UI, browser proof, and guarded deployment.

## 2. Phased Execution Roadmap

### Phase 0 — Canonicalization & Slice Roadmap (Current Gate)
- Scope: Public-safe documentation of Web App V2 direction, PRD addendum, execution slice plan, prototype review, and AFPD update.
- Artifacts: PRD addendum, execution slice plan, prototype direction review, evidence summary/proof.
- Estimate: Docs-only gate.

### Phase 1 — Stabilize Current Web Dashboard MVP
- Scope: Deploy exact separate cash matching (`CASH_UMUM`, `CASH_BENSIN`), Top Subcategory rendering, split Month/Year filters, production browser proof, followed by guarded Cash Makan registry insertion.
- Constraints: No `Cash` tombstone row insertion.
- Estimate: 1–3 focused workdays (NOT_SLA).

### Phase 2 — Web App V2 Shell
- Scope: Build responsive layout shell covering 4 core stable domains (Ringkasan, Pengeluaran, Akun & Saldo, Data Quality), mobile bottom navigation, desktop sidebar, loading/error/empty state handling, safe DOM rendering, request sequencing, Category and Subcategory previous-period comparison UI.
- Estimate: 2–4 focused workdays (NOT_SLA).

### Phase 3 — Domain Adapter Foundation
- Scope: Implement backend RPC boundary (`getDashboardOverviewSnapshot` and `getDashboardDomainSnapshot`), domain adapter contract, lazy-loading handler, common domain error/empty states. No canonical calculations in frontend.
- Estimate: 2–4 focused workdays (NOT_SLA).

### Phase 4 — Cicilan Rumah Vertical Slice (First Complex Domain)
- Scope: Schema audit for `Cicilan Rumah` tab, data contract, backend adapter, unit/integration tests, domain UI view, browser proof, guarded deployment.
- Estimate: 3–5 focused workdays (NOT_SLA).

### Phase 5 — Credit Card Vertical Slice
- Scope: `Credit Card` tab schema audit, contract, backend adapter, tests, frontend UI view, browser proof, guarded deployment.
- Estimate: 3–5 focused workdays (NOT_SLA).

### Phase 6 — Hutang Vertical Slice
- Scope: `Hutang` tab schema audit, contract, backend adapter, tests, frontend UI view, browser proof, guarded deployment.
- Estimate: 2–4 focused workdays (NOT_SLA).

### Phase 7 — Aset / Emas Vertical Slice
- Scope: `Aset` (Emas & future assets) tab schema audit, contract, backend adapter, tests, frontend UI view, browser proof, guarded deployment.
- Estimate: 2–4 focused workdays (NOT_SLA).

### Phase 8 — Unified Activity & Final Hardening
- Scope: Unified `Aktivitas` log view, cross-domain navigation polish, error boundary hardening, production readback verification.
- Estimate: 2–3 focused workdays (NOT_SLA).

## 3. Total Planning Range Summary
- **MVP+ Base Structure (Phases 0–2):** 5–8 focused workdays.
- **Through First Complex Domain (Phase 4):** 10–17 focused workdays.
- **Full Prototype Structure (Phases 0–8):** 18–30 focused workdays.
- **Calendar Expectation:** Approximately 5–8 calendar weeks accounting for reviews, limits, and debugging.
- **Planning Disclaimer:** These estimates are planning targets, NOT SLA or guaranteed delivery dates.

## 4. Anti-Freeze Execution Rules
1. One gate has one primary product deliverable.
2. No multi-domain mega gates.
3. Maximum 1–2 focused workdays without a visible artifact.
4. Visible artifacts: approved contract, candidate UI, working RPC, test proof, browser proof, deployment.
5. Same root error twice: stop, classify, do not randomly switch access methods.
6. Investigation exceeding ~2 hours: stop execution, create bounded forensic gate.
7. Each domain is an independently deployable vertical slice.
8. Production remains live while candidate work happens separately.
9. Do not combine workbook repair, backend contract, multi-domain UI, deployment, and unrelated AFPD repair in one gate.
10. No runtime PASS claim from static proof alone.
11. No deployment without clean repo, exact source hash, test PASS, owner visual acceptance where required, rollback version, and deployment readback.
12. Web App remains strictly read-only.

## 5. Next Immediate Gate
`AIRO_FINANCE_WEB_DASHBOARD_SEPARATE_CASH_ACCOUNTS_AND_TOP_SUBCATEGORY_GUARDED_DEPLOYMENT_PREFLIGHT_NO_DEPLOY`
