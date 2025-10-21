#!/usr/bin/env python3
"""
Fast Build Script for LaptopTester
Build với tối ưu hóa khởi động
"""

import subprocess
import sys
import os

def build_optimized_exe():
    """Build EXE với tối ưu hóa khởi động"""
    
    print("Building optimized LaptopTester...")
    
    # Tạo spec file tối ưu
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_enhanced.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'customtkinter',
        'psutil', 
        'PIL',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy', 
        'cv2',
        'pygame',
        'scipy',
        'pandas'
    ],
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
    name='LaptopTester_Fast',
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
)
'''
    
    # Ghi spec file
    with open('laptoptester_fast.spec', 'w') as f:
        f.write(spec_content)
    
    # Build với spec
    cmd = [sys.executable, "-m", "PyInstaller", "laptoptester_fast.spec"]
    
    print("Building... This will be faster!")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("✅ Fast build completed!")
        print("📦 File: dist/LaptopTester_Fast.exe")
        
        # Copy to portable
        if os.path.exists("dist/LaptopTester_Fast.exe"):
            os.makedirs("LaptopTester_Portable", exist_ok=True)
            import shutil
            shutil.copy2("dist/LaptopTester_Fast.exe", "LaptopTester_Portable/LaptopTester.exe")
            print("📁 Copied to portable folder")
    else:
        print("❌ Build failed")

if __name__ == "__main__":
    build_optimized_exe()