"""
Build LaptopTester Pro Portable EXE
Version: 2.7.2
Date: 15/10/2025

This script creates a portable .exe file using PyInstaller.
"""

import PyInstaller.__main__
import os
import shutil
import sys
from pathlib import Path

def clean_build_folders():
    """Clean up previous build artifacts"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['LaptopTester.spec', 'LaptopTesterPro.spec']
    
    print("🧹 Cleaning build folders...")
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  ✅ Removed {folder}/")
            except Exception as e:
                print(f"  ⚠️ Could not remove {folder}: {e}")
    
    for file in files_to_clean:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"  ✅ Removed {file}")
            except Exception as e:
                print(f"  ⚠️ Could not remove {file}: {e}")

def check_requirements():
    """Check if required packages are installed"""
    print("\n📦 Checking requirements...")
    
    required_packages = {
        'PyInstaller': 'PyInstaller',
        'customtkinter': 'customtkinter',
        'Pillow': 'PIL',  # PIL is the import name for Pillow
        'psutil': 'psutil',
        'pygame': 'pygame',
        'numpy': 'numpy'
    }
    
    missing = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} - NOT INSTALLED")
            missing.append(package_name)
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("Install them with: pip install " + " ".join(missing))
        return False
    
    return True

def build_exe():
    """Build the portable EXE file"""
    print("\n🔨 Building LaptopTester Pro...")
    
    # Build arguments
    args = [
        'main_enhanced_auto.py',
        '--name=LaptopTesterPro_v2.7.2',
        '--onefile',
        '--windowed',
        '--noconsole',
        '--clean',
        
        # Icon (if exists)
        # '--icon=assets/icons/logo.ico',
        
        # Add data files
        '--add-data=config.json;.',
        
        # Hidden imports
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=psutil',
        '--hidden-import=pygame',
        '--hidden-import=numpy',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=datetime',
        '--hidden-import=json',
        '--hidden-import=webbrowser',
        '--hidden-import=threading',
        '--hidden-import=multiprocessing',
        '--hidden-import=subprocess',
        '--hidden-import=platform',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=time',
        '--hidden-import=random',
        '--hidden-import=math',
        
        # Collect all for CustomTkinter
        '--collect-all=customtkinter',
        
        # Optimization
        '--strip',
        '--optimize=2',
        
        # Note: --win-private-assemblies removed in PyInstaller v6.0
        # '--win-private-assemblies',
        # '--win-no-prefer-redirects',
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ Build completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False

def create_distribution_folder():
    """Create a distribution folder with the EXE and necessary files"""
    print("\n📁 Creating distribution folder...")
    
    dist_folder = Path("LaptopTesterPro_Portable")
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir(exist_ok=True)
    
    # Copy EXE file
    exe_name = "LaptopTesterPro_v2.7.2.exe"
    if os.path.exists(f"dist/{exe_name}"):
        shutil.copy(f"dist/{exe_name}", dist_folder / exe_name)
        print(f"  ✅ Copied {exe_name}")
    else:
        print(f"  ⚠️ EXE file not found: {exe_name}")
        return False
    
    # Copy config.json if exists
    if os.path.exists("config.json"):
        shutil.copy("config.json", dist_folder / "config.json")
        print(f"  ✅ Copied config.json")
    
    # Create README
    readme_content = """# LaptopTester Pro v2.7.2 - Portable Edition

## 🚀 Cách sử dụng / How to Use

1. Chạy file `LaptopTesterPro_v2.7.2.exe`
2. Chọn chế độ kiểm tra (Cơ bản / Chuyên gia / Riêng lẻ)
3. Làm theo hướng dẫn trên màn hình
4. Xem báo cáo kết quả

## 📋 Yêu cầu hệ thống / System Requirements

- Windows 10/11 64-bit
- 4GB RAM (khuyến nghị 8GB)
- 500MB ổ cứng trống
- Kết nối Internet (cho một số test)

## 🌟 Tính năng / Features

- ✅ 13+ tests toàn diện
- ✅ Stress test CPU/GPU/RAM
- ✅ Báo cáo chi tiết (PDF/Excel)
- ✅ Hỗ trợ 2 ngôn ngữ (VI/EN)
- ✅ Dark mode
- ✅ Portable - không cần cài đặt

## 📞 Liên hệ / Contact

- 📍 237/1C Tôn Thất Thuyết, P. Vĩnh Hội, TPHCM
- 📱 Hotline: 0931.78.79.32
- 🌐 Facebook: fb.com/maytinh371nguyenkiem
- 🛒 Shopee: s.shopee.vn/7AUkbxe8uu

## 📄 Giấy phép / License

Copyright © 2025 Laptop Lê Ẩn & Gemini AI
All rights reserved.

---

*Version: 2.7.2*
*Build Date: 15/10/2025*
"""
    
    with open(dist_folder / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  ✅ Created README.txt")
    
    # Create a batch file to run the app
    batch_content = """@echo off
echo Starting LaptopTester Pro...
LaptopTesterPro_v2.7.2.exe
"""
    
    with open(dist_folder / "Run_LaptopTester.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    print("  ✅ Created Run_LaptopTester.bat")
    
    return True

def main():
    """Main build process"""
    print("=" * 60)
    print("🖥️  LaptopTester Pro - Portable EXE Builder")
    print("    Version: 2.7.2")
    print("    Date: 15/10/2025")
    print("=" * 60)
    
    # Step 1: Check requirements
    if not check_requirements():
        print("\n❌ Build cancelled - missing requirements")
        return False
    
    # Step 2: Clean old builds
    clean_build_folders()
    
    # Step 3: Build EXE
    if not build_exe():
        print("\n❌ Build failed")
        return False
    
    # Step 4: Create distribution folder
    if not create_distribution_folder():
        print("\n❌ Distribution folder creation failed")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 BUILD SUCCESSFUL!")
    print("=" * 60)
    print("\n📦 Output:")
    print("  → LaptopTesterPro_Portable/LaptopTesterPro_v2.7.2.exe")
    print("  → LaptopTesterPro_Portable/README.txt")
    print("  → LaptopTesterPro_Portable/Run_LaptopTester.bat")
    print("\n💡 Tip:")
    print("  - Toàn bộ folder 'LaptopTesterPro_Portable' có thể copy đi bất kỳ đâu")
    print("  - Không cần cài đặt, chạy trực tiếp file .exe")
    print("  - File .exe đã bao gồm mọi thứ cần thiết")
    print("\n🚀 Ready to distribute!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
