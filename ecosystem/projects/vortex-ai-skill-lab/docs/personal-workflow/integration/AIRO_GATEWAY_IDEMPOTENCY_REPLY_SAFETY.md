# AIRO Gateway Idempotency and Reply Safety

Status: patched.

## Root cause

Telegram/OpenClaw could write a transaction successfully and then return an error reply if the legacy persistence hook failed after the primary `record_from_text()` write.

The hook also wrote to the real DB during dry-run/temp-DB smoke tests and could overwrite the primary `persist_action`.

## Fix

- `record_transaction()` checks for an active semantic duplicate before insert.
- Repeated identical commands return `persist_action=skip_duplicate`.
- `local_handler.py` treats the legacy persistence hook as best-effort.
- The legacy hook is skipped for dry-run/temp DB runs and for duplicate replies.
- Legacy hook action is stored separately and no longer overwrites the primary `persist_action`.

## Validation

- Repeated `nabung 5000 ke blu` through `scripts/airo_personal_workflow_call.sh` creates one active temp DB row only.
- The real DB row count does not change during temp DB smoke.
- Live full-auto Sheets dry-run remains zero write candidates.
