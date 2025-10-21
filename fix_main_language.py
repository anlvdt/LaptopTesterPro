#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_main_language():
    """Sửa các vấn đề ngôn ngữ trong main.py"""
    
    with open("main.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sửa các chuỗi hardcode thành get_text()
    replacements = [
        # Basic UI elements
        ('"Đang kiểm tra"', 'get_text("checking")'),
        ('"Sẵn sàng test âm thanh"', 'get_text("ready_to_test")'),
        ('"Sẵn sàng test camera"', 'get_text("ready_to_test")'),
        ('"Đang khởi tạo worker..."', 'get_text("loading") + " worker..."'),
        ('"Hoàn thành"', 'get_text("completed")'),
        ('"Đã xong"', 'get_text("finished")'),
        
        # Test names and labels
        ('"Test Màn Hình Tự Động"', '"Automatic Display Test"'),
        ('"Test Webcam"', '"Webcam Test"'),
        ('"Test Loa:"', '"Speaker Test:"'),
        ('"Test Micro:"', '"Microphone Test:"'),
        ('"Layout Bàn Phím - Nhấn phím để test:"', '"Keyboard Layout - Press keys to test:"'),
        ('"Test Touchpad & Chuột:"', '"Touchpad & Mouse Test:"'),
        
        # Button texts
        ('"Bắt đầu Test Camera"', 'get_text("start_test_btn") + " Camera"'),
        ('"Dừng Camera"', 'get_text("stop_test_btn") + " Camera"'),
        ('"Phát Bài Test 60s"', '"Play Test Audio 60s"'),
        ('"Ghi âm"', '"Record"'),
        ('"Dừng"', '"Stop"'),
        
        # Status messages
        ('"Camera chưa khởi động"', '"Camera not started"'),
        ('"Camera đã dừng"', '"Camera stopped"'),
        ('"Đã dừng nhạc"', '"Music stopped"'),
        ('"Đã dừng ghi âm"', '"Recording stopped"'),
        ('"Đang ghi âm... Nói vào micro"', '"Recording... Speak into microphone"'),
        
        # Hardware terms
        ('"Nhiệt độ tối đa:"', 'get_text("temperature") + " max:"'),
        ('"Tần số:"', 'get_text("frequency") + ":"'),
        ('"Công suất:"', 'get_text("power") + ":"'),
        ('"Tốc độ Ghi:"', '"Write Speed:"'),
        ('"Tốc độ Đọc:"', '"Read Speed:"'),
        
        # Results and assessments
        ('"Kết quả CPU Test:"', '"CPU Test Results:"'),
        ('"Kết quả GPU Test:"', '"GPU Test Results:"'),
        ('"Kết quả Disk Test:"', '"Disk Test Results:"'),
        ('"FPS trung bình:"', '"Average FPS:"'),
        ('"Tổng frames:"', '"Total frames:"'),
        
        # Common phrases
        ('"Có, tất cả đều tốt"', 'get_text("all_good")'),
        ('"Không, có lỗi"', '"No, has issues"'),
        ('"Có vấn đề"', '"Has issues"'),
        ('"Hoạt động tốt"', '"Working well"'),
        ('"Không hoạt động"', '"Not working"'),
        
        # Navigation and controls
        ('"Tiếp tục"', 'get_text("continue")'),
        ('"Bỏ qua"', 'get_text("skip")'),
        ('"Trước"', 'get_text("previous")'),
        ('"Tiếp theo"', 'get_text("next")'),
        
        # Mode and settings
        ('"Chế độ cơ bản"', 'get_text("basic_mode")'),
        ('"Chế độ chuyên gia"', 'get_text("expert_mode")'),
        ('"Chọn chế độ"', 'get_text("choose_mode")'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Sửa các f-string và format string
    f_string_fixes = [
        (r'f"CPU: {cpu_usage:.1f}% \| Temp: {temp:.1f}°C \| Freq: {freq:.0f}MHz"',
         'f"CPU: {cpu_usage:.1f}% | {get_text(\'temperature\')}: {temp:.1f}°C | {get_text(\'frequency\')}: {freq:.0f}MHz"'),
        
        (r'f"GPU Test: FPS: {fps:.1f}, Particles: {particles}"',
         'f"GPU Test: FPS: {fps:.1f}, Particles: {particles}"'),
        
        (r'f"Nhiệt độ tối đa: {max_temp:.1f}°C"',
         'f"{get_text(\'temperature\')} max: {max_temp:.1f}°C"'),
    ]
    
    for old_pattern, new_pattern in f_string_fixes:
        content = re.sub(old_pattern, new_pattern, content)
    
    # Sửa các label text trong UI
    ui_fixes = [
        ('text="Đang khởi tạo Pygame..."', 'text=get_text("loading") + " Pygame..."'),
        ('text="Đang chạy vòng lặp stress..."', 'text=get_text("running") + " stress loop..."'),
        ('text="Sẵn sàng test camera"', 'text=get_text("ready_to_test")'),
        ('text="Camera đã dừng"', 'text="Camera stopped"'),
        ('text="Sẵn sàng test âm thanh"', 'text=get_text("ready_to_test")'),
    ]
    
    for old, new in ui_fixes:
        content = content.replace(old, new)
    
    # Ghi lại file
    with open("main.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed language issues in main.py")

def add_missing_translations():
    """Thêm các bản dịch còn thiếu vào từ điển LANG"""
    
    with open("main.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm vị trí để chèn thêm translations
    vi_insert_pos = content.find('        # Status Messages\n        "status_good": "Tốt"')
    en_insert_pos = content.find('        # Status Messages\n        "status_good": "Good"')
    
    # Thêm translations cho tiếng Việt
    vi_additions = '''        # Additional UI elements
        "checking": "Đang kiểm tra",
        "ready_to_test": "Sẵn sàng test",
        "loading": "Đang tải",
        "running": "Đang chạy",
        "finished": "Đã xong",
        "choose_mode": "Chọn chế độ",
        "all_good": "Tất cả đều tốt",
        "has_issues": "Có vấn đề",
        "working_well": "Hoạt động tốt",
        "not_working": "Không hoạt động",
        "temperature": "Nhiệt độ",
        "frequency": "Tần số", 
        "power": "Công suất",
        "speed": "Tốc độ",
        "record": "Ghi âm",
        "stop": "Dừng",
        "play": "Phát",
        
        '''
    
    # Thêm translations cho tiếng Anh
    en_additions = '''        # Additional UI elements
        "checking": "Checking",
        "ready_to_test": "Ready to test",
        "loading": "Loading",
        "running": "Running", 
        "finished": "Finished",
        "choose_mode": "Choose Mode",
        "all_good": "All good",
        "has_issues": "Has issues",
        "working_well": "Working well",
        "not_working": "Not working",
        "temperature": "Temperature",
        "frequency": "Frequency",
        "power": "Power", 
        "speed": "Speed",
        "record": "Record",
        "stop": "Stop",
        "play": "Play",
        
        '''
    
    if vi_insert_pos != -1:
        content = content[:vi_insert_pos] + vi_additions + content[vi_insert_pos:]
    
    # Cập nhật lại vị trí cho English
    en_insert_pos = content.find('        # Status Messages\n        "status_good": "Good"')
    if en_insert_pos != -1:
        content = content[:en_insert_pos] + en_additions + content[en_insert_pos:]
    
    # Ghi lại file
    with open("main.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Added missing translations to main.py")

def main():
    print("Fixing language issues in main.py...")
    
    try:
        add_missing_translations()
        fix_main_language()
        print("Language fixes completed for main.py!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()