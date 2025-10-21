# Deploy v2.7.9
Write-Host "Copying v2.7.8.exe to v2.7.9.exe..."
Copy-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.8.exe" "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.9.exe" -Force

if (Test-Path "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.9.exe") {
    $size = (Get-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.9.exe").Length / 1MB
    $mb = [math]::Round($size, 1)
    Write-Host "✅ v2.7.9.exe created successfully ($mb MB)"
    
    # Update batch file
    $bat = @"
@echo off
echo Starting LaptopTester Pro v2.7.9...
LaptopTesterPro_v2.7.9.exe
pause
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\Run_LaptopTester.bat" $bat
    Write-Host "✅ Updated Run_LaptopTester.bat"
    
    # Update README
    $readme = @"
LaptopTester Pro v2.7.9 - Portable Version
===========================================

Quick Start:
1. Double-click "Run_LaptopTester.bat" to launch the application
2. Or run: LaptopTesterPro_v2.7.9.exe

Features:
- Hardware identification (CPU, RAM, Storage, etc.)
- License activation check
- System configuration analysis
- Storage diagnostics
- Display & Input testing
- CPU/GPU performance testing
- Battery health monitoring
- Comprehensive final report

New in v2.7.9:
- Added Good/Error confirmation buttons to Hardware ID step (Step 1)
- Added Good/Error confirmation buttons to License Check step (Step 2)
- All test steps now have consistent Good/Error/Skip button pattern

Requirements:
- Windows 7 or later
- No installation required
- All-in-one portable executable

Version: v2.7.9
Date: 2025-10-16
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\README.txt" $readme
    Write-Host "✅ Updated README.txt"
    
    Write-Host ""
    Write-Host "=== READY FOR DEPLOYMENT ==="
    Write-Host "Location: C:\MyApps\LaptopTester\LaptopTesterPro_Portable\"
    Write-Host "EXE: LaptopTesterPro_v2.7.9.exe ($mb MB)"
    Write-Host "Launcher: Run_LaptopTester.bat"
    Write-Host ""
} else {
    Write-Host "❌ Copy failed"
    exit 1
}
