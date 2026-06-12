# AIRO SECOND BRAIN v0.4.1 RUNTIME ACCEPTANCE

This document defines the test procedures and possible acceptance statuses for the v0.4.1 Runtime Activation Addendum.

## Test Procedures
1. Ensure all 9 core scripts/files in `ops/runtime/`, `ops/notifications/`, and `ops/remote-queue/` exist.
2. Execute `--help`, `--dry-run`, and `--json` for runner, status, and queue scripts.
3. Validate anti-spam (no-op sync logs but doesn't notify).
4. Install Windows Task Scheduler task using `AIRO-SecondBrain-InstallTask.ps1`.
5. Verify `AIRO Finance` remains pristine (no dirty modifications from the runtime scripts).
6. Perform Secret Guard check to ensure no raw secrets are committed.

## Acceptance Result States
- `PASS`: Full success, including Task Scheduler installation and Telegram configuration.
- `PASS_WITH_TELEGRAM_LOG_ONLY`: Successful run, but Telegram is unconfigured or skipped (`telegram_status: log_only_unconfigured`).
- `PASS_WITH_INSTALL_BLOCKED`: Successful run, but Windows Task Scheduler installation was blocked due to permissions or policy.
- `BLOCKED`: Secret guard failed or another hard constraint violated.
- `FAIL`: Execution errors in the scripts.
