# 🔧 Individual Component Tests

## Tổng Quan

Module này cho phép test **từng thành phần riêng lẻ** của laptop mà không cần chạy toàn bộ wizard. Rất hữu ích khi:

- ✅ Muốn test nhanh một phần cứng cụ thể
- ✅ Debug vấn đề của từng component
- ✅ So sánh hiệu năng trước/sau nâng cấp
- ✅ Kiểm tra lại sau khi sửa chữa

## 📦 Cài Đặt

```bash
# Đảm bảo đã cài đặt dependencies
pip install -r requirements.txt

# Chạy individual tests
python individual_tests.py
```

## 🎯 Các Test Có Sẵn

### 1. Hardware Information Tests

#### 💻 Hardware Fingerprint
- **Mục đích**: Đọc thông tin phần cứng từ BIOS
- **Kiểm tra**: CPU, RAM, GPU, Serial Number, BIOS Date
- **Thời gian**: ~10 giây
- **Quan trọng**: ⭐⭐⭐⭐⭐ (Chống gian lận)

#### 🔑 Windows License
- **Mục đích**: Kiểm tra bản quyền Windows
- **Kiểm tra**: Activation status, expiry date
- **Thời gian**: ~5 giây
- **Quan trọng**: ⭐⭐⭐⭐

#### ⚙️ System Info
- **Mục đích**: So sánh thông tin Windows vs BIOS
- **Kiểm tra**: CPU mismatch detection
- **Thời gian**: ~10 giây
- **Quan trọng**: ⭐⭐⭐⭐

### 2. Storage Tests

#### 💿 HDD Health
- **Mục đích**: Kiểm tra sức khỏe ổ cứng
- **Kiểm tra**: S.M.A.R.T status, disk errors
- **Thời gian**: ~5 giây
- **Quan trọng**: ⭐⭐⭐⭐⭐ (Nguy cơ mất dữ liệu)

#### ⚡ HDD Speed (BENCHMARK)
- **Mục đích**: Đo tốc độ đọc/ghi thực tế
- **Kiểm tra**: 
  - Sequential Write Speed
  - Sequential Read Speed
  - Disk type detection (NVMe/SATA SSD/HDD)
- **Thời gian**: ~1-2 phút
- **File size**: 512MB
- **Quan trọng**: ⭐⭐⭐⭐⭐

**Kết quả mẫu:**
```
✍️ Tốc độ Ghi: 450.23 MB/s
📖 Tốc độ Đọc: 520.15 MB/s
🚀 Phân Tích: NVMe SSD (PCIe Gen3/4)

Khuyến nghị:
• Tốc độ xuất sắc cho gaming và workstation
• Phù hợp cho video editing 4K, 3D rendering
• Boot Windows trong 5-10 giây
```

**Cách đọc kết quả:**
- **> 400 MB/s**: NVMe SSD (Xuất sắc) 🚀
- **200-400 MB/s**: SATA SSD (Tốt) ⚡
- **100-200 MB/s**: HDD 7200 RPM (Trung bình) 💿
- **< 100 MB/s**: HDD 5400 RPM (Chậm) 🐌

### 3. Display & Input Tests

#### 🖥️ Screen Test
- **Mục đích**: Kiểm tra pixel chết, hở sáng
- **Kiểm tra**: Dead pixels, backlight bleeding, color accuracy
- **Thời gian**: ~30 giây
- **Quan trọng**: ⭐⭐⭐⭐

#### ⌨️ Keyboard & Mouse
- **Mục đích**: Test bàn phím và touchpad
- **Kiểm tra**: 
  - Key response (visual feedback)
  - Touchpad drawing test
  - Mouse click detection
- **Thời gian**: ~1-2 phút
- **Quan trọng**: ⭐⭐⭐⭐⭐

### 4. Power & Audio Tests

#### 🔋 Battery Health
- **Mục đích**: Đánh giá tình trạng pin
- **Kiểm tra**:
  - Design capacity vs Current capacity
  - Battery health percentage
  - Charge cycles
  - Time remaining
- **Thời gian**: ~5 giây
- **Quan trọng**: ⭐⭐⭐⭐⭐

**Kết quả mẫu:**
```
🔋 Mức Pin Hiện Tại: 85.3%
💾 Dung lượng thiết kế: 50.0 Wh
💾 Dung lượng hiện tại: 42.7 Wh
✅ Sức khỏe pin: 85.4%
🔄 Chu kỳ sạc: 146 chu kỳ
```

#### 🔊 Audio Test
- **Mục đích**: Test loa và micro
- **Kiểm tra**:
  - Stereo test (stereo_test.mp3)
  - Microphone recording
  - Audio quality
- **Thời gian**: ~30 giây
- **Quan trọng**: ⭐⭐⭐

### 5. Connectivity Tests

#### 📷 Webcam Test
- **Mục đích**: Test camera
- **Kiểm tra**:
  - Camera resolution (up to 1920x1080)
  - Obstruction detection
  - Image quality
