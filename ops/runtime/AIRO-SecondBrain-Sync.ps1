# AIRO-SecondBrain-Sync.ps1
# This script bridges the Windows environment to the WSL runtime runner.
# It acts as the scheduled action for the Windows Task Scheduler.

wsl.exe -d Ubuntu bash -c "cd /home/egitaristorandas/AI_WORKSPACES/airo-second-brain && ./ops/runtime/airo-runtime-runner.sh"
