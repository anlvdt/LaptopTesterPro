#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

def fix_step_specific_issues():
    """Sửa các vấn đề ngôn ngữ cụ thể trong từng bước"""
    
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sửa các text trong các step classes
    step_fixes = [
        # CPU Test Step
        ('text="Bắt đầu Test Màn Hình"', 'text=get_text("run_test") + " " + get_text("display_test")'),
        ('text="Bắt đầu Test Camera"', 'text=get_text("run_test") + " Camera"'),
        ('text="Dừng Camera"', 'text=get_text("stop_test") + " Camera"'),
        
        # Common button texts
        ('text="Bắt đầu Test"', 'text=get_text("run_test")'),
        ('text="Dừng Test"', 'text=get_text("stop_test")'),
        ('text="Test Màn Hình"', 'text=get_text("display_test")'),
        ('text="Test CPU"', 'text="CPU Test"'),
        ('text="Test GPU"', 'text="GPU Test"'),
        
        # Status messages
        ('text="Sẵn sàng test"', 'text=get_text("ready")'),
        ('text="Đang test"', 'text=get_text("testing")'),
        ('text="Test hoàn thành"', 'text=get_text("completed")'),
        ('text="Đã dừng"', 'text=get_text("stopped")'),
        
        # Hardware terms
        ('text="Nhiệt độ"', 'text=get_text("temperature")'),
        ('text="Tần số"', 'text=get_text("frequency")'),
        ('text="Công suất"', 'text=get_text("power")'),
        ('text="Tốc độ"', 'text=get_text("speed")'),
        
        # Actions
        ('text="Làm mới"', 'text=get_text("refresh")'),
        ('text="Xóa vết vẽ"', 'text=get_text("clear")'),
        
        # Results
        ('text="Xuất sắc"', 'text=get_text("excellent")'),
        ('text="Rất tốt"', 'text=get_text("very_good")'),
        ('text="Trung bình"', 'text=get_text("fair")'),
        ('text="Kém"', 'text=get_text("poor")'),
    ]
    
    for old, new in step_fixes:
        content = content.replace(old, new)
    
    # Sửa các label text
    label_fixes = [
        ('text="Test Tốc Độ Ổ Cứng"', 'text="Hard Drive Speed Test"'),
        ('text="Test Webcam"', 'text="Webcam Test"'),
        ('text="Test Màn Hình Tự Động"', 'text="Automatic Display Test"'),
        ('text="Test Touchpad & Chuột:"', 'text="Touchpad & Mouse Test:"'),
        ('text="Checklist Cổng Kết Nối:"', 'text="Ports Connectivity Checklist:"'),
        ('text="Thông Tin Pin Chi Tiết:"', 'text="Detailed Battery Information:"'),
        ('text="Test Loa:"', 'text="Speaker Test:"'),
        ('text="Test Micro với Biểu Đồ Sóng Âm:"', 'text="Microphone Test with Waveform:"'),
    ]
    
    for old, new in label_fixes:
        content = content.replace(old, new)
    
    # Ghi lại file
    with open("laptoptester.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK - Fixed step-specific language issues")

def add_more_translations():
    """Thêm nhiều bản dịch hơn vào từ điển"""
    
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Thêm vào từ điển tiếng Việt
    more_vi = '''        # Test step names
        "hardware_fingerprint": "Định danh phần cứng",
        "license_check": "Kiểm tra bản quyền",
        "system_configuration": "Cấu hình hệ thống",
        "hard_drive_health": "Sức khỏe ổ cứng",
        "display_test": "Kiểm tra màn hình",
        "keyboard_touchpad": "Bàn phím & Touchpad",
        "ports_connectivity": "Cổng kết nối",
        "battery_health": "Pin laptop",
        "speaker_microphone": "Loa & Micro",
        "webcam_test": "Webcam",
        "network_wifi": "Mạng & WiFi",
        "cpu_stress": "CPU Stress Test",
        "hard_drive_speed": "Tốc độ ổ cứng",
        "gpu_stress": "GPU Stress Test",
        "thermal_monitor": "Thermal Monitor",
        "bios_check": "Kiểm tra BIOS",
        "physical_inspection": "Kiểm tra ngoại hình",
        
        # Common test actions
        "start_camera": "Bắt đầu Camera",
        "stop_camera": "Dừng Camera",
        "start_recording": "Bắt đầu ghi âm",
        "stop_recording": "Dừng ghi âm",
        "play_recording": "Phát lại",
        "clear_canvas": "Xóa vết vẽ",
        "run_benchmark": "Chạy Benchmark",
        
        # Hardware status
        "working_well": "Hoạt động tốt",
        "has_issues": "Có vấn đề",
        "not_working": "Không hoạt động",
        "needs_attention": "Cần chú ý",'''
    
    # Thêm vào từ điển tiếng Anh
    more_en = '''        # Test step names
        "hardware_fingerprint": "Hardware Fingerprint",
        "license_check": "License Check",
        "system_configuration": "System Configuration",
        "hard_drive_health": "Hard Drive Health",
        "display_test": "Display Test",
        "keyboard_touchpad": "Keyboard & Touchpad",
        "ports_connectivity": "Ports Connectivity",
        "battery_health": "Battery Health",
        "speaker_microphone": "Speaker & Microphone",
        "webcam_test": "Webcam Test",
        "network_wifi": "Network & WiFi",
        "cpu_stress": "CPU Stress Test",
        "hard_drive_speed": "Hard Drive Speed",
        "gpu_stress": "GPU Stress Test",
        "thermal_monitor": "Thermal Monitor",
        "bios_check": "BIOS Check",
        "physical_inspection": "Physical Inspection",
        
        # Common test actions
        "start_camera": "Start Camera",
        "stop_camera": "Stop Camera",
        "start_recording": "Start Recording",
        "stop_recording": "Stop Recording",
        "play_recording": "Play Recording",
        "clear_canvas": "Clear Canvas",
        "run_benchmark": "Run Benchmark",
        
        # Hardware status
        "working_well": "Working Well",
        "has_issues": "Has Issues",
        "not_working": "Not Working",
        "needs_attention": "Needs Attention",'''
    
    # Tìm vị trí để chèn (sau các additions trước đó)
    vi_pos = content.find('        # Headers\n        "step": "Bước"')
    if vi_pos != -1:
        content = content[:vi_pos] + more_vi + '\n        ' + content[vi_pos:]
    
    en_pos = content.find('        # Headers\n        "step": "Step"')
    if en_pos != -1:
        content = content[:en_pos] + more_en + '\n        ' + content[en_pos:]
    
    # Ghi lại file
    with open("laptoptester.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK - Added more translations to dictionary")

def main():
    print("Fixing step-specific language issues...")
    
    try:
        fix_step_specific_issues()
        add_more_translations()
        print("Step language fixes completed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()