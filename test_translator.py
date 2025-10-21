#!/usr/bin/env python3
"""
Test Auto Translator
Demo và test các tính năng dịch tự động
"""

from translator import AutoTranslator, translate, translate_dict

def test_basic_translation():
    """Test dịch cơ bản"""
    print("=" * 60)
    print("TEST 1: DỊCH CƠ BẢN")
    print("=" * 60)
    
    translator = AutoTranslator()
    
    test_cases = [
        "CPU Test",
        "Battery Health",
        "GPU Performance",
        "Hard Drive Speed",
        "Network Status",
        "Memory Check",
        "Temperature Monitor",
        "BIOS Settings",
        "Windows License",
        "Keyboard Test",
    ]
    
    for text in test_cases:
        translated = translator.translate(text)
        print(f"{text:30} -> {translated}")
    print()

def test_sentence_translation():
    """Test dịch câu"""
    print("=" * 60)
    print("TEST 2: DỊCH CÂU")
    print("=" * 60)
    
    translator = AutoTranslator()
    
    sentences = [
        "CPU Test is running",
        "Battery Health Check completed",
        "GPU Performance Benchmark in progress",
        "Hard Drive not found",
        "Network Status: Good",
        "Temperature: 65°C",
        "Memory: 16GB RAM",
        "Test has passed",
        "Error: Not available",
        "Please wait, checking BIOS",
    ]
    
    for sentence in sentences:
        translated = translator.translate(sentence)
        print(f"EN: {sentence}")
        print(f"VI: {translated}")
        print()

def test_dict_translation():
    """Test dịch dictionary"""
    print("=" * 60)
    print("TEST 3: DỊCH DICTIONARY")
    print("=" * 60)
    
    test_data = {
        "CPU": "Intel Core i7",
        "GPU": "NVIDIA RTX 3060",
        "RAM": "16GB",
        "Storage": "512GB SSD",
        "Battery": "Good",
        "Status": "Running",
        "Result": "Pass",
        "Temperature": "65°C",
        "Performance": "Excellent",
    }
    
    translated = translate_dict(test_data)
    
    print("Original:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    print("\nTranslated:")
    for key, value in translated.items():
        print(f"  {key}: {value}")
    print()

def test_hardware_info():
    """Test dịch thông tin phần cứng"""
    print("=" * 60)
    print("TEST 4: THÔNG TIN PHẦN CỨNG")
    print("=" * 60)
    
    hardware_info = {
        "Model Laptop": "Dell XPS 15",
        "CPU": "Intel Core i7-11800H",
        "GPU": "NVIDIA GeForce RTX 3050 Ti",
        "RAM": "16GB DDR4",
        "Storage": "512GB NVMe SSD",
        "Display": "15.6 inch FHD",
        "Battery": "86Wh",
        "Status": "Good",
    }
    
    translated = translate_dict(hardware_info)
    
    print("Hardware Information:")
    for key, value in translated.items():
        print(f"  {key}: {value}")
    print()

def test_test_results():
    """Test dịch kết quả test"""
    print("=" * 60)
    print("TEST 5: KẾT QUẢ TEST")
    print("=" * 60)
    
    test_results = {
        "CPU Test": {"Status": "Pass", "Result": "Good"},
        "GPU Test": {"Status": "Pass", "Result": "Excellent"},
        "Memory Test": {"Status": "Pass", "Result": "Good"},
        "Storage Test": {"Status": "Warning", "Result": "Fair"},
        "Battery Test": {"Status": "Pass", "Result": "Good"},
        "Network Test": {"Status": "Pass", "Result": "Good"},
    }
    
    translated = translate_dict(test_results)
    
    print("Test Results:")
    for test_name, result in translated.items():
        print(f"\n{test_name}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    print()

def test_custom_terms():
    """Test thêm thuật ngữ tùy chỉnh"""
    print("=" * 60)
    print("TEST 6: THUẬT NGỮ TÙY CHỈNH")
    print("=" * 60)
    
    translator = AutoTranslator()
    
    # Thêm thuật ngữ mới
    translator.add_term("Throttling", "Giảm hiệu năng")
    translator.add_term("Bottleneck", "Nút thắt cổ chai")
    translator.add_term("Overheating", "Quá nhiệt")
    
    test_cases = [
        "CPU Throttling detected",
        "GPU Bottleneck found",
        "System Overheating warning",
    ]
    
    for text in test_cases:
        translated = translator.translate(text)
        print(f"EN: {text}")
        print(f"VI: {translated}")
        print()

def demo_integration():
    """Demo tích hợp vào ứng dụng"""
    print("=" * 60)
    print("DEMO: TÍCH HỢP VÀO ỨNG DỤNG")
    print("=" * 60)
    
    # Giả lập kết quả từ ứng dụng
    app_results = {
        "Physical Inspection": {
            "Result": "Good",
            "Status": "Pass",
            "Details": "No physical damage found"
        },
        "BIOS Check": {
            "Result": "Good",
            "Status": "Pass",
            "Details": "All settings correct"
        },
        "Hardware Fingerprint": {
            "Result": "Completed",
            "Status": "Pass",
            "CPU": "Intel Core i7-11800H",
            "GPU": "NVIDIA RTX 3050 Ti",
            "RAM": "16GB",
        },
        "License Check": {
            "Result": "Activated",
            "Status": "Pass",
            "Details": "Windows is activated permanently"
        },
    }
    
    # Dịch toàn bộ kết quả
    translated_results = translate_dict(app_results)
    
    print("Kết quả kiểm tra (đã dịch):\n")
    for step_name, result in translated_results.items():
        print(f"📋 {step_name}:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        print()

if __name__ == "__main__":
    print("\n=== AUTO TRANSLATOR - DEMO & TEST ===\n")
    
    # Chạy tất cả tests
    test_basic_translation()
    test_sentence_translation()
    test_dict_translation()
    test_hardware_info()
    test_test_results()
    test_custom_terms()
    demo_integration()
    
    print("=" * 60)
    print("[OK] TAT CA TESTS HOAN THANH")
    print("=" * 60)
