#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build LaptopTester to EXE
Đóng gói ứng dụng thành file .exe
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller
        print("[INFO] PyInstaller đã có sẵn")
        return True
    except ImportError:
        print("[INFO] Đang cài đặt PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Không thể cài đặt PyInstaller")
            return False

def create_spec_file():
    """Tạo file .spec cho PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['laptoptester.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('bin', 'bin'),
    ],
    hiddenimports=[
        'customtkinter',
        'psutil',
        'PIL',
        'requests',
        'json',
        'threading',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LaptopTester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('laptoptester.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("[INFO] Đã tạo file laptoptester.spec")

def build_exe():
    """Build file .exe"""
    
    print("=" * 50)
    print("    LaptopTester EXE Builder")
    print("=" * 50)
    
    # Kiểm tra file chính
    if not os.path.exists('laptoptester.py'):
        print("[ERROR] Không tìm thấy laptoptester.py")
        return False
    
    # Cài đặt PyInstaller
    if not install_pyinstaller():
        return False
    
    # Tạo thư mục assets nếu chưa có
    if not os.path.exists('assets'):
        os.makedirs('assets')
        print("[INFO] Đã tạo thư mục assets")
    
    if not os.path.exists('bin'):
        os.makedirs('bin')
        print("[INFO] Đã tạo thư mục bin")
    
    # Tạo file spec
    create_spec_file()
    
    # Dọn dẹp build cũ
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    print("[INFO] Bắt đầu build EXE...")
    print("[INFO] Quá trình này có thể mất vài phút...")
    
    try:
        # Build với PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed", 
            "--name=LaptopTester",
            "--add-data=assets;assets",
            "--add-data=bin;bin",
            "--hidden-import=customtkinter",
            "--hidden-import=psutil",
            "--hidden-import=PIL",
            "--hidden-import=requests",
            "laptoptester.py"
        ]
        
        # Thêm icon nếu có
        if os.path.exists('assets/icon.ico'):
            cmd.extend(["--icon=assets/icon.ico"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            exe_path = os.path.join('dist', 'LaptopTester.exe')
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"[SUCCESS] Build thành công!")
                print(f"[INFO] File EXE: {exe_path}")
                print(f"[INFO] Kích thước: {file_size:.1f} MB")
                
                # Tạo thư mục portable
                portable_dir = "LaptopTester_Portable"
                if os.path.exists(portable_dir):
                    shutil.rmtree(portable_dir)
                os.makedirs(portable_dir)
                
                # Copy file EXE
                shutil.copy2(exe_path, portable_dir)
                
                # Tạo README
                readme_content = """# LaptopTester Portable

## Cách sử dụng:
1. Chạy LaptopTester.exe với quyền Administrator
2. Làm theo hướng dẫn trên màn hình
3. Kết quả sẽ được lưu trong thư mục logs/

## Yêu cầu:
- Windows 10/11
- Quyền Administrator (cho một số tính năng)

## Lưu ý:
- Lần đầu chạy có thể mất thời gian để khởi tạo
- Một số antivirus có thể cảnh báo false positive
- Đảm bảo có kết nối internet cho một số tính năng

Phát triển bởi LaptopTester Team
"""
                
                with open(os.path.join(portable_dir, 'README.txt'), 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                
                print(f"[INFO] Đã tạo thư mục portable: {portable_dir}/")
                return True
            else:
                print("[ERROR] Không tìm thấy file EXE sau khi build")
                return False
        else:
            print("[ERROR] Build thất bại:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Lỗi build: {e}")
        return False

if __name__ == "__main__":
    try:
        success = build_exe()
        if success:
            print("\n[SUCCESS] Hoàn thành! File EXE đã sẵn sàng để chia sẻ.")
        else:
            print("\n[ERROR] Build thất bại!")
        
        input("\nNhấn Enter để thoát...")
        
    except KeyboardInterrupt:
        print("\n[INFO] Đã hủy build")
    except Exception as e:
        print(f"\n[ERROR] Lỗi: {e}")
        input("Nhấn Enter để thoát...")