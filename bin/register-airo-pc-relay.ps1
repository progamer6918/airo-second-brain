# bin/register-airo-pc-relay.ps1 — Register and Launch AIRO PC Relay as a Windows Scheduled Task
$ErrorActionPreference = "Stop"

$TASK_NAME = "AIRO_PC_Relay"
$SCRIPT_PATH = "C:\Users\Admin\.gemini\antigravity\scratch\airo-second-brain\bin\airo-pc-relay-win.ps1"
$WORKING_DIR = "C:\Users\Admin\.gemini\antigravity\scratch\airo-second-brain"

Write-Host "=================================================="
Write-Host "Registering AIRO PC Relay Scheduled Task..."
Write-Host "=================================================="

# 1. Stop and remove existing task if present
try {
    $existing = Get-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Stopping and unregistering existing task '$TASK_NAME'..."
        Stop-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
        Unregister-ScheduledTask -TaskName $TASK_NAME -Confirm:$false
    }
} catch {
    Write-Host "Note: No previous task to remove."
}

# 2. Kill any old standalone powershell running airo-pc-relay-win.ps1
$pidFile = "$env:USERPROFILE\.local\state\airo-second-brain\pc-action-bridge\relay-win.pid"
if (Test-Path $pidFile) {
    try {
        $oldPid = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($oldPid -and (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
            Write-Host "Terminating previous relay process (PID: $oldPid)..."
            Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    } catch {}
}

# 3. Create Action & Settings
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$SCRIPT_PATH`"" `
    -WorkingDirectory $WORKING_DIR

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Days 3650) `
    -MultipleInstances IgnoreNew `
    -RestartCount 5 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

# 4. Register Scheduled Task
Write-Host "Registering scheduled task '$TASK_NAME'..."
Register-ScheduledTask -TaskName $TASK_NAME -Action $action -Settings $settings -Description "AIRO Hermes Native Windows PC Computer Use Relay Daemon" | Out-Null

# 5. Configure Windows Logon Autostart via HKCU Run registry
Write-Host "Configuring logon autostart in HKCU Run registry..."
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $regPath -Name $TASK_NAME -Value "schtasks.exe /run /tn `"$TASK_NAME`"" -Force

# Also add shortcut to Startup folder for redundancy
try {
    $startupFolder = [Environment]::GetFolderPath("Startup")
    $shortcutPath = Join-Path $startupFolder "AIRO_PC_Relay.lnk"
    $wsh = New-Object -ComObject WScript.Shell
    $shortcut = $wsh.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$SCRIPT_PATH`""
    $shortcut.WorkingDirectory = $WORKING_DIR
    $shortcut.WindowStyle = 7 # Minimized/Hidden
    $shortcut.Save()
    Write-Host "Startup shortcut created at $shortcutPath"
} catch {
    Write-Host "Startup shortcut creation skipped: $_"
}

# 6. Start the task immediately
Write-Host "Starting scheduled task '$TASK_NAME'..."
Start-ScheduledTask -TaskName $TASK_NAME
Start-Sleep -Seconds 2

# 7. Verify Task State
$task = Get-ScheduledTask -TaskName $TASK_NAME
Write-Host "=================================================="
Write-Host "Task Name: $($task.TaskName)"
Write-Host "State:     $($task.State)"
Write-Host "=================================================="

if ($task.State -eq "Running") {
    Write-Host "✅ AIRO PC Relay is successfully RUNNING as an independent Windows Scheduled Task!"
} else {
    Write-Host "⚠️ Warning: Task state is $($task.State)"
}
