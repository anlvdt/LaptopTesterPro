# 📖 HƯỚNG DẪN CHI TIẾT - PHẦN 3

## CÁC TEST NÂNG CAO (EXPERT MODE)

### 10. 🔥 CPU Stress Test

**Mục đích**: Kiểm tra khả năng tản nhiệt và phát hiện throttling

**Test 2 phút**:
- Đẩy CPU lên 100% tải
- Theo dõi nhiệt độ, tần số, throttling
- Phát hiện vấn đề tản nhiệt

**Thông tin hiển thị**:
- ⚡ CPU Usage: X%
- 🌡️ Temperature: X°C
- 📡 Frequency: X MHz
- ⚠️ Throttling: None / Light / Moderate / Severe

**Phân tích throttling**:
- **None**: Không throttling → Tản nhiệt tốt
- **Light**: Throttling nhẹ → Chấp nhận được
- **Moderate**: Throttling trung bình → Cần chú ý
- **Severe**: Throttling nghiêm trọng → Vấn đề lớn

**Phát hiện khóa xung CPU**:
- Nếu tần số cố định (biến thiên <5%)
- Cảnh báo: "🔒 PHÁT HIỆN KHÓA XUNG CPU"
- Nguyên nhân: BIOS khóa, phần mềm hạn chế, chế độ tiết kiệm pin
- Giải pháp: Kiểm tra BIOS, chế độ nguồn Windows

**Cảnh báo nhiệt độ**:
- >70°C: ⚠️ Cảnh báo (màu vàng)
- >80°C: ⚠️ Nhiệt độ cao (màu cam)
- >95°C: 🚨 Nguy hiểm (màu đỏ)

**Giải pháp nếu throttling**:
- Vệ sinh quạt tản nhiệt
- Thay keo tản nhiệt
- Kiểm tra adapter nguồn (phải đúng watt)
- Cập nhật BIOS và driver

**Nút điều khiển**:
- ▶️ **Bắt đầu Test**: Chạy test 2 phút
- ⏹️ **Dừng Test**: Dừng bất cứ lúc nào

---

### 11. ⚡ Hard Drive Speed Test

**Mục đích**: Đo tốc độ đọc/ghi thực tế của ổ cứng

**Test 512MB**:
- Ghi tuần tự 512MB
- Đọc tuần tự 512MB
- Hiển thị tốc độ real-time

**Thông tin hiển thị**:
- 📝 Đang ghi: X MB/s (Trung bình: Y MB/s)
- 📖 Đang đọc: X MB/s (Trung bình: Y MB/s)
- 📊 Tiến độ: X%

**Kết quả**:
- Tốc độ Ghi: X MB/s
- Tốc độ Đọc: Y MB/s

**So sánh chuẩn**:
- **SSD NVMe**: 1500-3500 MB/s (đọc), 1000-3000 MB/s (ghi)
- **SSD SATA**: 400-550 MB/s (đọc/ghi)
- **HDD 7200rpm**: 80-160 MB/s (đọc/ghi)
- **HDD 5400rpm**: 50-120 MB/s (đọc/ghi)

**Đánh giá**:
- ✅ Đạt chuẩn → Tốt
- ⚠️ Thấp hơn 30% → Cần kiểm tra
- ❌ Quá chậm → Ổ cứng có vấn đề

---

### 12. 🎮 GPU Stress Test

**Mục đích**: Test GPU với đồ họa nặng, phát hiện artifacts

**Test 60 giây**:
- Cửa sổ 800x600 (KHÔNG fullscreen)
- Render particles, geometric patterns
- Hiển thị FPS real-time

**Thông tin hiển thị**:
- 🎮 FPS: X (real-time)
- 🎨 Particles: X
- ⏱️ Thời gian: X/60s
- 📊 Tiến độ: X%

**Quan sát**:
- Chớp giật (flickering)
- Sọc ngang (horizontal lines)
- Đốm màu lạ (color artifacts)
- Treo máy (freezing)

**Kết quả**:
- 🎮 FPS trung bình: X
- 🔻 FPS thấp nhất: X
- 🔺 FPS cao nhất: X
- 🎥 Tổng frames: X

**Đánh giá**:
- ✅ FPS ổn định >30, không artifacts → GPU tốt
- ⚠️ FPS dao động mạnh → Cần chú ý
- ❌ Có artifacts, treo máy → GPU có vấn đề

**Điều khiển**:
- ⏹️ **Stop Test**: Nhấn nút trên UI
- **ESC**: Nhấn trong cửa sổ test
- **X**: Đóng cửa sổ

---

### 13. 🌐 Network Test

**Mục đích**: Kiểm tra kết nối Internet, WiFi, DNS

**5 Test tự động**:

1. **Internet Connectivity**
   - Test kết nối đến Google, Cloudflare, OpenDNS
   - ✅ Kết nối thành công
   - ❌ Không kết nối được

2. **DNS Resolution**
   - Test phân giải domain: google.com, facebook.com, youtube.com
   - ✅ DNS hoạt động
   - ❌ DNS lỗi

