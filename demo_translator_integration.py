#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Translator Integration Test
Test translator voi ung dung LaptopTester
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from translator import translate, translate_dict

print("=" * 60)
print("DEMO: TRANSLATOR INTEGRATION TEST")
print("=" * 60)

# Test 1: Dịch các text trong UI
print("\n1. UI Text Translation:")
ui_texts = [
    "Hardware Fingerprint",
    "License Check", 
    "System Info",
    "Hard Drive Health",
    "Screen Test",
    "Keyboard Test",
    "Battery Health",
    "Audio Test",
    "Webcam Test",
    "CPU Stress Test",
    "GPU Stress Test"
]

for text in ui_texts:
    translated = translate(text)
    print(f"  {text:25} -> {translated}")

# Test 2: Dịch kết quả test
print("\n2. Test Results Translation:")
test_results = {
    "Hardware Fingerprint": {
        "Result": "Completed",
        "Status": "Good",
        "CPU": "Intel Core i7-11800H",
        "GPU": "NVIDIA RTX 3050 Ti"
    },
    "License Check": {
        "Result": "Activated permanently",
        "Status": "Good"
    },
    "Battery Health": {
        "Result": "Good",
        "Status": "Pass",
        "Health": "85%"
    }
}

translated_results = translate_dict(test_results)
print("\nOriginal:")
for step, result in test_results.items():
    print(f"  {step}: {result}")

print("\nTranslated:")
for step, result in translated_results.items():
    print(f"  {step}: {result}")

# Test 3: Dịch status messages
print("\n3. Status Messages:")
messages = [
    "Test is running",
    "CPU usage: 85%",
    "Temperature: 75°C",
    "Test completed successfully",
    "Error: Not found",
    "Warning: High temperature"
]

for msg in messages:
    translated = translate(msg)
    print(f"  EN: {msg}")
    print(f"  VI: {translated}")
    print()

print("=" * 60)
print("DEMO COMPLETED")
print("=" * 60)
print("\nTranslator đã sẵn sàng tích hợp vào main_enhanced_auto.py!")
print("Sử dụng: from translator import translate, translate_dict")
