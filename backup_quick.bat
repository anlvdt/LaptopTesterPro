@echo off
chcp 65001 >nul
title LaptopTester Quick Backup

echo 🔧 LaptopTester Quick Backup
echo =============================

:: Tạo backup nhanh với timestamp
set timestamp=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

set backup_name=LaptopTester_Quick_%timestamp%
set backup_dir=..\Backups

:: Tạo thư mục backup
if not exist "%backup_dir%" mkdir "%backup_dir%"

echo 📦 Tạo backup: %backup_name%.zip
echo 📁 Nguồn: %cd%

:: Tạo file ZIP với 7zip (nếu có) hoặc PowerShell
where 7z >nul 2>&1
if %errorlevel%==0 (
    echo 🔄 Sử dụng 7-Zip...
    7z a -tzip "%backup_dir%\%backup_name%.zip" *.py *.md *.txt assets\ bin\ -x!__pycache__\ -x!*.pyc -x!*.log -x!venv\ -x!env\
) else (
    echo 🔄 Sử dụng PowerShell...
    powershell -Command "Compress-Archive -Path '*.py','*.md','*.txt','assets','bin' -DestinationPath '%backup_dir%\%backup_name%.zip' -Force"
)

if exist "%backup_dir%\%backup_name%.zip" (
    echo ✅ Backup thành công!
    echo 📦 File: %backup_dir%\%backup_name%.zip
    
    :: Hiển thị kích thước file
    for %%A in ("%backup_dir%\%backup_name%.zip") do (
        set /a size=%%~zA/1024/1024
        echo 💾 Kích thước: !size! MB
    )
) else (
    echo ❌ Backup thất bại!
)

echo.
pause