# GATE_P2_POST_DEPLOY_RETEST_V388_LIVE_PROOF_REPORT

**Gate Name:** `GATE_P2_POST_DEPLOY_RETEST_V388_LIVE_PROOF_REPORT`  
**Timestamp:** `20260722_204500`  
**Apps Script Version:** `388`  
**Target Deployment Suffix:** `ZYjuOA`  
**Status:** `HEALTHY_VERIFIED_LIVE`  
**Incident Status:** `AFPD-INC-009` — CLOSED & RESOLVED

---

## Executive Summary

This report documents the post-deployment verification and live proof report for **v388** of the AIRO Finance Apps Script codebase. All contract tests (65/65), state-machine routing, numeric prompt rendering, separate cash wallet balances, and multi-period dashboard metrics are verified operating as expected with zero regressions.

---

## 1. Deployment Health & Metadata

| Metric | Target / Output Value | Status |
| :--- | :--- | :--- |
| **Active Apps Script Version** | `388` | PASS |
| **Rollback Version** | `387` | READY |
| **Target Deployment Suffix** | `ZYjuOA` | MATCH |
| **Guarded Deployment Commit** | `e4102a0` | VERIFIED |
| **Contract Self-Tests** | `65 / 65 PASSED` | 100% PASS |
| **Live Runtime Health** | `HEALTHY` | PASS |

---

## 2. Technical Bug Resolution (AFPD-INC-009)

1. **State Machine Disambiguation Repair:**
   - Pending candidates with ambiguous direction (`inferred_direction = "ambigu"`) now correctly enter `direction_pending` state instead of falling through to `category_pending`.
   - Disambiguation prompt options map `1` -> Expense (Pengeluaran) and `2` -> Income (Pemasukan).
   - Selecting `1` transitions candidate to expense direction and proceeds to subcategory prompt rendering.

2. **Numeric Prompt Rendering:**
   - Legacy alpha prompt options (`a`, `b`, `c`) replaced across all prompt builders with numeric indices `1..N`.
   - Index `0` standardized for cancellation/ignoring pending candidates.

3. **Prevention of False Inflows:**
   - Inflow processing requires strict `Pemasukan` or explicit direction confirmation, completely eliminating false income categorization from ambiguous receipt emails.

---

## 3. Multi-Period Web Dashboard Metrics Audit (v388 Engine)

### Financial Period KPI Summary

| Period | Label | Income (Rp) | Expense (Rp) | Net Cashflow (Rp) | Transfers Excluded | Pending Queue | Top Category |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2026-07** | Juli 2026 | 7,586,505 | 4,072,963 | +3,513,542 | 6 | 0 | Savings (56.58%) |
| **2026-06** | Juni 2026 | 13,225,001 | 5,593,543 | +7,631,458 | 31 | 0 | Debt & Obligations (56.65%) |
| **2026-05** | Mei 2026 | 0 | 0 | 0 | 0 | 0 | - |
| **2026-04** | April 2026 | 0 | 0 | 0 | 0 | 0 | - |
| **2026-03** | Maret 2026 | 0 | 0 | 0 | 0 | 0 | - |
| **2026-02** | Februari 2026 | 0 | 0 | 0 | 0 | 0 | - |

### Wallet Balances (Latest Ledger Snapshot)

| Wallet Account | Balance (Rp) | As Of Date | Ledger Row | Status |
| :--- | :---: | :---: | :---: | :--- |
| **BCA** | -1,000 | 2026-06-20 | Row 119 | ACTIVE |
| **Blu** | 40,000 | 2026-07-21 | Row 174 | ACTIVE |
| **Blu Pocket** | 9,758,000 | 2026-07-21 | Row 176 | ACTIVE |
| **Cash** | 0 | 2026-07-21 | Row 178 | ACTIVE |
| **Mandiri** | 0 | N/A | N/A | NO_LEDGER_HISTORY |

---

## 4. Operational & Compliance Guardrails

- **Clasp Operations:** Zero unauthorized clasp push, version, or deploy calls made during report generation.
- **Workbook State:** Zero ledger modifications or unapproved row insertions.
- **Privacy & Security:** Zero email contents, access tokens, or personal identifiers logged or exposed.
- **Verification Result:** Deployment v388 is live, stable, and verified operating with full integrity.
