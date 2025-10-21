# 📖 LaptopTester - Hướng Dẫn Sử Dụng / User Guide

## 🌍 Language / Ngôn Ngữ
- **Tiếng Việt**: Xem phần bên dưới
- **English**: See English section below

---

## 🇻🇳 HƯỚNG DẪN TIẾNG VIỆT

### 🚀 Khởi Động Ứng Dụng
```bash
python laptoptester_previous.py
```

### 🎯 Giao Diện Chính
- **Tab "Tổng quan"**: Màn hình chính với các nút bắt đầu
- **Tab "Kiểm tra từng thành phần"**: Grid 12 bài test riêng lẻ
- **Tab "Chọn chế độ"**: Lựa chọn Basic hoặc Expert mode

### 🔧 Thanh Điều Khiển (Header)
- **🌙/☀️**: Chuyển Dark/Light mode
- **VI/EN**: Chuyển ngôn ngữ Việt/Anh
- **✕**: Thoát ứng dụng

---

## 📋 CÁC BƯỚC KIỂM TRA CHI TIẾT

### 1. 💻 **Thông Tin Hệ Thống**
**Mục đích**: Hiển thị thông tin cơ bản của máy tính
- Hệ điều hành và phiên bản
- Bộ xử lý (CPU)
- Kiến trúc hệ thống (32/64-bit)
- Tên máy tính
- Dung lượng RAM
- Phiên bản Python

**Cách sử dụng**:
1. Thông tin tự động hiển thị
2. Nhấn "Hoàn thành" để tiếp tục

### 2. 🔑 **Kiểm Tra Bản Quyền Windows**
**Mục đích**: Kiểm tra trạng thái kích hoạt Windows
- Xác định Windows đã được kích hoạt chưa
- Hiển thị trạng thái license

**Cách sử dụng**:
1. Chạy với quyền Administrator để có kết quả chính xác
2. Đợi kiểm tra tự động (10 giây timeout)
3. Xem kết quả: "Đã kích hoạt" / "Chưa kích hoạt"

**Lưu ý**: Cần quyền admin để kiểm tra chính xác

### 3. 💾 **Kiểm Tra Ổ Cứng**
**Mục đích**: Kiểm tra dung lượng và tình trạng các ổ đĩa
- Hiển thị tất cả ổ đĩa có sẵn
- Dung lượng tổng và % sử dụng
- Phát hiện ổ đĩa có vấn đề

**Cách sử dụng**:
1. Thông tin tự động quét tất cả ổ đĩa
2. Kiểm tra % sử dụng (>90% = cảnh báo)
3. Nhấn "Hoàn thành"

### 4. 🖥️ **Kiểm Tra Màn Hình**
**Mục đích**: Test độ phân giải và hiển thị màu sắc
- Độ phân giải màn hình
- DPI (dots per inch)
- Kích thước vật lý màn hình
- Test 6 màu cơ bản

**Cách sử dụng**:
1. Xem thông tin độ phân giải và DPI
2. Kiểm tra 6 ô màu: Đỏ, Xanh lá, Xanh dương, Vàng, Tím, Cyan
3. Đảm bảo tất cả màu hiển thị rõ ràng

### 5. ⌨️ **Kiểm Tra Bàn Phím**
**Mục đích**: Test tất cả phím trên bàn phím
- Phát hiện phím bị hỏng
- Kiểm tra độ nhạy phím
- Theo dõi phím đã test

**Cách sử dụng**:
1. Click vào ô text để focus
2. Nhấn từng phím trên bàn phím
3. Xem danh sách phím đã nhấn hiển thị
4. Test các phím đặc biệt: Space, Enter, Shift, Ctrl, Alt

### 6. 🔌 **Kiểm Tra Cổng Kết Nối**
**Mục đích**: Kiểm tra các cổng USB, HDMI, Audio
- Cắm thiết bị vào từng cổng
- Kiểm tra nhận diện thiết bị
- Test cổng âm thanh

**Cách sử dụng**:
1. Chuẩn bị USB, tai nghe, cáp HDMI
2. Cắm từng thiết bị vào các cổng
3. Kiểm tra Windows có nhận diện không
4. Nhấn "Hoàn thành" khi test xong

### 7. 🔋 **Kiểm Tra Pin**
**Mục đích**: Kiểm tra tình trạng pin laptop
- Mức pin hiện tại (%)
- Trạng thái sạc/không sạc
- Thời gian pin còn lại (ước tính)
- Phát hiện máy bàn (không có pin)

**Cách sử dụng**:
1. Xem mức pin hiện tại
2. Rút/cắm sạc để test trạng thái
3. Kiểm tra thời gian ước tính
4. Pin <20% = cần sạc

