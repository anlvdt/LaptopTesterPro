"""
test_bios_detection.py - Test script for BIOS detection functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from bios_detector import bios_detector

def test_bios_detection():
    """Test all BIOS detection methods"""
    print("=== BIOS Detection Test ===\n")
    
    # Test CPU detection
    print("1. Testing CPU Detection:")
    try:
        cpu_info = bios_detector.get_cpu_info()
        print(f"   CPU: {cpu_info}")
        if "Không thể đọc" in cpu_info:
            print(f"   Last Error: {bios_detector.last_error}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test BIOS info
    print("2. Testing BIOS Information:")
    try:
        bios_info = bios_detector.get_bios_info()
        for key, value in bios_info.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test System info
    print("3. Testing System Information:")
    try:
        system_info = bios_detector.get_system_info()
        for key, value in system_info.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_bios_detection()