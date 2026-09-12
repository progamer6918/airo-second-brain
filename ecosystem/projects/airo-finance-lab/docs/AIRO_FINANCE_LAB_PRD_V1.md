# AIRO Finance Lab — Product Requirements Document (PRD) v1.0

- **Project**: `AIRO_FINANCE_LAB`
- **Document Version**: `1.0.0`
- **Status**: `DRAFT_DESIGN_ONLY`
- **Date**: `2026-09-11`
- **Authority**: Owner-Guided (`TASK=AIRO_FINANCE_LAB_DOCUMENTATION_PHASE_V1`)
- **Governing Principles**: Anti-EAB Pattern Prevention (Zero Scope Creep, Forgiving Workflow, Daily Value First, Clean Decoupled Architecture)

---

## 1. Executive Summary & Problem Statement

### 1.1 Context & Background
Personal finance tracking within the AIRO ecosystem previously relied on **AIRO Finance (Legacy Arfin)** and the **Earesmes-Arfin Bridge (EAB)**. 
- **Legacy Arfin** became a massive monolithic Google Apps Script (>15,000 lines) with complex multi-tab spreadsheet dependencies, rigid multi-turn clarification questions, and opaque Google edge container caching.
- **EAB** attempted to bridge conversational agents to Arfin before the foundational manual flow was rock-solid, resulting in over-scoped milestones, rigid state machines, and ultimately an incomplete implementation (`CLOSED_INCOMPLETE_PARTIAL_IMPLEMENTATION`).

### 1.2 The Core Problem
The Owner requires a frictionless, ultra-fast way to record daily transactions and track balances without:
1. Being trapped in rigid multi-question conversation trees (e.g. asking direction -> account -> category -> subcategory for a simple coffee purchase).
2. Dealing with fragile multi-bot bridges or edge runtime deployment delays.
3. Complex multi-tab formula maintenance where a single cell shift breaks dashboard synchronization.

### 1.3 Vision of AIRO Finance Lab
AIRO Finance Lab is an intentional "clean-slate laboratory" designed to engineer a **lightweight, reliable, daily-delightful personal finance system**. It prioritizes **immediate daily friction reduction** over grand automated architectures.

---

## 2. Core Design Principles (Anti-EAB Safeguards)

| Principle | Anti-Pattern Avoided (EAB Trap) | AIRO Finance Lab Standard |
|---|---|---|
| **1. Daily Value First** | Automating pipelines before verifying whether the daily manual input works. | The core single-turn entry (`catat ...`) must be used and loved daily by the Owner *before* any background automation or sync bridges are introduced. |
| **2. Forgiving Interaction** | Rigid finite state machines where typing "1" or out-of-order text gets trapped in legacy loops. | Single-turn atomic parsing. Sensible defaults applied with easy 1-tap undo/override. Never trap the user in a dead-end state machine. |
| **3. Ultra-Lean Scope Firewall** | Scope explosion (trying to support multi-bot routing, HMAC auth, multi-account transfers, and budget dashboards in MVP). | Strict MVP: Single-line expense/income logging and quick balance check. All other features are barred until MVP achieves 7 consecutive days of friction-free Owner use. |
| **4. Decoupled Architecture** | Entangled code where webhook handlers, business logic, formatting, and database writes live in one script. | Clean boundary separation: Interface (Telegram) $\leftrightarrow$ Business Engine (Python Service) $\leftrightarrow$ Storage (Append-only Ledger). |

---

## 3. Product Scope & Boundaries

### 3.1 In-Scope (Phase 1 MVP — "The 5-Second Logger")
1. **Single-Turn Natural Language Logging**:
   - Parse single-line natural inputs:
     - `makan siang 35k bca` $\rightarrow$ Amount: 35.000, Category: Makanan, Account: BCA.
     - `kopi 20k` $\rightarrow$ Amount: 20.000, Category: Kopi/Snack, Account: [Default Wallet].
     - `gaji 15jt bca` $\rightarrow$ Amount: 15.000.000, Direction: Income, Account: BCA.
2. **Instant Receipt & 1-Tap Confirmation / Undo**:
   - Bot responds immediately with a concise structured receipt.
   - Includes quick buttons or keyword: `[Batal / Undo]` and `[Ubah]`.
