# AIRO-SecondBrain-UninstallTask.ps1
# Removes the AIRO Second Brain Runtime Sync from Windows Task Scheduler

$TaskName = "AIRO Second Brain Runtime Sync"

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
    Write-Host "Successfully unregistered Task: $TaskName"
} catch {
    Write-Host "Task $TaskName not found or permission denied."
    Write-Host $_.Exception.Message
}
