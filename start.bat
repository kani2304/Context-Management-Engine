@echo off
title Context Management Engine Launcher
echo ========================================================
echo   Context Management Engine - AIML Capstone Project
echo ========================================================
echo.

:: Ensure we are in this script's directory
cd /d "%~dp0"

:: Detect Python command
set PYTHON_CMD=python
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    py -3.13 --version >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set PYTHON_CMD=py -3.13
    ) else (
        set PYTHON_CMD=py
    )
)

echo [1/2] Launching Backend Bridge on port 8000 using %PYTHON_CMD%...
start "CME Backend Bridge (FastAPI)" cmd /k "%PYTHON_CMD% -u backend_bridge.py"

echo [2/2] Launching React Frontend on port 5173...
start "CME Frontend UI (Vite)" cmd /k "npm run dev"

echo.
echo Waiting for Backend ML models to initialize (SentenceTransformers + FAISS)...
powershell -NoProfile -Command "for ($i = 0; $i -lt 40; $i++) { try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 1; if ($r.status -eq 'healthy') { Write-Host 'Backend is LIVE and healthy!'; break } } catch { Start-Sleep -Milliseconds 800 } }"

echo.
echo ========================================================
echo Both services are ready:
echo - Frontend:       http://localhost:5173/
echo - Backend Bridge: http://127.0.0.1:8000/api/health
echo ========================================================
echo Opening browser...
start http://localhost:5173/
pause
