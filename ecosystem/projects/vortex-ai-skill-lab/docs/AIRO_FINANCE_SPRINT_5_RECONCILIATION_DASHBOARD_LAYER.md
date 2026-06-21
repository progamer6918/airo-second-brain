# AIRO Finance Sprint 5 - Reconciliation Dashboard Layer

Status: Sprint 5 active contract.

This layer converts raw reconciliation audit output into dashboard-safe trust signals.
It does not repaint the final dashboard yet.

## Current Verified State

Latest verified audit:

    Account Ledger rows: 61
    Missing linked_txn_id: 37
    Missing source_tab: 0
    Duplicate linked_txn_id candidates: 0
    Lainnya category rows: 24

    Finance Events rows: 10
    transaction_created: 0
    Missing linked_txn_id: 0
    Missing source_tab: 0
    Failed/error rows: 0

    Account without Finance Event: 61
    Finance Event without Account: 0
    Status: needs_review
    Issue count: 98

## Decision

The audit command is live and read-only.

The next Sprint 5 task is not dashboard repaint.
The next Sprint 5 task is to build the reconciliation dashboard layer.

## Required Output Layer

The dashboard analytics layer must expose:

    data_status
    data_status_reason
    issue_count_total
    issue_count_active
    issue_count_legacy
    critical_count
    warning_count
    action_required_count
    last_reconciled_at
    last_reconciliation_mode

## Data Status Mapping

### Trusted

    active critical count = 0
    active warning count = 0
    no post-cutover Account Ledger row missing Finance Event
    no Finance Event failed/error row
    no partial_failed event
    no duplicate critical candidate

### Warning

    legacy-only Account Ledger rows without Finance Event
    missing linked_txn_id on legacy rows
    Lainnya category rows
    missing category / needs_category
    unmatched CC payment
    pending clarification
    reconciliation helper status = needs_review but no active critical issue

### Dirty

    post-cutover Account Ledger row missing Finance Event
    Finance Event failed/error row
    partial_failed event
    broken refs after cutover
    OTP/security email parsed
    critical missing amount/account
    duplicate critical candidate
    dashboard primary formula error

## Cutover-Aware Rule

AIRO uses cutover-forward model.

Historical Account Ledger rows before Finance Events cutover must not automatically make dashboard Dirty.
They should be classified as legacy_warning unless they affect active/current metrics.

New rows after Finance Events cutover must have proper Finance Event lineage.

## Issue Classification

### Legacy Warning

    pre-cutover Account Ledger without Finance Event
    pre-cutover missing linked_txn_id
    old Lainnya category row
    old row without clean lineage

### Active Warning

    post-cutover missing category
    post-cutover Lainnya category
    pending clarification
    post-cutover non-critical ref warning

### Active Dirty

    post-cutover Account Ledger without Finance Event
    post-cutover Finance Event without expected Account row
    Finance Event failed/error
    partial_failed
    broken ref
    duplicate critical

## Action Required Mapping

Action Required must be generated from reconciliation output.

Examples:

    [WARNING] 24 rows kategori Lainnya perlu dikaji
    [WARNING] 37 legacy rows missing linked_txn_id, monitor only unless active period affected
    [WARNING] 61 Account Ledger rows without Finance Event detected, classify legacy vs post-cutover
    [CRITICAL] post-cutover row missing Finance Event
    [CRITICAL] partial_failed event needs retry/fix

## Dashboard Rule

Existing Dashboard remains the final official dashboard.

During Sprint 5:
- do not repaint final dashboard
- do not create permanent second dashboard
- build dashboard analytics source first
- staging tab is allowed later in Sprint 6 only if needed

## Definition of Done

    Reconciliation result can be converted to Trusted / Warning / Dirty.
    Legacy vs active issues are separated.
    Action Required can be generated from reconciliation result.
    Dashboard can show Data Status without lying.
    Sprint 6 Dashboard Final can safely consume this layer.

## Next Step After This Contract

Patch Apps Script read-only helper to emit dashboard-ready reconciliation analytics fields:

    dashboard_status
    dashboard_status_reason
    issue_breakdown
    legacy_issue_count
    active_issue_count
    critical_count
    warning_count
    action_required

No write/deploy until tests pass.
