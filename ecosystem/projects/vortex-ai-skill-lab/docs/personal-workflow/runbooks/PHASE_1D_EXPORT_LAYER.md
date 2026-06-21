# Phase 1D Export Layer

## Goal

Prepare Google Workspace output without using OAuth yet.

## Added

- CSV export for transactions
- CSV export for installment payments
- JSON export for monthly summary
- Markdown monthly report
- CLI commands:
  - `export`
  - `report`

## Safety

No token, no OAuth, no Drive access, no Gmail access, no Calendar write.

## Test

```bash
python3 -m airo_personal_workflow.cli export --period 2026-05
python3 -m airo_personal_workflow.cli report --period 2026-05
python3 scripts/personal_workflow_export_smoke.py
