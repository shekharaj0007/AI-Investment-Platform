@echo off
echo Starting AI Financial Copilot...
echo.
echo Backend API:  http://localhost:8001
echo API Docs:     http://localhost:8001/docs
echo Frontend:     http://localhost:3001
echo.

start "Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 3 /nobreak > nul
start "Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"
echo Servers starting in separate windows...
