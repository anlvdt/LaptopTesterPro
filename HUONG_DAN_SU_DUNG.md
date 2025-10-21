# 📖 HƯỚNG DẪN SỬ DỤNG LAPTOPTESTER PRO

## 🎯 Giới thiệu
**LaptopTester Pro** là công cụ kiểm tra laptop toàn diện, giúp bạn đánh giá tình trạng phần cứng trước khi mua laptop cũ hoặc kiểm tra laptop hiện tại.

---

## 🚀 Khởi động ứng dụng

### Cách 1: Chạy từ Python
```bash
cd C:\MyApps\LaptopTester
python main_enhanced_auto.py
```

### Cách 2: Chạy từ file .exe (nếu đã build)
```bash
LaptopTester.exe
```

---

## 🎨 Giao diện chính

Khi khởi động, bạn sẽ thấy 4 tab chính:

### 1. 📊 **OVERVIEW (Tổng quan)**
- Hiển thị thông tin tổng quan về ứng dụng
- Giới thiệu các tính năng
- Hướng dẫn nhanh

### 2. ▶️ **START TEST (Bắt đầu test)**
- Chạy toàn bộ test theo thứ tự
- Tự động chuyển sang test tiếp theo
- Phù hợp cho test nhanh, toàn diện

### 3. 🔧 **INDIVIDUAL TESTS (Test riêng lẻ)**
- Chọn test cụ thể để chạy
- Phù hợp khi muốn test lại một phần cứng cụ thể
- Linh hoạt, tùy chỉnh

### 4. ❌ **EXIT (Thoát)**
- Thoát ứng dụng

---

## 📋 DANH SÁCH CÁC TEST

### 🔒 **Bảo mật & Định danh**

#### 1. **Hardware Fingerprint (Định danh phần cứng)**
- **Mục đích:** Kiểm tra cấu hình thực tế vs quảng cáo
- **Cách test:**
  - Test tự động chạy
  - So sánh thông tin CPU, RAM, GPU hiển thị
- **Đánh giá:**
  - ✅ Tốt: Thông tin khớp với mô tả
  - ❌ Lỗi: Có sai lệch (CPU yếu hơn, RAM ít hơn...)

#### 2. **Windows License (Bản quyền Windows)**
- **Mục đích:** Kiểm tra Windows có bản quyền không
- **Cách test:**
  - Test tự động chạy
  - Hiển thị trạng thái kích hoạt
- **Đánh giá:**
  - ✅ Tốt: Windows đã kích hoạt
  - ⚠️ Cảnh báo: Chưa kích hoạt (cần mua key)

### ⚙️ **Hiệu năng**

#### 3. **CPU Stress Test**
- **Mục đích:** Test CPU dưới tải cao, phát hiện throttling
- **Cách test:**
  1. Nhấn "Bắt đầu Test"
  2. CPU chạy 100% trong 3 phút
  3. Quan sát nhiệt độ và tần số
  4. Có thể nhấn "Dừng Test" bất cứ lúc nào
- **Đánh giá:**
  - ✅ Tốt: CPU ổn định, không giảm xung
  - ⚠️ Cảnh báo: Nhiệt độ cao >85°C
  - ❌ Lỗi: CPU giảm xung nhiều, >90°C

#### 4. **GPU Stress Test**
- **Mục đích:** Test GPU với đồ họa nặng
- **Cách test:**
  1. Nhấn "Bắt đầu Test"
  2. Cửa sổ pygame hiện lên (800x600)
  3. Quan sát particles, effects
  4. **Nhấn ESC hoặc "Dừng Test" để dừng**
- **Lưu ý:**
  - ⭐ Text vàng nhấp nháy: "Nhấn ESC để dừng"
  - ⭐ Cửa sổ KHÔNG fullscreen
  - ⭐ Quan sát FPS, Particles count
- **Đánh giá:**
  - ✅ Tốt: Không có artifacts, FPS ổn định
  - ❌ Lỗi: Có sọc, chớp, đốm màu lạ

#### 5. **HDD Speed (Tốc độ ổ cứng)**
- **Mục đích:** Đo tốc độ đọc/ghi ổ cứng
- **Cách test:**
  1. Nhấn "Bắt đầu Test"
  2. Đợi test hoàn thành
  3. Xem kết quả MB/s
- **Đánh giá:**
  - ✅ SSD: >300 MB/s
  - ✅ HDD: >80 MB/s
  - ❌ Chậm: <50 MB/s (HDD lỗi)

