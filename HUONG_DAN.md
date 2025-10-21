# 📖 HƯỚNG DẪN SỬ DỤNG LAPTOPTESTER PRO

## 🚀 CÁCH CHẠY ỨNG DỤNG

### Cách 1: Chạy nhanh (Khuyến nghị)
1. Double-click file **RUN.bat**
2. Đợi cài đặt thư viện (chỉ lần đầu)
3. Ứng dụng sẽ tự động mở

### Cách 2: Chạy thủ công
```bash
# Cài đặt thư viện (chỉ lần đầu)
pip install -r requirements.txt

# Chạy ứng dụng
python main_enhanced_auto.py
```

---

## 🎯 CÁC CHỂ ĐỘ KIỂM TRA

### 1️⃣ CHẾ ĐỘ CƠ BẢN (Basic Mode)
**Dành cho:** Người dùng thông thường, kiểm tra nhanh

**Bao gồm 10 bước:**
1. 🔒 Định danh phần cứng (BIOS)
2. 🔑 Bản quyền Windows
3. ⚙️ Cấu hình hệ thống
4. 💿 Sức khỏe ổ cứng
5. 🖥️ Màn hình
6. ⌨️ Bàn phím & Touchpad
7. 🔋 Pin
8. 🔊 Loa & Micro
9. 📹 Webcam
10. 🌐 Mạng

**Thời gian:** 15-20 phút

---

### 2️⃣ CHẾ ĐỘ CHUYÊN GIA (Expert Mode)
**Dành cho:** Người am hiểu kỹ thuật, kiểm tra chuyên sâu

**Bao gồm:** 10 bước cơ bản + 5 bước nâng cao:
11. 🔥 CPU Stress Test (2-3 phút)
12. ⚡ Tốc độ ổ cứng (1-2 phút)
13. 🎮 GPU Stress Test (1 phút)
14. 🌡️ Nhiệt độ & Hiệu năng
15. 🔧 System Stability Test

**Thời gian:** 30-40 phút

---

### 3️⃣ CHẾ ĐỘ TEST RIÊNG LẺ (Individual Test)
**Dành cho:** Kiểm tra từng tính năng cụ thể

**Cách sử dụng:**
1. Chọn "🔧 Kiểm Tra Riêng Lẻ"
2. Chọn bài test muốn chạy
3. Test xong nhấn "✖ Đóng"
4. Quay lại chọn test khác hoặc về trang chủ

---

## 📋 HƯỚNG DẪN TỪNG BƯỚC

### Bước 1: Định danh phần cứng
- **Mục đích:** Đọc thông tin từ BIOS (không thể giả mạo)
- **Cách làm:** Nhấn "Bắt đầu Test" → Đợi 5-10 giây
- **Lưu ý:** So sánh với thông tin quảng cáo của người bán

### Bước 2: Bản quyền Windows
- **Mục đích:** Kiểm tra Windows có bản quyền hợp lệ
- **Kết quả tốt:** "Kích hoạt vĩnh viễn"
- **Cảnh báo:** "Chưa kích hoạt" hoặc "Sẽ hết hạn"

### Bước 3: Cấu hình hệ thống
- **Mục đích:** So sánh thông tin Windows với BIOS
- **Kết quả tốt:** "✅ Khớp"
- **Cảnh báo:** "⚠️ Có sai lệch" → Kiểm tra lại

### Bước 4: Sức khỏe ổ cứng
- **Mục đích:** Đọc S.M.A.R.T status
- **Kết quả tốt:** "Tốt"
- **Nguy hiểm:** "Lỗi/Cảnh báo" → Ổ cứng sắp hỏng

### Bước 5: Màn hình
- **Mục đích:** Phát hiện pixel chết, hở sáng
- **Cách làm:** Nhấn "Bắt đầu Test" → Quan sát 5 màu
- **Nhấn ESC:** Để dừng test bất cứ lúc nào

### Bước 6: Bàn phím & Touchpad
- **Mục đích:** Test từng phím và chuột
- **Cách làm:** 
  - Gõ tất cả phím → Phím sáng xanh = OK
  - Vẽ trên vùng test touchpad
  - Click trái/phải để test chuột

### Bước 7: Pin
- **Mục đích:** Kiểm tra sức khỏe pin
- **Kết quả tốt:** >80% health
- **Cảnh báo:** 60-80% health
- **Nguy hiểm:** <60% health → Nên thay pin

