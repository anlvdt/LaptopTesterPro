"""
LaptopTester Pro v2.7.9 Build Script - Simple Version
Builds the portable EXE without timeout issues
"""

import os
import sys
import shutil
import subprocess

VERSION = "v2.7.9"
EXE_NAME = f"LaptopTesterPro_{VERSION}.exe"
DIST_FOLDER = "LaptopTesterPro_Portable"
SPEC_FILE = "LaptopTesterPro_v2.7.9.spec"

def create_build_main():
    """Create the entry point for PyInstaller"""
    print("✓ Creating build entry point...")
    content = '''"""
Build Main - Final Entry Point for v2.7.9
"""
import sys
import os
import multiprocessing
import customtkinter

# Set dark mode globally before App initialization
customtkinter.set_appearance_mode("Dark")

# Fix frozen paths
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# Support multiprocessing in frozen app
multiprocessing.freeze_support()

from main_enhanced_auto import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
'''
    with open("build_main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✓ build_main.py created")

def clean_build():
    """Clean old build artifacts"""
    print("🧹 Cleaning old build artifacts...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    
    # Remove old spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            try:
                os.remove(file)
            except:
                pass
    print("  ✓ Cleaned")

def build_exe():
    """Build the executable with PyInstaller"""
    print(f"\n🔨 Building {EXE_NAME}...")
    print("  This may take 5-10 minutes...")
    
    separator = ';' if sys.platform == 'win32' else ':'
    
    args = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--noconsole',
        f'--name=LaptopTesterPro_{VERSION}',
        f'--add-data=assets{separator}assets',
        '--collect-all=customtkinter',
        '--exclude-module=scipy',
        '--exclude-module=sklearn',
        '--exclude-module=matplotlib',
        '--exclude-module=torch',
        '--exclude-module=tensorflow',
        '--exclude-module=pandas',
        '--exclude-module=seaborn',
        'build_main.py'
    ]
    
    try:
        subprocess.run(args, check=True)
        print("  ✓ Build completed")
        return True
    except Exception as e:
        print(f"  ❌ Build failed: {e}")
        return False

def create_portable():
    """Create the portable distribution"""
    exe_path = f"dist/{EXE_NAME}"
    if not os.path.exists(exe_path):
        print(f"\n❌ EXE not found at {exe_path}")
        return False
    
    print(f"\n📦 Creating portable distribution...")
    
    if not os.path.exists(DIST_FOLDER):
        os.makedirs(DIST_FOLDER)
    
    # Remove old v2.7.8 to save space
    old_exe = os.path.join(DIST_FOLDER, "LaptopTesterPro_v2.7.8.exe")
    if os.path.exists(old_exe):
        print(f"  - Removing old version...")
        os.remove(old_exe)
    
    # Copy new EXE
    dest_exe = os.path.join(DIST_FOLDER, EXE_NAME)
    shutil.copy2(exe_path, dest_exe)
    exe_size = os.path.getsize(dest_exe) / (1024*1024)
    print(f"  ✓ Copied {EXE_NAME} ({exe_size:.1f} MB)")
    
    # Update batch file
    bat_path = os.path.join(DIST_FOLDER, "Run_LaptopTester.bat")
    bat_content = f"@echo off\necho Starting LaptopTester Pro {VERSION}...\n{EXE_NAME}\npause"
    with open(bat_path, 'w') as f:
        f.write(bat_content)
    print(f"  ✓ Updated Run_LaptopTester.bat")
    
    # Update README
    readme_path = os.path.join(DIST_FOLDER, "README.txt")
    readme_content = f"""LaptopTester Pro {VERSION} - Portable Version
=============================================

Quick Start:
1. Double-click "Run_LaptopTester.bat" to launch the application
2. Or run: LaptopTesterPro_{VERSION}.exe

Features:
- Hardware identification (CPU, RAM, Storage, etc.)
- License activation check
- System configuration analysis
- Storage diagnostics
- Display & Input testing
- CPU/GPU performance testing
- Battery health monitoring
- Comprehensive final report

Requirements:
- Windows 7 or later
- No installation required
- All-in-one portable executable

Version: {VERSION}
Date: 2025-10-16
"""
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"  ✓ Updated README.txt")
    
    return True

def main():
    print("="*60)
    print(f"LaptopTester Pro {VERSION} - Build Script")
    print("="*60)
    
    # Kill old instances
    if sys.platform == 'win32':
        subprocess.run(['taskkill', '/F', '/IM', 'LaptopTesterPro_v2.7.8.exe'], 
                      capture_output=True, check=False)
    
    clean_build()
    create_build_main()
    
    if not build_exe():
        print("\n❌ Build failed")
        return 1
    
    if not create_portable():
        print("\n❌ Portable creation failed")
        return 1
    
    print("\n" + "="*60)
    print(f"✅ BUILD {VERSION} COMPLETED SUCCESSFULLY!")
    print(f"   Location: {DIST_FOLDER}/")
    print(f"   Run: {DIST_FOLDER}/Run_LaptopTester.bat")
    print("="*60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
