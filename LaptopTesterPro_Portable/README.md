# 💻 LaptopTester Pro - Phần mềm kiểm tra laptop toàn diện

> **Version 2.7.2** | ✅ Latest Release | 📦 Portable EXE (79.3 MB)

---

## 🎯 Quick Start

### ⚡ Fastest Way to Use:
```
1. Download: LaptopTesterPro_v2.7.2.exe
2. Run: Double-click the .exe file
3. No installation needed - fully portable!
```

**Or** [Download from Releases](../../releases) →

---

## 🌟 Tính năng chính

LaptopTester là ứng dụng kiểm tra laptop chuyên nghiệp với giao diện hiện đại, được thiết kế để giúp bạn đánh giá toàn diện một chiếc laptop cũ trước khi mua.

> ⚠️ **Lưu ý quan trọng**: Ứng dụng này được phát triển dựa trên AI nên có thể có sai sót. Khuyến khích kiểm tra thêm bằng các ứng dụng chuyên dụng được cung cấp trong phần hướng dẫn để đảm bảo độ chính xác cao nhất.

### ✨ Các tính năng nổi bật:

- **🎨 Giao diện hiện đại**: CustomTkinter với animation mượt mà
- **📊 Kiểm tra toàn diện**: 15+ bước kiểm tra từ phần cứng đến phần mềm  
- **🔄 Tự động hóa cao**: Tích hợp các tools chuyên nghiệp
- **📱 Responsive**: Giao diện thích ứng với nhiều kích thước màn hình
- **🎯 Báo cáo chi tiết**: Export kết quả dưới nhiều định dạng
- **🔧 Đa nền tảng**: Hỗ trợ Windows (tối ưu), Linux, macOS

### 🧪 Các bước kiểm tra (16 tests):

1. **� System Information** (`system_info`) - Thu thập specs chi tiết: CPU, RAM, Storage, OS
2. **🔐 License Check** (`license_check`) - Kiểm tra bản quyền Windows
3. **💿 Hard Drive Health** (`harddrive_health`) - Health check, speed test, S.M.A.R.T data
4. **🖼️ Screen Test** (`screen_test`) - Pixel test, color accuracy, brightness, dead pixels
5. **⌨️ Keyboard Test** (`keyboard_test`) - Key mapping, response time test
6. **🔍 Physical Inspection** (`physical_inspection`) - Kiểm tra vật lý ngoài bộ vỏ
7. **🖥️ BIOS Check** (`bios_check`) - BIOS version, settings, TPM status
8. **⚙️ CPU Stress Test** (`cpu_stress`) - Stability under max load, temperature monitoring
9. **🎮 GPU Stress Test** (`gpu_stress`) - Graphics performance, memory test
10. **🔋 Battery Health** (`battery_health`) - Capacity, health status, charge cycles
11. **🔊 Audio Test** (`audio_test`) - Speaker test, microphone recording/playback
12. **📷 Webcam Test** (`webcam_test`) - Camera functionality, preview test
13. **🌐 Network Test** (`network_test`) - WiFi/Ethernet speed, connectivity test
14. **🌡️ Thermal Monitor** (`thermal_monitor`) - Real-time temperature monitoring
15. **⚡ System Stability** (`system_stability`) - Combined stress test (CPU+GPU+Memory)
16. **🔑 Hardware Fingerprint** (`hardware_fingerprint`) - Unique system identifier

## 🛠️ Cài đặt

### 📌 Version 2.7.2 - What's New

**Latest Release (Oct 17, 2025)**

✅ **Major Fixes:**
- ✨ **All 16 Test Results Now Recorded** - Fixed report missing details from 14 steps
- 🔐 **License Check Display Fixed** - Correct values displayed in report
- 📦 **Portable Build Ready** - No Python installation needed
- 🖼️ **Assets Included** - Logo and audio files in standalone executable
- ⚡ **Improved Scroll Navigation** - Better jump button detection

**Technical:** step_key constant architecture implemented for translation-safe storage

[Full Changelog](CHANGELOG.md) | [Release Notes](../../releases/tag/v2.7.2)

---

## 🛠️ Installation & Setup

### 📦 Option 1: Portable Executable (Recommended)

**No installation needed!**

```
1. Download: LaptopTesterPro_v2.7.2.exe (79.3 MB)
2. Run: Double-click to launch
3. Done! Works on Windows 10/11
```

✅ Pros:
- No Python/dependencies installation
- Single executable file
- Instant launch

### � Option 2: Run from Source (Developers)

**Requires Python 3.12.9+**

```bash
# 1. Clone repository
git clone https://github.com/your-username/LaptopTester.git
cd LaptopTester

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python main_enhanced_auto.py
```

✅ Pros:
- Source code accessible
- Easy to debug and modify
- Cross-platform (Windows/Linux/macOS)

### � Option 3: Build Your Own Executable

```bash
# Install PyInstaller
pip install pyinstaller==6.15.0

# Build portable executable
python build_simple_fast.py

# Output: LaptopTesterPro_Portable/LaptopTesterPro_v2.7.2.exe
```