- **Thời gian**: ~30 giây
- **Quan trọng**: ⭐⭐⭐

#### 🌐 Network Test
- **Mục đích**: Test kết nối mạng
- **Kiểm tra**:
  - Internet connectivity
  - DNS resolution
  - Network speed
  - WiFi info
  - Ping test
- **Thời gian**: ~30 giây
- **Quan trọng**: ⭐⭐⭐⭐

### 6. Stress Tests (Expert Mode)

#### 🔥 CPU Stress Test
- **Mục đích**: Test CPU dưới tải nặng
- **Kiểm tra**:
  - CPU temperature
  - Throttling detection
  - Frequency lock detection
  - Stability under load
- **Thời gian**: 2-3 phút
- **Quan trọng**: ⭐⭐⭐⭐⭐

**Phát hiện vấn đề:**
- ⚠️ **Throttling**: CPU giảm tần số do quá nhiệt/thiếu nguồn
- 🔒 **Frequency Lock**: CPU bị khóa tần số (BIOS/Power management)
- 🔥 **Overheating**: Nhiệt độ > 95°C (Nguy hiểm!)

#### 🎮 GPU Stress Test
- **Mục đích**: Test GPU dưới tải nặng
- **Kiểm tra**:
  - FPS stability
  - Visual artifacts
  - GPU temperature
  - Performance consistency
- **Thời gian**: 1-2 phút
- **Quan trọng**: ⭐⭐⭐⭐

## 🚀 Cách Sử Dụng

### Chạy Test Đơn Lẻ

1. Mở `individual_tests.py`
2. Click vào test muốn chạy
3. Làm theo hướng dẫn trên màn hình
4. Đánh giá kết quả

### Chạy Nhiều Tests

Bạn có thể mở nhiều test cùng lúc trong các cửa sổ riêng biệt.

### Lưu Kết Quả

Kết quả được lưu tự động trong `all_results` dictionary và in ra console.

## 📊 Benchmark Ổ Cứng Chi Tiết

### Cách Hoạt Động

1. **Tạo file test**: 512MB file ngẫu nhiên
2. **Sequential Write**: Ghi tuần tự với chunk 4MB
3. **Flush cache**: Đảm bảo dữ liệu ghi xuống đĩa
4. **Sequential Read**: Đọc tuần tự với chunk 4MB
5. **Cleanup**: Xóa file test

### Real-time Monitoring

- Biểu đồ tốc độ ghi (Write Speed)
- Biểu đồ tốc độ đọc (Read Speed)
- Progress bar với % hoàn thành
- Current speed và Average speed

### Phân Tích Kết Quả

Benchmark tự động phân tích và đưa ra:
- **Loại ổ cứng**: NVMe SSD / SATA SSD / HDD
- **Đánh giá hiệu năng**: Xuất sắc / Tốt / Trung bình / Chậm
- **Khuyến nghị sử dụng**: Gaming / Workstation / Office / Basic
- **Thời gian boot Windows**: Ước tính

## ⚠️ Lưu Ý Quan Trọng

### Disk Benchmark
- ⚠️ Cần ít nhất **600MB dung lượng trống**
- ⚠️ Đóng các ứng dụng khác để kết quả chính xác
- ⚠️ Không ngắt điện trong khi test
- ⚠️ SSD có thể chậm hơn khi gần đầy

### CPU/GPU Stress Tests
- ⚠️ Laptop sẽ nóng lên, đảm bảo tản nhiệt tốt
- ⚠️ Cắm sạc khi chạy stress test
- ⚠️ Dừng ngay nếu nhiệt độ > 100°C
- ⚠️ Không để laptop trên bề mặt mềm (chăn, gối)

### Webcam Test
- ⚠️ Cho phép quyền truy cập camera
- ⚠️ Đóng các ứng dụng khác đang dùng camera
- ⚠️ Che camera để test obstruction detection

## 🐛 Troubleshooting

### "Không tìm thấy worker_disk.py"
```bash
# Đảm bảo file worker_disk.py ở cùng thư mục
ls worker_disk.py
```

### "Không đủ dung lượng trống"
```bash
# Giải phóng dung lượng hoặc giảm file_size_mb
# Trong disk_benchmark_step.py, dòng 52:
# args=(self.queue, 60, 256),  # Giảm từ 512MB xuống 256MB
```

### "Camera không hoạt động"
```bash
# Cài đặt OpenCV
pip install opencv-python

# Kiểm tra camera
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### "Keyboard hook error"
```bash
# Chạy với quyền Administrator (Windows)
# Hoặc sudo (Linux)
```

## 📝 Kết Luận

Individual Tests cho phép:
- ✅ Test nhanh từng component
- ✅ Debug vấn đề cụ thể
- ✅ Benchmark chi tiết
- ✅ So sánh hiệu năng

**Khuyến nghị**: Chạy **HDD Speed Benchmark** và **CPU Stress Test** trước khi mua laptop cũ!

---

Made with ❤️ by LaptopTester Team
