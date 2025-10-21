# 🚀 Hướng Dẫn Khởi Động Nhanh - LaptopTester Pro v2.0

## ⚡ Cách Nhanh Nhất (Windows)

### Bước 1: Cài đặt Python
- Tải Python 3.8+ từ [python.org](https://www.python.org/downloads/)
- ✅ Chọn "Add Python to PATH" khi cài đặt

### Bước 2: Chạy ứng dụng
```bash
# Cách 1: Double-click file
run.bat

# Cách 2: Từ Command Prompt
cd c:\MyApps\LaptopTester
run.bat
```

Script `run.bat` sẽ tự động:
- ✅ Kiểm tra Python
- ✅ Tạo virtual environment
- ✅ Cài đặt dependencies
- ✅ Khởi động ứng dụng

## 📋 Yêu Cầu Hệ Thống

| Thành phần | Yêu cầu |
|------------|---------|
| **OS** | Windows 10/11 (khuyến nghị) |
| **Python** | 3.8 hoặc mới hơn |
| **RAM** | 4GB+ |
| **Ổ cứng** | 500MB trống |
| **Quyền** | Administrator (cho một số test) |

## 🎯 Chế Độ Sử Dụng

### 🟢 Basic Mode (Người dùng thông thường)
- Kiểm tra cơ bản: Thông tin hệ thống, ổ cứng, màn hình, bàn phím, pin, audio, camera
- Thời gian: ~15-20 phút
- Không cần kiến thức kỹ thuật

### 🔴 Expert Mode (Chuyên gia)
- Bao gồm tất cả test trong Basic Mode
- Thêm: CPU stress test, GPU benchmark, Memory test, Thermal monitoring
- Thời gian: ~30-45 phút
- Yêu cầu: Hiểu biết về hardware

## 🔧 Xử Lý Sự Cố

### ❌ Lỗi: "Python not found"
**Giải pháp:**
```bash
# Kiểm tra Python đã cài đặt
python --version

# Nếu chưa có, tải từ python.org
```

### ❌ Lỗi: "Failed to install dependencies"
**Giải pháp:**
```bash
# Cài thủ công
pip install -r requirements.txt

# Hoặc cài từng package
pip install customtkinter psutil pillow opencv-python
```

### ❌ Lỗi: "Permission denied"
**Giải pháp:**
- Chạy Command Prompt với quyền Administrator
- Click phải `run.bat` → "Run as administrator"

### ❌ Lỗi: "Import error"
**Giải pháp:**
```bash
# Cài lại dependencies
pip install --upgrade -r requirements.txt
```

## 📊 Các Bước Kiểm Tra

### Basic Mode (9 bước):
1. ✅ **Thông tin hệ thống** - CPU, RAM, OS
2. ✅ **License Windows** - Kiểm tra bản quyền
3. ✅ **Ổ cứng** - Health check, SMART status
4. ✅ **Màn hình** - Dead pixel, color test
5. ✅ **Bàn phím & Touchpad** - Key test, click test
6. ✅ **Pin** - Capacity, health, cycles
7. ✅ **Audio** - Speaker, microphone
8. ✅ **Camera** - Webcam test
9. ✅ **Tóm tắt** - Báo cáo kết quả

### Expert Mode (thêm 5 bước):
10. ✅ **CPU Stress Test** - Stability test
11. ✅ **GPU Performance** - Graphics benchmark
12. ✅ **Tốc độ ổ cứng** - Read/Write speed
13. ✅ **Mạng** - WiFi, Ethernet test
14. ✅ **Nhiệt độ** - Thermal monitoring

## 💾 Export Kết Quả

Sau khi hoàn thành, bạn có thể export kết quả:
- **PDF Report** - Báo cáo đầy đủ với biểu đồ
- **JSON Data** - Dữ liệu thô để phân tích
- **Text Summary** - Tóm tắt nhanh

## 🆘 Hỗ Trợ

### 📚 Tài liệu:
- [README.md](README.md) - Hướng dẫn đầy đủ
- [USER_GUIDE.md](USER_GUIDE.md) - Hướng dẫn chi tiết
- [FAQ](README.md#troubleshooting) - Câu hỏi thường gặp

### 💬 Liên hệ:
- **Email**: support@laptoptester.com
- **GitHub Issues**: Báo cáo lỗi
- **GitHub Discussions**: Hỏi đáp

## ⚠️ Lưu Ý Quan Trọng

> **Ứng dụng này được phát triển dựa trên AI nên có thể có sai sót.**
> 
> Khuyến khích kiểm tra thêm bằng các ứng dụng chuyên dụng:
> - **CrystalDiskInfo** - Kiểm tra ổ cứng
> - **HWiNFO** - Thông tin hardware
> - **AIDA64** - Benchmark toàn diện
> - **MemTest86** - Kiểm tra RAM

## 🎉 Sẵn Sàng!

Bây giờ bạn đã sẵn sàng sử dụng LaptopTester Pro v2.0!

```bash
# Chạy ngay
run.bat
```

---

Made with ❤️ by LaptopTester Team
