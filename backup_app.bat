@echo off
chcp 65001 >nul
echo ========================================
echo   LaptopTester - Backup Application
echo ========================================
echo.

set TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_NAME=LaptopTester_Backup_%TIMESTAMP%.zip

echo Creating backup: %BACKUP_NAME%
echo.

powershell -Command "Compress-Archive -Path 'main_enhanced_auto.py','requirements.txt','README.md','assets','workers','bin' -DestinationPath '%BACKUP_NAME%' -Force"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Backup completed successfully!
    echo File: %BACKUP_NAME%
    echo.
    dir "%BACKUP_NAME%" | findstr /C:"%BACKUP_NAME%"
) else (
    echo.
    echo ✗ Backup failed!
)

echo.
pause
