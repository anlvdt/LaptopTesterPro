@echo off
chcp 65001 >nul
echo ========================================
echo   LaptopTester - Cài đặt tự động
echo ========================================
echo.

echo [1/3] Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Không tìm thấy Python! Vui lòng cài Python 3.8+ từ python.org
    pause
    exit /b 1
)
python --version

echo.
echo [2/3] Cài đặt thư viện...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Lỗi cài đặt! Kiểm tra kết nối mạng và thử lại
    pause
    exit /b 1
)

echo.
echo [3/3] Tạo thư mục logs...
if not exist logs mkdir logs

echo.
echo ========================================
echo ✅ Cài đặt hoàn tất!
echo ========================================
echo.
echo Chạy ứng dụng: python main_enhanced_auto.py
echo Hoặc click đúp vào: RUN.bat
echo.
pause
