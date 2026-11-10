@echo off
echo ========================================================
echo   Starting AgriSaathi React + Vite Frontend
echo ========================================================
cd /d "%~dp0frontend"
npx vite --host 127.0.0.1 --port 5173
pause
