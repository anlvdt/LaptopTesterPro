#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix translations with newlines"""

NEWLINE_TRANS = {
    "Chọn từng thành phần\nđể kiểm tra riêng": "Select individual\ncomponents to test",
    "Các thông tin trên được đọc trực tiếp từ BIOS/UEFI và không thể giả mạo từ Windows.\nHãy so sánh với thông tin quảng cáo của người bán!": "Info above read directly from BIOS/UEFI, cannot be faked from Windows.\nCompare with seller's advertised specs!",
    "Hoàn thành kiểm tra!\n\nBạn có muốn thoát ứng dụng không?": "Testing completed!\n\nDo you want to exit?",
    "Hướng dẫn sử dụng\nchi tiết từng bước": "Detailed step-by-step\nuser guide",
    "Kiểm tra chuyên sâu\nvới stress test": "In-depth testing\nwith stress tests",
    "Kiểm tra nhanh\ncác chức năng chính": "Quick check\nof main functions",
    "Test sẽ hiển thị: Đen → Trắng → Đỏ → Xanh Lá → Xanh Dương\nMỗi màu 3 giây. Nhấn ESC để dừng.": "Test displays: Black → White → Red → Green → Blue\nEach color 3 seconds. Press ESC to stop.",
    "Tìm hiểu về\nLaptopTester Pro": "Learn about\nLaptopTester Pro",
    "\n❌ NHỮNG ĐIỀU CẦN TRÁNH:": "\n❌ THINGS TO AVOID:",
    "\n💡 Cách khắc phục:": "\n💡 How to fix:",
    "\n📋 CÁCH SẠC VÀ SỬ DỤNG PIN ĐÚNG CÁCH:": "\n📋 PROPER BATTERY CHARGING AND USAGE:",
    "Đóng ứng dụng\nLaptopTester Pro": "Close\nLaptopTester Pro",
    "• Di chuyển chuột/touchpad trên vùng test\n• Click trái và phải để test\n• Thử cuộn 2 ngón tay (touchpad)": "• Move mouse/touchpad on test area\n• Left and right click to test\n• Try two-finger scroll (touchpad)",
    "❌ Test âm thanh thất bại": "❌ Audio test failed",
}

# Read lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add new translations
import re
vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    # Add new entries
    new_entries = []
    for vi, en in NEWLINE_TRANS.items():
        vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_esc = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        new_entries.append(f'    "{vi_esc}": "{en_esc}",')
    
    # Insert before closing brace
    new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
    content = content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
    
    # Write
    with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added {len(NEWLINE_TRANS)} newline translations")
else:
    print("Could not find VI_TO_EN dictionary")
