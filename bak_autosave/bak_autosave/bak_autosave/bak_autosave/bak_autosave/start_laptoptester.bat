@echo off
title LaptopTester - Professional Laptop Testing Suite

echo.
echo ==========================================
echo   LaptopTester v1.5.0
echo   Professional Laptop Testing Suite  
echo ==========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] LaptopTester needs Administrator privileges for full functionality.
    echo Some hardware tests may not work properly without admin rights.
    echo.
    echo Press any key to continue anyway, or close this window and "Run as Administrator"
    pause
    echo.
)

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] No virtual environment found. Using system Python.
)

REM Check dependencies
echo [INFO] Checking dependencies...
python -c "import customtkinter, psutil, cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Missing required dependencies.
    echo Installing dependencies from requirements.txt...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo [INFO] Starting LaptopTester...
echo.

REM Start the application
python laptoptester.py

REM Handle exit
echo.
echo LaptopTester closed.
if exist "logs\" (
    echo Logs are available in the 'logs' folder for troubleshooting.
)
echo.
pause