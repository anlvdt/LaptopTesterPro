#!/usr/bin/env python3
"""
LaptopTester Pro - With Auto Translator
Demo tích hợp module dịch tự động
"""

# Import translator
from translator import translate, translate_dict, get_translator

# Ví dụ tích hợp vào LanguageManager
class EnhancedLanguageManager:
    def __init__(self):
        self.current_language = "vi"
        self.translator = get_translator()
        
        # Translations cơ bản
        self.translations = {
            "vi": {
                "app_title": "Laptop Tester Pro",
                "exit": "Thoát",
                "settings": "Cài đặt",
                # ... các translations khác
            },
            "en": {
                "app_title": "Laptop Tester Pro",
                "exit": "Exit",
                "settings": "Settings",
                # ... các translations khác
            }
        }
    
    def get_text(self, key):
        """Lấy text với auto-translate fallback"""
        # Thử lấy từ translations trước
        if key in self.translations[self.current_language]:
            return self.translations[self.current_language][key]
        
        # Nếu không có, dùng translator
        if self.current_language == "vi":
            return self.translator.translate(key)
        
        return key
    
    def translate_result(self, result_data):
        """Dịch kết quả test"""
        if self.current_language == "vi":
            return translate_dict(result_data)
        return result_data

# Ví dụ tích hợp vào BaseStepFrame
class EnhancedBaseStepFrame:
    def __init__(self, master, title, why_text, how_text, **kwargs):
        self.translator = get_translator()
        self.language = kwargs.get("language", "vi")
        
        # Dịch tự động nếu cần
        if self.language == "vi":
            self.title = self.translator.translate(title)
            self.why_text = self.translator.translate(why_text)
            self.how_text = self.translator.translate(how_text)
        else:
            self.title = title
            self.why_text = why_text
            self.how_text = how_text
        
        # ... rest of initialization
    
    def mark_completed(self, result_data, auto_advance=False):
        """Mark step as completed with translated results"""
        # Dịch kết quả nếu cần
        if self.language == "vi":
            result_data = translate_dict(result_data)
        
        # Record result
        if hasattr(self, 'record_result') and self.record_result:
            self.record_result(self.title, result_data)
        
        # Auto advance if needed
        if auto_advance and hasattr(self, 'go_to_next_step_callback'):
            self.go_to_next_step_callback()

# Ví dụ tích hợp vào SummaryStep
class EnhancedSummaryStep:
    def __init__(self, master, **kwargs):
        self.translator = get_translator()
        self.language = kwargs.get("language", "vi")
        # ... rest of initialization
    
    def display_summary(self, results):
        """Display summary with translated results"""
        # Dịch toàn bộ kết quả nếu cần
        if self.language == "vi":
            results = translate_dict(results)
        
        # Display results
        for step_name, result_data in results.items():
            self._create_result_item(step_name, result_data)
    
    def _create_result_item(self, step_name, result_data):
        """Create result item with translated content"""
        status = result_data.get("Status", "Unknown")
        result_text = result_data.get("Result", "N/A")
        
        # Dịch status và result nếu cần
        if self.language == "vi":
            status = self.translator.translate(status)
            result_text = self.translator.translate(result_text)
        
        # ... create UI elements

# Demo: Sử dụng trong thực tế
def demo_hardware_info_translation():
    """Demo dịch thông tin phần cứng"""
    print("=" * 60)
    print("DEMO: DỊCH THÔNG TIN PHẦN CỨNG")
    print("=" * 60)
    
    # Giả lập thông tin từ WMI
    hardware_info = {
        "Model Laptop": "Dell XPS 15 9510",
        "Serial Number": "ABC123456",
        "CPU": "Intel Core i7-11800H @ 2.30GHz",
        "GPU": "NVIDIA GeForce RTX 3050 Ti Laptop GPU",
        "Model Ổ Cứng": "Samsung SSD 980 PRO 512GB",
        "Ngày BIOS": "15/03/2023"
    }
    
    # Dịch sang tiếng Việt
    translated = translate_dict(hardware_info)
    
    print("\nThông tin phần cứng (đã dịch):")
    for key, value in translated.items():
        print(f"  {key}: {value}")
    print()

