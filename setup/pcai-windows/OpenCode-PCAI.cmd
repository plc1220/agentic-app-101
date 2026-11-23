@echo off
setlocal EnableExtensions DisableDelayedExpansion
title OpenCode PCAI
set "PCAI_DIR=%USERPROFILE%\.config\opencode\pcai"
if not exist "%PCAI_DIR%\pcai.json" goto missing_setup
if not exist "%PCAI_DIR%\pcai-ai-essentials-ca.crt" goto missing_setup
if not exist "%PCAI_DIR%\api-token" goto missing_setup
if not exist "%PCAI_DIR%\desktop-path.txt" goto missing_setup
"%SystemRoot%\System32\tasklist.exe" /FI "IMAGENAME eq OpenCode.exe" /NH 2>nul | "%SystemRoot%\System32\find.exe" /I "OpenCode.exe" >nul
if not errorlevel 1 goto running
"%SystemRoot%\System32\tasklist.exe" /FI "IMAGENAME eq opencode-desktop.exe" /NH 2>nul | "%SystemRoot%\System32\find.exe" /I "opencode-desktop.exe" >nul
if not errorlevel 1 goto running
"%SystemRoot%\System32\tasklist.exe" /FI "IMAGENAME eq opencode-cli.exe" /NH 2>nul | "%SystemRoot%\System32\find.exe" /I "opencode-cli.exe" >nul
if not errorlevel 1 goto running
set "PCAI_APP="
set /p "PCAI_APP="<"%PCAI_DIR%\desktop-path.txt"
if not defined PCAI_APP goto missing_app
if not exist "%PCAI_APP%" goto missing_app
set "NODE_EXTRA_CA_CERTS=%PCAI_DIR%\pcai-ai-essentials-ca.crt"
set "OPENCODE_CONFIG=%PCAI_DIR%\pcai.json"
set "NODE_TLS_REJECT_UNAUTHORIZED=1"
start "" /D "%USERPROFILE%" "%PCAI_APP%"
if errorlevel 1 goto missing_app
exit /b 0
:running
echo Save your work and fully quit OpenCode, including its tray instance.
echo Close your OpenCode CLI sessions too, then open this shortcut again.
goto fail
:missing_setup
echo Run Setup PCAI.cmd from the extracted package first.
goto fail
:missing_app
echo OpenCode has moved or could not start. Run Setup PCAI.cmd again.
goto fail
:fail
echo.
pause
exit /b 1
