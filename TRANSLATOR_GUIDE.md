# 🌐 Hướng Dẫn Sử Dụng Auto Translator

## 📋 Tổng Quan

Module `translator.py` cung cấp tính năng dịch tự động Anh-Việt cho ứng dụng LaptopTester. Module này:

- ✅ Dịch tự động các thuật ngữ kỹ thuật
- ✅ Hỗ trợ dịch chuỗi, dictionary, list
- ✅ Tích hợp sẵn 200+ thuật ngữ phổ biến
- ✅ Có thể mở rộng với thuật ngữ tùy chỉnh
- ✅ Nhẹ, nhanh, không cần internet

## 🚀 Cài Đặt

### Bước 1: Copy file vào project

```bash
# File translator.py đã có sẵn trong thư mục LaptopTester
```

### Bước 2: Import vào code

```python
from translator import translate, translate_dict, get_translator
```

## 💡 Cách Sử Dụng

### 1. Dịch Chuỗi Đơn Giản

```python
from translator import translate

# Dịch chuỗi
text = "CPU Test is running"
translated = translate(text)
print(translated)  # Output: "CPU Kiểm tra đang chạy"

# Dịch thuật ngữ
term = "Battery Health"
translated = translate(term)
print(translated)  # Output: "Pin Sức khỏe"
```

### 2. Dịch Dictionary

```python
from translator import translate_dict

# Dịch toàn bộ dictionary
data = {
    "CPU": "Intel Core i7",
    "Status": "Running",
    "Result": "Good"
}

translated = translate_dict(data)
print(translated)
# Output: {
#     "CPU": "Intel Core i7",
#     "Trạng thái": "Đang chạy",
#     "Kết quả": "Tốt"
# }
```

### 3. Dịch Kết Quả Test

```python
from translator import translate_dict

# Kết quả từ test step
test_result = {
    "Result": "Pass",
    "Status": "Good",
    "Temperature": "65°C",
    "Performance": "Excellent"
}

# Dịch sang tiếng Việt
translated_result = translate_dict(test_result)
# Output: {
#     "Kết quả": "Đạt",
#     "Trạng thái": "Tốt",
#     "Nhiệt độ": "65°C",
#     "Hiệu năng": "Xuất sắc"
# }
```

### 4. Thêm Thuật Ngữ Tùy Chỉnh

```python
from translator import get_translator

translator = get_translator()

# Thêm thuật ngữ mới
translator.add_term("Throttling", "Giảm hiệu năng")
translator.add_term("Bottleneck", "Nút thắt")
translator.add_term("Overclocking", "Ép xung")

# Sử dụng
text = "CPU Throttling detected"
translated = translator.translate(text)
print(translated)  # Output: "CPU Giảm hiệu năng detected"
```

### 5. Thêm Mẫu Câu

```python
from translator import get_translator

translator = get_translator()

# Thêm mẫu câu
translator.add_pattern("is overheating", "đang quá nhiệt")
translator.add_pattern("needs replacement", "cần thay thế")

# Sử dụng
text = "Battery is overheating"
translated = translator.translate(text)
print(translated)  # Output: "Pin đang quá nhiệt"
```

## 🔧 Tích Hợp Vào LaptopTester

### Tích Hợp Vào BaseStepFrame

```python
from translator import translate, translate_dict

class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        # Dịch title và text
        title_vi = translate(title)
        why_text_vi = translate(why_text)
        how_text_vi = translate(how_text)
        
        super().__init__(master, fg_color="transparent")
        # ... rest of code
```

### Tích Hợp Vào mark_completed

```python
def mark_completed(self, result_data, auto_advance=False):
    self._completed = True
    self._skipped = False
    
    # Dịch kết quả sang tiếng Việt
    result_data_vi = translate_dict(result_data)
    
    if self.record_result:
        self.record_result(self.title, result_data_vi)
    
    if auto_advance and self.go_to_next_step_callback:
        self.go_to_next_step_callback()
```

### Tích Hợp Vào SummaryStep

```python
def display_summary(self, results):
    # Dịch toàn bộ kết quả
    results_vi = translate_dict(results)
    
    # Hiển thị kết quả đã dịch
    for step_name, result_data in results_vi.items():
        self._create_result_item(step_name, result_data)
```

### Tích Hợp Vào LanguageManager

```python
class LanguageManager:
    def __init__(self):
        self.current_language = "vi"
        self.translator = get_translator()
    
    def get_text(self, key):
        # Nếu không có trong translations, dùng translator
        if key not in self.translations[self.current_language]:
            return self.translator.translate(key)
        return self.translations[self.current_language][key]
```

