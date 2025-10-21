@echo off
title Build LaptopTester EXE

echo Building LaptopTester.exe...
echo.

:: Install PyInstaller
pip install pyinstaller --quiet

:: Create folders
if not exist "assets" mkdir assets
if not exist "bin" mkdir bin

:: Build EXE
pyinstaller --onefile --windowed --name=LaptopTester laptoptester.py

:: Check result
if exist "dist\LaptopTester.exe" (
    echo.
    echo SUCCESS! EXE created in dist folder
    echo File: dist\LaptopTester.exe
    
    :: Show file size
    for %%A in ("dist\LaptopTester.exe") do (
        set /a size=%%~zA/1024/1024
        echo Size: !size! MB
    )
    
    :: Create portable folder
    if exist "LaptopTester_Portable" rmdir /s /q "LaptopTester_Portable"
    mkdir "LaptopTester_Portable"
    copy "dist\LaptopTester.exe" "LaptopTester_Portable\"
    
    echo.
    echo Portable version created in: LaptopTester_Portable\
    
) else (
    echo.
    echo ERROR: Build failed!
)

echo.
pause