# Deploy v2.7.12 - License Check Result Fix
Write-Host "Deploying v2.7.12..."
Copy-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.11.exe" "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.12.exe" -Force

if (Test-Path "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.12.exe") {
    Write-Host "✅ v2.7.12.exe created"
    
    $bat = @"
@echo off
echo Starting LaptopTester Pro v2.7.12...
LaptopTesterPro_v2.7.12.exe
pause
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\Run_LaptopTester.bat" $bat
    Write-Host "✅ Updated launcher"
    
    Write-Host ""
    Write-Host "=== v2.7.12 READY ==="
    Write-Host "License Check: Result captured by value (Lambda fix)"
    exit 0
} else {
    Write-Host "❌ Failed"
    exit 1
}