### 8. 🔊 **Kiểm Tra Âm Thanh**
**Mục đích**: Test loa và hệ thống âm thanh
- Phát âm thanh test 1000Hz
- Kiểm tra âm lượng
- Test chất lượng âm thanh

**Cách sử dụng**:
1. Đảm bảo âm lượng >50%
2. Nhấn "Phát âm thanh kiểm tra"
3. Nghe âm beep 0.5 giây
4. Kiểm tra loa trái/phải (nếu có)

### 9. 📷 **Kiểm Tra Camera**
**Mục đích**: Test webcam và camera tích hợp
- Phát hiện camera có sẵn
- Test khả năng chụp ảnh
- Kiểm tra chất lượng hình ảnh

**Cách sử dụng**:
1. Xem trạng thái camera
2. Nhấn "Mở camera" để test
3. Camera sẽ hiển thị 2 giây
4. Kiểm tra hình ảnh rõ nét

**Lưu ý**: Cần cài OpenCV: `pip install opencv-python`

### 10. 🧠 **Kiểm Tra CPU (Expert Mode)**
**Mục đích**: Stress test bộ xử lý
- Hiển thị % CPU real-time
- Số lượng cores
- Tần số CPU hiện tại
- Nhiệt độ CPU (nếu có)

**Cách sử dụng**:
1. Xem thông tin CPU ban đầu
2. Nhấn "Bắt đầu kiểm tra" để stress test
3. CPU sẽ chạy 100% trong 10 giây
4. Theo dõi nhiệt độ không quá 85°C

### 11. 🌡️ **Kiểm Tra Nhiệt Độ (Expert Mode)**
**Mục đích**: Monitor nhiệt độ hệ thống
- Nhiệt độ CPU
- Nhiệt độ GPU (nếu có)
- Tốc độ quạt
- Cảnh báo quá nóng

**Cách sử dụng**:
1. Để máy chạy bình thường 5 phút
2. Xem nhiệt độ idle
3. Chạy stress test và monitor
4. Nhiệt độ an toàn: CPU <80°C, GPU <85°C

---

## 🎮 CHẾ ĐỘ SỬ DỤNG

### 🟢 **Chế Độ Cơ Bản (Basic Mode)**
- **Đối tượng**: Người dùng thông thường
- **Thời gian**: 15-20 phút
- **Bao gồm**: 9 bước kiểm tra cơ bản
- **Phù hợp**: Kiểm tra nhanh trước khi mua laptop cũ

### 🔴 **Chế Độ Chuyên Gia (Expert Mode)**
- **Đối tượng**: Kỹ thuật viên, người am hiểu
- **Thời gian**: 30-45 phút
- **Bao gồm**: 13 bước kiểm tra đầy đủ
- **Phù hợp**: Kiểm tra chi tiết, đánh giá chuyên sâu

---

## 🚨 XỬ LÝ LỖI THƯỜNG GẶP

### ❌ **"Cannot check (need admin rights)"**
- **Nguyên nhân**: Thiếu quyền Administrator
- **Giải pháp**: Click phải → "Run as administrator"

### ❌ **"OpenCV library missing"**
- **Nguyên nhân**: Chưa cài OpenCV
- **Giải pháp**: `pip install opencv-python`

### ❌ **"No working camera found"**
- **Nguyên nhân**: Camera bị tắt hoặc hỏng
- **Giải pháp**: Kiểm tra Device Manager → Camera

### ❌ **"Battery check error"**
- **Nguyên nhân**: Máy bàn hoặc pin hỏng
- **Giải pháp**: Bình thường với máy bàn

### ❌ **"CPU read error"**
- **Nguyên nhân**: Lỗi psutil
- **Giải pháp**: `pip install --upgrade psutil`

---

## 🇺🇸 ENGLISH USER GUIDE

### 🚀 Starting the Application
```bash
python laptoptester_previous.py
```

### 🎯 Main Interface
- **"Overview" Tab**: Main screen with start buttons
- **"Individual Component Test" Tab**: Grid of 12 individual tests
- **"Select Mode" Tab**: Choose Basic or Expert mode

### 🔧 Header Controls
- **🌙/☀️**: Toggle Dark/Light mode
- **VI/EN**: Switch Vietnamese/English language
- **✕**: Exit application

---

## 📋 DETAILED TEST STEPS

### 1. 💻 **System Information**
**Purpose**: Display basic computer information
- Operating system and version
- Processor (CPU)
- System architecture (32/64-bit)
- Computer name
- RAM capacity
- Python version

**How to use**:
1. Information displays automatically
2. Click "Complete" to continue

### 2. 🔑 **Windows License Check**
**Purpose**: Check Windows activation status
- Determine if Windows is activated
- Display license status

