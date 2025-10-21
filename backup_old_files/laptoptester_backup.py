import os
import sys
import time
import platform
import socket
import locale
import subprocess
import threading
import multiprocessing
from queue import Queue
from PIL import Image
import psutil
import pywifi
import pygame
import wmi
import pythoncom
import ai_analyzer  # Thêm module AI
from app_overview import AppOverviewFrame

import customtkinter as ctk
import tkinter as tk

# Language and theme globals
CURRENT_LANG = "vi"
CURRENT_THEME = "light"

# Language dictionary
LANG = {
    "vi": {
        "title": "LaptopTester - Kiểm tra laptop toàn diện",
        "overview": "Tổng quan",
        "start_test": "Bắt đầu kiểm tra",
        "individual_test": "Kiểm tra từng thành phần",
        "exit": "Thoát",
        "dark_mode": "Chế độ tối",
        "language": "Ngôn ngữ",
        "system_info": "Thông tin hệ thống",
        "license_check": "Kiểm tra bản quyền",
        "storage_test": "Kiểm tra ổ cứng",
        "display_test": "Kiểm tra màn hình",
        "keyboard_test": "Kiểm tra bàn phím",
        "ports_test": "Kiểm tra cổng kết nối",
        "battery_test": "Kiểm tra pin",
        "audio_test": "Kiểm tra âm thanh",
        "camera_test": "Kiểm tra camera",
        "cpu_test": "Kiểm tra CPU",
        "gpu_test": "Kiểm tra GPU",
        "memory_test": "Kiểm tra RAM",
        "thermal_test": "Kiểm tra nhiệt độ",
        "summary": "Tổng kết"
    },
    "en": {
        "title": "LaptopTester - Comprehensive Laptop Testing",
        "overview": "Overview",
        "start_test": "Start Test",
        "individual_test": "Individual Component Test",
        "exit": "Exit",
        "dark_mode": "Dark Mode",
        "language": "Language",
        "system_info": "System Information",
        "license_check": "License Check",
        "storage_test": "Storage Test",
        "display_test": "Display Test",
        "keyboard_test": "Keyboard Test",
        "ports_test": "Ports Test",
        "battery_test": "Battery Test",
        "audio_test": "Audio Test",
        "camera_test": "Camera Test",
        "cpu_test": "CPU Test",
        "gpu_test": "GPU Test",
        "memory_test": "Memory Test",
        "thermal_test": "Thermal Test",
        "summary": "Summary"
    }
}

def get_text(key):
    return LANG[CURRENT_LANG].get(key, key)

def toggle_theme():
    global CURRENT_THEME
    CURRENT_THEME = "dark" if CURRENT_THEME == "light" else "light"
    if CURRENT_THEME == "dark":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

def toggle_language():
    global CURRENT_LANG
    CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi"

# --- ENHANCED THEME & ASSETS ---
class Theme:
    # Colors - Modern design system
    BACKGROUND="#FAFBFC"; FRAME="#FFFFFF"; CARD="#F8FAFC"; BORDER="#E1E5E9"; SEPARATOR = "#F1F3F4"
    TEXT="#1A202C"; TEXT_SECONDARY="#718096"; ACCENT="#4299E1"; ACCENT_HOVER="#3182CE"
    SUCCESS="#38A169"; WARNING="#D69E2E"; ERROR="#E53E3E"; SKIP="#A0AEC0"; SKIP_HOVER="#718096"
    INFO="#3182CE"; GRADIENT_START="#667EEA"; GRADIENT_END="#764BA2"
    # Typography - Modern font system
    TITLE_FONT=("Segoe UI", 32, "bold"); HEADING_FONT=("Segoe UI", 24, "bold"); SUBHEADING_FONT=("Segoe UI", 18, "bold")
    BODY_FONT=("Segoe UI", 14); SMALL_FONT=("Segoe UI", 12); KEY_FONT = ("Consolas", 11)
    # Layout - Compact spacing
    CORNER_RADIUS = 12; PADDING_X = 20; PADDING_Y = 16; BUTTON_HEIGHT = 40
    CARD_PADDING = 16; SECTION_SPACING = 12; ELEMENT_SPACING = 8
import numpy as np
import webbrowser
from tkinter import messagebox
import logging
import tempfile
import keyboard
from collections import deque
from worker_disk import run_benchmark as run_disk_benchmark
from worker_cpu import run_cpu_stress_test
from worker_gpu import run_gpu_stress

# Utility function for asset path
def asset_path(rel_path):
    return os.path.join(os.path.dirname(__file__), 'assets', rel_path)

# Logger setup
logger = logging.getLogger("laptoptester")
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)


# --- THEME AND ICON MANAGER ---

class IconManager:
    def __init__(self):
        self.CHECK = self._load_icon("icons/checkmark.png", (30, 30)); self.CROSS = self._load_icon("icons/cross.png", (30, 30))
        self.SKIP_ICON = self._load_icon("icons/skip.png", (30, 30)); self.WHY = self._load_icon("icons/lightbulb.png", (32, 32))
        self.HOW = self._load_icon("icons/checklist.png", (32, 32)); self.SHIELD = self._load_icon("icons/shield.png", (32, 32))
        self.BASIC_MODE = self._load_icon("icons/new_basic_mode.png", (100, 100)); self.EXPERT_MODE = self._load_icon("icons/new_expert_mode.png", (100, 100))
        self.ARROW_LEFT = self._load_icon("icons/new_arrow_left.png", (26, 26)); self.ARROW_RIGHT = self._load_icon("icons/new_arrow_right.png", (26, 26))
        self.SKIP_ARROW = self._load_icon("icons/new_skip_arrow.png", (26, 26)); self.HOME = self._load_icon("icons/home.png", (26, 26))
        self.EXPORT = self._load_icon("icons/export.png", (26, 26)); self.WIFI = self._load_icon("icons/wifi.png", (26, 26))
        self.CPU = self._load_icon("icons/cpu.png", (32, 32)); self.GPU = self._load_icon("icons/gpu.png", (32, 32))
        self.HDD = self._load_icon("icons/hdd.png", (32, 32))
        self.LOGO_SMALL = self._load_icon("icons/logo.png", (48, 48))

    def _load_icon(self, path, size):
        try: return ctk.CTkImage(Image.open(asset_path(path)), size=size)
        except Exception: return None

if __name__ == "__main__":
    try:
        # Set initial theme
        ctk.set_appearance_mode(CURRENT_THEME)
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()