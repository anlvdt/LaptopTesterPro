#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

def fix_main_language_issues():
    """Sửa các vấn đề ngôn ngữ chính trong file laptoptester.py"""
    
    # Đọc file
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Thêm các từ khóa thiếu vào từ điển tiếng Việt
    vi_additions = '''        # Additional UI elements
        "run_test": "Chạy Test",
        "stop_test": "Dừng Test",
        "ready": "Sẵn sàng",
        "running": "Đang chạy",
        "completed": "Hoàn thành",
        "stopped": "Đã dừng",
        "testing": "Đang test",
        "analyzing": "Đang phân tích",
        "loading": "Đang tải",
        "processing": "Đang xử lý",
        "refresh": "Làm mới",
        "clear": "Xóa",
        "save": "Lưu",
        "load": "Tải",
        "temperature": "Nhiệt độ",
        "frequency": "Tần số",
        "power": "Công suất",
        "speed": "Tốc độ",
        "excellent": "Xuất sắc",
        "very_good": "Rất tốt",
        "fair": "Trung bình",
        "poor": "Kém",
        "unknown": "Không rõ",
        "not_available": "Không có",
        "benchmark": "Đánh giá hiệu năng",
        "stress_test": "Test căng thẳng",
        "performance": "Hiệu năng",'''
    
    # Thêm các từ khóa thiếu vào từ điển tiếng Anh
    en_additions = '''        # Additional UI elements
        "run_test": "Run Test",
        "stop_test": "Stop Test",
        "ready": "Ready",
        "running": "Running",
        "completed": "Completed",
        "stopped": "Stopped",
        "testing": "Testing",
        "analyzing": "Analyzing",
        "loading": "Loading",
        "processing": "Processing",
        "refresh": "Refresh",
        "clear": "Clear",
        "save": "Save",
        "load": "Load",
        "temperature": "Temperature",
        "frequency": "Frequency",
        "power": "Power",
        "speed": "Speed",
        "excellent": "Excellent",
        "very_good": "Very Good",
        "fair": "Fair",
        "poor": "Poor",
        "unknown": "Unknown",
        "not_available": "Not Available",
        "benchmark": "Benchmark",
        "stress_test": "Stress Test",
        "performance": "Performance",'''
    
    # Tìm và chèn vào từ điển tiếng Việt
    vi_pos = content.find('        # Headers\n        "step": "Bước"')
    if vi_pos != -1:
        content = content[:vi_pos] + vi_additions + '\n        ' + content[vi_pos:]
    
    # Tìm và chèn vào từ điển tiếng Anh (cập nhật vị trí)
    en_pos = content.find('        # Headers\n        "step": "Step"')
    if en_pos != -1:
        content = content[:en_pos] + en_additions + '\n        ' + content[en_pos:]
    
    # Sửa một số chuỗi hardcode phổ biến
    simple_replacements = [
        ('"Bắt đầu Test"', 'get_text("run_test")'),
        ('"Dừng Test"', 'get_text("stop_test")'),
        ('"Sẵn sàng test"', 'get_text("ready")'),
        ('"Đang test"', 'get_text("testing")'),
        ('"Test hoàn thành"', 'get_text("completed")'),
        ('"Làm mới"', 'get_text("refresh")'),
        ('"Xóa"', 'get_text("clear")'),
    ]
    
    for old, new in simple_replacements:
        content = content.replace(old, new)
    
    # Ghi lại file
    with open("laptoptester.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK - Updated laptoptester.py with language fixes")

def main():
    print("Starting language fixes...")
    
    try:
        fix_main_language_issues()
        print("Language fixes completed successfully!")
        print("Please restart the application to see changes.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()