**How to use**:
1. Run with Administrator rights for accurate results
2. Wait for automatic check (10 second timeout)
3. View result: "Activated" / "Not activated"

**Note**: Requires admin rights for accurate checking

### 3. 💾 **Hard Drive Health**
**Purpose**: Check disk capacity and health
- Display all available drives
- Total capacity and usage percentage
- Detect problematic drives

**How to use**:
1. Information automatically scans all drives
2. Check usage percentage (>90% = warning)
3. Click "Complete"

### 4. 🖥️ **Display Test**
**Purpose**: Test resolution and color display
- Screen resolution
- DPI (dots per inch)
- Physical screen size
- Test 6 basic colors

**How to use**:
1. View resolution and DPI information
2. Check 6 color squares: Red, Green, Blue, Yellow, Magenta, Cyan
3. Ensure all colors display clearly

### 5. ⌨️ **Keyboard Test**
**Purpose**: Test all keyboard keys
- Detect broken keys
- Check key sensitivity
- Track tested keys

**How to use**:
1. Click text box to focus
2. Press each key on keyboard
3. View list of pressed keys displayed
4. Test special keys: Space, Enter, Shift, Ctrl, Alt

### 6. 🔌 **Ports Test**
**Purpose**: Check USB, HDMI, Audio ports
- Plug devices into each port
- Check device recognition
- Test audio ports

**How to use**:
1. Prepare USB, headphones, HDMI cable
2. Plug each device into ports
3. Check if Windows recognizes them
4. Click "Complete" when done testing

### 7. 🔋 **Battery Health**
**Purpose**: Check laptop battery condition
- Current battery level (%)
- Charging/not charging status
- Estimated remaining time
- Detect desktop (no battery)

**How to use**:
1. View current battery level
2. Unplug/plug charger to test status
3. Check estimated time
4. Battery <20% = needs charging

### 8. 🔊 **Audio Test**
**Purpose**: Test speakers and audio system
- Play 1000Hz test tone
- Check volume level
- Test audio quality

**How to use**:
1. Ensure volume >50%
2. Click "Play Test Tone"
3. Listen for 0.5 second beep
4. Check left/right speakers (if available)

### 9. 📷 **Camera Test**
**Purpose**: Test webcam and built-in camera
- Detect available cameras
- Test photo capability
- Check image quality

**How to use**:
1. View camera status
2. Click "Open Camera" to test
3. Camera will display for 2 seconds
4. Check image clarity

**Note**: Requires OpenCV: `pip install opencv-python`

### 10. 🧠 **CPU Test (Expert Mode)**
**Purpose**: Stress test processor
- Display real-time CPU %
- Number of cores
- Current CPU frequency
- CPU temperature (if available)

**How to use**:
1. View initial CPU information
2. Click "Start Test" for stress test
3. CPU will run 100% for 10 seconds
4. Monitor temperature not exceeding 85°C

### 11. 🌡️ **Thermal Test (Expert Mode)**
**Purpose**: Monitor system temperature
- CPU temperature
- GPU temperature (if available)
- Fan speed
- Overheating warnings

**How to use**:
1. Let machine run normally for 5 minutes
2. View idle temperature
3. Run stress test and monitor
4. Safe temperatures: CPU <80°C, GPU <85°C

---

## 🎮 USAGE MODES

### 🟢 **Basic Mode**
- **Target**: Regular users
- **Duration**: 15-20 minutes
- **Includes**: 9 basic test steps
- **Suitable for**: Quick check before buying used laptop

### 🔴 **Expert Mode**
- **Target**: Technicians, knowledgeable users
- **Duration**: 30-45 minutes
- **Includes**: 13 comprehensive test steps
- **Suitable for**: Detailed inspection, professional assessment

---

## 🚨 COMMON ERROR TROUBLESHOOTING

### ❌ **"Cannot check (need admin rights)"**
- **Cause**: Missing Administrator privileges
- **Solution**: Right-click → "Run as administrator"

### ❌ **"OpenCV library missing"**
- **Cause**: OpenCV not installed
- **Solution**: `pip install opencv-python`

### ❌ **"No working camera found"**
- **Cause**: Camera disabled or broken
- **Solution**: Check Device Manager → Camera

### ❌ **"Battery check error"**
- **Cause**: Desktop computer or broken battery
- **Solution**: Normal for desktop computers

### ❌ **"CPU read error"**
- **Cause**: psutil error
- **Solution**: `pip install --upgrade psutil`

---

## 📞 Hỗ Trợ / Support
- **GitHub**: [Repository Link]
- **Email**: support@laptoptester.com
- **Version**: 2.0 Final

---

**© 2024 LaptopTester Team. All rights reserved.**