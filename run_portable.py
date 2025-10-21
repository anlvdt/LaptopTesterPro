#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaptopTester Portable Runner
Chạy ứng dụng ở chế độ portable với auto-setup
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("[ERROR] Cần Python 3.8 trở lên")
        print(f"Phiên bản hiện tại: {sys.version}")
        return False
    return True

def install_package(package):
    """Cài đặt package nếu chưa có"""
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        print(f"[INFO] Đang cài đặt {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            return True
        except subprocess.CalledProcessError:
            print(f"[ERROR] Không thể cài đặt {package}")
            return False

def check_dependencies():
    """Kiểm tra và cài đặt dependencies cần thiết"""
    required_packages = [
        "customtkinter",
        "psutil", 
        "pillow",
        "requests"
    ]
    
    print("[INFO] Kiểm tra dependencies...")
    
    for package in required_packages:
        if not install_package(package):
            return False
    
    return True

def setup_directories():
    """Tạo các thư mục cần thiết"""
    dirs = ["logs", "assets", "bin"]
    
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"[INFO] Đã tạo thư mục: {dir_name}")

def run_application():
    """Chạy ứng dụng chính"""
    
    print("=" * 50)
    print("    LaptopTester - Portable Mode")
    print("=" * 50)
    
    # Kiểm tra Python
    if not check_python_version():
        input("Nhấn Enter để thoát...")
        return False
    
    # Kiểm tra file chính
    if not os.path.exists("laptoptester.py"):
        print("[ERROR] Không tìm thấy file laptoptester.py")
        input("Nhấn Enter để thoát...")
        return False
    
    # Setup môi trường
    setup_directories()
    
    # Kiểm tra dependencies
    if not check_dependencies():
        print("[ERROR] Không thể cài đặt dependencies")
        input("Nhấn Enter để thoát...")
        return False
    
    print("[INFO] Khởi động LaptopTester...")
    print()
    
    try:
        # Import và chạy ứng dụng
        import laptoptester
        return True
        
    except ImportError as e:
        print(f"[ERROR] Lỗi import: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Lỗi chạy ứng dụng: {e}")
        return False

if __name__ == "__main__":
    try:
        success = run_application()
        if not success:
            input("\nỨng dụng đã dừng. Nhấn Enter để thoát...")
    except KeyboardInterrupt:
        print("\n[INFO] Người dùng đã dừng ứng dụng")
    except Exception as e:
        print(f"\n[ERROR] Lỗi không mong muốn: {e}")
        input("Nhấn Enter để thoát...")