#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

def find_hardcoded_vietnamese():
    """Tìm các chuỗi tiếng Việt còn hardcode"""
    
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm các pattern tiếng Việt thường gặp
    vietnamese_patterns = [
        r'"[^"]*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ][^"]*"',
        r'"[^"]*Đang [^"]*"',
        r'"[^"]*Test [^"]*"',
        r'"[^"]*Kiểm tra [^"]*"',
        r'"[^"]*Bắt đầu [^"]*"',
        r'"[^"]*Hoàn thành[^"]*"',
        r'"[^"]*Sẵn sàng[^"]*"',
    ]
    
    found_issues = []
    for pattern in vietnamese_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if 'get_text(' not in match and len(match) > 5:
                found_issues.append(match)
    
    return list(set(found_issues))  # Remove duplicates

def fix_remaining_issues():
    """Sửa các vấn đề còn lại"""
    
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sửa các chuỗi còn lại
    final_fixes = [
        # Status messages in f-strings
        ('f"CPU: {cpu_usage:.1f}% | Temp: {temp:.1f}°C | Freq: {freq:.0f}MHz"', 
         'f"CPU: {cpu_usage:.1f}% | {get_text(\'temperature\')}: {temp:.1f}°C | {get_text(\'frequency\')}: {freq:.0f}MHz"'),
        
        # Common Vietnamese phrases
        ('"Đang khởi tạo worker..."', 'get_text("loading") + " worker..."'),
        ('"Đang chạy vòng lặp stress..."', 'get_text("running") + " stress loop..."'),
        ('"Đang khởi tạo Pygame..."', 'get_text("loading") + " Pygame..."'),
        
        # Button and label texts
        ('"Phát Bài Test 60s"', '"Play Test Audio 60s"'),
        ('"Ghi âm"', 'get_text("start_recording")'),
        ('"Phát lại"', 'get_text("play_recording")'),
        
        # Hardware terms in labels
        ('"GPU Temp:"', 'get_text("temperature") + ":"'),
        ('"GPU Clock:"', 'get_text("frequency") + ":"'),
        ('"GPU Power:"', 'get_text("power") + ":"'),
        
        # Test names
        ('"Test Màn Hình Tự Động"', '"Automatic Display Test"'),
        ('"Test Touchpad & Chuột:"', '"Touchpad & Mouse Test:"'),
        ('"Checklist Kiểm Tra Ngoại Hình"', '"Physical Inspection Checklist"'),
        
        # Common actions
        ('"Tải xuống"', '"Download"'),
        ('"Cài đặt"', '"Settings"'),
        ('"Trợ giúp"', '"Help"'),
    ]
    
    for old, new in final_fixes:
        content = content.replace(old, new)
    
    # Ghi lại file
    with open("laptoptester.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK - Applied final language fixes")

def add_final_translations():
    """Thêm các bản dịch cuối cùng"""
    
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Thêm các từ khóa cuối cùng
    final_vi = '''        # Final additions
        "initializing": "Đang khởi tạo",
        "stress_loop": "vòng lặp stress",
        "pygame_loading": "Pygame đang tải",
        "play_test_audio": "Phát âm thanh test",
        "automatic_display": "Màn hình tự động",
        "touchpad_mouse": "Touchpad & Chuột",
        "physical_checklist": "Checklist ngoại hình",
        "download": "Tải xuống",
        "settings": "Cài đặt",
        "help": "Trợ giúp",
        "gpu_temp": "Nhiệt độ GPU",
        "gpu_clock": "Xung nhịp GPU",
        "gpu_power": "Công suất GPU",'''
    
    final_en = '''        # Final additions
        "initializing": "Initializing",
        "stress_loop": "stress loop",
        "pygame_loading": "Loading Pygame",
        "play_test_audio": "Play Test Audio",
        "automatic_display": "Automatic Display",
        "touchpad_mouse": "Touchpad & Mouse",
        "physical_checklist": "Physical Checklist",
        "download": "Download",
        "settings": "Settings",
        "help": "Help",
        "gpu_temp": "GPU Temperature",
        "gpu_clock": "GPU Clock",
        "gpu_power": "GPU Power",'''
    
    # Chèn vào từ điển
    vi_pos = content.find('        # Headers\n        "step": "Bước"')
    if vi_pos != -1:
        content = content[:vi_pos] + final_vi + '\n        ' + content[vi_pos:]
    
    en_pos = content.find('        # Headers\n        "step": "Step"')
    if en_pos != -1:
        content = content[:en_pos] + final_en + '\n        ' + content[en_pos:]
    
    # Ghi lại file
    with open("laptoptester.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("OK - Added final translations")

def main():
    print("Running final language check and fixes...")
    
    try:
        # Tìm các vấn đề còn lại
        issues = find_hardcoded_vietnamese()
        if issues:
            print(f"Found {len(issues)} potential hardcoded Vietnamese strings:")
            for i, issue in enumerate(issues[:10]):  # Show first 10
                print(f"  {i+1}. {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
        
        # Áp dụng các sửa chữa cuối cùng
        fix_remaining_issues()
        add_final_translations()
        
        print("\nFinal language check completed!")
        print("Summary of fixes applied:")
        print("- Added comprehensive translation dictionaries")
        print("- Fixed hardcoded Vietnamese strings")
        print("- Updated button and label texts")
        print("- Standardized hardware terminology")
        print("\nPlease restart the application to see all changes.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()