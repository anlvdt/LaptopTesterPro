#!/usr/bin/env python3
"""
LaptopTester Backup Script
Sao lưu toàn bộ ứng dụng với timestamp
"""

import os
import shutil
import datetime
import zipfile

def backup_app():
    # Thư mục gốc
    source_dir = os.path.dirname(__file__)
    
    # Tạo tên backup với timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"LaptopTester_Backup_{timestamp}"
    
    # Thư mục backup
    backup_dir = os.path.join(os.path.dirname(source_dir), backup_name)
    
    print(f"Dang sao luu tu: {source_dir}")
    print(f"Den: {backup_dir}")
    
    # Copy toàn bộ thư mục
    shutil.copytree(source_dir, backup_dir, ignore=shutil.ignore_patterns(
        '__pycache__', '*.pyc', '*.pyo', '.git', 'logs', '*.tmp'
    ))
    
    # Tạo file ZIP
    zip_path = f"{backup_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, backup_dir)
                zipf.write(file_path, arc_path)
    
    # Xóa thư mục tạm
    shutil.rmtree(backup_dir)
    
    print(f"Backup hoan thanh: {zip_path}")
    print(f"Kich thuoc: {os.path.getsize(zip_path) / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    backup_app()