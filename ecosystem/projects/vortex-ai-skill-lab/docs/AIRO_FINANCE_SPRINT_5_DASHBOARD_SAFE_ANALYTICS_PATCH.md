# AIRO Finance Sprint 5 - Dashboard-Safe Reconciliation Analytics Patch

Status: Sprint 5 active patch.

This patch extends the read-only reconciliation helper with dashboard-safe analytics fields.

## Purpose

The raw reconciliation audit currently reports needs_review and issue_count 98.

The dashboard must not blindly treat all old Account Ledger gaps as Dirty, because AIRO uses cutover-forward model.

This patch converts raw audit output into:

    data_status
    dashboard_status
    data_status_reason
    dashboard_analytics
    issue_breakdown
    issue_count_active
    issue_count_legacy
    critical_count
    warning_count
    action_required

## Data Status Rule

Trusted:
- no active warning
- no active critical
- no legacy issue

Warning:
- legacy-only issue exists
- Lainnya category rows exist
- needs_review exists but active critical count is zero

Dirty:
- Finance Event without expected Account row
- Finance Event failed/error row
- partial_failed row
- active post-cutover broken lineage

## Current Expected Result

Based on current audit:

    Account Ledger rows: 61
    Missing linked_txn_id: 37
    Lainnya category rows: 24
    Finance Events rows: 10
    Account without Finance Event: 61
    Finance Event without Account: 0
    Status: needs_review
    Issue count: 98

Expected dashboard-safe status:

    Data Status: Warning

Reason:
- active critical count should be zero
- legacy/pre-cutover lineage needs classification
- Lainnya category needs review
- dashboard should not claim Trusted yet

## Dashboard Rule

This is not Sprint 6 repaint.

This patch only makes Sprint 5 reconciliation output consumable by Dashboard Final later.

Existing Dashboard remains official target.
Staging dashboard is only allowed later if needed in Sprint 6.

## Definition of Done

- read-only helper emits dashboard_analytics
- Telegram reply shows Dashboard Analytics section
- no Spreadsheet write is added
- tests pass
- Apps Script V2 deploys cleanly
- next live audit shows Data Status and Action Required
