#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động tìm và thay thế tất cả chuỗi tiếng Việt
"""

import re
import sys

# Mapping tiếng Việt -> tiếng Anh
TRANSLATIONS = {
    # Common phrases
    "Đang tải...": "Loading...",
    "Đang kiểm tra...": "Checking...",
    "Đang đọc...": "Reading...",
    "Sẵn sàng": "Ready",
    "Hoàn thành": "Completed",
    "Bỏ qua": "Skip",
    "Tiếp tục": "Continue",
    "Trước": "Previous",
    "Tiếp theo": "Next",
    
    # Test steps
    "Kiểm Tra Ngoại Hình": "Physical Inspection",
    "Kiểm Tra Cài Đặt BIOS": "BIOS Settings Check",
    "Định Danh Phần Cứng": "Hardware Fingerprint",
    "Bản Quyền Windows": "Windows License",
    "Cấu Hình Hệ Thống": "System Configuration",
    "Sức Khỏe Ổ Cứng": "Hard Drive Health",
    "Kiểm Tra Màn Hình": "Screen Test",
    "Bàn Phím & Touchpad": "Keyboard & Touchpad",
    "Pin Laptop": "Battery Health",
    "Loa & Micro": "Audio Test",
    
    # Status
    "Tốt": "Good",
    "Lỗi": "Error",
    "Cảnh báo": "Warning",
    "Không rõ": "Unknown",
    
    # Results
    "Kết quả": "Result",
    "Trạng thái": "Status",
    "Chi tiết": "Details",
    
    # Actions
    "Bắt đầu Test": "Start Test",
    "Dừng Test": "Stop Test",
    "Xóa vết vẽ": "Clear Drawing",
}

def find_vietnamese_strings(file_path):
    """Tìm tất cả chuỗi tiếng Việt trong file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern để tìm chuỗi có ký tự tiếng Việt
    pattern = r'["\']([^"\']*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^"\']*)["\']'
    
    matches = re.findall(pattern, content)
    return list(set(matches))

def main():
    file_path = 'main_enhanced_auto.py'
    
    print("Tìm chuỗi tiếng Việt trong", file_path)
    vietnamese_strings = find_vietnamese_strings(file_path)
    
    print(f"\nTìm thấy {len(vietnamese_strings)} chuỗi tiếng Việt:")
    for i, s in enumerate(vietnamese_strings[:30], 1):
        print(f"{i}. {s}")
    
    if len(vietnamese_strings) > 30:
        print(f"... và {len(vietnamese_strings) - 30} chuỗi khác")

if __name__ == "__main__":
    main()
