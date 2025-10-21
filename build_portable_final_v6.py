"""
LaptopTester Pro - Final Build Script (v6)
Builds a portable EXE with the user confirmation fix.
"""

import os
import sys
import shutil
import subprocess

def clean_build_folders():
    # ... (omitted for brevity) ...

def create_build_main():
    # ... (omitted for brevity) ...

def build_exe():
    print("\\n🔨 Building LaptopTester Pro (v2.7.7)...")
    
    separator = ';' if sys.platform == 'win32' else ':'
    
    args = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--noconsole',
        '--name=LaptopTesterPro_v2.7.7', # Version bump for confirmation fix
        
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
    # ... (omitted for brevity) ...

def main():
    print("="*60)
    print("LaptopTester Pro - Final Build Script (v6 - Confirmation Fix)")
    print("="*60)
    
    if sys.platform == 'win32':
        subprocess.run(['taskkill', '/F', '/IM', 'LaptopTesterPro_v2.7.6.exe'], capture_output=True, check=False)

    clean_build_folders()
    create_build_main()
    
    if not build_exe():
        return 1
    
    if not create_distribution_folder():
        return 1
    
    # Cleanup
    if os.path.exists("build_main.py"):
        os.remove("build_main.py")
    if os.path.exists("build_portable_final_v6.py"):
        os.remove("build_portable_final_v6.py")
        
    print("\\n✅ BUILD v2.7.7 COMPLETED SUCCESSFULLY!")
    
    return 0

if __name__ == "__main__":
    # Re-create the build_main.py for this build
    build_main_content = '''"""
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
        f.write(build_main_content)
        
    sys.exit(main())
