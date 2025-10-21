# -*- coding: utf-8 -*-
"""Translations for all steps"""

STEP_TRANS = {
    # Step 1 - Physical Inspection
    "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp.": "Physical condition reflects how previous owner used machine. Cracks, dents, loose hinges or stripped screws may indicate drops or unprofessional repairs.",
    "Kiểm tra vỏ máy, bản lề, cổng kết nối, ốc vít, tem bảo hành. Đánh giá tổng thể tình trạng vật lý.": "Check chassis, hinges, ports, screws, warranty seals. Assess overall physical condition.",
    "✓ Vỏ máy: Vết nứt, móp méo (đặc biệt góc máy)": "✓ Chassis: Cracks, dents (especially corners)",
    "✓ Bản lề: Mở/đóng 10-15 lần, nghe tiếng kêu kèn kẹt": "✓ Hinges: Open/close 10-15 times, listen for creaking",
    "✓ Bản lề giữ góc: Không rơ, không tự đóng": "✓ Hinge holds angle: No wobble, doesn't self-close",
    "✓ Vết nứt gần bản lề: DẤU HIỆU NGUY HIỂM": "✓ Cracks near hinges: DANGER SIGN",
    "✓ Cổng sạc: Cắm và lay nhẹ, KHÔNG được lỏng": "✓ Charging port: Plug and wiggle gently, must NOT be loose",
    "✓ USB: Cắm thử USB, kiểm tra độ chặt": "✓ USB: Test plug, check tightness",
    "✓ HDMI/DisplayPort: Không bị lỏng lẻo": "✓ HDMI/DisplayPort: Not loose",
    "✓ Audio jack: Cắm tai nghe thử": "✓ Audio jack: Test with headphones",
    "✓ Ốc vít: Không toét đầu (dấu hiệu tháo lắp)": "✓ Screws: Not stripped (sign of disassembly)",
    "✓ Tem bảo hành: Còn nguyên, không bị bóc": "✓ Warranty seals: Intact, not peeled",
    "✓ Serial number: Khớp với BIOS và sticker": "✓ Serial number: Matches BIOS and sticker",
    "✓ Khe tản nhiệt: Không bị bịt tắc bụi": "✓ Cooling vents: Not blocked by dust",
    "✓ Tem Lenovo chính hãng: Hologram, không nhòe": "✓ Genuine Lenovo sticker: Hologram, not blurry",
    "✓ Sticker dưới đáy: COA Windows, Serial, Model": "✓ Bottom stickers: COA Windows, Serial, Model",
    "✓ Asset tag: ThinkPad doanh nghiệp thường có": "✓ Asset tag: Corporate ThinkPads usually have",
    "✓ TrackPoint (nút đỏ): Hoạt động, không bị lỏng": "✓ TrackPoint (red dot): Working, not loose",
    "✓ ThinkLight/Đèn bàn phím: Test hoạt động": "✓ ThinkLight/Keyboard backlight: Test working",
    "✓ Khe Kensington Lock: Không bị gãy": "✓ Kensington Lock slot: Not broken",
    "⚠️ Kiểm tra BIOS có bị khóa Computrace không!": "⚠️ Check if BIOS has Computrace lock!",
    
    # Step 3 - Hard Drive
    "Ổ cứng": "Hard Drive",
    "Dung lượng": "Capacity",
    "Loại": "Type",
    "Nhiệt độ": "Temperature",
    
    # Step 7, 8, 9 - Instructions
    "Nhấn 'Bắt đầu Test' để chạy test màn hình tự động. Test sẽ hiển thị các màu khác nhau, nhấn ESC để dừng bất cứ lúc nào.": "Click 'Start Test' to run automatic screen test. Test displays different colors, press ESC to stop anytime.",
    "Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ sáng lên màu xanh dương, và chuyển sang xanh lá khi được nhả ra. Vẽ trên vùng test touchpad, thử click trái/phải.": "Press all keys sequentially. Keys light up blue when pressed, turn green when released. Draw on touchpad test area, try left/right click.",
    "Phát bài nhạc test và kiểm tra micro với biểu đồ sóng âm.": "Play test music and check microphone with waveform chart.",
    
    # Summary - Step by step results
    "Bước": "Step",
    "Kết quả": "Result",
    "Đạt": "Passed",
    "Cảnh báo": "Warning",
    "Bỏ qua": "Skipped",
}

print(f"STEP_TRANSLATIONS: {len(STEP_TRANS)} entries")
