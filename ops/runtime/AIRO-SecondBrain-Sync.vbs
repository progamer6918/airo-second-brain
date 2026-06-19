Set WshShell = CreateObject("WScript.Shell")
exitCode = WshShell.Run("wsl.exe -d Ubuntu bash -c ""cd /home/egitaristorandas/AI_WORKSPACES/airo-second-brain && ./ops/runtime/airo-runtime-runner.sh""", 0, True)
WScript.Quit exitCode