3. **Smart Heuristic Matching with Default Fallbacks**:
   - Known keywords map automatically to categories and wallets based on a local configuration dictionary.
   - If wallet or category is ambiguous, apply sane default (e.g., Default Wallet = Cash/BCA) and note it clearly in receipt.
4. **Append-Only Transaction Ledger**:
   - Clean, immutable record containing: `timestamp`, `amount`, `direction`, `category`, `account`, `note`, `raw_text`.
5. **Quick Balance & Spending Query**:
   - `saldo` $\rightarrow$ Lists current balance per active account.
   - `pengeluaran hari ini` / `pengeluaran bulan ini` $\rightarrow$ Compact summary of spending.

### 3.2 Explicitly Out-of-Scope (Deferred to Phase 2+)
- ❌ Automated Gmail / notification bank scrapers.
- ❌ Cross-bot bridges (No Hermes/Earesmes proxying until standalone bot is proven).
- ❌ Multi-currency or gold/investment valuation engine.
- ❌ Complex debt / mortgage amortization engines (e.g. Cicilan Rumah).
- ❌ Bidirectional spreadsheet dashboards with live formula evaluations.
- ❌ Automated recurring scheduling triggers.

---

## 4. User Journeys & Interaction Specifications

### Journey 1: Standard Expense Log (High Confidence)
```text
User: makan padang 28k bca
Bot:  ✅ Tercatat: Pengeluaran
      💰 Rp28.000 | 🏷️ Makanan | 🏦 BCA
      📝 Catatan: makan padang
      [Batal (1-Klik)]
```

### Journey 2: Log with Missing Details (Forgiving Default)
```text
User: bensin 50rb
Bot:  ✅ Tercatat: Pengeluaran
      💰 Rp50.000 | 🏷️ Transportasi | 🏦 Cash (Default)
      📝 Catatan: bensin
      Ketik 'bca' untuk ubah rekening, atau tekan [Batal].
```

### Journey 3: Quick Status & Balance Query
```text
User: saldo
Bot:  🏦 Saldo Terakhir:
      • BCA: Rp4.250.000
      • Blu: Rp1.120.000
      • Cash: Rp350.000
      Total Likuid: Rp5.720.000
```

### Journey 4: Cancellation / Undo
```text
User: [Batal] atau ketik 'batal'
Bot:  🗑️ Transaksi terakhir (Rp50.000 - bensin) telah dibatalkan.
```

---

## 5. Acceptance Criteria & Definition of Done (DoD)

### Milestone M1: Core Natural Parser & Storage Validation
- [ ] Natural language parser handles 20 benchmark test cases (Indonesian slang, k/rb suffixes, missing accounts).
- [ ] Append-only ledger correctly records validated transactions with cryptographic or monotonic row IDs.
- [ ] 1-Tap Undo reliably marks transactions as voided without corrupting ledger history.

### Milestone M2: Standalone Telegram Pilot
- [ ] Dedicated Telegram bot instance responds in $<2$ seconds.
- [ ] Zero state deadlocks: Any unexpected text or `/start` or `/cancel` resets context safely.
- [ ] Zero foreign message contamination (Compliant with Telegram Agent Identity Contract).

### Milestone M3: 7-Day Live Owner Value Proof (Mandatory Gate)
- [ ] Owner logs real personal transactions for 7 consecutive days.
- [ ] $<5\%$ clarification prompt rate for regular daily expenses.
- [ ] Explicit Owner statement: `DAILY_VALUE_PROVEN=PASS`.
- [ ] Only after M3 PASS may Phase 2 (automation / advanced reporting) be planned.

---

## 6. Kill Criteria & Risk Containment

1. **Parser Frustration Rule**: If the parser requires $>2$ clarifications on standard daily inputs, the natural language approach must be halted and replaced with strict micro-syntax or rapid interactive buttons.
2. **Runtime Invalidation Rule**: If any dependency (cloud provider, edge script, API) causes silent caching or unverified state updates, that platform component must be decommissioned immediately.
3. **Single Retest Failure Rule**: During development, any bug may only undergo ONE causal repair cycle. If the second test fails, execution halts for architecture review.
