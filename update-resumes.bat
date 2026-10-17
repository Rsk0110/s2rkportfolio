@echo off
rem Rebuilds all resume PDFs and website previews from your editable resume files,
rem then publishes them. The share links stay the same and show the new versions.
cd /d "%~dp0"
echo Rebuilding resumes...
python tools\update_resumes.py || exit /b 1
git add resume index.html
git commit -m "Update resumes"
git push
echo.
echo Resumes updated. The live links show the new versions in about a minute.
