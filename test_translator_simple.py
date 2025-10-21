#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Auto Translator - Simple Version
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from translator import AutoTranslator, translate, translate_dict

def test_basic():
    print("=" * 60)
    print("TEST 1: BASIC TRANSLATION")
    print("=" * 60)
    
    translator = AutoTranslator()
    
    tests = [
        ("CPU Test", "CPU Kiem tra"),
        ("Battery Health", "Pin Suc khoe"),
        ("GPU Performance", "GPU Hieu nang"),
        ("Hard Drive Speed", "O cung Toc do"),
        ("Network Status", "Mang Trang thai"),
    ]
    
    for en, expected in tests:
        result = translator.translate(en)
        print(f"{en:30} -> {result}")
    print()

def test_sentences():
    print("=" * 60)
    print("TEST 2: SENTENCE TRANSLATION")
    print("=" * 60)
    
    translator = AutoTranslator()
    
    sentences = [
        "CPU Test is running",
        "Battery Health Check completed",
        "GPU Performance Benchmark",
        "Hard Drive not found",
        "Network Status: Good",
    ]
    
    for sentence in sentences:
        translated = translator.translate(sentence)
        print(f"EN: {sentence}")
        print(f"VI: {translated}")
        print()

def test_dict():
    print("=" * 60)
    print("TEST 3: DICTIONARY TRANSLATION")
    print("=" * 60)
    
    data = {
        "CPU": "Intel Core i7",
        "GPU": "NVIDIA RTX 3060",
        "RAM": "16GB",
        "Storage": "512GB SSD",
        "Battery": "Good",
        "Status": "Running",
    }
    
    translated = translate_dict(data)
    
    print("Original:")
    for k, v in data.items():
        print(f"  {k}: {v}")
    
    print("\nTranslated:")
    for k, v in translated.items():
        print(f"  {k}: {v}")
    print()

def test_results():
    print("=" * 60)
    print("TEST 4: TEST RESULTS")
    print("=" * 60)
    
    results = {
        "CPU Test": {"Status": "Pass", "Result": "Good"},
        "GPU Test": {"Status": "Pass", "Result": "Excellent"},
        "Battery Test": {"Status": "Warning", "Result": "Fair"},
    }
    
    translated = translate_dict(results)
    
    print("Test Results:")
    for test, result in translated.items():
        print(f"\n{test}:")
        for k, v in result.items():
            print(f"  {k}: {v}")
    print()

if __name__ == "__main__":
    print("\n=== AUTO TRANSLATOR TEST ===\n")
    
    test_basic()
    test_sentences()
    test_dict()
    test_results()
    
    print("=" * 60)
    print("[OK] ALL TESTS COMPLETED")
    print("=" * 60)
