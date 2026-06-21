# AIRO Finance Sprint 6 - Dashboard Final Start

Status: Sprint 6 official start.

This is not a new architecture.
This follows AIRO Finance Final Kitab.

## Entry Condition

Sprint 5 core has live pass:

    admin audit sprint5 reconciliation

Live result:
- Mode: read-only
- Write performed: false
- Data Status: Warning
- Active issues: 24
- Legacy issues: 98
- Critical: 0
- Warnings: 25
- Action Required emitted

Decision:
- Sprint 5 core is sufficient for Dashboard Final start.
- Optional cutover-aware hardening is not a blocker.
- Sprint 6 can start using Data Status Warning.

## Official Sprint 6 Scope

Dashboard Final must include:

    Topbar
    Action Required
    Executive Command Center
    Wallet & Cashflow
    Domain Health
    Spending Intelligence
    Data Quality Center
    Smart Insight Panel
    Period selector
    Last synced
    Data Status
    Metric source-of-truth
    home_value_mode
    Conditional Email Ingestion Status hidden by default

## Dashboard Target Rule

Final official target:

    existing Dashboard tab

Allowed during build:

    staging tab only if needed

Forbidden:

    permanent second dashboard
    dashboard source-of-truth rewrite
    Cash Ledger dependency
    Transactions master
    Email panel placeholder while email_ingestion_enabled = false

## Source-of-Truth Contract

    Cash tersedia          -> Account Ledger
    Wallet balances        -> Account Ledger
    Inflow/outflow         -> Account Ledger
    Internal transfer      -> Account Ledger linked transfer rows
    CC outstanding         -> Credit Card
    Total hutang           -> Hutang
    Aset emas              -> Aset
    Cicilan progress       -> Cicilan Rumah
    Spending category      -> Finance Events clean category
    Pending category       -> Finance Events / quality status
    Pending clarification  -> pending state + Review Queue
    Data Status            -> Reconciliation + Data Quality rules
    Audit count            -> _AIRO_Audit_Log
    Net worth              -> home_value_mode formula
    Email health           -> hidden unless email_ingestion_enabled = true

## Sprint 6 Dashboard Sections

### 1. Topbar

Must show:
- Synced timestamp
- Data Status
- Alert count
- Period selector
- Mode: Personal Finance

### 2. Action Required

Must show max 4-6 real actionable items:
- Critical first
- Warning second
- Action label required
- Not passive insight

### 3. Executive Command Center

Primary:
- Net Worth
- Cash Tersedia
- Cashflow Bulan Ini
- Critical Alerts

Secondary:
- Total Aset
- Total Hutang
- Saving Rate
- Cicilan Rumah Progress

### 4. Wallet & Cashflow

Must read Account Ledger.
Must not read Cash Ledger.
Internal transfer must not inflate income/expense.

### 5. Domain Health

Sources:
- Credit Card
- Hutang
- Aset
- Cicilan Rumah

Badges:
- Clean
- Monitor
- Warning
- Critical

### 6. Spending Intelligence

Source:
- Finance Events with clean category

Rules:
- Missing category excluded from clean category breakdown
- Missing category appears as Pending Category / Warning

### 7. Data Quality Center

Sources:
- Review Queue
- Finance Events
- Audit Log
- Reconciliation
- Pending Clarification
- Email Ingestion Log only if enabled

Must control Topbar Data Status.

### 8. Smart Insight Panel

Interpretation only.
Action Required remains the to-do list.

### 9. Conditional Email Ingestion Status

Hidden in Sprint 6 because email_ingestion_enabled is false.

## Definition of Done

Dashboard Final is done only if:

    Dashboard reads correct source-of-truth.
    Dashboard does not read Cash Ledger.
    Missing category creates Warning.
    Unclean data is excluded from clean category.
    Data Status affects trust.
    Action Required contains real to-dos.
    Net worth does not double count.
    Dashboard is aesthetic, disciplined, advanced, and actionable.
    Email Ingestion Status hidden if email_ingestion_enabled = false.

## Next Implementation Step

Patch Apps Script with a Sprint 6 Dashboard Final builder in controlled mode.

The first implementation patch must:
- inspect existing Dashboard tab names
- avoid permanent second dashboard unless staging is explicitly used
- write source-of-truth formulas only
- include Data Status block
- include Action Required block
- keep Email Ingestion hidden
- not delete existing sheet data without backup
