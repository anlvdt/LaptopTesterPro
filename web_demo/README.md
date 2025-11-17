# LaptopTester Pro - Web Demo

## Tổng quan

Đây là phiên bản demo web responsive của LaptopTester Pro, được thiết kế đặc biệt để tối ưu cho màn hình nhỏ và ưu tiên không gian cho các chức năng test.

## ✨ Tính năng chính

### 📱 Responsive Design
- **Desktop (>768px):** Layout 2 cột với sidebar
- **Tablet (<=768px):** Layout 1 cột, sidebar chuyển xuống
- **Mobile (<=480px):** Layout compact với FAB

### 🎯 Compact Mode
- Ẩn header và sidebar để tối đa hóa vùng test
- Floating Action Button (FAB) cho test nhanh
- Toggle bằng nút 📱 trên header

### ⚡ Optimized Test Area
- Test panel ở vị trí trung tâm
- Nút Start/Stop kích thước lớn (touch-friendly)
- Progress bar với mô tả chi tiết
- Real-time status updates

## 🔧 Cấu trúc file

```
web_demo/
├── index.html      # Main UI
├── styles.css      # Responsive CSS
├── script.js       # Interactive Logic  
├── demo.html       # Documentation
└── README.md       # This file
```

## 🚀 Cách sử dụng

### Chạy demo local
1. Mở `demo.html` để xem hướng dẫn
2. Mở `index.html` trong browser để test UI
3. Thay đổi kích thước window để test responsive

### Test responsive
- **Desktop:** Mở trong browser thường
- **Mobile:** Sử dụng DevTools (F12) > Device Toolbar
- **Tablet:** Test ở kích thước 768px
- **Compact:** Click nút 📱 để bật compact mode

## 📐 Breakpoints

```css
/* Mobile First */
Base: 320px+
Tablet: 768px+
Desktop: 1024px+
Large: 1200px+

/* Compact Mode */
Auto-enable: <480px screens
```

## 🎨 Customization

### CSS Variables
```css
:root {
    --primary-color: #0078d4;    /* Màu chính */
    --gap-sm: 8px;               /* Khoảng cách nhỏ */
    --gap-md: 16px;              /* Khoảng cách vừa */
    --border-radius: 8px;        /* Bo góc */
}
```

### Layout Modes
- **Normal:** Header + Main + Sidebar
- **Compact:** Chỉ Main area + FAB
- **Mobile:** Auto-responsive với hamburger menu

## 🔌 Integration Options

### Option 1: Electron App
```bash
npm install electron
# Wrap HTML in Electron for desktop app
```

### Option 2: Python WebView
```python
import webview
webview.create_window('LaptopTester Pro', 'web_demo/index.html')
webview.start()
```

### Option 3: Flask/FastAPI
```python
from flask import Flask, render_template
app = Flask(__name__)
# Serve HTML as web app
```

### Option 4: CEF Python
```python
from cefpython3 import cefpython as cef
# Embed web UI in Python app
```

## ⚙️ JavaScript API

```javascript
// Main class
window.laptopTester = new LaptopTesterUI();

// Methods
laptopTester.startTest();        // Bắt đầu test
laptopTester.toggleCompactMode(); // Bật/tắt compact
laptopTester.showToast(msg, type); // Hiện thông báo
```

## 📱 PWA Features

- Service Worker ready
- Responsive meta tags  
- Touch-friendly interactions
- Offline-capable structure

## 🎯 Optimization Highlights

### Ưu tiên vùng Test
1. **Test Controls:** Luôn visible và accessible
2. **Progress Feedback:** Real-time với animation
3. **Results Display:** Instant và clear
4. **Quick Actions:** FAB cho mobile users

### UI/UX Improvements
- **44px minimum touch targets**
- **Adequate spacing for touch**
- **Clear visual hierarchy**
- **Smooth animations**
- **Toast notifications**

## 🚀 Next Steps

### Phase 1: Basic Integration
1. Connect với Python backend
2. Real test execution
3. Hardware API integration

### Phase 2: Enhanced Features  
1. WebRTC cho camera test
2. Keyboard event capture
3. System info APIs
4. Report generation

### Phase 3: Advanced
1. WebAssembly cho performance tests
2. Real-time monitoring
3. Cloud backup/sync
4. Multi-language support

## 📞 Hỗ trợ

- **Email:** anlvdt@gmail.com
- **GitHub:** https://github.com/anlvdt/LaptopTesterPro.git
- **Demo:** Mở `demo.html` để xem hướng dẫn chi tiết

---

**LaptopTester Pro Web Demo** - Tối ưu cho màn hình nhỏ, ưu tiên chức năng test