## 📊 Từ Điển Tích Hợp Sẵn

### Phần Cứng (Hardware)
- CPU, Processor, Core, Thread
- GPU, Graphics, Video Card
- RAM, Memory, Storage
- Hard Drive, SSD, HDD
- Battery, Power, Adapter
- Display, Screen, Monitor
- Keyboard, Touchpad, Mouse
- Speaker, Audio, Microphone
- Webcam, Camera
- WiFi, Bluetooth, Network

### Trạng Thái (Status)
- Good, Bad, Excellent, Poor
- Pass, Fail, Warning
- OK, Error, Success
- Running, Completed, Ready
- Pending, Skipped

### Hành Động (Actions)
- Start, Stop, Pause
- Continue, Skip, Next
- Previous, Back, Exit
- Save, Export, Import
- Cancel, Confirm, Close

### Đơn Vị (Units)
- GB, MB, KB, TB
- GHz, MHz
- °C, °F
- %, ms, seconds, minutes

## 🎯 Ví Dụ Thực Tế

### Ví Dụ 1: Dịch Thông Tin Phần Cứng

```python
from translator import translate_dict

hardware_info = {
    "Model Laptop": "Dell XPS 15",
    "CPU": "Intel Core i7-11800H",
    "GPU": "NVIDIA GeForce RTX 3050 Ti",
    "RAM": "16GB DDR4",
    "Storage": "512GB NVMe SSD",
    "Battery": "Good",
    "Status": "Running"
}

translated = translate_dict(hardware_info)
# Kết quả đã dịch sang tiếng Việt
```

### Ví Dụ 2: Dịch Kết Quả Test

```python
from translator import translate_dict

test_results = {
    "CPU Test": {"Status": "Pass", "Result": "Good"},
    "GPU Test": {"Status": "Pass", "Result": "Excellent"},
    "Battery Test": {"Status": "Warning", "Result": "Fair"}
}

translated = translate_dict(test_results)
# Tất cả keys và values đều được dịch
```

### Ví Dụ 3: Dịch Thông Báo

```python
from translator import translate

messages = [
    "Test is running, please wait",
    "CPU temperature is high",
    "Battery health check completed",
    "Network connection not found"
]

for msg in messages:
    print(translate(msg))
```

## 🔍 Test Module

Chạy file test để xem demo:

```bash
python test_translator.py
```

Output sẽ hiển thị:
- ✅ Test dịch cơ bản
- ✅ Test dịch câu
- ✅ Test dịch dictionary
- ✅ Test thông tin phần cứng
- ✅ Test kết quả test
- ✅ Test thuật ngữ tùy chỉnh
- ✅ Demo tích hợp

## 📝 Lưu Ý

### Ưu Điểm
- ✅ Không cần internet
- ✅ Nhanh, nhẹ
- ✅ Dễ tích hợp
- ✅ Có thể mở rộng
- ✅ Hỗ trợ nested dictionary

### Hạn Chế
- ⚠️ Chỉ dịch từ điển có sẵn
- ⚠️ Không dịch ngữ cảnh phức tạp
- ⚠️ Cần thêm thuật ngữ mới thủ công

### Khi Nào Nên Dùng
- ✅ Dịch thuật ngữ kỹ thuật
- ✅ Dịch status, result
- ✅ Dịch UI labels
- ✅ Dịch thông báo đơn giản

### Khi Nào Không Nên Dùng
- ❌ Dịch văn bản dài
- ❌ Dịch tài liệu phức tạp
- ❌ Cần dịch chính xác 100%

## 🚀 Nâng Cao

### Tích Hợp API Dịch Online (Tùy Chọn)

Nếu cần dịch chính xác hơn, có thể tích hợp Google Translate API:

```python
from translator import AutoTranslator
from googletrans import Translator

class EnhancedTranslator(AutoTranslator):
    def __init__(self):
        super().__init__()
        self.online_translator = Translator()
    
    def translate(self, text):
        # Thử dịch offline trước
        result = super().translate(text)
        
        # Nếu không thay đổi, dùng online
        if result == text:
            try:
                result = self.online_translator.translate(text, dest='vi').text
            except:
                pass
        
        return result
```

## 📞 Hỗ Trợ

Nếu cần thêm thuật ngữ hoặc có vấn đề, vui lòng:
1. Mở file `translator.py`
2. Thêm vào `self.dictionary` hoặc `self.patterns`
3. Test lại với `test_translator.py`

## 📄 License

Module này là một phần của LaptopTester Pro.
Copyright © 2024 LaptopTester Team.
