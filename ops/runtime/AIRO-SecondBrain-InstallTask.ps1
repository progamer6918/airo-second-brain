# AIRO-SecondBrain-InstallTask.ps1
# Installs the AIRO Second Brain Runtime Sync in Windows Task Scheduler

$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $IsAdmin) {
    Write-Host "SCHEDULER_INSTALL=BLOCKED_PERMISSION"
    Write-Host "Reason: PowerShell is not elevated / Administrator permission required"
    exit 1
}

$TaskName = "AIRO Second Brain Runtime Sync"
$SyncScriptPath = Join-Path $PSScriptRoot "AIRO-SecondBrain-Sync.ps1"
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$SyncScriptPath`""

$Trigger1 = New-ScheduledTaskTrigger -AtLogon
$Trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -DontStopOnIdleEnd -Hidden

try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($Trigger1, $Trigger2) -Principal $Principal -Settings $Settings -Force | Out-Null
} catch {
    Write-Host "SCHEDULER_INSTALL=FAIL"
    Write-Host "Reason: $($_.Exception.Message)"
    exit 1
}

$Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($Task) {
    Write-Host "SCHEDULER_INSTALL=PASS"
    Write-Host "TaskName=$TaskName"
    Write-Host "State=$($Task.State)"
    exit 0
} else {
    Write-Host "SCHEDULER_INSTALL=FAIL_VERIFY_NOT_FOUND"
    exit 1
}
