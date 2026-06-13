# AIRO Manual Sync Queue Policy

`inbox/manual-sync-queue.md` is staging, not canonical. Operator AIRO Sync / Antigravity must follow this lifecycle policy.

## Lifecycle States

- **PENDING**: Staged capture that has not been processed.
- **SUMMARIZED**: A short, operator-friendly summary has been generated.
- **OWNER_ACTION_REQUESTED**: Action card sent to owner on Telegram.
- **OWNER_APPROVED_ACTION**: Owner has clicked approval in Telegram.
- **PROCESSING**: The operator is currently executing the promotion/processing action.
- **CANONICALIZED**: Content has been written to canonical project files.
- **READBACK_VERIFIED**: The changes have passed canonical verification / readback.
- **PROCESSED**: The staged block has been marked as resolved.
- **ARCHIVED**: Staged block is moved to the archives.
- **QUEUE_COMPACTED**: Staging file has been cleaned of processed entries.
- **PUSHED**: Changes have been pushed to origin main.

Other valid states:
- **DEFERRED**: Deferred project backlog.
- **ARCHIVED_OBSOLETE**: Obsolete capture archived.
- **BLOCKED_NEEDS_OWNER**: Blocked due to unresolved business choices.
- **BLOCKED_CONFLICT**: Blocked due to merge conflicts.
- **BLOCKED_SECRET**: Blocked by secret guard.

## Core Rules

1. **Staging Status Only**: `inbox/manual-sync-queue.md` is a temporary staging file. Do not trust or promote blocks unless requested by the owner or approved via Telegram actions.
2. **Latest Detection**: The latest capture is defined as the last valid heading matching `## YYYY-MM-DD — ...` at the bottom of the active queue.
3. **Archiving processed blocks**: Processed captures must move to `archive/manual-sync-queue/YYYY-MM-DD/<capture-id>.md`. Never delete capture history.
4. **Archiving deferred captures**: Deferred captures must move to `inbox/deferred/` or `decisions/deferred/`.
5. **Compaction**: The active staging queue `inbox/manual-sync-queue.md` must be compacted after processing.
6. **Readback Safeguard**: Never mark a capture block as processed or archive it unless the canonical readback check passes.
