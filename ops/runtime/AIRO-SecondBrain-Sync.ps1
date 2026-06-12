# AIRO-SecondBrain-Sync.ps1
# This script bridges the Windows environment to the WSL runtime runner.
# Note: AIRO-SecondBrain-Sync.vbs is now preferred for completely silent background execution.

wsl.exe -d Ubuntu bash -c "cd /home/egitaristorandas/AI_WORKSPACES/airo-second-brain && ./ops/runtime/airo-runtime-runner.sh"
