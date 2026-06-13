' AIRO Earesmes — Telegram Listener VBS Launcher
' Runs WSL listener in background without showing a console window.
' Used by Windows Task Scheduler (AIRO Earesmes Telegram Listener).
' Safe: does not expose credentials. Does not block UI.

Option Explicit

Dim objShell
Dim strCommand
Dim strWslDistro
Dim strRepoDir
Dim strPythonScript
Dim strLogFile
Dim strTimestamp

Set objShell = CreateObject("WScript.Shell")

strWslDistro   = "Ubuntu"
strPythonScript = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain/ops/telegram/telegram-action-listener.py"
strLogFile     = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain/logs/telegram-listener.log"

' Run listener via WSL, hidden (0 = hide window), no wait (False = async)
strCommand = "wsl -d " & strWslDistro & " python3 " & strPythonScript

objShell.Run strCommand, 0, False

Set objShell = Nothing
