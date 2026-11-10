@echo off
echo ========================================================
echo   Launching AgriSaathi (Backend + Frontend)
echo ========================================================
start "AgriSaathi Backend" cmd /c "%~dp0start_backend.bat"
start "AgriSaathi Frontend" cmd /c "%~dp0start_frontend.bat"
echo Both servers are launching!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:5173
