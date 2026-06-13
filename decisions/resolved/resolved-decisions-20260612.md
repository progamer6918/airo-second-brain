# Resolved Decisions — 2026-06-12

The following decisions have been resolved and implemented as part of the operational baseline.

## accepted_runtime_baseline

### 1. Distillation automation trigger
- **Resolution**: Manual trigger first. Automation may suggest, not directly rewrite canonical files.
- **Implementation**: Completed in Phase 4/5. `airo-distill` generates proposals in `distill/proposals/` to await manual owner approval.

### 2. Concurrent consumer lock mechanism
- **Resolution**: Use append-only inbox files per consumer/session first. Avoid simultaneous edits to canonical files. Added lock files to prevent concurrent sync collisions.
- **Implementation**: File locks (`locks/airo-sync.lock` and `locks/airo-runtime.lock`) prevent parallel sync runner execution.

### 3. Hermes session-start hook
- **Resolution**: Add local startup routine that reads BOOT.md, CURRENT.md, CONTEXT.md, AGENTS.md, and SECURITY.md.
- **Implementation**: Integrated into WSL session entry procedures via `airo-bootstrap`.

### 4. Scheduled Task Hidden Launcher
- **Resolution**: Windows Task Scheduler executes `wscript.exe` with arguments pointing to `AIRO-SecondBrain-Sync.vbs` to execute the WSL runner windowlessly without flashes.
- **Implementation**: Implemented in `ops/runtime/` (InstallTask.ps1 and VBS launcher).

### 5. Telegram Notify Connection and Cooldown Policy
- **Resolution**: Configured local credentials via `/home/egitaristorandas/.airo/telegram.env` and implemented throttling rules (3600s for degraded warnings, 21600s for online/liveness and review notices) to prevent no-op sync spam.
- **Implementation**: Implemented in `ops/notifications/telegram-notify.sh` and integrated into the runner.