3. **WiFi Information**
   - SSID: Tên mạng WiFi
   - Signal Strength: Cường độ tín hiệu
   - ✅ Có thông tin WiFi
   - ⚠️ Không có WiFi (dùng dây)

4. **Download Speed**
   - Đo tốc độ download thực tế
   - Kết quả: X Mbps
   - ✅ Tốc độ tốt (>10 Mbps)
   - ⚠️ Tốc độ chậm (<5 Mbps)

5. **Ping Test**
   - Ping đến Google, Cloudflare, FPT, VNPT
   - Kết quả: X ms
   - ✅ Ping thấp (<50ms)
   - ⚠️ Ping cao (>100ms)

**Đánh giá**:
- ✅ Tất cả test pass → Mạng tốt
- ⚠️ Một số test fail → Có vấn đề nhỏ
- ❌ Nhiều test fail → Mạng có vấn đề

---

### 14. 🌡️ Thermal Monitor

**Mục đích**: Giám sát nhiệt độ và hiệu năng real-time

**Thông tin hiển thị**:
- 🌡️ CPU: X°C (màu xanh/vàng/đỏ)
- ⚡ CPU: X%
- 💾 Memory: X%

**Biểu đồ real-time**:
- Đường nhiệt độ CPU theo thời gian
- Cập nhật mỗi giây

**Cách sử dụng**:
1. Nhấn **"🚀 Start Monitor"**
2. Mở các ứng dụng nặng (game, video, Photoshop)
3. Quan sát nhiệt độ có tăng cao không
4. Nhấn **"⏹️ Stop"** khi xong

**Đánh giá**:
- ✅ Nhiệt độ <80°C khi tải nặng → Tản nhiệt tốt
- ⚠️ Nhiệt độ 80-90°C → Cần chú ý
- ❌ Nhiệt độ >90°C → Tản nhiệt kém

---

## CÁC TEST BỔ SUNG

### 15. 👁️ Physical Inspection (Kiểm Tra Ngoại Hình)

**Checklist 40+ điểm**:

**💻 Vỏ Máy & Bản Lề**:
- ✓ Vỏ máy: Vết nứt, móp méo (đặc biệt góc máy)
- ✓ Bản lề: Mở/đóng 10-15 lần, nghe tiếng kêu
- ✓ Bản lề giữ góc: Không rơ, không tự đóng
- ✓ Vết nứt gần bản lề: DẤU HIỆU NGUY HIỂM

**🔌 Cổng Kết Nối**:
- ✓ Cổng sạc: Cắm và lay nhẹ, KHÔNG được lỏng
- ✓ USB: Cắm thử USB, kiểm tra độ chặt
- ✓ HDMI/DisplayPort: Không bị lỏng lẻo
- ✓ Audio jack: Cắm tai nghe thử

**🔩 Ốc Vít & Tem**:
- ✓ Ốc vít: Không toét đầu (dấu hiệu tháo lắp)
- ✓ Tem bảo hành: Còn nguyên, không bị bóc
- ✓ Serial number: Khớp với BIOS và sticker
- ✓ Khe tản nhiệt: Không bị bịt tắc bụi

**🔴 THINKPAD ĐẶC BIỆT**:
- ✓ Tem Lenovo chính hãng: Hologram
- ✓ Sticker dưới đáy: COA Windows, Serial, Model
- ✓ TrackPoint (nút đỏ): Hoạt động, không lỏng
- ✓ ThinkLight/Đèn bàn phím: Test hoạt động
- ✓ Khe Kensington Lock: Không bị gãy

---

### 16. ⚙️ BIOS Check (Kiểm Tra Cài Đặt BIOS)

**Cách vào BIOS**:
- Dell/Alienware: F2 hoặc F12
- HP/Compaq: F10 hoặc ESC
- Lenovo/ThinkPad: F1, F2 hoặc Enter
- ASUS: F2 hoặc Delete
- Acer: F2 hoặc Delete
- MSI: Delete hoặc F2

**Checklist 30+ cài đặt**:

**⚡ Hiệu Năng CPU**:
- ✓ Intel Turbo Boost: Phải 'Enabled'
- ✓ AMD Turbo Core: Phải 'Enabled'
- ✓ CPU C-States: Nên 'Enabled' (tiết kiệm pin)
- ✓ Virtualization (VT-x/AMD-V): 'Enabled' nếu dùng VM

**💾 RAM**:
- ✓ XMP/DOCP Profile: Nên bật (RAM chạy đúng tốc độ)
- ✓ Kiểm tra dung lượng RAM hiển thị khớp

**⛔ CẢNH BÁO NGHIÊM TRỌNG - MẬT KHẨU BIOS**:
- 🚫 Supervisor/Admin Password: Phải TRỐNG
- 🚫 HDD/SSD Password: Phải TRỐNG
- ❌ Nếu có mật khẩu: KHÔNG MUA!

