@echo off
chcp 65001 >nul
title LaptopTester - Portable Runner

echo ========================================
echo    LaptopTester - Portable Mode
echo ========================================
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python không được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python 3.8+ từ https://python.org
    pause
    exit /b 1
)

:: Kiểm tra file chính
if not exist "laptoptester.py" (
    echo [ERROR] Không tìm thấy file laptoptester.py
    echo Vui lòng đảm bảo bạn đang ở thư mục đúng
    pause
    exit /b 1
)

:: Kiểm tra requirements
if exist "requirements.txt" (
    echo [INFO] Kiểm tra dependencies...
    pip install -r requirements.txt --quiet --disable-pip-version-check
    if %errorlevel% neq 0 (
        echo [WARNING] Một số package có thể chưa được cài đặt
    )
)

:: Tạo thư mục cần thiết
if not exist "logs" mkdir logs
if not exist "assets" mkdir assets
if not exist "bin" mkdir bin

echo [INFO] Khởi động LaptopTester...
echo.

:: Chạy ứng dụng với quyền admin nếu có thể
python laptoptester.py

:: Kiểm tra lỗi
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ứng dụng đã dừng với lỗi (Exit code: %errorlevel%)
    echo Kiểm tra file log để biết thêm chi tiết
)

echo.
echo Ứng dụng đã đóng. Nhấn phím bất kỳ để thoát...
pause >nul