#!/usr/bin/env python3
"""
Startup Optimization for LaptopTester
Tối ưu hóa khởi động ứng dụng
"""

import os
import sys
import threading
import time

# Lazy import strategy
def lazy_import():
    """Import heavy modules in background"""
    try:
        import numpy
        import cv2
        import pygame
        import matplotlib
        print("[STARTUP] Heavy modules loaded in background")
    except:
        pass

# Pre-compile regex patterns
import re
CPU_PATTERN = re.compile(r'(intel|amd|ryzen|i[3579])', re.IGNORECASE)
RAM_PATTERN = re.compile(r'(\d+(?:\.\d+)?)\s*GB', re.IGNORECASE)

# Cache system info
_SYSTEM_CACHE = {}

def get_cached_system_info():
    """Get cached system info to avoid repeated calls"""
    global _SYSTEM_CACHE
    
    if not _SYSTEM_CACHE:
        try:
            import psutil
            import platform
            
            _SYSTEM_CACHE = {
                'cpu_count': psutil.cpu_count(),
                'memory_total': round(psutil.virtual_memory().total / (1024**3), 1),
                'processor': platform.processor(),
                'system': platform.system()
            }
        except:
            _SYSTEM_CACHE = {'error': True}
    
    return _SYSTEM_CACHE

# Optimize imports
def optimize_imports():
    """Optimize module imports for faster startup"""
    
    # Start background loading
    threading.Thread(target=lazy_import, daemon=True).start()
    
    # Pre-cache system info
    threading.Thread(target=get_cached_system_info, daemon=True).start()

if __name__ == "__main__":
    print("Optimizing startup...")
    optimize_imports()
    time.sleep(1)
    print("Optimization complete!")