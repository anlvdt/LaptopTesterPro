@echo off
chcp 65001 >nul
cls

echo ============================================================
echo   LaptopTester Pro - Build Portable EXE
echo   Version: 2.7.2
echo   Date: 15/10/2025
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo    Vui lòng cài đặt Python từ https://python.org
    pause
    exit /b 1
)

echo ✅ Python đã cài đặt
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ PyInstaller chưa được cài đặt
    echo    Đang cài đặt PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Không thể cài đặt PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller đã sẵn sàng
echo.

REM Run the build script
echo 🔨 Đang build ứng dụng (có thể mất 3-5 phút)...
echo.
python build_portable_enhanced.py

if errorlevel 1 (
    echo.
    echo ❌ Build thất bại!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   🎉 BUILD THÀNH CÔNG!
echo ============================================================
echo.
echo 📦 File .exe đã được tạo trong folder:
echo    → LaptopTesterPro_Portable\
echo.
echo 💡 Bạn có thể:
echo    - Copy toàn bộ folder đi bất kỳ đâu
echo    - Chạy file .exe mà không cần cài đặt
echo    - Chia sẻ cho người khác sử dụng
echo.

REM Ask if user wants to open the folder
echo Bạn có muốn mở folder output không? (Y/N)
set /p OPEN_FOLDER=
if /i "%OPEN_FOLDER%"=="Y" (
    start explorer LaptopTesterPro_Portable
)

echo.
echo ============================================================
pause
