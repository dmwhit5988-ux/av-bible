@echo off
rem Theoria Studio launcher: sets up the Python environment (again whenever
rem requirements.txt changes), then starts the Studio.
title Theoria Studio
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo First-time setup: creating Python environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment. Is Python installed?
        pause
        exit /b 1
    )
)

rem Install the requirements when requirements.txt differs from the copy last
rem installed; its SHA-256 is kept in .venv\requirements.sha256.
set "REQ_HASH="
set "OLD_HASH="
for /f "skip=1 delims=" %%h in ('certutil -hashfile requirements.txt SHA256') do (
    if not defined REQ_HASH set "REQ_HASH=%%h"
)
if not defined REQ_HASH set "REQ_HASH=unhashed"
if exist ".venv\requirements.sha256" set /p OLD_HASH=<".venv\requirements.sha256"
if not "%REQ_HASH%"=="%OLD_HASH%" (
    echo Installing requirements...
    ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt
    if errorlevel 1 (
        echo Installing the requirements failed; see the messages above.
        pause
        exit /b 1
    )
    >".venv\requirements.sha256" echo %REQ_HASH%
)

rem pythonw has no console, so a Studio that can't even load would vanish
rem without a word. Import it here first; if that fails, run it with
rem python.exe in this window so the traceback stays on screen. (Once it
rem loads, app.py reports its own failures in a message box and in
rem cache\studio_error.log.)
".venv\Scripts\python.exe" -c "import app" >nul 2>&1
if errorlevel 1 (
    echo Theoria Studio failed to start. Running it here to show the error...
    echo.
    ".venv\Scripts\python.exe" app.py
    pause
    exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" app.py