**Đặc biệt ThinkPad**:
- Mật khẩu BIOS ThinkPad gần như KHÔNG THỂ phá
- Phá phải thay Mainboard (5-10 triệu)
- Nếu khóa HDD: Ổ cứng thành gạch!

**🔒 Bảo Mật Khác**:
- ⚠️ Computrace/Absolute: Phải 'Disabled' hoặc 'Inactive'
- ⚠️ Intel AMT/vPro: Nên 'Disabled' (trừ doanh nghiệp)
- ✓ Secure Boot: 'Enabled' cho bảo mật
- ✓ TPM: 'Enabled' (Windows 11 yêu cầu)

---

### 17. 🔥 System Stability (Test Ổn Định Tổng Hợp)

**Mục đích**: Test CPU + GPU + RAM đồng thời

**Test 3 phút**:
- CPU stress: Multi-process stress tất cả cores
- GPU stress: pygame rendering trong background
- RAM monitor: Theo dõi memory usage
- Temperature monitor: Theo dõi nhiệt độ

**Thông tin hiển thị**:
- CPU: X%
- GPU: Y%
- RAM: Z%
- Temp: T°C

**Đánh giá**:
- ✅ Không treo, nhiệt độ <90°C → Hệ thống ổn định
- ⚠️ Nhiệt độ cao, throttling → Cần chú ý
- ❌ Treo máy, tự khởi động lại → Không ổn định

---

## 📊 BÁO CÁO TỔNG KẾT

### Thông Tin Hiển Thị

**Quick Stats**:
- 📋 Tổng Test: X
- ✅ Đạt: Y
- ❌ Lỗi: Z
- 📊 Tỷ Lệ Đạt: W%

**Đánh Giá Tổng Thể**:
- ✅ **>80%**: LAPTOP TÌNH TRẠNG TỐT
- ⚠️ **60-80%**: LAPTOP CẦN CHÚ Ý
- ❌ **<60%**: LAPTOP CÓ VẤN ĐỀ NGHIÊM TRỌNG

**Phân Loại Theo Category**:
- 🔒 Bảo mật & Định danh
- ⚡ Hiệu năng
- 🖥️ Giao diện
- 💻 Phần cứng

**Công Cụ Chuyên Nghiệp Bổ Sung**:
- CrystalDiskMark: Test ổ cứng chuyên sâu
- HWiNFO64: Thông tin phần cứng chi tiết
- MemTest86: Test RAM chuyên sâu
- FurMark: GPU stress test chuyên nghiệp

**Export Báo Cáo**:
- 📄 **Xuất PDF**: Báo cáo đầy đủ với charts
- 📊 **Xuất Excel**: Dữ liệu để phân tích
- 📋 **Copy Text**: Tóm tắt nhanh

---

## 💡 MẸO SỬ DỤNG

### Trước Khi Test

1. **Sạc đầy pin** (>80%) để test chính xác
2. **Đóng tất cả ứng dụng** đang chạy
3. **Kết nối Internet** để test mạng
4. **Chuẩn bị USB** để test cổng USB
5. **Chuẩn bị tai nghe** để test audio jack

### Trong Khi Test

1. **Đọc kỹ hướng dẫn** mỗi bước (bên trái)
2. **Không vội vàng** - làm từng bước cẩn thận
3. **Chụp ảnh kết quả** quan trọng
4. **Ghi chú vấn đề** phát hiện được
5. **Có thể bỏ qua** test không cần thiết

### Sau Khi Test

1. **Xem báo cáo tổng kết** kỹ
2. **Export PDF** để lưu trữ
3. **So sánh với giá** người bán đưa ra
4. **Thương lượng giá** nếu có vấn đề
5. **Quyết định mua** dựa trên kết quả

---

## ❓ GIẢI ĐÁP THẮC MẮC

**Q: Test mất bao lâu?**
A: Basic 20-30 phút, Expert 40-60 phút, Individual tùy chọn

**Q: Có cần Internet không?**
A: Không bắt buộc, nhưng cần để test mạng

**Q: Có thể dừng giữa chừng không?**
A: Có, nhấn "Dừng Test" hoặc ESC

**Q: Kết quả có chính xác không?**
A: 90-95% chính xác, nên dùng thêm tools chuyên nghiệp

**Q: Có thể test nhiều lần không?**
A: Có, không giới hạn số lần test

**Q: Có hại cho laptop không?**
A: Không, các test an toàn

**Q: Cần quyền Administrator không?**
A: Một số test cần (BIOS info, battery report)

**Q: Hỗ trợ laptop Mac không?**
A: Chưa hỗ trợ tốt, chỉ tối ưu cho Windows

---

## 📞 HỖ TRỢ

**Địa chỉ**: 237/1C Tôn Thất Thuyết, P. Vĩnh Hải (P.3, Q.4 cũ), TPHCM

**Donate MoMo**: 0976896621

**Shopee Affiliate**: https://s.shopee.vn/7AUkbxe8uu

---

**Phát triển bởi**: Laptop Lê Ân & Gemini AI  
**Phiên bản**: 2.0 Final  
**Cập nhật**: 2024-01-XX
