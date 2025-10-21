#!/usr/bin/env python3
"""
LaptopTester Health Check Script
Kiểm tra tính toàn vẹn và sẵn sàng của dự án
"""

import os
import sys
from pathlib import Path

class HealthChecker:
    def __init__(self):
        self.root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.passed = 0
        self.total = 0
    
    def check(self, name, condition, error_msg=None, warning=False):
        """Kiểm tra một điều kiện"""
        self.total += 1
        if condition:
            self.passed += 1
            print(f"[OK] {name}")
            return True
        else:
            msg = error_msg or f"{name} failed"
            if warning:
                self.warnings.append(msg)
                print(f"[WARN] {name}")
            else:
                self.errors.append(msg)
                print(f"[FAIL] {name}")
            return False
    
    def run(self):
        """Chạy tất cả các kiểm tra"""
        print("="*60)
        print("   LaptopTester Health Check - Kiem tra du an")
        print("="*60 + "\n")
        
        # 1. Kiểm tra file chính
        print("[FILES] Kiem tra Files Chinh:")
        self.check("main_enhanced_auto.py", 
                   (self.root / "main_enhanced_auto.py").exists(),
                   "File main không tồn tại")
        self.check("requirements.txt", 
                   (self.root / "requirements.txt").exists(),
                   "File requirements.txt không tồn tại")
        self.check("README.md", 
                   (self.root / "README.md").exists(),
                   "File README.md không tồn tại")
        
        # 2. Kiểm tra thư mục
        print("\n[FOLDERS] Kiem tra Thu Muc:")
        self.check("assets/", 
                   (self.root / "assets").exists(),
                   "Thư mục assets không tồn tại")
        self.check("assets/icons/", 
                   (self.root / "assets" / "icons").exists(),
                   "Thư mục assets/icons không tồn tại")
        self.check("bin/LibreHardwareMonitor/", 
                   (self.root / "bin" / "LibreHardwareMonitor").exists(),
                   "LibreHardwareMonitor không tồn tại", warning=True)
        self.check("workers/", 
                   (self.root / "workers").exists(),
                   "Thư mục workers không tồn tại", warning=True)
        
        # 3. Kiểm tra worker files
        print("\n[WORKERS] Kiem tra Worker Files:")
        workers = ["worker_battery.py", "worker_cpu.py", "worker_disk.py", 
                   "worker_gpu.py", "worker_hw_monitor.py"]
        for worker in workers:
            self.check(worker, 
                       (self.root / worker).exists(),
                       f"Worker {worker} không tồn tại", warning=True)
        
        # 4. Kiểm tra assets
        print("\n[ASSETS] Kiem tra Assets:")
        self.check("stereo_test.mp3", 
                   (self.root / "assets" / "stereo_test.mp3").exists(),
                   "File audio test không tồn tại", warning=True)
        
        icons_dir = self.root / "assets" / "icons"
        if icons_dir.exists():
            icon_count = len(list(icons_dir.glob("*.png")))
            self.check(f"Icons ({icon_count} files)", 
                       icon_count >= 20,
                       f"Chỉ có {icon_count} icons (cần ít nhất 20)", warning=True)
        
        # 5. Kiểm tra Python syntax
        print("\n[PYTHON] Kiem tra Python Syntax:")
        try:
            import py_compile
            py_compile.compile(str(self.root / "main_enhanced_auto.py"), doraise=True)
            self.check("main_enhanced_auto.py syntax", True)
        except Exception as e:
            self.check("main_enhanced_auto.py syntax", False, str(e))
        
        # 6. Kiểm tra dependencies
        print("\n[DEPS] Kiem tra Dependencies:")
        required_packages = [
            "customtkinter", "psutil", "PIL", "cv2", 
            "pygame", "sounddevice", "keyboard"
        ]
        for package in required_packages:
            try:
                __import__(package)
                self.check(package, True)
            except ImportError:
                self.check(package, False, 
                          f"Package {package} chưa cài đặt", warning=True)
        
        # 7. Kiểm tra documentation
        print("\n[DOCS] Kiem tra Documentation:")
        docs = ["QUICKSTART.md", "LICENSE", ".gitignore"]
        for doc in docs:
            self.check(doc, 
                       (self.root / doc).exists(),
                       f"File {doc} không tồn tại", warning=True)
        
        # Tổng kết
        print("\n" + "="*60)
        print(f"[RESULTS] Ket Qua: {self.passed}/{self.total} tests passed")
        
        if self.errors:
            print(f"\n[ERROR] Loi nghiem trong ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")
        
        if self.warnings:
            print(f"\n[WARNING] Canh bao ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n[SUCCESS] Du an hoan toan san sang!")
            return 0
        elif not self.errors:
            print("\n[SUCCESS] Du an san sang (co mot so canh bao nho)")
            return 0
        else:
            print("\n[ERROR] Du an co loi can sua!")
            return 1

if __name__ == "__main__":
    checker = HealthChecker()
    sys.exit(checker.run())
