@echo off
set PID_FILE=%USERPROFILE%\.local\state\airo-second-brain\pc-action-bridge\relay-win.pid
if exist "%PID_FILE%" (
    set /p RELAY_PID=<"%PID_FILE%"
    echo Stopping AIRO PC Relay (PID: %RELAY_PID%)...
    taskkill /PID %RELAY_PID% /F >nul 2>&1
    del "%PID_FILE%" >nul 2>&1
    echo [OK] AIRO PC Relay stopped.
) else (
    echo AIRO PC Relay is not currently running.
)
