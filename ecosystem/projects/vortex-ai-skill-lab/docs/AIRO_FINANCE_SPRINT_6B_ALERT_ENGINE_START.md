# AIRO Finance Sprint 6B - Alert Engine Start

Status: Sprint 6B official start.

## Entry Condition

Sprint 6 Dashboard Final live pass is recorded.

Sprint 6B starts with a read-only alert engine planner.

## Scope

Sprint 6B Alert Engine v1 covers:

- Credit Card due alert
- Data Status Dirty alert
- Partial write failure alert
- Pending clarification timeout alert
- Cash threshold alert
- Cooldown foundation
- ACK foundation

## Admin Commands

    admin alert sprint6b plan
    admin alerts sprint6b plan
    admin sprint6b alert plan
    admin sprint6b alerts plan
    admin alerts sprint6b dryrun

## Safety

The planner must be read-only.

Expected:
- write_performed: false
- google_write_performed: false
- proactive_send_performed: false
- trigger_created: false

## Current Behavior

The planner reads:
- Sprint 5 reconciliation dashboard analytics
- Dashboard/source tab status
- Credit Card source availability
- Review Queue source availability
- Account Ledger source availability
- Finance Events source availability
- _AIRO_Audit_Log availability

It generates alert candidates but does not send proactive alerts.

## Next

After live dry-run plan passes:

- implement scheduled alert runner
- implement cooldown storage
- implement ACK command
- install trigger only after runner live test passes