def demo_test_results_translation():
    """Demo dịch kết quả test"""
    print("=" * 60)
    print("DEMO: DỊCH KẾT QUẢ TEST")
    print("=" * 60)
    
    # Giả lập kết quả test
    test_results = {
        "Physical Inspection": {
            "Result": "Good",
            "Status": "Pass",
            "Details": "No physical damage"
        },
        "BIOS Check": {
            "Result": "Good",
            "Status": "Pass",
            "Details": "All settings correct"
        },
        "Hardware Fingerprint": {
            "Result": "Completed",
            "Status": "Pass",
            "CPU": "Intel Core i7",
            "GPU": "NVIDIA RTX 3050 Ti"
        },
        "License Check": {
            "Result": "Activated",
            "Status": "Pass",
            "Details": "Windows activated permanently"
        },
        "Battery Health": {
            "Result": "Good",
            "Status": "Pass",
            "Capacity": "85%",
            "Cycles": "120"
        }
    }
    
    # Dịch toàn bộ
    translated = translate_dict(test_results)
    
    print("\nKết quả kiểm tra (đã dịch):")
    for step_name, result in translated.items():
        print(f"\n📋 {step_name}:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    print()

def demo_status_messages_translation():
    """Demo dịch thông báo trạng thái"""
    print("=" * 60)
    print("DEMO: DỊCH THÔNG BÁO TRẠNG THÁI")
    print("=" * 60)
    
    messages = [
        "CPU Test is running",
        "Battery Health Check completed",
        "GPU Performance Benchmark in progress",
        "Hard Drive not found",
        "Network Status: Good",
        "Temperature: 65°C - Warning",
        "Memory: 16GB RAM - Good",
        "Test has passed successfully",
        "Error: Device not available",
        "Please wait, checking BIOS settings",
    ]
    
    print("\nThông báo (đã dịch):")
    for msg in messages:
        translated = translate(msg)
        print(f"  EN: {msg}")
        print(f"  VI: {translated}")
        print()

def demo_custom_terms():
    """Demo thêm thuật ngữ tùy chỉnh"""
    print("=" * 60)
    print("DEMO: THUẬT NGỮ TÙY CHỈNH")
    print("=" * 60)
    
    translator = get_translator()
    
    # Thêm thuật ngữ chuyên ngành
    custom_terms = {
        "Throttling": "Giảm hiệu năng",
        "Bottleneck": "Nút thắt cổ chai",
        "Overheating": "Quá nhiệt",
        "Undervolting": "Giảm điện áp",
        "Overclocking": "Ép xung",
        "Thermal Paste": "Keo tản nhiệt",
        "Repaste": "Thay keo tản nhiệt",
        "Liquid Metal": "Kim loại lỏng",
    }
    
    for en, vi in custom_terms.items():
        translator.add_term(en, vi)
    
    # Test với thuật ngữ mới
    test_messages = [
        "CPU Throttling detected",
        "GPU Bottleneck found",
        "System Overheating warning",
        "Thermal Paste needs replacement",
        "Overclocking not recommended",
    ]
    
    print("\nThông báo với thuật ngữ tùy chỉnh:")
    for msg in test_messages:
        translated = translator.translate(msg)
        print(f"  EN: {msg}")
        print(f"  VI: {translated}")
        print()

def demo_integration_example():
    """Demo tích hợp hoàn chỉnh"""
    print("=" * 60)
    print("DEMO: TÍCH HỢP HOÀN CHỈNH")
    print("=" * 60)
    
    # Giả lập flow của ứng dụng
    print("\n1. Khởi tạo Language Manager với Translator:")
    lang_manager = EnhancedLanguageManager()
    print(f"   ✅ Language: {lang_manager.current_language}")
    
    print("\n2. Lấy text với auto-translate:")
    texts = ["CPU Test", "Battery Health", "Network Status"]
    for text in texts:
        translated = lang_manager.get_text(text)
        print(f"   {text} -> {translated}")
    
    print("\n3. Dịch kết quả test:")
    result = {
        "Result": "Pass",
        "Status": "Good",
        "Temperature": "65°C"
    }
    translated_result = lang_manager.translate_result(result)
    print(f"   Original: {result}")
    print(f"   Translated: {translated_result}")
    
    print("\n4. Tích hợp vào BaseStepFrame:")
    print("   ✅ Title, why_text, how_text được dịch tự động")
    print("   ✅ Result data được dịch khi mark_completed")
    
    print("\n5. Tích hợp vào SummaryStep:")
    print("   ✅ Tất cả results được dịch trước khi hiển thị")
    print()

if __name__ == "__main__":
    print("\n🌐 LAPTOPTESTER PRO - AUTO TRANSLATOR DEMO\n")
    
    # Chạy tất cả demos
    demo_hardware_info_translation()
    demo_test_results_translation()
    demo_status_messages_translation()
    demo_custom_terms()
    demo_integration_example()
    
    print("=" * 60)
    print("✅ DEMO HOÀN THÀNH")
    print("=" * 60)
    print("\n📖 Xem thêm: TRANSLATOR_GUIDE.md")
    print("🧪 Test module: python test_translator.py")
    print()