#### 6. **System Stability (Ổn định hệ thống)**
- **Mục đích:** Test tổng hợp CPU+GPU+RAM
- **Cách test:**
  1. Nhấn "Bắt đầu Test (3-5 phút)"
  2. Test chạy 180 giây
  3. Quan sát: "Thời gian: Xs / 180s | CPU | RAM | Nhiệt độ"
  4. **Có thể nhấn "Dừng Test" để dừng**
- **Đánh giá:**
  - ✅ Tốt: Hệ thống ổn định, không restart
  - ❌ Lỗi: Máy restart, đơ, tắt nguồn

### 🖥️ **Giao diện**

#### 7. **Screen Test (Kiểm tra màn hình)**
- **Mục đích:** Phát hiện dead pixel, màu sắc
- **Cách test:**
  1. Nhấn các nút màu: Red, Green, Blue, White, Black
  2. Quan sát toàn màn hình
  3. Tìm điểm sáng, tối bất thường
- **Đánh giá:**
  - ✅ Tốt: Không có dead pixel
  - ❌ Lỗi: Có điểm sáng/tối, màu lệch

#### 8. **Keyboard & Touchpad**
- **Mục đích:** Test từng phím và touchpad
- **Cách test:**
  1. Nhấn từng phím trên bàn phím
  2. Phím bật sáng khi hoạt động
  3. Vẽ trên canvas để test touchpad
  4. Nhấn "Xóa vết vẽ" để xóa
- **Đánh giá:**
  - ✅ Tốt: Tất cả phím hoạt động, touchpad mượt
  - ❌ Lỗi: Có phím không bật sáng, touchpad đơ

#### 9. **Audio Test (Loa & Micro)**
- **Mục đích:** Test loa và micro
- **Cách test:**
  - **Loa:** Nhấn "▶️ Play Test Sound" để nghe
  - **Micro:** Nhấn "🎤 Ghi âm" → Nói → "⏹️ Dừng" → "▶️ Phát"
- **Đánh giá:**
  - ✅ Tốt: Loa rõ ràng, mic thu âm tốt
  - ❌ Lỗi: Loa rè, mic không thu được âm

#### 10. **Webcam Test**
- **Mục đích:** Test camera
- **Cách test:**
  1. Nhấn "📷 Start Webcam"
  2. Xem hình ảnh camera
  3. Nhấn "📸 Capture Photo" để chụp
  4. Nhấn "⏹️ Stop Webcam" để dừng
- **Đánh giá:**
  - ✅ Tốt: Hình ảnh rõ nét
  - ❌ Lỗi: Mờ, nhiễu, không hoạt động

### 🔋 **Phần cứng**

#### 11. **Battery Health (Pin laptop)**
- **Mục đích:** Kiểm tra tình trạng pin
- **Cách test:**
  - Test tự động hiển thị thông tin pin
  - Xem Design Capacity vs Full Charge Capacity
- **Đánh giá:**
  - ✅ Tốt: >80% dung lượng thiết kế
  - ⚠️ Cảnh báo: 50-80%
  - ❌ Lỗi: <50% (pin chai)

#### 12. **HDD Health (Sức khỏe ổ cứng)**
- **Mục đích:** Kiểm tra SMART status
- **Cách test:**
  - Test tự động chạy
  - Hiển thị SMART attributes
- **Đánh giá:**
  - ✅ Tốt: SMART status OK
  - ❌ Lỗi: Có bad sectors, cảnh báo SMART

#### 13. **Network Test (Kiểm tra mạng)**
- **Mục đích:** Test kết nối mạng
- **Cách test:**
  1. Nhấn "Bắt đầu Test"
  2. Ping Google, Cloudflare
  3. Test tốc độ download
- **Đánh giá:**
  - ✅ Tốt: Ping <50ms, tốc độ tốt
  - ❌ Lỗi: Không kết nối được

---

## 📊 BÁO CÁO TỔNG KẾT

Sau khi hoàn thành tất cả test, bạn sẽ thấy **Summary (Tổng kết)**:

### Nội dung báo cáo:

#### 1. **Thống kê tổng quan**
- Tổng số test
- Số test đạt
- Số test lỗi
- Tỷ lệ thành công (%)

#### 2. **Đánh giá tổng thể**
- 🟢 **LAPTOP TÌNH TRẠNG TỐT** (>90% test đạt)
- 🟡 **LAPTOP CẦN CHÚ Ý** (70-90% test đạt)
- 🔴 **LAPTOP CÓ VẤN ĐỀ NGHIÊM TRỌNG** (<70% test đạt)

#### 3. **Chi tiết từng category**
- 🔒 Bảo mật & Định danh
- ⚙️ Hiệu năng
- 🖥️ Giao diện
- 🔋 Phần cứng

