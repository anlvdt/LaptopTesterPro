# Deploy v2.7.10 with scroll improvements
Write-Host "Copying v2.7.9.exe to v2.7.10.exe..."
Copy-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.9.exe" "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.10.exe" -Force

if (Test-Path "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.10.exe") {
    $size = (Get-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.10.exe").Length / 1MB
    $mb = [math]::Round($size, 1)
    Write-Host "✅ v2.7.10.exe created successfully ($mb MB)"
    
    # Update batch file
    $bat = @"
@echo off
echo Starting LaptopTester Pro v2.7.10...
LaptopTesterPro_v2.7.10.exe
pause
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\Run_LaptopTester.bat" $bat
    Write-Host "✅ Updated Run_LaptopTester.bat"
    
    # Update README
    $readme = @"
LaptopTester Pro v2.7.10 - Portable Version
============================================

Quick Start:
1. Double-click "Run_LaptopTester.bat" to launch the application
2. Or run: LaptopTesterPro_v2.7.10.exe

Features:
- Hardware identification (CPU, RAM, Storage, etc.)
- License activation check
- System configuration analysis
- Storage diagnostics
- Display & Input testing
- CPU/GPU performance testing
- Battery health monitoring
- Comprehensive final report

New in v2.7.10:
- Fixed License Check result display in final report
- Added scroll jump buttons (▲▼) on all scrollable sections
- Quick navigation to top/bottom of long test results

New in v2.7.9:
- Added Good/Error confirmation buttons to Hardware ID step (Step 1)
- Added Good/Error confirmation buttons to License Check step (Step 2)
- All test steps now have consistent Good/Error/Skip button pattern

Requirements:
- Windows 7 or later
- No installation required
- All-in-one portable executable

Version: v2.7.10
Date: 2025-10-16
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\README.txt" $readme
    Write-Host "✅ Updated README.txt"
    
    Write-Host ""
    Write-Host "=== READY FOR DEPLOYMENT ==="
    Write-Host "Location: C:\MyApps\LaptopTester\LaptopTesterPro_Portable\"
    Write-Host "EXE: LaptopTesterPro_v2.7.10.exe ($mb MB)"
    Write-Host "Launcher: Run_LaptopTester.bat"
    Write-Host ""
    Write-Host "Changes in v2.7.10:"
    Write-Host "  ✓ License Check status now shows correctly in report"
    Write-Host "  ✓ Scroll navigation buttons added to all sections"
    Write-Host ""
} else {
    Write-Host "❌ Copy failed"
    exit 1
}
