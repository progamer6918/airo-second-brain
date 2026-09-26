@echo off
title AIRO PC Action Relay Launcher
echo Starting AIRO Native Windows PC Action Relay...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0register-airo-pc-relay.ps1"
echo.
echo Log file: %USERPROFILE%\.local\state\airo-second-brain\pc-action-bridge\relay-win.log
echo.
timeout /t 3 >nul
