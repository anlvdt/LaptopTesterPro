#!/usr/bin/env python3
"""
Script to translate Vietnamese text to English in main.py
"""

# Dictionary mapping Vietnamese to English
TRANSLATIONS = {
    # Theme and UI
    "Sáng": "Light",
    "Tối": "Dark",
    "Giao diện": "Theme",
    "Ngôn ngữ": "Language",
    "Cài đặt": "Settings",
    "Thoát": "Exit",
    
    # Navigation
    "← Trước": "← Previous",
    "Tiếp theo →": "Next →",
    "Bỏ qua": "Skip",
    "Tiếp tục": "Continue",
    
    # Mode selection
    "Chọn Chế Độ Kiểm Tra": "Select Test Mode",
    "Chế Độ Cơ bản": "Basic Mode",
    "Chế Độ Chuyên Gia": "Expert Mode",
    "Chế độ Chuyên gia": "Expert Mode",
    "Chế độ Cơ bản": "Basic Mode",
    "🎯 Chế độ Cơ bản": "🎯 Basic Mode",
    "🔥 Chế độ Chuyên gia": "🔥 Expert Mode",
    
    # Status
    "Sẵn sàng": "Ready",
    "Đang chạy": "Running",
    "Hoàn thành": "Completed",
    "Lỗi": "Error",
    "Tốt": "Good",
    "Cảnh báo": "Warning",
    "Xuất sắc": "Excellent",
    "Trung bình": "Fair",
    "Kém": "Poor",
    
    # Step 1: Physical Inspection
    "Kiểm Tra Ngoại Hình": "Physical Inspection",
    "Kiểm tra ngoại hình": "Physical inspection",
    "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp. Đặc biệt với ThinkPad, kiểm tra tem bảo hành và serial number.": 
        "Physical condition reflects how the previous owner used the laptop. Cracks, dents, loose hinges, or stripped screws may indicate drops or unprofessional repairs. For ThinkPad, check warranty seals and serial numbers.",
    
    "🔍 Checklist Kiểm Tra Ngoại Hình": "🔍 Physical Inspection Checklist",
    "💻 Bên Ngoài:": "💻 Exterior:",
    "- Vỏ máy: Kiểm tra vết nứt, rạn nứt, móp méo": "- Case: Check for cracks, fractures, dents",
    "- Bản lề màn hình: Mở/đóng nhiều lần, nghe tiếng kêu": "- Screen hinges: Open/close multiple times, listen for sounds",
    "- Bàn phím: Kiểm tra phím lỏng, không nhấn": "- Keyboard: Check for loose or non-responsive keys",
    "- Touchpad: Bề mặt phẳng, không bị lồi": "- Touchpad: Surface should be flat, not bulging",
    "- Cổng kết nối: USB, HDMI, audio, sạc": "- Ports: USB, HDMI, audio, charging",
    "- Lỗ thoát khí: Không bị bịt tắc": "- Vents: Not blocked",
    
    "🔩 Phần Cứng:": "🔩 Hardware:",
    "- Ốc vít: Kiểm tra các ốc không bị toét, thiếu": "- Screws: Check for stripped or missing screws",
    "- Nhãn dán: Còn nguyên, không bị xóa": "- Labels: Intact, not removed",
    "- Đèn LED: Hoạt động bình thường": "- LEDs: Working normally",
    "- Lưới thoát khí: Sạch sẽ, không bụi bẩn": "- Vent grills: Clean, no dust buildup",
    
    "⚠️ Dấu Hiệu Cảnh Báo:": "⚠️ Warning Signs:",
    "- Bản lề rất lỏng hoặc kêu kèn kẹt": "- Very loose hinges or squeaking sounds",
    "- Cổng sạc lỏng, không giữ chặt": "- Loose charging port, doesn't hold firmly",
    "- Vết nứt gần bản lề (nguy hiểm)": "- Cracks near hinges (dangerous)",
    "- Mùi lạ (cháy, hóa chất)": "- Strange odors (burning, chemicals)",
    "- Ốc vít bị toét nhiều (dấu hiệu tháo lắp)": "- Many stripped screws (sign of disassembly)",
    
    "Dựa trên checklist trên, tình trạng vật lý tổng thể của máy như thế nào?": "Based on the checklist above, what is the overall physical condition?",
    "✨ Rất tốt - Như mới": "✨ Excellent - Like new",
    "✅ Tốt - Vết nhỏ": "✅ Good - Minor wear",
    "⚠️ Trung bình - Có lỗi nhỏ": "⚠️ Fair - Minor issues",
    "❌ Kém - Nhiều vấn đề": "❌ Poor - Multiple issues",
    
    # Step 2: BIOS
    "Kiểm Tra Cài Đặt BIOS": "BIOS Settings Check",
    "Kiểm tra BIOS": "BIOS check",
    "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp.": 
        "BIOS contains fundamental settings. Check to ensure optimal performance and no enterprise lockdown features.",
    "Các cài đặt trong BIOS có chính xác và an toàn không?": "Are BIOS settings correct and safe?",
    "Có, mọi cài đặt đều đúng": "Yes, all settings are correct",
    "Không, có cài đặt sai/bị khóa": "No, incorrect settings/locked",
    
    # Step 3: Hardware Fingerprint
    "Định Danh Phần Cứng": "Hardware Identification",
    "Định danh phần cứng": "Hardware identification",
    "Đây là bước quan trọng nhất để chống lừa đảo. Các thông tin dưới đây được đọc trực tiếp từ BIOS và linh kiện phần cứng. Chúng **cực kỳ khó làm giả** từ bên trong Windows.":
        "This is the most important step to prevent fraud. Information below is read directly from BIOS and hardware components. They are **extremely difficult to fake** from within Windows.",
    "Hãy so sánh các thông tin 'vàng' này với cấu hình mà người bán quảng cáo. Nếu có bất kỳ sự sai lệch nào, hãy đặt câu hỏi và kiểm tra thật kỹ.":
        "Compare this 'golden' information with the seller's advertised specs. If there are any discrepancies, ask questions and verify carefully.",
    
    "Model Laptop": "Laptop Model",
    "Serial Number": "Serial Number",
    "CPU": "CPU",
    "GPU": "GPU",
    "Model Ổ Cứng": "Hard Drive Model",
    "Ngày BIOS": "BIOS Date",
    "Đang đọc...": "Reading...",
    
    "💡 Khả Năng Sử Dụng Phần Cứng": "💡 Hardware Capability",
    "Gaming & Rendering": "Gaming & Rendering",
    "Phù hợp cho gaming AAA, render 3D, video editing chuyên nghiệp": "Suitable for AAA gaming, 3D rendering, professional video editing",
    "Workstation": "Workstation",
    "Xử lý đa nhiệm nặng, phát triển phần mềm, máy ảo": "Heavy multitasking, software development, virtual machines",
    "Gaming Casual": "Casual Gaming",
    "Chơi game ở mức trung bình, streaming, content creation": "Mid-level gaming, streaming, content creation",
    "Văn phòng nâng cao": "Advanced Office",
    "Office, lập trình, thiết kế đồ họa 2D, đa nhiệm vừa phải": "Office, programming, 2D graphics design, moderate multitasking",
    "Văn phòng cơ bản": "Basic Office",
    "Office, web browsing, email, xem phim": "Office, web browsing, email, watching videos",
    "Học tập": "Education",
    "Học online, soạn thảo văn bản, nghiên cứu": "Online learning, document editing, research",
    "Đồ họa chuyên nghiệp": "Professional Graphics",
    "GPU rời mạnh, phù hợp cho CAD, 3D modeling, AI/ML": "Powerful dedicated GPU, suitable for CAD, 3D modeling, AI/ML",
    
    "Định danh phần cứng đã hoàn thành. Bạn có muốn tiếp tục?": "Hardware identification completed. Continue?",
    
    # Step 4: License Check
    "Bản Quyền Windows": "Windows License",
    "Bản quyền Windows": "Windows license",
    "Một máy tính có bản quyền Windows hợp lệ đảm bảo bạn nhận được các bản cập nhật bảo mật quan trọng và tránh các rủi ro pháp lý.":
        "A computer with valid Windows license ensures you receive important security updates and avoid legal risks.",
    "Ứng dụng sẽ tự động chạy lệnh kiểm tra trạng thái kích hoạt của Windows. Kết quả sẽ hiển thị bên dưới.":
        "The app will automatically check Windows activation status. Results will be displayed below.",
    "Đang kiểm tra...": "Checking...",
    "Kiểm tra bản quyền đã hoàn thành. Bạn có muốn tiếp tục?": "License check completed. Continue?",
    
    # Step 5-7: Placeholders
    "Cấu Hình Windows": "Windows Configuration",
    "Cấu hình hệ thống": "System configuration",
    "Sức Khỏe Ổ Cứng": "Hard Drive Health",
    "Sức khỏe ổ cứng": "Hard drive health",
    "Màn Hình": "Display",
    "Kiểm tra màn hình": "Display test",
    
    # Step 8: Keyboard & Touchpad
    "Bàn phím & Touchpad & Chuột": "Keyboard & Touchpad & Mouse",
    "Bàn phím & Touchpad": "Keyboard & Touchpad",
    "Một phím bị liệt, kẹt, hoặc touchpad bị loạn/mất cử chỉ đa điểm sẽ làm gián đoạn hoàn toàn công việc.":
        "A dead, stuck key, or malfunctioning touchpad/multi-touch gestures will completely disrupt work.",
    "Bàn phím, Touchpad và Chuột có hoạt động tốt không?": "Do keyboard, touchpad and mouse work properly?",
    "Có, tất cả đều tốt": "Yes, all working well",
    "Không, có lỗi": "No, there are issues",
    
    # Step 9-10: Placeholders
    "Cổng Kết Nối": "Ports & Connectivity",
    "Cổng kết nối": "Ports connectivity",
    "Pin Laptop": "Battery",
    "Pin laptop": "Battery",
    
    # Step 11: Speaker Test
    "Loa & Micro": "Speakers & Microphone",
    "Kiểm tra loa để đảm bảo âm thanh rõ ràng, không bị rè, tạp âm hay méo tiếng. Loa hỏng là vấn đề phổ biến trên laptop cũ.":
        "Check speakers to ensure clear sound, no buzzing, noise or distortion. Broken speakers are common in used laptops.",
    "Nhấn nút phát âm thanh test. Lắng nghe kỹ từng kênh trái/phải. Kiểm tra âm lượng tối đa có bị méo không.":
        "Press play button to test audio. Listen carefully to left/right channels. Check if maximum volume is distorted.",
    
    "🔊 Test Loa Stereo": "🔊 Stereo Speaker Test",
    "- Tăng âm lượng lên 50-70%": "- Increase volume to 50-70%",
    "- Nghe kênh trái và phải có cân bằng không": "- Listen if left and right channels are balanced",
    "- Kiểm tra có tiếng rè, tạp âm, méo tiếng không": "- Check for buzzing, noise, or distortion",
    "- Test ở âm lượng tối đa (cẩn thận!)": "- Test at maximum volume (careful!)",
    
    "▶️ Phát âm thanh test": "▶️ Play test audio",
    "⏹️ Dừng": "⏹️ Stop",
    "❌ Không tìm thấy file audio": "❌ Audio file not found",
    "🔊 Đang phát...": "🔊 Playing...",
    "⏹️ Đã dừng": "⏹️ Stopped",
    
    "Loa hoạt động như thế nào?": "How do the speakers work?",
    "✅ Tốt - Rõ ràng, cân bằng": "✅ Good - Clear, balanced",
    "⚠️ Trung bình - Có tạp âm nhẹ": "⚠️ Fair - Slight noise",
    "❌ Kém - Rè, méo, mất kênh": "❌ Poor - Buzzing, distortion, channel loss",
    
    # Step 12: Webcam
    "Webcam": "Webcam",
    
    # Step 13: Network Test
    "Mạng & WiFi": "Network & WiFi",
    "Kết nối mạng ổn định quan trọng cho công việc và giải trí online.": "Stable network connection is important for work and online entertainment.",
    "Test sẽ kiểm tra Internet, WiFi, DNS, tốc độ và ping.": "Test will check Internet, WiFi, DNS, speed and ping.",
    "🚀 Bắt Đầu Test": "🚀 Start Test",
    "Sẵn sàng test mạng": "Ready to test network",
    "Đang test": "Testing",
    "Test mạng hoàn thành. Tiếp tục?": "Network test completed. Continue?",
    
    # Expert mode steps
    "CPU Stress Test": "CPU Stress Test",
    "Tốc Độ Ổ Cứng": "Hard Drive Speed",
    "Tốc độ ổ cứng": "Hard drive speed",
    "GPU Stress Test": "GPU Stress Test",
    
    "Thermal Monitor": "Thermal Monitor",
    "Giám sát nhiệt độ CPU real-time để phát hiện vấn đề tản nhiệt và throttling.": "Monitor CPU temperature in real-time to detect cooling issues and throttling.",
    "Nhấn Start để bắt đầu monitoring. Có thể chạy Stress Test để kiểm tra dưới tải nặng.": "Press Start to begin monitoring. Can run Stress Test to check under heavy load.",
    "🚀 Start Monitor": "🚀 Start Monitor",
    "⏹️ Stop": "⏹️ Stop",
    "🌡️ CPU": "🌡️ CPU",
    "⚡ CPU": "⚡ CPU",
    "Chưa bắt đầu monitoring...": "Monitoring not started...",
    "✅ Bắt đầu monitoring...": "✅ Starting monitoring...",
    "⏹️ Dừng monitoring. Max temp": "⏹️ Stopped monitoring. Max temp",
    "🔥 CẢNH BÁO: CPU quá nóng": "🔥 WARNING: CPU overheating",
    "Monitoring hoàn thành. Tiếp tục?": "Monitoring completed. Continue?",
    
    # Summary
    "Báo Cáo Tổng Kết": "Summary Report",
    "📊 BÁO CÁO TỔNG KẾT": "📊 SUMMARY REPORT",
    "📋 Tổng số test": "📋 Total tests",
    "✅ Đạt": "✅ Passed",
    "⚠️ Cảnh báo": "⚠️ Warning",
    "❌ Lỗi": "❌ Failed",
    "📊 Tỷ lệ": "📊 Success rate",
    "📝 Chi Tiết Kết Quả": "📝 Detailed Results",
    "📄 Xuất PDF": "📄 Export PDF",
    "📊 Xuất Excel": "📊 Export Excel",
    "📋 Copy Text": "📋 Copy Text",
    "Dựa trên": "Based on",
    
    # Results
    "Kết quả": "Result",
    "Trạng thái": "Status",
    "Chi tiết": "Details",
    "Đã hiển thị checklist": "Checklist displayed",
    "Đã lấy định danh phần cứng": "Hardware identification retrieved",
    "Đã kích hoạt vĩnh viễn": "Permanently activated",
    "Chưa kích hoạt": "Not activated",
    "Hoạt động tốt": "Working well",
    "Có lỗi": "Has issues",
    "Loa hoạt động tốt": "Speakers working well",
    "Loa có tạp âm nhẹ": "Speakers have slight noise",
    "Loa có vấn đề nghiêm trọng": "Speakers have serious issues",
    "Đã test mạng": "Network tested",
    
    # Common phrases
    "Tại sao cần test?": "Why test?",
    "Hướng dẫn thực hiện:": "How to perform:",
    "💡 Gợi ý đọc kết quả:": "💡 Tips for reading results:",
    "- Màu xanh: Kết quả tốt, an toàn": "- Green: Good result, safe",
    "- Màu vàng: Cảnh báo, cần chú ý": "- Yellow: Warning, needs attention",
    "- Màu đỏ: Lỗi nghiêm trọng, cần xử lý": "- Red: Serious error, needs handling",
    
    # Step counter
    "Bước": "Step",
    "Tổng kết": "Summary",
    "bước hoàn thành": "steps completed",
    
    # Misc
    "Không thể kiểm tra": "Cannot check",
    "Chỉ hỗ trợ Windows": "Windows only",
    "Không xác định": "Unknown",
    "Không đọc được": "Cannot read",
    "Không tìm thấy": "Not found",
    "Lỗi": "Error",
}

def translate_file(input_file, output_file):
    """Translate Vietnamese text to English in a file"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sort by length (longest first) to avoid partial replacements
    sorted_translations = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for vietnamese, english in sorted_translations:
        # Only replace if it's in a string context (between quotes)
        content = content.replace(f'"{vietnamese}"', f'"{english}"')
        content = content.replace(f"'{vietnamese}'", f"'{english}'")
        content = content.replace(f'f"{vietnamese}', f'f"{english}')
        content = content.replace(f"f'{vietnamese}", f"f'{english}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Translation completed: {output_file}")

if __name__ == "__main__":
    translate_file("main.py", "main_english.py")
    print("Done! Check main_english.py")
