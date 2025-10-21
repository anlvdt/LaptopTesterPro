#!/usr/bin/env python3
"""
Script to automatically fix hardcoded Vietnamese text in main.py
"""

import re

# Dictionary of hardcoded Vietnamese text to replace
replacements = {
    # Common hardcoded text
    '"Đang kiểm tra..."': 'get_text("checking")',
    '"Đang đọc..."': 'get_text("loading")',
    '"Sẵn sàng để bắt đầu."': 'get_text("ready_to_test")',
    '"Bắt đầu Test"': 'get_text("start_test_btn")',
    '"Dừng Test"': 'get_text("stop_test_btn")',
    '"Hoàn thành."': 'get_text("finished")',
    '"Test đã hoàn thành"': 'get_text("test_completed")',
    
    # Button texts
    '"✓ All Good"': 'f"✓ {get_text(\'all_good\')}"',
    '"✗ Issues Found"': 'f"✗ {get_text(\'issues_found\')}"',
    '"✓ Config Match"': 'f"✓ {get_text(\'config_match\')}"',
    '"✗ Mismatch"': 'f"✗ {get_text(\'mismatch\')}"',
    '"✓ Screen OK"': 'f"✓ {get_text(\'screen_ok\')}"',
    '"✗ Screen Issues"': 'f"✗ Screen Issues"',
    '"✓ Input OK"': 'f"✓ {get_text(\'input_ok\')}"',
    '"✗ Input Issues"': 'f"✗ Input Issues"',
    '"✓ Audio Clear"': 'f"✓ {get_text(\'audio_clear\')}"',
    '"✗ Audio Issues"': 'f"✗ Audio Issues"',
    '"✓ Webcam OK"': 'f"✓ {get_text(\'webcam_ok\')}"',
    '"✗ Webcam Issues"': 'f"✗ Webcam Issues"',
    '"CPU hoạt động tốt"': 'get_text("cpu_good")',
    '"GPU hoạt động tốt"': 'get_text("gpu_good")',
    '"Tốc độ tốt"': 'get_text("speed_good")',
    '"Skip"': 'get_text("skip")',
    
    # Test descriptions
    '"Kiểm tra bản quyền đã hoàn thành. Bạn có muốn tiếp tục?"': 'get_text("test_completed") + ". " + get_text("continue") + "?"',
    '"Cấu hình có khớp với thông tin quảng cáo không?"': '"Config matches advertised specs?" if CURRENT_LANG == "en" else "Cấu hình có khớp với thông tin quảng cáo không?"',
    '"Ổ cứng có hoạt động tốt không?"': '"Hard drives working properly?" if CURRENT_LANG == "en" else "Ổ cứng có hoạt động tốt không?"',
    '"Bạn có phát hiện điểm chết, hở sáng, ám màu hay chớp giật bất thường không?"': '"Any dead pixels, backlight bleeding, or flickering detected?" if CURRENT_LANG == "en" else "Bạn có phát hiện điểm chết, hở sáng, ám màu hay chớp giật bất thường không?"',
    '"Bàn phím, touchpad và chuột có hoạt động tốt không?"': '"Keyboard, touchpad and mouse working properly?" if CURRENT_LANG == "en" else "Bàn phím, touchpad và chuột có hoạt động tốt không?"',
    '"Loa và micro hoạt động bình thường không?"': '"Speakers and microphone working normally?" if CURRENT_LANG == "en" else "Loa và micro hoạt động bình thường không?"',
    '"Webcam có hoạt động bình thường không?"': '"Webcam working normally?" if CURRENT_LANG == "en" else "Webcam có hoạt động bình thường không?"',
}

def fix_language_file():
    """Read main.py, apply replacements, and write back"""
    
    # Read the file
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply replacements
    for old_text, new_text in replacements.items():
        content = content.replace(old_text, new_text)
    
    # Write back
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Language fixes applied successfully!")
    print(f"Applied {len(replacements)} replacements")

if __name__ == "__main__":
    fix_language_file()