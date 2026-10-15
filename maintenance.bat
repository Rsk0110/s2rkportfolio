@echo off
rem Turns maintenance mode on or off on the live site.
rem   maintenance on   -> visitors see the "Back very soon" page
rem   maintenance off  -> site is live again
cd /d "%~dp0"
if /i "%~1"=="on"  set VALUE=true
if /i "%~1"=="off" set VALUE=false
if not defined VALUE (
  echo Usage: maintenance on ^| off
  exit /b 1
)
powershell -NoProfile -Command "(Get-Content site-config.js -Raw) -replace '(?m)^(\s*)maintenance:\s*(true|false)', '${1}maintenance: %VALUE%' | Set-Content site-config.js -NoNewline -Encoding utf8"
git add site-config.js
git commit -m "Maintenance mode %~1"
git push
echo.
echo Maintenance mode is now %~1. GitHub Pages updates in about a minute.
