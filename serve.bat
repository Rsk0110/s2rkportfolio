@echo off
rem Runs the portfolio locally at http://localhost:8000 (Ctrl+C to stop).
cd /d "%~dp0"
start "" http://localhost:8000
python -m http.server 8000
