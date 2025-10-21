"""
LaptopTester Pro - Final Build Script (v2)
Builds a portable EXE including all necessary assets and multiprocessing fix.
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
    
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            try:
                os.remove(file)
                print(f"🧹 Removed {file}")
            except:
                pass

def create_build_main():
    """Creates a minimal entry point for the build."""
    content = '''"""
Build Main - Minimal entry point for PyInstaller
"""
import sys
import os
import multiprocessing

# This is crucial for PyInstaller to find the assets folder
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# This prevents new windows from opening on multiprocessing
multiprocessing.freeze_support()

from main_enhanced_auto import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
'''
    with open("build_main.py", "w") as f:
        f.write(content)
    print("✓ Created minimal build entry point: build_main.py")

def build_exe():
    """Build EXE with PyInstaller, including data assets."""
    print("\\n🔨 Building LaptopTester Pro (Final v2)...")
    print("This will take 2-3 minutes...\\n")
    
    separator = ';' if sys.platform == 'win32' else ':'
    
    args = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--noconsole',
        '--name=LaptopTesterPro_v2.7.3', # Version bump
        
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
    except subprocess.CalledProcessError as e:
        print(f"\\n❌ Build failed with error code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Build cancelled by user")
        return False

def create_distribution_folder():
    """Create distribution folder."""
    dist_folder = "LaptopTesterPro_Portable"
    exe_name = "LaptopTesterPro_v2.7.3.exe"
    
    if not os.path.exists(f"dist/{exe_name}"):
        print(f"\\n❌ EXE file not found: dist/{exe_name}")
        return False
    
    print(f"\\n📦 Creating distribution folder: {dist_folder}/")
    
    if os.path.exists(dist_folder):
        # Clean the folder but don't delete it, in case the user has it open
        for item in os.listdir(dist_folder):
            item_path = os.path.join(dist_folder, item)
            try:
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"  - Warning: Could not remove {item_path}: {e}")

    else:
        os.makedirs(dist_folder)
    
    shutil.copy2(f"dist/{exe_name}", f"{dist_folder}/{exe_name}")
    print(f"   ✓ Copied {exe_name}")
    
    readme_content = "Run LaptopTesterPro_v2.7.3.exe to start."
    with open(f"{dist_folder}/README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("   ✓ Created README.txt")
    
    bat_content = "@echo off\\ntitle LaptopTester Pro v2.7.3\\necho Starting...\\nLaptopTesterPro_v2.7.3.exe"
    with open(f"{dist_folder}/Run_LaptopTester.bat", 'w') as f:
        f.write(bat_content)
    print("   ✓ Created Run_LaptopTester.bat")
    
    exe_size = os.path.getsize(f"{dist_folder}/{exe_name}") / (1024*1024)
    print(f"\\n✅ Distribution package created successfully!")
    print(f"   📊 EXE Size: {exe_size:.1f} MB")
    
    return True

def main():
    print("="*60)
    print("LaptopTester Pro - Final Build Script (v2 with MP Fix)")
    print("="*60)
    
    clean_build_folders()
    create_build_main()
    
    if not build_exe():
        print("\\n❌ Build failed!")
        return 1
    
    if not create_distribution_folder():
        print("\\n❌ Failed to create distribution package!")
        return 1
    
    if os.path.exists("build_main.py"):
        os.remove("build_main.py")
        
    print("\\n" + "="*60)
    print("✅ BUILD COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
