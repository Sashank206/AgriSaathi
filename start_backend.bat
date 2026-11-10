@echo off
echo ========================================================
echo   Starting AgriSaathi FastAPI Backend (Python 3.11)
echo ========================================================
cd /d "%~dp0backend"
"C:\Users\ESWAR\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn app.main:app --app-dir "%~dp0backend" --host 127.0.0.1 --port 8000 --reload
pause
