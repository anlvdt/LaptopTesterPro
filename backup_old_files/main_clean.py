#!/usr/bin/env python3
"""
LaptopTester Pro - Clean Main File
"""

import os
import sys
import time
import platform
import threading
import multiprocessing
import tempfile
import math
import logging
from queue import Queue
import webbrowser
from tkinter import messagebox
import tkinter as tk

# Third-party imports
import customtkinter as ctk
import psutil
import numpy as np
from PIL import Image

# Optional imports
try:
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

# Configuration
CURRENT_LANG = "vi"
CURRENT_THEME = "dark"

# Language Dictionary
LANG = {
    "vi": {
        "title": "LaptopTester Pro - Kiểm tra laptop toàn diện",
        "overview": "Tổng quan",
        "start_test": "Bắt đầu",
        "individual_test": "Test riêng lẻ", 
        "exit": "Thoát",
        "dark_mode": "Tối",
        "language": "Ngôn ngữ",
        "basic_mode": "Cơ bản",
        "expert_mode": "Chuyên gia",
        "hardware_fingerprint": "Định danh phần cứng",
        "license_check": "Bản quyền Windows",
        "system_info": "Cấu hình hệ thống",
        "harddrive_health": "Sức khỏe ổ cứng",
        "screen_test": "Kiểm tra màn hình",
        "keyboard_test": "Bàn phím & Touchpad",
        "battery_health": "Pin laptop",
        "audio_test": "Loa & Micro",
        "webcam_test": "Webcam",
        "cpu_stress": "CPU Stress Test",
        "harddrive_speed": "Tốc độ ổ cứng",
        "gpu_stress": "GPU Stress Test",
        "summary": "Tổng kết",
        "continue": "Tiếp tục",
        "skip": "Bỏ qua",
        "good": "Tốt",
        "error": "Lỗi",
        "previous": "Trước",
        "next": "Tiếp theo",
        "complete": "Hoàn thành",
        "ready": "Sẵn sàng",
        "checking": "Đang kiểm tra",
        "testing": "Đang test",
        "loading": "Đang tải",
        "finished": "Đã xong",
        "start_test_btn": "Bắt đầu Test",
        "stop_test_btn": "Dừng Test",
        "clear_canvas": "Xóa vết vẽ",
        "all_good": "Tất cả đều tốt",
        "config_match": "Cấu hình khớp",
        "mismatch": "Có sai lệch",
        "screen_ok": "Màn hình bình thường",
        "input_ok": "Thiết bị nhập tốt",
        "audio_clear": "Âm thanh rõ ràng",
        "webcam_ok": "Webcam hoạt động tốt",
        "cpu_good": "CPU ổn định",
        "gpu_good": "GPU ổn định",
        "battery_good": "Pin tốt",
        "ready_to_test": "Sẵn sàng test",
        "status_good": "Tốt",
        "status_error": "Lỗi",
        "status_warning": "Cảnh báo",
        "status_skip": "Bỏ qua"
    },
    "en": {
        "title": "LaptopTester Pro - Comprehensive Laptop Testing",
        "overview": "Overview",
        "start_test": "Start",
        "individual_test": "Individual",
        "exit": "Exit",
        "dark_mode": "Dark",
        "language": "Language",
        "basic_mode": "Basic",
        "expert_mode": "Expert",
        "hardware_fingerprint": "Hardware Fingerprint",
        "license_check": "Windows License",
        "system_info": "System Info",
        "harddrive_health": "HDD Health",
        "screen_test": "Screen Test",
        "keyboard_test": "Keyboard & Touchpad",
        "battery_health": "Battery Health",
        "audio_test": "Audio Test",
        "webcam_test": "Webcam Test",
        "cpu_stress": "CPU Stress Test",
        "harddrive_speed": "HDD Speed",
        "gpu_stress": "GPU Stress Test",
        "summary": "Summary",
        "continue": "Continue",
        "skip": "Skip",
        "good": "Good",
        "error": "Error",
        "previous": "Previous",
        "next": "Next",
        "complete": "Complete",
        "ready": "Ready",
        "checking": "Checking",
        "testing": "Testing",
        "loading": "Loading",
        "finished": "Finished",
        "start_test_btn": "Start Test",
        "stop_test_btn": "Stop Test",
        "clear_canvas": "Clear Drawing",
        "all_good": "All good",
        "config_match": "Config matches",
        "mismatch": "Mismatch detected",
        "screen_ok": "Screen normal",
        "input_ok": "Input devices OK",
        "audio_clear": "Audio clear",
        "webcam_ok": "Webcam working",
        "cpu_good": "CPU stable",
        "gpu_good": "GPU stable",
        "battery_good": "Battery good",
        "ready_to_test": "Ready to test",
        "status_good": "Good",
        "status_error": "Error",
        "status_warning": "Warning",
        "status_skip": "Skipped"
    }
}

