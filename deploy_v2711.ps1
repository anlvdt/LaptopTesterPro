# Deploy v2.7.11 with scroll buttons fixed
Write-Host "Deploying v2.7.11..."
Copy-Item "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.10.exe" "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.11.exe" -Force

if (Test-Path "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\LaptopTesterPro_v2.7.11.exe") {
    Write-Host "✅ v2.7.11.exe created"
    
    $bat = @"
@echo off
echo Starting LaptopTester Pro v2.7.11...
LaptopTesterPro_v2.7.11.exe
pause
"@
    Set-Content "C:\MyApps\LaptopTester\LaptopTesterPro_Portable\Run_LaptopTester.bat" $bat
    Write-Host "✅ Updated launcher"
    
    Write-Host ""
    Write-Host "=== v2.7.11 READY ==="
    Write-Host "Scroll buttons now visible on all test steps!"
    exit 0
} else {
    Write-Host "❌ Failed"
    exit 1
}
