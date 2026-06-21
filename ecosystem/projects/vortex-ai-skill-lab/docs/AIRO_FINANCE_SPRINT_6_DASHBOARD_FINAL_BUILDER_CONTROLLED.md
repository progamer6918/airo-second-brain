# AIRO Finance Sprint 6 - Dashboard Final Controlled Builder

Status: Sprint 6 controlled implementation.

## Purpose

This patch adds a dry-run admin route:

    admin dashboard sprint6 plan
    admin sprint6 plan
    admin sprint6 dryrun
    admin sprint6 dry-run

The route inspects the Dashboard Final plan without writing to Google Sheets.

## Safety

The route must return:

    write_performed: false
    google_write_performed: false
    mode: dry-run

It must not:
- clear Dashboard
- delete tabs
- create permanent second dashboard
- use Cash Ledger as a source
- show Email Ingestion Status while email_ingestion_enabled=false

## Official Target

    existing Dashboard tab

## Sections Included

- Topbar
- Action Required
- Executive Command Center
- Wallet & Cashflow
- Domain Health
- Spending Intelligence
- Data Quality Center
- Smart Insight Panel
- Period Selector
- Last Synced
- Data Status

## Source Contract

- Cash tersedia: Account Ledger
- Wallet balances: Account Ledger
- Inflow/outflow: Account Ledger
- Internal transfer: Account Ledger linked transfer rows
- CC outstanding: Credit Card
- Total hutang: Hutang
- Aset emas: Aset
- Cicilan progress: Cicilan Rumah
- Spending category: Finance Events clean category
- Pending category: Finance Events / quality status
- Data Status: Sprint 5 reconciliation dashboard analytics
- Audit count: _AIRO_Audit_Log
- Email health: hidden because email_ingestion_enabled=false

## Next

Run Telegram validation:

    admin dashboard sprint6 plan

Expected:
- Sprint 6 Dashboard Final plan reply
- Mode: dry-run
- Write performed: false
- Existing Dashboard detected
- Source Contract status listed
- Cash Ledger forbidden policy shown
