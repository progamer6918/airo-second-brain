# AIRO Second Brain Runtime

This directory contains the operational runtime scripts for AIRO Second Brain.

## Architecture

- **Scheduler Boundary**: The primary scheduler for this runtime is the native OS scheduler (e.g., **Windows Task Scheduler**, `cron`, or `systemd`). The AI assistant Earesmes (or others) acts only as a notifier and a manual trigger, not as the primary continuous loop.
- **Entrypoint**: `airo-runtime-runner.sh` serves as the single unified entrypoint for syncs, health checks, queue processing, and notifications.
- **Windows Integration**: 
  - `AIRO-SecondBrain-Sync.ps1`: The target script for Task Scheduler.
  - `AIRO-SecondBrain-InstallTask.ps1`: Automated installer to register the task (runs every 5 minutes and at logon).
  - `AIRO-SecondBrain-UninstallTask.ps1`: Automated uninstaller.

## Usage

To manually trigger a runtime cycle:
```bash
./airo-runtime-runner.sh
```

To view the runtime status:
```bash
./airo-runtime-status.sh
```
