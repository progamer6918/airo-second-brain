@echo off
title Stop AIRO PC Action Relay
echo Stopping AIRO PC Relay Scheduled Task...
schtasks /end /tn "AIRO_PC_Relay" >nul 2>&1
set PID_FILE=%USERPROFILE%\.local\state\airo-second-brain\pc-action-bridge\relay-win.pid
if exist "%PID_FILE%" (
    set /p RELAY_PID=<"%PID_FILE%"
    echo Stopping AIRO PC Relay process (PID: %RELAY_PID%)...
    taskkill /PID %RELAY_PID% /F >nul 2>&1
    del "%PID_FILE%" >nul 2>&1
)
echo [OK] AIRO PC Relay stopped.
timeout /t 3 >nul
