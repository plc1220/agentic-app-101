@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
  set "DEMO_PYTHON=py -3"
) else (
  set "DEMO_PYTHON=python"
)
%DEMO_PYTHON% -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 'Python 3.10 or newer is required.')"
if errorlevel 1 goto failed
if not exist .env (
  copy .env.example .env >nul
  echo Created .env. Add your Gemini API key there, then run run.bat again.
  goto failed
)
if not exist .venv\Scripts\python.exe (
  %DEMO_PYTHON% -m venv .venv
  if errorlevel 1 goto failed
)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
.venv\Scripts\python.exe run_agent.py
if errorlevel 1 goto failed
pause
exit /b 0
:failed
echo Setup or execution stopped. Resolve the message above and try again.
pause
exit /b 1
