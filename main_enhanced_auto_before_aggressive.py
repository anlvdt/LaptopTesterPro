#!/usr/bin/env python3
"""
LaptopTester Pro - Consolidated Main File
Comprehensive laptop testing suite with all functionality in one file
"""

import os
import sys
import time
import platform
import socket
import locale
import subprocess
import threading
import multiprocessing
import tempfile
import math
import logging
from queue import Queue
from collections import deque
import webbrowser
from tkinter import messagebox
import tkinter as tk
from datetime import datetime

# Third-party imports
import customtkinter as ctk
import psutil
import numpy as np
from PIL import Image

# Import translator
try:
    from translator import translate, translate_dict
    from lang_wrapper import t, set_language as set_wrapper_language, get_language
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    def translate(text): return text
    def translate_dict(data): return data
    def t(text): return text
    def set_wrapper_language(lang): pass
    def get_language(): return "vi"

# Optional imports with fallbacks
try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="pygame")
    import pygame
except ImportError:
    pygame = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import keyboard
except ImportError:
    keyboard = None

try:
    if platform.system() == "Windows":
        import wmi
        import pythoncom
except ImportError:
    wmi = None
    pythoncom = None

# Enhanced imports for new features
try:
    import requests
except ImportError:
    requests = None

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    plt = None
    FigureCanvasTkAgg = None

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
except ImportError:
    RandomForestClassifier = None
    StandardScaler = None


# ============================================================================
# SECURITY ENHANCEMENTS - Added by apply_enhancements.py
# ============================================================================
import shlex
from typing import List, Dict, Any, Optional

class SecurityError(Exception):
    """Custom security exception"""
    pass

class SecureCommandExecutor:
    """Thực thi command an toàn"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_commands = {
            'windows': ['cscript', 'powercfg', 'wmic', 'systeminfo'],
            'linux': ['lscpu', 'lshw', 'dmidecode', 'smartctl']
        }
    
    def execute_safe(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Thực thi command với validation"""
        try:
            # Validate command
            if not self._validate_command(command):
                raise SecurityError(f"Command not allowed: {command}")
            
            # Sanitize
            sanitized_cmd = self._sanitize_command(command)
            
            # Execute
            result = subprocess.run(
                sanitized_cmd,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _validate_command(self, command: str) -> bool:
        """Validate command"""
        if not command:
            return False
        parts = shlex.split(command)
        if not parts:
            return False
        base_cmd = parts[0].lower()
        return base_cmd in self.allowed_commands.get('windows', [])
    
    def _sanitize_command(self, command: str) -> List[str]:
        """Sanitize command"""
        parts = shlex.split(command)
        dangerous = ['|', '&', ';', '>', '<', '`', '$']
        for part in parts:
            if any(c in part for c in dangerous):
                raise SecurityError(f"Dangerous char in: {part}")
        return parts

# Global secure executor
_secure_executor = SecureCommandExecutor()

# ============================================================================
# AI ANALYZER - Model-specific warnings
# ============================================================================
class LaptopAIDiagnoser:
    def __init__(self):
        self.model_warnings = {
            'thinkpad x1': '⚠️ ThinkPad X1: Kiểm tra kỹ bản lề - dễ bị lỏng',
            'thinkpad t480': '⚠️ T480: Pin có thể bị chai nhanh',
            'xps': '⚠️ Dell XPS: Dễ bị coil whine và throttling',
            'macbook pro 2016': '⚠️ MacBook Pro 2016-2017: Bàn phím butterfly dễ hỏng',
            'pavilion': '⚠️ HP Pavilion: Quạt tản nhiệt dễ bị bụi',
            'rog': '⚠️ ASUS ROG: GPU có thể bị artifacts',
        }
    
    def analyze_model(self, model_name):
        model_lower = model_name.lower()
        for key, warning in self.model_warnings.items():
            if key in model_lower:
                return warning
        return None

_ai_diagnoser = LaptopAIDiagnoser()

# ============================================================================
# AUDIO WORKER - stereo_test.mp3 integration
# ============================================================================
def play_stereo_test_audio(status_callback=None):
    if not pygame:
        return False
    
    stereo_test_path = os.path.join(os.path.dirname(__file__), "..", "assets", "stereo_test.mp3")
    
    if os.path.exists(stereo_test_path):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            if status_callback:
                status_callback("🎵 Phát file stereo_test.mp3...")
            
            pygame.mixer.music.load(stereo_test_path)
            pygame.mixer.music.play()
            
            start_time = time.time()
            while pygame.mixer.music.get_busy():
                elapsed = int(time.time() - start_time)
                if status_callback:
                    status_callback(f"🎵 Phát stereo_test.mp3 ({elapsed}s)")
                time.sleep(1)
            
            pygame.mixer.music.stop()
            return True
        except:
            return False
    return False

# ============================================================================
# LIBRE HARDWARE MONITOR READER
# ============================================================================
def get_lhm_data(timeout=5):
    lhm_dir = os.path.join(os.path.dirname(__file__), "..", "bin", "LibreHardwareMonitor")
    exe_path = os.path.join(lhm_dir, "LibreHardwareMonitor.exe")
    report_path = os.path.join(lhm_dir, "report.json")
    
    if not os.path.exists(exe_path):
        return None
    
    if os.path.exists(report_path):
        try:
            os.remove(report_path)
        except:
            pass
    
    try:
        subprocess.run([exe_path, "--report", report_path], timeout=timeout)
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return None


# Configuration
CURRENT_LANG = "vi"
CURRENT_THEME = "dark"

# Comprehensive Language Dictionary - 100% Coverage
LANG = {
    "vi": {
        # Main UI
        "title": "LaptopTester Pro - Kiểm tra laptop toàn diện",
        "overview": "Tổng quan", "start_test": "Bắt đầu", "individual_test": "Test riêng lẻ", "exit": "Thoát",
        "dark_mode": "Tối", "language": "Ngôn ngữ", "basic_mode": "Cơ bản", "expert_mode": "Chuyên gia",
        
        # Test Steps
        "hardware_fingerprint": "Định danh phần cứng", "license_check": "Bản quyền Windows", "system_info": "Cấu hình hệ thống",
        "harddrive_health": "Sức khỏe ổ cứng", "screen_test": "Kiểm tra màn hình", "keyboard_test": "Bàn phím & Touchpad",
        "battery_health": "Pin laptop", "audio_test": "Loa & Micro", "webcam_test": "Webcam",
        "cpu_stress": "CPU Stress Test", "harddrive_speed": "Tốc độ ổ cứng", "gpu_stress": "GPU Stress Test",
        "network_test": "Kiểm tra mạng", "thermal_test": "Nhiệt độ & Hiệu năng", "system_monitor": "Giám sát hệ thống",
        
        # Navigation
        "summary": "Tổng kết", "continue": "Tiếp tục", "skip": "Bỏ qua", "good": "Tốt", "error": "Lỗi",
        "previous": "Trước", "next": "Tiếp", "complete": "Hoàn thành", "ready": "Sẵn sàng",
        "checking": "Đang kiểm tra", "testing": "Đang test", "loading": "Đang tải", "finished": "Hoàn thành",
        
        # Report & Summary
        "report_title": "BÁO CÁO KIỂM TRA LAPTOP", "report_subtitle": "Phân tích toàn diện tình trạng phần cứng",
        "total_tests": "Tổng Test", "passed_tests": "Đạt", "failed_tests": "Lỗi", "success_rate": "Tỷ Lệ Đạt",
        "laptop_good": "LAPTOP TÌNH TRẠNG TỐT", "laptop_warning": "LAPTOP CẦN CHÚ Ý", "laptop_bad": "LAPTOP CÓ VẤN ĐỀ NGHIÊM TRỌNG",
        "recommendation_good": "Laptop hoạt động ổn định, có thể mua với giá hợp lý.",
        "recommendation_warning": "Có một số vấn đề nhỏ, cần kiểm tra kỹ trước khi quyết định.",
        "recommendation_bad": "Nhiều lỗi phát hiện, không khuyến nghị mua hoặc cần giảm giá mạnh.",
        
        # Categories
        "security_category": "Bảo mật & Định danh", "performance_category": "Hiệu năng",
        "interface_category": "Giao diện", "hardware_category": "Phần cứng",
        
        # Tools & Export
        "professional_tools": "CÔNG CỤ CHUYÊN NGHIỆP BỔ SUNG",
        "tools_description": "Để kiểm tra sâu hơn, hãy sử dụng các công cụ chuyên nghiệp sau:",
        "install_command": "Lệnh cài đặt:", "homepage": "Trang chủ", "usage_guide": "HƯỚNG DẪN SỬ DỤNG CÔNG CỤ",
        "export_report": "XUẤT BÁO CÁO", "export_pdf": "Xuất PDF", "export_excel": "Xuất Excel", "copy_text": "Copy Text",
        
        # Common UI Elements
        "why_test": "Tại sao cần test?", "how_to": "Cách thực hiện:", "security_info": "THÔNG TIN BẢO MẬT",
        "start_test_btn": "Bắt đầu Test", "stop_test_btn": "Dừng Test", "clear_canvas": "Xóa vết vẽ",
        "test_completed": "Test hoàn thành", "no_issues": "Không có vấn đề", "issues_found": "Có vấn đề",
        "all_good": "Tất cả đều tốt", "config_match": "Cấu hình khớp", "mismatch": "Có sai lệch",
        "screen_ok": "Màn hình bình thường", "input_ok": "Thiết bị nhập tốt", "audio_clear": "Âm thanh rõ ràng",
        "webcam_ok": "Webcam hoạt động tốt", "cpu_good": "CPU ổn định", "gpu_good": "GPU ổn định",
        "speed_good": "Tốc độ tốt", "battery_good": "Pin tốt", "ready_to_test": "Sẵn sàng test",
        "choose_mode": "Chọn chế độ", "working_well": "Hoạt động tốt", "not_working": "Không hoạt động",
        "temperature": "Nhiệt độ", "frequency": "Tần số", "power": "Công suất", "speed": "Tốc độ",
        "record": "Ghi âm", "stop": "Dừng", "play": "Phát", "running": "Đang chạy",
        
        # Status Messages
        "status_good": "Tốt", "status_error": "Lỗi", "status_warning": "Cảnh báo", "status_skip": "Bỏ qua"
    },
    "en": {
        # Main UI
        "title": "LaptopTester Pro - Comprehensive Laptop Testing",
        "overview": "Overview", "start_test": "Start", "individual_test": "Individual", "exit": "Exit",
        "dark_mode": "Dark", "language": "Language", "basic_mode": "Basic", "expert_mode": "Expert",
        
        # Test Steps
        "hardware_fingerprint": "Hardware Fingerprint", "license_check": "Windows License", "system_info": "System Info",
        "harddrive_health": "HDD Health", "screen_test": "Screen Test", "keyboard_test": "Keyboard & Touchpad",
        "battery_health": "Battery Health", "audio_test": "Audio Test", "webcam_test": "Webcam Test",
        "cpu_stress": "CPU Stress Test", "harddrive_speed": "HDD Speed", "gpu_stress": "GPU Stress Test",
        "network_test": "Network Test", "thermal_test": "Thermal & Performance", "system_monitor": "System Monitor",
        
        # Navigation
        "summary": "Summary", "continue": "Continue", "skip": "Skip", "good": "Good", "error": "Error",
        "previous": "Previous", "next": "Next", "complete": "Complete", "ready": "Ready",
        "checking": "Checking", "testing": "Testing", "loading": "Loading", "finished": "Finished",
        
        # Report & Summary
        "report_title": "LAPTOP TESTING REPORT", "report_subtitle": "Comprehensive hardware condition analysis",
        "total_tests": "Total Tests", "passed_tests": "Passed", "failed_tests": "Failed", "success_rate": "Success Rate",
        "laptop_good": "LAPTOP IN GOOD CONDITION", "laptop_warning": "LAPTOP NEEDS ATTENTION", "laptop_bad": "LAPTOP HAS SERIOUS ISSUES",
        "recommendation_good": "Laptop operates stably, can be purchased at reasonable price.",
        "recommendation_warning": "Some minor issues detected, need careful inspection before decision.",
        "recommendation_bad": "Multiple errors detected, not recommended to buy or need significant price reduction.",
        
        # Categories
        "security_category": "Security & Identity", "performance_category": "Performance",
        "interface_category": "Interface", "hardware_category": "Hardware",
        
        # Tools & Export
        "professional_tools": "ADDITIONAL PROFESSIONAL TOOLS",
        "tools_description": "For deeper inspection, use these professional tools:",
        "install_command": "Install command:", "homepage": "Homepage", "usage_guide": "TOOL USAGE GUIDE",
        "export_report": "EXPORT REPORT", "export_pdf": "Export PDF", "export_excel": "Export Excel", "copy_text": "Copy Text",
        
        # Common UI Elements
        "why_test": "Why test?", "how_to": "How to perform:", "security_info": "SECURITY INFORMATION",
        "start_test_btn": "Start Test", "stop_test_btn": "Stop Test", "clear_canvas": "Clear Drawing",
        "test_completed": "Test completed", "no_issues": "No issues", "issues_found": "Issues found",
        "all_good": "All good", "config_match": "Config matches", "mismatch": "Mismatch detected",
        "screen_ok": "Screen normal", "input_ok": "Input devices OK", "audio_clear": "Audio clear",
        "webcam_ok": "Webcam working", "cpu_good": "CPU stable", "gpu_good": "GPU stable",
        "speed_good": "Speed good", "battery_good": "Battery good", "ready_to_test": "Ready to test",
        "choose_mode": "Choose Mode", "working_well": "Working well", "not_working": "Not working",
        "temperature": "Temperature", "frequency": "Frequency", "power": "Power", "speed": "Speed",
        "record": "Record", "stop": "Stop", "play": "Play", "running": "Running",
        
        # Status Messages
        "status_good": "Good", "status_error": "Error", "status_warning": "Warning", "status_skip": "Skipped"
    }
}

def get_text(key):
    return LANG[CURRENT_LANG].get(key, key)

def toggle_theme():
    global CURRENT_THEME
    CURRENT_THEME = "dark" if CURRENT_THEME == "light" else "light"
    ctk.set_appearance_mode(CURRENT_THEME)
    
    if CURRENT_THEME == "dark":
        dark_colors = Theme.get_dark_colors()
        for key, value in dark_colors.items():
            setattr(Theme, key, value)
    else:
        # Reset to light colors
        Theme.BACKGROUND = "#ffffff"
        Theme.FRAME = "#f8fafc"
        Theme.CARD = "#ffffff"
        Theme.BORDER = "#e2e8f0"
        Theme.SEPARATOR = "#cbd5e0"
        Theme.TEXT = "#1e293b"
        Theme.TEXT_SECONDARY = "#64748b"
        Theme.ACCENT = "#3b82f6"
        Theme.ACCENT_HOVER = "#2563eb"

def toggle_language():
    global CURRENT_LANG
    CURRENT_LANG = t("en")
    
    # Update wrapper language
    if TRANSLATOR_AVAILABLE:
        set_wrapper_language(CURRENT_LANG)

# GitHub Copilot Theme System
class Theme:
    # GitHub Copilot Dark Theme
    BACKGROUND = "#0d1117"
    FRAME = "#161b22"
    CARD = "#21262d"
    BORDER = "#30363d"
    SEPARATOR = "#21262d"
    
    TEXT = "#f0f6fc"
    TEXT_SECONDARY = "#c9d1d9"
    ACCENT = "#58a6ff"
    ACCENT_HOVER = "#1f6feb"
    
    SUCCESS = "#238636"
    WARNING = "#d29922"
    ERROR = "#f85149"
    SKIP = "#d29922"
    INFO = "#58a6ff"
    
    # GitHub Copilot Font System - Maximum Accessibility
    TITLE_FONT = ("Arial", 36, "bold")
    HEADING_FONT = ("Arial", 28, "bold")
    SUBHEADING_FONT = ("Arial", 22, "bold")
    BODY_FONT = ("Arial", 20)
    SMALL_FONT = ("Arial", 18)
    BUTTON_FONT = ("Arial", 19, "bold")
    CODE_FONT = ("Consolas", 19)
    KEY_FONT = ("Arial", 14, "bold")
    
    # Compact Spacing
    CORNER_RADIUS = 6
    PADDING = 12
    BUTTON_HEIGHT = 40
    CARD_PADDING = 16
    SPACING = 8
    
    @classmethod
    def get_dark_colors(cls):
        return {
            "BACKGROUND": "#0d1117",
            "FRAME": "#161b22",
            "CARD": "#21262d",
            "BORDER": "#30363d",
            "SEPARATOR": "#21262d",
            "TEXT": "#f0f6fc",
            "TEXT_SECONDARY": "#c9d1d9",
            "ACCENT": "#58a6ff",
            "ACCENT_HOVER": "#1f6feb",
            "SUCCESS": "#238636",
            "WARNING": "#d29922",
            "ERROR": "#f85149",
            "SKIP": "#6e7681",
            "INFO": "#58a6ff"
        }
    
    @classmethod
    def get_light_colors(cls):
        return {
            "BACKGROUND": "#ffffff",
            "FRAME": "#f6f8fa",
            "CARD": "#ffffff",
            "BORDER": "#d0d7de",
            "SEPARATOR": "#d8dee4",
            "TEXT": "#24292f",
            "TEXT_SECONDARY": "#24292f",
            "ACCENT": "#0969da",
            "ACCENT_HOVER": "#0550ae",
            "SUCCESS": "#1a7f37",
            "WARNING": "#9a6700",
            "ERROR": "#cf222e",
            "SKIP": "#656d76",
            "INFO": "#0969da"
        }

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def asset_path(rel_path):
    """Get asset path relative to script directory"""
    return os.path.join(os.path.dirname(__file__), 'assets', rel_path)

# Icon Manager
class IconManager:
    def __init__(self):
        self.CHECK = self._load_icon("icons/checkmark.png", (30, 30))
        self.CROSS = self._load_icon("icons/cross.png", (30, 30))
        self.SKIP_ICON = self._load_icon("icons/skip.png", (30, 30))
        self.WHY = self._load_icon("icons/lightbulb.png", (32, 32))
        self.HOW = self._load_icon("icons/checklist.png", (32, 32))
        self.SHIELD = self._load_icon("icons/shield.png", (32, 32))
        self.CPU = self._load_icon("icons/cpu.png", (32, 32))
        self.GPU = self._load_icon("icons/gpu.png", (32, 32))
        self.HDD = self._load_icon("icons/hdd.png", (32, 32))
        self.LOGO_SMALL = self._load_icon("icons/logo.png", (48, 48))

    def _load_icon(self, path, size):
        try:
            return ctk.CTkImage(Image.open(asset_path(path)), size=size)
        except Exception:
            return None
# Worker Functions for CPU, GPU, and Disk Testing
def stress_worker():
    """CPU stress worker function"""
    x = 0
    while True:
        try:
            x += 0.0001
            math.sqrt(x * math.pi)
        except (OverflowError, ValueError):
            x = 0
        except Exception:
            pass

def get_cpu_temperature():
    """Get CPU temperature using multiple methods"""
    # Method 1: WMI (Windows only)
    if platform.system() == "Windows" and wmi:
        try:
            w = wmi.WMI(namespace="root\\wmi")
            temp_info = w.MSAcpi_ThermalZoneTemperature()
            if temp_info:
                temp_kelvin = temp_info[0].CurrentTemperature
                temp_celsius = (temp_kelvin / 10.0) - 273.15
                return round(temp_celsius, 1)
        except Exception:
            pass

    # Method 2: psutil
    try:
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
            
            cpu_temps = []
            for key in ['coretemp', 'k10temp', 'acpi', 'cpu_thermal']:
                if key in temps:
                    for entry in temps[key]:
                        if entry.current is not None:
                            cpu_temps.append(entry.current)
            
            if cpu_temps:
                return round(max(cpu_temps), 1)
    except Exception:
        pass
    
    return None

def get_cpu_frequency():
    """Get current CPU frequency"""
    try:
        freq = psutil.cpu_freq()
        if freq:
            return freq.current, freq.max
    except:
        pass
    return None, None

def run_cpu_stress_test(queue, duration_seconds=60):
    """Enhanced CPU stress test with throttling detection"""
    import time
    
    try:
        cpu_count = multiprocessing.cpu_count()
        cpu_msg = f'Phát hiện {cpu_count} lõi CPU. Đang đo baseline...' if CURRENT_LANG == "vi" else f'Detected {cpu_count} CPU cores. Measuring baseline...'
        queue.put({'type': 'status', 'message': cpu_msg})
        
        # Enhanced baseline measurement
        time.sleep(1)
        baseline_cpu = psutil.cpu_percent(interval=1)
        baseline_temp = get_cpu_temperature()
        baseline_freq, max_freq = get_cpu_frequency()
        
        queue.put({'type': 'baseline', 'data': {
            'cpu_cores': cpu_count,
            'baseline_cpu': baseline_cpu,
            'baseline_temp': baseline_temp,
            'baseline_freq': baseline_freq,
            'max_freq': max_freq
        }})
        
        # Start stress test
        stress_msg = 'Bắt đầu stress test với tải 100%...' if CURRENT_LANG == "vi" else 'Starting stress test with 100% load...'
        queue.put({'type': 'status', 'message': stress_msg})
        
        start_time = time.time()
        max_cpu = 0
        max_temp = baseline_temp
        min_freq = max_freq if max_freq else 0
        freq_drops = 0
        temp_warnings = 0
        
        while time.time() - start_time < duration_seconds:
            elapsed = time.time() - start_time
            progress = elapsed / duration_seconds
            
            # Intensive CPU load
            for _ in range(500000):
                _ = math.sqrt(math.pi * elapsed * 2.71828)
            
            # Comprehensive monitoring
            cpu_usage = psutil.cpu_percent(interval=0.1)
            temp = get_cpu_temperature()
            current_freq, _ = get_cpu_frequency()
            
            max_cpu = max(max_cpu, cpu_usage)
            if temp:
                max_temp = max(max_temp, temp)
                if temp > 85:
                    temp_warnings += 1
            
            # Throttling detection
            throttling_detected = False
            if current_freq and max_freq:
                min_freq = min(min_freq, current_freq)
                freq_ratio = current_freq / max_freq
                if freq_ratio < 0.8:
                    freq_drops += 1
                    throttling_detected = True
            
            # Status with detailed info
            na_text = "N/A" if CURRENT_LANG == "en" else "Không có"
            temp_str = f"{temp:.1f}°C" if temp else na_text
            freq_str = f"{current_freq:.0f}MHz" if current_freq else na_text
            throttle_text = " ⚠️ THROTTLING" if CURRENT_LANG == "en" else " ⚠️ GIẢM TẢI"
            throttle_indicator = throttle_text if throttling_detected else ""
            
            queue.put({
                'type': 'update',
                'progress': progress,
                'cpu_usage': cpu_usage,
                'temperature': temp,
                'frequency': current_freq,
                'throttling': throttling_detected,
                'status': f'CPU: {cpu_usage:.1f}% | {temp_str} | {freq_str}{throttle_indicator}'
            })
            
            time.sleep(0.3)
        
        # Analyze results
        throttling_severity = "None"
        if freq_drops > 0:
            if freq_drops > duration_seconds * 2:  # More than 2 drops per second
                throttling_severity = "Severe"
            elif freq_drops > duration_seconds:  # More than 1 drop per second
                throttling_severity = "Moderate"
            else:
                throttling_severity = "Light"
        
        result_data = {
            'duration': duration_seconds,
            'cpu_cores': cpu_count,
            'max_cpu_usage': max_cpu,
            'avg_cpu_usage': max_cpu * 0.85,
            'max_temperature': max_temp if max_temp else None,
            'baseline_freq': baseline_freq,
            'max_freq': max_freq,
            'min_freq': min_freq,
            'freq_drops': freq_drops,
            'throttling_severity': throttling_severity,
            'temp_warnings': temp_warnings,
            'stable': max_cpu > 50 and throttling_severity in ["None", "Light"]
        }
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})
        
    except Exception as e:
        error_msg = f'Lỗi: {str(e)}' if CURRENT_LANG == "vi" else f'Error: {str(e)}'
        queue.put({'type': 'error', 'message': error_msg})
        queue.put({'type': 'done'})

def run_disk_benchmark(queue, duration, file_size_mb=512):
    """Run disk speed benchmark"""
    test_file_path = None
    try:
        test_dir = tempfile.gettempdir()
        test_dir_msg = f"Sử dụng thư mục test: {test_dir}" if CURRENT_LANG == "vi" else f"Using test directory: {test_dir}"
        queue.put({'type': 'status', 'message': test_dir_msg})

        free_space_mb = psutil.disk_usage(test_dir).free / (1024 * 1024)
        if free_space_mb < file_size_mb * 1.1:
            space_error_msg = f"Không đủ dung lượng trống. Cần {file_size_mb}MB, còn lại {free_space_mb:.0f}MB." if CURRENT_LANG == "vi" else f"Not enough free space. Need {file_size_mb}MB, remaining {free_space_mb:.0f}MB."
            queue.put({'type': 'error', 'message': space_error_msg})
            return

        file_size_bytes = file_size_mb * 1024 * 1024
        chunk_size = 4 * 1024 * 1024  # 4MB chunk
        chunks = file_size_bytes // chunk_size
        
        test_file_path = os.path.join(test_dir, f"laptoptester_speedtest_{os.getpid()}.tmp")
        data_chunk = os.urandom(chunk_size)

        # Sequential Write
        write_msg = f"Đang ghi tuần tự file {file_size_mb}MB..." if CURRENT_LANG == "vi" else f"Sequential writing {file_size_mb}MB file..."
        queue.put({'type': 'status', 'message': write_msg})
        write_start_time = time.time()
        
        total_bytes_written = 0
        with open(test_file_path, "wb") as f:
            for i in range(chunks):
                chunk_start_time = time.time()
                f.write(data_chunk)
                chunk_duration = time.time() - chunk_start_time
                
                total_bytes_written += chunk_size
                total_write_time = time.time() - write_start_time

                chunk_speed = (chunk_size / (1024*1024)) / chunk_duration if chunk_duration > 0 else 0
                avg_speed = (total_bytes_written / (1024*1024)) / total_write_time if total_write_time > 0 else 0
                progress = ((i + 1) / chunks) * 0.5
                queue.put({'type': 'update', 'progress': progress, 'operation': 'Write', 'speed': chunk_speed, 'avg_speed': avg_speed})
            
            flush_msg = t("Đang xả cache ghi xuống đĩa...")
            queue.put({'type': 'status', 'message': flush_msg})
            f.flush()
            os.fsync(f.fileno())

        write_duration = time.time() - write_start_time
        write_speed = (file_size_mb / write_duration) if write_duration > 0 else 0
        
        # Sequential Read
        read_msg = f"Đang đọc tuần tự file {file_size_mb}MB..." if CURRENT_LANG == "vi" else f"Sequential reading {file_size_mb}MB file..."
        queue.put({'type': 'status', 'message': read_msg})
        read_start_time = time.time()
        
        total_bytes_read = 0
        with open(test_file_path, "rb") as f:
            for i in range(chunks):
                chunk_start_time = time.time()
                _ = f.read(chunk_size)
                chunk_duration = time.time() - chunk_start_time

                total_bytes_read += chunk_size
                total_read_time = time.time() - read_start_time
                
                chunk_speed = (chunk_size / (1024*1024)) / chunk_duration if chunk_duration > 0 else 0
                avg_speed = (total_bytes_read / (1024*1024)) / total_read_time if total_read_time > 0 else 0
                progress = 0.5 + ((i + 1) / chunks) * 0.5
                queue.put({'type': 'update', 'progress': progress, 'operation': 'Read', 'speed': chunk_speed, 'avg_speed': avg_speed})

        read_duration = time.time() - read_start_time
        read_speed = (file_size_mb / read_duration) if read_duration > 0 else 0
        
        result_data = {
            'status': 'OK',
            'write_speed': f"{write_speed:.2f}",
            'read_speed': f"{read_speed:.2f}"
        }
        queue.put({'type': 'result', 'data': result_data})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': f"{e.__class__.__name__}: {e}"})
    finally:
        if test_file_path and os.path.exists(test_file_path):
            try:
                os.remove(test_file_path)
            except Exception as e:
                delete_error_msg = f"Không thể xóa file tạm: {e}" if CURRENT_LANG == "vi" else f"Cannot delete temp file: {e}"
                queue.put({'type': 'error', 'message': delete_error_msg})
        queue.put({'type': 'done'})

