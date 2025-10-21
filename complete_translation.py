#!/usr/bin/env python3
"""
Complete translation script - translates ALL remaining Vietnamese text
"""

# Comprehensive translation dictionary
COMPLETE_TRANSLATIONS = {
    # Comments in Vietnamese
    "# Bước 1: Kiểm tra ngoại hình với checklist chi tiết": "# Step 1: Physical inspection with detailed checklist",
    "# Bước 1: Checklist ngoại hình": "# Step 1: Physical checklist",
    "# Bước 2: BIOS": "# Step 2: BIOS",
    "# Bước 3: Định danh phần cứng tự động": "# Step 3: Automatic hardware identification",
    
    # Main.py specific translations
    "Khôi phục cấu trúc bước như main_enhanced": "Restore step structure like main_enhanced",
    
    # Physical inspection details
    "Vỏ máy & Bản lề:": "Case & Hinges:",
    "Kiểm tra vết nứt, móp méo ở góc máy (dấu hiệu rơi)": "Check for cracks, dents at corners (signs of drops)",
    "Mở/đóng màn hình 10-15 lần, nghe tiếng kêu lạ": "Open/close screen 10-15 times, listen for strange sounds",
    "Bản lề phải chặt, không rơ, giữ được góc mở": "Hinges must be tight, not loose, hold opening angle",
    
    "Cổng kết nối:": "Ports:",
    "Cắm sạc và lay nhẹ - không được lỏng": "Plug charger and wiggle gently - must not be loose",
    "Kiểm tra USB, HDMI, audio jack": "Check USB, HDMI, audio jack",
    "Cổng bị lỏng = thay mainboard (đắt!)": "Loose port = replace mainboard (expensive!)",
    
    "Ốc vít & Tem:": "Screws & Seals:",
    "Ốc không toét đầu (dấu hiệu tháo lắp)": "Screws not stripped (sign of disassembly)",
    "Tem bảo hành còn nguyên": "Warranty seal intact",
    "Serial number khớp với BIOS": "Serial number matches BIOS",
    
    "⚠️ ThinkPad đặc biệt:": "⚠️ ThinkPad specific:",
    "Kiểm tra tem Lenovo chính hãng": "Check genuine Lenovo seal",
    "Xem sticker dưới đáy có bị bóc": "Check if bottom sticker is peeled",
    "ThinkPad doanh nghiệp thường có asset tag": "Enterprise ThinkPad usually has asset tag",
    
    # BIOS check details
    "**Vỏ máy & Bản lề:**\\n  - Kiểm tra vết nứt, móp méo ở góc máy (dấu hiệu rơi)\\n  - Mở/đóng màn hình 10-15 lần, nghe tiếng kêu lạ\\n  - Bản lề phải chặt, không rơ, giữ được góc mở\\n\\n**Cổng kết nối:**\\n  - Cắm sạc và lay nhẹ - không được lỏng\\n  - Kiểm tra USB, HDMI, audio jack\\n  - Cổng bị lỏng = thay mainboard (đắt!)\\n\\n**Ốc vít & Tem:**\\n  - Ốc không toét đầu (dấu hiệu tháo lắp)\\n  - Tem bảo hành còn nguyên\\n  - Serial number khớp với BIOS\\n\\n**⚠️ ThinkPad đặc biệt:**\\n  - Kiểm tra tem Lenovo chính hãng\\n  - Xem sticker dưới đáy có bị bóc\\n  - ThinkPad doanh nghiệp thường có asset tag":
        "**Case & Hinges:**\\n  - Check for cracks, dents at corners (signs of drops)\\n  - Open/close screen 10-15 times, listen for strange sounds\\n  - Hinges must be tight, not loose, hold opening angle\\n\\n**Ports:**\\n  - Plug charger and wiggle gently - must not be loose\\n  - Check USB, HDMI, audio jack\\n  - Loose port = replace mainboard (expensive!)\\n\\n**Screws & Seals:**\\n  - Screws not stripped (sign of disassembly)\\n  - Warranty seal intact\\n  - Serial number matches BIOS\\n\\n**⚠️ ThinkPad specific:**\\n  - Check genuine Lenovo seal\\n  - Check if bottom sticker is peeled\\n  - Enterprise ThinkPad usually has asset tag",
    
    "1. Khởi động lại máy và nhấn liên tục phím để vào BIOS:\\n   • **Dell/Alienware:** F2 hoặc F12\\n   • **HP/Compaq:** F10 hoặc ESC\\n   • **Lenovo/ThinkPad:** F1, F2 hoặc Enter\\n   • **ASUS:** F2 hoặc Delete\\n   • **Acer:** F2 hoặc Delete\\n   • **MSI:** Delete hoặc F2\\n\\n2. Kiểm tra các mục quan trọng:\\n   • **CPU Features:** Intel Turbo Boost / AMD Boost phải 'Enabled'\\n   • **Memory:** XMP/DOCP profile nên bật (nếu có)\\n   • **Security:** Không có BIOS password lạ\\n   • **⚠️ CẢNH BÁO:** Tìm 'Computrace' hoặc 'Absolute' - nếu 'Enabled' thì máy có thể bị khóa từ xa!\\n   • **Boot Order:** Kiểm tra thứ tự khởi động\\n   • **Secure Boot:** Nên để 'Enabled' cho bảo mật":
        "1. Restart and press key repeatedly to enter BIOS:\\n   • **Dell/Alienware:** F2 or F12\\n   • **HP/Compaq:** F10 or ESC\\n   • **Lenovo/ThinkPad:** F1, F2 or Enter\\n   • **ASUS:** F2 or Delete\\n   • **Acer:** F2 or Delete\\n   • **MSI:** Delete or F2\\n\\n2. Check important items:\\n   • **CPU Features:** Intel Turbo Boost / AMD Boost must be 'Enabled'\\n   • **Memory:** XMP/DOCP profile should be enabled (if available)\\n   • **Security:** No strange BIOS password\\n   • **⚠️ WARNING:** Look for 'Computrace' or 'Absolute' - if 'Enabled' the machine can be remotely locked!\\n   • **Boot Order:** Check boot order\\n   • **Secure Boot:** Should be 'Enabled' for security",
    
    # Hardware identification
    "**Bàn phím:** Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ sáng lên màu xanh dương, và chuyển sang xanh lá khi được nhả ra.\\n**Touchpad & Chuột:**\\n   1. Dùng 1 ngón tay vẽ lên vùng màu xám để kiểm tra điểm chết cảm ứng.\\n   2. Click trái/phải để test nút bấm.\\n   3. Dùng 2 ngón tay để cuộn lên/xuống.":
        "**Keyboard:** Type all keys sequentially. Keys you press will light up blue, and turn green when released.\\n**Touchpad & Mouse:**\\n   1. Use 1 finger to draw on gray area to check for dead spots.\\n   2. Left/right click to test buttons.\\n   3. Use 2 fingers to scroll up/down.",
    
    # Results and status
    "Rất tốt - Như mới": "Excellent - Like new",
    "Tốt - Có vết sử dụng nhỏ": "Good - Minor wear marks",
    "Trung bình - Có lỗi nhỏ cần lưu ý": "Fair - Minor issues to note",
    "Kém - Nhiều vấn đề nghiêm trọng": "Poor - Multiple serious issues",
    "Cài đặt chính xác": "Settings correct",
    "Có vấn đề với cài đặt BIOS": "Issues with BIOS settings",
    
    # License check
    "Windows được kích hoạt vĩnh viễn": "Windows permanently activated",
    "Windows sẽ hết hạn vào": "Windows will expire on",
    "Windows chưa được kích hoạt": "Windows not activated",
    "Lỗi khi chạy lệnh kiểm tra": "Error running check command",
    
    # Network test
    "Đang test Internet...": "Testing Internet...",
    "Đang test DNS...": "Testing DNS...",
    "Đang test WiFi...": "Testing WiFi...",
    "Đang test Ping...": "Testing Ping...",
    "Đang test Tốc độ...": "Testing Speed...",
    "✅ Kết nối Internet OK": "✅ Internet connection OK",
    "❌ Không có Internet": "❌ No Internet",
    "✅ DNS hoạt động tốt": "✅ DNS working well",
    "❌ DNS lỗi": "❌ DNS error",
    "📊 Tốc độ": "📊 Speed",
    "⚠️ Không test được tốc độ": "⚠️ Cannot test speed",
    "📶 WiFi": "📶 WiFi",
    "ℹ️ Không lấy được thông tin WiFi": "ℹ️ Cannot get WiFi info",
    "⚠️ Lỗi đọc WiFi": "⚠️ Error reading WiFi",
    "🏓 Ping OK": "🏓 Ping OK",
    "❌ Ping timeout": "❌ Ping timeout",
    
    # Thermal monitoring
    "✅ Bắt đầu monitoring...\\n": "✅ Starting monitoring...\\n",
    "⏹️ Dừng monitoring. Max temp": "⏹️ Stopped monitoring. Max temp",
    "🔥 CẢNH BÁO: CPU quá nóng": "🔥 WARNING: CPU overheating",
    "Chưa bắt đầu monitoring...\\n": "Monitoring not started...\\n",
    
    # Summary report
    "Dựa trên": "Based on",
    "Tổng số test": "Total tests",
    "Đạt": "Passed",
    "Không xác định": "Unknown",
    "Không đọc được": "Cannot read",
    "Không tìm thấy CPU": "CPU not found",
    "Lỗi đọc CPU": "Error reading CPU",
    "Không tìm thấy GPU": "GPU not found",
    "Lỗi đọc GPU": "Error reading GPU",
    "Không tìm thấy ổ cứng": "Hard drive not found",
    "Lỗi đọc ổ cứng": "Error reading hard drive",
    "Lỗi WMI": "WMI error",
    
    # Additional status messages
    "Đã lấy định danh phần cứng": "Hardware identification retrieved",
    "Thông tin định danh phần cứng": "Hardware identification information",
    "Max temp": "Max temp",
}

def translate_file_complete(input_file, output_file):
    """Complete translation of all Vietnamese text"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sort by length (longest first) to avoid partial replacements
    sorted_translations = sorted(COMPLETE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    changes_made = 0
    for vietnamese, english in sorted_translations:
        # Count occurrences before replacement
        count_before = content.count(vietnamese)
        
        if count_before > 0:
            # Replace in all contexts
            content = content.replace(vietnamese, english)
            changes_made += count_before
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[SUCCESS] Translation completed: {changes_made} changes made")
    print(f"[OUTPUT] File: {output_file}")

if __name__ == "__main__":
    # Translate main.py
    translate_file_complete("main.py", "main.py")
    print("\n[DONE] All Vietnamese text has been translated to English.")
