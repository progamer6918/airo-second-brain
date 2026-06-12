# AIRO-SecondBrain-InstallTask.ps1
# Installs the AIRO Second Brain Runtime Sync in Windows Task Scheduler

$TaskName = "AIRO Second Brain Runtime Sync"
$Action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "-d Ubuntu bash -c `"cd /home/egitaristorandas/AI_WORKSPACES/airo-second-brain && ./ops/runtime/airo-runtime-runner.sh`""

$Trigger1 = New-ScheduledTaskTrigger -AtLogon
$Trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -DontStopOnIdleEnd -Hidden

try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($Trigger1, $Trigger2) -Principal $Principal -Settings $Settings -Force
    Write-Host "Successfully registered Task: $TaskName"
} catch {
    Write-Host "Failed to register Task. Permission denied or policy blocked."
    Write-Host $_.Exception.Message
}
