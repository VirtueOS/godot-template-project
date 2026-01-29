@echo off

set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "RESET=[0m"


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


echo %GREEN% ========================================== %RESET%
echo %GREEN%	Starting project set up 		        %RESET%
echo %GREEN% ========================================== %RESET%
echo.
echo.
echo.

echo %YELLOW% 1. Check for python %RESET%
echo.
call python/setup_python.bat
if %errorlevel% neq 0 (
    echo Script failed with error code: %errorlevel%
    pause
    exit /b %errorlevel%
)


echo.
echo %YELLOW% 2. Setup Godot addons %RESET%
echo.
cd addons
python setup_godot_addons.py
cd ..

echo.
echo %YELLOW% 2. Setup git hooks %RESET%
echo.
cd git_hooks
python install_git_hooks.py
cd ..

pause