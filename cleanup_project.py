#!/usr/bin/env python3
"""
Cleanup Script - Dọn dẹp project LaptopTester
Xóa các files/folders không cần thiết
"""

import os
import shutil
from datetime import datetime

def cleanup_project():
    """Dọn dẹp project"""
    
    print("=" * 60)
    print("🧹 LAPTOPTESTER PROJECT CLEANUP")
    print("=" * 60)
    print()
    
    # Folders to remove
    folders_to_remove = [
        "backup_old_files",
        "backup_enhanced",
        "bak_20250828",
        "bak_20250829_nice_keyboard",
        "bak_autosave"
    ]
    
    # Files patterns to remove
    files_to_remove = [
        "test_*.py",
        "fix_*.py",
        "debug_*.py",
        "temp_*.py",
        "simple_*.py"
    ]
    
    # Old logs (older than 30 days)
    old_logs_pattern = "logs/laptoptester_202509*.log"
    
    total_saved = 0
    
    # Remove old backup folders
    print("📁 Xóa thư mục backup cũ...")
    for folder in folders_to_remove:
        if os.path.exists(folder):
            try:
                size = get_folder_size(folder)
                shutil.rmtree(folder)
                total_saved += size
                print(f"  ✅ Đã xóa: {folder} ({size/1024/1024:.1f} MB)")
            except Exception as e:
                print(f"  ❌ Lỗi xóa {folder}: {e}")
        else:
            print(f"  ⏭️  Không tồn tại: {folder}")
    
    print()
    
    # Remove test/fix files
    print("🗑️  Xóa files test/fix...")
    import glob
    for pattern in files_to_remove:
        files = glob.glob(pattern)
        for file in files:
            try:
                size = os.path.getsize(file)
                os.remove(file)
                total_saved += size
                print(f"  ✅ Đã xóa: {file}")
            except Exception as e:
                print(f"  ❌ Lỗi xóa {file}: {e}")
    
    print()
    
    # Remove old logs
    print("📝 Xóa logs cũ (tháng 9/2025)...")
    if os.path.exists("logs"):
        old_logs = glob.glob(old_logs_pattern)
        for log in old_logs:
            try:
                size = os.path.getsize(log)
                os.remove(log)
                total_saved += size
                print(f"  ✅ Đã xóa: {log}")
            except Exception as e:
                print(f"  ❌ Lỗi xóa {log}: {e}")
    
    print()
    
    # Create .gitignore
    print("📄 Tạo .gitignore...")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Logs
logs/
*.log

# Backups
backup_*/
bak_*/
*.bak

# Test files
test_*.py
fix_*.py
debug_*.py
temp_*.py

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
*.spec
build/
dist/

# Virtual env
venv/
env/
ENV/
"""
    
    try:
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print("  ✅ Đã tạo .gitignore")
    except Exception as e:
        print(f"  ❌ Lỗi tạo .gitignore: {e}")
    
    print()
    
    # Create LICENSE
    print("📜 Tạo LICENSE...")
    license_content = f"""Copyright © {datetime.now().year} LaptopTester Team

All rights reserved.

This software and associated documentation files (the "Software") are proprietary
and confidential. Unauthorized copying, distribution, or use of this Software,
via any medium, is strictly prohibited.

For licensing inquiries, please contact: support@laptoptester.com
"""
    
    try:
        with open("LICENSE", "w", encoding="utf-8") as f:
            f.write(license_content)
        print("  ✅ Đã tạo LICENSE")
    except Exception as e:
        print(f"  ❌ Lỗi tạo LICENSE: {e}")
    
    print()
    print("=" * 60)
    print(f"✅ HOÀN THÀNH! Đã tiết kiệm: {total_saved/1024/1024:.1f} MB")
    print("=" * 60)
    print()
    print("📦 Các files quan trọng vẫn còn:")
    print("  ✅ main_enhanced_auto.py")
    print("  ✅ worker_*.py")
    print("  ✅ assets/")
    print("  ✅ bin/")
    print("  ✅ Documentation")
    print("  ✅ Backup .zip files")
    print()

def get_folder_size(folder):
    """Tính kích thước folder"""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
    except:
        pass
    return total

if __name__ == "__main__":
    print()
    response = input("⚠️  Bạn có chắc muốn dọn dẹp project? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        cleanup_project()
    else:
        print("❌ Đã hủy cleanup")
