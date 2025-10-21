#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để sửa tất cả các chỗ chưa được dịch trong LaptopTester
"""

import os
import re

def fix_main_file():
    """Sửa file chính laptoptester.py"""
    file_path = "laptoptester.py"
    
    # Đọc file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Thêm các từ khóa còn thiếu vào từ điển
    lang_dict_vi = '''        # Test components
        "hardware_fingerprint": "Định danh phần cứng",
        "physical_inspection": "Kiểm tra ngoại hình", 
        "bios_check": "Kiểm tra BIOS",
        "network_test": "Mạng & WiFi",
        "thermal_test": "Thermal Monitor",
        "webcam_test": "Webcam",
        "microphone_test": "Kiểm tra micro",
        "speaker_test": "Loa & Micro",
        "ports_connectivity": "Cổng kết nối",
        "hard_drive_speed": "Tốc độ ổ cứng",
        
        # Status messages
        "ready": "Sẵn sàng",
        "running": "Đang chạy",
        "completed": "Hoàn thành",
        "stopped": "Đã dừng",
        "testing": "Đang test",
        "analyzing": "Đang phân tích",
        "loading": "Đang tải",
        "processing": "Đang xử lý",
        
        # Actions
        "run_test": "Chạy Test",
        "stop_test": "Dừng Test", 
        "restart": "Khởi động lại",
        "refresh": "Làm mới",
        "export": "Xuất báo cáo",
        "save": "Lưu",
        "load": "Tải",
        "reset": "Đặt lại",
        "clear": "Xóa",
        
        # Test results
        "excellent": "Xuất sắc",
        "very_good": "Rất tốt",
        "fair": "Trung bình", 
        "poor": "Kém",
        "unknown": "Không rõ",
        "not_available": "Không có",
        "not_supported": "Không hỗ trợ",
        
        # Hardware terms
        "temperature": "Nhiệt độ",
        "frequency": "Tần số",
        "voltage": "Điện áp",
        "power": "Công suất",
        "usage": "Sử dụng",
        "load": "Tải",
        "speed": "Tốc độ",
        "capacity": "Dung lượng",
        "health": "Sức khỏe",
        "cycles": "Chu kỳ",
        
        # Time units
        "seconds": "giây",
        "minutes": "phút", 
        "hours": "giờ",
        "days": "ngày",
        
        # File operations
        "file_not_found": "Không tìm thấy file",
        "permission_denied": "Không có quyền truy cập",
        "disk_full": "Đĩa đầy",
        "invalid_format": "Định dạng không hợp lệ",
        
        # Network
        "connected": "Đã kết nối",
        "disconnected": "Mất kết nối", 
        "connecting": "Đang kết nối",
        "timeout": "Hết thời gian chờ",
        "ping": "Ping",
        "download": "Tải xuống",
        "upload": "Tải lên",
        
        # Common UI
        "close": "Đóng",
        "minimize": "Thu nhỏ",
        "maximize": "Phóng to",
        "settings": "Cài đặt",
        "help": "Trợ giúp",
        "about": "Giới thiệu",
        "version": "Phiên bản",
        "update": "Cập nhật",
        
        # Test specific
        "benchmark": "Đánh giá hiệu năng",
        "stress_test": "Test căng thẳng",
        "stability_test": "Test ổn định",
        "performance": "Hiệu năng",
        "compatibility": "Tương thích",
        "reliability": "Độ tin cậy"'''
    
    lang_dict_en = '''        # Test components  
        "hardware_fingerprint": "Hardware Fingerprint",
        "physical_inspection": "Physical Inspection",
        "bios_check": "BIOS Check", 
        "network_test": "Network & WiFi",
        "thermal_test": "Thermal Monitor",
        "webcam_test": "Webcam",
        "microphone_test": "Microphone Test",
        "speaker_test": "Speaker & Microphone", 
        "ports_connectivity": "Ports Connectivity",
        "hard_drive_speed": "Hard Drive Speed",
        
        # Status messages
        "ready": "Ready",
        "running": "Running", 
        "completed": "Completed",
        "stopped": "Stopped",
        "testing": "Testing",
        "analyzing": "Analyzing",
        "loading": "Loading",
        "processing": "Processing",
        
        # Actions
        "run_test": "Run Test",
        "stop_test": "Stop Test",
        "restart": "Restart", 
        "refresh": "Refresh",
        "export": "Export",
        "save": "Save",
        "load": "Load",
        "reset": "Reset",
        "clear": "Clear",
        
        # Test results
        "excellent": "Excellent",
        "very_good": "Very Good",
        "fair": "Fair",
        "poor": "Poor", 
        "unknown": "Unknown",
        "not_available": "Not Available",
        "not_supported": "Not Supported",
        
        # Hardware terms
        "temperature": "Temperature",
        "frequency": "Frequency",
        "voltage": "Voltage",
        "power": "Power",
        "usage": "Usage",
        "load": "Load",
        "speed": "Speed", 
        "capacity": "Capacity",
        "health": "Health",
        "cycles": "Cycles",
        
        # Time units
        "seconds": "seconds",
        "minutes": "minutes",
        "hours": "hours", 
        "days": "days",
        
        # File operations
        "file_not_found": "File not found",
        "permission_denied": "Permission denied",
        "disk_full": "Disk full",
        "invalid_format": "Invalid format",
        
        # Network
        "connected": "Connected",
        "disconnected": "Disconnected",
        "connecting": "Connecting", 
        "timeout": "Timeout",
        "ping": "Ping",
        "download": "Download",
        "upload": "Upload",
        
        # Common UI
        "close": "Close",
        "minimize": "Minimize",
        "maximize": "Maximize",
        "settings": "Settings",
        "help": "Help",
        "about": "About",
        "version": "Version",
        "update": "Update",
        
        # Test specific
        "benchmark": "Benchmark",
        "stress_test": "Stress Test", 
        "stability_test": "Stability Test",
        "performance": "Performance",
        "compatibility": "Compatibility",
        "reliability": "Reliability"'''
    
    # Tìm vị trí để chèn từ điển mới
    vi_insert_pos = content.find('        # Headers\n        "step": "Bước"')
    en_insert_pos = content.find('        # Headers\n        "step": "Step"')
    
    if vi_insert_pos != -1:
        content = content[:vi_insert_pos] + lang_dict_vi + ',\n        ' + content[vi_insert_pos:]
    
    # Cập nhật lại vị trí cho English sau khi đã chèn Vietnamese
    en_insert_pos = content.find('        # Headers\n        "step": "Step"')
    if en_insert_pos != -1:
        content = content[:en_insert_pos] + lang_dict_en + ',\n        ' + content[en_insert_pos:]
    
    # Sửa các chuỗi hardcode thành dùng get_text()
    replacements = [
        # Button texts
        (r'"Bắt đầu Test"', 'get_text("run_test")'),
        (r'"Dừng Test"', 'get_text("stop_test")'),
        (r'"Tiếp tục"', 'get_text("continue")'),
        (r'"Hoàn thành"', 'get_text("completed")'),
        (r'"Sẵn sàng"', 'get_text("ready")'),
        (r'"Đang chạy"', 'get_text("running")'),
        (r'"Đã dừng"', 'get_text("stopped")'),
        
        # Status messages  
        (r'"Đang khởi tạo"', 'get_text("loading")'),
        (r'"Đang xử lý"', 'get_text("processing")'),
        (r'"Đang phân tích"', 'get_text("analyzing")'),
        
        # Test names in buttons
        (r'"Test Màn Hình"', 'get_text("display_test")'),
        (r'"Test CPU"', 'get_text("cpu_test")'),
        (r'"Test GPU"', 'get_text("gpu_test")'),
        (r'"Test Webcam"', 'get_text("webcam_test")'),
        (r'"Test Camera"', 'get_text("webcam_test")'),
        
        # Common actions
        (r'"Làm mới"', 'get_text("refresh")'),
        (r'"Xóa"', 'get_text("clear")'),
        (r'"Lưu"', 'get_text("save")'),
        (r'"Tải"', 'get_text("load")'),
        
        # Hardware terms
        (r'"Nhiệt độ"', 'get_text("temperature")'),
        (r'"Tần số"', 'get_text("frequency")'),
        (r'"Công suất"', 'get_text("power")'),
        (r'"Tốc độ"', 'get_text("speed")'),
        
        # Results
        (r'"Xuất sắc"', 'get_text("excellent")'),
        (r'"Rất tốt"', 'get_text("very_good")'),
        (r'"Trung bình"', 'get_text("fair")'),
        (r'"Kém"', 'get_text("poor")'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    # Ghi lại file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] Da cap nhat file laptoptester.py")

def fix_worker_files():
    """Sửa các file worker"""
    
    # Worker CPU
    cpu_replacements = [
        (r'"Phát hiện \{cpu_count\} lõi CPU\. Bắt đầu stress test\.\.\."', 
         'f"Phát hiện {cpu_count} lõi CPU. Bắt đầu stress test..."'),
        (r'"Đã khởi động \{len\(workers\)\} processes"',
         'f"Đã khởi động {len(workers)} processes"'),
        (r'"Lỗi khởi động worker \{i\}: \{str\(e\)\}"',
         'f"Lỗi khởi động worker {i}: {str(e)}"'),
        (r'"⚠️ Nhiệt độ CPU rất cao: \{temp:\\.1f\}°C!"',
         'f"⚠️ Nhiệt độ CPU rất cao: {temp:.1f}°C!"'),
        (r'"⚠️ Công suất CPU cao: \{power:\\.1f\}W"',
         'f"⚠️ Công suất CPU cao: {power:.1f}W"'),
    ]
    
    # GPU Worker
    gpu_replacements = [
        (r'"Lỗi thiếu thư viện cho test GPU: \{e\\.name\}"',
         'f"Lỗi thiếu thư viện cho test GPU: {e.name}"'),
        (r'"Đang khởi tạo Pygame\.\.\."', '"Đang khởi tạo Pygame..."'),
        (r'"Đang chạy vòng lặp stress\.\.\."', '"Đang chạy vòng lặp stress..."'),
        (r'"Thời gian: \{current_time:\\.1f\}s / \{duration\}s"',
         'f"Thời gian: {current_time:.1f}s / {duration}s"'),
        (r'"FPS: \{fps:\\.1f\}"', 'f"FPS: {fps:.1f}"'),
        (r'"Particles: \{len\(particles\)\}"', 'f"Particles: {len(particles)}"'),
    ]
    
    # Disk Worker  
    disk_replacements = [
        (r'"Sử dụng thư mục test: \{test_dir\}"',
         'f"Sử dụng thư mục test: {test_dir}"'),
        (r'"Không đủ dung lượng trống\. Cần \{file_size_mb\}MB, còn lại \{free_space_mb:\\.0f\}MB\\."',
         'f"Không đủ dung lượng trống. Cần {file_size_mb}MB, còn lại {free_space_mb:.0f}MB."'),
        (r'"Đang ghi tuần tự file \{file_size_mb\}MB\.\.\."',
         'f"Đang ghi tuần tự file {file_size_mb}MB..."'),
        (r'"Đang đọc tuần tự file \{file_size_mb\}MB\.\.\."',
         'f"Đang đọc tuần tự file {file_size_mb}MB..."'),
    ]
    
    workers = [
        ("worker_cpu.py", cpu_replacements),
        ("worker_gpu.py", gpu_replacements), 
        ("worker_disk.py", disk_replacements)
    ]
    
    for filename, replacements in workers:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old, new in replacements:
                content = re.sub(old, new, content)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[OK] Da cap nhat {filename}")

def add_missing_translations():
    """Thêm các bản dịch còn thiếu vào file chính"""
    
    missing_translations = {
        # Test step names
        "Định danh phần cứng": "Hardware Fingerprint",
        "Bản quyền Windows": "Windows License", 
        "Cấu hình hệ thống": "System Configuration",
        "Sức khỏe ổ cứng": "Hard Drive Health",
        "Kiểm tra màn hình": "Display Test",
        "Bàn phím & Touchpad": "Keyboard & Touchpad",
        "Cổng kết nối": "Ports Connectivity",
        "Pin laptop": "Battery Health",
        "Loa & Micro": "Speaker & Microphone",
        "Webcam": "Webcam Test",
        "Mạng & WiFi": "Network & WiFi",
        "CPU Stress Test": "CPU Stress Test",
        "Tốc độ ổ cứng": "Hard Drive Speed",
        "GPU Stress Test": "GPU Stress Test", 
        "Thermal Monitor": "Thermal Monitor",
        "Kiểm tra BIOS": "BIOS Check",
        "Kiểm tra ngoại hình": "Physical Inspection",
        
        # Button texts
        "Bắt đầu Test": "Start Test",
        "Dừng Test": "Stop Test",
        "Chạy Test": "Run Test",
        "Test hoàn thành": "Test Completed",
        "Sẵn sàng test": "Ready to Test",
        "Đang test": "Testing",
        
        # Status messages
        "Đang khởi tạo": "Initializing",
        "Đang xử lý": "Processing", 
        "Đang phân tích": "Analyzing",
        "Hoàn thành": "Completed",
        "Đã dừng": "Stopped",
        "Lỗi": "Error",
        
        # Hardware terms
        "Nhiệt độ": "Temperature",
        "Tần số": "Frequency", 
        "Công suất": "Power",
        "Tốc độ": "Speed",
        "Dung lượng": "Capacity",
        "Sức khỏe": "Health",
        
        # Results
        "Xuất sắc": "Excellent",
        "Rất tốt": "Very Good",
        "Tốt": "Good", 
        "Trung bình": "Fair",
        "Kém": "Poor",
        "Không rõ": "Unknown"
    }
    
    print("[INFO] Danh sach cac ban dich can them:")
    for vi, en in missing_translations.items():
        print(f"  {vi} -> {en}")

def main():
    """Chạy tất cả các sửa chữa"""
    print("[FIX] Bat dau sua chua ngon ngu cho LaptopTester...")
    
    try:
        fix_main_file()
        fix_worker_files() 
        add_missing_translations()
        
        print("\n[OK] Hoan thanh sua chua ngon ngu!")
        print("[INFO] Nhung gi da duoc sua:")
        print("  - Them tu dien ngon ngu mo rong")
        print("  - Sua cac chuoi hardcode thanh get_text()")
        print("  - Cap nhat cac file worker")
        print("  - Chuan hoa format string")
        
        print("\n[WARNING] Luu y:")
        print("  - Khoi dong lai ung dung de thay thay doi")
        print("  - Kiem tra chuc nang chuyen ngon ngu")
        print("  - Bao cao neu con cho nao chua duoc dich")
        
    except Exception as e:
        print(f"[ERROR] Loi khi sua chua: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()