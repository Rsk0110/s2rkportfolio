@echo off
rem Publishes your latest changes to the live site.
rem Usage: publish "what you changed"
cd /d "%~dp0"
set MSG=%~1
if "%MSG%"=="" set MSG=Update portfolio
git add -A
git commit -m "%MSG%"
git push
echo.
echo Published. GitHub Pages updates in about a minute.
