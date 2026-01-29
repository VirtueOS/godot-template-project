@echo off

:: Check for admin rights using net session
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -ArgumentList '%cd%' -Verb RunAs"
    exit /b
)

:: Go to project folder after restarting as admin
if not "%~1"=="" (
    cd /d "%~1"
)

call python .\setup_godot_addons.py
pause