#### 4. **Phân tích khả năng sử dụng**
- Dựa trên CPU, GPU, RAM
- Gợi ý: Office, Gaming, Rendering, v.v.

#### 5. **Xuất báo cáo**
- 📄 **Export PDF**: Xuất file PDF
- 📊 **Export Excel**: Xuất file Excel
- 📋 **Copy Text**: Copy text vào clipboard

---

## ⚙️ CÀI ĐẶT & TÙY CHỈNH

### Thay đổi ngôn ngữ
- Nhấn nút **"Language"** ở góc trên
- Chuyển giữa Tiếng Việt ↔ English

### Thay đổi theme
- Nhấn nút **"Dark/Light"** ở góc trên
- Chuyển giữa Dark mode ↔ Light mode

### Chế độ Expert
- Nhấn nút **"Expert Mode"**
- Hiển thị thông tin kỹ thuật chi tiết hơn

---

## 💡 MẸO SỬ DỤNG

### ✅ Khi mua laptop cũ:
1. Chạy **START TEST** để test toàn bộ
2. Chú ý **Hardware Fingerprint** (kiểm tra cấu hình)
3. Chú ý **Battery Health** (pin còn bao nhiêu %)
4. Chú ý **Screen Test** (dead pixel)
5. Chú ý **Keyboard Test** (phím nào lỗi)

### ✅ Khi laptop đang dùng bị lỗi:
1. Chạy **INDIVIDUAL TESTS**
2. Test phần cứng nghi ngờ lỗi
3. VD: Máy nóng → chạy **CPU Stress Test**, **Thermal Test**

### ✅ Kiểm tra định kỳ:
- Mỗi 3-6 tháng chạy một lần
- Theo dõi **Battery Health**, **HDD Health**
- So sánh hiệu năng có giảm không

---

## ⚠️ LƯU Ý QUAN TRỌNG

### ❌ KHÔNG nên:
- Chạy stress test khi laptop đang sạc ở nhiệt độ cao
- Chạy GPU test trên laptop cũ yếu quá (có thể tắt máy)
- Bỏ qua cảnh báo nhiệt độ >90°C

### ✅ NÊN:
- Đặt laptop trên bề mặt phẳng, thoáng khi test
- Cắm sạc khi chạy stress test
- Quan sát kỹ màn hình khi test Screen
- Test từng phím một khi test Keyboard

---

## 🔧 XỬ LÝ LỖI

### Lỗi: "Pygame không có sẵn"
```bash
pip install pygame
```

### Lỗi: "Permission denied" khi test HDD
- Chạy ứng dụng với quyền Administrator

### Lỗi: "Camera not found"
- Kiểm tra camera có được bật trong Settings không
- Kiểm tra driver camera

### Test bị đơ:
- Nhấn nút **"Dừng Test"**
- Nếu không được, nhấn **ESC** (với GPU test)
- Restart ứng dụng nếu cần

---

## 📞 HỖ TRỢ

### Báo lỗi:
1. Chụp ảnh màn hình lỗi
2. Ghi lại các bước tái hiện lỗi
3. Gửi về email hoặc GitHub Issues

### Yêu cầu tính năng mới:
- Mô tả tính năng cần thêm
- Giải thích tại sao cần tính năng đó

---

## 🎓 KINH NGHIỆM MUA LAPTOP CŨ

### Phần cứng quan trọng nhất:
1. **Pin** - Khó thay, đắt
2. **Màn hình** - Dead pixel, ghosting
3. **Bàn phím** - Phím lỗi khó sửa
4. **Mainboard** - Cổng lỏng, lỗi nghiêm trọng

### Có thể chấp nhận:
- Pin chai 70-80% (có thể dùng sạc liên tục)
- CPU/RAM yếu hơn quảng cáo 1 chút
- Ổ cứng chậm (có thể thay)

### KHÔNG nên mua:
- Pin <50%
- Dead pixel nhiều
- Phím nhiều chữ lỗi
- Cổng sạc lỏng
- Máy tự tắt khi stress test

---

## ✨ TÍNH NĂNG NỔI BẬT

### 🎯 Test toàn diện 13+ tests
### ⚡ Nút dừng test bất cứ lúc nào
### 🌐 Hỗ trợ 2 ngôn ngữ (VI/EN)
### 🎨 Theme tối/sáng
### 📊 Báo cáo PDF/Excel
### 🔧 Test riêng lẻ linh hoạt
### 💻 Giao diện đẹp, dễ dùng

---

**Chúc bạn tìm được chiếc laptop ưng ý! 🚀**
