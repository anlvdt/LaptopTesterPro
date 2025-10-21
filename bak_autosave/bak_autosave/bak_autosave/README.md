# 💻 LaptopTester - Phần mềm kiểm tra laptop toàn diện

## 🌟 Tính năng chính

LaptopTester là ứng dụng kiểm tra laptop chuyên nghiệp với giao diện hiện đại, được thiết kế để giúp bạn đánh giá toàn diện một chiếc laptop cũ trước khi mua.

### ✨ Các tính năng nổi bật:

- **🎨 Giao diện hiện đại**: CustomTkinter với animation mượt mà
- **📊 Kiểm tra toàn diện**: 15+ bước kiểm tra từ phần cứng đến phần mềm  
- **🔄 Tự động hóa cao**: Tích hợp các tools chuyên nghiệp
- **📱 Responsive**: Giao diện thích ứng với nhiều kích thước màn hình
- **🎯 Báo cáo chi tiết**: Export kết quả dưới nhiều định dạng
- **🔧 Đa nền tảng**: Hỗ trợ Windows (tối ưu), Linux, macOS

### 🧪 Các bước kiểm tra:

#### 📋 Kiểm tra cơ bản:
1. **Thông tin hệ thống** - Thu thập specs chi tiết
2. **License Windows** - Kiểm tra bản quyền OS và phần mềm
3. **Ổ cứng** - Health check, speed test, benchmark
4. **Màn hình** - Pixel test, color accuracy, brightness
5. **Bàn phím** - Key mapping, responsiveness
6. **Cổng kết nối** - USB, HDMI, audio, network
7. **Pin** - Capacity, health, charge cycles
8. **Audio** - Speaker, microphone quality
9. **Camera** - Webcam functionality test

#### ⚡ Kiểm tra nâng cao (Expert mode):
- **CPU Stress Test** - Stability under maximum load
- **GPU Performance** - Graphics benchmarking  
- **Memory Test** - RAM stress testing
- **Thermal Management** - Temperature monitoring
- **System Stability** - Combined stress tests

## 🛠️ Cài đặt

### Yêu cầu hệ thống:
- **OS**: Windows 10/11 (khuyến nghị), Linux, macOS
- **Python**: 3.8+ 
- **RAM**: 4GB+ 
- **Storage**: 500MB+ free space
- **Quyền**: Administrator (Windows) cho một số tính năng

### 📦 Cài đặt nhanh:

```bash
# 1. Clone repository
git clone https://github.com/your-username/laptoptester.git
cd laptoptester

# 2. Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate     # Windows

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Chạy ứng dụng
python laptoptester.py
```

### 🔧 Cài đặt thủ công từng bước:

```bash
# Core libraries
pip install customtkinter>=5.2.0 psutil>=5.9.0

# Media processing  
pip install pillow opencv-python pygame sounddevice scipy

# System utilities
pip install beautifulsoup4 requests numpy py-cpuinfo keyboard

# Windows specific (chỉ trên Windows)
pip install wmi pywifi pywin32
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