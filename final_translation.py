#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final translation - translate ALL remaining Vietnamese strings"""

FINAL_TRANSLATIONS = {
    # BIOS instructions
    "   • **ASUS:** F2 hoặc Delete\\n": "   • **ASUS:** F2 or Delete\\n",
    "   • **Acer:** F2 hoặc Delete\\n": "   • **Acer:** F2 or Delete\\n",
    "   • **Boot Order:** Kiểm tra thứ tự khởi động\\n": "   • **Boot Order:** Check boot order\\n",
    "   • **CPU Features:** Intel Turbo Boost / AMD Boost phải ": "   • **CPU Features:** Intel Turbo Boost / AMD Boost must be ",
    "   • **Dell/Alienware:** F2 hoặc F12\\n": "   • **Dell/Alienware:** F2 or F12\\n",
    "   • **HP/Compaq:** F10 hoặc ESC\\n": "   • **HP/Compaq:** F10 or ESC\\n",
    "   • **Lenovo/ThinkPad:** F1, F2 hoặc Enter\\n": "   • **Lenovo/ThinkPad:** F1, F2 or Enter\\n",
    "   • **MSI:** Delete hoặc F2\\n\\n": "   • **MSI:** Delete or F2\\n\\n",
    "   • **Memory:** XMP/DOCP profile nên bật (nếu có)\\n": "   • **Memory:** XMP/DOCP profile should be enabled (if available)\\n",
    "   • **Secure Boot:** Nên để ": "   • **Secure Boot:** Should be set to ",
    "   • **Security:** Không có BIOS password lạ\\n": "   • **Security:** No strange BIOS password\\n",
    "   • **⚠️ CẢNH BÁO:** Tìm ": "   • **⚠️ WARNING:** Look for ",
    " - nếu ": " - if ",
    " hoặc ": " or ",
    " thì máy có thể bị khóa từ xa!\\n": " the machine can be remotely locked!\\n",
    " vào ": " on ",
    "1. Khởi động lại máy và nhấn liên tục phím để vào BIOS:\\n": "1. Restart and press key repeatedly to enter BIOS:\\n",
    "2. Kiểm tra các mục quan trọng:\\n": "2. Check important items:\\n",
    " cho bảo mật": " for security",
    
    # UI elements
    " Hướng dẫn thực hiện:": " How to perform:",
    " Tại sao cần test?": " Why test?",
    "- Màu xanh: Kết quả tốt, an toàn\\n- Màu vàng: Cảnh báo, cần chú ý\\n- Màu đỏ: Lỗi nghiêm trọng, cần xử lý": "- Green: Good result, safe\\n- Yellow: Warning, needs attention\\n- Red: Serious error, needs handling",
    "Bỏ qua bước hiện tại": "Skip current step",
    "Chế Độ Cơ Bản": "Basic Mode",
    "Chọn chế độ kiểm tra": "Select test mode",
    "Cập nhật trạng thái các nút navigation": "Update navigation button states",
    "Cắm thiết bị": "Plug in device",
    "Hiển thị nhận định khả năng sử dụng phần cứng": "Display hardware capability assessment",
    "Hoàn thành!": "Completed!",
    "Không rõ": "Unknown",
    "Kiểm tra S.M.A.R.T": "Check S.M.A.R.T",
    "Kiểm tra pin": "Check battery",
    "Kiểm tra pixel": "Check pixels",
    "Mở camera": "Open camera",
    "Phân tích khả năng sử dụng dựa trên thông tin phần cứng từ BIOS": "Analyze usage capability based on hardware information from BIOS",
    "Summary ({total_steps} bước hoàn thành)": "Summary ({total_steps} steps completed)",
    "Sẽ hết hạn ({expiry_date})": "Will expire ({expiry_date})",
    "Test cổng": "Test ports",
    "Test màn hình": "Test display",
    "Test tốc độ": "Test speed",
    "Thông tin hệ thống": "System information",
    "Tốc độ": "Speed",
    "Tự động kiểm tra": "Auto check",
    "Tự động đọc": "Auto read",
    "Tỷ lệ": "Rate",
    "kích hoạt vĩnh viễn": "permanently activated",
    "sẽ hết hạn": "will expire",
    "Đọc thông tin pin": "Read battery info",
    "Error đọc CPU: {e}": "Error reading CPU: {e}",
}

def apply_final_translation(input_file):
    """Apply final translation"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sort by length (longest first)
    sorted_translations = sorted(FINAL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    changes = 0
    for vietnamese, english in sorted_translations:
        if vietnamese in content:
            content = content.replace(vietnamese, english)
            changes += 1
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[SUCCESS] Applied {changes} final translations to {input_file}")

if __name__ == "__main__":
    apply_final_translation("main.py")
    print("[DONE] All translations completed!")
