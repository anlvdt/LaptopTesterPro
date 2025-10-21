# 📖 HƯỚNG DẪN CHI TIẾT - PHẦN 2

## MODE 2: CHUYÊN GIA (Expert Mode)

**Dành cho**: Người am hiểu kỹ thuật, mua laptop gaming/workstation

**Thời gian**: 40-60 phút

**14 Bước Test** (Bao gồm tất cả Basic + 5 test nâng cao):

### Các Test Cơ Bản (1-9): Giống Basic Mode

### Các Test Nâng Cao (10-14):

**10. 🔥 CPU Stress Test**
- Đẩy CPU lên 100% tải trong 2 phút
- Theo dõi nhiệt độ, tần số, throttling
- Phát hiện vấn đề tản nhiệt

**11. ⚡ Tốc Độ Ổ Cứng**
- Test tốc độ đọc/ghi thực tế
- Ghi 512MB → Đọc 512MB
- So sánh với chuẩn SSD/HDD

**12. 🎮 GPU Stress Test**
- Test GPU với đồ họa nặng 60 giây
- Hiển thị FPS, Particles
- Phát hiện artifacts, flickering

**13. 🌐 Kiểm Tra Mạng**
- Test Internet, DNS, WiFi
- Đo tốc độ download
- Test ping đến nhiều server

**14. 🌡️ Thermal Monitor**
- Giám sát nhiệt độ CPU, RAM real-time
- Có thể mở app nặng để test
- Xem biểu đồ nhiệt độ

**Cách sử dụng**:
1. Nhấn **"🔬 CHUYÊN GIA"**
2. Làm theo từng bước như Basic Mode
3. Các test nâng cao sẽ tự động chạy
4. Có thể nhấn **"Dừng Test"** bất cứ lúc nào
5. Xem báo cáo chi tiết với phân tích throttling, frequency drops

---

## MODE 3: TEST RIÊNG LẺ (Individual Tests)

**Dành cho**: Kiểm tra lại một tính năng cụ thể

**17 Tests Có Sẵn**:

### Nhóm Bảo Mật & Định Danh
1. **🔍 Hardware Fingerprint** - Định danh phần cứng từ BIOS
2. **🔑 License Check** - Kiểm tra bản quyền Windows
3. **💻 System Info** - Thông tin cấu hình hệ thống

### Nhóm Phần Cứng
4. **💿 Hard Drive Health** - Sức khỏe ổ cứng (S.M.A.R.T)
5. **⚡ Hard Drive Speed** - Tốc độ đọc/ghi ổ cứng
6. **🔋 Battery Health** - Sức khỏe pin và dung lượng

### Nhóm Giao Diện
7. **🖥️ Screen Test** - Kiểm tra màn hình (dead pixels, backlight bleeding)
8. **⌨️ Keyboard Test** - Bàn phím & Touchpad
9. **🔊 Audio Test** - Loa & Micro
10. **📷 Webcam Test** - Webcam

### Nhóm Kết Nối
11. **🌐 Network Test** - Kết nối mạng & WiFi

### Nhóm Hiệu Năng
12. **🔥 CPU Stress Test** - Test CPU
13. **🎮 GPU Stress Test** - Test GPU
14. **🌡️ Thermal Monitor** - Giám sát nhiệt độ
15. **🔥 System Stability** - Test ổn định tổng hợp (CPU+GPU+RAM)

### Nhóm Kiểm Tra Vật Lý
16. **👁️ Physical Inspection** - Checklist kiểm tra ngoại hình
17. **⚙️ BIOS Check** - Checklist kiểm tra cài đặt BIOS

**Cách sử dụng**:
1. Nhấn **"🎯 RIÊNG LẺ"**
2. Chọn test muốn chạy
3. Nhấn **"▶️ Chạy Test"**
4. Cửa sổ popup hiện ra với test
5. Làm theo hướng dẫn
6. Nhấn **"❌ Đóng"** khi xong

---

## 📋 CHI TIẾT TỪNG BƯỚC TEST

### 1. 🔍 Hardware Fingerprint (Định Danh Phần Cứng)

**Mục đích**: Đọc thông tin phần cứng TRỰC TIẾP từ BIOS - không thể giả mạo

**Checklist 8 điểm**:
- ✓ Model laptop từ BIOS
- ✓ Serial Number từ BIOS (không thể fake)
- ✓ CPU chính xác (tên, cores, threads)
- ✓ Dung lượng RAM thực tế
- ✓ Tất cả GPU (onboard + rời)
- ✓ Model và dung lượng ổ cứng
- ✓ Ngày phát hành BIOS
- ✓ UEFI/Legacy boot mode

