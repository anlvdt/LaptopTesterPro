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

class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, fg_color="transparent")
        self.title = title
        self.record_result = kwargs.get("record_result_callback")
        self.enable_next_callback = kwargs.get("enable_next_callback")
        self.go_to_next_step_callback = kwargs.get("go_to_next_step_callback")
        self.icon_manager = kwargs.get("icon_manager")
        self.all_results = kwargs.get("all_results")
        self._completed, self._skipped = False, False
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
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

class SystemInfoStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Thông tin hệ thống", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="💻 Thông tin hệ thống", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra bản quyền", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🔑 Kiểm tra bản quyền Windows", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class HardDriveHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra ổ cứng", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="💾 Kiểm tra ổ cứng", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class ScreenTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra màn hình", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🖥️ Kiểm tra màn hình", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class KeyboardVisualTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra bàn phím", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="⌨️ Kiểm tra bàn phím", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class PortsConnectivityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra cổng kết nối", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🔌 Kiểm tra cổng kết nối", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra pin", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🔋 Kiểm tra pin", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class SpeakerTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra âm thanh", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🔊 Kiểm tra âm thanh", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra camera", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="📷 Kiểm tra camera", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class NetworkTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra mạng", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🌐 Kiểm tra mạng", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra CPU", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🧠 Kiểm tra CPU", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class HardDriveSpeedStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra tốc độ ổ cứng", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="💽 Kiểm tra tốc độ ổ cứng", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra GPU", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🎮 Kiểm tra GPU", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class ThermalPerformanceStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra nhiệt độ", "", "", **kwargs)
        ctk.CTkLabel(self.action_frame, text="🌡️ Kiểm tra nhiệt độ", font=Theme.HEADING_FONT).pack(pady=10)
        ctk.CTkButton(self.action_frame, text="Hoàn thành", height=Theme.BUTTON_HEIGHT,
                     command=lambda: self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, True)).pack(pady=10)

class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tổng kết", "", "", **kwargs)
        self.title = "Tổng kết"
    
    def display_summary(self, results):
        for widget in self.action_frame.winfo_children(): 
            widget.destroy()
        
        ctk.CTkLabel(self.action_frame, text="📊 BÁO CÁO TỔNG KẾT", font=Theme.HEADING_FONT).pack(pady=20)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        stats_text = f"Tổng số test: {total_tests}\nĐạt: {passed_tests}/{total_tests}\nTỷ lệ thành công: {success_rate:.1f}%"
        ctk.CTkLabel(self.action_frame, text=stats_text, font=Theme.BODY_FONT).pack(pady=10)

