@echo off
rem Makes a tailored cover letter (PDF + editable HTML + Overleaf .tex) in Documents\Rsk\Resumes\Cover Letters.
cd /d "%~dp0"
set /p COMPANY=Company name: 
set /p ROLE=Role title (e.g. Software Developer Intern): 
set /p TERM=Term (e.g. Winter 2027): 
set /p WHY=Why this company? Finish the sentence "I am drawn to them because of ...": 
set /p MANAGER=Hiring manager name (leave blank if unknown): 
set /p FOCUS=Lead with which projects? general / web / ai / games [general]: 
if "%FOCUS%"=="" set FOCUS=general
if "%MANAGER%"=="" (
  python tools\build_cover_letter.py --company "%COMPANY%" --role "%ROLE%" --term "%TERM%" --why "%WHY%" --focus %FOCUS%
) else (
  python tools\build_cover_letter.py --company "%COMPANY%" --role "%ROLE%" --term "%TERM%" --why "%WHY%" --focus %FOCUS% --manager "%MANAGER%"
)
explorer "%USERPROFILE%\Documents\Rsk\Resumes\Cover Letters"
pause