**Cách thực hiện**:
1. Nhấn **"Bắt đầu Test"**
2. Chờ 5-10 giây để đọc thông tin
3. Xem thông tin chi tiết hiển thị
4. **QUAN TRỌNG**: So sánh với thông tin quảng cáo của người bán
5. Kiểm tra phần **"💡 Khả Năng Sử Dụng Phần Cứng"**
   - Ví dụ: "🎮 Gaming AAA & Rendering: Cyberpunk 2077, RDR2 Ultra"
   - Hoặc: "📝 Văn Phòng: Office, Web, Netflix 1080p"

**Cảnh báo**:
- 🔒 Thông tin này từ BIOS - KHÔNG THỂ GIẢ MẠO
- ⚠️ Nếu khác với quảng cáo → Có thể bị lừa đảo
- ⚠️ Nếu có cảnh báo model-specific → Chú ý kiểm tra kỹ

**Ví dụ cảnh báo**:
- "⚠️ ThinkPad X1: Kiểm tra kỹ bản lề - dễ bị lỏng"
- "⚠️ Dell XPS: Dễ bị coil whine và throttling"
- "⚠️ MacBook Pro 2016: Bàn phím butterfly dễ hỏng"

---

### 2. 🔑 License Check (Kiểm Tra Bản Quyền Windows)

**Mục đích**: Kiểm tra Windows có bản quyền hợp lệ không

**Checklist 5 điểm**:
- ✓ Chạy lệnh slmgr.vbs /xpr
- ✓ Xác định: Vĩnh viễn / Có hạn / Chưa kích hoạt
- ✓ Kiểm tra ngày hết hạn (nếu có)
- ✓ Đánh giá tính hợp pháp
- ✓ Cảnh báo nếu chưa kích hoạt

**Kết quả có thể**:
- ✅ **"Windows được kích hoạt vĩnh viễn"** → Tốt
- ⚠️ **"Windows sẽ hết hạn vào [ngày]"** → Cần chú ý
- ❌ **"Windows chưa được kích hoạt"** → Không tốt

**Lưu ý**:
- Windows có bản quyền → Nhận updates bảo mật
- Windows không bản quyền → Rủi ro pháp lý, không update

---

### 3. 💻 System Info (Thông Tin Hệ Thống)

**Mục đích**: Hiển thị thông tin Windows nhận diện và so sánh với BIOS

**So sánh tự động**:
- CPU (BIOS) vs CPU (Windows)
- ✅ Khớp → Tốt
- ⚠️ Có sai lệch → Kiểm tra lại

**Thông tin hiển thị**:
- CPU: Tên, cores, threads, tần số
- RAM: Dung lượng, số slot, tốc độ
- GPU: Tất cả card đồ họa
- Ổ cứng: Model, dung lượng, interface

---

### 4. 💿 Hard Drive Health (Sức Khỏe Ổ Cứng)

**Mục đích**: Đọc "báo cáo y tế" (S.M.A.R.T) của ổ cứng

**Kết quả**:
- ✅ **"Tốt"** → Ổ cứng khỏe mạnh
- ⚠️ **"Lỗi/Cảnh báo"** → Ổ cứng sắp hỏng, rủi ro cao

**Lưu ý**:
- Ổ cứng sắp hỏng = Mất dữ liệu
- Nếu "Lỗi" → Không nên mua hoặc giảm giá mạnh

---

### 5. 🖥️ Screen Test (Kiểm Tra Màn Hình)

**Mục đích**: Phát hiện điểm chết, hở sáng, ám màu, chớp giật

**Test tự động 5 màu**:
1. Đen (phát hiện hở sáng - backlight bleeding)
2. Trắng (phát hiện điểm chết, ám màu)
3. Đỏ (phát hiện pixel lỗi)
4. Xanh lá (phát hiện pixel lỗi)
5. Xanh dương (phát hiện pixel lỗi)

**Cách thực hiện**:
1. Nhấn **"Bắt đầu Test"**
2. Màn hình sẽ hiển thị toàn màn hình từng màu (3 giây/màu)
3. Quan sát kỹ:
   - **Pixel chết**: Chấm đen/sáng không đổi màu
   - **Hở sáng**: Vùng sáng bất thường trên nền đen
   - **Ám màu**: Vùng tối bất thường trên nền sáng
   - **Chớp giật**: Nhấp nháy ở viền màn hình
4. Nhấn **ESC** để dừng bất cứ lúc nào

**Đánh giá**:
- ✅ Không có vấn đề → Màn hình tốt
- ❌ Có điểm chết/hở sáng → Yêu cầu giảm giá hoặc không mua