## 🚀 Sử dụng

### 🎯 Chế độ Basic (Người dùng thông thường):
1. Khởi động ứng dụng với quyền Administrator
2. Chọn **"Basic Mode"** 
3. Làm theo hướng dẫn từng bước
4. Đánh giá kết quả cuối cùng

### 🔬 Chế độ Expert (Chuyên gia):
1. Chọn **"Expert Mode"**
2. Bao gồm tất cả test nâng cao
3. Stress testing với monitoring real-time
4. Báo cáo chi tiết về performance

### 📊 Export kết quả:
- **PDF Report**: Báo cáo đầy đủ với charts
- **JSON Data**: Dữ liệu thô cho analysis
- **Text Summary**: Tóm tắt nhanh

## 🏗️ Kiến trúc

```
laptoptester/
├── 📄 laptoptester.py          # Main application
├── 🔧 worker_*.py             # Worker modules cho các test
├── 📁 assets/                 # Icons, sounds, test files  
├── 📁 bin/                    # External tools (CrystalDiskMark, etc.)
├── 📁 logs/                   # Application logs
├── 📄 requirements.txt        # Dependencies
└── 📖 README.md              # Documentation
```

### 🧩 Modules chính:

- **`BaseStepFrame`**: Abstract class cho tất cả test steps
- **`WizardFrame`**: Main navigation và flow control
- **`Theme`**: UI styling và constants
- **`AnimationHelper`**: Smooth animations và transitions
- **`NotificationToast`**: User feedback system
- **`Worker modules`**: Background processing cho heavy tests

## 🔍 Chi tiết kỹ thuật

### 🎨 UI/UX Features:
- **Smooth Animations**: Fade in/out, slide transitions
- **Progress Indicators**: Real-time progress với visual feedback
- **Toast Notifications**: Non-intrusive user alerts
- **Responsive Design**: Thích ứng với resolution khác nhau
- **Dark/Light Theme**: Automatic system detection

### ⚡ Performance Optimizations:
- **Async Processing**: Multi-threading cho heavy operations
- **Caching**: Step results caching để navigation nhanh
- **Memory Management**: Proper cleanup và resource handling
- **Error Recovery**: Robust error handling với user-friendly messages

### 🔧 External Tools Integration:
- **CrystalDiskMark**: Professional disk benchmarking
- **LibreHardwareMonitor**: Real-time hardware monitoring
- **PowerCFG**: Windows battery reporting
- **Eizo Monitor Test**: Professional display testing

## 🤝 Contributing

### 🐛 Bug Reports:
1. Tạo issue với detailed description
2. Include logs từ `logs/` folder
3. Specify OS, Python version, hardware specs

### ✨ Feature Requests:
1. Mô tả feature chi tiết
2. Explain use case và benefits
3. Suggest implementation approach

### 💻 Code Contributions:
```bash
# 1. Fork repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes với proper testing
# 4. Follow coding standards:
black laptoptester.py  # Format code
flake8 laptoptester.py # Lint check

# 5. Commit với descriptive message
git commit -m "Add: Amazing new feature for CPU testing"

# 6. Push và create Pull Request
```

## 📄 License

Copyright © 2024 LaptopTester Team. All rights reserved.

**Commercial License** - Liên hệ để licensing cho commercial use.

## 🆘 Support

### 📚 Documentation:
- [Wiki](wiki/): Detailed guides và tutorials
- [API Docs](docs/): Developer documentation  
- [FAQ](FAQ.md): Câu hỏi thường gặp

### 💬 Community:
- **Issues**: GitHub Issues cho bug reports
- **Discussions**: GitHub Discussions cho Q&A
- **Email**: support@laptoptester.com

### 🔧 Troubleshooting:
| Vấn đề | Giải pháp |
|--------|-----------|
| Import errors | Cài đặt lại requirements.txt |
| Permission denied | Chạy với Administrator |
| Worker timeouts | Tăng timeout trong settings |
| UI not responsive | Update CustomTkinter |

## 🗺️ Roadmap

### 🎯 Version 2.0 (Coming Soon):
- [ ] **Cloud Sync**: Backup results to cloud
- [ ] **Mobile Companion**: Android/iOS app
- [ ] **AI Analysis**: Machine learning cho result analysis
- [ ] **Multi-language**: Internationalization support
- [ ] **Plugin System**: Extensible architecture
- [ ] **Web Interface**: Browser-based version

### 🔮 Long-term:
- Advanced GPU testing với ML workloads
- Network performance testing
- SSD wear leveling analysis  
- Predictive failure analysis
- Integration với hardware databases

## 🙏 Acknowledgments

- **CustomTkinter**: Modern UI framework
- **PSUtil**: System monitoring capabilities  
- **OpenCV**: Computer vision processing
- **Community Contributors**: Testing và feedback

---

**⭐ Nếu project này hữu ích, hãy star repository để support development!**

Made with ❤️ by LaptopTester Team