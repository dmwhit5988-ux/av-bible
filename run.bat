@echo off
rem AV Bible launcher — creates the environment on first run, then starts the app.
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo First-time setup: creating Python environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment. Is Python installed?
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt
)

start "" ".venv\Scripts\pythonw.exe" app.py
