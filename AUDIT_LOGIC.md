# RÀ SOÁT LOGIC TÍNH TOÁN CÁC BƯỚC TEST

## ✅ 1. BATTERY HEALTH (Pin) - ĐÃ FIX
**Trước**: Dùng WMI không chính xác, fallback về giá trị giả (50 Wh, 85%, 150 cycles)
**Sau**: 
- Chạy `powercfg /batteryreport` để lấy dữ liệu chính thức từ Windows
- Parse HTML với encoding UTF-8 và DOTALL flag
- Lấy chính xác: Design Capacity, Full Charge Capacity, Cycle Count
- Tính Battery Health = (Full / Design) * 100%
**Kết quả**: 45.03 Wh, 33.6 Wh, 74.6%, 279 cycles ✓

## ✅ 2. HARDWARE FINGERPRINT (Định danh phần cứng) - CẦN KIỂM TRA
**Logic hiện tại**: Dùng `wmic` và `systeminfo`
```python
wmic cpu get name,numberofcores,maxclockspeed
wmic memorychip get capacity,speed
wmic diskdrive get model,size
wmic path win32_videocontroller get name
systeminfo | findstr /C:"System Model"
```
**Đánh giá**: ✓ Chính xác, lấy từ Windows Management Instrumentation

## ⚠️ 3. LICENSE CHECK (Kiểm tra bản quyền) - CẦN KIỂM TRA
**Logic hiện tại**: Dùng `slmgr /dli` và `slmgr /xpr`
**Vấn đề tiềm ẩn**: Cần quyền Administrator
**Đề xuất**: Thêm fallback nếu không có quyền admin

## ✅ 4. SYSTEM INFO (Thông tin hệ thống) - CHÍNH XÁC
**Logic**: Dùng `psutil` và `platform`
- CPU: `psutil.cpu_count()`, `psutil.cpu_freq()`
- RAM: `psutil.virtual_memory()`
- Disk: `psutil.disk_usage()`
- OS: `platform.system()`, `platform.release()`
**Đánh giá**: ✓ Thư viện chuẩn, chính xác

## ⚠️ 5. HARD DRIVE HEALTH - CẦN KIỂM TRA SMART
**Logic hiện tại**: Chỉ dùng `psutil.disk_usage()` và `psutil.disk_io_counters()`
**Vấn đề**: Không đọc SMART data (health, temperature, reallocated sectors)
**Đề xuất**: Thêm `smartctl` hoặc `wmic diskdrive get status`

## ✅ 6. CPU STRESS TEST - CHÍNH XÁC
**Logic**: 
- Chạy multiprocessing với tính toán số nguyên tố
- Monitor CPU usage, temperature, frequency
- Dùng `psutil.cpu_percent()`, `psutil.sensors_temperatures()`
**Đánh giá**: ✓ Stress test thực sự, không giả lập

## ⚠️ 7. GPU STRESS TEST - CẦN KIỂM TRA
**Logic hiện tại**: Dùng OpenGL rendering
**Vấn đề**: Không lấy được GPU temperature, usage chính xác
**Đề xuất**: Dùng `nvidia-smi` cho NVIDIA, `radeontop` cho AMD

## ⚠️ 8. HARD DRIVE SPEED - CẦN KIỂM TRA
**Logic hiện tại**: Tự viết benchmark (write/read file)
**Vấn đề**: Không chính xác như CrystalDiskMark
**Đề xuất**: Tích hợp CrystalDiskMark CLI nếu có

## ✅ 9. SCREEN TEST - CHÍNH XÁC
**Logic**: Hiển thị màu fullscreen, user tự đánh giá
**Đánh giá**: ✓ Phù hợp, không cần tính toán

## ✅ 10. KEYBOARD TEST - CHÍNH XÁC
**Logic**: Dùng `keyboard` library để detect key press
**Đánh giá**: ✓ Chính xác, real-time detection

## ⚠️ 11. AUDIO TEST - CẦN KIỂM TRA
**Logic hiện tại**: Generate tone bằng numpy/scipy
**Vấn đề**: Không test microphone thực sự (chỉ mock)
**Đề xuất**: Dùng `sounddevice` để record và analyze

## ⚠️ 12. WEBCAM TEST - CẦN KIỂM TRA
**Logic hiện tại**: Dùng OpenCV `cv2.VideoCapture()`
**Vấn đề**: Obstruction detection có thể không chính xác
**Đánh giá**: ✓ Cơ bản OK, có thể cải thiện detection

## ⚠️ 13. NETWORK TEST - CẦN KIỂM TRA
**Logic hiện tại**: 
- Ping google.com
- DNS lookup
- Speed test (download file)
- WiFi info từ `pywifi`
**Vấn đề**: Speed test không chính xác như Speedtest.net
**Đề xuất**: Dùng `speedtest-cli` library

## ⚠️ 14. THERMAL MONITOR - CẦN KIỂM TRA
**Logic hiện tại**: Dùng `psutil.sensors_temperatures()`
**Vấn đề**: Trên Windows thường không có sensors
**Đề xuất**: Dùng LibreHardwareMonitor hoặc OpenHardwareMonitor

## ✅ 15. SYSTEM STABILITY - CHÍNH XÁC
**Logic**: Combined stress test (CPU + GPU + Disk)
**Đánh giá**: ✓ Stress test thực sự

---

## TỔNG KẾT CẦN FIX:

### 🔴 CRITICAL (Ảnh hưởng lớn):
1. **Hard Drive Health**: Thêm SMART data reading
2. **GPU Stress Test**: Lấy GPU temp/usage chính xác
3. **Thermal Monitor**: Fix temperature reading trên Windows

### 🟡 MEDIUM (Cải thiện):
4. **Hard Drive Speed**: Tích hợp CrystalDiskMark
5. **Network Speed**: Dùng speedtest-cli
6. **Audio Test**: Test microphone thực sự

### 🟢 LOW (Optional):
7. **License Check**: Thêm fallback cho non-admin
8. **Webcam**: Cải thiện obstruction detection
