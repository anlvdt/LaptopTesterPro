#!/usr/bin/env python3
"""
LaptopTester Pro Enhanced - Main Launcher
Run this file to start the enhanced version
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main_enhanced import EnhancedLaptopTesterApp
    
    if __name__ == "__main__":
        print("🚀 Starting LaptopTester Pro Enhanced...")
        print("📦 Loading advanced modules...")
        
        app = EnhancedLaptopTesterApp()
        app.run()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("📋 Please install required packages:")
    print("   pip install -r requirements_enhanced.txt")
    input("Press Enter to exit...")
except Exception as e:
    print(f"❌ Error: {e}")
    input("Press Enter to exit...")