### Bước 8: Loa & Micro
- **Mục đích:** Test âm thanh
- **Cách làm:**
  - Nhấn "🎵 Phát Stereo Test"
  - Nhấn "🎤 Ghi âm" để test micro

### Bước 9: Webcam
- **Mục đích:** Test camera
- **Cách làm:** Nhấn "Bắt đầu Test Camera"
- **Tính năng:** Tự động phát hiện vật cản (che camera)

### Bước 10: Mạng
- **Mục đích:** Test kết nối Internet, WiFi
- **Nhấn:** "Bắt đầu Test" để kiểm tra tự động

---

## 🔥 STRESS TEST (Chế độ Expert)

### CPU Stress Test
- **Mục đích:** Kiểm tra tản nhiệt CPU
- **Thời gian:** 2-3 phút
- **Quan sát:**
  - Nhiệt độ: <85°C = Tốt
  - Throttling: None/Light = Tốt
  - Tần số: Ổn định = Tốt

### GPU Stress Test
- **Mục đích:** Test card đồ họa
- **Thời gian:** 1 phút
- **Quan sát:** FPS ổn định, không có artifacts

### Tốc độ ổ cứng
- **Mục đích:** Đo tốc độ đọc/ghi thực tế
- **Thời gian:** 1-2 phút
- **Kết quả tốt:**
  - SSD: >300 MB/s
  - HDD: >80 MB/s

---

## 📊 BÁO CÁO KẾT QUẢ

### Sau khi hoàn thành test:
1. Xem tổng quan: Tỷ lệ đạt, số lỗi
2. Đọc đánh giá AI
3. Xem khả năng sử dụng phần cứng
4. Xuất báo cáo:
   - 📄 PDF: Báo cáo đầy đủ
   - 📊 Excel: Dữ liệu chi tiết
   - 📋 Copy Text: Sao chép nhanh

### Công cụ chuyên nghiệp bổ sung:
- 💾 CrystalDiskInfo: Kiểm tra ổ cứng
- 🌡️ HWiNFO64: Giám sát nhiệt độ
- ⚡ CPU-Z: Thông tin CPU/RAM
- 🎮 GPU-Z: Thông tin GPU
- 🔥 FurMark: Stress test GPU
- 🧠 MemTest86: Test RAM

---

## 🏠 QUAY VỀ TRANG CHỦ

**Mọi lúc, mọi nơi:**
- Nhấn nút **🏠 Trang chủ** ở góc trên bên trái
- Hoặc nhấn nút **❌ Thoát** ở màn hình chính

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Quyền Administrator
- Một số tính năng cần quyền Admin
- Click phải RUN.bat → "Run as Administrator"

### 2. Độ chính xác
- Ứng dụng phát triển bằng AI, có thể có sai sót
- Khuyến khích dùng thêm công cụ chuyên nghiệp

### 3. Khi có lỗi
- Đóng ứng dụng và chạy lại
- Kiểm tra đã cài đủ thư viện chưa
- Chạy với quyền Administrator

### 4. Laptop cũ
- Pin <60%: Cân nhắc thay pin
- Nhiệt độ >85°C: Vệ sinh tản nhiệt
- Ổ cứng "Lỗi": Nguy cơ mất dữ liệu cao

---

## 💡 MẸO SỬ DỤNG

1. **Chạy test đầy đủ:** Dùng chế độ Expert để kiểm tra kỹ
2. **Test riêng lẻ:** Khi chỉ cần kiểm tra 1 tính năng cụ thể
3. **Lưu báo cáo:** Export PDF để gửi cho người bán
4. **So sánh giá:** Dựa vào kết quả để thương lượng giá
5. **Kiểm tra lại:** Dùng công cụ chuyên nghiệp để xác nhận

---

## 🛒 MUA LAPTOP UY TÍN

Sau khi test xong, nếu muốn mua laptop mới hoặc cũ uy tín:
👉 **Truy cập:** https://s.shopee.vn/7AUkbxe8uu

**Ưu điểm:**
- ✅ Laptop chính hãng, bảo hành đầy đủ
- ✅ Giá cạnh tranh, nhiều ưu đãi
- ✅ Giao hàng toàn quốc
- ✅ Hỗ trợ trả góp 0%

---

## 📞 HỖ TRỢ

**Nếu gặp vấn đề:**
1. Đọc lại hướng dẫn này
2. Kiểm tra file README.md
3. Chạy lại với quyền Administrator

**Phát triển bởi:** LaptopTester Team
**Phiên bản:** 2.0
**Ngày cập nhật:** 2025

---

Made with ❤️ by LaptopTester Pro
