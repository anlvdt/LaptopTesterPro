╔══════════════════════════════════════════════════════════════╗
║          LAPTOPTESTER - HƯỚNG DẪN CÀI ĐẶT NHANH             ║
╚══════════════════════════════════════════════════════════════╝

📋 YÊU CẦU HỆ THỐNG:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Windows 10/11 (64-bit)
✅ Python 3.8 trở lên
✅ 4GB RAM trở lên
✅ 500MB dung lượng trống
✅ Quyền Administrator (cho một số tính năng)

🚀 CÀI ĐẶT NHANH (3 BƯỚC):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BƯỚC 1: Cài đặt Python (nếu chưa có)
   → Tải từ: https://www.python.org/downloads/
   → Chọn "Add Python to PATH" khi cài đặt
   → Khởi động lại máy sau khi cài

BƯỚC 2: Cài đặt thư viện
   → Click đúp vào: INSTALL.bat
   → Đợi quá trình cài đặt hoàn tất

BƯỚC 3: Chạy ứng dụng
   → Click đúp vào: RUN.bat
   → Hoặc chạy: python main_enhanced_auto.py

🎯 CHẠY NHANH (Đã cài đặt):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   → Click đúp: RUN.bat

📁 CẤU TRÚC THỨ MỤC:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LaptopTester/
├── main_enhanced_auto.py    ← File chính
├── requirements.txt          ← Danh sách thư viện
├── INSTALL.bat              ← Cài đặt tự động
├── RUN.bat                  ← Chạy ứng dụng
├── assets/                  ← Icons, sounds
│   ├── icons/              ← Biểu tượng UI
│   └── stereo_test.mp3     ← File test âm thanh
├── bin/                     ← Tools bên ngoài
│   └── LibreHardwareMonitor/
└── logs/                    ← Log files

⚠️ XỬ LÝ LỖI THƯỜNG GẶP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Python không được nhận dạng..."
   → Cài đặt Python và chọn "Add to PATH"
   → Khởi động lại Command Prompt

❌ "pip install lỗi..."
   → Chạy: python -m pip install --upgrade pip
   → Thử lại: pip install -r requirements.txt

❌ "Import error: customtkinter..."
   → Chạy: pip install customtkinter --upgrade

❌ "Permission denied..."
   → Click phải RUN.bat → "Run as Administrator"

❌ "Missing assets/icons..."
   → Đảm bảo giải nén đầy đủ thư mục assets/

🔧 CÀI ĐẶT THỦ CÔNG (Nếu INSTALL.bat lỗi):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Mở Command Prompt (cmd)
2. Di chuyển đến thư mục: cd C:\path\to\LaptopTester
3. Chạy: pip install -r requirements.txt
4. Chạy: python main_enhanced_auto.py

📚 THƯ VIỆN SỬ DỤNG:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• customtkinter - Giao diện hiện đại
• psutil - Thông tin hệ thống
• Pillow - Xử lý ảnh
• opencv-python - Computer vision
• pygame - Âm thanh
• sounddevice - Audio testing
• keyboard - Keyboard testing
• numpy, scipy - Tính toán
• wmi, pywin32 - Windows APIs

💡 MẸO SỬ DỤNG:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Chạy với quyền Administrator để test đầy đủ
✓ Đóng các ứng dụng nặng trước khi test
✓ Kết nối sạc khi test pin
✓ Chuẩn bị USB, tai nghe để test cổng
✓ Chọn Basic Mode cho test nhanh
✓ Chọn Expert Mode cho test chuyên sâu

📞 HỖ TRỢ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Xem README.md để biết chi tiết
• Kiểm tra logs/ nếu có lỗi
• GitHub Issues cho bug reports

═══════════════════════════════════════════════════════════════
         Phát triển bởi LaptopTester Team - 2024
═══════════════════════════════════════════════════════════════
