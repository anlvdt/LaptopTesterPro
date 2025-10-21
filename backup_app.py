#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaptopTester Backup Script
Sao lưu toàn bộ ứng dụng LaptopTester
"""

import os
import shutil
import zipfile
from datetime import datetime
import json

def create_backup():
    """Tạo backup toàn bộ ứng dụng"""
    
    # Thư mục gốc của ứng dụng
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tạo tên backup với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"LaptopTester_Backup_{timestamp}"
    backup_dir = os.path.join(os.path.dirname(app_dir), "Backups")
    backup_path = os.path.join(backup_dir, backup_name)
    
    # Tạo thư mục backup nếu chưa có
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"Bat dau backup ung dung LaptopTester...")
    print(f"Nguon: {app_dir}")
    print(f"Dich: {backup_path}")
    
    # Danh sách file/folder cần backup
    items_to_backup = [
        "laptoptester.py",
        "worker_*.py",
        "test_*.py", 
        "*.md",
        "requirements.txt",
        "assets/",
        "bin/",
        "logs/",
        "*.json",
        "*.txt"
    ]
    
    # Danh sách loại trừ
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo", 
        ".git",
        "venv/",
        "env/",
        "*.log",
        "temp/",
        "cache/"
    ]
    
    try:
        # Tạo backup folder
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy files và folders
        copied_files = 0
        for root, dirs, files in os.walk(app_dir):
            # Loại trừ các thư mục không cần thiết
            dirs[:] = [d for d in dirs if not any(pattern.replace('/', '') in d for pattern in exclude_patterns)]
            
            # Tính relative path
            rel_path = os.path.relpath(root, app_dir)
            if rel_path == '.':
                dest_dir = backup_path
            else:
                dest_dir = os.path.join(backup_path, rel_path)
                os.makedirs(dest_dir, exist_ok=True)
            
            # Copy files
            for file in files:
                if not any(pattern.replace('*', '') in file for pattern in exclude_patterns if '*' in pattern):
                    if not any(pattern in file for pattern in exclude_patterns if '*' not in pattern):
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(dest_dir, file)
                        shutil.copy2(src_file, dest_file)
                        copied_files += 1
        
        # Tạo backup info
        backup_info = {
            "backup_date": datetime.now().isoformat(),
            "source_path": app_dir,
            "backup_path": backup_path,
            "files_count": copied_files,
            "app_version": "LaptopTester v1.0"
        }
        
        with open(os.path.join(backup_path, "backup_info.json"), 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        # Tạo file ZIP
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arc_path)
        
        # Xóa thư mục backup (giữ lại file ZIP)
        shutil.rmtree(backup_path)
        
        # Tính kích thước backup
        backup_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
        
        print(f"Backup hoan thanh!")
        print(f"File backup: {zip_path}")
        print(f"So files: {copied_files}")
        print(f"Kich thuoc: {backup_size:.2f} MB")
        
        return zip_path
        
    except Exception as e:
        print(f"Loi backup: {str(e)}")
        return None

def restore_backup(backup_zip_path, restore_dir=None):
    """Khôi phục từ file backup"""
    
    if not os.path.exists(backup_zip_path):
        print(f"❌ File backup không tồn tại: {backup_zip_path}")
        return False
    
    if restore_dir is None:
        restore_dir = os.path.join(os.path.dirname(backup_zip_path), "Restored_LaptopTester")
    
    try:
        print(f"🔄 Khôi phục backup từ: {backup_zip_path}")
        print(f"📁 Khôi phục tới: {restore_dir}")
        
        # Tạo thư mục khôi phục
        os.makedirs(restore_dir, exist_ok=True)
        
        # Giải nén backup
        with zipfile.ZipFile(backup_zip_path, 'r') as zipf:
            zipf.extractall(restore_dir)
        
        # Đọc thông tin backup
        info_file = os.path.join(restore_dir, "backup_info.json")
        if os.path.exists(info_file):
            with open(info_file, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            print(f"📅 Ngày backup: {backup_info.get('backup_date', 'N/A')}")
            print(f"📊 Số files: {backup_info.get('files_count', 'N/A')}")
        
        print(f"✅ Khôi phục hoàn thành!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khôi phục: {str(e)}")
        return False

def list_backups():
    """Liệt kê các backup có sẵn"""
    
    app_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(os.path.dirname(app_dir), "Backups")
    
    if not os.path.exists(backup_dir):
        print("📂 Chưa có backup nào")
        return []
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith("LaptopTester_Backup_") and file.endswith(".zip"):
            file_path = os.path.join(backup_dir, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            backups.append({
                'name': file,
                'path': file_path,
                'size': file_size,
                'date': file_time
            })
    
    # Sắp xếp theo ngày (mới nhất trước)
    backups.sort(key=lambda x: x['date'], reverse=True)
    
    print(f"📋 Danh sách backup ({len(backups)} files):")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['name']}")
        print(f"   📅 {backup['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   💾 {backup['size']:.2f} MB")
        print()
    
    return backups

if __name__ == "__main__":
    # Tự động tạo backup mà không cần menu
    print("LaptopTester Backup Tool")
    print("=" * 40)
    
    backup_path = create_backup()
    if backup_path:
        print(f"\nBackup thanh cong: {backup_path}")
    else:
        print("\nBackup that bai!")
    
    input("\nNhan Enter de thoat...")
        