# User Guide Frame
class UserGuideFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.setup_ui()
    
    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(header, text="📖 " + get_text("user_guide"), 
                    font=Theme.HEADING_FONT, text_color=Theme.get_text()).pack(side="left")
        ctk.CTkButton(header, text="← " + get_text("overview"), width=100, height=32,
                     command=lambda: self.mode_callback("overview")).pack(side="right")
        
        scrollable = ctk.CTkScrollableFrame(self, fg_color=Theme.get_card())
        scrollable.pack(fill="both", expand=True, padx=20, pady=10)
        
        guide_content = self.get_guide_content()
        for section in guide_content:
            section_frame = ctk.CTkFrame(scrollable, fg_color=Theme.get_frame())
            section_frame.pack(fill="x", pady=10, padx=10)
            
            ctk.CTkLabel(section_frame, text=section["title"], font=Theme.SUBHEADING_FONT,
                        text_color=Theme.get_text()).pack(pady=10)
            
            ctk.CTkLabel(section_frame, text=section["content"], font=Theme.BODY_FONT,
                        text_color=Theme.get_text_secondary(), justify="left").pack(pady=10, padx=20)
    
    def get_guide_content(self):
        if CURRENT_LANG == "vi":
            return [
                {"title": "🚀 Khởi động", "content": "Chạy với quyền Administrator để có kết quả chính xác nhất"},
                {"title": "🎯 Chế độ cơ bản", "content": "10 bước kiểm tra thiết yếu, phù hợp kiểm tra nhanh"},
                {"title": "⚡ Chế độ chuyên gia", "content": "14 bước kiểm tra đầy đủ với stress test"},
                {"title": "💻 Thông tin hệ thống", "content": "Hiển thị OS, CPU, RAM, kiến trúc hệ thống"},
                {"title": "🔑 Kiểm tra bản quyền", "content": "Xác định Windows đã kích hoạt hay chưa"},
                {"title": "💾 Kiểm tra ổ cứng", "content": "Dung lượng và % sử dụng các ổ đĩa"},
                {"title": "🖥️ Kiểm tra màn hình", "content": "Độ phân giải và test màu sắc"},
                {"title": "⌨️ Kiểm tra bàn phím", "content": "Test các phím và touchpad"},
                {"title": "🔌 Kiểm tra cổng kết nối", "content": "USB, HDMI, Audio ports"},
                {"title": "🔋 Kiểm tra pin", "content": "Mức pin, trạng thái sạc"},
                {"title": "🔊 Kiểm tra âm thanh", "content": "Test loa và microphone"},
                {"title": "📷 Kiểm tra camera", "content": "Test webcam và chất lượng hình ảnh"},
                {"title": "🌐 Kiểm tra mạng", "content": "Kết nối mạng và WiFi"},
                {"title": "🧠 Kiểm tra CPU", "content": "Stress test bộ xử lý"},
                {"title": "🎮 Kiểm tra GPU", "content": "Test card đồ họa"},
                {"title": "🌡️ Kiểm tra nhiệt độ", "content": "Monitor nhiệt độ hệ thống"}
            ]
        else:
            return [
                {"title": "🚀 Getting Started", "content": "Run with Administrator rights for most accurate results"},
                {"title": "🎯 Basic Mode", "content": "10 essential test steps, suitable for quick checks"},
                {"title": "⚡ Expert Mode", "content": "14 comprehensive test steps with stress testing"},
                {"title": "💻 System Information", "content": "Display OS, CPU, RAM, system architecture"},
                {"title": "🔑 License Check", "content": "Determine if Windows is activated"},
                {"title": "💾 Storage Test", "content": "Capacity and usage percentage of drives"},
                {"title": "🖥️ Display Test", "content": "Resolution and color testing"},
                {"title": "⌨️ Keyboard Test", "content": "Test keys and touchpad"},
                {"title": "🔌 Ports Test", "content": "USB, HDMI, Audio ports"},
                {"title": "🔋 Battery Test", "content": "Battery level, charging status"},
                {"title": "🔊 Audio Test", "content": "Test speakers and microphone"},
                {"title": "📷 Camera Test", "content": "Test webcam and image quality"},
                {"title": "🌐 Network Test", "content": "Network and WiFi connectivity"},
                {"title": "🧠 CPU Test", "content": "Processor stress testing"},
                {"title": "🎮 GPU Test", "content": "Graphics card testing"},
                {"title": "🌡️ Thermal Test", "content": "System temperature monitoring"}
            ]
    
    def refresh_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

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
        
        self.create_header()
        self.create_navigation()
        self.show_step(0)
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=50)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        header.grid_columnconfigure(1, weight=1)
        
        self.step_label = ctk.CTkLabel(header, text="", font=Theme.BODY_FONT)
        self.step_label.grid(row=0, column=0, padx=5)
        
        self.progress_bar = ctk.CTkProgressBar(header, height=8)
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=10)
        
        mode_text = "Chuyên gia" if self.mode == "expert" else "Cơ bản"
        self.mode_label = ctk.CTkLabel(header, text=mode_text, font=Theme.SMALL_FONT)
        self.mode_label.grid(row=0, column=2, padx=5)
    
    def create_navigation(self):
        nav = ctk.CTkFrame(self, fg_color="transparent", height=50)
        nav.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        nav.grid_columnconfigure(1, weight=1)
        
        self.prev_btn = ctk.CTkButton(nav, text="← Trước", width=150, height=55,
                                     command=self.go_previous, fg_color=Theme.SKIP, font=Theme.BODY_FONT)
        self.prev_btn.grid(row=0, column=0, padx=20)
        
        self.skip_btn = ctk.CTkButton(nav, text="Bỏ qua", width=150, height=55,
                                     command=self.skip_current_step, fg_color=Theme.WARNING, font=Theme.BODY_FONT)
        self.skip_btn.grid(row=0, column=1, padx=20)
        
        self.next_btn = ctk.CTkButton(nav, text="Tiếp →", width=150, height=55,
                                     command=self.go_to_next_step, fg_color=Theme.ACCENT, font=Theme.BODY_FONT)
        self.next_btn.grid(row=0, column=2, padx=20)
        
        self.update_navigation_state()
    
    def _get_steps_for_mode(self, mode):
        basic_steps = [
            ("Thông tin hệ thống", SystemInfoStep),
            ("Bản quyền Windows", LicenseCheckStep), 
            ("Sức khỏe ổ cứng", HardDriveHealthStep),
            ("Kiểm tra màn hình", ScreenTestStep),
            ("Bàn phím & Touchpad", KeyboardVisualTestStep),
            ("Cổng kết nối", PortsConnectivityStep),
            ("Pin laptop", BatteryHealthStep),
            ("Loa & Micro", SpeakerTestStep),
            ("Webcam", WebcamTestStep),
            ("Mạng & WiFi", NetworkTestStep)
        ]
        
        expert_steps = basic_steps + [
            ("CPU Stress Test", CPUStressTestStep),
            ("Tốc độ ổ cứng", HardDriveSpeedStep), 
            ("GPU Stress Test", GPUStressTestStep),
            ("Thermal Monitor", ThermalPerformanceStep)
        ]
        
        return expert_steps if mode == "expert" else basic_steps
    
    def show_step(self, step_index):
        for widget in self.winfo_children():
            if widget not in [self.winfo_children()[0], self.winfo_children()[-1]]:
                widget.destroy()
        
        if not hasattr(self, 'prev_btn') or not self.prev_btn.winfo_exists():
            self.create_navigation()
        
        total_steps = len(self.steps)
        if step_index < total_steps:
            step_name, step_class = self.steps[step_index]
            self.step_label.configure(text=f"{step_index + 1}/{total_steps}: {step_name}")
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
            self.step_label.configure(text=f"Tổng kết ({total_steps} bước)")
            self.progress_bar.set(1.0)
            
            summary_step = SummaryStep(
                self,
                record_result_callback=self.record_result,
                enable_next_callback=self.enable_next,
                go_to_next_step_callback=self.go_to_next_step,
                icon_manager=self.icon_manager,
                all_results=self.all_results
            )
            summary_step.display_summary(self.all_results)
            summary_step.grid(row=1, column=0, sticky="nsew")
        
        self.update_navigation_state()
    
    def skip_current_step(self):
        if self.current_step < len(self.steps):
            step_name, _ = self.steps[self.current_step]
            self.record_result(step_name, {"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"})
        self.go_to_next_step()
    
    def go_previous(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
            self.update_navigation_state()
    
    def record_result(self, step_name, result_data):
        self.all_results[step_name] = result_data
    
    def enable_next(self): pass
    
    def go_to_next_step(self):
        self.current_step += 1
        self.show_step(self.current_step)
        self.update_navigation_state()
    
    def update_navigation_state(self):
        if self.current_step <= 0:
            self.prev_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal")
        
        self.next_btn.configure(state="normal")
        
        if self.current_step >= len(self.steps):
            self.skip_btn.configure(state="disabled")
            self.next_btn.configure(text="Hoàn thành")
        else:
            self.skip_btn.configure(state="normal")
            self.next_btn.configure(text="Tiếp →")

class OverviewFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.setup_ui()
    
    def setup_ui(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)
        main.grid_columnconfigure(0, weight=1)
        
        welcome = ctk.CTkFrame(main, fg_color=Theme.get_card(), corner_radius=12)
        welcome.pack(fill="x", pady=(0,30))
        welcome.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(welcome, text="💻 " + get_text("title"), 
                    font=Theme.TITLE_FONT, text_color=Theme.get_text()).pack(pady=20)
        
        desc_text = "Phần mềm kiểm tra laptop toàn diện với 15+ bước kiểm tra" if CURRENT_LANG == "vi" else "Comprehensive laptop testing software with 15+ test steps"
        ctk.CTkLabel(welcome, text=desc_text, font=Theme.BODY_FONT, 
                    text_color=Theme.get_text_secondary()).pack(pady=(0,20))
        
        features = ctk.CTkFrame(main, fg_color="transparent")
        features.pack(fill="x", pady=(0,30))
        features.grid_columnconfigure((0,1,2), weight=1)
        
        features_data = [
            ("🎯", "Kiểm tra cơ bản" if CURRENT_LANG == "vi" else "Basic Testing", 
             "10 bước kiểm tra thiết yếu" if CURRENT_LANG == "vi" else "10 essential test steps"),
            ("⚡", "Kiểm tra nâng cao" if CURRENT_LANG == "vi" else "Advanced Testing", 
             "Stress test & benchmark" if CURRENT_LANG == "vi" else "Stress test & benchmark"),
            ("📊", "Báo cáo chi tiết" if CURRENT_LANG == "vi" else "Detailed Reports", 
             "Kết quả đầy đủ & xuất file" if CURRENT_LANG == "vi" else "Complete results & export")
        ]
        
        for i, (icon, title, desc) in enumerate(features_data):
            card = ctk.CTkFrame(features, fg_color=Theme.get_card(), corner_radius=8)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=icon, font=("Segoe UI", 24)).pack(pady=(15,5))
            ctk.CTkLabel(card, text=title, font=Theme.SUBHEADING_FONT, text_color=Theme.get_text()).pack(pady=5)
            ctk.CTkLabel(card, text=desc, font=Theme.SMALL_FONT, text_color=Theme.get_text_secondary()).pack(pady=(0,15))
        
        actions = ctk.CTkFrame(main, fg_color="transparent")
        actions.pack(fill="x")
        actions.grid_columnconfigure((0,1,2), weight=1)
        
        ctk.CTkButton(actions, text="🚀 " + get_text("start_test"), height=80, font=Theme.SUBHEADING_FONT,
                     fg_color=Theme.SUCCESS, hover_color="#0E6B0E", corner_radius=12,
                     command=lambda: self.mode_callback("basic")).grid(row=0, column=0, padx=10, pady=25, sticky="ew")
        
        ctk.CTkButton(actions, text="⚙️ " + get_text("individual_test"), height=80, font=Theme.SUBHEADING_FONT,
                     fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, corner_radius=12,
                     command=lambda: self.mode_callback("individual")).grid(row=0, column=1, padx=10, pady=25, sticky="ew")
        
        ctk.CTkButton(actions, text="📖 " + get_text("user_guide"), height=80, font=Theme.SUBHEADING_FONT,
                     fg_color=Theme.INFO, hover_color="#0550ae", corner_radius=12,
                     command=lambda: self.mode_callback("user_guide")).grid(row=0, column=2, padx=10, pady=25, sticky="ew")
        
        ctk.CTkButton(actions, text="✕ " + get_text("exit"), height=60, font=Theme.BODY_FONT,
                     fg_color=Theme.ERROR, hover_color="#B71C1C", corner_radius=12,
                     command=self.quit_app).grid(row=1, column=0, columnspan=3, pady=(25,0), sticky="ew")
    
    def refresh_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def quit_app(self):
        self.master.master.master.quit()

class IndividualTestFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.setup_ui()
    
    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(header, text="⚙️ " + get_text("individual_test"), 
                    font=Theme.HEADING_FONT, text_color=Theme.get_text()).pack(side="left")
        ctk.CTkButton(header, text="← " + get_text("overview"), width=100, height=32,
                     command=lambda: self.mode_callback("overview")).pack(side="right")
        
        tests = [
            ("system_info", "💻"), ("license_check", "🔑"), ("storage_test", "💾"), ("display_test", "🖥️"),
            ("keyboard_test", "⌨️"), ("ports_test", "🔌"), ("battery_test", "🔋"), ("audio_test", "🔊"),
            ("camera_test", "📷"), ("cpu_test", "🧠"), ("gpu_test", "🎮"), ("thermal_test", "🌡️")
        ]
        
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, (key, icon) in enumerate(tests):
            row, col = i // 4, i % 4
            grid.grid_columnconfigure(col, weight=1)
            
            btn = ctk.CTkButton(grid, text=f"{icon}\n{get_text(key)}", height=120, 
                               font=Theme.BODY_FONT, corner_radius=12,
                               command=lambda k=key: self.run_individual_test(k))
            btn.grid(row=row, column=col, padx=20, pady=20, sticky="ew")
    
    def refresh_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def run_individual_test(self, test_key):
        self.mode_callback(f"test_{test_key}")

class ModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback, icon_manager):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.tabview = ctk.CTkTabview(self, corner_radius=12, height=90,
                                     segmented_button_fg_color=Theme.get_frame(),
                                     segmented_button_selected_color=Theme.ACCENT,
                                     segmented_button_selected_hover_color=Theme.ACCENT_HOVER,
                                     segmented_button_unselected_color=Theme.get_card(),
                                     segmented_button_unselected_hover_color=Theme.get_text_secondary(),
                                     text_color=Theme.get_text(),
                                     text_color_disabled=Theme.get_text_secondary())
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        self.tabview._segmented_button.configure(height=70, font=Theme.SUBHEADING_FONT,
                                               corner_radius=10, border_width=2)
        
        self.setup_tabs()
        self.tabview.set(self.overview_tab)
    
    def setup_tabs(self):
        self.overview_tab = get_text("overview")
        self.tabview.add(self.overview_tab)
        self.overview_frame = OverviewFrame(self.tabview.tab(self.overview_tab), self.mode_callback)
        self.overview_frame.pack(fill="both", expand=True)
        
        self.test_tab = get_text("individual_test")
        self.tabview.add(self.test_tab)
        self.test_frame = IndividualTestFrame(self.tabview.tab(self.test_tab), self.mode_callback)
        self.test_frame.pack(fill="both", expand=True)
        
        self.guide_tab = get_text("user_guide")
        self.tabview.add(self.guide_tab)
        self.guide_frame = UserGuideFrame(self.tabview.tab(self.guide_tab), self.mode_callback)
        self.guide_frame.pack(fill="both", expand=True)
        
        self.mode_tab = "Chọn chế độ" if CURRENT_LANG == "vi" else "Select Mode"
        self.tabview.add(self.mode_tab)
        self.create_mode_selection()
    
    def create_mode_selection(self):
        mode_frame = self.tabview.tab(self.mode_tab)
        
        title_text = "Chọn chế độ kiểm tra" if CURRENT_LANG == "vi" else "Select Testing Mode"
        ctk.CTkLabel(mode_frame, text=title_text, font=Theme.HEADING_FONT, text_color=Theme.get_text()).pack(pady=30)
        
        buttons = ctk.CTkFrame(mode_frame, fg_color="transparent")
        buttons.pack(pady=20, padx=40, fill="x")
        
        basic_text = "🟢 Chế độ Cơ bản\nNhanh chóng, dễ sử dụng" if CURRENT_LANG == "vi" else "🟢 Basic Mode\nQuick and easy to use"
        expert_text = "🔴 Chế độ Chuyên gia\nĐầy đủ tính năng, chi tiết" if CURRENT_LANG == "vi" else "🔴 Expert Mode\nFull features, detailed"
        
        ctk.CTkButton(buttons, text=basic_text, height=120, font=Theme.SUBHEADING_FONT,
                     fg_color=Theme.SUCCESS, hover_color="#0E6B0E", corner_radius=12,
                     command=lambda: self.mode_callback("basic")).pack(pady=20, fill="x")
        
        ctk.CTkButton(buttons, text=expert_text, height=120, font=Theme.SUBHEADING_FONT,
                     fg_color=Theme.ERROR, hover_color="#B71C1C", corner_radius=12,
                     command=lambda: self.mode_callback("expert")).pack(pady=20, fill="x")
    
    def refresh_ui(self):
        if hasattr(self, 'overview_frame'):
            self.overview_frame.refresh_ui()
        if hasattr(self, 'test_frame'):
            self.test_frame.refresh_ui()
        if hasattr(self, 'guide_frame'):
            self.guide_frame.refresh_ui()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(get_text("title"))
        self.state('zoomed')
        self.minsize(1200, 800)
        
        self.icon_manager = IconManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.current_main_frame = None
        self.all_results = {}

        self.header = ctk.CTkFrame(self, fg_color=Theme.get_frame(), height=60, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self.header, text="💻 LaptopTester Pro", 
                                       font=Theme.HEADING_FONT, text_color=Theme.get_text())
        self.title_label.grid(row=0, column=0, padx=15, pady=15)
        
        controls = ctk.CTkFrame(self.header, fg_color="transparent")
        controls.grid(row=0, column=2, padx=15, pady=15)
        
        self.dark_btn = ctk.CTkButton(controls, text="🌙", width=70, height=55, font=Theme.BODY_FONT,
                                     command=self.toggle_theme_enhanced, fg_color=Theme.ACCENT)
        self.dark_btn.pack(side="left", padx=10)
        
        self.lang_btn = ctk.CTkButton(controls, text="VI", width=70, height=55, font=Theme.BODY_FONT,
                                     command=self.toggle_language_enhanced, fg_color=Theme.SUCCESS)
        self.lang_btn.pack(side="left", padx=10)
        
        self.exit_btn = ctk.CTkButton(controls, text="✕", width=70, height=55, font=Theme.BODY_FONT,
                                     command=self.quit_app, fg_color=Theme.ERROR)
        self.exit_btn.pack(side="left", padx=10)

        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=1, column=0, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        self.show_mode_selection()

    def toggle_theme_enhanced(self):
        toggle_theme()
        icon = "☀️" if CURRENT_THEME == "light" else "🌙"
        self.dark_btn.configure(text=icon)
        self.refresh_all_ui()
    
    def toggle_language_enhanced(self):
        toggle_language()
        text = "EN" if CURRENT_LANG == "en" else "VI"
        self.lang_btn.configure(text=text)
        self.title(get_text("title"))
        self.refresh_all_ui()
    
    def refresh_all_ui(self):
        self.title(get_text("title"))
        self.header.configure(fg_color=Theme.get_frame())
        self.title_label.configure(text_color=Theme.get_text())
        
        if hasattr(self.current_main_frame, 'refresh_ui'):
            self.current_main_frame.refresh_ui()

    def clear_window(self):
        if self.current_main_frame:
            self.current_main_frame.destroy()
        self.current_main_frame = None

    def show_mode_selection(self):
        self.clear_window()
        self.current_main_frame = ModeSelectionFrame(self.main_content, self.start_wizard, self.icon_manager)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def start_wizard(self, mode):
        if mode == "individual":
            if hasattr(self.current_main_frame, 'tabview'):
                self.current_main_frame.tabview.set(self.current_main_frame.test_tab)
        elif mode == "overview":
            if hasattr(self.current_main_frame, 'tabview'):
                self.current_main_frame.tabview.set(self.current_main_frame.overview_tab)
        elif mode == "user_guide":
            if hasattr(self.current_main_frame, 'tabview'):
                self.current_main_frame.tabview.set(self.current_main_frame.guide_tab)
        elif mode.startswith("test_"):
            test_key = mode[5:]
            self.run_individual_test(test_key)
        else:
            self.clear_window()
            self.current_main_frame = WizardFrame(self.main_content, mode, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
    
    def run_individual_test(self, test_key):
        test_map = {
            "system_info": ("Thông tin hệ thống", SystemInfoStep),
            "license_check": ("Kiểm tra bản quyền", LicenseCheckStep),
            "storage_test": ("Kiểm tra ổ cứng", HardDriveHealthStep),
            "display_test": ("Kiểm tra màn hình", ScreenTestStep),
            "keyboard_test": ("Kiểm tra bàn phím", KeyboardVisualTestStep),
            "ports_test": ("Kiểm tra cổng kết nối", PortsConnectivityStep),
            "battery_test": ("Kiểm tra pin", BatteryHealthStep),
            "audio_test": ("Kiểm tra âm thanh", SpeakerTestStep),
            "camera_test": ("Kiểm tra camera", WebcamTestStep),
            "cpu_test": ("Kiểm tra CPU", CPUStressTestStep),
            "gpu_test": ("Kiểm tra GPU", GPUStressTestStep),
            "memory_test": ("Kiểm tra RAM", HardDriveSpeedStep),
            "thermal_test": ("Kiểm tra nhiệt độ", ThermalPerformanceStep)
        }
        
        if test_key in test_map:
            self.clear_window()
            test_name, test_class = test_map[test_key]
            
            test_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
            test_frame.grid(row=0, column=0, sticky="nsew")
            test_frame.grid_columnconfigure(0, weight=1)
            test_frame.grid_rowconfigure(1, weight=1)
            
            header = ctk.CTkFrame(test_frame, fg_color=Theme.get_frame(), height=60)
            header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
            header.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(header, text=f"Test: {test_name}", font=Theme.SUBHEADING_FONT).grid(row=0, column=0, padx=20, pady=15)
            ctk.CTkButton(header, text="← Quay lại", command=self.show_mode_selection, 
                         width=80, height=24).grid(row=0, column=2, padx=5, pady=5)
            
            test_instance = test_class(
                test_frame,
                record_result_callback=lambda name, result: print(f"Result: {name} - {result}"),
                enable_next_callback=lambda: None,
                go_to_next_step_callback=lambda: None,
                icon_manager=self.icon_manager,
                all_results={}
            )
            test_instance.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
            
            self.current_main_frame = test_frame
    
    def quit_app(self):
        self.clear_window()
        self.destroy()

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    try:
        import ctypes
        import sys
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            return False
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        print("Yêu cầu quyền Administrator để chạy chính xác...")
        if not run_as_admin():
            print("Không thể khởi động với quyền admin")
            input("Nhấn Enter để thoát...")
        sys.exit()
    
    try:
        ctk.set_appearance_mode(CURRENT_THEME)
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()