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
import customtkinter as ctk
import tkinter as tk
import numpy as np
import webbrowser
from tkinter import messagebox
import logging
import tempfile
import keyboard
from collections import deque

# Language and theme globals
CURRENT_LANG = "vi"
CURRENT_THEME = "dark"

# Language dictionary
LANG = {
    "vi": {
        "title": "LaptopTester - Kiểm tra laptop toàn diện",
        "overview": "Tổng quan",
        "start_test": "Bắt đầu kiểm tra",
        "individual_test": "Kiểm tra từng thành phần",
        "user_guide": "Hướng dẫn sử dụng",
        "exit": "Thoát",
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
        "user_guide": "User Guide",
        "exit": "Exit",
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
    ctk.set_appearance_mode(CURRENT_THEME)

def toggle_language():
    global CURRENT_LANG
    CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi"

# Enhanced theme system
class Theme:
    @staticmethod
    def get_colors():
        if CURRENT_THEME == "dark":
            return {
                "BACKGROUND": "transparent", "FRAME": "#161b22", "CARD": "#0d1117", 
                "BORDER": "#30363d", "SEPARATOR": "#30363d",
                "TEXT": "#f0f6fc", "TEXT_SECONDARY": "#8b949e"
            }
        else:
            return {
                "BACKGROUND": "transparent", "FRAME": "#f6f8fa", "CARD": "#ffffff", 
                "BORDER": "#d0d7de", "SEPARATOR": "#d0d7de",
                "TEXT": "#24292f", "TEXT_SECONDARY": "#656d76"
            }
    
    ACCENT="#0969da"; ACCENT_HOVER="#0550ae"
    SUCCESS="#1a7f37"; WARNING="#9a6700"; ERROR="#cf222e"; SKIP="#656d76"; SKIP_HOVER="#424a53"
    INFO="#0969da"; GRADIENT_START="#0969da"; GRADIENT_END="#0550ae"
    
    @classmethod
    def get_bg(cls): return cls.get_colors()["BACKGROUND"]
    @classmethod
    def get_frame(cls): return cls.get_colors()["FRAME"]
    @classmethod
    def get_card(cls): return cls.get_colors()["CARD"]
    @classmethod
    def get_text(cls): return cls.get_colors()["TEXT"]
    @classmethod
    def get_text_secondary(cls): return cls.get_colors()["TEXT_SECONDARY"]
    
    TITLE_FONT=("Segoe UI", 40, "bold"); HEADING_FONT=("Segoe UI", 28, "bold"); SUBHEADING_FONT=("Segoe UI", 24, "bold")
    BODY_FONT=("Segoe UI", 18); SMALL_FONT=("Segoe UI", 16); KEY_FONT = ("Consolas", 16)
    CORNER_RADIUS = 8; PADDING_X = 20; PADDING_Y = 15; BUTTON_HEIGHT = 50
    CARD_PADDING = 20; SECTION_SPACING = 15; ELEMENT_SPACING = 10

class IconManager:
    def __init__(self):
        self.CHECK = None; self.CROSS = None; self.SKIP_ICON = None
        self.WHY = None; self.HOW = None; self.SHIELD = None

# Enhanced BaseStepFrame from original
class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.title = title
        self.record_result = kwargs.get("record_result_callback")
        self.enable_next_callback = kwargs.get("enable_next_callback")
        self.go_to_next_step_callback = kwargs.get("go_to_next_step_callback")
        self.icon_manager = kwargs.get("icon_manager")
        self.all_results = kwargs.get("all_results")
        
        self._completed, self._skipped = False, False
        self.after_id = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        
        # Compact guide container
        guide_container = ctk.CTkFrame(self, fg_color=Theme.get_frame(), corner_radius=Theme.CORNER_RADIUS)
        guide_container.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        guide_container.grid_columnconfigure(0, weight=1)
        guide_container.grid_rowconfigure(0, weight=1)
        guide_container.grid_rowconfigure(1, weight=1)
        
        why_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        why_frame.grid(row=0, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(why_frame, text="💡 Tại sao cần test?", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w")
        ctk.CTkLabel(why_frame, text=why_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.get_text()).pack(anchor="w", pady=(Theme.ELEMENT_SPACING,0))
        
        ctk.CTkFrame(guide_container, height=1, fg_color=Theme.get_colors()["SEPARATOR"]).grid(row=1, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.ELEMENT_SPACING)
        
        how_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        how_frame.grid(row=2, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(how_frame, text="📋 Hướng dẫn thực hiện:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w")
        ctk.CTkLabel(how_frame, text=how_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.get_text()).pack(anchor="w", pady=(Theme.ELEMENT_SPACING,0))
        
        # Action container
        action_container = ctk.CTkFrame(self, fg_color="transparent")
        action_container.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        action_container.grid_columnconfigure(0, weight=1)
        action_container.grid_rowconfigure(0, weight=1)
        
        self.action_frame = ctk.CTkFrame(action_container, fg_color=Theme.get_card(), corner_radius=Theme.CORNER_RADIUS)
        self.action_frame.grid(row=0, column=0, sticky="nsew")
        self.action_frame.grid_columnconfigure(0, weight=1)

    def is_ready_to_proceed(self): return self._completed or self._skipped
    def mark_completed(self, result_data, auto_advance=False):
        self._completed = True
        if self.record_result:
            self.record_result(self.title, result_data)
        if auto_advance and self.go_to_next_step_callback:
            self.go_to_next_step_callback()
    def mark_skipped(self, result_data): 
        self._skipped = True
        if self.record_result:
            self.record_result(self.title, result_data)
        if self.go_to_next_step_callback:
            self.go_to_next_step_callback()
    def stop_tasks(self): pass
    def handle_result_generic(self, is_ok, ok_data, bad_data):
        result = ok_data if is_ok else bad_data
        self.mark_completed(result, auto_advance=True)

# Test steps from original with compact interface
class HardwareFingerprintStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            "Định Danh Phần Cứng",
            "Đây là bước quan trọng nhất để chống lừa đảo. Các thông tin dưới đây được đọc trực tiếp từ BIOS và linh kiện phần cứng.",
            "Hãy so sánh các thông tin này với cấu hình mà người bán quảng cáo. Nếu có bất kỳ sự sai lệch nào, hãy đặt câu hỏi.",
            **kwargs
        )
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.info_labels = {}
        
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        self.loading_spinner.start()
        
        self.container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.container.grid_columnconfigure(1, weight=1)
        
        self.info_items = ["Model Laptop", "Serial Number", "CPU", "GPU", "Model Ổ Cứng", "Ngày BIOS"]
        for idx, item in enumerate(self.info_items):
            row_frame = ctk.CTkFrame(self.container, fg_color="transparent")
            row_frame.grid(row=idx, column=0, sticky="w", pady=10, padx=20)
            ctk.CTkLabel(row_frame, text="🛡️", font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(row_frame, text=f"{item}:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(side="left", padx=(0, 15))
            self.info_labels[item] = ctk.CTkLabel(row_frame, text="", justify="left", font=Theme.BODY_FONT, text_color=Theme.get_text_secondary(), wraplength=900)
            self.info_labels[item].pack(side="left")
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        
        threading.Thread(target=self.fetch_hardware_info, daemon=True).start()

    def fetch_hardware_info(self):
        hw_info = {k: "Đang đọc..." for k in self.info_items}
        if platform.system() == "Windows":
            pythoncom.CoInitializeEx(0)
            try:
                c = wmi.WMI()
                system_info = c.Win32_ComputerSystem()[0]
                hw_info["Model Laptop"] = f"{system_info.Manufacturer} {system_info.Model}"
                
                bios = c.Win32_BIOS()[0]
                hw_info["Serial Number"] = getattr(bios, 'SerialNumber', 'N/A')
                
                try:
                    bios_date = getattr(bios, 'ReleaseDate', '')
                    if bios_date and len(bios_date) >= 8:
                        bios_date_str = bios_date.split('.')[0]
                        hw_info["Ngày BIOS"] = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
                    else:
                        hw_info["Ngày BIOS"] = "Không xác định"
                except:
                    hw_info["Ngày BIOS"] = "Không đọc được"
                
                try:
                    processors = c.Win32_Processor()
                    if processors:
                        cpu_name = processors[0].Name.strip()
                        hw_info["CPU"] = cpu_name
                    else:
                        hw_info["CPU"] = "Không tìm thấy CPU"
                except Exception as e:
                    hw_info["CPU"] = f"Lỗi đọc CPU: {e}"
                
                try:
                    gpus = c.Win32_VideoController()
                    gpu_names = [gpu.Name for gpu in gpus if gpu.Name]
                    hw_info["GPU"] = "\\n".join(gpu_names) if gpu_names else "Không tìm thấy GPU"
                except:
                    hw_info["GPU"] = "Lỗi đọc GPU"
                
                try:
                    drives = c.Win32_DiskDrive()
                    drive_models = [d.Model for d in drives if d.Model]
                    hw_info["Model Ổ Cứng"] = "\\n".join(drive_models) if drive_models else "Không tìm thấy ổ cứng"
                except:
                    hw_info["Model Ổ Cứng"] = "Lỗi đọc ổ cứng"
                    
            except Exception as e: 
                hw_info = {k: f"Lỗi WMI: {e}" for k in self.info_items}
            finally: 
                pythoncom.CoUninitialize()
        else: 
            hw_info = {k: "Chỉ hỗ trợ Windows" for k in self.info_items}
        
        if self.winfo_exists(): 
            self.after(0, self.display_info, hw_info)

    def display_info(self, hw_info):
        full_details = ""
        self.loading_spinner.grid_remove()
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        for key, value in hw_info.items():
            if key in self.info_labels:
                self.info_labels[key].configure(text=value)
            full_details += f"  - {key}: {value}\\n"
        
        self.mark_completed({"Kết quả": "Đã lấy định danh phần cứng", "Trạng thái": "Tốt", "Chi tiết": f"Thông tin định danh phần cứng:\\n{full_details}"}, auto_advance=False)
        self.show_result_choices()
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Định danh phần cứng đã hoàn thành. Bạn có muốn tiếp tục?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text="Tiếp tục", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tiếp tục", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        
        self.btn_skip = ctk.CTkButton(button_bar, text="Bỏ qua", command=lambda: self.mark_skipped({"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"}), fg_color=Theme.SKIP, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)

class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bản Quyền Windows", "Một máy tính có bản quyền Windows hợp lệ đảm bảo bạn nhận được các bản cập nhật bảo mật quan trọng.", "Ứng dụng sẽ tự động chạy lệnh kiểm tra trạng thái kích hoạt của Windows.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.action_frame, text="Đang kiểm tra...", font=Theme.SUBHEADING_FONT, text_color=Theme.get_text_secondary())
        self.status_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        
        threading.Thread(target=self.check_license, daemon=True).start()

    def check_license(self):
        status, color, result_data = "Không thể kiểm tra", Theme.WARNING, {"Kết quả": "Không thể kiểm tra", "Trạng thái": "Lỗi"}
        if platform.system() == "Windows":
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                output_bytes = subprocess.check_output("cscript //Nologo C:\\\\Windows\\\\System32\\\\slmgr.vbs /xpr", shell=False, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
                try: 
                    result = output_bytes.decode('utf-8').lower()
                except UnicodeDecodeError: 
                    result = output_bytes.decode(locale.getpreferredencoding(), errors='ignore').lower()
                
                activated_strings = ["activated permanently", "kích hoạt vĩnh viễn", "the machine is permanently activated"]
                if any(s in result for s in activated_strings):
                    status, color, result_data = "Windows được kích hoạt vĩnh viễn", Theme.SUCCESS, {"Kết quả": "Đã kích hoạt vĩnh viễn", "Trạng thái": "Tốt"}
                elif "will expire" in result or "sẽ hết hạn" in result:
                    expiry_date = result.split("on")[-1].strip() if "on" in result else result.split(" vào ")[-1].strip()
                    status, color, result_data = f"Windows sẽ hết hạn vào {expiry_date}", Theme.WARNING, {"Kết quả": f"Sẽ hết hạn ({expiry_date})", "Trạng thái": "Lỗi"}
                else: 
                    status, color, result_data = "Windows chưa được kích hoạt", Theme.ERROR, {"Kết quả": "Chưa kích hoạt", "Trạng thái": "Lỗi"}
            except (subprocess.CalledProcessError, FileNotFoundError):
                status, color, result_data = "Lỗi khi chạy lệnh kiểm tra", Theme.ERROR, {"Kết quả": "Lỗi khi chạy lệnh kiểm tra", "Trạng thái": "Lỗi"}
        else:
            status, color, result_data = "Chỉ hỗ trợ Windows", Theme.SKIP, {"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"}
        
        if self.winfo_exists():
            self.after(0, self.update_ui, status, color, result_data)

    def update_ui(self, status, color, result_data):
        self.status_label.configure(text=status, text_color=color)
        self.mark_completed(result_data, auto_advance=False)
        self.show_result_choices()
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Kiểm tra bản quyền đã hoàn thành. Bạn có muốn tiếp tục?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text="Tiếp tục", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tiếp tục", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        
        self.btn_skip = ctk.CTkButton(button_bar, text="Bỏ qua", command=lambda: self.mark_skipped({"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"}), fg_color=Theme.SKIP, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)

# Continue with more test steps in next part...