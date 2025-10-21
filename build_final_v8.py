"""
LaptopTester Pro - Definitive Build Script (v2.7.8)
Includes the final fix for result details reporting.
"""

import os
import sys
import shutil
import subprocess

VERSION = "v2.7.8"
EXE_NAME = f"LaptopTesterPro_{VERSION}.exe"
DIST_FOLDER = "LaptopTesterPro_Portable"

def clean_build_folders():
    print("🧹 Cleaning old build artifacts...")
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            try:
                os.remove(file)
            except OSError:
                pass

def create_build_main():
    print("✓ Creating minimal build entry point (build_main.py)...")
    content = '''"""
Build Main - Final Entry Point
"""
import sys
import os
import multiprocessing
import customtkinter

customtkinter.set_appearance_mode("Dark")

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

multiprocessing.freeze_support()

from main_enhanced_auto import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
'''
    with open("build_main.py", "w", encoding="utf-8") as f:
        f.write(content)

def build_exe():
    print(f"\\n🔨 Building {EXE_NAME}...")
    
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
        subprocess.run(args, check=True, capture_output=False)
        return True
    except Exception as e:
        print(f"\\n❌ Build failed: {e}")
        return False

def create_distribution_folder():
    if not os.path.exists(f"dist/{EXE_NAME}"):
        print(f"\\n❌ EXE file not found after build.")
        return False
    
    print(f"\\n📦 Creating distribution folder: {DIST_FOLDER}/")
    
    if not os.path.exists(DIST_FOLDER):
        os.makedirs(DIST_FOLDER)

    for item in os.listdir(DIST_FOLDER):
        if item.startswith("LaptopTesterPro") and item.endswith(".exe"):
            os.remove(os.path.join(DIST_FOLDER, item))

    shutil.copy2(f"dist/{EXE_NAME}", os.path.join(DIST_FOLDER, EXE_NAME))
    
    bat_content = f"@echo off\\ntitle LaptopTester Pro {VERSION}\\necho Starting...\\n{EXE_NAME}"
    with open(os.path.join(DIST_FOLDER, "Run_LaptopTester.bat"), 'w') as f:
        f.write(bat_content)
    
    exe_size = os.path.getsize(os.path.join(DIST_FOLDER, EXE_NAME)) / (1024*1024)
    print(f"   ✓ Copied {EXE_NAME} ({exe_size:.1f} MB)")
    
    return True

def main():
    print("="*60)
    print(f"LaptopTester Pro - Definitive Build Script for {VERSION}")
    print("="*60)
    
    if sys.platform == 'win32':
        print("- Terminating previous versions (if any)...")
        subprocess.run(['taskkill', '/F', '/IM', 'LaptopTesterPro_v2.7.7.exe'], capture_output=True, check=False)

    clean_build_folders()
    create_build_main()
    
    if not build_exe():
        return 1
    
    if not create_distribution_folder():
        return 1
    
    print("\\n" + "="*60)
    print(f"✅ BUILD {VERSION} COMPLETED SUCCESSFULLY!")
    print(f"   Your application is ready in the '{DIST_FOLDER}' folder.")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