def get_text(key):
    return LANG[CURRENT_LANG].get(key, key)

def toggle_theme():
    global CURRENT_THEME
    CURRENT_THEME = "dark" if CURRENT_THEME == "light" else "light"
    ctk.set_appearance_mode(CURRENT_THEME)

def toggle_language():
    global CURRENT_LANG
    CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi"

# Theme System
class Theme:
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
    SKIP = "#6e7681"
    INFO = "#58a6ff"
    
    TITLE_FONT = ("Segoe UI", 36, "bold")
    HEADING_FONT = ("Segoe UI", 28, "bold")
    SUBHEADING_FONT = ("Segoe UI", 22, "bold")
    BODY_FONT = ("Segoe UI", 20)
    SMALL_FONT = ("Segoe UI", 18)
    BUTTON_FONT = ("Segoe UI", 19, "bold")
    CODE_FONT = ("Consolas", 19)
    
    CORNER_RADIUS = 6
    PADDING = 12
    BUTTON_HEIGHT = 36
    CARD_PADDING = 16
    SPACING = 8

# Simple App Class
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=Theme.BACKGROUND)
        self.title(get_text("title"))
        self.state('zoomed')
        self.minsize(1200, 800)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_main_content()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=60, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        # Title
        ctk.CTkLabel(header, text="💻 LaptopTester Pro", font=Theme.HEADING_FONT, text_color=Theme.TEXT).grid(row=0, column=0, padx=Theme.PADDING, pady=Theme.PADDING)
        
        # Controls
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.grid(row=0, column=2, padx=Theme.PADDING, pady=Theme.PADDING)
        
        ctk.CTkButton(controls, text="🌙", command=self.toggle_theme, width=40, height=32).pack(side="left", padx=Theme.SPACING)
        ctk.CTkButton(controls, text="VI", command=self.toggle_language, width=40, height=32).pack(side="left", padx=Theme.SPACING)
        ctk.CTkButton(controls, text="✕", command=self.quit, width=32, height=32, fg_color=Theme.ERROR).pack(side="left", padx=Theme.SPACING)
    
    def create_main_content(self):
        main = ctk.CTkFrame(self, fg_color=Theme.BACKGROUND)
        main.grid(row=1, column=0, sticky="nsew")
        
        # Welcome message
        welcome = ctk.CTkFrame(main, fg_color=Theme.ACCENT, corner_radius=8)
        welcome.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(welcome, text="🎉 Chào mừng đến với LaptopTester Pro!", font=Theme.HEADING_FONT, text_color="white").pack(pady=20)
        ctk.CTkLabel(welcome, text="Phần mềm kiểm tra laptop chuyên nghiệp", font=Theme.BODY_FONT, text_color="white").pack(pady=(0,20))
        
        # Mode selection
        modes = ctk.CTkFrame(main, fg_color=Theme.FRAME)
        modes.pack(fill="both", expand=True, padx=20, pady=20)
        modes.grid_columnconfigure((0,1), weight=1)
        
        # Basic mode
        basic = ctk.CTkFrame(modes, fg_color=Theme.CARD)
        basic.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        
        ctk.CTkLabel(basic, text="⚙️ " + get_text("basic_mode"), font=Theme.SUBHEADING_FONT, text_color=Theme.SUCCESS).pack(pady=15)
        ctk.CTkLabel(basic, text="Kiểm tra nhanh các chức năng chính", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=10)
        ctk.CTkButton(basic, text="Chọn chế độ cơ bản", command=lambda: self.start_test("basic"), fg_color=Theme.SUCCESS, height=40).pack(pady=20)
        
        # Expert mode  
        expert = ctk.CTkFrame(modes, fg_color=Theme.CARD)
        expert.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        
        ctk.CTkLabel(expert, text="🔥 " + get_text("expert_mode"), font=Theme.SUBHEADING_FONT, text_color=Theme.ERROR).pack(pady=15)
        ctk.CTkLabel(expert, text="Kiểm tra chuyên sâu với stress test", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=10)
        ctk.CTkButton(expert, text="Chọn chế độ chuyên gia", command=lambda: self.start_test("expert"), fg_color=Theme.ERROR, height=40).pack(pady=20)
    
    def start_test(self, mode):
        messagebox.showinfo("Thông báo", f"Bắt đầu test ở chế độ {mode}")
    
    def toggle_theme(self):
        toggle_theme()
        # Refresh UI colors here if needed
    
    def toggle_language(self):
        toggle_language()
        # Refresh UI text here if needed
        self.title(get_text("title"))

if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            multiprocessing.freeze_support()
        
        ctk.set_appearance_mode(CURRENT_THEME)
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()