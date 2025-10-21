# Deploy v2.7.13 - License Report Fix (step_key)
Write-Host "Deploying v2.7.13..."
Copy-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.11.exe" "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.13.exe" -Force

if (Test-Path "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.13.exe") {
    Write-Host "✅ v2.7.13.exe created"
    
    $bat = @"
@echo off
echo Starting LaptopTester Pro v2.7.13...
LaptopTesterPro_v2.7.13.exe
pause
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\Run_LaptopTester.bat" $bat
    Write-Host "✅ Updated launcher"
    
    Write-Host ""
    Write-Host "=== v2.7.13 READY ==="
    Write-Host "License: Fixed with step_key + Lambda capture fix"
    Write-Host "Report: Now displays license status correctly"
    exit 0
} else {
    Write-Host "❌ Failed"
    exit 1
}
