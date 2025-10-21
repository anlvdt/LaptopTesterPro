# Deploy v2.7.10 with scroll button fixes
Write-Host "Copying v2.7.9.exe to v2.7.10.exe..."
Copy-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.9.exe" "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.10.exe" -Force

if (Test-Path "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.10.exe") {
    Write-Host "✅ v2.7.10.exe created successfully"
    
    # Update batch file
    $bat = @"
@echo off
echo Starting LaptopTester Pro v2.7.10...
LaptopTesterPro_v2.7.10.exe
pause
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\Run_LaptopTester.bat" $bat
    Write-Host "✅ Updated Run_LaptopTester.bat"
    
    Write-Host ""
    Write-Host "=== READY FOR DEPLOYMENT ==="
    exit 0
} else {
    Write-Host "❌ Copy failed"
    exit 1
}
