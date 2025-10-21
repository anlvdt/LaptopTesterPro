"""
utils.py - Các hàm tiện ích chung cho LaptopTester
"""
import platform
import os

def is_windows():
    return platform.system() == "Windows"

def asset_path(rel_path):
    return os.path.join(os.path.dirname(__file__), 'assets', rel_path)
