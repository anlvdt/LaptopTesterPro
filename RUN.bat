@echo off
chcp 65001 >nul
python main_enhanced_auto.py
if errorlevel 1 (
    echo.
    echo ❌ Lỗi khởi động! Chạy INSTALL.bat trước
    pause
)
