@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
  set "DEMO_PYTHON=py -3"
) else (
  set "DEMO_PYTHON=python"
)
%DEMO_PYTHON% -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 'Python 3.11 or newer is required by Deep Agents.')"
if errorlevel 1 goto failed
if not exist .env (
  copy .env.example .env >nul
  echo Created .env. Add your Gemini key, or set AGENT_MODE=sample for the offline walkthrough.
  goto failed
)
if not exist .venv\Scripts\python.exe (
  %DEMO_PYTHON% -m venv .venv
  if errorlevel 1 goto failed
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
.venv\Scripts\python.exe launch.py
if errorlevel 1 goto failed
exit /b 0
:failed
echo Setup stopped. Resolve the message above and run run.bat again.
pause
exit /b 1
