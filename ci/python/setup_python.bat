@echo off

echo Checking for Python...

set PYTHON_COMMAND=""

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_COMMAND="python"
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_COMMAND="python3"
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_COMMAND="py"
)

if %PYTHON_COMMAND% equ "" (
    echo Please, install python and restart!
    python
    pause
    exit /b 1
)

echo %PYTHON_COMMAND% is installed!
%PYTHON_COMMAND% --version

echo .
echo Installing colorama
pip install colorama
exit /b 0