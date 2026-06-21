# Airo Personal Workflow Decision Log

## Decision 1: Use Full Database + Google Workspace as Output

Chosen architecture:
- SQLite is the local source of truth.
- Google Workspace is used as output and review layer.

Reason:
- SQLite gives reliable local memory and query capability.
- Google Sheets remains human-readable.
- Google Docs can receive monthly reports.
- Google Drive can store receipts and attachments.
- Google Calendar can later receive due-date reminders.

## Decision 2: Google Workspace Must Start as Dry-Run

Reason:
- Avoid OAuth/token risk during early development.
- Validate exports and reports before real API write.
- Keep the system safe for full free-tier usage.

## Decision 3: No Hard Delete for Finance Data

Finance records should use soft delete instead of hard delete.

Reason:
- Prevent accidental loss.
- Preserve auditability.
- Make rollback possible.

## Decision 4: Telegram is the Primary Interface

Telegram is used as the daily command interface.

Reason:
- Fast command input.
- Easy mobile access.
- Natural fit for short personal workflow commands.

## Decision 5: Airo, EarnsAI, Vortex Skill Lab, and Bubu Stay Separated

Project roles:
- Airo/OpenClaw: personal PC and workflow assistant.
- Vortex AI Skill Lab: skill library and architecture documentation.
- EarnsAI Pulse Trading: paper-only trading system, not touched by this workflow.
- Bubu the Receptionist: receptionist/capture assistant, not full PC executor.

## Decision 6: Full Free-Tier Constraint

The architecture prioritizes:
- local SQLite
- local exports
- dry-run Google plans
- optional free-tier Google API later
- no paid database dependency
- no heavy local model requirement
