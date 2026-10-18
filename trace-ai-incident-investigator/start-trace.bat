@echo off
setlocal

cd /d "%~dp0"
echo ========================================
echo             TRACE LAUNCHER
echo ========================================
echo.
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found.
    echo.
    echo Create it using:
    echo py -m venv .venv
    echo.
    pause
    exit /b 1
)
if not exist "frontend\package.json" (
    echo ERROR: Frontend package.json not found.
    pause
    exit /b 1
)
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed.
        pause
        exit /b 1
    )
    cd ..
)
echo Starting TRACE backend...
start "TRACE Backend" cmd /k ""%CD%\.venv\Scripts\python.exe" -m uvicorn src.api:app --reload"
echo Starting TRACE frontend...
start "TRACE Frontend" cmd /k "cd /d "%CD%\frontend" && npm run dev"

echo Waiting for services to initialize...
timeout /t 5 /nobreak >nul
echo Opening TRACE dashboard...
start "" "http://localhost:5173"
echo.
echo TRACE startup commands executed.
echo Keep the backend and frontend windows open.
echo.
pause
