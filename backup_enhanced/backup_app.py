#!/usr/bin/env python3
"""
Backup script cho LaptopTester
Tạo backup toàn bộ ứng dụng với timestamp
"""

import os
import shutil
import zipfile
from datetime import datetime
import sys

def create_backup():
    # Thư mục gốc của ứng dụng
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tạo tên backup với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"LaptopTester_Backup_{timestamp}"
    
    # Thư mục backup
    backup_dir = os.path.join(os.path.dirname(app_dir), backup_name)
    backup_zip = f"{backup_dir}.zip"
    
    print(f"[BACKUP] Dang sao luu LaptopTester...")
    print(f"[SOURCE] Nguon: {app_dir}")
    print(f"[TARGET] Dich: {backup_zip}")
    
    try:
        # Tạo file ZIP backup
        with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(app_dir):
                # Bỏ qua thư mục không cần thiết
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'logs', 'temp']]
                
                for file in files:
                    # Bỏ qua file không cần thiết
                    if file.endswith(('.pyc', '.pyo', '.log', '.tmp')):
                        continue
                        
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, os.path.dirname(app_dir))
                    zipf.write(file_path, arc_path)
                    print(f"  [OK] {arc_path}")
        
        # Thống kê
        backup_size = os.path.getsize(backup_zip) / (1024 * 1024)  # MB
        print(f"\n[SUCCESS] Backup hoan thanh!")
        print(f"[FILE] File: {backup_zip}")
        print(f"[SIZE] Kich thuoc: {backup_size:.2f} MB")
        
        return backup_zip
        
    except Exception as e:
        print(f"[ERROR] Loi backup: {e}")
        return None

if __name__ == "__main__":
    backup_file = create_backup()
    if backup_file:
        print(f"\n[DONE] Backup thanh cong: {backup_file}")
    else:
        print("\n[FAIL] Backup that bai!")
        sys.exit(1)