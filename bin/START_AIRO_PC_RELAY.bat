@echo off
title AIRO PC Action Relay
echo Starting AIRO Native Windows PC Action Relay in background...
start /b powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0airo-pc-relay-win.ps1"
echo [OK] AIRO PC Relay launched. Check log: %USERPROFILE%\.local\state\airo-second-brain\pc-action-bridge\relay-win.log