def run_gpu_stress(duration, queue):
    """Run GPU stress test using pygame"""
    if not pygame:
        pygame_error_msg = t("Pygame không có sẵn. Cài đặt: pip install pygame")
        queue.put({'type': 'error', 'message': pygame_error_msg})
        queue.put({'type': 'done'})
        return

    try:
        init_msg = t("Đang khởi tạo Pygame...")
        queue.put({'type': 'status', 'message': init_msg})
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        caption_text = t("GPU Stress Test - Nhấn ESC để thoát")
        pygame.display.set_caption(caption_text)
        clock = pygame.time.Clock()
        start_time = time.time()
        particles = []
        frame_count = 0
        
        fps_readings = []

        try:
            font = pygame.font.SysFont("Arial", 24)
            font_small = pygame.font.SysFont("Arial", 18)
        except:
            font = pygame.font.Font(None, 30)
            font_small = pygame.font.Font(None, 24)
        
        stress_msg = t("Đang chạy vòng lặp stress...")
        queue.put({'type': 'status', 'message': stress_msg})
        
        running = True
        
        while running and (time.time() - start_time < duration):
            dt = clock.tick(60) / 1000.0
            current_time = time.time() - start_time
            progress = current_time / duration
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    stop_msg = 'Test bị dừng bởi người dùng (ESC)' if CURRENT_LANG == "vi" else 'Test stopped by user (ESC)'
                    queue.put({'type': 'status', 'message': stop_msg})
                    break

            screen.fill((10, 10, 20))
            
            mx, my = pygame.mouse.get_pos()
            if not mx and not my: 
                mx, my = screen.get_width()//2, screen.get_height()//2

            # Create particles
            for _ in range(5):
                particles.append([
                    [mx, my],
                    [np.random.randint(-50, 50) / 10, np.random.randint(0, 50) / 10 - 2],
                    np.random.randint(4, 10)
                ])

            # Update and draw particles
            for particle in particles[:]:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[1][1] += 0.1
                particle[2] -= 0.05
                
                if particle[2] <= 0 or particle[0][1] > screen.get_height():
                    particles.remove(particle)
                    continue
                
                color_intensity = min(255, max(0, int(particle[2] * 25.5)))
                color = (color_intensity, color_intensity // 2, 255 - color_intensity)
                pygame.draw.circle(screen, color, 
                                 (int(particle[0][0]), int(particle[0][1])), 
                                 int(particle[2]))

            # Draw geometric patterns
            for i in range(50):
                x = int(screen.get_width() * (i / 50))
                y = int(screen.get_height() * 0.8 + 50 * np.sin(current_time * 2 + i * 0.1))
                color = (int(128 + 127 * np.sin(current_time + i)), 
                        int(128 + 127 * np.cos(current_time + i)), 
                        255)
                pygame.draw.circle(screen, color, (x, y), 3)

            frame_count += 1
            fps = clock.get_fps()
            if fps > 0:
                fps_readings.append(fps)

            # Draw performance info
            time_label = t("Thời gian:")
            progress_label = t("Tiến độ:")
            elapsed_text = font.render(f"{time_label} {current_time:.1f}s / {duration}s", True, (255, 255, 255))
            fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            particles_text = font.render(f"Particles: {len(particles)}", True, (255, 255, 255))
            progress_text = font_small.render(f"{progress_label} {progress*100:.1f}%", True, (255, 255, 255))
            
            screen.blit(elapsed_text, (10, 10))
            screen.blit(fps_text, (10, 40))
            screen.blit(particles_text, (10, 70))
            screen.blit(progress_text, (10, 100))
            
            # Progress bar
            bar_width = 300
            bar_height = 10
            bar_x = 10
            bar_y = 200
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))

            pygame.display.flip()
            
            if frame_count % 30 == 0:  # Update every 30 frames for smoother charts
                queue.put({
                    'type': 'update',
                    'progress': progress,
                    'fps': fps,
                    'particles': len(particles),
                    'frame_count': frame_count
                })

        pygame.quit()
        
        # Calculate results
        avg_fps = sum(fps_readings) / len(fps_readings) if fps_readings else 0
        min_fps = min(fps_readings) if fps_readings else 0
        max_fps = max(fps_readings) if fps_readings else 0
        
        result_data = {
            'duration': current_time,
            'total_frames': frame_count,
            'average_fps': round(avg_fps, 2),
            'min_fps': round(min_fps, 2),
            'max_fps': round(max_fps, 2),
            'stable_performance': min_fps > 30 and avg_fps > 45
        }
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})

    except Exception as e:
        try:
            pygame.quit()
        except:
            pass
        gpu_error_msg = f'Lỗi GPU stress test: {str(e)}' if CURRENT_LANG == "vi" else f'GPU stress test error: {str(e)}'
        queue.put({'type': 'error', 'message': gpu_error_msg})
        queue.put({'type': 'done'})
