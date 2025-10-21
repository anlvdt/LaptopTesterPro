# 💻 LaptopTester - Comprehensive Laptop Testing Software

## 🌟 Main Features

LaptopTester is a professional laptop testing application with modern interface, designed to help you comprehensively evaluate an old laptop before purchasing.

### ✨ Outstanding Features:

- **🎨 Modern Interface**: CustomTkinter with smooth animations
- **📊 Comprehensive Testing**: 15+ testing steps from hardware to software  
- **🔄 High Automation**: Integration with professional tools
- **📱 Responsive**: Interface adapts to multiple screen sizes
- **🎯 Detailed Reports**: Export results in multiple formats
- **🔧 Cross-platform**: Supports Windows (optimized), Linux, macOS

### 🧪 Testing Steps:

#### 📋 Basic Testing:
1. **System Information** - Collect detailed specs
2. **Windows License** - Check OS and software licensing
3. **Hard Drive** - Health check, speed test, benchmark
4. **Display** - Pixel test, color accuracy, brightness
5. **Keyboard** - Key mapping, responsiveness
6. **Ports** - USB, HDMI, audio, network
7. **Battery** - Capacity, health, charge cycles
8. **Audio** - Speaker, microphone quality
9. **Camera** - Webcam functionality test

#### ⚡ Advanced Testing (Expert mode):
- **CPU Stress Test** - Stability under maximum load
- **GPU Performance** - Graphics benchmarking  
- **Memory Test** - RAM stress testing
- **Thermal Management** - Temperature monitoring
- **System Stability** - Combined stress tests

## 🛠️ Installation

### System Requirements:
- **OS**: Windows 10/11 (recommended), Linux, macOS
- **Python**: 3.8+ 
- **RAM**: 4GB+ 
- **Storage**: 500MB+ free space
- **Permissions**: Administrator (Windows) for some features

### 📦 Quick Installation:

```bash
# 1. Clone repository
git clone https://github.com/your-username/laptoptester.git
cd laptoptester

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python laptoptester.py
```

### 🔧 Manual Step-by-step Installation:

```bash
# Core libraries
pip install customtkinter>=5.2.0 psutil>=5.9.0

# Media processing  
pip install pillow opencv-python pygame sounddevice scipy

# System utilities
pip install beautifulsoup4 requests numpy py-cpuinfo keyboard

# Windows specific (Windows only)
pip install wmi pywifi pywin32
```

## 🚀 Usage

### 🎯 Basic Mode (Regular Users):
1. Launch application with Administrator privileges
2. Select **"Basic Mode"** 
3. Follow step-by-step instructions
4. Evaluate final results

### 🔬 Expert Mode (Professionals):
1. Select **"Expert Mode"**
2. Includes all advanced tests
3. Stress testing with real-time monitoring
4. Detailed performance reports

### 📊 Export Results:
- **PDF Report**: Complete report with charts
- **JSON Data**: Raw data for analysis
- **Text Summary**: Quick summary

## 🏗️ Architecture

```
laptoptester/
├── 📄 laptoptester.py          # Main application
├── 🔧 worker_*.py             # Worker modules for tests
├── 📁 assets/                 # Icons, sounds, test files  
├── 📁 bin/                    # External tools (CrystalDiskMark, etc.)
├── 📁 logs/                   # Application logs
├── 📄 requirements.txt        # Dependencies
└── 📖 README.md              # Documentation
```

### 🧩 Main Modules:

- **`BaseStepFrame`**: Abstract class for all test steps
- **`WizardFrame`**: Main navigation and flow control
- **`Theme`**: UI styling and constants
- **`AnimationHelper`**: Smooth animations and transitions
- **`NotificationToast`**: User feedback system
- **`Worker modules`**: Background processing for heavy tests

## 🔍 Technical Details

### 🎨 UI/UX Features:
- **Smooth Animations**: Fade in/out, slide transitions
- **Progress Indicators**: Real-time progress with visual feedback
- **Toast Notifications**: Non-intrusive user alerts
- **Responsive Design**: Adapts to different resolutions
- **Dark/Light Theme**: Automatic system detection

### ⚡ Performance Optimizations:
- **Async Processing**: Multi-threading for heavy operations
- **Caching**: Step results caching for fast navigation
- **Memory Management**: Proper cleanup and resource handling
- **Error Recovery**: Robust error handling with user-friendly messages

### 🔧 External Tools Integration:
- **CrystalDiskMark**: Professional disk benchmarking
- **LibreHardwareMonitor**: Real-time hardware monitoring
- **PowerCFG**: Windows battery reporting
- **Eizo Monitor Test**: Professional display testing

## 🤝 Contributing

### 🐛 Bug Reports:
1. Create issue with detailed description
2. Include logs from `logs/` folder
3. Specify OS, Python version, hardware specs

### ✨ Feature Requests:
1. Describe feature in detail
2. Explain use case and benefits
3. Suggest implementation approach

### 💻 Code Contributions:
```bash
# 1. Fork repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes with proper testing
# 4. Follow coding standards:
black laptoptester.py  # Format code
flake8 laptoptester.py # Lint check

# 5. Commit with descriptive message
git commit -m "Add: Amazing new feature for CPU testing"

# 6. Push and create Pull Request
```

## 📄 License

Copyright © 2024 LaptopTester Team. All rights reserved.

**Commercial License** - Contact for licensing for commercial use.

## 🆘 Support

### 📚 Documentation:
- [Wiki](wiki/): Detailed guides and tutorials
- [API Docs](docs/): Developer documentation  
- [FAQ](FAQ.md): Frequently asked questions

### 💬 Community:
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for Q&A
- **Email**: support@laptoptester.com

### 🔧 Troubleshooting:
| Issue | Solution |
|-------|----------|
| Import errors | Reinstall requirements.txt |
| Permission denied | Run with Administrator |
| Worker timeouts | Increase timeout in settings |
| UI not responsive | Update CustomTkinter |

## 🗺️ Roadmap

### 🎯 Version 2.0 (Coming Soon):
- [ ] **Cloud Sync**: Backup results to cloud
- [ ] **Mobile Companion**: Android/iOS app
- [ ] **AI Analysis**: Machine learning for result analysis
- [ ] **Multi-language**: Internationalization support
- [ ] **Plugin System**: Extensible architecture
- [ ] **Web Interface**: Browser-based version

### 🔮 Long-term:
- Advanced GPU testing with ML workloads
- Network performance testing
- SSD wear leveling analysis  
- Predictive failure analysis
- Integration with hardware databases

## 🙏 Acknowledgments

- **CustomTkinter**: Modern UI framework
- **PSUtil**: System monitoring capabilities  
- **OpenCV**: Computer vision processing
- **Community Contributors**: Testing and feedback

---

**⭐ If this project is useful, please star the repository to support development!**

Made with ❤️ by LaptopTester Team