---

### 6. ⌨️ Keyboard & Touchpad Test

**Mục đích**: Kiểm tra tất cả phím và touchpad hoạt động

**Layout 6 hàng đầy đủ**:
- Hàng 1: ESC, F1-F12, Delete, Insert, Home, Page Up/Down, End
- Hàng 2: `, 1-9, 0, -, =, Backspace
- Hàng 3: Tab, Q-P, [, ], \
- Hàng 4: Caps Lock, A-L, ;, ', Enter
- Hàng 5: Shift, Z-M, ,, ., /, Right Shift
- Hàng 6: Ctrl, Fn, Windows, Alt, Space, Right Alt, Right Ctrl, Arrow keys

**Cách test bàn phím**:
1. Gõ lần lượt TẤT CẢ các phím
2. Phím được nhấn → Sáng **xanh dương**
3. Phím được nhả → Chuyển **xanh lá**
4. Kiểm tra phím nào không đổi màu → Phím đó bị liệt

**Cách test touchpad**:
1. Di chuyển ngón tay trên vùng test → Vẽ vết
2. Click trái → Hiện chữ **"L"** màu đỏ
3. Click phải → Hiện chữ **"R"** màu xanh
4. Cuộn 2 ngón tay → Hiện mũi tên ↑↓
5. Xem số lần click được đếm

**Đánh giá**:
- ✅ Tất cả phím đổi màu, touchpad hoạt động → Tốt
- ❌ Có phím không đổi màu, touchpad không click được → Có vấn đề

---

### 7. 🔋 Battery Health (Sức Khỏe Pin)

**Mục đích**: Đánh giá tình trạng pin, dung lượng còn lại

**Thông tin hiển thị**:
- 🔋 Mức pin hiện tại: X%
- ⚡ Trạng thái: Sạc điện / Dùng pin
- ⏰ Thời gian còn lại / Thời gian sạc đầy
- 💾 Dung lượng thiết kế: X Wh
- 💾 Dung lượng hiện tại: X Wh
- ✅ Sức khỏe pin: X% (Tốt/Trung bình/Yếu)
- 🔄 Chu kỳ sạc: X cycles

**Đánh giá**:
- ✅ **>80%**: Pin còn tốt
- ⚠️ **60-80%**: Pin trung bình, cần chăm sóc
- ❌ **<60%**: Pin yếu, nên thay

**Lời khuyên chăm sóc pin**:
- ✓ Giữ pin 20-80% để kéo dài tuổi thọ
- ✓ Rút sạc khi đã đầy nếu không dùng lâu
- ✓ Tránh để pin xuống <20% thường xuyên
- ✓ Dùng sạc chính hãng
- ✗ Tránh sạc qua đêm thường xuyên
- ✗ Tránh để pin xuống 0%

---

### 8. 🔊 Audio Test (Loa & Micro)

**Mục đích**: Kiểm tra loa và micro hoạt động

**Test loa**:
1. Nhấn **"🎵 Phát Stereo Test"**
2. Nghe file stereo_test.mp3 (nếu có)
3. Hoặc nghe tone test 440Hz
4. Kiểm tra:
   - Loa trái/phải đều có tiếng
   - Không bị rè, lạc, méo
   - Âm lượng đủ lớn

**Test micro**:
1. Nhấn **"🎤 Ghi âm"**
2. Nói vào micro 5 giây
3. Nhấn **"⏹️ Dừng"**
4. Kiểm tra có ghi được âm không

**Đánh giá**:
- ✅ Loa rõ ràng, micro ghi được → Tốt
- ❌ Loa rè/méo, micro không hoạt động → Có vấn đề

---

### 9. 📷 Webcam Test

**Mục đích**: Kiểm tra webcam hoạt động và chất lượng

**Cách test**:
1. Nhấn **"Bắt đầu Test Camera"**
2. Webcam sẽ mở và hiển thị hình ảnh
3. Kiểm tra:
   - Hình ảnh rõ nét
   - Màu sắc chính xác
   - Không bị mờ/nhòe
4. **Test phát hiện vật cản**:
   - Che camera bằng tay
   - Ứng dụng sẽ phát hiện và cảnh báo
5. Nhấn **"Dừng Camera"** khi xong

**Thông tin hiển thị**:
- 📷 Độ phân giải tối đa: 1920x1080 (hoặc thấp hơn)
- 🎥 FPS: 30 fps
- ⚠️ Cảnh báo nếu phát hiện vật cản

**Đánh giá**:
- ✅ Hình ảnh rõ, phát hiện vật cản → Tốt
- ❌ Không mở được, hình mờ → Có vấn đề

