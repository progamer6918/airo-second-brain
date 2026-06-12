# AIRO-SecondBrain-UninstallTask.ps1
# Removes the AIRO Second Brain Runtime Sync from Windows Task Scheduler

$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $IsAdmin) {
    Write-Host "SCHEDULER_UNINSTALL=BLOCKED_PERMISSION"
    Write-Host "Reason: PowerShell is not elevated / Administrator permission required"
    exit 1
}

$TaskName = "AIRO Second Brain Runtime Sync"

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop | Out-Null
    Write-Host "SCHEDULER_UNINSTALL=PASS"
    exit 0
} catch {
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if (-not $Task) {
        Write-Host "SCHEDULER_UNINSTALL=PASS_ALREADY_REMOVED"
        exit 0
    }
    Write-Host "SCHEDULER_UNINSTALL=FAIL"
    Write-Host "Reason: $($_.Exception.Message)"
    exit 1
}
