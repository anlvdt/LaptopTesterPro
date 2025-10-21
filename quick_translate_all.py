#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick translate all untranslated strings"""

# Simple translations for mode selection
quick_trans = {
    "⚙️ Chế Độ Cơ Bản": "⚙️ Basic Mode",
    "Kiểm tra nhanh\\ncác chức năng chính": "Quick check\\nof main functions",
    "▶️ CƠ BẢN": "▶️ BASIC",
    "🔥 Chế Độ Chuyên Gia": "🔥 Expert Mode",
    "Kiểm tra chuyên sâu\\nvới stress test": "In-depth testing\\nwith stress tests",
    "🔥 CHUYÊN GIA": "🔥 EXPERT",
    "🔧 Kiểm Tra Riêng Lẻ": "🔧 Individual Testing",
    "Chọn từng thành phần\\nđể kiểm tra riêng": "Select individual\\ncomponents to test",
    "🔧 RIÊNG LẺ": "🔧 INDIVIDUAL",
    "📖 Giới Thiệu": "📖 About",
    "Tìm hiểu về\\nLaptopTester Pro": "Learn about\\nLaptopTester Pro",
    "📖 GIỚI THIỆU": "📖 ABOUT",
    "📚 Hướng Dẫn": "📚 Guide",
    "Hướng dẫn sử dụng\\nchi tiết từng bước": "Detailed step-by-step\\nuser guide",
    "📚 HƯỚNG DẪN": "📚 GUIDE",
    "❌ Thoát": "❌ Exit",
    "Đóng ứng dụng\\nLaptopTester Pro": "Close\\nLaptopTester Pro",
    "❌ THOÁT": "❌ EXIT",
    "🎯 Chọn chế độ kiểm tra phù hợp:": "🎯 Select appropriate test mode:",
    "Kiểm tra laptop toàn diện - Chuyên nghiệp": "Comprehensive Laptop Testing - Professional",
    "💻 Phát triển bởi: Laptop Lê Ẩn & Gemini AI": "💻 Developed by: Laptop Lê Ẩn & Gemini AI",
}

# Read lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace
for vi, en in quick_trans.items():
    vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"')
    en_esc = en.replace('\\', '\\\\').replace('"', '\\"')
    old = f'    "{vi_esc}": "{vi_esc}",'
    new = f'    "{vi_esc}": "{en_esc}",'
    content = content.replace(old, new)

# Write
with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Translated {len(quick_trans)} strings")
