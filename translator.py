#!/usr/bin/env python3
"""
Auto Translator Module - Anh-Việt
Dịch tự động các chuỗi tiếng Anh sang tiếng Việt
"""

class AutoTranslator:
    def __init__(self):
        # Từ điển dịch Anh-Việt cho các thuật ngữ phổ biến
        self.dictionary = {
            # Hardware terms
            "CPU": "CPU", "Processor": "Bộ xử lý", "Core": "Nhân", "Thread": "Luồng",
            "GPU": "GPU", "Graphics": "Đồ họa", "Video Card": "Card đồ họa",
            "RAM": "RAM", "Memory": "Bộ nhớ", "Storage": "Lưu trữ",
            "Hard Drive": "Ổ cứng", "SSD": "SSD", "HDD": "HDD",
            "Motherboard": "Bo mạch chủ", "BIOS": "BIOS", "UEFI": "UEFI",
            "Battery": "Pin", "Power": "Nguồn", "Adapter": "Sạc",
            "Display": "Màn hình", "Screen": "Màn hình", "Monitor": "Màn hình",
            "Keyboard": "Bàn phím", "Touchpad": "Touchpad", "Mouse": "Chuột",
            "Speaker": "Loa", "Audio": "Âm thanh", "Microphone": "Micro",
            "Webcam": "Webcam", "Camera": "Camera",
            "WiFi": "WiFi", "Bluetooth": "Bluetooth", "Network": "Mạng",
            "Port": "Cổng", "USB": "USB", "HDMI": "HDMI",
            
            # Status terms
            "Good": "Tốt", "Bad": "Xấu", "Excellent": "Xuất sắc", "Poor": "Kém",
            "Pass": "Đạt", "Fail": "Lỗi", "Warning": "Cảnh báo",
            "OK": "OK", "Error": "Lỗi", "Success": "Thành công",
            "Running": "Đang chạy", "Completed": "Hoàn thành", "Ready": "Sẵn sàng",
            "Pending": "Chờ xử lý", "Skipped": "Bỏ qua",
            
            # Test terms
            "Test": "Kiểm tra", "Check": "Kiểm tra", "Scan": "Quét",
            "Benchmark": "Đánh giá", "Stress Test": "Test tải nặng",
            "Performance": "Hiệu năng", "Speed": "Tốc độ",
            "Temperature": "Nhiệt độ", "Health": "Sức khỏe",
            "Status": "Trạng thái", "Result": "Kết quả",
            
            # Actions
            "Start": "Bắt đầu", "Stop": "Dừng", "Pause": "Tạm dừng",
            "Continue": "Tiếp tục", "Skip": "Bỏ qua", "Next": "Tiếp theo",
            "Previous": "Trước", "Back": "Quay lại", "Exit": "Thoát",
            "Save": "Lưu", "Export": "Xuất", "Import": "Nhập",
            "Cancel": "Hủy", "Confirm": "Xác nhận", "Close": "Đóng",
            
            # Common phrases
            "Please wait": "Vui lòng đợi", "Loading": "Đang tải",
            "Processing": "Đang xử lý", "Checking": "Đang kiểm tra",
            "Not found": "Không tìm thấy", "Not available": "Không khả dụng",
            "Not supported": "Không hỗ trợ", "Unknown": "Không rõ",
            "Yes": "Có", "No": "Không",
            
            # Units
            "GB": "GB", "MB": "MB", "KB": "KB", "TB": "TB",
            "GHz": "GHz", "MHz": "MHz",
            "°C": "°C", "°F": "°F",
            "%": "%", "ms": "ms", "seconds": "giây", "minutes": "phút",
            
            # Laptop parts
            "Laptop": "Laptop", "Notebook": "Laptop",
            "Chassis": "Vỏ máy", "Case": "Vỏ máy",
            "Hinge": "Bản lề", "Screw": "Ốc vít",
            "Fan": "Quạt tản nhiệt", "Cooling": "Làm mát",
            "Thermal Paste": "Keo tản nhiệt",
            
            # Software
            "Windows": "Windows", "License": "Bản quyền",
            "Activated": "Đã kích hoạt", "Not activated": "Chưa kích hoạt",
            "Driver": "Driver", "Software": "Phần mềm",
            "Operating System": "Hệ điều hành", "OS": "HĐH",
            
            # Brands (keep original)
            "Intel": "Intel", "AMD": "AMD", "NVIDIA": "NVIDIA",
            "Dell": "Dell", "HP": "HP", "Lenovo": "Lenovo",
            "ASUS": "ASUS", "Acer": "Acer", "MSI": "MSI",
            "ThinkPad": "ThinkPad", "MacBook": "MacBook",
        }
        
        # Mẫu câu phổ biến
        self.patterns = {
            "is running": "đang chạy",
            "is completed": "đã hoàn thành",
            "is ready": "đã sẵn sàng",
            "not found": "không tìm thấy",
            "not available": "không khả dụng",
            "not supported": "không được hỗ trợ",
            "please wait": "vui lòng đợi",
            "in progress": "đang tiến hành",
            "has failed": "đã thất bại",
            "has passed": "đã đạt",
        }
    
    def translate(self, text):
        """
        Dịch văn bản từ tiếng Anh sang tiếng Việt
        Args:
            text: Chuỗi tiếng Anh cần dịch
        Returns:
            Chuỗi tiếng Việt đã dịch
        """
        if not text or not isinstance(text, str):
            return text
        
        # Giữ nguyên nếu đã có tiếng Việt
        if self._has_vietnamese(text):
            return text
        
        result = text
        
        # Dịch theo mẫu câu trước
        for en_pattern, vi_pattern in self.patterns.items():
            if en_pattern.lower() in result.lower():
                result = result.lower().replace(en_pattern.lower(), vi_pattern)
        
        # Dịch từng từ
        words = result.split()
        translated_words = []
        
        for word in words:
            # Loại bỏ dấu câu
            clean_word = word.strip('.,!?;:()[]{}"\'-')
            prefix = word[:len(word)-len(word.lstrip('.,!?;:()[]{}"\'-'))]
            suffix = word[len(clean_word)+len(prefix):]
            
            # Tìm trong từ điển
            translated = self.dictionary.get(clean_word, 
                        self.dictionary.get(clean_word.lower(), 
                        self.dictionary.get(clean_word.capitalize(), clean_word)))
            
            translated_words.append(prefix + translated + suffix)
        
        return ' '.join(translated_words)
    
    def translate_dict(self, data):
        """
        Dịch tất cả giá trị string trong dictionary
        Args:
            data: Dictionary cần dịch
        Returns:
            Dictionary đã dịch
        """
        if not isinstance(data, dict):
            return data
        
        result = {}
        for key, value in data.items():
            # Dịch key
            translated_key = self.translate(key) if isinstance(key, str) else key
            
            # Dịch value
            if isinstance(value, str):
                result[translated_key] = self.translate(value)
            elif isinstance(value, dict):
                result[translated_key] = self.translate_dict(value)
            elif isinstance(value, list):
                result[translated_key] = [self.translate(v) if isinstance(v, str) else v for v in value]
            else:
                result[translated_key] = value
        
        return result
    
    def _has_vietnamese(self, text):
        """Kiểm tra xem chuỗi có chứa ký tự tiếng Việt không"""
        vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
        vietnamese_chars += vietnamese_chars.upper()
        return any(c in vietnamese_chars for c in text)
    
    def add_term(self, english, vietnamese):
        """Thêm thuật ngữ mới vào từ điển"""
        self.dictionary[english] = vietnamese
    
    def add_pattern(self, english_pattern, vietnamese_pattern):
        """Thêm mẫu câu mới"""
        self.patterns[english_pattern] = vietnamese_pattern

# Singleton instance
_translator = None

def get_translator():
    """Lấy instance của translator"""
    global _translator
    if _translator is None:
        _translator = AutoTranslator()
    return _translator

def translate(text):
    """Hàm tiện ích để dịch nhanh"""
    return get_translator().translate(text)

def translate_dict(data):
    """Hàm tiện ích để dịch dictionary"""
    return get_translator().translate_dict(data)

# Test function
if __name__ == "__main__":
    translator = AutoTranslator()
    
    # Test cases
    test_cases = [
        "CPU Test is running",
        "Battery Health Check",
        "GPU Performance Benchmark",
        "Hard Drive Speed Test",
        "Network Status: Good",
        "Temperature: 65°C",
        "Memory: 16GB RAM",
        "Test completed successfully",
        "Error: Not found",
        "Please wait, checking BIOS",
    ]
    
    print("=== Auto Translator Test ===\n")
    for text in test_cases:
        translated = translator.translate(text)
        print(f"EN: {text}")
        print(f"VI: {translated}")
        print()
