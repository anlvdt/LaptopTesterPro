"""
LaptopTester Pro - Simple Fast Build Script
Builds portable EXE with only essential dependencies
"""

import os
import sys
import shutil
import subprocess

def clean_build_folders():
    """Remove old build artifacts"""
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            print(f"🧹 Removing {folder}/...")
            shutil.rmtree(folder, ignore_errors=True)
    
    # Remove .spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            try:
                os.remove(file)
                print(f"🧹 Removed {file}")
            except:
                pass

def build_exe():
    """Build EXE with PyInstaller"""
    print("\n🔨 Building LaptopTester Pro (Fast Mode)...")
    print("This will take 2-3 minutes...\n")
    
    # Essential PyInstaller arguments only
    args = [
        'pyinstaller',
        '--onefile',                    # Single EXE file
        '--windowed',                   # No console window
        '--noconsole',                  # No console window
        '--name=LaptopTesterPro_v2.7.2',
        
        # Icon (if exists)
        # '--icon=icon.ico',
        
        # Essential hidden imports
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--hidden-import=psutil',
        '--hidden-import=wmi',
        '--hidden-import=pygame',
        
        # Collect CustomTkinter data
        '--collect-all=customtkinter',
        
        # Include assets folder with logo and audio files
        '--add-data=assets;assets',
        
        # Exclude heavy, unused libraries
        '--exclude-module=scipy',
        '--exclude-module=sklearn',
        '--exclude-module=matplotlib',
        '--exclude-module=torch',
        '--exclude-module=tensorflow',
        '--exclude-module=pandas',
        '--exclude-module=seaborn',

        # Main file
        'build_main.py'
    ]
    
    try:
        result = subprocess.run(args, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        return False

def create_distribution_folder():
    """Create distribution folder with EXE and docs"""
    dist_folder = "LaptopTesterPro_Portable"
    exe_name = "LaptopTesterPro_v2.7.2.exe"
    
    if not os.path.exists(f"dist/{exe_name}"):
        print(f"\n❌ EXE file not found: dist/{exe_name}")
        return False
    
    print(f"\n📦 Creating distribution folder: {dist_folder}/")
    
    # Create folder
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Copy EXE
    shutil.copy2(f"dist/{exe_name}", f"{dist_folder}/{exe_name}")
    print(f"   ✓ Copied {exe_name}")
    
    # Create README
    readme_content = """LaptopTester Pro v2.7.2 - Portable Edition
==========================================

CÁCH SỬ DỤNG / HOW TO USE:
- Chạy file LaptopTesterPro_v2.7.2.exe
- Run LaptopTesterPro_v2.7.2.exe

TÍNH NĂNG / FEATURES:
✓ Kiểm tra CPU, RAM, Disk, GPU (CPU, RAM, Disk, GPU Testing)
✓ Đọc thông tin phần cứng chi tiết (Detailed Hardware Information)
✓ Giao diện song ngữ Việt-Anh (Bilingual Vietnamese-English Interface)
✓ Hướng dẫn chi tiết cho từng bước test (Step-by-step Testing Guide)
✓ Không cần cài đặt Python (No Python Installation Required)

YÊU CẦU HỆ THỐNG / SYSTEM REQUIREMENTS:
- Windows 10/11 64-bit
- 4GB RAM trở lên (4GB+ RAM)
- 200MB dung lượng trống (200MB free space)

HỖ TRỢ / SUPPORT:
- Shopee: https://s.shopee.vn/2AyjvtHF3F

Phát triển bởi / Developed by: LaptopTester Team
© 2024 All Rights Reserved
"""
    
    with open(f"{dist_folder}/README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("   ✓ Created README.txt")
    
    # Create simple launcher BAT
    bat_content = """@echo off
title LaptopTester Pro
echo Starting LaptopTester Pro...
LaptopTesterPro_v2.7.2.exe
"""
    
    with open(f"{dist_folder}/Run_LaptopTester.bat", 'w') as f:
        f.write(bat_content)
    print("   ✓ Created Run_LaptopTester.bat")
    
    # Get EXE size
    exe_size = os.path.getsize(f"{dist_folder}/{exe_name}") / (1024*1024)
    print(f"\n✅ Distribution package created successfully!")
    print(f"   📁 Folder: {dist_folder}/")
    print(f"   📊 EXE Size: {exe_size:.1f} MB")
    
    return True

def main():
    print("="*60)
    print("LaptopTester Pro - Fast Build Script")
    print("="*60)
    
    # Step 1: Clean
    print("\n[1/3] Cleaning old builds...")
    clean_build_folders()
    
    # Step 2: Build
    print("\n[2/3] Building EXE (this may take 2-3 minutes)...")
    if not build_exe():
        print("\n❌ Build failed!")
        input("\nPress Enter to exit...")
        return 1
    
    # Step 3: Package
    print("\n[3/3] Creating distribution package...")
    if not create_distribution_folder():
        print("\n❌ Failed to create distribution package!")
        input("\nPress Enter to exit...")
        return 1
    
    print("\n" + "="*60)
    print("✅ BUILD COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📁 Your portable app is ready in: LaptopTesterPro_Portable/")
    print("   You can now:")
    print("   1. Test the EXE by running it")
    print("   2. Compress the folder to .zip for distribution")
    print("   3. Copy to USB drive or share online")
    
    input("\nPress Enter to exit...")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