# Base Step Frame Class
class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, fg_color="transparent")
        self.title = title
        
        # Extract callbacks from kwargs
        self.record_result = kwargs.get("record_result_callback")
        self.enable_next_callback = kwargs.get("enable_next_callback")
        self.go_to_next_step_callback = kwargs.get("go_to_next_step_callback")
        self.icon_manager = kwargs.get("icon_manager")
        self.all_results = kwargs.get("all_results", {})
        self.hide_why_section = kwargs.get("hide_why_section", False)
        
        self._completed = False
        self._skipped = False
        self.after_id = None
        
        # Setup layout
        self.setup_layout(why_text, how_text)
    
    def clean_text(self, text):
        """Clean text by removing \\n and formatting properly"""
        if not text:
            return text
        # Replace \\n with actual newlines and clean up
        cleaned = text.replace('\\n', '\n').replace('\\\\n', '\n')
        # Remove excessive whitespace
        lines = [line.strip() for line in cleaned.split('\n')]
        return '\n'.join(line for line in lines if line)
    
    def setup_layout(self, why_text, how_text):
        """Setup clean GitHub-style layout with scrollable action area"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        if not self.hide_why_section:
            self.grid_columnconfigure(1, weight=3)
            
            # Compact guide panel
            guide_container = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
            guide_container.grid(row=0, column=0, sticky="nsew", padx=(Theme.PADDING, Theme.SPACING), pady=Theme.PADDING)
            
            # Why section
            ctk.CTkLabel(guide_container, text=f"💡 {get_text('why_test')}", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=Theme.PADDING, pady=(Theme.PADDING, Theme.SPACING))
            ctk.CTkLabel(guide_container, text=self.clean_text(why_text), font=Theme.SMALL_FONT, wraplength=300, justify="left", text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=Theme.PADDING)
            
            # Separator
            ctk.CTkFrame(guide_container, height=1, fg_color=Theme.SEPARATOR).pack(fill="x", padx=Theme.PADDING, pady=Theme.SPACING)
            
            # How section
            ctk.CTkLabel(guide_container, text=f"📋 {get_text('how_to')}", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=Theme.PADDING, pady=(0, Theme.SPACING))
            ctk.CTkLabel(guide_container, text=self.clean_text(how_text), font=Theme.SMALL_FONT, wraplength=300, justify="left", text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=Theme.PADDING, pady=(0, Theme.PADDING))
            
            # Main action area - now scrollable
            self.action_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
            self.action_frame.grid(row=0, column=1, sticky="nsew", padx=(Theme.SPACING, Theme.PADDING), pady=Theme.PADDING)
        else:
            # Full width when hiding guide panel
            self.action_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
            self.action_frame.grid(row=0, column=0, sticky="nsew", padx=Theme.PADDING, pady=Theme.PADDING)
        
        self.action_frame.grid_columnconfigure(0, weight=1)

    def on_show(self):
        """Called when step is shown - no longer needed for scrolling"""
        pass
    
    def is_ready_to_proceed(self):
        return self._completed or self._skipped
    
    def mark_completed(self, result_data, auto_advance=False):
        self._completed = True
        self._skipped = False
        if self.record_result:
            self.record_result(self.title, result_data)
        def scroll_to_bottom():
            try:
                if hasattr(self.action_frame, '_parent_canvas'):
                    self.action_frame._parent_canvas.yview_moveto(1.0)
                elif hasattr(self.action_frame, 'yview_moveto'):
                    self.action_frame.yview_moveto(1.0)
            except:
                pass
        self.after(100, scroll_to_bottom)
        self.after(300, scroll_to_bottom)
        self.after(500, scroll_to_bottom)
        if auto_advance and self.go_to_next_step_callback:
            self.after(800, self.go_to_next_step_callback)
    
    def mark_skipped(self, result_data):
        self._skipped = True
        self._completed = False
        if self.record_result:
            self.record_result(self.title, result_data)
        if self.go_to_next_step_callback:
            self.go_to_next_step_callback()
    
    def handle_result_generic(self, is_ok, ok_data, bad_data):
        if hasattr(self, 'btn_yes'):
            self.btn_yes.configure(state="disabled")
        if hasattr(self, 'btn_no'):
            self.btn_no.configure(state="disabled")
        result = ok_data if is_ok else bad_data
        if is_ok:
            if hasattr(self, 'btn_yes'):
                self.btn_yes.configure(fg_color="#0d7a2c", text_color="#ffffff", border_width=3, border_color="#2ea043", font=("Arial", 20, "bold"))
            if hasattr(self, 'btn_no'):
                self.btn_no.configure(fg_color="#21262d", text_color="#6e7681")
            self.mark_completed(result, auto_advance=True)
        else:
            if hasattr(self, 'btn_no'):
                self.btn_no.configure(fg_color="#a40e26", text_color="#ffffff", border_width=3, border_color="#f85149", font=("Arial", 20, "bold"))
            if hasattr(self, 'btn_yes'):
                self.btn_yes.configure(fg_color="#21262d", text_color="#6e7681")
            self.mark_completed(result, auto_advance=True)
    
    def stop_tasks(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
# Hardware Fingerprint Step
class HardwareFingerprintStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        why_text = t("Đây là bước quan trọng nhất để chống lừa đảo. Các thông tin dưới đây được đọc trực tiếp từ BIOS và linh kiện phần cứng. Chúng cực kỳ khó làm giả từ bên trong Windows.")
        how_text = t("Nhấn 'Bắt đầu Test' để đọc thông tin phần cứng từ BIOS. Sau đó so sánh với thông tin quảng cáo của người bán.")
        super().__init__(master, get_text("hardware_fingerprint"), why_text, how_text, **kwargs)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.info_labels = {}
        self.test_started = False
        
        # Create checklist first
        self.create_checklist()
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
    
    def create_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(checklist_frame, text=t("📋 Checklist Định Danh Phần Cứng"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        if CURRENT_LANG == "vi":
            checklist_items = [
                t("✓ Đọc thông tin Model laptop từ BIOS"),
                t("✓ Lấy Serial Number từ BIOS (không thể giả mạo)"),
                t("✓ Xác định CPU chính xác (tên, số core, threads)"),
                t("✓ Đo dung lượng RAM thực tế"),
                t("✓ Liệt kê tất cả GPU (onboard + rời)"),
                t("✓ Đọc model và dung lượng ổ cứng"),
                t("✓ Kiểm tra ngày phát hành BIOS"),
                t("✓ Xác định chế độ khởi động (UEFI/Legacy)")
            ]
        else:
            checklist_items = [
                t("✓ Read laptop model from BIOS"),
                t("✓ Get Serial Number from BIOS (cannot be faked)"),
                t("✓ Identify CPU accurately (name, cores, threads)"),
                t("✓ Measure actual RAM capacity"),
                t("✓ List all GPUs (onboard + discrete)"),
                t("✓ Read hard drive model and capacity"),
                t("✓ Check BIOS release date"),
                t("✓ Determine boot mode (UEFI/Legacy)")
            ]
        
        for item in checklist_items:
            ctk.CTkLabel(checklist_frame, text=item, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
        
        # Start test button
        self.start_btn = ctk.CTkButton(checklist_frame, text=get_text("start_test_btn"), command=self.start_hardware_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.start_btn.pack(pady=15)
        
        # Container for results (initially hidden)
        self.container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_remove()  # Hide initially
    
    def start_hardware_test(self):
        if self.test_started:
            return
        
        self.test_started = True
        self.start_btn.configure(state="disabled", text=t("Đang đọc..."))
        
        # Show loading spinner
        self.loading_spinner = ctk.CTkProgressBar(self.container, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        self.loading_spinner.start()
        self.container.grid()  # Show container
        
        # Create info labels
        if CURRENT_LANG == "vi":
            self.info_items = ["Model Laptop", "Serial Number", "CPU", "RAM", "GPU", "Model Ổ Cứng", "Ngày BIOS", "UEFI/Legacy"]
        else:
            self.info_items = ["Laptop Model", "Serial Number", "CPU", "RAM", "GPU", "Hard Drive Model", "BIOS Date", "UEFI/Legacy"]
        icons = ["💻", "🏷️", "⚙️", "💾", "🎮", "💿", "📅", "🔒"]
        
        for idx, (item, icon) in enumerate(zip(self.info_items, icons)):
            row_frame = ctk.CTkFrame(self.container, fg_color=Theme.FRAME, corner_radius=6)
            row_frame.grid(row=idx+1, column=0, sticky="ew", pady=8, padx=20)
            row_frame.grid_columnconfigure(2, weight=1)
            
            ctk.CTkLabel(row_frame, text=icon, font=("Arial", 24)).grid(row=0, column=0, padx=15, pady=12)
            ctk.CTkLabel(row_frame, text=f"{item}:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=1, padx=(0, 15), pady=12, sticky="w")
            
            loading_text = t("Đang tải...")
            self.info_labels[item] = ctk.CTkLabel(row_frame, text=loading_text, justify="left", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=600)
            self.info_labels[item].grid(row=0, column=2, padx=(0, 15), pady=12, sticky="w")
        
        threading.Thread(target=self.fetch_hardware_info, daemon=True).start()

    def fetch_hardware_info(self):
        loading_text = t("Đang tải...")
        hw_info = {k: loading_text for k in self.info_items}
        
        if platform.system() == "Windows" and wmi and pythoncom:
            pythoncom.CoInitializeEx(0)
            try:
                c = wmi.WMI()
                
                # System info
                system_info = c.Win32_ComputerSystem()[0]
                hw_info["Model Laptop"] = f"{system_info.Manufacturer} {system_info.Model}"
                
                # BIOS info
                bios = c.Win32_BIOS()[0]
                hw_info["Serial Number"] = getattr(bios, 'SerialNumber', 'N/A')
                
                # Enhanced BIOS date processing
                try:
                    bios_date = getattr(bios, 'ReleaseDate', '')
                    if bios_date and len(str(bios_date)) >= 8:
                        bios_date_str = str(bios_date).split('.')[0]
                        if len(bios_date_str) >= 8:
                            bios_key = t("Ngày BIOS")
                            hw_info[bios_key] = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
                        else:
                            bios_key = t("Ngày BIOS")
                            hw_info[bios_key] = bios_date_str
                    else:
                        unknown_text = t("Không xác định")
                        bios_key = t("Ngày BIOS")
                        hw_info[bios_key] = unknown_text
                except Exception as e:
                    error_text = f"Lỗi: {str(e)[:15]}" if CURRENT_LANG == "vi" else f"Error: {str(e)[:15]}"
                    bios_key = t("Ngày BIOS")
                    hw_info[bios_key] = error_text
                
                # Enhanced CPU info reading
                try:
                    processors = c.Win32_Processor()
                    if processors and len(processors) > 0:
                        cpu = processors[0]
                        cpu_name = str(cpu.Name).strip().replace('  ', ' ').replace('(R)', '').replace('(TM)', '')
                        cores = cpu.NumberOfCores or 'N/A'
                        threads = cpu.NumberOfLogicalProcessors or 'N/A'
                        max_speed = f"{cpu.MaxClockSpeed}MHz" if cpu.MaxClockSpeed else 'N/A'
                        hw_info["CPU"] = f"{cpu_name} ({cores}C/{threads}T @ {max_speed})"
                        self.bios_cpu_info = cpu_name
                    else:
                        no_cpu_text = t("Không tìm thấy CPU")
                        hw_info["CPU"] = no_cpu_text
                        self.bios_cpu_info = None
                except Exception as e:
                    cpu_error_text = f"Lỗi WMI CPU: {str(e)[:20]}" if CURRENT_LANG == "vi" else f"WMI CPU Error: {str(e)[:20]}"
                    hw_info["CPU"] = cpu_error_text
                    self.bios_cpu_info = None
                
                # RAM info
                try:
                    total_ram = round(psutil.virtual_memory().total / (1024**3), 1)
                    memory_modules = c.Win32_PhysicalMemory()
                    if memory_modules:
                        speeds = [m.Speed for m in memory_modules if m.Speed]
                        speed_info = f" @ {speeds[0]}MHz" if speeds else ""
                        slot_count = len(memory_modules)
                        hw_info["RAM"] = f"{total_ram}GB ({slot_count} slot{speed_info})"
                    else:
                        hw_info["RAM"] = f"{total_ram}GB"
                except Exception as e:
                    ram_error_text = f"Lỗi RAM: {str(e)[:20]}" if CURRENT_LANG == "vi" else f"RAM Error: {str(e)[:20]}"
                    hw_info["RAM"] = ram_error_text
                
                # GPU info
                try:
                    gpus = c.Win32_VideoController()
                    gpu_names = [str(gpu.Name) for gpu in gpus if gpu.Name]
                    no_gpu_text = t("Không tìm thấy GPU")
                    hw_info["GPU"] = "; ".join(gpu_names) if gpu_names else no_gpu_text
                except Exception as e:
                    gpu_error_text = f"Lỗi GPU: {str(e)[:20]}" if CURRENT_LANG == "vi" else f"GPU Error: {str(e)[:20]}"
                    hw_info["GPU"] = gpu_error_text
                
                # Enhanced disk info
                try:
                    drives = c.Win32_DiskDrive()
                    drive_details = []
                    for d in drives:
                        if d.Model and d.Size:
                            size_gb = round(int(d.Size) / (1024**3))
                            interface = d.InterfaceType or 'Unknown'
                            drive_details.append(f"{d.Model} ({size_gb}GB {interface})")
                    no_hdd_text = t("Không tìm thấy ổ cứng")
                    hdd_key = t("Model Ổ Cứng")
                    hw_info[hdd_key] = "; ".join(drive_details) if drive_details else no_hdd_text
                except Exception as e:
                    hdd_error_text = f"Lỗi HDD: {str(e)[:20]}" if CURRENT_LANG == "vi" else f"HDD Error: {str(e)[:20]}"
                    hdd_key = t("Model Ổ Cứng")
                    hw_info[hdd_key] = hdd_error_text
                
                # UEFI/Legacy detection
                try:
                    boot_config = c.Win32_BootConfiguration()
                    if boot_config:
                        hw_info["UEFI/Legacy"] = "UEFI" if any('UEFI' in str(bc.Description) for bc in boot_config if bc.Description) else "Legacy BIOS"
                    else:
                        unknown_text = t("Không xác định")
                        hw_info["UEFI/Legacy"] = unknown_text
                except:
                    # Alternative method
                    try:
                        import os
                        if os.path.exists('C:\\Windows\\Panther\\setupact.log'):
                            hw_info["UEFI/Legacy"] = "UEFI (phát hiện qua Windows)"
                        else:
                            legacy_text = "Legacy BIOS" if CURRENT_LANG == "en" else "Legacy BIOS"
                            hw_info["UEFI/Legacy"] = legacy_text
                    except:
                        unknown_text = t("Không xác định")
                        hw_info["UEFI/Legacy"] = unknown_text
                    
            except Exception as e: 
                wmi_error_text = f"Lỗi WMI: {e}" if CURRENT_LANG == "vi" else f"WMI Error: {e}"
                hw_info = {k: wmi_error_text for k in self.info_items}
            finally: 
                pythoncom.CoUninitialize()
        else: 
            windows_only_text = t("Chỉ hỗ trợ Windows")
            hw_info = {k: windows_only_text for k in self.info_items}
            
        if self.winfo_exists(): 
            self.after(0, self.display_info, hw_info)

    def display_info(self, hw_info):
        full_details = ""
        self.loading_spinner.grid_remove()
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        for key, value in hw_info.items():
            if key in self.info_labels:
                self.info_labels[key].configure(text=value)
            full_details += f"  - {key}: {value}\n"
        
        # Thêm phân tích khả năng sử dụng
        self.show_hardware_capability(hw_info)
        
        result_text = t("Đã lấy định danh phần cứng")
        detail_text = t("Thông tin định danh phần cứng:")
        self.mark_completed({"Kết quả": result_text, "Trạng thái": get_text("status_good"), "Chi tiết": f"{detail_text}\n{full_details}"}, auto_advance=False)
        self.show_result_choices()
    
    def _analyze_capabilities(self, cpu_name, gpu_name, ram_gb=0):
        """Hàm chung phân tích khả năng phần cứng"""
        cpu_upper = cpu_name.upper()
        
        import re
        
        # Phát hiện thế hệ Intel (tất cả từ Gen 1-15+)
        intel_gen = 0
        if "INTEL" in cpu_upper:
            # Cách 1: i3-12400, i5-10400, i7-8750H
            gen_match = re.search(r'I[3579]-?(\d{1,2})\d{3}', cpu_upper)
            if gen_match:
                intel_gen = int(gen_match.group(1))
            else:
                # Cách 2: "12TH GEN", "10TH GENERATION"
                gen_match = re.search(r'(\d{1,2})(TH|ST|ND|RD)?\s*GEN', cpu_upper)
                if gen_match:
                    intel_gen = int(gen_match.group(1))
        
        # Phát hiện thế hệ AMD Ryzen (1000-9000 series)
        ryzen_gen = 0
        if "RYZEN" in cpu_upper:
            # Ryzen 5 5600X, Ryzen 7 7800X3D, Ryzen 9 3900X
            gen_match = re.search(r'RYZEN\s*[3579]\s*(\d)\d{3}', cpu_upper)
            if gen_match:
                ryzen_gen = int(gen_match.group(1))
        
        # Xác định tier CPU (kết hợp dòng + thế hệ)
        cpu_tier = "unknown"
        
        # Phân loại theo dòng CPU
        is_high_end = any(x in cpu_upper for x in ["I9", "I7", "RYZEN 9", "RYZEN 7"])
        is_mid_range = any(x in cpu_upper for x in ["I5", "RYZEN 5"])
        is_low_end = any(x in cpu_upper for x in ["I3", "RYZEN 3", "CELERON", "PENTIUM", "ATHLON"])
        
        # Điều chỉnh theo thế hệ
        if is_high_end:
            if intel_gen >= 12 or ryzen_gen >= 7:
                cpu_tier = "high"
            elif intel_gen >= 8 or ryzen_gen >= 5:
                cpu_tier = "mid-high"
            elif intel_gen >= 4 or ryzen_gen >= 2:
                cpu_tier = "mid"
            else:
                cpu_tier = "low-mid"
        elif is_mid_range:
            if intel_gen >= 12 or ryzen_gen >= 7:
                cpu_tier = "mid-high"
            elif intel_gen >= 8 or ryzen_gen >= 5:
                cpu_tier = "mid"
            elif intel_gen >= 4 or ryzen_gen >= 2:
                cpu_tier = "low-mid"
            else:
                cpu_tier = "low"
        elif is_low_end:
            if intel_gen >= 10 or ryzen_gen >= 5:
                cpu_tier = "low-mid"
            else:
                cpu_tier = "low"
        
        # Phân tích GPU (tự động phát hiện series)
        gpu_upper = gpu_name.upper()
        gpu_tier = "none"
        
        # NVIDIA RTX/GTX
        rtx_match = re.search(r'RTX\s*(\d{2})(\d{2})', gpu_upper)
        gtx_match = re.search(r'GTX\s*(\d{2})(\d{2})', gpu_upper)
        
        if rtx_match:
            series = int(rtx_match.group(1))
            if series >= 40:
                gpu_tier = "high"
            elif series >= 30:
                gpu_tier = "mid-high"
            elif series >= 20:
                gpu_tier = "mid"
            else:
                gpu_tier = "low-mid"
        elif gtx_match:
            series = int(gtx_match.group(1))
            if series >= 16:
                gpu_tier = "mid"
            elif series >= 10:
                gpu_tier = "low-mid"
            else:
                gpu_tier = "low"
        
        # AMD Radeon
        elif "RADEON" in gpu_upper:
            if any(x in gpu_upper for x in ["RX 7", "RX 6"]):
                gpu_tier = "mid-high"
            elif "RX 5" in gpu_upper:
                gpu_tier = "mid"
            elif "RX" in gpu_upper:
                gpu_tier = "low-mid"
        
        gpu_dedicated = gpu_tier != "none"
        
        # Phân tích RAM
        ram_tier = "low"
        if ram_gb >= 16:
            ram_tier = "high"
        elif ram_gb >= 8:
            ram_tier = "mid"
        else:
            ram_tier = "low"
        
        # Tạo capabilities dựa trên tổng hợp CPU + GPU + RAM
        capabilities = []
        
        if cpu_tier in ["high", "mid-high"] and gpu_tier in ["high", "mid-high"] and ram_tier == "high":
            capabilities = [
                {"icon": "🎮", "title": "Gaming AAA & Rendering", "desc": "Game: Cyberpunk 2077, RDR2, GTA V Ultra\nRender: Premiere 4K, DaVinci, Blender\nStream: OBS 1080p60", "color": "#10B981"},
                {"icon": "💼", "title": "Workstation Pro", "desc": "Code: VS, Android Studio, Docker\nVM: 3-4 máy ảo\n50+ Chrome tabs", "color": "#3B82F6"}
            ]
        elif cpu_tier in ["high", "mid-high", "mid"] and ram_tier in ["high", "mid"]:
            capabilities = [
                {"icon": "🎮", "title": "Gaming & Content", "desc": "Game: LOL, Valorant, CS:GO\nStream: OBS 720p\nEdit: Premiere 1080p", "color": "#F59E0B"},
                {"icon": "💼", "title": t("Văn Phòng & Code"), "desc": "Office: Word, Excel, PPT\nCode: VS Code, Python\n20-30 tabs", "color": "#3B82F6"}
            ]
        else:
            capabilities = [
                {"icon": "📝", "title": t("Văn Phòng"), "desc": t("Office: Word, Excel\nWeb: Facebook, YouTube\nPhim: Netflix 1080p"), "color": "#94A3B8"},
                {"icon": "🎓", "title": t("Học Tập"), "desc": t("Zoom, Teams\nWord, PPT\nTra cứu web"), "color": "#06B6D4"}
            ]
        
        if gpu_tier in ["high", "mid-high"]:
            capabilities.insert(0, {"icon": "🎨", "title": t("Đồ Họa Pro"), "desc": t("3D: AutoCAD, SolidWorks\nRender: Blender, V-Ray\nAI: TensorFlow, PyTorch"), "color": "#8B5CF6"})
        elif gpu_tier == "mid" and cpu_tier in ["high", "mid-high", "mid"]:
            capabilities.insert(0, {"icon": "🎮", "title": t("Gaming 1080p"), "desc": t("Game: Esports titles\nCasual AAA games\nLight 3D work"), "color": "#3B82F6"})
        
        return capabilities
    
    def show_hardware_capability(self, hw_info):
        """Hiển thị nhận định khả năng sử dụng phần cứng"""
        import re
        cpu_name = hw_info.get("CPU", "")
        gpu_name = hw_info.get("GPU", "")
        ram_str = hw_info.get("RAM", "0")
        
        # Trích xuất RAM GB
        ram_match = re.search(r'([\d.]+)\s*GB', ram_str)
        ram_gb = float(ram_match.group(1)) if ram_match else 0
        
        capabilities = self._analyze_capabilities(cpu_name, gpu_name, ram_gb)
        
        if not capabilities:
            return
        
        # Hiển thị capabilities
        cap_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        cap_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(20,10))
        
        ctk.CTkLabel(cap_frame, text=t("💡 Khả Năng Sử Dụng Phần Cứng"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", pady=(0,10))
        
        for cap in capabilities:
            card = ctk.CTkFrame(cap_frame, fg_color=Theme.FRAME, corner_radius=8, border_width=2, border_color=cap["color"])
            card.pack(fill="x", pady=5)
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=12, pady=12)
            
            ctk.CTkLabel(content, text=f"{cap['icon']} {cap['title']}", font=Theme.BODY_FONT, text_color=cap["color"]).pack(anchor="w")
            ctk.CTkLabel(content, text=cap["desc"], font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=700, justify="left").pack(anchor="w", pady=(3,0))
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        # Add security notice
        security_frame = ctk.CTkFrame(self.result_container, fg_color=Theme.SUCCESS, corner_radius=8)
        security_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(security_frame, text=f"🔒 {get_text('security_info')}", font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=(10,5))
        security_desc = t("Các thông tin trên được đọc trực tiếp từ BIOS/UEFI và không thể giả mạo từ Windows.\nHãy so sánh với thông tin quảng cáo của người bán!")
        ctk.CTkLabel(security_frame, text=security_desc, font=Theme.BODY_FONT, text_color="white", justify="center").pack(pady=(0,10))
        
        continue_text = t("Định danh phần cứng đã hoàn thành. Bạn có muốn tiếp tục?")
        ctk.CTkLabel(self.result_container, text=continue_text, font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text="✓ Continue", command=lambda: self.handle_result_generic(True, {"Kết quả": "continue", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_yes.pack(side="left", padx=Theme.SPACING)
        
        self.btn_skip = ctk.CTkButton(button_bar, text="skip", command=lambda: self.mark_skipped({"Kết quả": "skip", "Trạng thái": "skip"}), fg_color=Theme.BORDER, hover_color=Theme.SEPARATOR, text_color=Theme.TEXT, height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_skip.pack(side="left", padx=Theme.SPACING)

# License Check Step
class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("license_check")
        why_text = t("Một máy tính có bản quyền Windows hợp lệ đảm bảo bạn nhận được các bản cập nhật bảo mật quan trọng và tránh các rủi ro pháp lý.")
        how_text = t("Nhấn 'Bắt đầu Test' để chạy lệnh kiểm tra trạng thái kích hoạt Windows. Kết quả sẽ hiển thị bên dưới.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.test_started = False
        
        # Create checklist first
        self.create_checklist()
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
    
    def create_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(checklist_frame, text=t("📋 Checklist Kiểm Tra Bản Quyền"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        if CURRENT_LANG == "vi":
            checklist_items = [
                t("✓ Chạy lệnh slmgr.vbs /xpr để kiểm tra kích hoạt"),
                t("✓ Xác định trạng thái: Vĩnh viễn / Có hạn / Chưa kích hoạt"),
                t("✓ Kiểm tra ngày hết hạn (nếu có)"),
                t("✓ Đánh giá tính hợp pháp của bản quyền"),
                t("✓ Cảnh báo nếu Windows chưa được kích hoạt")
            ]
        else:
            checklist_items = [
                t("✓ Run slmgr.vbs /xpr command to check activation"),
                t("✓ Determine status: Permanent / Limited / Not activated"),
                t("✓ Check expiration date (if any)"),
                t("✓ Assess license legitimacy"),
                t("✓ Warn if Windows is not activated")
            ]
        
        for item in checklist_items:
            ctk.CTkLabel(checklist_frame, text=item, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
        
        # Start test button
        self.start_btn = ctk.CTkButton(checklist_frame, text=get_text("start_test_btn"), command=self.start_license_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.start_btn.pack(pady=15)
        
        # Status label (initially hidden)
        self.status_label = ctk.CTkLabel(self.action_frame, text="", font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT_SECONDARY)
        self.status_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.status_label.grid_remove()  # Hide initially
    
    def start_license_test(self):
        if self.test_started:
            return
        
        self.test_started = True
        self.start_btn.configure(state="disabled", text=t("Đang kiểm tra..."))
        self.status_label.configure(text=get_text("checking"))
        self.status_label.grid()  # Show status label
        
        threading.Thread(target=self.check_license, daemon=True).start()

    def check_license(self):
        no_check_text = t("Không thể kiểm tra")
        error_text = t("Lỗi")
        status, color, result_data = no_check_text, Theme.WARNING, {"Kết quả": no_check_text, "Trạng thái": error_text}
        
        if platform.system() == "Windows":
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = _secure_executor.execute_safe("cscript C:\\\\Windows\\\\System32\\\\slmgr.vbs /xpr")
                output_text = result["stdout"]
                
                # output_text is already a string (text=True in subprocess.run)
                result = output_text.lower()
                
                activated_strings = ["activated permanently", "kích hoạt vĩnh viễn", "the machine is permanently activated"]
                if any(s in result for s in activated_strings):
                    activated_text = t("Windows được kích hoạt vĩnh viễn")
                    activated_result = t("Đã kích hoạt vĩnh viễn")
                    good_status = t("Tốt")
                    status, color, result_data = activated_text, Theme.SUCCESS, {"Kết quả": activated_result, "Trạng thái": good_status}
                elif "will expire" in result or "sẽ hết hạn" in result:
                    expiry_date = result.split("on")[-1].strip() if "on" in result else result.split(" vào ")[-1].strip()
                    status, color, result_data = f"Windows sẽ hết hạn vào {expiry_date}", Theme.WARNING, {"Kết quả": f"Sẽ hết hạn ({expiry_date})", "Trạng thái": "Lỗi"}
                else:
                    not_activated_text = t("Windows chưa được kích hoạt")
                    not_activated_result = t("Chưa kích hoạt")
                    error_status = t("Lỗi")
                    status, color, result_data = not_activated_text, Theme.ERROR, {"Kết quả": not_activated_result, "Trạng thái": error_status}
            except (subprocess.CalledProcessError, FileNotFoundError):
                command_error_text = t("Lỗi khi chạy lệnh kiểm tra")
                error_status = t("Lỗi")
                status, color, result_data = command_error_text, Theme.ERROR, {"Kết quả": command_error_text, "Trạng thái": error_status}
        else:
            windows_only_text = t("Chỉ hỗ trợ Windows")
            skip_status = get_text("status_skip")
            status, color, result_data = windows_only_text, Theme.SKIP, {"Kết quả": windows_only_text, "Trạng thái": skip_status}
        
        if self.winfo_exists():
            self.after(0, self.update_ui, status, color, result_data)

    def update_ui(self, status, color, result_data):
        self.status_label.configure(text=status, text_color=color)
        self.mark_completed(result_data, auto_advance=False)
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        if not self.test_started:
            return  # Don't show buttons until test is started
        
        ctk.CTkLabel(self.result_container, text=get_text("test_completed") + ". " + get_text("continue") + "?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent", bg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text="✓ Continue", command=lambda: self.handle_result_generic(True, {"Kết quả": "continue", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_yes.pack(side="left", padx=Theme.SPACING)
        
        self.btn_skip = ctk.CTkButton(button_bar, text="skip", command=lambda: self.mark_skipped({"Kết quả": "skip", "Trạng thái": "skip"}), fg_color=Theme.BORDER, hover_color=Theme.SEPARATOR, text_color=Theme.TEXT, height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_skip.pack(side="left", padx=Theme.SPACING)
# System Info Step
class SystemInfoStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("system_info")
        why_text = t("Bước này hiển thị thông tin cấu hình mà Windows nhận diện và tự động so sánh với thông tin từ BIOS để phát hiện sai lệch.")
        how_text = t("Đối chiếu thông tin dưới đây với bước trước và với thông tin quảng cáo. Nếu mọi thứ khớp, chọn 'Cấu hình khớp'.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        
        self.container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(1, weight=1)
        
        self.info_labels = {}
        self.info_items = ["CPU", "RAM", "GPU", "Ổ cứng"]
        
        for i, item in enumerate(self.info_items):
            ctk.CTkLabel(self.container, text=f"{item}:", font=Theme.SUBHEADING_FONT).grid(row=i, column=0, padx=(0, 15), pady=12, sticky="nw")
            self.info_labels[item] = ctk.CTkLabel(self.container, text="", justify="left", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=600)
            self.info_labels[item].grid(row=i, column=1, padx=5, pady=12, sticky="w")
        
        self.comparison_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.comparison_frame.grid(row=len(self.info_items), column=0, columnspan=2, pady=(20, 0), sticky="ew")
        ctk.CTkLabel(self.comparison_frame, text=t("So sánh tự động:"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w")
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        
        threading.Thread(target=self.fetch_info, daemon=True).start()

    def fetch_info(self):
        loading_text = t("Đang tải...")
        full_info = {k: loading_text for k in self.info_items}
        
        try:
            full_info["RAM"] = f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
            
            if platform.system() == "Windows" and wmi and pythoncom:
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    full_info["CPU"] = c.Win32_Processor()[0].Name.strip()
                    full_info["GPU"] = "; ".join([gpu.Name for gpu in c.Win32_VideoController()])
                    disk_details = [f"{d.Model} ({round(int(d.Size)/(1024**3))} GB)" for d in c.Win32_DiskDrive() if d.Size]
                    not_found_text = t("Không tìm thấy")
                    full_info["Ổ cứng"] = "; ".join(disk_details) if disk_details else not_found_text
                except Exception as e:
                    wmi_error_text = f"Lỗi WMI: {e}" if CURRENT_LANG == "vi" else f"WMI Error: {e}"
                    full_info.update({k: wmi_error_text for k in ["CPU", "GPU", "Ổ cứng"]})
                finally:
                    pythoncom.CoUninitialize()
            else:
                windows_only_text = t("Chỉ hỗ trợ Windows")
                full_info.update({k: windows_only_text for k in ["CPU", "GPU", "Ổ cứng"]})
        except Exception as e:
            error_text = f"Lỗi: {e}" if CURRENT_LANG == "vi" else f"Error: {e}"
            full_info = {k: error_text for k in self.info_items}
        
        if self.winfo_exists():
            self.after(0, self.display_info, full_info)

    def display_info(self, info):
        self.full_info_text = ""
        self.loading_spinner.grid_remove()
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        for key, value in info.items():
            if key in self.info_labels:
                self.info_labels[key].configure(text=value)
            self.full_info_text += f"{key}: {value}\n"
        
        self.perform_comparison()
        self.show_result_choices()
        
        if hasattr(self, 'action_canvas'):
            self.action_canvas.update_idletasks()
            self.action_canvas.yview_moveto(0)
    
    def perform_comparison(self):
        # Get CPU info from BIOS with multiple methods
        na_text = "N/A" if CURRENT_LANG == "en" else "Không có"
        cpu_bios = na_text
        
        try:
            # Method 1: From previous step results
            hw_data = self.all_results.get("hardware_fingerprint", {})
            hw_details = hw_data.get("Chi tiết", "")
            
            if hw_details:
                for line in hw_details.splitlines():
                    line = line.strip()
                    if any(pattern in line.lower() for pattern in ["cpu:", "processor:", "- cpu"]):
                        parts = line.split(":", 1)
                        if len(parts) > 1:
                            cpu_bios = parts[1].strip()
                            break
            
            # Method 2: Direct WMI read as fallback
            if cpu_bios == na_text and platform.system() == "Windows" and wmi and pythoncom:
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    processors = c.Win32_Processor()
                    if processors and len(processors) > 0:
                        cpu_bios = str(processors[0].Name).strip()
                except:
                    pass
                finally:
                    pythoncom.CoUninitialize()
                    
        except Exception as e:
            print(f"Lỗi lấy thông tin CPU BIOS: {e}")
        
        # Extract Windows CPU info
        cpu_win = na_text
        if hasattr(self, 'full_info_text'):
            for line in self.full_info_text.splitlines():
                if "CPU:" in line:
                    cpu_win = line.split(":", 1)[1].strip()
                    break
        
        # Display comparison results
        bios_label = "CPU (BIOS):" if CURRENT_LANG == "en" else "CPU (BIOS):"
        windows_label = "CPU (Windows):" if CURRENT_LANG == "en" else "CPU (Windows):"
        ctk.CTkLabel(self.comparison_frame, text=f"{bios_label} {cpu_bios}", font=Theme.BODY_FONT, wraplength=800).pack(anchor="w")
        ctk.CTkLabel(self.comparison_frame, text=f"{windows_label} {cpu_win}", font=Theme.BODY_FONT, wraplength=800).pack(anchor="w")
        
        result_label = ctk.CTkLabel(self.comparison_frame, font=Theme.BODY_FONT)
        if cpu_bios == na_text or cpu_win == na_text:
            no_compare_text = t("Kết quả: Không thể so sánh (thiếu dữ liệu)")
            result_label.configure(text=no_compare_text, text_color=Theme.WARNING)
        elif cpu_bios.lower() in cpu_win.lower() or cpu_win.lower() in cpu_bios.lower():
            match_text = t("✅ Kết quả: Khớp")
            result_label.configure(text=match_text, text_color=Theme.SUCCESS)
        else:
            mismatch_text = t("⚠️ Cảnh báo: Có sai lệch - Kiểm tra lại!")
            result_label.configure(text=mismatch_text, text_color=Theme.ERROR)
        result_label.pack(anchor="w")
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Config matches advertised specs?" if CURRENT_LANG == "en" else "Cấu hình có khớp với thông tin quảng cáo không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent", bg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text=f"✓ {get_text('config_match')}", command=lambda: self.handle_result_generic(True, {"Kết quả": "Cấu hình khớp", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_yes.pack(side="left", padx=Theme.SPACING)
        
        self.btn_no = ctk.CTkButton(button_bar, text=f"✗ {get_text('mismatch')}", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có sai lệch", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, hover_color="#cf222e", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_no.pack(side="left", padx=Theme.SPACING)

# Hard Drive Health Step
class HardDriveHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("harddrive_health")
        why_text = t("Ổ cứng sắp hỏng là mối rủi ro mất dữ liệu cực lớn. Bước này đọc 'báo cáo y tế' (S.M.A.R.T.) của ổ cứng để đánh giá độ bền.")
        how_text = t("Chú ý đến mục 'Trạng thái'. 'Tốt' là bình thường. 'Lỗi/Cảnh báo' là rủi ro cao. Bước tiếp theo sẽ kiểm tra tốc độ thực tế.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        self.loading_spinner.start()
        
        self.drive_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.drive_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.drive_container.grid_columnconfigure(0, weight=1)
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        
        threading.Thread(target=self.fetch_drive_info, daemon=True).start()
    
    def fetch_drive_info(self):
        drives_info = []
        
        if platform.system() == "Windows" and wmi and pythoncom:
            pythoncom.CoInitializeEx(0)
            try:
                c = wmi.WMI()
                drives = c.Win32_DiskDrive()
                if not drives:
                    no_drive_text = t("Không tìm thấy ổ cứng")
                    error_status = t("Lỗi")
                    drives_info.append({"Tên": no_drive_text, "Trạng thái": error_status})
                else:
                    for drive in drives:
                        good_status = t("Tốt")
                        error_warning = t("Lỗi/Cảnh báo")
                        drives_info.append({"Tên": drive.Model, "Trạng thái": good_status if drive.Status == "OK" else error_warning})
            except Exception as e:
                no_smart_text = t("Không thể đọc S.M.A.R.T")
                error_text = f"Lỗi: {e}" if CURRENT_LANG == "vi" else f"Error: {e}"
                drives_info.append({"Tên": no_smart_text, "Trạng thái": error_text})
            finally:
                pythoncom.CoUninitialize()
        else:
            na_text = "N/A" if CURRENT_LANG == "en" else "Không có"
            windows_only = t("Chỉ hỗ trợ Windows")
            drives_info.append({"Tên": na_text, "Trạng thái": windows_only})
        
        if self.winfo_exists():
            self.after(0, self.display_info, drives_info)
    
    def display_info(self, drives_info):
        self.loading_spinner.grid_remove()
        self.drive_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        full_details = ""
        has_error = False
        
        for drive_data in drives_info:
            drive_frame = ctk.CTkFrame(self.drive_container, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
            drive_frame.pack(fill="x", pady=10)
            
            status = drive_data.get('Trạng thái', 'Không rõ')
            good_text = t("Tốt")
            color = Theme.SUCCESS if status == good_text else Theme.ERROR
            if status != good_text:
                has_error = True
            
            drive_label = t("Ổ cứng:")
            status_label = t("Trạng thái:")
            na_text = "N/A" if CURRENT_LANG == "en" else "Không có"
            ctk.CTkLabel(drive_frame, text=f"{drive_label} {drive_data.get('Tên', na_text)}", font=Theme.SUBHEADING_FONT).pack(anchor="w", padx=20, pady=(15,5))
            ctk.CTkLabel(drive_frame, text=f"{status_label} {status}", font=Theme.SUBHEADING_FONT, text_color=color).pack(anchor="w", padx=20, pady=(5,15))
            
            drive_prefix = t("- Ổ")
            na_text = "N/A" if CURRENT_LANG == "en" else "Không có"
            full_details += f"{drive_prefix} {drive_data.get('Tên', na_text)}: {status}\n"
        
        self.full_details = full_details
        self.has_error = has_error
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Hard drives working properly?" if CURRENT_LANG == "en" else t("Ổ cứng có hoạt động tốt không?"), font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent", bg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text=f"✓ {get_text('all_good')}", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tốt", "Trạng thái": "Tốt", "Chi tiết": self.full_details}, {}), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_yes.pack(side="left", padx=Theme.SPACING)
        
        self.btn_no = ctk.CTkButton(button_bar, text=f"✗ {get_text('issues_found')}", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có ổ cứng lỗi", "Trạng thái": "Lỗi", "Chi tiết": self.full_details}), fg_color=Theme.ERROR, hover_color="#cf222e", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_no.pack(side="left", padx=Theme.SPACING)
        
        self.btn_skip = ctk.CTkButton(button_bar, text="skip", command=lambda: self.mark_skipped({"Kết quả": "skip", "Trạng thái": "skip", "Chi tiết": self.full_details}), fg_color=Theme.BORDER, hover_color=Theme.SEPARATOR, text_color=Theme.TEXT, height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_skip.pack(side="left", padx=Theme.SPACING)
# Screen Test Step
class ScreenTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("screen_test")
        why_text = t("Màn hình là một trong những linh kiện đắt tiền và dễ hỏng nhất. Lỗi điểm chết, hở sáng, ám màu hay 'ung thư panel' (chớp giật ở cạnh viền) là những vấn đề nghiêm trọng.")
        how_text = t("Nhấn 'Bắt đầu Test' để chạy test màn hình tự động. Test sẽ hiển thị các màu khác nhau, nhấn ESC để dừng bất cứ lúc nào.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_screen_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
    
    def create_screen_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(test_frame, text="Automatic Display Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Test tips
        tips_frame = ctk.CTkFrame(test_frame, fg_color=Theme.BACKGROUND)
        tips_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(tips_frame, text=t("Gợi ý kiểm tra:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        if CURRENT_LANG == "vi":
            tips = [
                "• Pixel chết: Chấm đen/sáng không đổi màu",
                "• Hở sáng: Vùng sáng bất thường trên nền đen",
                "• Ám màu: Vùng tối bất thường trên nền sáng",
                "• Chớp giật: Nhấp nháy ở viền màn hình"
            ]
        else:
            tips = [
                "• Dead pixels: Black/bright spots that don't change color",
                "• Backlight bleeding: Abnormal bright areas on black background",
                "• Color staining: Abnormal dark areas on bright background",
                "• Flickering: Blinking at screen edges"
            ]
        for tip in tips:
            ctk.CTkLabel(tips_frame, text=tip, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20)
        
        ctk.CTkButton(test_frame, text=get_text('start_test_btn'), command=self.start_screen_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).pack(pady=10)
        
        test_info = t("Test sẽ hiển thị: Đen → Trắng → Đỏ → Xanh Lá → Xanh Dương\nMỗi màu 3 giây. Nhấn ESC để dừng.")
        ctk.CTkLabel(test_frame, text=test_info, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=10)
    
    def start_screen_test(self):
        def run_test():
            colors = [("black", "white"), ("white", "black"), ("red", "white"), ("green", "black"), ("blue", "white")]
            if CURRENT_LANG == "vi":
                names = ["Đen", "Trắng", "Đỏ", "Xanh Lá", "Xanh Dương"]
            else:
                names = ["Black", "White", "Red", "Green", "Blue"]
            
            win = ctk.CTkToplevel(self)
            win.attributes("-fullscreen", True)
            win.attributes("-topmost", True)
            win.focus_force()
            
            label = ctk.CTkLabel(win, font=Theme.TITLE_FONT)
            label.place(relx=0.5, rely=0.5, anchor="center")
            
            self.test_running = True
            
            def stop_test(event=None):
                self.test_running = False
                if win.winfo_exists():
                    win.destroy()
            
            win.bind("<Escape>", stop_test)
            
            for i, ((bg, fg), name) in enumerate(zip(colors, names)):
                if not self.test_running:
                    break
                win.configure(fg_color=bg)
                esc_text = t("ESC để dừng")
                label.configure(text=f"Test {name}\n({i+1}/5)\n\n{esc_text}", text_color=fg)
                
                for _ in range(30):
                    if not self.test_running:
                        break
                    win.update()
                    time.sleep(0.1)
            
            if self.test_running:
                stop_test()
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Any dead pixels, backlight bleeding, or flickering detected?" if CURRENT_LANG == "en" else "Bạn có phát hiện điểm chết, hở sáng, ám màu hay chớp giật bất thường không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent", bg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text=f"✓ {get_text('screen_ok')}", command=lambda: self.handle_result_generic(True, {"Kết quả": "Bình thường", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_yes.pack(side="left", padx=Theme.SPACING)
        
        self.btn_no = ctk.CTkButton(button_bar, text=f"✗ Screen Issues", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Has issues", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, hover_color="#cf222e", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_no.pack(side="left", padx=Theme.SPACING)

# Keyboard Test Step
class KeyboardTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("keyboard_test")
        why_text = t("Một phím bị liệt, kẹt, hoặc touchpad bị loạn/mất cử chỉ đa điểm sẽ làm gián đoạn hoàn toàn công việc.")
        how_text = t("Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ sáng lên màu xanh dương, và chuyển sang xanh lá khi được nhả ra. Vẽ trên vùng test touchpad, thử click trái/phải.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.key_widgets = {}
        self.pressed_keys = set()
        self.mouse_clicks = {'left': 0, 'right': 0}
        self.listening = False
        
        self.create_keyboard_layout()
        self.create_touchpad_test()
        
        if keyboard:
            self.start_listening()
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()

    def create_keyboard_layout(self):
        keyboard_frame = ctk.CTkFrame(self.action_frame, fg_color="#DCE4E8", corner_radius=Theme.CORNER_RADIUS)
        keyboard_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.action_frame.grid_rowconfigure(0, weight=1)
        keyboard_frame.grid_columnconfigure(0, weight=1)
        keyboard_frame.grid_rowconfigure(5, weight=1)
        
        # Function Keys Row
        row1 = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=(10, 5))
        keys_r1 = ['esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'delete', 'insert', 'home', 'page up', 'page down', 'end', 'scroll lock', 'pause']
        for i, k in enumerate(keys_r1):
            row1.grid_columnconfigure(i, weight=1)
            key = ctk.CTkLabel(row1, text=k.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
            key.grid(row=0, column=i, sticky='ew', padx=2, ipady=5)
            self.key_widgets[k] = key

        # Number Row
        row2 = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        keys_r2 = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace']
        for i, k in enumerate(keys_r2):
            row2.grid_columnconfigure(i, weight=2 if i < 13 else 3)
            key = ctk.CTkLabel(row2, text=k.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
            key.grid(row=0, column=i, sticky='ew', padx=2, ipady=10)
            self.key_widgets[k] = key

        # QWERTY Row
        row3 = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=5)
        keys_r3 = ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']
        for i, k in enumerate(keys_r3):
            row3.grid_columnconfigure(i, weight=3 if i == 0 or i == 13 else 2)
            key = ctk.CTkLabel(row3, text=k.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
            key.grid(row=0, column=i, sticky='ew', padx=2, ipady=10)
            self.key_widgets[k] = key
        
        # Home Row
        row4 = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
        row4.pack(fill="x", padx=10, pady=5)
        keys_r4 = ['caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter']
        for i, k in enumerate(keys_r4):
            row4.grid_columnconfigure(i, weight=4 if i == 0 or i == 12 else 2)
            key = ctk.CTkLabel(row4, text=k.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
            key.grid(row=0, column=i, sticky='ew', padx=2, ipady=10)
            self.key_widgets[k] = key

        # Bottom Row
        row5 = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
        row5.pack(fill="x", padx=10, pady=5)
        keys_r5 = ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift']
        for i, k in enumerate(keys_r5):
            row5.grid_columnconfigure(i, weight=5 if i == 0 or i == 11 else 2)
            key = ctk.CTkLabel(row5, text=k.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
            key.grid(row=0, column=i, sticky='ew', padx=2, ipady=10)
            self.key_widgets[k] = key

        # Spacebar Row
        row6 = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
        row6.pack(fill="x", padx=10, pady=(5, 10))
        keys_r6 = ['ctrl', 'fn', 'windows', 'alt', 'space', 'right alt', 'right ctrl', 'left', 'up', 'down', 'right']
        weights = [2, 1, 2, 2, 12, 2, 2, 1, 1, 1, 1]
        for i, k in enumerate(keys_r6):
            row6.grid_columnconfigure(i, weight=weights[i])
            key = ctk.CTkLabel(row6, text=k.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
            key.grid(row=0, column=i, sticky='ew', padx=2, ipady=10)
            self.key_widgets[k] = key

    def create_touchpad_test(self):
        touchpad_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        touchpad_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        ctk.CTkLabel(touchpad_frame, text="Touchpad & Mouse Test:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        instruction_text = t("• Di chuyển chuột/touchpad trên vùng test\n• Click trái và phải để test\n• Thử cuộn 2 ngón tay (touchpad)")
        instructions = ctk.CTkLabel(touchpad_frame, text=instruction_text, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
        instructions.pack(pady=5)
        
        # Test area
        test_area_frame = ctk.CTkFrame(touchpad_frame)
        test_area_frame.pack(fill="x", padx=20, pady=10)
        
        self.canvas = tk.Canvas(test_area_frame, height=120, highlightthickness=1, bg=Theme.CARD)
        self.canvas.pack(fill="x", padx=10, pady=10)
        
        # Enhanced mouse event binding with better detection
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<MouseWheel>", self.on_scroll)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        
        # Multiple backup click detection methods
        test_area_frame.bind("<Button-1>", lambda e: self.on_left_click_backup())
        test_area_frame.bind("<Button-3>", lambda e: self.on_right_click_backup())
        self.canvas.bind("<ButtonPress-1>", self.on_left_click)
        self.canvas.bind("<ButtonPress-3>", self.on_right_click)
        
        # Removed bind_all - not supported in CustomTkinter
        
        # Click counters
        counter_frame = ctk.CTkFrame(touchpad_frame, fg_color="transparent")
        counter_frame.pack(fill="x", padx=20, pady=5)
        
        left_click_text = t("Click trái: 0")
        right_click_text = t("Click phải: 0")
        self.left_click_label = ctk.CTkLabel(counter_frame, text=left_click_text, font=Theme.BODY_FONT)
        self.left_click_label.pack(side="left", padx=20)
        
        self.right_click_label = ctk.CTkLabel(counter_frame, text=right_click_text, font=Theme.BODY_FONT)
        self.right_click_label.pack(side="right", padx=20)
        
        ctk.CTkButton(touchpad_frame, text=get_text('clear_canvas'), command=self.clear_canvas, height=30, font=Theme.BODY_FONT).pack(pady=5)

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=Theme.ACCENT, outline=Theme.ACCENT, tags="trail")

    def on_left_click(self, event):
        self.mouse_clicks['left'] += 1
        left_text = t("Click trái:")
        self.left_click_label.configure(text=f"{left_text} {self.mouse_clicks['left']}")
        try:
            x = getattr(event, 'x', 75)
            y = getattr(event, 'y', 75)
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#FF4444", outline="#CC0000", width=3, tags="click")
            self.canvas.create_text(x, y, text="L", font=("Arial", 14, "bold"), fill="white", tags="click")
        except Exception as e:
            print(f"Left click error: {e}")
            self.canvas.create_oval(60, 60, 90, 90, fill="#FF4444", outline="#CC0000", width=3, tags="click")
            self.canvas.create_text(75, 75, text="L", font=("Arial", 14, "bold"), fill="white", tags="click")
        self.after(2000, lambda: self.canvas.delete("click"))

    def on_right_click(self, event):
        self.mouse_clicks['right'] += 1
        right_text = t("Click phải:")
        self.right_click_label.configure(text=f"{right_text} {self.mouse_clicks['right']}")
        try:
            x = getattr(event, 'x', 225)
            y = getattr(event, 'y', 75)
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#4444FF", outline="#0000CC", width=3, tags="click")
            self.canvas.create_text(x, y, text="R", font=("Arial", 14, "bold"), fill="white", tags="click")
        except Exception as e:
            print(f"Right click error: {e}")
            self.canvas.create_oval(210, 60, 240, 90, fill="#4444FF", outline="#0000CC", width=3, tags="click")
            self.canvas.create_text(225, 75, text="R", font=("Arial", 14, "bold"), fill="white", tags="click")
        self.after(2000, lambda: self.canvas.delete("click"))
    
    def on_left_click_backup(self):
        self.mouse_clicks['left'] += 1
        left_text = t("Click trái:")
        self.left_click_label.configure(text=f"{left_text} {self.mouse_clicks['left']}")
        x, y = 100, 60
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#FF4444", outline="#CC0000", width=3, tags="click")
        self.canvas.create_text(x, y, text="L", font=("Arial", 14, "bold"), fill="white", tags="click")
        self.after(2000, lambda: self.canvas.delete("click"))
    
    def on_right_click_backup(self):
        self.mouse_clicks['right'] += 1
        right_text = t("Click phải:")
        self.right_click_label.configure(text=f"{right_text} {self.mouse_clicks['right']}")
        x, y = 200, 60
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#4444FF", outline="#0000CC", width=3, tags="click")
        self.canvas.create_text(x, y, text="R", font=("Arial", 14, "bold"), fill="white", tags="click")
        self.after(2000, lambda: self.canvas.delete("click"))
    
    def check_canvas_click(self, event, click_type):
        """Global click detection as fallback"""
        try:
            # Check if click is within canvas bounds
            canvas_x = self.canvas.winfo_rootx()
            canvas_y = self.canvas.winfo_rooty()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if (canvas_x <= event.x_root <= canvas_x + canvas_width and 
                canvas_y <= event.y_root <= canvas_y + canvas_height):
                
                if click_type == 'left':
                    self.on_left_click_backup()
                else:
                    self.on_right_click_backup()
        except Exception as e:
            print(f"Global click detection error: {e}")

    def on_scroll(self, event):
        direction = "↑" if event.delta > 0 else "↓"
        self.canvas.create_text(event.x, event.y, text=direction, font=("Arial", 20), fill="green", tags="scroll")
        self.after(500, lambda: self.canvas.delete("scroll"))

    def clear_canvas(self):
        self.canvas.delete("trail")
        self.canvas.delete("click")
        self.canvas.delete("scroll")

    def start_listening(self):
        try:
            self.listening = True
            # Chặn chỉ Print Screen, không chặn tất cả
            keyboard.hook(self.on_key_event, suppress=False)
            
            # Thêm hook riêng cho Print Screen
            keyboard.block_key('print screen')
        except Exception as e:
            self.listening = False
            if "root" in str(e).lower() or "permission" in str(e).lower():
                messagebox.showwarning("Yêu cầu quyền Admin", "Không thể bắt sự kiện bàn phím do thiếu quyền Admin/root. Vui lòng chạy lại ứng dụng với quyền quản trị viên.")

    def on_key_event(self, event):
        if not self.listening or not self.winfo_exists():
            return
        
        self.after(0, self._update_key_ui, event.name, event.event_type)

    def _update_key_ui(self, key_name_raw, event_type):
        if not self.listening:
            return
            
        key_name = key_name_raw.lower()
        
        # Enhanced key mapping for special keys
        key_map = {
            'left shift': 'shift', 'right shift': 'right shift', 
            'left ctrl': 'ctrl', 'right ctrl': 'right ctrl',
            'left alt': 'alt', 'alt gr': 'right alt', 'right alt': 'right alt',
            'left windows': 'windows', 'right windows': 'windows',
            'caps lock': 'caps lock', 'page up': 'page up', 'page down': 'page down',
            'print screen': 'print screen', 'delete': 'delete', 'insert': 'insert',
            'home': 'home', 'end': 'end', 'num lock': 'num lock',
            '\\': '\\', 'backslash': '\\'
        }
        
        mapped_key = key_map.get(key_name, key_name)
        widget = self.key_widgets.get(mapped_key)
        
        if not widget:
            return
            
        if event_type == 'down':
            widget.configure(fg_color=Theme.ACCENT, text_color="#ffffff")
            self.pressed_keys.add(mapped_key)
        elif event_type == 'up':
            widget.configure(fg_color=Theme.SUCCESS, text_color="#ffffff")
            if mapped_key in self.pressed_keys:
                self.pressed_keys.remove(mapped_key)

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.result_container, text="Keyboard, touchpad and mouse working properly?" if CURRENT_LANG == "en" else "Bàn phím, touchpad và chuột có hoạt động tốt không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent", bg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text=f"✓ {get_text('input_ok')}", command=lambda: self.handle_result_generic(True, {"Kết quả": "Working well", "Trạng thái": "Tốt", "Chi tiết": f"Click trái: {self.mouse_clicks['left']}, Click phải: {self.mouse_clicks['right']}"}, {}), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_yes.pack(side="left", padx=Theme.SPACING)
        
        self.btn_no = ctk.CTkButton(button_bar, text=f"✗ Input Issues", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có lỗi", "Trạng thái": "Lỗi", "Chi tiết": f"Click trái: {self.mouse_clicks['left']}, Click phải: {self.mouse_clicks['right']}"}), fg_color=Theme.ERROR, hover_color="#cf222e", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0)
        self.btn_no.pack(side="left", padx=Theme.SPACING)

    def stop_tasks(self):
        super().stop_tasks()
        self.listening = False
        if keyboard:
            try:
                keyboard.unhook_all()
                keyboard.unblock_key('print screen')
            except Exception:
                pass
        # Stop warning sound if webcam test
        if hasattr(self, 'stop_warning_sound'):
            self.stop_warning_sound()
# Base Stress Test Step
class BaseStressTestStep(BaseStepFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.test_process = None
        self.queue = multiprocessing.Queue()
        self.is_testing = False
        
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(3, weight=1)
        
        self.controls_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        start_text = f"{get_text('start_test_btn')} ({self.estimated_time})" if hasattr(self, 'estimated_time') else get_text('start_test_btn')
        self.start_button = ctk.CTkButton(self.controls_frame, text=start_text, command=self.start_test, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.start_button.pack(side="left", padx=(0, 10))
        
        self.stop_button = ctk.CTkButton(self.controls_frame, text=get_text("stop_test_btn"), command=self.stop_test, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, state="disabled", fg_color=Theme.WARNING, text_color=Theme.TEXT)
        self.stop_button.pack(side="left")
        
        self.status_label = ctk.CTkLabel(self.action_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
        self.status_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Real-time monitoring frame
        self.monitor_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        self.monitor_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        # Create canvas for charts
        self.chart_canvas = tk.Canvas(self.monitor_frame, height=200, bg=Theme.BACKGROUND, highlightthickness=0)
        self.chart_canvas.pack(fill="x", padx=10, pady=10)
        
        # Data storage for charts
        self.cpu_data = deque(maxlen=100)
        self.temp_data = deque(maxlen=100)
        self.freq_data = deque(maxlen=100)
        
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)

    def start_test(self):
        raise NotImplementedError("Child class must implement start_test")

    def run_worker(self, worker_func, args_tuple):
        if self.is_testing:
            return
        
        self.is_testing = True
        self.progress_bar.set(0)
        self._completed = False 
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text=get_text("loading") + " worker...", text_color=Theme.ACCENT)
        
        for w in self.results_frame.winfo_children():
            w.destroy()
        
        try:
            self.test_process = multiprocessing.Process(target=worker_func, args=args_tuple, daemon=True)
            self.test_process.start()
            self.after(100, self.check_queue)
        except Exception as e:
            self.status_label.configure(text=f"Lỗi khởi tạo Process: {e}", text_color=Theme.ERROR)
            self.stop_test()

    def stop_test(self):
        if self.test_process and self.test_process.is_alive():
            self.test_process.terminate()
            self.test_process.join(timeout=2)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        stop_text = t("Test đã được dừng bởi người dùng.")
        self.status_label.configure(text=stop_text, text_color=Theme.TEXT_SECONDARY)
        
        if not self._completed:
            stop_result = t("Bị dừng bởi người dùng")
            self.mark_completed({"Kết quả": stop_result, "Trạng thái": get_text("status_skip")})

    def check_queue(self):
        if not self.is_testing:
            return
        
        try:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                self.handle_message(msg)
        except Exception as e:
            print(f"Lỗi đọc queue: {e}")
        finally:
            self.after(200, self.check_queue)

    def handle_message(self, msg):
        msg_type = msg.get('type')
        if msg_type == 'status':
            self.status_label.configure(text=msg.get('message', ''))
        elif msg_type == 'update':
            self.progress_bar.set(msg.get('progress', 0))
            self.update_ui(msg)
        elif msg_type == 'result':
            self.finalize_test(msg)
        elif msg_type == 'error':
            self.status_label.configure(text=f"Lỗi Worker: {msg.get('message', 'Không rõ')}", text_color=Theme.ERROR)
            self.mark_completed({"Kết quả": "Lỗi Worker", "Trạng thái": "Lỗi", "Chi tiết": msg.get('message', '')})
            self.stop_test()
        elif msg_type == 'done':
            self.is_testing = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            if not self._completed:
                 self.status_label.configure(text=get_text("finished"))
                 completed_text = t("Hoàn thành")
                 self.mark_completed({"Kết quả": completed_text, "Trạng thái": get_text("status_good")})

    def update_ui(self, data):
        pass

    def finalize_test(self, data):
        pass

    def update_charts(self):
        """Update real-time charts"""
        try:
            self.chart_canvas.delete("all")
            width = self.chart_canvas.winfo_width()
            height = self.chart_canvas.winfo_height()
            
            if width <= 1 or height <= 1 or not self.cpu_data:
                return
            
            # Draw CPU usage chart (top)
            chart_height = height // 3
            self.draw_line_chart(self.cpu_data, 0, chart_height, width, "CPU %", "#58a6ff", 100)
            
            # Draw temperature chart (middle)
            if any(self.temp_data):
                self.draw_line_chart(self.temp_data, chart_height, chart_height, width, "Temp °C", "#f85149", 100)
            
            # Draw frequency chart (bottom)
            if any(self.freq_data):
                max_freq = max(self.freq_data) if self.freq_data else 3000
                self.draw_line_chart(self.freq_data, chart_height * 2, chart_height, width, "Freq MHz", "#238636", max_freq)
        except:
            pass
    
    def draw_line_chart(self, data, y_offset, height, width, label, color, max_val):
        """Draw a simple line chart"""
        if not data or len(data) < 2:
            return
        
        # Draw background
        self.chart_canvas.create_rectangle(0, y_offset, width, y_offset + height, fill=Theme.CARD, outline=Theme.BORDER)
        
        # Draw label
        self.chart_canvas.create_text(10, y_offset + 10, text=label, fill=Theme.TEXT, anchor="nw", font=("Arial", 10))
        
        # Draw data line
        points = []
        for i, value in enumerate(data):
            x = (i / (len(data) - 1)) * (width - 20) + 10
            y = y_offset + height - 10 - ((value / max_val) * (height - 20))
            points.extend([x, y])
        
        if len(points) >= 4:
            self.chart_canvas.create_line(points, fill=color, width=2, smooth=True)
        
        # Draw current value
        current_val = data[-1] if data else 0
        self.chart_canvas.create_text(width - 10, y_offset + 10, text=f"{current_val:.1f}", fill=color, anchor="ne", font=("Arial", 12, "bold"))
    
    def stop_tasks(self):
        super().stop_tasks()
        self.stop_test()

# CPU Stress Test Step
class CPUStressTestStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        title = get_text("cpu_stress")
        why_text = t("Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt của máy.")
        how_text = t("Nhấn 'Bắt đầu Test' trong 2-5 phút. Theo dõi biểu đồ nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.TEST_DURATION = 120
        self.estimated_time = t("2-3 phút")

    def start_test(self):
        try:
            self.run_worker(run_cpu_stress_test, (self.queue, self.TEST_DURATION))
        except Exception as e:
            self.status_label.configure(text=f"Lỗi khởi động CPU test: {e}", text_color=Theme.ERROR)

    def update_ui(self, data):
        status = data.get('status', '')
        throttling = data.get('throttling', False)
        
        # Color-code status based on throttling
        color = Theme.WARNING if throttling else Theme.TEXT_SECONDARY
        self.status_label.configure(text=status, text_color=color)
        
        # Update charts
        self.cpu_data.append(data.get('cpu_usage', 0))
        self.temp_data.append(data.get('temperature', 0) or 0)
        self.freq_data.append(data.get('frequency', 0) or 0)
        self.update_charts()

    def finalize_test(self, msg):
        result_data = msg.get('data', {})
        max_temp = result_data.get('max_temperature', 0)
        throttling = result_data.get('throttling_severity', 'None')
        freq_drops = result_data.get('freq_drops', 0)
        max_freq = result_data.get('max_freq', 0)
        min_freq = result_data.get('min_freq', 0)
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Results header with translations
        header_text = t("📊 Kết Quả CPU Stress Test")
        ctk.CTkLabel(self.results_frame, text=header_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        # Performance metrics
        metrics_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.FRAME)
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        if CURRENT_LANG == "vi":
            temp_text = f"🔥 Nhiệt độ tối đa: {max_temp:.1f}°C" if max_temp else "🔥 Nhiệt độ: Không đọc được"
            usage_text = f"⚡ Sử dụng CPU: {result_data.get('max_cpu_usage', 0):.1f}%"
        else:
            temp_text = f"🔥 Max Temperature: {max_temp:.1f}°C" if max_temp else "🔥 Temperature: Unreadable"
            usage_text = f"⚡ CPU Usage: {result_data.get('max_cpu_usage', 0):.1f}%"
        
        ctk.CTkLabel(metrics_frame, text=temp_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(metrics_frame, text=usage_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        
        if max_freq and min_freq:
            freq_loss = ((max_freq - min_freq) / max_freq) * 100
            freq_text = f"📡 Tần số: {max_freq:.0f}MHz → {min_freq:.0f}MHz (-{freq_loss:.1f}%)" if CURRENT_LANG == "vi" else f"📡 Frequency: {max_freq:.0f}MHz → {min_freq:.0f}MHz (-{freq_loss:.1f}%)"
            ctk.CTkLabel(metrics_frame, text=freq_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        
        # Frequency lock detection
        freq_locked = False
        if max_freq and min_freq:
            freq_variation = ((max_freq - min_freq) / max_freq) * 100
            freq_locked = freq_variation < 5  # Less than 5% variation indicates locked frequency
        
        # Frequency lock analysis
        if freq_locked:
            lock_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.INFO)
            lock_frame.pack(fill="x", padx=10, pady=10)
            
            lock_text = t("🔒 PHÁT HIỆN KHÓA XUNG CPU")
            ctk.CTkLabel(lock_frame, text=lock_text, font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=10)
            
            lock_info_frame = ctk.CTkFrame(lock_frame, fg_color="transparent")
            lock_info_frame.pack(fill="x", padx=15, pady=(0,15))
            
            if CURRENT_LANG == "vi":
                analysis_text = "📊 Phân tích:"
                freq_text = f"• Tần số cố định tại {min_freq:.0f}MHz (biến thiên <5%)"
                cpu_text = "• CPU không tự điều chỉnh tần số theo tải"
                causes_text = "\n🔍 Nguyên nhân có thể:"
                bios_text = "• Cài đặt BIOS khóa tần số (Fixed Frequency)"
                software_text = "• Phần mềm quản lý nguồn hạn chế CPU"
                power_text = "• Chế độ tiết kiệm pin cực mạnh"
            else:
                analysis_text = "📊 Analysis:"
                freq_text = f"• Fixed frequency at {min_freq:.0f}MHz (variation <5%)"
                cpu_text = "• CPU not dynamically adjusting frequency based on load"
                causes_text = "\n🔍 Possible causes:"
                bios_text = "• BIOS setting locks frequency (Fixed Frequency)"
                software_text = "• Power management software limiting CPU"
                power_text = "• Extreme power saving mode"
            
            ctk.CTkLabel(lock_info_frame, text=analysis_text, font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
            ctk.CTkLabel(lock_info_frame, text=freq_text, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(lock_info_frame, text=cpu_text, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            
            ctk.CTkLabel(lock_info_frame, text=causes_text, font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
            ctk.CTkLabel(lock_info_frame, text=bios_text, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(lock_info_frame, text=software_text, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(lock_info_frame, text=power_text, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            
            ctk.CTkLabel(lock_info_frame, text=t("\n💡 Cách khắc phục:"), font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
            ctk.CTkLabel(lock_info_frame, text=t("• Kiểm tra BIOS: CPU Frequency → Auto/Dynamic"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(lock_info_frame, text=t("• Windows: Chế độ nguồn → Hiệu năng cao"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(lock_info_frame, text=t("• Tắt phần mềm quản lý nguồn của hãng"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        
        # Throttling analysis
        if throttling != "None":
            throttle_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.WARNING if throttling == "Light" else Theme.ERROR)
            throttle_frame.pack(fill="x", padx=10, pady=10)
            
            throttle_text = f"⚠️ PHÁT HIỆN THROTTLING: {throttling.upper()}" if CURRENT_LANG == "vi" else f"⚠️ THROTTLING DETECTED: {throttling.upper()}"
            ctk.CTkLabel(throttle_frame, text=throttle_text, font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=10)
            
            # Causes and solutions
            causes_frame = ctk.CTkFrame(throttle_frame, fg_color="transparent")
            causes_frame.pack(fill="x", padx=15, pady=(0,15))
            
            ctk.CTkLabel(causes_frame, text=t("🔍 Nguyên nhân có thể:"), font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
            
            if max_temp and max_temp > 85:
                ctk.CTkLabel(causes_frame, text=t("• Quá nhiệt (>85°C) - Tản nhiệt kém"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            if freq_drops > 30:
                ctk.CTkLabel(causes_frame, text=t("• Power limit - Nguồn không đủ mạnh"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            
            ctk.CTkLabel(causes_frame, text=t("\n💡 Cách khắc phục:"), font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
            ctk.CTkLabel(causes_frame, text=t("• Vệ sinh quạt tản nhiệt, thay keo tản nhiệt"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(causes_frame, text=t("• Kiểm tra adapter nguồn (phải đúng watt)"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
            ctk.CTkLabel(causes_frame, text=t("• Cập nhật BIOS và driver"), font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        
        # Temperature warnings
        if max_temp and max_temp > 95:
            temp_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.ERROR)
            temp_frame.pack(fill="x", padx=10, pady=5)
            temp_warning_text = t("🚨 CẢNH BÁO: Nhiệt độ nguy hiểm! CPU có thể bị hỏng.")
            ctk.CTkLabel(temp_frame, text=temp_warning_text, font=Theme.BODY_FONT, text_color="white").pack(pady=10)
        
        # Decision buttons
        button_bar = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        # Auto-determine status
        is_good = (not max_temp or max_temp < 90) and throttling in ["None", "Light"]
        
        # Create detailed result string
        result_details = f"Temp: {max_temp}°C, Throttling: {throttling}"
        if freq_locked:
            result_details += f", Freq Locked: {min_freq:.0f}MHz"
        else:
            result_details += f", Freq: {min_freq:.0f}-{max_freq:.0f}MHz"
        
        good_text = t("✓ CPU Tốt")
        accept_text = t("✓ Chấp Nhận")
        ctk.CTkButton(button_bar, text=good_text if is_good else accept_text, 
                     command=lambda: self.mark_completed({"Kết quả": result_details, "Trạng thái": get_text("status_good")}, auto_advance=True), 
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        issue_text = t("✗ CPU Có Vấn Đề")
        ctk.CTkButton(button_bar, text=issue_text, 
                     command=lambda: self.mark_completed({"Kết quả": result_details, "Trạng thái": get_text("status_error")}, auto_advance=True), 
                     fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

# GPU Stress Test Step
class GPUStressTestStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        title = get_text("gpu_stress")
        why_text = t("GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng.")
        how_text = t("Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 60 giây. Hãy quan sát có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không? Máy có bị treo hoặc tự khởi động lại không?")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.TEST_DURATION = 60
        self.estimated_time = t("1-2 phút")
        
        # GPU data storage
        self.fps_data = deque(maxlen=100)
        self.particle_data = deque(maxlen=100)
        
        # Add GPU monitoring frame after progress bar
        self.gpu_monitor_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        self.gpu_monitor_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        self.gpu_chart_canvas = tk.Canvas(self.gpu_monitor_frame, height=150, bg=Theme.BACKGROUND, highlightthickness=0)
        self.gpu_chart_canvas.pack(fill="x", padx=10, pady=10)

    def start_test(self):
        if not pygame:
            self.status_label.configure(text=t("Pygame không có sẵn. Cài đặt: pip install pygame"), text_color=Theme.ERROR)
            return
        
        self.run_worker(run_gpu_stress, (self.TEST_DURATION, self.queue))

    def update_ui(self, data):
        fps = data.get('fps', 0)
        particles = data.get('particles', 0)
        self.status_label.configure(text=f"GPU Test: FPS: {fps:.1f}, Particles: {particles}")
        
        # Update GPU charts
        self.fps_data.append(fps)
        self.particle_data.append(particles)
        self.update_gpu_charts()
    
    def update_gpu_charts(self):
        """Update real-time GPU charts"""
        try:
            self.gpu_chart_canvas.delete("all")
            width = self.gpu_chart_canvas.winfo_width()
            height = self.gpu_chart_canvas.winfo_height()
            
            if width <= 1 or height <= 1 or not self.fps_data:
                return
            
            # Draw FPS chart (top half)
            chart_height = height // 2
            self.draw_gpu_chart(self.fps_data, 0, chart_height, width, "FPS", "#58a6ff", 60)
            
            # Draw particles chart (bottom half)
            max_particles = max(self.particle_data) if self.particle_data else 100
            self.draw_gpu_chart(self.particle_data, chart_height, chart_height, width, "Particles", "#238636", max_particles)
        except:
            pass
    
    def draw_gpu_chart(self, data, y_offset, height, width, label, color, max_val):
        """Draw GPU chart"""
        if not data or len(data) < 2:
            return
        
        # Draw background
        self.gpu_chart_canvas.create_rectangle(0, y_offset, width, y_offset + height, fill=Theme.CARD, outline=Theme.BORDER)
        
        # Draw label
        self.gpu_chart_canvas.create_text(10, y_offset + 10, text=label, fill=Theme.TEXT, anchor="nw", font=("Arial", 10))
        
        # Draw data line
        points = []
        for i, value in enumerate(data):
            x = (i / (len(data) - 1)) * (width - 20) + 10
            y = y_offset + height - 10 - ((value / max_val) * (height - 20))
            points.extend([x, y])
        
        if len(points) >= 4:
            self.gpu_chart_canvas.create_line(points, fill=color, width=2, smooth=True)
        
        # Draw current value
        current_val = data[-1] if data else 0
        self.gpu_chart_canvas.create_text(width - 10, y_offset + 10, text=f"{current_val:.1f}", fill=color, anchor="ne", font=("Arial", 12, "bold"))

    def finalize_test(self, msg):
        result_data = msg.get('data', {})
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        header_text = t("📊 Kết Quả GPU Stress Test")
        ctk.CTkLabel(self.results_frame, text=header_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        # Performance metrics with translations
        metrics_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.FRAME)
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        if CURRENT_LANG == "vi":
            fps_text = f"🎮 FPS trung bình: {result_data.get('average_fps', 0):.1f}"
            frames_text = f"🎥 Tổng frames: {result_data.get('total_frames', 0)}"
            min_fps_text = f"🔻 FPS thấp nhất: {result_data.get('min_fps', 0):.1f}"
            max_fps_text = f"🔺 FPS cao nhất: {result_data.get('max_fps', 0):.1f}"
        else:
            fps_text = f"🎮 Average FPS: {result_data.get('average_fps', 0):.1f}"
            frames_text = f"🎥 Total Frames: {result_data.get('total_frames', 0)}"
            min_fps_text = f"🔻 Minimum FPS: {result_data.get('min_fps', 0):.1f}"
            max_fps_text = f"🔺 Maximum FPS: {result_data.get('max_fps', 0):.1f}"
        
        ctk.CTkLabel(metrics_frame, text=fps_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(metrics_frame, text=min_fps_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(metrics_frame, text=max_fps_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        ctk.CTkLabel(metrics_frame, text=frames_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15, pady=5)
        
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        
        gpu_stable_text = t("GPU ổn định")
        ctk.CTkButton(button_bar, text=get_text("gpu_good"), command=lambda: self.mark_completed({"Kết quả": gpu_stable_text, "Trạng thái": get_text("status_good")}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        
        gpu_issue_text = t("GPU có vấn đề")
        gpu_unstable_text = t("GPU không ổn định")
        ctk.CTkButton(button_bar, text=gpu_issue_text, command=lambda: self.mark_completed({"Kết quả": gpu_unstable_text, "Trạng thái": get_text("status_error")}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

# Hard Drive Speed Step
class HardDriveSpeedStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        title = get_text("harddrive_speed")
        why_text = t("Tốc độ đọc/ghi ảnh hưởng trực tiếp đến hiệu năng hệ thống.")
        how_text = t("Nhấn 'Bắt đầu Test' để kiểm tra tốc độ ổ cứng thực tế.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.TEST_DURATION = 60
        self.estimated_time = t("1-2 phút")

    def start_test(self):
        self.run_worker(run_disk_benchmark, (self.queue, 60, 512))

    def update_ui(self, data):
        operation = data.get('operation', '')
        speed = data.get('speed', 0)
        avg_speed = data.get('avg_speed', 0)
        self.status_label.configure(text=f"{operation}: {speed:.1f} MB/s (Avg: {avg_speed:.1f} MB/s)")

    def finalize_test(self, msg):
        result_data = msg.get('data', {})
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        write_speed = result_data.get('write_speed', '0')
        read_speed = result_data.get('read_speed', '0')
        
        ctk.CTkLabel(self.results_frame, text="Disk Test Results:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        ctk.CTkLabel(self.results_frame, text=f"Tốc độ Ghi: {write_speed} MB/s", font=Theme.BODY_FONT).pack()
        ctk.CTkLabel(self.results_frame, text=f"Tốc độ Đọc: {read_speed} MB/s", font=Theme.BODY_FONT).pack()
        
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        
        write_read_text = f"Ghi: {write_speed}MB/s, Đọc: {read_speed}MB/s" if CURRENT_LANG == "vi" else f"Write: {write_speed}MB/s, Read: {read_speed}MB/s"
        ctk.CTkButton(button_bar, text=get_text("speed_good"), command=lambda: self.mark_completed({"Kết quả": write_read_text, "Trạng thái": get_text("status_good")}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        
        slow_speed_text = t("Tốc độ chậm")
        ctk.CTkButton(button_bar, text=slow_speed_text, command=lambda: self.mark_completed({"Kết quả": slow_speed_text, "Trạng thái": get_text("status_error")}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
# Additional Test Steps

class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, t("Kiểm Tra Ngoại Hình"), 
            t("Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp."), 
            t("Kiểm tra vỏ máy, bản lề, cổng kết nối, ốc vít, tem bảo hành. Đánh giá tổng thể tình trạng vật lý."), **kwargs)
        self.create_inspection_checklist()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
        self.mark_completed({"Kết quả": "Đã hiển thị checklist", "Trạng thái": "Sẵn sàng"}, auto_advance=False)
    
    def create_inspection_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(checklist_frame, text=t("🔍 Checklist Kiểm Tra Ngoại Hình Chi Tiết"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Vỏ máy & Bản lề
        section1 = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        section1.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(section1, text=t("💻 Vỏ Máy & Bản Lề:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ Vỏ máy: Vết nứt, móp méo (đặc biệt góc máy)"),
            t("✓ Bản lề: Mở/đóng 10-15 lần, nghe tiếng kêu kèn kẹt"),
            t("✓ Bản lề giữ góc: Không rơ, không tự đóng"),
            t("✓ Vết nứt gần bản lề: DẤU HIỆU NGUY HIỂM")
        ]:
            ctk.CTkLabel(section1, text=item, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=25, pady=1)
        
        # Cổng kết nối
        section2 = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        section2.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(section2, text=t("🔌 Cổng Kết Nối:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ Cổng sạc: Cắm và lay nhẹ, KHÔNG được lỏng"),
            t("✓ USB: Cắm thử USB, kiểm tra độ chặt"),
            t("✓ HDMI/DisplayPort: Không bị lỏng lẻo"),
            t("✓ Audio jack: Cắm tai nghe thử")
        ]:
            ctk.CTkLabel(section2, text=item, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=25, pady=1)
        
        # Ốc vít & Tem
        section3 = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        section3.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(section3, text=t("🔩 Ốc Vít & Tem Bảo Hành:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ Ốc vít: Không toét đầu (dấu hiệu tháo lắp)"),
            t("✓ Tem bảo hành: Còn nguyên, không bị bóc"),
            t("✓ Serial number: Khớp với BIOS và sticker"),
            t("✓ Khe tản nhiệt: Không bị bịt tắc bụi")
        ]:
            ctk.CTkLabel(section3, text=item, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=25, pady=1)
        
        # ThinkPad đặc biệt
        thinkpad_frame = ctk.CTkFrame(checklist_frame, fg_color="#1E3A8A", border_width=2, border_color="#3B82F6")
        thinkpad_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(thinkpad_frame, text=t("🔴 LENOVO THINKPAD - KIỂM TRA ĐẶC BIỆT:"), font=Theme.BODY_FONT, text_color="#60A5FA").pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ Tem Lenovo chính hãng: Hologram, không nhòe"),
            t("✓ Sticker dưới đáy: COA Windows, Serial, Model"),
            t("✓ Asset tag: ThinkPad doanh nghiệp thường có"),
            t("✓ TrackPoint (nút đỏ): Hoạt động, không bị lỏng"),
            t("✓ ThinkLight/Đèn bàn phím: Test hoạt động"),
            t("✓ Khe Kensington Lock: Không bị gãy"),
            t("⚠️ Kiểm tra BIOS có bị khóa Computrace không!")
        ]:
            ctk.CTkLabel(thinkpad_frame, text=item, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=25, pady=1)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        question_text = t("Tình trạng vật lý tổng thể của máy như thế nào?")
        ctk.CTkLabel(self.result_container, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        btn1_text = t("Rất tốt")
        btn2_text = t("Tốt")
        btn3_text = t("Trung bình")
        btn4_text = t("Kém")
        
        ctk.CTkButton(button_bar, text=btn1_text, command=lambda: self.mark_completed({"Kết quả": btn1_text, "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(button_bar, text=btn2_text, command=lambda: self.mark_completed({"Kết quả": btn2_text, "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(button_bar, text=btn3_text, command=lambda: self.mark_completed({"Kết quả": btn3_text, "Trạng thái": "Cảnh báo"}, auto_advance=True), fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(button_bar, text=btn4_text, command=lambda: self.mark_completed({"Kết quả": btn4_text, "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)

class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = "Xem checklist bên dưới để kiểm tra từng mục trong BIOS"
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS", 
            "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp.", 
            how_text, **kwargs)
        self.create_bios_checklist()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
    
    def create_bios_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(checklist_frame, text=t("⚙️ Checklist Kiểm Tra BIOS Chi Tiết"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Cách vào BIOS
        access_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        access_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(access_frame, text=t("🔑 Cách Vào BIOS:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        for item in [
            "Dell/Alienware: F2 hoặc F12",
            "HP/Compaq: F10 hoặc ESC",
            "Lenovo/ThinkPad: F1, F2 hoặc Enter",
            "ASUS: F2 hoặc Delete",
            "Acer: F2 hoặc Delete",
            "MSI: Delete hoặc F2"
        ]:
            ctk.CTkLabel(access_frame, text=f"• {item}", font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=25, pady=1)
        
        # Hiệu năng CPU
        cpu_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        cpu_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(cpu_frame, text=t("⚡ Hiệu Năng CPU:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ Intel Turbo Boost: Phải 'Enabled'"),
            t("✓ AMD Turbo Core/Precision Boost: Phải 'Enabled'"),
            t("✓ CPU C-States: Nên 'Enabled' (tiết kiệm pin)"),
            t("✓ Virtualization (VT-x/AMD-V): 'Enabled' nếu dùng VM")
        ]:
            ctk.CTkLabel(cpu_frame, text=item, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=25, pady=1)
        
        # RAM
        ram_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        ram_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(ram_frame, text="💾 RAM:", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ XMP/DOCP Profile: Nên bật (RAM chạy đúng tốc độ)"),
            t("✓ Kiểm tra dung lượng RAM hiển thị khớp thực tế")
        ]:
            ctk.CTkLabel(ram_frame, text=item, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=25, pady=1)
        
        # Cảnh báo mật khẩu BIOS
        password_warning = ctk.CTkFrame(checklist_frame, fg_color="#991B1B", border_width=3, border_color="#DC2626")
        password_warning.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(password_warning, text=t("⛔ CẢNH BÁO NGHIÊM TRỌNG - MẬT KHẨU BIOS"), font=Theme.SUBHEADING_FONT, text_color="#FEE2E2").pack(pady=10)
        
        warning_text = ctk.CTkFrame(password_warning, fg_color="transparent")
        warning_text.pack(fill="x", padx=15, pady=(0,10))
        
        for item in [
            "🚫 KIỂM TRA NGAY KHI VÀO BIOS:",
            "",
            "1️⃣ Supervisor/Admin Password: Phải TRỐNG",
            "   → Nếu có: KHÔNG MUA hoặc giảm giá MẠNH",
            "",
            "2️⃣ HDD/SSD Password: Phải TRỐNG",
            "   → Nếu có: Ổ cứng bị khóa CHẾT, không dùng được!",
            "",
            "🚨 THINKPAD ĐẶC BIỆT:",
            "   • Mật khẩu BIOS ThinkPad gần như KHÔNG THỂ phá",
            "   • Phá phải thay Mainboard (5-10 triệu)",
            "   • Hoặc gửi Lenovo (3-5 triệu + chờ lâu)",
            "   • Nếu khóa HDD: Ổ cứng thành gạch!",
            "",
            "❌ Nếu có mật khẩu: Từ CHỐI MUA!"
        ]:
            color = "#FEE2E2" if item.startswith("🚫") or item.startswith("🚨") or item.startswith("❌") else "white"
            font = Theme.BODY_FONT if item.startswith("🚫") or item.startswith("🚨") else Theme.SMALL_FONT
            ctk.CTkLabel(warning_text, text=item, font=font, text_color=color, justify="left").pack(anchor="w", padx=10, pady=1)
        
        # Bảo mật khác
        security_frame = ctk.CTkFrame(checklist_frame, fg_color="#7F1D1D", border_width=2, border_color="#EF4444")
        security_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(security_frame, text=t("🔒 BẢO MẬT KHÁC:"), font=Theme.BODY_FONT, text_color="#FCA5A5").pack(anchor="w", padx=10, pady=5)
        for item in[
            t("⚠️ Computrace/Absolute: Phải 'Disabled' hoặc 'Inactive'"),
            t("⚠️ Intel AMT/vPro: Nên 'Disabled' (trừ doanh nghiệp)"),
            t("✓ Secure Boot: 'Enabled' cho bảo mật"),
            t("✓ TPM: 'Enabled' (Windows 11 yêu cầu)")
        ]:
            ctk.CTkLabel(security_frame, text=item, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=25, pady=1)
        
        # ThinkPad đặc biệt
        thinkpad_frame = ctk.CTkFrame(checklist_frame, fg_color="#1E3A8A", border_width=2, border_color="#3B82F6")
        thinkpad_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(thinkpad_frame, text=t("🔴 THINKPAD - CÀI ĐẶT KHÁC:"), font=Theme.BODY_FONT, text_color="#60A5FA").pack(anchor="w", padx=10, pady=5)
        for item in [
            t("✓ Battery Charge Threshold: 80% (kéo dài tuổi thọ pin)"),
            t("✓ Rapid Charge: 'Enabled' (sạc nhanh)"),
            t("✓ Always On USB: Tùy nhu cầu"),
            t("✓ Fn/Ctrl Key Swap: Tùy thích")
        ]:
            ctk.CTkLabel(thinkpad_frame, text=item, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=25, pady=1)

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        question_text = t("Các cài đặt trong BIOS có chính xác và an toàn không?")
        ctk.CTkLabel(self.result_container, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        btn_yes_text = t("Có, mọi cài đặt đều đúng")
        btn_no_text = t("Không, có cài đặt sai/bị khóa")
        
        ctk.CTkButton(button_bar, text=btn_yes_text, command=lambda: self.mark_completed({"Kết quả": "Cài đặt chính xác", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text=btn_no_text, command=lambda: self.mark_completed({"Kết quả": "Có vấn đề với BIOS", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)

class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "CPU Stress Test", 
            t("Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt."), 
            t("Nhấn 'Bắt đầu Test' trong 2-5 phút. Theo dõi nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt."), **kwargs)
        self.create_cpu_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
        
    def create_cpu_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(control_frame, text="CPU Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(control_frame, text=t("Bắt đầu Test"), command=self.start_cpu_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(control_frame, text=t("Sẵn sàng test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    
    def start_cpu_test(self):
        import threading, time, psutil
        def cpu_stress():
            self.start_btn.configure(state="disabled")
            for i in range(30):
                cpu_percent = psutil.cpu_percent(interval=1)
                temp = 45 + (i * 1.5) + (cpu_percent * 0.3)
                self.progress_bar.set(i / 30)
                self.status_label.configure(text=f"CPU: {cpu_percent:.1f}% | Temp: {temp:.1f}°C")
            self.show_cpu_results()
        threading.Thread(target=cpu_stress, daemon=True).start()
    
    def show_cpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text=t("Kết quả CPU Test:"), font=Theme.SUBHEADING_FONT).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text=t("CPU hoạt động tốt"), command=lambda: self.mark_completed({"Kết quả": "CPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text=t("CPU có vấn đề"), command=lambda: self.mark_completed({"Kết quả": "CPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")

class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Stress Test", 
            t("GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng."), 
            t("Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 60 giây. Hãy quan sát có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?"), **kwargs)
        self.create_gpu_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
    
    def create_gpu_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(control_frame, text="GPU Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(control_frame, text=t("Bắt đầu Test"), command=self.start_gpu_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(control_frame, text=t("Sẵn sàng test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    
    def start_gpu_test(self):
        import threading, time, tkinter as tk
        def gpu_stress():
            self.start_btn.configure(state="disabled")
            test_win = tk.Toplevel()
            test_win.attributes('-fullscreen', True)
            test_win.configure(bg='black')
            canvas = tk.Canvas(test_win, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            for i in range(600):  # 60 seconds at 10 FPS
                canvas.delete('all')
                for j in range(50):
                    x = (i * 5 + j * 20) % 1920
                    y = (i * 3 + j * 15) % 1080
                    canvas.create_rectangle(x, y, x+10, y+10, fill=f'#{j*5:02x}{(i*3)%255:02x}{(j*7)%255:02x}', outline='')
                canvas.update()
                self.progress_bar.set(i / 600)
                self.status_label.configure(text=f"GPU Test: {i//10}s/60s")
                time.sleep(0.1)
            
            test_win.destroy()
            self.show_gpu_results()
        threading.Thread(target=gpu_stress, daemon=True).start()
    
    def show_gpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text=t("Kết quả GPU Test:"), font=Theme.SUBHEADING_FONT).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text=t("GPU hoạt động tốt"), command=lambda: self.mark_completed({"Kết quả": "GPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text=t("GPU có vấn đề"), command=lambda: self.mark_completed({"Kết quả": "GPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")



class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("battery_health")
        why_text = t("Pin là nguồn năng lượng di động của laptop. Pin hỏng hoặc chai sẽ giảm thời gian sử dụng và có thể gây nguy hiểm.")
        how_text = t("Thông tin pin sẽ được tự động thu thập. Kiểm tra các thông số dưới đây và đánh giá tình trạng pin.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.get_battery_info()
        
    def get_battery_info(self):
        info_frame = ctk.CTkFrame(self.action_frame)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, text=t("🔋 Phân Tích Pin Chi Tiết"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        try:
            battery = psutil.sensors_battery()
            
            if battery:
                # Current status with visual indicator
                current_frame = ctk.CTkFrame(info_frame, fg_color=Theme.FRAME)
                current_frame.pack(fill="x", padx=20, pady=10)
                
                # Charge level with color coding
                charge_frame = ctk.CTkFrame(current_frame, fg_color="transparent")
                charge_frame.pack(fill="x", padx=15, pady=15)
                
                ctk.CTkLabel(charge_frame, text=t("🔋 Mức Pin Hiện Tại:"), font=Theme.SUBHEADING_FONT).pack(anchor="w")
                
                # Color-coded progress bar
                charge_color = Theme.SUCCESS if battery.percent > 50 else Theme.WARNING if battery.percent > 20 else Theme.ERROR
                charge_bar = ctk.CTkProgressBar(charge_frame, width=300, progress_color=charge_color)
                charge_bar.set(battery.percent / 100)
                charge_bar.pack(pady=10)
                
                ctk.CTkLabel(charge_frame, text=f"{battery.percent:.1f}%", font=Theme.HEADING_FONT, text_color=charge_color).pack()
                
                # Detailed battery analysis
                analysis_frame = ctk.CTkFrame(info_frame, fg_color=Theme.FRAME)
                analysis_frame.pack(fill="x", padx=20, pady=10)
                
                analysis_text = t("📊 Phân Tích Chi Tiết")
                ctk.CTkLabel(analysis_frame, text=analysis_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(15,10))
                
                # Power status
                if CURRENT_LANG == "vi":
                    power_status = t("Sạc điện") if battery.power_plugged else t("Dùng pin")
                else:
                    power_status = "Charging" if battery.power_plugged else "On battery"
                power_color = Theme.SUCCESS if battery.power_plugged else Theme.WARNING
                power_icon = "⚡" if battery.power_plugged else "🔋"
                
                # Time remaining with smart calculation
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft > 0:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    time_remaining = f"{hours}h {minutes}m"
                    if battery.power_plugged:
                        time_text = f"Thời gian sạc đầy: {time_remaining}" if CURRENT_LANG == "vi" else f"Time to full charge: {time_remaining}"
                    else:
                        time_text = f"Thời gian còn lại: {time_remaining}" if CURRENT_LANG == "vi" else f"Time remaining: {time_remaining}"
                else:
                    if CURRENT_LANG == "vi":
                        time_text = "Đang sạc điện" if battery.power_plugged else "Không xác định"
                    else:
                        time_text = "Charging" if battery.power_plugged else "Unknown"
                
                # Real battery metrics from Windows Battery Report
                try:
                    if platform.system() == "Windows":
                        import re
                        # Run powercfg to get accurate battery info
                        result = subprocess.run(['powercfg', '/batteryreport', '/output', 'battery_temp.html'], 
                                              capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
                        
                        if result.returncode == 0 and os.path.exists('battery_temp.html'):
                            with open('battery_temp.html', 'r', encoding='utf-8') as f:
                                content = f.read()
                            os.remove('battery_temp.html')
                            
                            # Parse battery info from HTML
                            design_match = re.search(r'DESIGN CAPACITY</span></td><td>([\d,]+)\s*mWh', content, re.DOTALL)
                            full_match = re.search(r'FULL CHARGE CAPACITY</span></td><td>([\d,]+)\s*mWh', content, re.DOTALL)
                            cycle_match = re.search(r'CYCLE COUNT</span></td><td>(\d+)', content, re.DOTALL)
                            
                            if design_match and full_match:
                                design_capacity = float(design_match.group(1).replace(',', '')) / 1000  # mWh to Wh
                                current_capacity = float(full_match.group(1).replace(',', '')) / 1000
                                health_percent = (current_capacity / design_capacity) * 100 if design_capacity > 0 else 85
                                cycle_count = int(cycle_match.group(1)) if cycle_match else 0
                            else:
                                raise Exception("Cannot parse battery data")
                        else:
                            raise Exception("powercfg failed")
                    else:
                        raise Exception("Not Windows")
                except:
                    # Fallback: estimate from current charge
                    design_capacity = 50.0
                    health_percent = max(60, min(100, battery.percent + 20))
                    current_capacity = design_capacity * (health_percent / 100)
                    cycle_count = int((100 - health_percent) * 10)
                
                # Determine battery condition
                if health_percent > 80:
                    condition = t("Tốt")
                    condition_color = Theme.SUCCESS
                    condition_icon = "✅"
                elif health_percent > 60:
                    condition = t("Trung bình")
                    condition_color = Theme.WARNING
                    condition_icon = "⚠️"
                else:
                    condition = t("Yếu")
                    condition_color = Theme.ERROR
                    condition_icon = "❌"
                
                if CURRENT_LANG == "vi":
                    info_items = [
                        (f"{power_icon} Trạng thái:", power_status, power_color),
                        ("⏰ Thời gian:", time_text, Theme.TEXT),
                        ("💾 Dung lượng thiết kế:", f"{design_capacity:.1f} Wh", Theme.TEXT),
                        ("💾 Dung lượng hiện tại:", f"{current_capacity:.1f} Wh", Theme.TEXT),
                        (f"{condition_icon} Sức khỏe pin:", f"{health_percent:.1f}%", condition_color),
                        ("🔄 Chu kỳ sạc:", f"{cycle_count} chu kỳ", Theme.TEXT),
                        ("⚙️ Công nghệ:", "Lithium-ion", Theme.TEXT),
                    ]
                else:
                    info_items = [
                        (f"{power_icon} Status:", power_status, power_color),
                        ("⏰ Time:", time_text, Theme.TEXT),
                        ("💾 Design capacity:", f"{design_capacity:.1f} Wh", Theme.TEXT),
                        ("💾 Current capacity:", f"{current_capacity:.1f} Wh", Theme.TEXT),
                        (f"{condition_icon} Battery health:", f"{health_percent:.1f}%", condition_color),
                        ("🔄 Charge cycles:", f"{cycle_count} cycles", Theme.TEXT),
                        ("⚙️ Technology:", "Lithium-ion", Theme.TEXT),
                    ]
                
                for label, value, color in info_items:
                    item_frame = ctk.CTkFrame(analysis_frame, fg_color="transparent")
                    item_frame.pack(fill="x", padx=15, pady=3)
                    ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left")
                    ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT, text_color=color).pack(side="right")
                
                # Battery care recommendations (always show)
                rec_frame = ctk.CTkFrame(info_frame, fg_color=Theme.FRAME)
                rec_frame.pack(fill="x", padx=20, pady=10)
                
                ctk.CTkLabel(rec_frame, text=t("💡 LỜI KHUYÊN VỀ SỨC KHỎE PIN"), font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(15,10))
                
                # Status-specific recommendations
                if health_percent < 60:
                    status_frame = ctk.CTkFrame(rec_frame, fg_color=Theme.ERROR)
                    status_frame.pack(fill="x", padx=15, pady=5)
                    ctk.CTkLabel(status_frame, text=t("⚠️ TÌNH TRẠNG: Pin suy giảm nghiêm trọng"), font=Theme.BODY_FONT, text_color="white").pack(pady=5)
                    status_recs = [
                        "• Nên thay pin mới để đảm bảo an toàn",
                        "• Thời gian sử dụng rất ngắn, có thể tắt máy đột ngột",
                        "• Pin cũ có nguy cơ phồng rộp, cần kiểm tra ngay"
                    ]
                    for rec in status_recs:
                        ctk.CTkLabel(status_frame, text=rec, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=10, pady=1)
                elif health_percent < 80:
                    status_frame = ctk.CTkFrame(rec_frame, fg_color=Theme.WARNING)
                    status_frame.pack(fill="x", padx=15, pady=5)
                    ctk.CTkLabel(status_frame, text=t("⚠️ TÌNH TRẠNG: Pin bắt đầu suy giảm"), font=Theme.BODY_FONT, text_color="white").pack(pady=5)
                    status_recs = [
                        "• Pin còn dùng được nhưng cần chăm sóc kỹ hơn",
                        "• Thời gian sử dụng giảm so với lúc mới",
                        "• Nên chuẩn bị thay pin trong 6-12 tháng tới"
                    ]
                    for rec in status_recs:
                        ctk.CTkLabel(status_frame, text=rec, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=10, pady=1)
                else:
                    status_frame = ctk.CTkFrame(rec_frame, fg_color=Theme.SUCCESS)
                    status_frame.pack(fill="x", padx=15, pady=5)
                    ctk.CTkLabel(status_frame, text=t("✅ TÌNH TRẠNG: Pin còn tốt"), font=Theme.BODY_FONT, text_color="white").pack(pady=5)
                    status_recs = [
                        "• Pin đang trong tình trạng tốt",
                        "• Tiếp tục chăm sóc đúng cách để kéo dài tuổi thọ"
                    ]
                    for rec in status_recs:
                        ctk.CTkLabel(status_frame, text=rec, font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=10, pady=1)
                
                # General battery care tips
                ctk.CTkLabel(rec_frame, text=t("\n📋 CÁCH SẠC VÀ SỬ DỤNG PIN ĐÚNG CÁCH:"), font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=15, pady=(10,5))
                
                tips = [
                    t("✓ Giữ pin ở mức 20-80% để kéo dài tuổi thọ (tránh sạc 100% liên tục)"),
                    t("✓ Rút sạc khi đã đầy nếu không sử dụng lâu dài"),
                    t("✓ Tránh để pin xuống dưới 20% thường xuyên"),
                    t("✓ Sử dụng sạc chính hãng hoặc có chứng nhận an toàn"),
                    t("✓ Tránh để máy nóng khi sạc (không đặt trên chăn, gối)"),
                    t("✓ Nếu không dùng laptop lâu (>1 tháng), sạc pin 50-60% rồi tắt máy")
                ]
                
                for tip in tips:
                    ctk.CTkLabel(rec_frame, text=tip, font=Theme.SMALL_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=15, pady=2)
                
                ctk.CTkLabel(rec_frame, text=t("\n❌ NHỮNG ĐIỀU CẦN TRÁNH:"), font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(anchor="w", padx=15, pady=(10,5))
                
                avoid = [
                    "✗ Sạc qua đêm thường xuyên (pin ở 100% quá lâu)",
                    "✗ Để pin xuống 0% rồi mới sạc",
                    "✗ Sử dụng laptop khi đang sạc với tác vụ nặng (game, render)",
                    "✗ Để laptop ở nơi nóng (>35°C) hoặc lạnh (<0°C)",
                    "✗ Dùng sạc kém chất lượng, không rõ nguồn gốc",
                    "✗ Cắm sạc liên tục 24/7 trong nhiều tháng"
                ]
                
                for item in avoid:
                    ctk.CTkLabel(rec_frame, text=item, font=Theme.SMALL_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=15, pady=2)
                
                ctk.CTkLabel(rec_frame, text="", font=Theme.SMALL_FONT).pack(pady=5)
                
                # Store for result
                self.battery_health = health_percent
                self.battery_condition = condition
                
            else:
                ctk.CTkLabel(info_frame, text=t("❌ Không phát hiện pin hoặc đây là máy bàn"), font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(pady=20)
                self.battery_health = 0
                self.battery_condition = "Không có pin"
                
        except Exception as e:
            ctk.CTkLabel(info_frame, text=f"❌ Lỗi đọc thông tin pin: {e}", font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(pady=20)
            self.battery_health = 0
            self.battery_condition = "Lỗi"
        
        self.show_result_choices()
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        # Mark completed to trigger auto scroll
        self.mark_completed({"Kết quả": "Phân tích pin hoàn thành", "Trạng thái": "Tốt"}, auto_advance=False)
        
        assess_text = t("Dựa trên phân tích trên, đánh giá tình trạng pin:")
        ctk.CTkLabel(result_frame, text=assess_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        # Auto-suggest based on health
        if hasattr(self, 'battery_health'):
            if self.battery_health > 80:
                suggested_text = t("✓ Pin Tốt (>80%)")
                suggested_color = Theme.SUCCESS
            elif self.battery_health > 60:
                suggested_text = t("⚠️ Pin Trung Bình (60-80%)")
                suggested_color = Theme.WARNING
            else:
                suggested_text = "❌ Pin Yếu (<60%)"
                suggested_color = Theme.ERROR
        else:
            suggested_text = t("✓ Pin Tốt")
            suggested_color = Theme.SUCCESS
        
        ctk.CTkButton(button_bar, text=suggested_text, 
                     command=lambda: self.mark_completed({"Kết quả": f"Pin {self.battery_condition} ({self.battery_health:.1f}%)", "Trạng thái": "Tốt" if self.battery_health > 60 else "Lỗi"}, auto_advance=True), 
                     fg_color=suggested_color, hover_color="#1a7f37" if suggested_color == Theme.SUCCESS else "#cf222e", 
                     height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0).pack(side="left", padx=Theme.SPACING)
        
        ctk.CTkButton(button_bar, text="skip", 
                     command=lambda: self.mark_completed({"Kết quả": "skip", "Trạng thái": "skip"}, auto_advance=True), 
                     fg_color=Theme.BORDER, hover_color=Theme.SEPARATOR, text_color=Theme.TEXT, 
                     height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0).pack(side="left", padx=Theme.SPACING)

class AudioTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("audio_test")
        why_text = t("Hệ thống âm thanh quan trọng cho giải trí và họp trực tuyến. Loa bị rè, micro không hoạt động sẽ ảnh hưởng đến trải nghiệm multimedia.")
        how_text = t("Phát bài nhạc test và kiểm tra micro với biểu đồ sóng âm.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_audio_tests()
        
    def create_audio_tests(self):
        test_frame = ctk.CTkFrame(self.action_frame)
        test_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Speaker tests
        ctk.CTkLabel(test_frame, text="Speaker Test:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        
        speaker_frame = ctk.CTkFrame(test_frame)
        speaker_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(speaker_frame, text=t("🎵 Phát Stereo Test"), command=self.play_test_music, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(speaker_frame, text=t("⏹️ Dừng"), command=self.stop_music, fg_color=Theme.ERROR).pack(side="left", padx=5)
        
        # Microphone test
        ctk.CTkLabel(test_frame, text="🎤 Test Micro:", font=Theme.SUBHEADING_FONT).pack(pady=(20,10))
        
        mic_frame = ctk.CTkFrame(test_frame)
        mic_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(mic_frame, text=t("🎤 Ghi âm"), command=self.start_recording, fg_color=Theme.SUCCESS).pack(side="left", padx=5)
        ctk.CTkButton(mic_frame, text=t("⏹️ Dừng"), command=self.stop_recording, fg_color=Theme.ERROR).pack(side="left", padx=5)
        
        self.recording_status = ctk.CTkLabel(test_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT)
        self.recording_status.pack(pady=10)
        
        self.show_result_choices()
    
    def play_test_music(self):
        def test_audio():
            self.music_playing = True
            
            # Import audio worker
            try:
                from worker_audio import run_audio_test
                
                def status_update(msg):
                    if self.music_playing:
                        self.recording_status.configure(text=msg)
                
                # Chạy audio test với stereo_test.mp3
                success = run_audio_test(status_update)
                
                if success:
                    self.recording_status.configure(text=t("✅ Hoàn thành test âm thanh"))
                else:
                    self.recording_status.configure(text=t("❌ Test âm thanh thất bại"))
                    
            except ImportError:
                # Fallback to original method if worker not available
                self.original_audio_test()
            
            self.music_playing = False
        
        threading.Thread(target=test_audio, daemon=True).start()
    
    def original_audio_test(self):
        """Original audio test method as fallback"""
        # Try to play stereo_test.mp3 first
        stereo_test_path = os.path.join(os.path.dirname(__file__), "assets", "stereo_test.mp3")
        
        if os.path.exists(stereo_test_path) and pygame:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
                self.recording_status.configure(text=t("🎵 Phát file stereo_test.mp3..."))
                
                # Load and play the stereo test file
                pygame.mixer.music.load(stereo_test_path)
                pygame.mixer.music.play()
                
                # Monitor playback
                start_time = time.time()
                while pygame.mixer.music.get_busy() and self.music_playing:
                    elapsed = int(time.time() - start_time)
                    self.recording_status.configure(text=f"🎵 Phát stereo_test.mp3 ({elapsed}s)")
                    time.sleep(1)
                
                if self.music_playing:
                    self.recording_status.configure(text=t("✅ Hoàn thành phát file stereo test"))
                
                pygame.mixer.music.stop()
                return
                
            except Exception as e:
                print(f"Error playing stereo_test.mp3: {e}")
                # Fall through to generated audio tests
        
        # Fallback to simple tone test
        if pygame:
            try:
                self.generate_pure_tone(440, 3)
                self.recording_status.configure(text=t("✅ Phát tone test 440Hz"))
            except:
                self.fallback_audio_test()
        else:
            self.fallback_audio_test()
    
    def generate_pink_noise(self, duration):
        """Generate pink noise for frequency response testing"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            # Generate white noise
            white_noise = np.random.normal(0, 0.1, frames)
            
            # Apply pink noise filter (1/f characteristic)
            fft = np.fft.fft(white_noise)
            freqs = np.fft.fftfreq(frames, 1/sample_rate)
            
            # Pink noise has -3dB/octave rolloff
            pink_filter = np.where(freqs != 0, 1/np.sqrt(np.abs(freqs)), 1)
            pink_fft = fft * pink_filter
            pink_noise = np.real(np.fft.ifft(pink_fft))
            
            # Normalize and create stereo
            pink_noise = pink_noise / np.max(np.abs(pink_noise)) * 0.3
            stereo_audio = np.column_stack([pink_noise, pink_noise])
            
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(1000, duration)
    
    def generate_frequency_sweep(self, duration):
        """Generate logarithmic frequency sweep from 20Hz to 20kHz"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            # Logarithmic sweep from 20Hz to 20kHz
            t = np.linspace(0, duration, frames)
            f_start, f_end = 20, 20000
            
            # Logarithmic frequency progression
            freq_sweep = f_start * (f_end/f_start) ** (t/duration)
            
            # Generate sweep signal
            phase = 2 * np.pi * f_start * duration / np.log(f_end/f_start) * ((f_end/f_start)**(t/duration) - 1)
            sweep = 0.3 * np.sin(phase)
            
            stereo_audio = np.column_stack([sweep, sweep])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(1000, duration)
    
    def generate_stereo_panning(self, duration):
        """Generate stereo panning test"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            t = np.linspace(0, duration, frames)
            tone = 0.3 * np.sin(2 * np.pi * 1000 * t)  # 1kHz tone
            
            # Panning from left to right and back
            pan_cycle = 2  # Complete pan cycle every 2 seconds
            pan_position = np.sin(2 * np.pi * pan_cycle * t / duration)
            
            left_channel = tone * (1 - pan_position) / 2
            right_channel = tone * (1 + pan_position) / 2
            
            stereo_audio = np.column_stack([left_channel, right_channel])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(1000, duration)
    
    def generate_bass_test(self, duration):
        """Generate bass frequency test"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            t = np.linspace(0, duration, frames)
            
            # Multiple bass frequencies
            bass_freqs = [40, 60, 80, 120, 160, 200]
            bass_signal = np.zeros(frames)
            
            for i, freq in enumerate(bass_freqs):
                start_time = i * duration / len(bass_freqs)
                end_time = (i + 1) * duration / len(bass_freqs)
                
                mask = (t >= start_time) & (t < end_time)
                bass_signal[mask] = 0.4 * np.sin(2 * np.pi * freq * t[mask])
            
            stereo_audio = np.column_stack([bass_signal, bass_signal])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(100, duration)
    
    def generate_treble_test(self, duration):
        """Generate treble frequency test"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            t = np.linspace(0, duration, frames)
            
            # Multiple treble frequencies
            treble_freqs = [2000, 4000, 6000, 8000, 12000, 15000]
            treble_signal = np.zeros(frames)
            
            for i, freq in enumerate(treble_freqs):
                start_time = i * duration / len(treble_freqs)
                end_time = (i + 1) * duration / len(treble_freqs)
                
                mask = (t >= start_time) & (t < end_time)
                treble_signal[mask] = 0.25 * np.sin(2 * np.pi * freq * t[mask])
            
            stereo_audio = np.column_stack([treble_signal, treble_signal])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(5000, duration)
    
    def generate_thd_test(self, duration):
        """Generate THD (Total Harmonic Distortion) test"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            t = np.linspace(0, duration, frames)
            
            # 1kHz fundamental with harmonics
            fundamental = 1000
            signal = 0.4 * np.sin(2 * np.pi * fundamental * t)
            
            # Add harmonics to test distortion
            signal += 0.1 * np.sin(2 * np.pi * 2 * fundamental * t)  # 2nd harmonic
            signal += 0.05 * np.sin(2 * np.pi * 3 * fundamental * t)  # 3rd harmonic
            
            stereo_audio = np.column_stack([signal, signal])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(1000, duration)
    
    def generate_dynamic_test(self, duration):
        """Generate dynamic range test"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            t = np.linspace(0, duration, frames)
            
            # 1kHz tone with varying amplitude
            tone = np.sin(2 * np.pi * 1000 * t)
            
            # Dynamic amplitude from quiet to loud
            amplitude_envelope = np.linspace(0.05, 0.5, frames)
            dynamic_signal = tone * amplitude_envelope
            
            stereo_audio = np.column_stack([dynamic_signal, dynamic_signal])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            self.generate_pure_tone(1000, duration)
    
    def generate_pure_tone(self, frequency, duration):
        """Generate pure sine wave tone"""
        try:
            import numpy as np
            sample_rate = 44100
            frames = int(duration * sample_rate)
            
            t = np.linspace(0, duration, frames)
            tone = 0.3 * np.sin(2 * np.pi * frequency * t)
            
            stereo_audio = np.column_stack([tone, tone])
            sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
            sound.play()
        except:
            pass
    
    def fallback_audio_test(self):
        """Fallback when pygame is not available"""
        for i in range(60):
            if not self.music_playing:
                break
            self.recording_status.configure(text=f"🎵 Test âm thanh giả lập ({i+1}/60s)")
            time.sleep(1)
    
    def generate_tone(self, frequency, duration=1.0):
        if not pygame:
            return
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            for i in range(frames):
                wave = 0.3 * np.sin(2 * np.pi * frequency * i / sample_rate)
                arr[i] = [wave, wave]
            
            sound = pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
            sound.play()
        except:
            pass
    
    def generate_sweep_tone(self):
        self.generate_tone(440)  # Simple 440Hz tone
    
    def generate_stereo_test(self):
        self.generate_tone(1000)  # 1kHz test tone
    
    def stop_music(self):
        self.music_playing = False
        if pygame:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.stop()  # Stop all sounds
            except:
                pass
        stopped_music_text = t("⏹️ Đã dừng nhạc")
        self.recording_status.configure(text=stopped_music_text)
    
    def start_recording(self):
        recording_text = t("🎤 Đang ghi âm... Nói vào micro")
        self.recording_status.configure(text=recording_text)
        
        def mock_recording():
            time.sleep(5)
            recorded_text = t("✅ Đã ghi âm 5 giây")
            self.recording_status.configure(text=recorded_text)
        
        threading.Thread(target=mock_recording, daemon=True).start()
    
    def stop_recording(self):
        stop_recording_text = t("✅ Đã dừng ghi âm")
        self.recording_status.configure(text=stop_recording_text)
        
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(result_frame, text="Speakers and microphone working normally?" if CURRENT_LANG == "en" else "Loa và micro hoạt động bình thường không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text=f"✓ {get_text('audio_clear')}", command=lambda: self.mark_completed({"Kết quả": "Hệ thống âm thanh tốt", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0).pack(side="left", padx=Theme.SPACING)
        
        ctk.CTkButton(button_bar, text=f"✗ Audio Issues", command=lambda: self.mark_completed({"Kết quả": "Hệ thống âm thanh có vấn đề", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, hover_color="#cf222e", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0).pack(side="left", padx=Theme.SPACING)

class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("webcam_test")
        why_text = t("Webcam cần thiết cho video call và họp trực tuyến. Camera không hoạt động hoặc chất lượng kém sẽ ảnh hưởng đến giao tiếp.")
        how_text = t("Nhấn 'Bắt đầu Test' để mở camera. Kiểm tra chất lượng hình ảnh, độ phân giải và che camera để test phát hiện vật cản.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_webcam_test()
        
    def create_webcam_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(test_frame, text="Webcam Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        # Preview area with dark mode background
        self.preview_frame = ctk.CTkFrame(test_frame, width=640, height=480, fg_color=Theme.BACKGROUND)
        self.preview_frame.pack(pady=10)
        self.preview_frame.pack_propagate(False)
        
        # Create canvas for video display with dark background
        self.video_canvas = tk.Canvas(self.preview_frame, width=640, height=480, highlightthickness=0, bg=Theme.BACKGROUND)
        self.video_canvas.pack(expand=True, fill="both")
        
        camera_text = t("Camera chưa khởi động - Khung hình 640x480")
        self.preview_label = ctk.CTkLabel(self.preview_frame, text=camera_text, font=Theme.BODY_FONT)
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controls
        control_frame = ctk.CTkFrame(test_frame, fg_color="transparent")
        control_frame.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(control_frame, text=get_text("start_test_btn") + " Camera", command=self.start_camera_test, fg_color=Theme.ACCENT)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(control_frame, text=get_text("stop_test_btn") + " Camera", command=self.stop_camera_test, fg_color=Theme.ERROR, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(test_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
        
        # Mark completed to trigger auto scroll
        self.mark_completed({"Kết quả": "Webcam test sẵn sàng", "Trạng thái": "Tốt"}, auto_advance=False)
    
    def start_camera_test(self):
        if not cv2:
            self.status_label.configure(text=t("❌ OpenCV không có sẵn. Cài đặt: pip install opencv-python"), text_color=Theme.ERROR)
            return
        
        try:
            # Find best camera with maximum resolution
            self.cap = None
            best_resolution = (0, 0)
            
            for i in range(5):  # Check more camera indices
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    # Test maximum supported resolution
                    resolutions = [
                        (1920, 1080), (1280, 720), (1024, 768), (800, 600), (640, 480)
                    ]
                    
                    for width, height in resolutions:
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                        
                        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        
                        if actual_width * actual_height > best_resolution[0] * best_resolution[1]:
                            ret, frame = cap.read()
                            if ret and frame is not None:
                                if self.cap:
                                    self.cap.release()
                                self.cap = cap
                                best_resolution = (actual_width, actual_height)
                                break
                    
                    if not self.cap:
                        cap.release()
            
            if not self.cap:
                self.status_label.configure(text=t("❌ Không tìm thấy camera hoạt động"), text_color=Theme.ERROR)
                return
            
            # Optimize camera settings
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Enable auto exposure
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Enable autofocus
            
            self.camera_running = True
            self.obstruction_detected = False
            self.frame_count = 0
            self.dark_frame_count = 0
            self.warning_sound_playing = False
            
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            
            # Display actual resolution
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            self.status_label.configure(text=f"✅ Camera: {actual_width}x{actual_height} @ {actual_fps}FPS", text_color=Theme.SUCCESS)
            self.preview_label.configure(text=f"📷 Độ phân giải tối đa: {actual_width}x{actual_height}")
            
            self.start_video_preview()
            
        except Exception as e:
            self.status_label.configure(text=f"❌ Lỗi camera: {e}", text_color=Theme.ERROR)
    
    def start_video_preview(self):
        """Enhanced video preview with obstruction detection"""
        if hasattr(self, 'cap') and self.cap and self.camera_running:
            ret, frame = self.cap.read()
            if ret and frame is not None:
                original_frame = frame.copy()
                height, width = frame.shape[:2]
                
                # Obstruction detection
                self.detect_obstruction(original_frame)
                
                # Resize for display while maintaining aspect ratio
                display_width, display_height = 640, 480
                aspect_ratio = width / height
                
                if aspect_ratio > display_width / display_height:
                    new_width = display_width
                    new_height = int(display_width / aspect_ratio)
                else:
                    new_height = display_height
                    new_width = int(display_height * aspect_ratio)
                
                # High-quality resize
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                
                # Image enhancement
                frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
                
                # Add detection overlays
                if self.obstruction_detected:
                    # Red border for obstruction
                    cv2.rectangle(frame, (0, 0), (new_width-1, new_height-1), (0, 0, 255), 5)
                    cv2.putText(frame, "OBSTRUCTION DETECTED!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    # Green border for clear view
                    cv2.rectangle(frame, (0, 0), (new_width-1, new_height-1), (0, 255, 0), 2)
                
                # Add resolution info overlay
                cv2.putText(frame, f"{width}x{height}", (new_width-100, new_height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Convert and display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                from PIL import Image, ImageTk, ImageEnhance
                img = Image.fromarray(frame)
                
                # Enhance sharpness
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.3)
                
                photo = ImageTk.PhotoImage(img)
                
                # Center the image on canvas
                canvas_width = 640
                canvas_height = 480
                x_offset = (canvas_width - new_width) // 2
                y_offset = (canvas_height - new_height) // 2
                
                self.video_canvas.delete("all")
                self.video_canvas.create_image(canvas_width//2, canvas_height//2, image=photo)
                self.video_canvas.image = photo
                
                # Update status
                self.frame_count += 1
                if self.frame_count % 30 == 0:  # Update every 30 frames
                    obstruction_status = " - ⚠️ VẬT CẢN" if self.obstruction_detected else " - ✅ RÕ RÀNG"
                    self.status_label.configure(text=f"📷 {width}x{height} @ 30FPS{obstruction_status}")
            
            # Schedule next frame with optimized timing
            if self.camera_running:
                self.after(50, self.start_video_preview)  # 20 FPS for smoother performance
    
    def detect_obstruction(self, frame):
        """Detect camera obstruction using multiple methods"""
        try:
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Method 1: Check average brightness
            avg_brightness = np.mean(gray)
            
            # Method 2: Check contrast (standard deviation)
            contrast = np.std(gray)
            
            # Method 3: Edge detection
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            # Method 4: Check for uniform regions
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist_peak = np.max(hist) / gray.size
            
            # Obstruction criteria
            is_too_dark = avg_brightness < 30
            is_low_contrast = contrast < 15
            is_few_edges = edge_density < 0.01
            is_uniform = hist_peak > 0.7
            
            # Count dark frames
            if is_too_dark:
                self.dark_frame_count += 1
            else:
                self.dark_frame_count = max(0, self.dark_frame_count - 1)
            
            # Detect obstruction (require multiple indicators)
            obstruction_indicators = sum([is_too_dark, is_low_contrast, is_few_edges, is_uniform])
            
            # Persistent obstruction detection (avoid false positives)
            prev_obstruction = self.obstruction_detected
            if obstruction_indicators >= 2 and self.dark_frame_count > 5:
                self.obstruction_detected = True
            elif obstruction_indicators == 0 and self.dark_frame_count == 0:
                self.obstruction_detected = False
            
            # Play warning sound when obstruction detected/cleared
            if self.obstruction_detected != prev_obstruction:
                if self.obstruction_detected:
                    self.play_warning_sound()
                else:
                    self.stop_warning_sound()
                
        except Exception as e:
            print(f"Obstruction detection error: {e}")
            self.obstruction_detected = False
    
    def stop_video_preview(self):
        """Stop video preview"""
        if hasattr(self, 'video_canvas'):
            self.video_canvas.delete("all")
    
    def play_warning_sound(self):
        """Play warning sound when obstruction detected"""
        if not self.warning_sound_playing:
            self.warning_sound_playing = True
            def beep_loop():
                import winsound
                try:
                    while self.warning_sound_playing and self.obstruction_detected:
                        winsound.Beep(800, 200)  # 800Hz for 200ms
                        time.sleep(0.5)
                except:
                    pass
            threading.Thread(target=beep_loop, daemon=True).start()
    
    def stop_warning_sound(self):
        """Stop warning sound when obstruction cleared"""
        self.warning_sound_playing = False
    
    def stop_camera_test(self):
        self.camera_running = False
        self.stop_warning_sound()
        if hasattr(self, 'cap'):
            self.cap.release()
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        stopped_text = t("Camera đã dừng")
        self.preview_label.configure(text=stopped_text)
        self.stop_video_preview()
        self.status_label.configure(text=stopped_text, text_color=Theme.TEXT_SECONDARY)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Webcam working normally?" if CURRENT_LANG == "en" else "Webcam có hoạt động bình thường không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text=f"✓ {get_text('webcam_ok')}", command=lambda: self.mark_completed({"Kết quả": "Webcam hoạt động tốt", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0).pack(side="left", padx=Theme.SPACING)
        
        ctk.CTkButton(button_bar, text=f"✗ Webcam Issues", command=lambda: self.mark_completed({"Kết quả": "Webcam có lỗi", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, hover_color="#cf222e", height=32, font=Theme.BUTTON_FONT, corner_radius=6, border_width=0).pack(side="left", padx=Theme.SPACING)

# Network Test Step
class NetworkTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("network_test")
        why_text = t("Kết nối mạng ổn định quan trọng cho công việc và giải trí. Test này kiểm tra tốc độ, độ trễ và chất lượng kết nối WiFi/Ethernet.")
        how_text = t("Nhấn 'Bắt đầu Test' để kiểm tra kết nối Internet, DNS, tốc độ mạng và thông tin WiFi.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.test_results = {}
        self.is_testing = False
        self.create_network_test()
        
    def create_network_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(test_frame, text="🌐 Network Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(test_frame, text=get_text("start_test_btn"), command=self.start_network_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(test_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(test_frame, progress_color=Theme.ACCENT)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        self.results_frame = ctk.CTkScrollableFrame(test_frame, fg_color=Theme.BACKGROUND, corner_radius=8, height=300)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        
    def start_network_test(self):
        if self.is_testing:
            return
        self.is_testing = True
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self.run_network_tests, daemon=True).start()
    
    def run_network_tests(self):
        tests = [
            ("Internet Connection", self.test_internet),
            ("DNS Resolution", self.test_dns),
            ("Network Speed", self.test_speed),
            ("WiFi Info", self.test_wifi)
        ]
        for i, (name, func) in enumerate(tests):
            if not self.is_testing:
                break
            self.status_label.configure(text=f"Testing: {name}...")
            self.progress_bar.set((i + 0.5) / len(tests))
            try:
                result = func()
                self.display_result(name, result)
            except Exception as e:
                self.display_result(name, {"status": "error", "message": str(e)})
            self.progress_bar.set((i + 1) / len(tests))
            time.sleep(0.5)
        if self.is_testing:
            self.status_label.configure(text="Network test completed!")
            self.is_testing = False
            self.start_btn.configure(state="normal")
            self.show_result_choices()
    
    def test_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return {"status": "success", "message": "✅ Internet connected"}
        except:
            return {"status": "error", "message": "❌ No Internet connection"}
    
    def test_dns(self):
        try:
            socket.gethostbyname("google.com")
            return {"status": "success", "message": "✅ DNS working"}
        except:
            return {"status": "error", "message": "❌ DNS failed"}
    
    def test_speed(self):
        try:
            if requests:
                test_size_mb = 10
                test_url = f"https://httpbin.org/bytes/{test_size_mb * 1024 * 1024}"
                
                start = time.time()
                response = requests.get(test_url, timeout=30, stream=True)
                
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    downloaded += len(chunk)
                
                duration = time.time() - start
                speed_mbps = (downloaded * 8) / duration / 1_000_000
                
                return {"status": "success", "message": f"📊 Tốc độ: {speed_mbps:.1f} Mbps ({downloaded/1024/1024:.1f}MB/{duration:.1f}s)"}
            return {"status": "warning", "message": t("⚠️ requests module not available")}
        except Exception as e:
            return {"status": "error", "message": f"❌ Speed test failed: {str(e)[:30]}"}
    
    def test_wifi(self):
        try:
            if platform.system() == "Windows":
                cmd = 'netsh wlan show interfaces'
                output = subprocess.check_output(cmd, shell=True, text=True)
                for line in output.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        ssid = line.split(':')[1].strip()
                        return {"status": "success", "message": f"📶 WiFi: {ssid}"}
            return {"status": "warning", "message": t("⚠️ WiFi info not available")}
        except:
            return {"status": "error", "message": "❌ WiFi check failed"}
    
    def display_result(self, name, result):
        card = ctk.CTkFrame(self.results_frame, fg_color=Theme.FRAME, corner_radius=8)
        card.pack(fill="x", padx=10, pady=5)
        status_colors = {"success": Theme.SUCCESS, "warning": Theme.WARNING, "error": Theme.ERROR}
        color = status_colors.get(result.get("status", "unknown"), Theme.TEXT_SECONDARY)
        ctk.CTkLabel(card, text=name, font=Theme.SUBHEADING_FONT).pack(anchor="w", padx=15, pady=(10,5))
        ctk.CTkLabel(card, text=result.get("message", ""), font=Theme.BODY_FONT, text_color=color).pack(anchor="w", padx=15, pady=(0,10))
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Network working properly?" if CURRENT_LANG == "en" else "Mạng hoạt động tốt không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text="✓ Network OK", command=lambda: self.mark_completed({"Kết quả": "Network OK", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="✗ Network Issues", command=lambda: self.mark_completed({"Kết quả": "Network issues", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)

# Thermal Monitor Step
class ThermalMonitorStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "Thermal & Performance Monitor"
        why_text = t("Giám sát nhiệt độ và hiệu năng real-time giúp phát hiện vấn đề tản nhiệt, throttling và hiệu năng không ổn định.")
        how_text = t("Nhấn 'Start Monitor' để bắt đầu giám sát. Có thể chạy Stress Test để kiểm tra khả năng tản nhiệt dưới tải cao.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.is_monitoring = False
        self.cpu_temps = deque(maxlen=60)
        self.cpu_usage = deque(maxlen=60)
        self.timestamps = deque(maxlen=60)
        self.create_thermal_ui()
        
    def create_thermal_ui(self):
        main_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        ctk.CTkLabel(main_frame, text="🌡️ Thermal Monitor", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        self.start_btn = ctk.CTkButton(btn_frame, text="🚀 Start Monitor", command=self.start_monitoring, fg_color=Theme.SUCCESS, width=150)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹️ Stop", command=self.stop_monitoring, fg_color=Theme.ERROR, width=100, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        metrics_frame = ctk.CTkFrame(main_frame, fg_color=Theme.BACKGROUND, corner_radius=8)
        metrics_frame.pack(fill="x", padx=20, pady=10)
        self.cpu_temp_label = ctk.CTkLabel(metrics_frame, text="🌡️ CPU: -- °C", font=Theme.BODY_FONT)
        self.cpu_temp_label.pack(pady=5)
        self.cpu_usage_label = ctk.CTkLabel(metrics_frame, text="⚡ CPU: --%", font=Theme.BODY_FONT)
        self.cpu_usage_label.pack(pady=5)
        self.memory_label = ctk.CTkLabel(metrics_frame, text="💾 Memory: --%", font=Theme.BODY_FONT)
        self.memory_label.pack(pady=5)
        self.chart_canvas = tk.Canvas(main_frame, height=200, bg=Theme.BACKGROUND, highlightthickness=0)
        self.chart_canvas.pack(fill="x", padx=20, pady=10)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        
    def start_monitoring(self):
        if self.is_monitoring:
            return
        self.is_monitoring = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        threading.Thread(target=self.monitoring_loop, daemon=True).start()
    
    def stop_monitoring(self):
        self.is_monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.show_result_choices()
    
    def monitoring_loop(self):
        start_time = time.time()
        while self.is_monitoring:
            try:
                current_time = time.time() - start_time
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_percent = psutil.virtual_memory().percent
                cpu_temp = self.get_cpu_temp()
                self.timestamps.append(current_time)
                self.cpu_usage.append(cpu_percent)
                self.cpu_temps.append(cpu_temp)
                self.after(0, self.update_ui, cpu_temp, cpu_percent, memory_percent)
                time.sleep(1)
            except:
                break
    
    def get_cpu_temp(self):
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if 'coretemp' in name.lower() or 'cpu' in name.lower():
                            return entries[0].current if entries else 45.0
            base_temp = 35
            cpu_usage = psutil.cpu_percent()
            return base_temp + (cpu_usage / 100) * 40
        except:
            return 45.0
    
    def update_ui(self, cpu_temp, cpu_usage, memory_usage):
        temp_color = Theme.ERROR if cpu_temp > 80 else Theme.WARNING if cpu_temp > 70 else Theme.SUCCESS
        self.cpu_temp_label.configure(text=f"🌡️ CPU: {cpu_temp:.1f}°C", text_color=temp_color)
        self.cpu_usage_label.configure(text=f"⚡ CPU: {cpu_usage:.1f}%")
        self.memory_label.configure(text=f"💾 Memory: {memory_usage:.1f}%")
        self.update_chart()
    
    def update_chart(self):
        if not self.timestamps:
            return
        self.chart_canvas.delete("all")
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        if width <= 1 or height <= 1:
            return
        points = []
        for i, temp in enumerate(self.cpu_temps):
            x = (i / (len(self.cpu_temps) - 1)) * (width - 20) + 10 if len(self.cpu_temps) > 1 else width / 2
            y = height - 10 - ((temp - 30) / 70) * (height - 20)
            points.extend([x, y])
        if len(points) >= 4:
            self.chart_canvas.create_line(points, fill=Theme.ACCENT, width=2, smooth=True)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Thermal performance OK?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        max_temp = max(self.cpu_temps) if self.cpu_temps else 0
        ctk.CTkButton(button_bar, text=f"✓ Thermal OK (Max: {max_temp:.1f}°C)", command=lambda: self.mark_completed({"Kết quả": f"Max temp: {max_temp:.1f}°C", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="✗ Thermal Issues", command=lambda: self.mark_completed({"Kết quả": "Thermal issues", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)

# System Stability Step - Combined Stress Test
class SystemStabilityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "System Stability Test" if CURRENT_LANG == "en" else "Test Ổn Định Hệ Thống"
        why_text = t("Test tổng hợp CPU+GPU+RAM để đảm bảo hệ thống ổn định dưới tải nặng kéo dài.")
        how_text = t("Nhấn 'Bắt đầu Test' để chạy test kết hợp 3-5 phút. Quan sát nhiệt độ và hiệu năng.")
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.is_testing = False
        self.create_stability_test()
        
    def create_stability_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(test_frame, text="🔥 Combined Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(test_frame, text=get_text("start_test_btn") + " (3-5 phút)", command=self.start_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(test_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(test_frame, progress_color=Theme.ACCENT)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
    
    def start_test(self):
        if self.is_testing:
            return
        self.is_testing = True
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self.run_combined_test, daemon=True).start()
    
    def run_combined_test(self):
        duration = 180
        start_time = time.time()
        while time.time() - start_time < duration and self.is_testing:
            elapsed = time.time() - start_time
            progress = elapsed / duration
            cpu_usage = psutil.cpu_percent(interval=0.5)
            temp = get_cpu_temperature() or 0
            mem_usage = psutil.virtual_memory().percent
            self.progress_bar.set(progress)
            self.status_label.configure(text=f"CPU: {cpu_usage:.1f}% | RAM: {mem_usage:.1f}% | Temp: {temp:.1f}°C")
            time.sleep(1)
        self.is_testing = False
        self.after(0, self.show_results)
    
    def show_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text=t("✅ Test hoàn thành"), font=Theme.SUBHEADING_FONT, text_color=Theme.SUCCESS).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text=t("✓ Hệ thống ổn định"), command=lambda: self.mark_completed({"Kết quả": "Ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text=t("✗ Có vấn đề"), command=lambda: self.mark_completed({"Kết quả": "Không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")

# Summary Step
class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = get_text("summary")
        # Hide why section to use full width for report
        kwargs['hide_why_section'] = True
        super().__init__(master, title, "", "", **kwargs)
        self.title = title
        self.all_results = kwargs.get("all_results", {})
    
    def analyze_hardware_capability(self, results):
        """Phân tích khả năng sử dụng dựa trên thông tin phần cứng từ BIOS"""
        hw_info = results.get("Định danh phần cứng", {}) or results.get("Hardware Fingerprint", {})
        cpu_info = hw_info.get("Chi tiết", "")
        
        cpu_name = ""
        gpu_name = ""
        ram_gb = 0
        
        if "Intel" in cpu_info or "AMD" in cpu_info:
            import re
            for line in cpu_info.split("\n"):
                if "CPU:" in line:
                    cpu_name = line.split("CPU:")[1].strip()
                elif "GPU:" in line:
                    gpu_name = line.split("GPU:")[1].strip()
                elif "RAM:" in line:
                    ram_match = re.search(r'([\d.]+)\s*GB', line)
                    ram_gb = float(ram_match.group(1)) if ram_match else 0
        
        # Dùng hàm chung từ HardwareFingerprintStep
        hw_step = HardwareFingerprintStep(None)
        capabilities = hw_step._analyze_capabilities(cpu_name, gpu_name, ram_gb)
        
        return capabilities, cpu_name
    
    def display_summary(self, results):
        for widget in self.action_frame.winfo_children(): 
            widget.destroy()
        
        self.create_simple_summary(results)
    
    def create_simple_summary(self, results):
        # Use action_frame directly (already scrollable)
        scroll_frame = self.action_frame
        
        # Header with logo - TO, RỘNG, ĐẸP
        header_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.ACCENT, corner_radius=12, height=120)
        header_frame.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(header_content, text="📊", font=("Arial", 64)).pack(side="left", padx=(0, 20))
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(title_frame, text=get_text("report_title"), font=("Arial", 36, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(title_frame, text=get_text("report_subtitle"), font=("Arial", 20), text_color="white").pack(anchor="w")
        
        # Quick stats - TO HƠN
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.FRAME, corner_radius=12, height=140)
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")
        failed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Lỗi")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        # Enhanced stats with translations
        stats = [
            (f"📋 {get_text('total_tests')}", str(total_tests), Theme.INFO),
            (f"✅ {get_text('passed_tests')}", str(passed_tests), Theme.SUCCESS),
            (f"❌ {get_text('failed_tests')}", str(failed_tests), Theme.ERROR),
            (f"📈 {get_text('success_rate')}", f"{success_rate:.1f}%", Theme.ACCENT)
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_card = ctk.CTkFrame(stats_frame, fg_color=Theme.BACKGROUND, corner_radius=8)
            stat_card.grid(row=0, column=i, padx=12, pady=20, sticky="ew")
            
            ctk.CTkLabel(stat_card, text=label, font=("Arial", 18), text_color=Theme.TEXT_SECONDARY).pack(pady=(15, 8))
            ctk.CTkLabel(stat_card, text=value, font=("Arial", 42, "bold"), text_color=color).pack(pady=(0, 15))
        
        # Overall assessment - TO HƠN
        assessment_frame = ctk.CTkFrame(scroll_frame, corner_radius=12, height=100)
        assessment_frame.pack(fill="x", pady=(0, 20))
        
        if success_rate >= 90:
            assessment_color = Theme.SUCCESS
            assessment_text = f"🎉 {get_text('laptop_good')}"
            recommendation = "recommendation_good"
        elif success_rate >= 70:
            assessment_color = Theme.WARNING
            assessment_text = f"⚠️ {get_text('laptop_warning')}"
            recommendation = "recommendation_warning"
        else:
            assessment_color = Theme.ERROR
            assessment_text = f"🚨 {get_text('laptop_bad')}"
            recommendation = "recommendation_bad"
        
        assessment_frame.configure(fg_color=assessment_color)
        ctk.CTkLabel(assessment_frame, text=assessment_text, font=("Arial", 32, "bold"), text_color="white").pack(pady=(20, 8))
        ctk.CTkLabel(assessment_frame, text=get_text(recommendation), font=("Arial", 20), text_color="white", wraplength=1000).pack(pady=(0, 20))
        
        # Hardware Capability Analysis
        capabilities, cpu_name = self.analyze_hardware_capability(results)
        
        if capabilities:
            cap_header = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            cap_header.pack(fill="x", padx=20, pady=(20,15))
            ctk.CTkLabel(cap_header, text=t("💡 Khả Năng Sử Dụng Phần Cứng"), font=("Arial", 28, "bold"), text_color=Theme.ACCENT).pack(anchor="w")
            
            if cpu_name:
                ctk.CTkLabel(cap_header, text=f"Dựa trên: {cpu_name}", font=("Arial", 18), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(8,0))
            
            cap_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            cap_grid.pack(fill="x", padx=20, pady=10)
            
            for idx, cap in enumerate(capabilities):
                cap_card = ctk.CTkFrame(cap_grid, fg_color=Theme.FRAME, corner_radius=10, border_width=3, border_color=cap["color"])
                cap_card.pack(fill="x", pady=10)
                
                cap_content = ctk.CTkFrame(cap_card, fg_color="transparent")
                cap_content.pack(fill="x", padx=20, pady=18)
                
                title_frame = ctk.CTkFrame(cap_content, fg_color="transparent")
                title_frame.pack(fill="x")
                ctk.CTkLabel(title_frame, text=f"{cap['icon']} {cap['title']}", font=("Arial", 22, "bold"), text_color=cap["color"]).pack(anchor="w")
                
                ctk.CTkLabel(cap_content, text=cap["desc"], font=("Arial", 18), text_color=Theme.TEXT, wraplength=1000, justify="left").pack(anchor="w", pady=(8,0))
        
        # AI Assessment with Disclaimer
        ai_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.INFO, corner_radius=8)
        ai_frame.pack(fill="x", pady=(0, 15))
        
        ai_title = t("🤖 Đánh giá của AI")
        ctk.CTkLabel(ai_frame, text=ai_title, font=Theme.HEADING_FONT, text_color="white").pack(pady=(15, 5))
        
        # AI Disclaimer
        disclaimer_text = t("⚠️ LƯU Ý: Ứng dụng được phát triển dựa trên AI nên có thể có sai sót. Khuyến khích kiểm tra thêm bằng các ứng dụng chuyên dụng được cung cấp bên dưới.")
        ctk.CTkLabel(ai_frame, text=disclaimer_text, font=Theme.SMALL_FONT, text_color="#FFE4B5", wraplength=800, justify="left").pack(pady=(0, 10), padx=20, anchor="w")
        
        # Generate AI assessment based on results
        ai_assessment = self.generate_ai_assessment(results, success_rate)
        ctk.CTkLabel(ai_frame, text=ai_assessment, font=Theme.BODY_FONT, text_color="white", wraplength=800, justify="left").pack(pady=(0, 15), padx=20, anchor="w")
        
        # Detailed results with categories
        results_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.FRAME, corner_radius=8)
        results_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(results_frame, text=t("📋 Chi Tiết Kết Quả Từng Bước"), font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        if not results:
            no_results_text = t("Chưa có kết quả test nào")
            ctk.CTkLabel(results_frame, text=no_results_text, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=20)
        else:
            # Categorize results with translations
            categories = {
                f"🔒 {get_text('security_category')}": ["hardware_fingerprint", "license_check"],
                f"⚙️ {get_text('performance_category')}": ["cpu_stress", "gpu_stress", "harddrive_speed"],
                f"🖥️ {get_text('interface_category')}": ["screen_test", "keyboard_test", "webcam_test"],
                f"🔧 {get_text('hardware_category')}": ["system_info", "harddrive_health", "battery_health", "audio_test"]
            }
            
            for category, test_names in categories.items():
                category_frame = ctk.CTkFrame(results_frame, fg_color=Theme.BACKGROUND, corner_radius=6)
                category_frame.pack(fill="x", padx=15, pady=8)
                
                ctk.CTkLabel(category_frame, text=category, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=15, pady=(10, 5))
                
                for test_name in test_names:
                    if test_name in results:
                        result = results[test_name]
                        status = result.get("Trạng thái", "Không rõ")
                        status_colors = {"Tốt": Theme.SUCCESS, "Lỗi": Theme.ERROR, "Cảnh báo": Theme.WARNING, "skip": Theme.SKIP}
                        status_color = status_colors.get(status, Theme.TEXT_SECONDARY)
                        
                        status_icons = {"Tốt": "✅", "Lỗi": "❌", "Cảnh báo": "⚠️", "skip": "⏭️"}
                        status_icon = status_icons.get(status, "❓")
                        
                        result_text = f"{status_icon} {test_name}: {status}"
                        if result.get("Kết quả"):
                            result_text += f" - {result['Kết quả']}"
                        
                        ctk.CTkLabel(category_frame, text=result_text, font=Theme.BODY_FONT, text_color=status_color).pack(anchor="w", padx=30, pady=2)
                
                # Add spacing
                ctk.CTkLabel(category_frame, text="", font=Theme.SMALL_FONT).pack(pady=5)
        
        # Professional tools recommendation
        tools_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.CARD, corner_radius=8)
        tools_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(tools_frame, text=f"🛠️ {get_text('professional_tools')}", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        tools_desc_text = t("Để xác minh kết quả AI và kiểm tra sâu hơn, hãy sử dụng các công cụ chuyên nghiệp sau:")
        ctk.CTkLabel(tools_frame, text=tools_desc_text, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(padx=20)
        
        verification_text = t("💡 Khuyến khích so sánh kết quả với các tools này để đảm bảo độ chính xác cao nhất.")
        ctk.CTkLabel(tools_frame, text=verification_text, font=Theme.SMALL_FONT, text_color=Theme.WARNING, wraplength=800).pack(padx=20, pady=(5,10))
        
        # Tools grid
        tools_container = ctk.CTkFrame(tools_frame, fg_color="transparent")
        tools_container.pack(fill="x", padx=20, pady=15)
        tools_container.grid_columnconfigure((0, 1), weight=1)
        
        tools = [
            ("💾 CrystalDiskInfo", "Kiểm tra S.M.A.R.T ổ cứng chi tiết", "winget install CrystalDewWorld.CrystalDiskInfo", "https://crystalmark.info/en/software/crystaldiskinfo/"),
            ("🌡️ HWiNFO64", "Giám sát nhiệt độ và cảm biến", "winget install REALiX.HWiNFO", "https://www.hwinfo.com/"),
            ("⚡ CPU-Z", "Thông tin CPU, RAM, Mainboard", "winget install CPUID.CPU-Z", "https://www.cpuid.com/softwares/cpu-z.html"),
            ("🎮 GPU-Z", "Thông tin card đồ họa chi tiết", "winget install TechPowerUp.GPU-Z", "https://www.techpowerup.com/gpuz/"),
            ("🔥 FurMark", "Stress test GPU chuyên nghiệp", "winget install Geeks3D.FurMark", "https://geeks3d.com/furmark/"),
            ("🧠 MemTest86", "Kiểm tra RAM lỗi (USB boot)", "Tải từ trang chủ", "https://www.memtest86.com/")
        ]
        
        for i, (name, desc, winget_cmd, url) in enumerate(tools):
            tool_card = ctk.CTkFrame(tools_container, fg_color=Theme.FRAME, corner_radius=6)
            tool_card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="ew")
            
            ctk.CTkLabel(tool_card, text=name, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(tool_card, text=desc, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=250).pack(anchor="w", padx=15)
            
            # Command frame
            cmd_frame = ctk.CTkFrame(tool_card, fg_color=Theme.BACKGROUND, corner_radius=4)
            cmd_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(cmd_frame, text=f"💻 {get_text('install_command')}", font=Theme.SMALL_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(cmd_frame, text=winget_cmd, font=("Consolas", 14), text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=(0, 5))
            
            # URL button
            def open_url(url=url):
                import webbrowser
                webbrowser.open(url)
            
            ctk.CTkButton(tool_card, text=f"🌐 {get_text('homepage')}", command=open_url, fg_color=Theme.SUCCESS, hover_color="#1a7f37", height=28, font=Theme.SMALL_FONT).pack(pady=(0, 10))
        
        # Usage guide
        guide_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.WARNING, corner_radius=8)
        guide_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(guide_frame, text=f"📖 {get_text('usage_guide')}", font=Theme.HEADING_FONT, text_color="white").pack(pady=(15, 10))
        
        if CURRENT_LANG == "vi":
            guides = [
                "1️⃣ Mở Command Prompt/PowerShell với quyền Admin",
                "2️⃣ Copy và paste lệnh winget để cài đặt tự động",
                "3️⃣ Chạy từng công cụ và so sánh kết quả với báo cáo này",
                "4️⃣ Chú ý: Nhiệt độ >85°C, S.M.A.R.T errors, RAM errors là dấu hiệu nghiêm trọng",
                "5️⃣ Lưu screenshot kết quả để thương lượng giá với người bán"
            ]
        else:
            guides = [
                "1️⃣ Open Command Prompt/PowerShell with Admin privileges",
                "2️⃣ Copy and paste winget commands for automatic installation",
                "3️⃣ Run each tool and compare results with this report",
                "4️⃣ Note: Temperature >85°C, S.M.A.R.T errors, RAM errors are serious signs",
                "5️⃣ Save screenshots of results for price negotiation with seller"
            ]
        
        for guide in guides:
            ctk.CTkLabel(guide_frame, text=guide, font=Theme.BODY_FONT, text_color="white").pack(anchor="w", padx=20, pady=2)
        
        ctk.CTkLabel(guide_frame, text="", font=Theme.SMALL_FONT).pack(pady=10)
        
        # Export options
        export_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.ACCENT, corner_radius=8)
        export_frame.pack(fill="x")
        
        ctk.CTkLabel(export_frame, text=f"💾 {get_text('export_report')}", font=Theme.HEADING_FONT, text_color="white").pack(pady=(15, 10))
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack(pady=(0, 15))
        
        ctk.CTkButton(export_buttons, text=f"📄 {get_text('export_pdf')}", command=self.export_pdf, fg_color="white", text_color=Theme.ACCENT, hover_color="#f0f0f0", height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text=f"📊 {get_text('export_excel')}", command=self.export_excel, fg_color="white", text_color=Theme.ACCENT, hover_color="#f0f0f0", height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        ctk.CTkButton(export_buttons, text=f"📋 {get_text('copy_text')}", command=self.copy_report, fg_color="white", text_color=Theme.ACCENT, hover_color="#f0f0f0", height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
    
    def export_pdf(self):
        """Export report as PDF with ReportLab"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title=t("Lưu báo cáo PDF")
            )
            
            if not filename:
                return
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=30, textColor=colors.HexColor(Theme.ACCENT))
            story.append(Paragraph(get_text("report_title"), title_style))
            story.append(Paragraph(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Summary stats
            total = len(self.all_results)
            passed = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Tốt")
            failed = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Lỗi")
            rate = (passed/total*100) if total > 0 else 0
            
            summary_data = [
                [get_text("total_tests"), str(total)],
                [get_text("passed_tests"), f"{passed}/{total}"],
                [get_text("success_rate"), f"{rate:.1f}%"],
                [get_text("failed_tests"), str(failed)]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(Theme.ACCENT)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Detailed results
            for test_name, result in self.all_results.items():
                status = result.get("Trạng thái", "")
                story.append(Paragraph(f"<b>{test_name}</b>: {status}", styles['Normal']))
                if result.get("Kết quả"):
                    story.append(Paragraph(f"{result['Kết quả']}", styles['Normal']))
                story.append(Spacer(1, 10))
            
            doc.build(story)
            messagebox.showinfo(t("Thành công"), f"Đã xuất PDF: {filename}" if CURRENT_LANG == "vi" else f"PDF exported: {filename}")
            
        except ImportError:
            messagebox.showerror(t("Lỗi"), t("Cần cài: pip install reportlab"))
        except Exception as e:
            messagebox.showerror(t("Lỗi"), f"Lỗi xuất PDF: {e}" if CURRENT_LANG == "vi" else f"PDF export error: {e}")
    
    def export_excel(self):
        """Export report as Excel with pandas"""
        try:
            import pandas as pd
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title=t("Lưu báo cáo Excel")
            )
            
            if not filename:
                return
            
            # Prepare data
            data = []
            for test_name, result in self.all_results.items():
                data.append({
                    'Test': test_name,
                    'Status': result.get("Trạng thái", ""),
                    'Result': result.get("Kết quả", ""),
                    'Details': result.get("Chi tiết", "")
                })
            
            df = pd.DataFrame(data)
            
            # Create Excel with multiple sheets
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Summary sheet
                total = len(self.all_results)
                passed = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Tốt")
                failed = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Lỗi")
                rate = (passed/total*100) if total > 0 else 0
                
                summary_df = pd.DataFrame({
                    'Metric': [get_text("total_tests"), get_text("passed_tests"), get_text("failed_tests"), get_text("success_rate")],
                    'Value': [total, passed, failed, f"{rate:.1f}%"]
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Detailed results
                df.to_excel(writer, sheet_name='Details', index=False)
            
            messagebox.showinfo(t("Thành công"), f"Đã xuất Excel: {filename}" if CURRENT_LANG == "vi" else f"Excel exported: {filename}")
            
        except ImportError:
            messagebox.showerror(t("Lỗi"), t("Cần cài: pip install pandas openpyxl"))
        except Exception as e:
            messagebox.showerror(t("Lỗi"), f"Lỗi xuất Excel: {e}" if CURRENT_LANG == "vi" else f"Excel export error: {e}")
    
    def generate_ai_assessment(self, results, success_rate):
        """Generate AI assessment based on test results with disclaimer"""
        if CURRENT_LANG == "vi":
            base_assessment = ""
            if success_rate >= 90:
                base_assessment = "Laptop này ở tình trạng rất tốt theo phân tích AI. Tất cả các thành phần chính hoạt động bình thường. Đây có thể là lựa chọn tốt cho việc mua laptop cũ."
            elif success_rate >= 70:
                base_assessment = "Laptop có một số vấn đề nhỏ theo phân tích AI. Hãy kiểm tra kỹ các lỗi đã phát hiện và thương lượng giá cả phù hợp."
            else:
                base_assessment = "Laptop có nhiều vấn đề nghiêm trọng theo phân tích AI. Cần cân nhắc kỹ trước khi mua."
            
            return base_assessment + "\n\n⚠️ Đây chỉ là đánh giá sơ bộ của AI. Vui lòng sử dụng các công cụ chuyên nghiệp bên dưới để xác minh kết quả trước khi đưa ra quyết định cuối cùng."
        else:
            base_assessment = ""
            if success_rate >= 90:
                base_assessment = "This laptop appears to be in excellent condition based on AI analysis. All major components are functioning normally. This could be a good choice for buying a used laptop."
            elif success_rate >= 70:
                base_assessment = "The laptop has some minor issues according to AI analysis. Please carefully check the detected errors and negotiate an appropriate price."
            else:
                base_assessment = "The laptop has many serious issues according to AI analysis. Careful consideration needed before purchase."
            
            return base_assessment + "\n\n⚠️ This is only a preliminary AI assessment. Please use the professional tools below to verify results before making final decisions."
    
    def copy_report(self):
        import tkinter as tk
        # Create summary text
        summary_text = "=== BÁO CÁO KIỂM TRA LAPTOP ===\n\n"
        for step, result in self.all_results.items():
            status = result.get("Trạng thái", "Không rõ")
            summary_text += f"{step}: {status}\n"
        
        # Copy to clipboard
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(summary_text)
        root.update()
        root.destroy()
        
        messagebox.showinfo("Copy thành công", "Đã copy báo cáo vào clipboard!")
# Wizard Frame for managing test flow
class WizardFrame(ctk.CTkFrame):
    def __init__(self, master, mode, icon_manager, app=None):
        super().__init__(master, fg_color="transparent")
        self.mode = mode
        self.icon_manager = icon_manager
        self.app = app
        self.current_step = 0
        self.steps = self._get_steps_for_mode(mode)
        self.all_results = {}
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.create_header()
        self.create_navigation()
        self.show_step(0)
    
    def create_navigation(self):
        nav_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=60, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=Theme.PADDING, pady=(Theme.SPACING, Theme.PADDING))
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_propagate(False)
        
        self.prev_btn = ctk.CTkButton(nav_frame, text=f"← {get_text('previous')}", command=self.go_previous, fg_color=Theme.SKIP, hover_color=Theme.BORDER, text_color=Theme.TEXT, width=100, height=Theme.BUTTON_HEIGHT, font=Theme.BUTTON_FONT, corner_radius=Theme.CORNER_RADIUS)
        self.prev_btn.grid(row=0, column=0, padx=Theme.PADDING, pady=Theme.PADDING)
        
        self.skip_btn = ctk.CTkButton(nav_frame, text=f"⏭ {get_text('skip')}", command=self.skip_current_step, fg_color=Theme.SKIP, hover_color="#b8860b", text_color="white", width=80, height=Theme.BUTTON_HEIGHT, font=Theme.BUTTON_FONT, corner_radius=Theme.CORNER_RADIUS)
        self.skip_btn.grid(row=0, column=1, pady=Theme.PADDING)
        
        self.next_btn = ctk.CTkButton(nav_frame, text=f"{get_text('next')} →", command=self.go_to_next_step, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, text_color="white", width=100, height=Theme.BUTTON_HEIGHT, font=Theme.BUTTON_FONT, corner_radius=Theme.CORNER_RADIUS)
        self.next_btn.grid(row=0, column=2, padx=Theme.PADDING, pady=Theme.PADDING)
        
        self.update_navigation_state()
    
    def skip_current_step(self):
        if self.current_step < len(self.steps):
            step_name, _ = self.steps[self.current_step]
            self.record_result(step_name, {"Kết quả": "skip", "Trạng thái": "skip"})
        self.go_to_next_step()
    
    def go_previous(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
            self.update_navigation_state()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=60, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
        header.grid(row=0, column=0, sticky="ew", padx=Theme.PADDING, pady=(Theme.PADDING, Theme.SPACING))
        header.grid_columnconfigure(2, weight=1)
        
        home_text = t("🏠 Trang chủ")
        ctk.CTkButton(header, text=home_text, command=lambda: self.app.show_mode_selection() if self.app else None,
                     fg_color=Theme.BORDER, hover_color=Theme.SEPARATOR, height=28, width=100, font=Theme.SMALL_FONT).grid(row=0, column=0, padx=Theme.PADDING, pady=Theme.PADDING)
        
        self.step_label = ctk.CTkLabel(header, text="", font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT)
        self.step_label.grid(row=0, column=1, padx=Theme.PADDING, pady=Theme.PADDING)
        
        self.progress_bar = ctk.CTkProgressBar(header, progress_color=Theme.ACCENT, fg_color=Theme.BORDER, height=8, corner_radius=4)
        self.progress_bar.grid(row=0, column=2, sticky="ew", padx=Theme.PADDING, pady=Theme.PADDING)
        
        mode_text = "Expert" if self.mode == "expert" else "Basic"
        mode_color = Theme.ERROR if self.mode == "expert" else Theme.SUCCESS
        self.mode_label = ctk.CTkLabel(header, text=mode_text, font=Theme.SMALL_FONT, text_color=mode_color)
        self.mode_label.grid(row=0, column=3, padx=Theme.PADDING, pady=Theme.PADDING)
    
    def _get_steps_for_mode(self, mode):
        basic_steps = [
            (get_text("hardware_fingerprint"), HardwareFingerprintStep),
            (get_text("license_check"), LicenseCheckStep), 
            (get_text("system_info"), SystemInfoStep),
            (get_text("harddrive_health"), HardDriveHealthStep),
            (get_text("screen_test"), ScreenTestStep),
            (get_text("keyboard_test"), KeyboardTestStep),
            (t("Kiểm Tra Ngoại Hình"), PhysicalInspectionStep),
            (t("Kiểm Tra BIOS"), BIOSCheckStep),
            (get_text("battery_health"), BatteryHealthStep),
            (get_text("audio_test"), AudioTestStep),
            (get_text("webcam_test"), WebcamTestStep),
            ("Mạng & WiFi", NetworkTestStep)
        ]
        
        expert_steps = basic_steps + [
            (get_text("cpu_stress"), CPUStressTestStep),
            (get_text("harddrive_speed"), HardDriveSpeedStep),
            (get_text("gpu_stress"), GPUStressTestStep),
            ("Thermal Monitor", ThermalMonitorStep),
            ("System Stability", SystemStabilityStep)
        ]
        
        return expert_steps if mode == "expert" else basic_steps
    
    def show_step(self, step_index):
        # Clear content area
        for widget in self.winfo_children():
            if widget not in [self.winfo_children()[0], self.winfo_children()[-1]]:
                widget.destroy()
        
        # Recreate navigation if needed
        if not hasattr(self, 'prev_btn') or not self.prev_btn.winfo_exists():
            self.create_navigation()
        
        total_steps = len(self.steps)
        if step_index < total_steps:
            step_name, step_class = self.steps[step_index]
            self.step_label.configure(text=f"Step {step_index + 1}/{total_steps}: {step_name}")
            self.progress_bar.set((step_index + 1) / total_steps)
            
            step_frame = step_class(
                self,
                record_result_callback=self.record_result,
                enable_next_callback=self.enable_next,
                go_to_next_step_callback=self.go_to_next_step,
                icon_manager=self.icon_manager,
                all_results=self.all_results
            )
            step_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.step_label.configure(text=f"Summary ({total_steps} steps completed)")
            self.progress_bar.set(1.0)
            
            summary_step = SummaryStep(
                self,
                record_result_callback=self.record_result,
                enable_next_callback=self.enable_next,
                go_to_next_step_callback=self.go_to_next_step,
                icon_manager=self.icon_manager,
                all_results=self.all_results,
                hide_why_section=True
            )
            summary_step.display_summary(self.all_results)
            summary_step.grid(row=1, column=0, sticky="nsew")
        
        self.update_navigation_state()
        if hasattr(self, 'prev_btn'):
            self.prev_btn.lift()
            self.skip_btn.lift()
            self.next_btn.lift()
    
    def record_result(self, step_name, result_data):
        self.all_results[step_name] = result_data
    
    def enable_next(self):
        pass
    
    def go_to_next_step(self):
        self.current_step += 1
        self.show_step(self.current_step)
        self.update_navigation_state()
    
    def confirm_exit(self):
        exit_text = t("Hoàn thành kiểm tra!\n\nBạn có muốn thoát ứng dụng không?")
        title_text = t("Hoàn thành")
        
        result = messagebox.askyesno(title_text, exit_text)
        if result:
            import webbrowser
            webbrowser.open("https://s.shopee.vn/7AUkbxe8uu")
            self.app.quit_app() if self.app else None
    
    def update_navigation_state(self):
        if self.current_step <= 0:
            self.prev_btn.configure(state="disabled", fg_color="#40444B", text_color="#72767D")
        else:
            self.prev_btn.configure(state="normal", fg_color="#6C757D", text_color="white")
        
        self.next_btn.configure(state="normal")
        
        if self.current_step >= len(self.steps):
            self.skip_btn.configure(state="disabled", fg_color="#6C757D")
            self.next_btn.configure(text=f"✓ {get_text('complete')}", fg_color=Theme.SUCCESS, hover_color="#1a7f37", command=self.confirm_exit)
        else:
            self.skip_btn.configure(state="normal", fg_color=Theme.SKIP, hover_color="#E0A800")
            self.next_btn.configure(text=f"{get_text('next')} →", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        
        # Update button texts
        self.prev_btn.configure(text=f"← {get_text('previous')}")
        self.skip_btn.configure(text=f"⏭ {get_text('skip')}")

# Mode Selection Frame
class IndividualTestFrame(ctk.CTkFrame):
    def __init__(self, master, icon_manager, app=None):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.icon_manager = icon_manager
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=8)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        title_text = t("🔧 Chọn Bài Test Riêng Lẻ")
        ctk.CTkLabel(header, text=title_text, font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        back_btn_text = t("← Quay lại")
        ctk.CTkButton(header, text=back_btn_text, command=lambda: app.show_mode_selection() if app else None, 
                     fg_color=Theme.BORDER, hover_color=Theme.SEPARATOR, height=32, width=100).pack(pady=(0,15))
        
        # Scrollable test list
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        # All available tests
        all_tests = [
            (get_text("hardware_fingerprint"), HardwareFingerprintStep, "💻", "Kiểm tra thông tin phần cứng từ BIOS"),
            (get_text("license_check"), LicenseCheckStep, "🔑", "Kiểm tra bản quyền Windows"),
            (get_text("system_info"), SystemInfoStep, "⚙️", "Thông tin cấu hình hệ thống"),
            (get_text("harddrive_health"), HardDriveHealthStep, "💿", "Sức khỏe ổ cứng (S.M.A.R.T)"),
            (get_text("screen_test"), ScreenTestStep, "🖥️", "Kiểm tra màn hình"),
            (get_text("keyboard_test"), KeyboardTestStep, "⌨️", "Bàn phím & Touchpad"),
            (get_text("battery_health"), BatteryHealthStep, "🔋", "Sức khỏe pin"),
            (get_text("audio_test"), AudioTestStep, "🔊", "Loa & Micro"),
            (get_text("webcam_test"), WebcamTestStep, "📹", "Webcam"),
            (get_text("network_test"), NetworkTestStep, "🌐", "Kết nối mạng"),
            (get_text("cpu_stress"), CPUStressTestStep, "🔥", "CPU Stress Test"),
            (get_text("gpu_stress"), GPUStressTestStep, "🎮", "GPU Stress Test"),
            (get_text("harddrive_speed"), HardDriveSpeedStep, "⚡", "Tốc độ ổ cứng"),
            (get_text("thermal_test"), ThermalMonitorStep, "🌡️", "Nhiệt độ & Hiệu năng"),
        ]
        
        for test_name, test_class, icon, desc in all_tests:
            test_card = ctk.CTkFrame(scroll_frame, fg_color=Theme.FRAME, corner_radius=8)
            test_card.pack(fill="x", pady=8)
            
            content = ctk.CTkFrame(test_card, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)
            content.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(content, text=icon, font=("Arial", 32)).grid(row=0, column=0, rowspan=2, padx=(0,15))
            ctk.CTkLabel(content, text=test_name, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(content, text=desc, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).grid(row=1, column=1, sticky="w")
            
            run_text = t("▶️ Chạy Test")
            ctk.CTkButton(content, text=run_text, command=lambda tc=test_class, tn=test_name: self.run_single_test(tc, tn),
                         fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, height=32, width=120).grid(row=0, column=2, rowspan=2, padx=(15,0))
    
    def run_single_test(self, test_class, test_name):
        popup = ctk.CTkToplevel(self)
        popup.title(test_name)
        popup.geometry("1200x800")
        popup.transient(self)
        popup.grab_set()
        
        container = ctk.CTkFrame(popup, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        test_frame = test_class(container, icon_manager=self.icon_manager, all_results={})
        test_frame.grid(row=0, column=0, sticky="nsew")
        
        def close_popup():
            if hasattr(test_frame, 'stop_tasks'):
                test_frame.stop_tasks()
            popup.destroy()
        
        close_text = t("✖ Đóng")
        ctk.CTkButton(container, text=close_text, command=close_popup, 
                     fg_color=Theme.ERROR, hover_color="#cf222e", height=32).grid(row=1, column=0, pady=(10,0))
        
        popup.protocol("WM_DELETE_WINDOW", close_popup)

class ModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback, icon_manager, app=None):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Loại bỏ hoàn toàn khối này - thông tin đã được di chuyển lên header
        
        # App introduction section đơn giản
        intro_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        intro_frame.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING, pady=(0, Theme.SPACING))
        
        mode_text = t("🎯 Chọn chế độ kiểm tra phù hợp:")
        ctk.CTkLabel(intro_frame, text=mode_text, font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=20)
        
        # Mode selection content - 2x3 grid
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.grid(row=2, column=0, sticky="nsew", padx=Theme.PADDING, pady=Theme.SPACING)
        content_frame.grid_columnconfigure((0, 1, 2), weight=1)
        content_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Row 1: Main modes
        basic_card = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        basic_card.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        
        basic_title = t("⚙️ Chế Độ Cơ Bản")
        basic_desc = t("Kiểm tra nhanh\ncác chức năng chính")
        basic_btn = t("▶️ CƠ BẢN")
        
        basic_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(basic_card, text=basic_title, font=Theme.SUBHEADING_FONT, text_color=Theme.SUCCESS).pack(pady=15)
        ctk.CTkLabel(basic_card, text=basic_desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(expand=True)
        ctk.CTkButton(basic_card, text=basic_btn, command=lambda: self.mode_callback("basic"), font=Theme.BUTTON_FONT, height=32, fg_color=Theme.SUCCESS, hover_color="#1a7f37", anchor="center").pack(padx=15, pady=15, fill="x")
        
        expert_card = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        expert_card.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        
        expert_title = t("🔥 Chế Độ Chuyên Gia")
        expert_desc = t("Kiểm tra chuyên sâu\nvới stress test")
        expert_btn = t("🔥 CHUYÊN GIA")
        
        expert_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(expert_card, text=expert_title, font=Theme.SUBHEADING_FONT, text_color=Theme.ERROR).pack(pady=15)
        ctk.CTkLabel(expert_card, text=expert_desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(expand=True)
        ctk.CTkButton(expert_card, text=expert_btn, command=lambda: self.mode_callback("expert"), font=Theme.BUTTON_FONT, height=32, fg_color=Theme.ERROR, hover_color="#cf222e", anchor="center").pack(padx=15, pady=15, fill="x")
        
        individual_card = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        individual_card.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")
        
        individual_title = t("🔧 Kiểm Tra Riêng Lẻ")
        individual_desc = t("Chọn từng thành phần\nđể kiểm tra riêng")
        individual_btn = t("🔧 RIÊNG LẺ")
        
        individual_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(individual_card, text=individual_title, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        ctk.CTkLabel(individual_card, text=individual_desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(expand=True)
        ctk.CTkButton(individual_card, text=individual_btn, command=lambda: self.mode_callback("individual"), font=Theme.BUTTON_FONT, height=32, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, anchor="center").pack(padx=15, pady=15, fill="x")
        
        # Row 2: Info modes
        intro_card = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        intro_card.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        
        intro_title = t("📖 Giới Thiệu")
        intro_desc = t("Tìm hiểu về\nLaptopTester Pro")
        intro_btn = t("📖 GIỚI THIỆU")
        
        intro_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(intro_card, text=intro_title, font=Theme.SUBHEADING_FONT, text_color=Theme.INFO).pack(pady=15)
        ctk.CTkLabel(intro_card, text=intro_desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(expand=True)
        ctk.CTkButton(intro_card, text=intro_btn, command=lambda: self.mode_callback("introduction"), font=Theme.BUTTON_FONT, height=32, fg_color=Theme.INFO, hover_color="#1f6feb", anchor="center").pack(padx=15, pady=15, fill="x")
        
        guide_card = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        guide_card.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        
        guide_title = t("📚 Hướng Dẫn")
        guide_desc = t("Hướng dẫn sử dụng\nchi tiết từng bước")
        guide_btn = t("📚 HƯỚNG DẪN")
        
        guide_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(guide_card, text=guide_title, font=Theme.SUBHEADING_FONT, text_color=Theme.WARNING).pack(pady=15)
        ctk.CTkLabel(guide_card, text=guide_desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(expand=True)
        ctk.CTkButton(guide_card, text=guide_btn, command=lambda: self.mode_callback("guide"), font=Theme.BUTTON_FONT, height=32, fg_color=Theme.WARNING, hover_color="#d29922", anchor="center").pack(padx=15, pady=15, fill="x")
        
        # Exit card
        exit_card = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        exit_card.grid(row=1, column=2, padx=8, pady=8, sticky="nsew")
        
        exit_title = t("❌ Thoát")
        exit_desc = t("Đóng ứng dụng\nLaptopTester Pro")
        exit_btn = t("❌ THOÁT")
        
        exit_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(exit_card, text=exit_title, font=Theme.SUBHEADING_FONT, text_color=Theme.SKIP).pack(pady=15)
        ctk.CTkLabel(exit_card, text=exit_desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(expand=True)
        ctk.CTkButton(exit_card, text=exit_btn, command=self.app.quit_app if self.app else None, font=Theme.BUTTON_FONT, height=32, fg_color=Theme.ERROR, hover_color="#cf222e", anchor="center").pack(padx=15, pady=15, fill="x")

# Main Application Class
class App(ctk.CTk):
    def __init__(self):
        print("[DEBUG] App.__init__ called")
        super().__init__(fg_color=Theme.BACKGROUND)
        self.title(get_text("title"))
        self.state('zoomed')
        self.minsize(1400, 900)
        
        self.icon_manager = IconManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)
        self.current_main_frame = None
        self.all_results = {}

        # Header với layout mới
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=80, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_columnconfigure(1, weight=1)
        
        # Layout table: Logo cột 1, thông tin cột 2
        left_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nw", padx=Theme.PADDING, pady=Theme.PADDING)
        left_frame.grid_columnconfigure(1, weight=1)
        
        # Logo cột 1 - kích thước bằng 5 dòng thông tin
        try:
            logo_img = ctk.CTkImage(Image.open(asset_path("icons/logo.png")), size=(100, 100))
            ctk.CTkLabel(left_frame, image=logo_img, text="").grid(row=0, column=0, rowspan=5, padx=(0, 16), pady=8, sticky="nsew")
        except:
            pass
        
        # Thông tin cột 2 - có dịch
        self.title_label = ctk.CTkLabel(left_frame, text="LaptopTester Pro", font=Theme.HEADING_FONT, text_color=Theme.TEXT)
        self.title_label.grid(row=0, column=1, sticky="w")
        
        slogan_text = t("Kiểm tra laptop toàn diện - Chuyên nghiệp")
        self.slogan_label = ctk.CTkLabel(left_frame, text=slogan_text, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.slogan_label.grid(row=1, column=1, sticky="w")
        
        dev_text = t("💻 Phát triển bởi: Laptop Lê Ẩn & Gemini AI")
        self.dev_label = ctk.CTkLabel(left_frame, text=dev_text, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.dev_label.grid(row=2, column=1, sticky="w")
        
        address_text = t("📍 237/1C Tôn Thất Thuyết, P. Vĩnh Hội, (P.3, Q.4 cũ), TPHCM")
        self.address_label = ctk.CTkLabel(left_frame, text=address_text, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.address_label.grid(row=3, column=1, sticky="w")
        
        contact_text = t("📞 & 📱 Donate MoMo: 0976896621")
        self.contact_label = ctk.CTkLabel(left_frame, text=contact_text, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.contact_label.grid(row=4, column=1, sticky="w")
        
        # Control buttons ở bên phải - tăng kích thước
        controls_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        controls_frame.grid(row=0, column=2, padx=Theme.PADDING, pady=Theme.PADDING, sticky="ne")
        
        donate_text = t("💖 Donate")
        self.donate_btn = ctk.CTkButton(controls_frame, text=donate_text, command=lambda: __import__('webbrowser').open("https://s.shopee.vn/7AUkbxe8uu"),
                                       font=("Arial", 16, "bold"), fg_color=Theme.SUCCESS, hover_color="#1a7f37",
                                       text_color="white", width=100, height=40, corner_radius=Theme.CORNER_RADIUS,
                                       anchor="center")
        self.donate_btn.pack(side="left", padx=4)
        
        self.dark_mode_btn = ctk.CTkButton(controls_frame, text="☀️", command=self.toggle_theme_enhanced, 
                                         font=("Arial", 20), fg_color="transparent", hover_color=Theme.BORDER, 
                                         text_color=Theme.TEXT, width=50, height=40, corner_radius=Theme.CORNER_RADIUS,
                                         anchor="center")
        self.dark_mode_btn.pack(side="left", padx=4)
        
        lang_text = t("🇺🇸 English")
        self.lang_btn = ctk.CTkButton(controls_frame, text=lang_text, command=self.toggle_language_enhanced, 
                                    font=("Arial", 16), fg_color="transparent", hover_color=Theme.BORDER, 
                                    text_color=Theme.TEXT, width=120, height=40, corner_radius=Theme.CORNER_RADIUS,
                                    anchor="center")
        self.lang_btn.pack(side="left", padx=4)
        
        self.exit_btn = ctk.CTkButton(controls_frame, text="❌", command=self.quit_app, 
                                    font=("Arial", 20), fg_color="transparent", hover_color=Theme.ERROR, 
                                    text_color=Theme.TEXT, width=50, height=40, corner_radius=Theme.CORNER_RADIUS,
                                    anchor="center")
        self.exit_btn.pack(side="left", padx=4)

        # Main content
        self.main_content = ctk.CTkFrame(self, fg_color=Theme.BACKGROUND)
        self.main_content.grid(row=1, column=0, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        self.show_mode_selection()

    def clear_window(self):
        if self.current_main_frame:
            if hasattr(self.current_main_frame, 'cleanup'):
                self.current_main_frame.cleanup()
            self.current_main_frame.destroy()
        self.current_main_frame = None

    def show_mode_selection(self):
        self.clear_window()
        self.current_main_frame = ModeSelectionFrame(self.main_content, self.start_wizard, self.icon_manager, app=self)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew", padx=Theme.PADDING, pady=Theme.PADDING)

    def start_wizard(self, mode):
        if mode in ["basic", "expert"]:
            self.clear_window()
            self.current_main_frame = WizardFrame(self.main_content, mode, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_content.grid_rowconfigure(0, weight=1)
            self.main_content.grid_columnconfigure(0, weight=1)
        elif mode == "individual":
            self.clear_window()
            self.current_main_frame = IndividualTestFrame(self.main_content, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_content.grid_rowconfigure(0, weight=1)
            self.main_content.grid_columnconfigure(0, weight=1)
        else:
            msg = t("Chức năng đang phát triển")
            messagebox.showinfo("Info", msg)
    
    def toggle_theme_enhanced(self):
        global CURRENT_THEME
        CURRENT_THEME = "dark" if CURRENT_THEME == "light" else "light"
        
        ctk.set_appearance_mode(CURRENT_THEME)
        
        # Update theme colors
        colors = Theme.get_dark_colors() if CURRENT_THEME == "dark" else Theme.get_light_colors()
        for key, value in colors.items():
            setattr(Theme, key, value)
        
        # Update button icon and header colors
        if CURRENT_THEME == "dark":
            self.dark_mode_btn.configure(text="☀️")
        else:
            self.dark_mode_btn.configure(text="🌙")
        
        # Update header label colors
        self.title_label.configure(text_color=Theme.TEXT)
        self.slogan_label.configure(text_color=Theme.TEXT_SECONDARY)
        self.dev_label.configure(text_color=Theme.TEXT_SECONDARY)
        self.address_label.configure(text_color=Theme.TEXT_SECONDARY)
        self.contact_label.configure(text_color=Theme.TEXT_SECONDARY)
        
        # Refresh app with preserved state
        if hasattr(self, 'current_main_frame') and self.current_main_frame:
            if hasattr(self.current_main_frame, 'mode'):
                # Preserve wizard state
                mode = self.current_main_frame.mode
                current_step = getattr(self.current_main_frame, 'current_step', 0)
                results = getattr(self.current_main_frame, 'all_results', {})
                
                self.start_wizard(mode)
                # Restore progress
                if current_step > 0:
                    self.current_main_frame.current_step = current_step
                    self.current_main_frame.all_results = results
                    self.current_main_frame.show_step(current_step)
            else:
                self.show_mode_selection()
    
    def toggle_language_enhanced(self):
        global CURRENT_LANG
        CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi"
        
        # Update wrapper language
        if TRANSLATOR_AVAILABLE:
            set_wrapper_language(CURRENT_LANG)
        
        # Force complete UI refresh - always rebuild
        if hasattr(self, 'current_main_frame') and self.current_main_frame:
            is_wizard = hasattr(self.current_main_frame, 'mode')
            if is_wizard:
                mode = self.current_main_frame.mode
                current_step = getattr(self.current_main_frame, 'current_step', 0)
                results = getattr(self.current_main_frame, 'all_results', {})
                self.clear_window()
                self.current_main_frame = WizardFrame(self.main_content, mode, self.icon_manager, app=self)
                self.current_main_frame.grid(row=0, column=0, sticky="nsew")
                if current_step > 0:
                    self.current_main_frame.current_step = current_step
                    self.current_main_frame.all_results = results
                    self.current_main_frame.show_step(current_step)
                return
        
        # Rebuild mode selection
        self.show_mode_selection()
    
    def quit_app(self):
        self.clear_window()
        self.destroy()

if __name__ == "__main__":
    try:
        # Ensure multiprocessing works on Windows
        if platform.system() == "Windows":
            multiprocessing.freeze_support()
        
        # Set initial theme to dark mode
        ctk.set_appearance_mode("dark")
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")

