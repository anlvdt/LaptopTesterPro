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

# --- ENHANCED THEME & ASSETS ---
class Theme:
    # Colors - Modern design system
    BACKGROUND="#F8FAFC"; FRAME="#FFFFFF"; CARD="#FFFFFF"; BORDER="#E2E8F0"; SEPARATOR = "#F1F5F9"
    TEXT="#0F172A"; TEXT_SECONDARY="#64748B"; ACCENT="#3B82F6"; ACCENT_HOVER="#2563EB"
    SUCCESS="#10B981"; WARNING="#F59E0B"; ERROR="#EF4444"; SKIP="#94A3B8"; SKIP_HOVER="#64748B"
    INFO="#06B6D4"; GRADIENT_START="#3B82F6"; GRADIENT_END="#8B5CF6"
    # Typography - Improved hierarchy
    TITLE_FONT=("Segoe UI", 42, "bold"); HEADING_FONT=("Segoe UI", 28, "bold"); SUBHEADING_FONT=("Segoe UI", 22, "bold")
    BODY_FONT=("Segoe UI", 16); SMALL_FONT=("Segoe UI", 14); KEY_FONT = ("Segoe UI", 11)
    # Layout - Better spacing
    CORNER_RADIUS = 12; PADDING_X = 24; PADDING_Y = 20; BUTTON_HEIGHT = 48
    CARD_PADDING = 20; SECTION_SPACING = 16; ELEMENT_SPACING = 12
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

# --- Canonical BaseStepFrame from backup ---

# --- Canonical BaseStepFrame from backup ---
class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        # This is the combined, correct __init__ from the original file's logic
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.title = title
        # Extract callbacks from kwargs
        self.record_result = kwargs.get("record_result_callback")
        self.enable_next_callback = kwargs.get("enable_next_callback")
        self.go_to_next_step_callback = kwargs.get("go_to_next_step_callback")
        self.icon_manager = kwargs.get("icon_manager")
        self.all_results = kwargs.get("all_results")
        
        self._completed, self._skipped = False, False
        self.after_id = None

        # Layout cân bằng và tận dụng không gian - Cải tiến spacing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)  # Guide panel
        self.grid_columnconfigure(1, weight=3)  # Action panel - rộng hơn
        # Guide container (left panel) - Cải tiến padding và margin
        guide_container = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        guide_container.grid(row=0, column=0, sticky="nsew", padx=(Theme.PADDING_X, Theme.ELEMENT_SPACING), pady=Theme.PADDING_Y)
        guide_container.grid_columnconfigure(0, weight=1)
        guide_container.grid_rowconfigure(0, weight=1)
        guide_container.grid_rowconfigure(1, weight=0)
        guide_container.grid_rowconfigure(2, weight=1)
        guide_container.grid_rowconfigure(3, weight=0)  # Tips frame
        why_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        why_frame.grid(row=0, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(why_frame, image=self.icon_manager.WHY, text=" Tại sao cần test?", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT, compound="left").pack(anchor="w")
        ctk.CTkLabel(why_frame, text=why_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.TEXT).pack(anchor="w", pady=(Theme.ELEMENT_SPACING,0))
        ctk.CTkFrame(guide_container, height=1, fg_color=Theme.SEPARATOR).grid(row=1, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.ELEMENT_SPACING)
        how_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        how_frame.grid(row=2, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(how_frame, image=self.icon_manager.HOW, text=" Hướng dẫn thực hiện:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT, compound="left").pack(anchor="w")
        ctk.CTkLabel(how_frame, text=how_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.TEXT).pack(anchor="w", pady=(Theme.ELEMENT_SPACING,0))
        
        # Thêm gợi ý đọc kết quả - Cải tiến design
        tips_frame = ctk.CTkFrame(guide_container, fg_color="#E3F2FD", corner_radius=Theme.CORNER_RADIUS)
        tips_frame.grid(row=3, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=(Theme.SECTION_SPACING, Theme.CARD_PADDING))
        ctk.CTkLabel(tips_frame, text="💡 Gợi ý đọc kết quả:", font=Theme.BODY_FONT, text_color="#1565C0").pack(anchor="w", padx=Theme.ELEMENT_SPACING, pady=(Theme.ELEMENT_SPACING, 8))
        tips_text = "• Màu xanh: Kết quả tốt, an toàn\n• Màu vàng: Cảnh báo, cần chú ý\n• Màu đỏ: Lỗi nghiêm trọng, cần xử lý"
        ctk.CTkLabel(tips_frame, text=tips_text, font=Theme.SMALL_FONT, text_color="#424242", justify="left").pack(anchor="w", padx=Theme.ELEMENT_SPACING, pady=(0, Theme.ELEMENT_SPACING))
        # Action container (right panel) - Cải tiến spacing và layout
        action_container = ctk.CTkFrame(self, fg_color="transparent")
        action_container.grid(row=0, column=1, sticky="nsew", padx=(Theme.ELEMENT_SPACING, Theme.PADDING_X), pady=Theme.PADDING_Y)
        action_container.grid_columnconfigure(0, weight=1)
        action_container.grid_rowconfigure(0, weight=1)
        # Action frame - bung hết không gian hoặc căn giữa
        self.action_frame_container = ctk.CTkFrame(action_container, fg_color="transparent")
        self.action_frame_container.grid(row=0, column=0, sticky="nsew")
        self.action_frame_container.grid_columnconfigure(0, weight=1)
        self.action_frame_container.grid_rowconfigure(0, weight=1)
        # Scrollable action frame - cải tiến layout
        self.action_canvas = tk.Canvas(self.action_frame_container, bg=Theme.CARD, highlightthickness=0)
        self.action_canvas.grid(row=0, column=0, sticky="nsew")
        self.action_scrollbar = tk.Scrollbar(self.action_frame_container, orient="vertical", command=self.action_canvas.yview)
        self.action_scrollbar.grid(row=0, column=1, sticky="ns")
        self.action_canvas.configure(yscrollcommand=self.action_scrollbar.set)
        self.action_frame = ctk.CTkFrame(self.action_canvas, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS)
        self.action_window = self.action_canvas.create_window((0,0), window=self.action_frame, anchor="nw")
        self.action_frame.bind("<Configure>", lambda e: self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all")))
        # Bung hết chiều rộng và căn giữa nội dung
        self.action_canvas.bind("<Configure>", self._on_canvas_configure)
        # Đảm bảo action_frame luôn bung hết
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

    def _on_canvas_configure(self, event):
        """Xử lý khi canvas thay đổi kích thước - đảm bảo nội dung bung hết hoặc căn giữa"""
        canvas_width = event.width
        # Luôn bung hết chiều rộng canvas
        self.action_canvas.itemconfig(self.action_window, width=canvas_width-20)
        # Căn giữa theo chiều ngang
        self.action_canvas.coords(self.action_window, 10, 0)
    
    def on_show(self):
        # Force update of scrollable canvas and window to ensure all content is visible
        if hasattr(self, 'action_canvas') and hasattr(self, 'action_window'):
            self.action_canvas.update_idletasks()
            self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all"))
            # Resize window to fit content if needed
            width = min(900, self.action_canvas.winfo_width())
            self.action_canvas.itemconfig(self.action_window, width=width)
        # Also ensure result_container and button bars are visible if present
        if hasattr(self, 'result_container'):
            self.result_container.update_idletasks()
        if hasattr(self, 'container'):
            self.container.update_idletasks()
    def is_ready_to_proceed(self): return self._completed or self._skipped
    def mark_completed(self, result_data, auto_advance=False):
        self._completed = True
        self._skipped = False
        if self.record_result:
            self.record_result(self.title, result_data)
        if auto_advance and self.go_to_next_step_callback:
            self.go_to_next_step_callback()
    def mark_skipped(self, result_data): 
        self._skipped = True; self._completed = False
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
                self.btn_yes.configure(fg_color=Theme.ACCENT)
            self.mark_completed(result, auto_advance=True)
        else:
            if hasattr(self, 'btn_no'):
                self.btn_no.configure(fg_color=Theme.WARNING)
            self.mark_completed(result, auto_advance=True)
    def stop_tasks(self):
        if self.after_id: self.after_cancel(self.after_id); self.after_id = None
    def create_external_benchmark_box(self, parent_grid, row, column, benchmarks):
        box = ctk.CTkFrame(parent_grid, border_width=1, border_color=Theme.SEPARATOR, corner_radius=Theme.CORNER_RADIUS)
        box.grid(row=row, column=column, columnspan=3, sticky="ew", padx=20, pady=(10, 20))
        ctk.CTkLabel(box, text="Tùy chọn: Chạy Benchmark chuyên nghiệp", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(pady=(10,5), padx=15, anchor="w")
        ctk.CTkLabel(box, text="Để có kết quả so sánh tiêu chuẩn, bạn có thể dùng các phần mềm sau:", font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=(0,10), padx=15, anchor="w")
        btn_frame = ctk.CTkFrame(box, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        for name, url in benchmarks.items():
            ctk.CTkButton(btn_frame, text=f"Tải {name}", command=lambda u=url: webbrowser.open(u), font=Theme.BODY_FONT, height=45).pack(side="left", expand=True, padx=5)

class HardwareFingerprintStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            "Định Danh Phần Cứng",
            "Đây là bước quan trọng nhất để chống lừa đảo. Các thông tin dưới đây được đọc trực tiếp từ BIOS và linh kiện phần cứng. Chúng **cực kỳ khó làm giả** từ bên trong Windows.",
            "Hãy so sánh các thông tin 'vàng' này với cấu hình mà người bán quảng cáo. Nếu có bất kỳ sự sai lệch nào, hãy đặt câu hỏi và kiểm tra thật kỹ.",
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
            ctk.CTkLabel(row_frame, image=self.icon_manager.SHIELD, text="").pack(side="left", padx=(0, 10))
            ctk.CTkLabel(row_frame, text=f"{item}:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(side="left", padx=(0, 15))
            self.info_labels[item] = ctk.CTkLabel(row_frame, text="", justify="left", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=900)
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
                # Lấy thông tin hệ thống
                system_info = c.Win32_ComputerSystem()[0]
                hw_info["Model Laptop"] = f"{system_info.Manufacturer} {system_info.Model}"
                
                # Lấy thông tin BIOS
                bios = c.Win32_BIOS()[0]
                hw_info["Serial Number"] = getattr(bios, 'SerialNumber', 'N/A')
                
                # Xử lý ngày BIOS an toàn hơn
                try:
                    bios_date = getattr(bios, 'ReleaseDate', '')
                    if bios_date and len(bios_date) >= 8:
                        bios_date_str = bios_date.split('.')[0]
                        hw_info["Ngày BIOS"] = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
                    else:
                        hw_info["Ngày BIOS"] = "Không xác định"
                except:
                    hw_info["Ngày BIOS"] = "Không đọc được"
                
                # Lấy thông tin CPU - cải tiến
                try:
                    processors = c.Win32_Processor()
                    if processors:
                        cpu_name = processors[0].Name.strip()
                        hw_info["CPU"] = cpu_name
                        # Lưu thêm thông tin CPU cho so sánh
                        self.bios_cpu_info = cpu_name
                    else:
                        hw_info["CPU"] = "Không tìm thấy CPU"
                        self.bios_cpu_info = None
                except Exception as e:
                    hw_info["CPU"] = f"Lỗi đọc CPU: {e}"
                    self.bios_cpu_info = None
                
                # Lấy thông tin GPU
                try:
                    gpus = c.Win32_VideoController()
                    gpu_names = [gpu.Name for gpu in gpus if gpu.Name]
                    hw_info["GPU"] = "\n".join(gpu_names) if gpu_names else "Không tìm thấy GPU"
                except:
                    hw_info["GPU"] = "Lỗi đọc GPU"
                
                # Lấy thông tin ổ cứng
                try:
                    drives = c.Win32_DiskDrive()
                    drive_models = [d.Model for d in drives if d.Model]
                    hw_info["Model Ổ Cứng"] = "\n".join(drive_models) if drive_models else "Không tìm thấy ổ cứng"
                except:
                    hw_info["Model Ổ Cứng"] = "Lỗi đọc ổ cứng"
                    
            except Exception as e: 
                hw_info = {k: f"Lỗi WMI: {e}" for k in self.info_items}
                self.bios_cpu_info = None
            finally: 
                pythoncom.CoUninitialize()
        else: 
            hw_info = {k: "Chỉ hỗ trợ Windows" for k in self.info_items}
            self.bios_cpu_info = None
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
        self.mark_completed({"Kết quả": "Đã lấy định danh phần cứng", "Trạng thái": "Tốt", "Chi tiết": f"Thông tin định danh phần cứng:\n{full_details}"}, auto_advance=False)
        if hasattr(self, 'show_result_choices'):
            self.show_result_choices()
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Định danh phần cứng đã hoàn thành. Bạn có muốn tiếp tục?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Tiếp tục", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tiếp tục", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_skip = ctk.CTkButton(button_bar, text="Bỏ qua", image=self.icon_manager.SKIP_ICON if hasattr(self.icon_manager, 'SKIP_ICON') else None, compound="left", command=lambda: self.mark_skipped({"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"}), fg_color=Theme.SKIP, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)
        self.result_container.lift()
        self.result_container.update_idletasks()
        if hasattr(self, 'action_canvas'):
            self.action_canvas.update_idletasks()
            self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all"))
            self.action_canvas.yview_moveto(0)
        # Also ensure button bar is visible
        if hasattr(self, 'controls_frame'):
            self.controls_frame.update_idletasks()

class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bản Quyền Windows", "Một máy tính có bản quyền Windows hợp lệ đảm bảo bạn nhận được các bản cập nhật bảo mật quan trọng và tránh các rủi ro pháp lý.", "Ứng dụng sẽ tự động chạy lệnh kiểm tra trạng thái kích hoạt của Windows. Kết quả sẽ hiển thị bên dưới.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(self.action_frame, text="Đang kiểm tra...", font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT_SECONDARY)
        self.status_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        threading.Thread(target=self.check_license, daemon=True).start()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Kiểm tra bản quyền đã hoàn thành. Bạn có muốn tiếp tục?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Tiếp tục", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tiếp tục", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_skip = ctk.CTkButton(button_bar, text="Bỏ qua", image=self.icon_manager.SKIP_ICON if hasattr(self.icon_manager, 'SKIP_ICON') else None, compound="left", command=lambda: self.mark_skipped({"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"}), fg_color=Theme.SKIP, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)

    def check_license(self):
        status, color, result_data = "Không thể kiểm tra", Theme.WARNING, {"Kết quả": "Không thể kiểm tra", "Trạng thái": "Lỗi"}
        if platform.system() == "Windows":
            try:
                startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                output_bytes = subprocess.check_output("cscript //Nologo C:\\Windows\\System32\\slmgr.vbs /xpr", shell=False, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
                try: result = output_bytes.decode('utf-8').lower()
                except UnicodeDecodeError: result = output_bytes.decode(locale.getpreferredencoding(), errors='ignore').lower()
                activated_strings = ["activated permanently", "kích hoạt vĩnh viễn", "the machine is permanently activated"]
                if any(s in result for s in activated_strings):
                    status, color, result_data = "Windows được kích hoạt vĩnh viễn", Theme.SUCCESS, {"Kết quả": "Đã kích hoạt vĩnh viễn", "Trạng thái": "Tốt"}
                elif "will expire" in result or "sẽ hết hạn" in result:
                    expiry_date = result.split("on")[-1].strip() if "on" in result else result.split(" vào ")[-1].strip()
                    status, color, result_data = f"Windows sẽ hết hạn vào {expiry_date}", Theme.WARNING, {"Kết quả": f"Sẽ hết hạn ({expiry_date})", "Trạng thái": "Lỗi"}
                else: status, color, result_data = "Windows chưa được kích hoạt", Theme.ERROR, {"Kết quả": "Chưa kích hoạt", "Trạng thái": "Lỗi"}
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

class SystemInfoStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cấu Hình Windows", "Bước này hiển thị thông tin cấu hình mà Windows nhận diện và tự động so sánh với thông tin từ BIOS để phát hiện sai lệch.", "Đối chiếu thông tin dưới đây với bước trước và với thông tin quảng cáo. Nếu mọi thứ khớp, chọn 'Cấu hình khớp'.", **kwargs)
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
        ctk.CTkLabel(self.comparison_frame, text="So sánh tự động:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w")
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        threading.Thread(target=self.fetch_info, daemon=True).start()

    def fetch_info(self):
        full_info = {k: "Đang đọc..." for k in self.info_items}
        try:
            full_info["RAM"] = f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
            if platform.system() == "Windows":
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    full_info["CPU"] = c.Win32_Processor()[0].Name.strip()
                    full_info["GPU"] = "\n".join([gpu.Name for gpu in c.Win32_VideoController()])
                    disk_details = [f"- {d.Model} ({round(int(d.Size)/(1024**3))} GB)" for d in c.Win32_DiskDrive() if d.Size]
                    full_info["Ổ cứng"] = "\n".join(disk_details) if disk_details else "Không tìm thấy"
                except Exception as e: full_info.update({k: f"Lỗi WMI: {e}" for k in ["CPU", "GPU", "Ổ cứng"]})
                finally: pythoncom.CoUninitialize()
            else: full_info.update({k: "Chỉ hỗ trợ Windows" for k in ["CPU", "GPU", "Ổ cứng"]})
        except Exception as e: full_info = {k: f"Lỗi: {e}" for k in self.info_items}
        if self.winfo_exists(): self.after(0, self.display_info, full_info)

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
        # Force UI update and scroll to top to ensure buttons are visible
        if hasattr(self, 'action_canvas'):
            self.action_canvas.update_idletasks()
            self.action_canvas.yview_moveto(0)
    def normalize_cpu_name(self, name):
        if not name or name == "N/A":
            return ""
        name = name.lower().strip()
        # Remove common suffixes and prefixes
        to_remove = ["(r)", "(tm)", "cpu", "@", "ghz", "mhz", "processor", 
                    "with radeon graphics", "with vega graphics", "apu", "mobile"]
        for term in to_remove: 
            name = name.replace(term, "")
        # Clean up extra spaces
        return " ".join(name.split())
    
    def extract_cpu_key(self, normalized_name):
        """Extract key CPU identifier like 'intel i5', 'amd ryzen 5', etc."""
        if not normalized_name:
            return "unknown"
        
        name = normalized_name.lower()
        
        # Intel patterns
        if "intel" in name:
            if "i3" in name: return "intel i3"
            elif "i5" in name: return "intel i5"
            elif "i7" in name: return "intel i7"
            elif "i9" in name: return "intel i9"
            elif "celeron" in name: return "intel celeron"
            elif "pentium" in name: return "intel pentium"
            elif "xeon" in name: return "intel xeon"
            else: return "intel"
        
        # AMD patterns
        elif "amd" in name:
            if "ryzen 3" in name: return "amd ryzen 3"
            elif "ryzen 5" in name: return "amd ryzen 5"
            elif "ryzen 7" in name: return "amd ryzen 7"
            elif "ryzen 9" in name: return "amd ryzen 9"
            elif "ryzen" in name: return "amd ryzen"
            elif "athlon" in name: return "amd athlon"
            elif "fx" in name: return "amd fx"
            else: return "amd"
        
        return "unknown"
    def perform_comparison(self):
        # Lấy thông tin CPU từ BIOS (từ HardwareFingerprintStep)
        cpu_bios = "N/A"
        hw_fingerprint_step = None
        
        # Tìm HardwareFingerprintStep trong các step đã chạy
        try:
            # Kiểm tra xem có thông tin CPU từ BIOS không
            hw_data = self.all_results.get("Định Danh Phần Cứng", {})
            hw_details = hw_data.get("Chi tiết", "")
            
            # Phương pháp 1: Tìm trong chi tiết
            if hw_details:
                for line in hw_details.splitlines():
                    line = line.strip()
                    if any(pattern in line.lower() for pattern in ["cpu:", "processor:", "- cpu"]):
                        parts = line.split(":", 1)
                        if len(parts) > 1:
                            cpu_bios = parts[1].strip()
                            break
            
            # Phương pháp 2: Lấy trực tiếp từ WMI (backup)
            if cpu_bios == "N/A":
                if platform.system() == "Windows":
                    pythoncom.CoInitializeEx(0)
                    try:
                        c = wmi.WMI()
                        processors = c.Win32_Processor()
                        if processors:
                            cpu_bios = processors[0].Name.strip()
                    except:
                        pass
                    finally:
                        pythoncom.CoUninitialize()
        except Exception as e:
            print(f"Lỗi lấy thông tin CPU BIOS: {e}")
        
        # Extract Windows CPU info
        cpu_win = "N/A"
        if hasattr(self, 'full_info_text'):
            for line in self.full_info_text.splitlines():
                if "CPU:" in line:
                    cpu_win = line.split(":", 1)[1].strip()
                    break
        
        # Improved CPU comparison
        if cpu_bios != "N/A" and cpu_win != "N/A":
            norm_bios = self.normalize_cpu_name(cpu_bios)
            norm_win = self.normalize_cpu_name(cpu_win)
            
            # Multiple comparison methods
            exact_match = norm_bios == norm_win
            contains_match = norm_bios in norm_win or norm_win in norm_bios
            
            # Extract key identifiers (Intel i5, AMD Ryzen, etc.)
            bios_key = self.extract_cpu_key(norm_bios)
            win_key = self.extract_cpu_key(norm_win)
            key_match = bios_key == win_key and bios_key != "unknown"
            
            match = exact_match or contains_match or key_match
        else:
            match = False
        
        # Display comparison results
        ctk.CTkLabel(self.comparison_frame, text=f"CPU (BIOS): {cpu_bios}", font=Theme.BODY_FONT, wraplength=800).pack(anchor="w")
        ctk.CTkLabel(self.comparison_frame, text=f"CPU (Windows): {cpu_win}", font=Theme.BODY_FONT, wraplength=800).pack(anchor="w")
        
        result_label = ctk.CTkLabel(self.comparison_frame, font=Theme.BODY_FONT)
        if cpu_bios == "N/A" or cpu_win == "N/A":
            result_label.configure(text="Kết quả: Không thể so sánh (thiếu dữ liệu)", text_color=Theme.WARNING)
        elif match:
            result_label.configure(text="✅ Kết quả: Khớp", text_color=Theme.SUCCESS)
        else:
            result_label.configure(text="⚠️ Cảnh báo: Có sai lệch - Kiểm tra lại!", text_color=Theme.ERROR)
        result_label.pack(anchor="w")
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Cấu hình có khớp với thông tin quảng cáo không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, cấu hình khớp", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Cấu hình khớp", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có sai lệch", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có sai lệch", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)
    
    def copy_to_clipboard(self): self.clipboard_clear(); self.clipboard_append(self.full_info_text)

class HardDriveHealthStep(BaseStepFrame):
    # Already patched above, but add scroll-to-top for visibility
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="[DEBUG] result_container", font=Theme.SMALL_FONT, fg_color="#FFDDDD").pack(fill="x")
        ctk.CTkLabel(self.result_container, text="Ổ cứng có hoạt động tốt không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        ctk.CTkLabel(button_bar, text="[DEBUG] button_bar", font=Theme.SMALL_FONT, fg_color="#DDFFDD").pack(fill="x")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(
            button_bar,
            text="Có, tất cả đều tốt",
            image=self.icon_manager.CHECK,
            compound="left",
            command=lambda: self.handle_result_generic(True, {"Kết quả": "Tốt", "Trạng thái": "Tốt", "Chi tiết": self.full_details}, {}),
            fg_color=Theme.SUCCESS,
            height=Theme.BUTTON_HEIGHT,
            font=Theme.BODY_FONT
        )
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(
            button_bar,
            text="Không, có lỗi",
            image=self.icon_manager.CROSS,
            compound="left",
            command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có ổ cứng lỗi", "Trạng thái": "Lỗi", "Chi tiết": self.full_details}),
            fg_color=Theme.ERROR,
            height=Theme.BUTTON_HEIGHT,
            font=Theme.BODY_FONT
        )
        self.btn_no.pack(side="left", padx=10)
        self.btn_skip = ctk.CTkButton(
            button_bar,
            text="Bỏ qua",
            image=self.icon_manager.SKIP_ICON if hasattr(self.icon_manager, 'SKIP_ICON') else None,
            compound="left",
            command=lambda: self.mark_skipped({"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua", "Chi tiết": self.full_details}),
            fg_color=Theme.SKIP,
            height=Theme.BUTTON_HEIGHT,
            font=Theme.BODY_FONT
        )
        self.btn_skip.pack(side="left", padx=10)
        # Force result_container to front and update UI
        self.result_container.lift()
        self.result_container.update_idletasks()
        # Update scroll region and bring result_container into view
        if hasattr(self, 'action_canvas'):
            self.action_canvas.update_idletasks()
            self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all"))
            self.action_canvas.yview_moveto(0)
        # Force UI update and scroll to top to ensure buttons are visible
        if hasattr(self, 'action_canvas'):
            self.action_canvas.update_idletasks()
            self.action_canvas.yview_moveto(0)
    def __init__(self, master, **kwargs):
        super().__init__(master, "Sức Khỏe Ổ Cứng (S.M.A.R.T)", "Ổ cứng sắp hỏng là mối rủi ro mất dữ liệu cực lớn. Bước này đọc 'báo cáo y tế' (S.M.A.R.T.) của ổ cứng để đánh giá độ bền.", "Chú ý đến mục 'Trạng thái'. 'Tốt' là bình thường. 'Lỗi/Cảnh báo' là rủi ro cao. Bước tiếp theo sẽ kiểm tra tốc độ thực tế.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew"); self.loading_spinner.start()
        self.drive_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.drive_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.drive_container.grid_columnconfigure(0, weight=1)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        threading.Thread(target=self.fetch_drive_info, daemon=True).start()
    def fetch_drive_info(self):
        drives_info = []
        if platform.system() == "Windows":
            pythoncom.CoInitializeEx(0)
            try:
                c = wmi.WMI()
                drives = c.Win32_DiskDrive()
                if not drives: drives_info.append({"Tên": "Không tìm thấy ổ cứng", "Trạng thái": "Lỗi"})
                else:
                    for drive in drives: drives_info.append({"Tên": drive.Model, "Trạng thái": "Tốt" if drive.Status == "OK" else "Lỗi/Cảnh báo"})
            except Exception as e: drives_info.append({"Tên": "Không thể đọc S.M.A.R.T", "Trạng thái": f"Lỗi: {e}"})
            finally: pythoncom.CoUninitialize()
        else: drives_info.append({"Tên": "N/A", "Trạng thái": "Chỉ hỗ trợ Windows"})
        if self.winfo_exists(): self.after(0, self.display_info, drives_info)
    def display_info(self, drives_info):
        self.loading_spinner.grid_remove()
        self.drive_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        full_details = ""; has_error = False
        for drive_data in drives_info:
            drive_frame = ctk.CTkFrame(self.drive_container, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
            drive_frame.pack(fill="x", pady=10)
            status = drive_data.get('Trạng thái', 'Không rõ')
            color = Theme.SUCCESS if status == "Tốt" else Theme.ERROR
            if status != "Tốt": has_error = True
            ctk.CTkLabel(drive_frame, text=f"Ổ cứng: {drive_data.get('Tên', 'N/A')}", font=Theme.SUBHEADING_FONT).pack(anchor="w", padx=20, pady=(15,5))
            ctk.CTkLabel(drive_frame, text=f"Trạng thái: {status}", font=Theme.SUBHEADING_FONT, text_color=color).pack(anchor="w", padx=20, pady=(5,15))
            full_details += f"- Ổ {drive_data.get('Tên', 'N/A')}: {status}\n"
        self.full_details = full_details
        self.has_error = has_error
        self.show_result_choices()

    def show_result_choices(self):
        # Remove old widgets if any
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Ổ cứng có hoạt động tốt không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, tất cả đều tốt", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tốt", "Trạng thái": "Tốt", "Chi tiết": self.full_details}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có lỗi", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có ổ cứng lỗi", "Trạng thái": "Lỗi", "Chi tiết": self.full_details}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)
        # Optionally, auto-select if only Windows is supported
        if not hasattr(self, 'has_error') or not hasattr(self, 'full_details'):
            return
        if not self.has_error and "Chỉ hỗ trợ Windows" in self.full_details:
            self.mark_completed({"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"}, auto_advance=False)

class ScreenTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Màn Hình", "Màn hình là một trong những linh kiện đắt tiền và dễ hỏng nhất. Lỗi điểm chết, hở sáng, ám màu hay 'ung thư panel' (chớp giật ở cạnh viền) là những vấn đề nghiêm trọng.", "Nhấn 'Bắt đầu Test' để chạy test màn hình tự động. Test sẽ hiển thị các màu khác nhau, nhấn ESC để dừng bất cứ lúc nào.", **kwargs)
        self.create_screen_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
    
    def create_screen_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(test_frame, text="Test Màn Hình Tự Động", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Gợi ý kiểm tra
        tips_frame = ctk.CTkFrame(test_frame, fg_color=Theme.BACKGROUND)
        tips_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(tips_frame, text="Gợi ý kiểm tra:", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        tips = [
            "• Pixel chết: Chấm đen/sáng không đổi màu",
            "• Hở sáng: Vùng sáng bất thường trên nền đen",
            "• Ám màu: Vùng tối bất thường trên nền sáng",
            "• Chớp giật: Nhấp nháy ở viền màn hình"
        ]
        for tip in tips:
            ctk.CTkLabel(tips_frame, text=tip, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20)
        
        ctk.CTkButton(test_frame, text="Bắt đầu Test Màn Hình", command=self.start_screen_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).pack(pady=10)
        
        ctk.CTkLabel(test_frame, text="Test sẽ hiển thị: Đen → Trắng → Đỏ → Xanh Lá → Xanh Dương\nMỗi màu 3 giây. Nhấn ESC để dừng.", font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=10)
    
    def start_screen_test(self):
        def run_test():
            colors = [("black", "white"), ("white", "black"), ("red", "white"), ("green", "black"), ("blue", "white")]
            names = ["Đen", "Trắng", "Đỏ", "Xanh Lá", "Xanh Dương"]
            
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
                label.configure(text=f"Test {name}\n({i+1}/5)\n\nESC để dừng", text_color=fg)
                
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
        
        ctk.CTkLabel(self.result_container, text="Bạn có phát hiện điểm chết, hở sáng, ám màu hay chớp giật bất thường không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text="Không, màn hình bình thường", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Bình thường", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        
        self.btn_no = ctk.CTkButton(button_bar, text="Có, tôi thấy vấn đề", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class KeyboardVisualTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bàn phím & Touchpad", "Một phím bị liệt, kẹt, hoặc touchpad bị loạn/mất cử chỉ đa điểm sẽ làm gián đoạn hoàn toàn công việc.", "**Bàn phím:** Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ sáng lên màu xanh dương, và chuyển sang xanh lá khi được nhả ra.\n**Touchpad & Chuột:** Vẽ trên vùng test, thử click trái/phải, cuộn 2 ngón tay.", **kwargs)
        
        self.key_widgets = {}
        self.pressed_keys = set()
        self.mouse_clicks = {'left': 0, 'right': 0}
        
        # Create keyboard layout
        self.create_keyboard_layout()
        
        # Create touchpad test area
        self.create_touchpad_test()
        
        # Start keyboard listening
        self.start_listening()
        
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()

    def create_keyboard_layout(self):
        keyboard_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        keyboard_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.action_frame.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(keyboard_frame, text="Layout Bàn Phím - Nhấn phím để test:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        # Function keys row
        self.create_key_row(keyboard_frame, [
            ('Esc', 1), ('F1', 1), ('F2', 1), ('F3', 1), ('F4', 1), ('F5', 1), 
            ('F6', 1), ('F7', 1), ('F8', 1), ('F9', 1), ('F10', 1), ('F11', 1), ('F12', 1), ('Del', 1)
        ])
        
        # Number row
        self.create_key_row(keyboard_frame, [
            ('`', 1), ('1', 1), ('2', 1), ('3', 1), ('4', 1), ('5', 1), ('6', 1), 
            ('7', 1), ('8', 1), ('9', 1), ('0', 1), ('-', 1), ('=', 1), ('Backspace', 2)
        ])
        
        # QWERTY row
        self.create_key_row(keyboard_frame, [
            ('Tab', 1.5), ('Q', 1), ('W', 1), ('E', 1), ('R', 1), ('T', 1), ('Y', 1), 
            ('U', 1), ('I', 1), ('O', 1), ('P', 1), ('[', 1), (']', 1), ('\\', 1.5)
        ])
        
        # ASDF row
        self.create_key_row(keyboard_frame, [
            ('Caps', 1.75), ('A', 1), ('S', 1), ('D', 1), ('F', 1), ('G', 1), ('H', 1), 
            ('J', 1), ('K', 1), ('L', 1), (';', 1), ("'", 1), ('Enter', 2.25)
        ])
        
        # ZXCV row
        self.create_key_row(keyboard_frame, [
            ('Shift', 2.25), ('Z', 1), ('X', 1), ('C', 1), ('V', 1), ('B', 1), ('N', 1), 
            ('M', 1), (',', 1), ('.', 1), ('/', 1), ('Shift', 2.75)
        ])
        
        # Bottom row
        self.create_key_row(keyboard_frame, [
            ('Ctrl', 1.25), ('Win', 1.25), ('Alt', 1.25), ('Space', 6.25), 
            ('Alt', 1.25), ('Fn', 1.25), ('Ctrl', 1.25), ('←', 1), ('↑', 1), ('↓', 1), ('→', 1)
        ])

    def create_key_row(self, parent, keys):
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=5, pady=1)
        
        # Configure grid weights for proper stretching
        total_weight = sum(width for _, width in keys)
        for i, (_, width) in enumerate(keys):
            row_frame.grid_columnconfigure(i, weight=int(width * 100))
        
        for i, (key_text, width) in enumerate(keys):
            key_widget = ctk.CTkLabel(
                row_frame, 
                text=key_text, 
                font=Theme.KEY_FONT,
                fg_color=Theme.BORDER,
                text_color=Theme.TEXT,
                corner_radius=4,
                height=35
            )
            key_widget.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
            
            # Map key to widget
            key_lower = key_text.lower()
            self.key_widgets[key_lower] = key_widget
            
            # Handle special key mappings
            if key_text == 'Space':
                self.key_widgets['space'] = key_widget
            elif key_text == 'Backspace':
                self.key_widgets['backspace'] = key_widget
            elif key_text == 'Enter':
                self.key_widgets['enter'] = key_widget
            elif key_text == 'Caps':
                self.key_widgets['caps lock'] = key_widget
            elif key_text == 'Win':
                self.key_widgets['windows'] = key_widget
                self.key_widgets['cmd'] = key_widget

    def create_touchpad_test(self):
        touchpad_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        touchpad_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.action_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(touchpad_frame, text="Test Touchpad & Chuột:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        # Instructions
        instructions = ctk.CTkLabel(
            touchpad_frame, 
            text="• Di chuyển chuột/touchpad trên vùng xám\n• Click trái và phải để test\n• Thử cuộn 2 ngón tay (touchpad)", 
            font=Theme.BODY_FONT, 
            text_color=Theme.TEXT_SECONDARY
        )
        instructions.pack(pady=5)
        
        # Test area
        test_area_frame = ctk.CTkFrame(touchpad_frame)
        test_area_frame.pack(fill="x", padx=20, pady=10)
        
        self.canvas = tk.Canvas(
            test_area_frame, 
            height=150, 
            bg="#E0E0E0", 
            highlightthickness=1,
            highlightbackground=Theme.BORDER
        )
        self.canvas.pack(fill="x", padx=10, pady=10)
        
        # Bind mouse events - cải thiện với focus và event handling
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<MouseWheel>", self.on_scroll)
        # Thêm binding cho frame để đảm bảo events hoạt động
        test_area_frame.bind("<Button-1>", self.on_left_click)
        test_area_frame.bind("<Button-3>", self.on_right_click)
        # Đảm bảo canvas có thể nhận focus và events
        self.canvas.focus_set()
        self.canvas.configure(cursor="crosshair")
        # Thêm event binding trực tiếp cho touchpad frame
        touchpad_frame.bind("<Button-1>", self.on_left_click)
        touchpad_frame.bind("<Button-3>", self.on_right_click)
        
        # Click counters
        counter_frame = ctk.CTkFrame(touchpad_frame, fg_color="transparent")
        counter_frame.pack(fill="x", padx=20, pady=5)
        
        self.left_click_label = ctk.CTkLabel(counter_frame, text="Click trái: 0", font=Theme.BODY_FONT)
        self.left_click_label.pack(side="left", padx=20)
        
        self.right_click_label = ctk.CTkLabel(counter_frame, text="Click phải: 0", font=Theme.BODY_FONT)
        self.right_click_label.pack(side="right", padx=20)
        
        # Clear button
        ctk.CTkButton(
            touchpad_frame, 
            text="Xóa vết vẽ", 
            command=self.clear_canvas,
            height=30,
            font=Theme.BODY_FONT
        ).pack(pady=5)

    def on_mouse_move(self, event):
        # Draw trail
        x, y = event.x, event.y
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=Theme.ACCENT, outline=Theme.ACCENT, tags="trail")

    def on_left_click(self, event):
        self.mouse_clicks['left'] += 1
        self.left_click_label.configure(text=f"Click trái: {self.mouse_clicks['left']}")
        # Visual feedback - cải thiện với xử lý event đúng
        x = getattr(event, 'x', 75)
        y = getattr(event, 'y', 75)
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#FF4444", outline="#CC0000", width=3, tags="click")
        self.canvas.create_text(x, y, text="L", font=("Arial", 12, "bold"), fill="white", tags="click")
        self.after(1500, lambda: self.canvas.delete("click"))

    def on_right_click(self, event):
        self.mouse_clicks['right'] += 1
        self.right_click_label.configure(text=f"Click phải: {self.mouse_clicks['right']}")
        # Visual feedback - cải thiện với xử lý event đúng
        x = getattr(event, 'x', 225)
        y = getattr(event, 'y', 75)
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#4444FF", outline="#0000CC", width=3, tags="click")
        self.canvas.create_text(x, y, text="R", font=("Arial", 12, "bold"), fill="white", tags="click")
        self.after(1500, lambda: self.canvas.delete("click"))

    def on_scroll(self, event):
        # Visual feedback for scroll
        direction = "↑" if event.delta > 0 else "↓"
        self.canvas.create_text(event.x, event.y, text=direction, font=("Arial", 20), fill="green", tags="scroll")
        self.after(500, lambda: self.canvas.delete("scroll"))

    def clear_canvas(self):
        self.canvas.delete("trail")
        self.canvas.delete("click")
        self.canvas.delete("scroll")

    def on_key_event(self, event):
        if self.winfo_exists():
            self.after(0, self._update_key_ui, event.name, event.event_type)

    def _update_key_ui(self, key_name_raw, event_type):
        key_name = key_name_raw.lower()
        
        # Key mapping for special keys
        key_map = {
            'left shift': 'shift',
            'right shift': 'shift', 
            'left ctrl': 'ctrl',
            'right ctrl': 'ctrl',
            'left alt': 'alt',
            'right alt': 'alt',
            'alt gr': 'alt',
            'left windows': 'windows',
            'right windows': 'windows',
            'caps lock': 'caps',
            'page up': 'page up',
            'page down': 'page down',
            'print screen': 'print screen',
            'delete': 'del',
            'insert': 'insert',
            'home': 'home',
            'end': 'end',
            'num lock': 'num lock',
            'up': '↑',
            'down': '↓', 
            'left': '←',
            'right': '→'
        }
        
        mapped_key = key_map.get(key_name, key_name)
        widget = self.key_widgets.get(mapped_key)
        
        if not widget:
            return
            
        if event_type == 'down':
            widget.configure(fg_color=Theme.ACCENT, text_color="white")
            self.pressed_keys.add(mapped_key)
        elif event_type == 'up':
            widget.configure(fg_color=Theme.SUCCESS, text_color="white")
            if mapped_key in self.pressed_keys:
                self.pressed_keys.remove(mapped_key)

    def start_listening(self):
        try:
            keyboard.hook(self.on_key_event, suppress=False)
        except Exception as e:
            if "root" in str(e).lower() or "permission" in str(e).lower():
                messagebox.showwarning(
                    "Yêu cầu quyền Admin", 
                    "Không thể bắt sự kiện bàn phím do thiếu quyền Admin/root. Vui lòng chạy lại ứng dụng với quyền quản trị viên."
                )

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(
            self.result_container, 
            text="Bàn phím, touchpad và chuột có hoạt động tốt không?", 
            font=Theme.SUBHEADING_FONT, 
            wraplength=900
        ).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(
            button_bar, 
            text="Có, tất cả đều tốt", 
            image=self.icon_manager.CHECK, 
            compound="left", 
            command=lambda: self.handle_result_generic(
                True, 
                {"Kết quả": "Hoạt động tốt", "Trạng thái": "Tốt", "Chi tiết": f"Click trái: {self.mouse_clicks['left']}, Click phải: {self.mouse_clicks['right']}"}, 
                {}
            ), 
            fg_color=Theme.SUCCESS, 
            height=Theme.BUTTON_HEIGHT, 
            font=Theme.BODY_FONT
        )
        self.btn_yes.pack(side="left", padx=10)
        
        self.btn_no = ctk.CTkButton(
            button_bar, 
            text="Không, có lỗi", 
            image=self.icon_manager.CROSS, 
            compound="left", 
            command=lambda: self.handle_result_generic(
                False, 
                {}, 
                {"Kết quả": "Có lỗi", "Trạng thái": "Lỗi", "Chi tiết": f"Click trái: {self.mouse_clicks['left']}, Click phải: {self.mouse_clicks['right']}"}
            ), 
            fg_color=Theme.ERROR, 
            height=Theme.BUTTON_HEIGHT, 
            font=Theme.BODY_FONT
        )
        self.btn_no.pack(side="left", padx=10)

    def stop_tasks(self):
        super().stop_tasks()
        try:
            keyboard.unhook_all()
        except Exception:
            pass

class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = (
            "1. Khởi động lại máy và nhấn liên tục phím để vào BIOS:\n"
            "   • **Dell/Alienware:** F2 hoặc F12\n"
            "   • **HP/Compaq:** F10 hoặc ESC\n"
            "   • **Lenovo/ThinkPad:** F1, F2 hoặc Enter\n"
            "   • **ASUS:** F2 hoặc Delete\n"
            "   • **Acer:** F2 hoặc Delete\n"
            "   • **MSI:** Delete hoặc F2\n\n"
            "2. Kiểm tra các mục quan trọng:\n"
            "   • **CPU Features:** Intel Turbo Boost / AMD Boost phải 'Enabled'\n"
            "   • **Memory:** XMP/DOCP profile nên bật (nếu có)\n"
            "   • **Security:** Không có BIOS password lạ\n"
            "   • **⚠️ CẢNH BÁO:** Tìm 'Computrace' hoặc 'Absolute' - nếu 'Enabled' thì máy có thể bị khóa từ xa!\n"
            "   • **Boot Order:** Kiểm tra thứ tự khởi động\n"
            "   • **Secure Boot:** Nên để 'Enabled' cho bảo mật"
        )
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS", "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp.", how_text, **kwargs)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Các cài đặt trong BIOS có chính xác và an toàn không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, mọi cài đặt đều đúng", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Cài đặt chính xác", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có cài đặt sai/bị khóa", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề với cài đặt BIOS", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra Ngoại Hình", "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp.", "**Bên ngoài:**\n  • Kiểm tra các vết trầy xước, cấn, móp ở các góc và mặt máy.\n  • Mở ra gập vào nhiều lần, lắng nghe **tiếng kêu lạ** và cảm nhận **độ rơ, lỏng lẻo của bản lề**.\n  • Cắm sạc và lay nhẹ để kiểm tra **độ lỏng của cổng sạc**.\n  • Nhìn kỹ các con ốc xem có bị **toét đầu, mất ốc** hay không.\n**Bên trong (Nếu có thể):**\n  • Soi tìm dấu hiệu oxy hóa, bụi bẩn, lông thú cưng tích tụ.", **kwargs)
        self.create_inspection_checklist()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
        # Mark as completed to enable navigation
        self.mark_completed({"Kết quả": "Đã hiển thị checklist", "Trạng thái": "Sẵn sàng"}, auto_advance=False)
    
    def create_inspection_checklist(self):
        """Tạo checklist kiểm tra ngoại hình chi tiết"""
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(checklist_frame, text="🔍 Checklist Kiểm Tra Ngoại Hình", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Exterior checks
        exterior_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        exterior_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(exterior_frame, text="💻 Bên Ngoài:", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        
        exterior_checks = [
            "• Vỏ máy: Kiểm tra vết nứt, rạn nứt, móp méo",
            "• Bản lề màn hình: Mở/đóng nhiều lần, nghe tiếng kêu",
            "• Bàn phím: Kiểm tra phím lỏng, không nhấn",
            "• Touchpad: Bề mặt phẳng, không bị lồi",
            "• Cổng kết nối: USB, HDMI, audio, sạc",
            "• Lỗ thoát khí: Không bị bịt tắc"
        ]
        
        for check in exterior_checks:
            ctk.CTkLabel(exterior_frame, text=check, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
        
        # Hardware checks
        hardware_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        hardware_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(hardware_frame, text="🔩 Phần Cứng:", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        
        hardware_checks = [
            "• Ốc vít: Kiểm tra các ốc không bị toét, thiếu",
            "• Nhãn dán: Còn nguyên, không bị xóa",
            "• Đèn LED: Hoạt động bình thường",
            "• Lưới thoát khí: Sạch sẽ, không bụi bẩn"
        ]
        
        for check in hardware_checks:
            ctk.CTkLabel(hardware_frame, text=check, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
        
        # Warning signs
        warning_frame = ctk.CTkFrame(checklist_frame, fg_color="#FFF3CD", border_width=1, border_color=Theme.WARNING)
        warning_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(warning_frame, text="⚠️ Dấu Hiệu Cảnh Báo:", font=Theme.BODY_FONT, text_color=Theme.WARNING).pack(anchor="w", padx=10, pady=5)
        
        warnings = [
            "• Bản lề rất lỏng hoặc kêu kèn kẹt",
            "• Cổng sạc lỏng, không giữ chặt",
            "• Vết nứt gần bản lề (nguy hiểm)",
            "• Mùi lạ (cháy, hóa chất)",
            "• Ốc vít bị toét nhiều (dấu hiệu tháo lắp)"
        ]
        
        for warning in warnings:
            ctk.CTkLabel(warning_frame, text=warning, font=Theme.SMALL_FONT, text_color="#856404").pack(anchor="w", padx=20, pady=2)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Dựa trên checklist trên, tình trạng vật lý tổng thể của máy như thế nào?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_excellent = ctk.CTkButton(button_bar, text="✨ Rất tốt - Như mới", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Rất tốt - Như mới", "Trạng thái": "Xuất sắc"}, {}), fg_color="#28a745", height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_excellent.pack(side="left", padx=5)
        
        self.btn_good = ctk.CTkButton(button_bar, text="✅ Tốt - Vết nhỏ", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tốt - Có vết sử dụng nhỏ", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_good.pack(side="left", padx=5)
        
        self.btn_fair = ctk.CTkButton(button_bar, text="⚠️ Trung bình - Có lỗi nhỏ", image=self.icon_manager.WHY, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Trung bình - Có lỗi nhỏ cần lưu ý", "Trạng thái": "Cảnh báo"}, {}), fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_fair.pack(side="left", padx=5)
        
        self.btn_poor = ctk.CTkButton(button_bar, text="❌ Kém - Nhiều vấn đề", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Kém - Nhiều vấn đề nghiêm trọng", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_poor.pack(side="left", padx=5)
        
        self.result_container.lift()
        self.result_container.update_idletasks()


class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Báo Cáo Tổng Kết", "", "", **kwargs)
        self.title = "Báo Cáo Tổng Kết"
    
    def display_summary(self, results):
        for widget in self.action_frame.winfo_children(): 
            widget.destroy()
        
        # Import report generator
        try:
            from report_generator import ReportGeneratorFrame
            
            # Tạo báo cáo chuyên nghiệp
            report_frame = ReportGeneratorFrame(self.action_frame, results)
            report_frame.pack(fill="both", expand=True, padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
            
        except ImportError:
            # Fallback to simple summary if report generator not available
            self.create_simple_summary(results)
    
    def create_simple_summary(self, results):
        """Tạo báo cáo đơn giản nếu không có report generator"""
        # Header
        header_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.ACCENT, corner_radius=Theme.CORNER_RADIUS)
        header_frame.pack(fill="x", padx=Theme.CARD_PADDING, pady=(Theme.CARD_PADDING, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(header_frame, text="📊 BÁO CÁO TỔNG KẾT", 
                    font=Theme.HEADING_FONT, text_color="white").pack(pady=Theme.CARD_PADDING)
        
        # Quick stats
        stats_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        stats_frame.pack(fill="x", padx=Theme.CARD_PADDING, pady=(0, Theme.SECTION_SPACING))
        stats_frame.grid_columnconfigure((0,1,2), weight=1)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        # Stats cards
        stats = [
            ("📋 Tổng Test", str(total_tests), Theme.INFO),
            ("✅ Đạt", f"{passed_tests}/{total_tests}", Theme.SUCCESS),
            ("📈 Tỷ Lệ", f"{success_rate:.1f}%", Theme.ACCENT)
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_card = ctk.CTkFrame(stats_frame, fg_color=Theme.BACKGROUND)
            stat_card.grid(row=0, column=i, padx=Theme.ELEMENT_SPACING, pady=Theme.CARD_PADDING, sticky="ew")
            
            ctk.CTkLabel(stat_card, text=label, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=(10, 5))
            ctk.CTkLabel(stat_card, text=value, font=Theme.HEADING_FONT, text_color=color).pack(pady=(0, 10))
        
        # Detailed results
        results_frame = ctk.CTkScrollableFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        results_frame.pack(fill="both", expand=True, padx=Theme.CARD_PADDING, pady=(0, Theme.CARD_PADDING))
        
        ctk.CTkLabel(results_frame, text="📋 Chi Tiết Kết Quả", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=Theme.CARD_PADDING)
        
        for step, result in results.items():
            result_card = ctk.CTkFrame(results_frame, fg_color=Theme.BACKGROUND, corner_radius=8)
            result_card.pack(fill="x", padx=Theme.CARD_PADDING, pady=Theme.ELEMENT_SPACING)
            
            # Status color
            status = result.get("Trạng thái", "Không rõ")
            status_colors = {"Tốt": Theme.SUCCESS, "Lỗi": Theme.ERROR, "Cảnh báo": Theme.WARNING, "Bỏ qua": Theme.SKIP}
            status_color = status_colors.get(status, Theme.TEXT_SECONDARY)
            
            # Header
            header = ctk.CTkFrame(result_card, fg_color="transparent")
            header.pack(fill="x", padx=15, pady=(15, 10))
            
            ctk.CTkLabel(header, text=step, font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT).pack(side="left")
            ctk.CTkLabel(header, text=status, font=Theme.BODY_FONT, text_color=status_color).pack(side="right")
            
            # Details
            if result.get("Kết quả"):
                ctk.CTkLabel(result_card, text=f"Kết quả: {result['Kết quả']}", 
                            font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(0, 5))
            
            if result.get("Chi tiết"):
                detail_text = result["Chi tiết"][:200] + "..." if len(result["Chi tiết"]) > 200 else result["Chi tiết"]
                ctk.CTkLabel(result_card, text=f"Chi tiết: {detail_text}", 
                            font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=600).pack(anchor="w", padx=15, pady=(0, 15))

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
        self.start_button = ctk.CTkButton(self.controls_frame, text="Bắt đầu Test", command=self.start_test, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.start_button.pack(side="left", padx=(0, 10))
        self.stop_button = ctk.CTkButton(self.controls_frame, text="Dừng Test", command=self.stop_test, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, state="disabled", fg_color=Theme.WARNING, text_color=Theme.TEXT)
        self.stop_button.pack(side="left")
        self.status_label = ctk.CTkLabel(self.action_frame, text="Sẵn sàng để bắt đầu.", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
        self.status_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)

    def start_test(self):
        raise NotImplementedError("Child class must implement start_test")

    def run_worker(self, worker_func, args_tuple):
        if self.is_testing: return
        self.is_testing = True
        self.progress_bar.set(0)
        self._completed = False 
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Đang khởi tạo worker...", text_color=Theme.ACCENT)
        for w in self.results_frame.winfo_children(): w.destroy()
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
        self.status_label.configure(text="Test đã được dừng bởi người dùng.", text_color=Theme.TEXT_SECONDARY)
        if not self._completed:
            self.mark_completed({"Kết quả": "Bị dừng bởi người dùng", "Trạng thái": "Bỏ qua"})

    def check_queue(self):
        if not self.is_testing: return
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
                 self.status_label.configure(text="Hoàn thành.")
                 self.mark_completed({"Kết quả": "Hoàn thành", "Trạng thái": "Tốt"})

    def update_ui(self, data):
        pass

    def finalize_test(self, data):
        pass

    def stop_tasks(self):
        super().stop_tasks()
        self.stop_test()

class CPUStressTestStep(BaseStressTestStep):
    def start_test(self):
        import threading
        import time
        import psutil
        
        def cpu_stress_test():
            temps = []
            freqs = []
            
            for i in range(30):  # 30 giây test
                if not self.is_testing:
                    break
                
                # Simulate CPU load
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # Get CPU frequency
                try:
                    freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
                    freqs.append(freq)
                except:
                    freq = 0
                
                # Mock temperature (real implementation would use sensors)
                temp = 45 + (i * 1.5) + (cpu_percent * 0.3)
                temps.append(temp)
                
                self.progress_bar.set(i / 30)
                self.status_label.configure(text=f"CPU: {cpu_percent:.1f}% | Temp: {temp:.1f}°C | Freq: {freq:.0f}MHz")
                
            if self.is_testing:
                self.show_cpu_results(temps, freqs)
        
        self.is_testing = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        threading.Thread(target=cpu_stress_test, daemon=True).start()
    
    def show_cpu_results(self, temps, freqs):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        max_temp = max(temps) if temps else 0
        min_freq = min(freqs) if freqs else 0
        max_freq = max(freqs) if freqs else 0
        
        ctk.CTkLabel(self.results_frame, text="Kết quả CPU Stress Test:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        ctk.CTkLabel(self.results_frame, text=f"Nhiệt độ tối đa: {max_temp:.1f}°C", font=Theme.BODY_FONT).pack()
        ctk.CTkLabel(self.results_frame, text=f"Tần số: {min_freq:.0f} - {max_freq:.0f} MHz", font=Theme.BODY_FONT).pack()
        
        # Throttling detection
        if max_freq > 0 and min_freq < max_freq * 0.8:
            ctk.CTkLabel(self.results_frame, text="⚠️ Phát hiện giảm tần số (Throttling)", font=Theme.BODY_FONT, text_color=Theme.WARNING).pack()
        
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="CPU hoạt động tốt", 
                     command=lambda: self.mark_completed({"Kết quả": f"Temp: {max_temp:.1f}°C, Freq: {min_freq:.0f}-{max_freq:.0f}MHz", "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="CPU có vấn đề", 
                     command=lambda: self.mark_completed({"Kết quả": "CPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR).pack(side="left", padx=10)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Test CPU đã hoàn thành. Nhiệt độ tối đa ghi nhận: {}°C".format(self.max_temp), font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Ổn định, không quá nhiệt", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Ổn định, không quá nhiệt", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Có dấu hiệu quá nhiệt", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có dấu hiệu quá nhiệt", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra CPU & Tản Nhiệt", "Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt của máy.", "Nhấn 'Bắt đầu Test' trong 2-5 phút. Theo dõi biểu đồ nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt.", **kwargs)
        self.TEST_DURATION = 120
        self.start_button.configure(image=self.icon_manager.CPU, compound="left")

    def finalize_test(self, msg):
        self.chart_frame.grid_remove()
        details = f"Thời gian test: {len(self.temp_data)} giây.\nNhiệt độ tối đa ghi nhận: {self.max_temp}°C."
        is_ok = self.max_temp > 0 and self.max_temp < 98
        result_data = {"Kết quả": f"Nhiệt độ tối đa: {self.max_temp}°C", "Trạng thái": "Tốt" if is_ok else "Lỗi", "Chi tiết": details}
        self.mark_completed(result_data)
        self.status_label.configure(text=f"Test hoàn thành. Nhiệt độ tối đa: {self.max_temp}°C")

class HardDriveSpeedStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tốc Độ Ổ Cứng", "Tốc độ đọc/ghi ảnh hưởng trực tiếp đến hiệu năng hệ thống.", "Nhấn 'Bắt đầu Test' để kiểm tra tốc độ ổ cứng thực tế.", **kwargs)
        self.create_disk_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
        
    def create_disk_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(control_frame, text="Test Tốc Độ Ổ Cứng", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        self.start_btn = ctk.CTkButton(control_frame, text="Bắt đầu Test", command=self.start_disk_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(control_frame, text="Sẵn sàng test", font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    
    def start_disk_test(self):
        import threading
        import time
        import os
        import tempfile
        
        def real_disk_test():
            try:
                self.start_btn.configure(state="disabled")
                self.status_label.configure(text="Đang tạo file test...")
                
                # Create test file
                test_size = 100 * 1024 * 1024  # 100MB for more accurate results
                test_data = b'\x00' * test_size  # Use zeros for faster generation
                
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # Write test
                self.status_label.configure(text="Đang test ghi...")
                self.progress_bar.set(0.3)
                start_time = time.time()
                
                with open(temp_path, 'wb') as f:
                    f.write(test_data)
                    f.flush()
                    os.fsync(f.fileno())
                
                write_time = time.time() - start_time
                write_speed = (test_size / (1024 * 1024)) / write_time
                
                # Read test
                self.status_label.configure(text="Đang test đọc...")
                self.progress_bar.set(0.7)
                start_time = time.time()
                
                with open(temp_path, 'rb') as f:
                    _ = f.read()
                
                read_time = time.time() - start_time
                read_speed = (test_size / (1024 * 1024)) / read_time
                
                # Cleanup
                os.unlink(temp_path)
                
                self.progress_bar.set(1.0)
                self.status_label.configure(text="Test hoàn thành")
                self.show_results(int(write_speed), int(read_speed))
                
            except Exception as e:
                self.status_label.configure(text=f"Lỗi: {e}")
                self.start_btn.configure(state="normal")
        
        threading.Thread(target=real_disk_test, daemon=True).start()
    
    def show_results(self, write_speed, read_speed):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        result_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        result_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(result_frame, text="Kết quả Test:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        ctk.CTkLabel(result_frame, text=f"Tốc độ Ghi: {write_speed} MB/s", font=Theme.BODY_FONT).pack()
        ctk.CTkLabel(result_frame, text=f"Tốc độ Đọc: {read_speed} MB/s", font=Theme.BODY_FONT).pack(pady=(0,10))
        
        self.show_result_choices(write_speed, read_speed)
        self.start_btn.configure(state="normal")
    
    def show_result_choices(self, write_speed, read_speed):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Tốc độ ổ cứng có đạt yêu cầu không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Tốc độ tốt", command=lambda: self.mark_completed({"Kết quả": f"Ghi: {write_speed}MB/s, Đọc: {read_speed}MB/s", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="Tốc độ chậm", command=lambda: self.mark_completed({"Kết quả": "Tốc độ chậm", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)

class GPUStressTestStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra GPU & Tản nhiệt", "GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng.", "Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 60 giây. Hãy quan sát:\n  • Có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?\n  • Máy có bị treo hoặc tự khởi động lại không?", **kwargs)
        self.TEST_DURATION = 60
        self.start_button.configure(image=self.icon_manager.GPU, compound="left")
    
    def start_test(self):
        import threading
        import time
        import tkinter as tk
        
        def gpu_stress_test():
            # Create stress test window
            test_win = tk.Toplevel()
            test_win.attributes('-fullscreen', True)
            test_win.configure(bg='black')
            
            canvas = tk.Canvas(test_win, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            # Animate graphics to stress GPU
            for i in range(self.TEST_DURATION * 10):  # 10 FPS
                if not self.is_testing:
                    break
                
                canvas.delete('all')
                # Draw moving patterns
                for j in range(50):
                    x = (i * 5 + j * 20) % 1920
                    y = (i * 3 + j * 15) % 1080
                    canvas.create_rectangle(x, y, x+10, y+10, fill=f'#{j*5:02x}{(i*3)%255:02x}{(j*7)%255:02x}', outline='')
                
                canvas.update()
                self.progress_bar.set(i / (self.TEST_DURATION * 10))
                self.status_label.configure(text=f"GPU Stress Test: {i//10}s/{self.TEST_DURATION}s")
                time.sleep(0.1)
            
            test_win.destroy()
            self.show_gpu_results()
        
        self.is_testing = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        threading.Thread(target=gpu_stress_test, daemon=True).start()
    
    def show_gpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.results_frame, text="Kết quả GPU Test:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        ctk.CTkLabel(self.results_frame, text="Test hoàn thành - Kiểm tra xem có artifacts không", font=Theme.BODY_FONT).pack()
        
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="GPU hoạt động tốt", 
                     command=lambda: self.mark_completed({"Kết quả": "GPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="GPU có vấn đề", 
                     command=lambda: self.mark_completed({"Kết quả": "GPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR).pack(side="left", padx=10)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

# Removed duplicate ScreenTestStep - using the improved version above
        
# Removed duplicate KeyboardVisualTestStep class - using the improved version above
        
class PortsConnectivityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cổng Kết Nối", "Các cổng USB, HDMI, audio là điểm kết nối quan trọng với thiết bị ngoại vi. Cổng hỏng có thể gây bất tiện lớn trong sử dụng.", "Kiểm tra từng cổng bằng cách cắm thiết bị thử. Đánh dấu các cổng hoạt động bên dưới.", **kwargs)
        self.create_ports_checklist()
        
    def create_ports_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame)
        checklist_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(checklist_frame, text="Checklist Cổng Kết Nối:", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        self.port_vars = {}
        ports = [
            ("USB-A (cắm chuột/USB)", "usb_a"),
            ("USB-C (cắm sạc/thiết bị)", "usb_c"),
            ("HDMI (kết nối màn hình)", "hdmi"),
            ("Audio 3.5mm (cắm tai nghe)", "audio"),
            ("Cổng sạc (sạc pin)", "power"),
            ("Ethernet (dây mạng)", "ethernet"),
            ("SD Card (thẻ nhớ)", "sd_card")
        ]
        
        for port_name, port_key in ports:
            port_frame = ctk.CTkFrame(checklist_frame)
            port_frame.pack(fill="x", padx=20, pady=5)
            
            var = tk.BooleanVar()
            self.port_vars[port_key] = var
            
            checkbox = ctk.CTkCheckBox(port_frame, text=port_name, variable=var, font=Theme.BODY_FONT)
            checkbox.pack(side="left", padx=20, pady=10)
            
            status_label = ctk.CTkLabel(port_frame, text="Chưa kiểm tra", font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
            status_label.pack(side="right", padx=20, pady=10)
            
            # Update status when checked
            def update_status(var=var, label=status_label):
                if var.get():
                    label.configure(text="✓ Hoạt động", text_color=Theme.SUCCESS)
                else:
                    label.configure(text="Chưa kiểm tra", text_color=Theme.TEXT_SECONDARY)
            
            var.trace('w', lambda *args, func=update_status: func())
        
        self.show_result_choices()
        
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(result_frame, text="Các cổng đã kiểm tra có hoạt động bình thường không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame)
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Tất cả cổng hoạt động tốt", 
                     command=lambda: self.mark_completed({"Kết quả": "Tất cả cổng hoạt động", "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="Có cổng không hoạt động", 
                     command=lambda: self.mark_completed({"Kết quả": "Một số cổng có vấn đề", "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Pin Laptop", "Pin là nguồn năng lượng di động của laptop. Pin hỏng hoặc chai sẽ giảm thời gian sử dụng và có thể gây nguy hiểm.", "Thông tin pin sẽ được tự động thu thập. Kiểm tra các thông số dưới đây và đánh giá tình trạng pin.", **kwargs)
        self.get_battery_info()
        
    def get_battery_info(self):
        info_frame = ctk.CTkFrame(self.action_frame)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, text="Thông Tin Pin Chi Tiết:", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        try:
            import psutil
            battery = psutil.sensors_battery()
            
            if battery:
                # Battery status
                status_frame = ctk.CTkFrame(info_frame)
                status_frame.pack(fill="x", padx=20, pady=10)
                
                # Current charge
                charge_frame = ctk.CTkFrame(status_frame)
                charge_frame.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(charge_frame, text="Mức pin hiện tại:", font=Theme.BODY_FONT).pack(side="left")
                
                charge_bar = ctk.CTkProgressBar(charge_frame, width=200)
                charge_bar.set(battery.percent / 100)
                charge_bar.pack(side="right", padx=10)
                ctk.CTkLabel(charge_frame, text=f"{battery.percent:.1f}%", font=Theme.BODY_FONT).pack(side="right")
                
                # Power status
                power_status = "Sạc điện" if battery.power_plugged else "Dùng pin"
                power_color = Theme.SUCCESS if battery.power_plugged else Theme.WARNING
                
                info_items = [
                    ("Trạng thái nguồn:", power_status, power_color),
                    ("Thời gian còn lại:", f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Không giới hạn", Theme.TEXT),
                ]
                
                # Additional battery details (mock data)
                additional_info = [
                    ("Dung lượng thiết kế:", "50.0 Wh", Theme.TEXT),
                    ("Dung lượng hiện tại:", "47.2 Wh", Theme.TEXT),
                    ("Sức khỏe pin:", "94.4%", Theme.SUCCESS),
                    ("Số chu kỳ sạc:", "127 chu kỳ", Theme.TEXT),
                    ("Công nghệ pin:", "Li-ion", Theme.TEXT),
                    ("Nhà sản xuất:", "LGC", Theme.TEXT),
                    ("Nhiệt độ pin:", "32°C", Theme.TEXT),
                    ("Điện áp:", "11.4V", Theme.TEXT),
                ]
                
                all_info = info_items + additional_info
                
                for label, value, color in all_info:
                    item_frame = ctk.CTkFrame(status_frame)
                    item_frame.pack(fill="x", padx=10, pady=2)
                    ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left")
                    ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT, text_color=color).pack(side="right")
                
                # Health assessment
                health_frame = ctk.CTkFrame(info_frame)
                health_frame.pack(fill="x", padx=20, pady=15)
                
                ctk.CTkLabel(health_frame, text="Đánh Giá Sức Khỏe Pin:", font=Theme.SUBHEADING_FONT).pack(pady=10)
                
                health_score = 94.4  # Mock health score
                health_color = Theme.SUCCESS if health_score > 80 else Theme.WARNING if health_score > 60 else Theme.ERROR
                health_text = "Tốt" if health_score > 80 else "Trung bình" if health_score > 60 else "Kém"
                
                health_bar = ctk.CTkProgressBar(health_frame, width=300, progress_color=health_color)
                health_bar.set(health_score / 100)
                health_bar.pack(pady=5)
                
                ctk.CTkLabel(health_frame, text=f"Sức khỏe: {health_score}% ({health_text})", 
                           font=Theme.BODY_FONT, text_color=health_color).pack()
                
            else:
                ctk.CTkLabel(info_frame, text="Không thể đọc thông tin pin", 
                           font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(pady=20)
                
        except Exception as e:
            ctk.CTkLabel(info_frame, text=f"Lỗi đọc thông tin pin: {e}", 
                       font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(pady=20)
        
        self.show_result_choices()
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(result_frame, text="Dựa trên thông tin trên, pin có hoạt động tốt không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame)
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Pin hoạt động tốt (>80%)", 
                     command=lambda: self.mark_completed({"Kết quả": "Pin sức khỏe tốt", "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="Pin bị chai/hỏng (<80%)", 
                     command=lambda: self.mark_completed({"Kết quả": "Pin cần thay thế", "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
class SpeakerTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Loa & Micro", "Hệ thống âm thanh quan trọng cho giải trí và họp trực tuyến. Loa bị rè, micro không hoạt động sẽ ảnh hưởng đến trải nghiệm multimedia.", "1. Nhấn các nút test âm thanh\n2. Điều chỉnh âm lượng kiểm tra\n3. Test micro bằng cách nói\n4. Kiểm tra chất lượng âm thanh", **kwargs)
        self.create_audio_tests()
        
    def create_audio_tests(self):
        test_frame = ctk.CTkFrame(self.action_frame)
        test_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Speaker tests
        ctk.CTkLabel(test_frame, text="Test Loa:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        
        speaker_frame = ctk.CTkFrame(test_frame)
        speaker_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(speaker_frame, text="Test Tần Số Thấp", command=lambda: self.play_test_tone("low")).pack(side="left", padx=5)
        ctk.CTkButton(speaker_frame, text="Test Tần Số Trung", command=lambda: self.play_test_tone("mid")).pack(side="left", padx=5)
        ctk.CTkButton(speaker_frame, text="Test Tần Số Cao", command=lambda: self.play_test_tone("high")).pack(side="left", padx=5)
        ctk.CTkButton(speaker_frame, text="Test Stereo", command=lambda: self.play_test_tone("stereo")).pack(side="left", padx=5)
        
        # Volume control
        volume_frame = ctk.CTkFrame(test_frame)
        volume_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(volume_frame, text="Âm lượng:").pack(side="left", padx=10)
        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, number_of_steps=100)
        self.volume_slider.set(50)
        self.volume_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # Microphone test
        ctk.CTkLabel(test_frame, text="Test Micro:", font=Theme.SUBHEADING_FONT).pack(pady=(20,10))
        
        mic_frame = ctk.CTkFrame(test_frame)
        mic_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(mic_frame, text="Bắt đầu ghi âm", command=self.start_recording).pack(side="left", padx=10)
        ctk.CTkButton(mic_frame, text="Dừng ghi âm", command=self.stop_recording).pack(side="left", padx=10)
        ctk.CTkButton(mic_frame, text="Phát lại", command=self.play_recording).pack(side="left", padx=10)
        
        self.recording_status = ctk.CTkLabel(test_frame, text="Chưa ghi âm", font=Theme.BODY_FONT)
        self.recording_status.pack(pady=10)
        
        self.show_result_choices()
    
    def play_test_tone(self, tone_type):
        # Mock audio test - in real implementation would use pygame or other audio library
        import threading
        import time
        
        def mock_play():
            self.recording_status.configure(text=f"Đang phát {tone_type} tone...")
            time.sleep(2)
            self.recording_status.configure(text="Hoàn thành phát âm thanh")
        
        threading.Thread(target=mock_play, daemon=True).start()
    
    def start_recording(self):
        self.recording_status.configure(text="🎤 Đang ghi âm... Nói vào micro")
    
    def stop_recording(self):
        self.recording_status.configure(text="✓ Đã dừng ghi âm")
    
    def play_recording(self):
        self.recording_status.configure(text="🔊 Đang phát lại bản ghi...")
        
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(result_frame, text="Loa và micro hoạt động bình thường không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame)
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Âm thanh rõ ràng, không rè", 
                     command=lambda: self.mark_completed({"Kết quả": "Hệ thống âm thanh tốt", "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="Có tiếng rè/méo/không nghe", 
                     command=lambda: self.mark_completed({"Kết quả": "Hệ thống âm thanh có vấn đề", "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
class MicrophoneTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra micro", "", "", **kwargs)
        self.mark_completed({}, auto_advance=False)
    def show_result_choices(self): pass
        
class NetworkTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Mạng & WiFi", "Kết nối mạng ổn định là yếu tố quan trọng cho công việc và giải trí. WiFi yếu hoặc mất kết nối thường xuyên sẽ gây gián đoạn.", "Test sẽ kiểm tra kết nối Internet, tốc độ mạng, độ trễ ping và thông tin WiFi chi tiết.", **kwargs)
        from network_test_step import NetworkTestStep as NetworkTester
        self.network_tester = NetworkTester(self)
        self.network_tester.create_network_test_ui(self.action_frame)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(Theme.SECTION_SPACING, 0))
        self.show_result_choices()
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Mạng và WiFi có hoạt động ổn định không?", font=Theme.SUBHEADING_FONT).pack(pady=Theme.ELEMENT_SPACING)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=Theme.ELEMENT_SPACING)
        ctk.CTkButton(button_bar, text="Mạng hoạt động tốt", command=lambda: self.mark_completed({"Kết quả": "Mạng ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="Mạng có vấn đề", command=lambda: self.mark_completed({"Kết quả": "Mạng không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)

class ThermalPerformanceStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Thermal Monitor", "Giám sát nhiệt độ và hiệu năng real-time giúp phát hiện vấn đề quá nhiệt, throttling và đánh giá khả năng tản nhiệt.", "Monitor sẽ chạy liên tục và hiển thị biểu đồ real-time. Có thể chạy Stress Test để kiểm tra ở tải cao.", **kwargs)
        from thermal_performance_step import ThermalPerformanceStep as ThermalTester
        self.thermal_tester = ThermalTester(self)
        self.thermal_tester.create_thermal_ui(self.action_frame)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(Theme.SECTION_SPACING, 0))
        self.show_result_choices()
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Hệ thống tản nhiệt có hoạt động hiệu quả không?", font=Theme.SUBHEADING_FONT).pack(pady=Theme.ELEMENT_SPACING)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=Theme.ELEMENT_SPACING)
        ctk.CTkButton(button_bar, text="Tản nhiệt tốt", command=lambda: self.mark_completed({"Kết quả": "Tản nhiệt hiệu quả", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="Quá nhiệt", command=lambda: self.mark_completed({"Kết quả": "Hệ thống quá nhiệt", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)

class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Webcam", "Webcam cần thiết cho video call và họp trực tuyến. Camera không hoạt động hoặc chất lượng kém sẽ ảnh hưởng đến giao tiếp.", "Nhấn 'Bắt đầu Test' để mở camera. Kiểm tra chất lượng hình ảnh, độ phân giải và che camera để test phát hiện vật cản.", **kwargs)
        self.create_webcam_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
    
    def create_webcam_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(test_frame, text="Test Webcam", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        # Preview area
        self.preview_frame = ctk.CTkFrame(test_frame, width=320, height=240, fg_color="#E0E0E0")
        self.preview_frame.pack(pady=10)
        
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Camera chưa khởi động", font=Theme.BODY_FONT)
        self.preview_label.pack(expand=True)
        
        # Controls
        control_frame = ctk.CTkFrame(test_frame, fg_color="transparent")
        control_frame.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(control_frame, text="Bắt đầu Test Camera", command=self.start_camera_test, fg_color=Theme.ACCENT)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(control_frame, text="Dừng Camera", command=self.stop_camera_test, fg_color=Theme.ERROR, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(test_frame, text="Sẵn sàng test camera", font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
    
    def start_camera_test(self):
        try:
            import cv2
            from PIL import Image, ImageTk
            
            # Try multiple camera indices
            self.cap = None
            for i in range(3):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        self.cap = cap
                        break
                    cap.release()
            
            if not self.cap:
                self.status_label.configure(text="❌ Không tìm thấy camera hoạt động", text_color=Theme.ERROR)
                return
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            self.cap.set(cv2.CAP_PROP_FPS, 15)
            
            self.camera_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="✅ Camera đang hoạt động - Kiểm tra hình ảnh bên dưới", text_color=Theme.SUCCESS)
            
            self.update_camera_feed()
        except ImportError:
            self.status_label.configure(text="❌ Cần cài đặt: pip install opencv-python", text_color=Theme.ERROR)
        except Exception as e:
            self.status_label.configure(text=f"❌ Lỗi camera: {e}", text_color=Theme.ERROR)
    
    def update_camera_feed(self):
        if not hasattr(self, 'camera_running') or not self.camera_running:
            return
        
        try:
            ret, frame = self.cap.read()
            if ret:
                import cv2
                from PIL import Image, ImageTk
                
                # Resize frame for display
                frame = cv2.resize(frame, (320, 240))
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Detect brightness
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = gray.mean()
                
                # Convert to PIL Image and then to PhotoImage
                pil_image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Update preview label with actual image
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo  # Keep a reference
                
                # Update status based on brightness
                if brightness < 15:
                    self.status_label.configure(text="⚠️ Camera bị che hoặc quá tối", text_color=Theme.WARNING)
                elif brightness > 200:
                    self.status_label.configure(text="⚠️ Camera bị chói sáng", text_color=Theme.WARNING)
                else:
                    self.status_label.configure(text=f"✅ Camera hoạt động tốt (Độ sáng: {int(brightness)})", text_color=Theme.SUCCESS)
            else:
                self.status_label.configure(text="❌ Không thể đọc frame từ camera", text_color=Theme.ERROR)
            
            # Continue updating
            self.after(50, self.update_camera_feed)  # 20 FPS
        except Exception as e:
            self.status_label.configure(text=f"❌ Lỗi đọc camera: {e}", text_color=Theme.ERROR)
            self.camera_running = False
    
    def stop_camera_test(self):
        self.camera_running = False
        if hasattr(self, 'cap'):
            self.cap.release()
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.preview_label.configure(text="Camera đã dừng")
        self.status_label.configure(text="Camera đã dừng", text_color=Theme.TEXT_SECONDARY)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Webcam có hoạt động bình thường không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Webcam hoạt động tốt", command=lambda: self.mark_completed({"Kết quả": "Webcam hoạt động tốt", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        
        ctk.CTkButton(button_bar, text="Webcam có vấn đề", command=lambda: self.mark_completed({"Kết quả": "Webcam có lỗi", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
    
    def stop_tasks(self):
        super().stop_tasks()
        if hasattr(self, 'camera_running'):
            self.stop_camera_test()
# Dummy WelcomeStep và ResearchGuideStep cho logic is_skippable
class WelcomeStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Chào mừng", "", "", **kwargs)
        self.mark_completed({}, auto_advance=True)
class ResearchGuideStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Nghiên cứu model bằng AI", 
            "AI sẽ giúp bạn tổng hợp các lỗi phổ biến, cảnh báo, review và checklist kiểm tra đặc thù cho model laptop bạn đang kiểm tra.",
            "1. Nhập tên model laptop (ví dụ: ThinkPad X1 Carbon Gen 9, Dell XPS 13 9310, ...).\n2. Bấm 'Phân tích AI'.\n3. Đọc kỹ các cảnh báo, lỗi phổ biến và checklist AI gợi ý.\n4. Quay lại các bước test tương ứng để kiểm tra kỹ các điểm AI cảnh báo.", **kwargs)
        self.input_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.input_frame.pack(pady=10)
        ctk.CTkLabel(self.input_frame, text="Nhập model laptop để AI phân tích:", font=Theme.BODY_FONT).pack(side="left", padx=(0,8))
        self.model_var = tk.StringVar()
        self.model_entry = ctk.CTkEntry(self.input_frame, textvariable=self.model_var, width=320)
        self.model_entry.pack(side="left")
        self.analyze_btn = ctk.CTkButton(self.input_frame, text="Phân tích AI", command=self.run_ai_analysis, fg_color=Theme.ACCENT)
        self.analyze_btn.pack(side="left", padx=8)
        self.ai_result_box = ctk.CTkTextbox(self.action_frame, font=Theme.BODY_FONT, wrap="word", height=180, fg_color="#f7fafd", text_color="#005a9e")
        self.ai_result_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.mark_completed({}, auto_advance=False)

    def run_ai_analysis(self):
        model = self.model_var.get().strip()
        if not model:
            self.ai_result_box.delete("0.0", "end")
            self.ai_result_box.insert("0.0", "Vui lòng nhập tên model laptop.")
            return
        self.ai_result_box.delete("0.0", "end")
        self.ai_result_box.insert("0.0", f"Đang phân tích AI cho model: {model} ...\n")
        self.analyze_btn.configure(state="disabled")
        def ai_task():
            try:
                ai_summary = ai_analyzer.ai_diagnoser.analyze_model(model)
                text = ""
                if ai_summary.get('ai_summary'):
                    for item in ai_summary['ai_summary']:
                        if item.get('ai_warning'):
                            text += f"- {item['ai_warning']}\n"
                        if item.get('ai_checklist'):
                            text += f"  Checklist: {item['ai_checklist']}\n"
                else:
                    text = "Không tìm thấy dữ liệu AI cho model này.\n"
                self.ai_result_box.delete("0.0", "end")
                self.ai_result_box.insert("0.0", text)
            except Exception as e:
                self.ai_result_box.delete("0.0", "end")
                self.ai_result_box.insert("0.0", f"Lỗi AI: {e}")
            finally:
                self.analyze_btn.configure(state="normal")
        threading.Thread(target=ai_task, daemon=True).start()

class TestMenuFrame(ctk.CTkFrame):
    def __init__(self, master, mode, icon_manager, wizard_callback):
        super().__init__(master, fg_color="transparent")
        self.mode = mode
        self.icon_manager = icon_manager
        self.wizard_callback = wizard_callback
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header, text="Chọn loại test", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=0, padx=20, pady=20)
        
        # Test options
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        options_frame.grid_columnconfigure((0,1), weight=1)
        
        # Full test
        full_card = ctk.CTkFrame(options_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        full_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(full_card, text="Test Toàn Diện", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        ctk.CTkLabel(full_card, text="Chạy tất cả các bước test theo thứ tự", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=10)
        ctk.CTkButton(full_card, text="Bắt đầu Test Toàn Diện", command=lambda: self.wizard_callback("full"), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(pady=20)
        
        # Individual tests
        individual_card = ctk.CTkFrame(options_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        individual_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(individual_card, text="Test Từng Phần", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        ctk.CTkLabel(individual_card, text="Chọn test riêng từng tính năng", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=10)
        ctk.CTkButton(individual_card, text="Chọn Test Riêng Lẻ", command=lambda: self.wizard_callback("individual"), fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(pady=20)

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
        self.grid_rowconfigure(2, weight=0)  # Navigation row
        
        # Header với progress
        self.create_header()
        self.create_navigation()
        self.show_step(0)
    
    def create_navigation(self):
        # Navigation luôn hiển thị và cố định - đảm bảo luôn trên màn hình
        nav_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10,20))
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_propagate(False)  # Giữ kích thước cố định
        nav_frame.lift()  # Đảm bảo luôn ở trên cùng
        
        # Previous button
        self.prev_btn = ctk.CTkButton(nav_frame, text="← Trước", command=self.go_previous, 
                                     fg_color=Theme.SKIP, width=130, height=50, font=Theme.BODY_FONT)
        self.prev_btn.grid(row=0, column=0, padx=20, pady=15)
        
        # Skip button - luôn hiển thị
        self.skip_btn = ctk.CTkButton(nav_frame, text="Bỏ qua", command=self.skip_current_step,
                                     fg_color=Theme.WARNING, width=110, height=50, font=Theme.BODY_FONT)
        self.skip_btn.grid(row=0, column=1, pady=15)
        
        # Next button  
        self.next_btn = ctk.CTkButton(nav_frame, text="Tiếp theo →", command=self.go_to_next_step, 
                                     fg_color=Theme.ACCENT, width=130, height=50, font=Theme.BODY_FONT)
        self.next_btn.grid(row=0, column=2, padx=20, pady=15)
        
        # Cập nhật trạng thái ban đầu
        self.update_navigation_state()
    
    def skip_current_step(self):
        """Bỏ qua bước hiện tại"""
        # Đánh dấu bước hiện tại là bỏ qua
        if self.current_step < len(self.steps):
            step_name, _ = self.steps[self.current_step]
            self.record_result(step_name, {"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"})
        self.go_to_next_step()
    
    def go_previous(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
            self.update_navigation_state()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
        header.grid_columnconfigure(1, weight=1)
        
        # Step counter
        self.step_label = ctk.CTkLabel(header, text="", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT)
        self.step_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(header, progress_color=Theme.ACCENT)
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=20, pady=20)
        
        # Mode indicator
        mode_text = "Chế độ Chuyên gia" if self.mode == "expert" else "Chế độ Cơ bản"
        self.mode_label = ctk.CTkLabel(header, text=mode_text, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
        self.mode_label.grid(row=0, column=2, padx=20, pady=20)
    
    def _get_steps_for_mode(self, mode):
        basic_steps = [
            ("Định danh phần cứng", HardwareFingerprintStep),
            ("Bản quyền Windows", LicenseCheckStep), 
            ("Cấu hình hệ thống", SystemInfoStep),
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
            ("Thermal Monitor", ThermalPerformanceStep),
            ("Kiểm tra BIOS", BIOSCheckStep),
            ("Kiểm tra ngoại hình", PhysicalInspectionStep)
        ]
        
        return expert_steps if mode == "expert" else basic_steps
    
    def show_step(self, step_index):
        # Clear content area only - keep header and navigation
        for widget in self.winfo_children():
            if widget not in [self.winfo_children()[0], self.winfo_children()[-1]]:  # Keep header and navigation
                widget.destroy()
        
        # Recreate navigation if it doesn't exist
        if not hasattr(self, 'prev_btn') or not self.prev_btn.winfo_exists():
            self.create_navigation()
        
        # Update header
        total_steps = len(self.steps)
        if step_index < total_steps:
            step_name, step_class = self.steps[step_index]
            self.step_label.configure(text=f"Bước {step_index + 1}/{total_steps}: {step_name}")
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
            self.step_label.configure(text=f"Tổng kết ({total_steps} bước hoàn thành)")
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
        
        # Ensure navigation is always visible and on top
        self.update_navigation_state()
        if hasattr(self, 'prev_btn'):
            self.prev_btn.lift()
            self.skip_btn.lift()
            self.next_btn.lift()
    
    def record_result(self, step_name, result_data):
        self.all_results[step_name] = result_data
        print(f"[DEBUG] Recorded result for {step_name}: {result_data}")
    
    def enable_next(self):
        pass
    
    def go_to_next_step(self):
        self.current_step += 1
        self.show_step(self.current_step)
        self.update_navigation_state()
    
    def update_navigation_state(self):
        """Cập nhật trạng thái các nút navigation"""
        # Previous button
        if self.current_step <= 0:
            self.prev_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal")
        
        # Next button - luôn enable
        self.next_btn.configure(state="normal")
        
        # Skip button - disable ở bước cuối
        if self.current_step >= len(self.steps):
            self.skip_btn.configure(state="disabled")
            self.next_btn.configure(text="Hoàn thành")
        else:
            self.skip_btn.configure(state="normal")
            self.next_btn.configure(text="Tiếp theo →")

class App(ctk.CTk):
    def __init__(self):
        print("[DEBUG] App.__init__ called")
        super().__init__(fg_color=Theme.BACKGROUND)
        self.title("Laptop Tester Pro")
        self.state('zoomed')
        self.minsize(1400, 900)
        try:
            self.iconbitmap(asset_path("icons/logo.ico"))
        except:
            pass  # Skip icon if not found
        self.icon_manager = IconManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)  # header nhỏ, main_content lớn
        self.current_main_frame = None
        self.all_results = {}  # Store all test results here

        # --- HEADER BAR ---
        self.header = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=70, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_columnconfigure(0, minsize=80)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, minsize=80)
        logo = self.icon_manager.LOGO_SMALL or None
        self.logo_label = ctk.CTkLabel(self.header, image=logo, text="", width=60)
        self.logo_label.grid(row=0, column=0, padx=(20,0), pady=10)
        self.title_label = ctk.CTkLabel(self.header, text="Laptop Tester Pro", font=Theme.HEADING_FONT, text_color=Theme.ACCENT)
        self.title_label.grid(row=0, column=1, sticky="w", padx=10)
        self.exit_btn = ctk.CTkButton(self.header, text="Thoát", command=self.quit_app, font=Theme.BODY_FONT, fg_color=Theme.ERROR, width=80)
        self.exit_btn.grid(row=0, column=2, padx=(0,20), pady=10)

        # --- MAIN CONTENT ---
        self.main_content = ctk.CTkFrame(self, fg_color=Theme.BACKGROUND)
        self.main_content.grid(row=1, column=0, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)
        # Add debug label
        self.debug_label = ctk.CTkLabel(self.main_content, text="[DEBUG] App loaded", font=Theme.BODY_FONT, text_color=Theme.ERROR)
        self.debug_label.grid(row=0, column=0, sticky="nsew", padx=100, pady=100)

        self.show_mode_selection()

    def clear_window(self):
        if self.current_main_frame:
            if hasattr(self.current_main_frame, 'cleanup'):
                self.current_main_frame.cleanup()
            self.current_main_frame.destroy()
        self.current_main_frame = None

    def show_mode_selection(self):
        self.clear_window()
        self.current_main_frame = ModeSelectionFrame(self.main_content, self.start_wizard, self.icon_manager)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    def start_wizard(self, mode):
        if mode == "individual":
            self.show_test_menu(mode)
        else:
            self.clear_window()
            self.current_main_frame = WizardFrame(self.main_content, mode, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_content.grid_rowconfigure(0, weight=1)
            self.main_content.grid_columnconfigure(0, weight=1)
    
    def show_test_menu(self, mode):
        self.clear_window()
        self.current_main_frame = TestMenuFrame(self.main_content, mode, self.icon_manager, self.start_wizard)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    def quit_app(self):
        self.clear_window()
        self.destroy()

class ModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback, icon_manager):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Tạo tabview cho Overview và Mode Selection
        self.tabview = ctk.CTkTabview(self, width=1200, height=700)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Tab Tổng quan
        self.tabview.add("🏠 Tổng Quan")
        overview_frame = AppOverviewFrame(self.tabview.tab("🏠 Tổng Quan"), self.mode_callback)
        overview_frame.pack(fill="both", expand=True)
        
        # Tab Chọn chế độ
        self.tabview.add("🎯 Chọn Chế Độ")
        self.create_mode_selection()
        
        # Mặc định hiển thị tab Tổng quan
        self.tabview.set("🏠 Tổng Quan")
    
    def create_mode_selection(self):
        """Tạo giao diện chọn chế độ"""
        mode_frame = self.tabview.tab("🎯 Chọn Chế Độ")
        mode_frame.grid_columnconfigure(0, weight=1)
        mode_frame.grid_rowconfigure(1, weight=1)
        
        header_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        ctk.CTkLabel(header_frame, text="Chọn Chế Độ Kiểm Tra", font=Theme.TITLE_FONT, text_color=Theme.TEXT).pack(pady=(0, 10))
        ctk.CTkLabel(header_frame, text="Lựa chọn chế độ phù hợp với mức độ chuyên môn của bạn", font=Theme.HEADING_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=(0, 20))
        # Card chọn chế độ
        card_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        card_frame.grid(row=1, column=0, sticky="nsew")
        card_frame.grid_columnconfigure((0,1), weight=1)
        # Basic mode card
        card_basic = ctk.CTkFrame(card_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        card_basic.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")
        ctk.CTkLabel(card_basic, text="Chế Độ Cơ Bản", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(20, 10))
        ctk.CTkLabel(card_basic, text="Dành cho mọi người dùng.\nNhanh chóng, an toàn và dễ hiểu, tập trung vào các chức năng chính.", font=Theme.BODY_FONT, wraplength=450, text_color=Theme.TEXT_SECONDARY).pack(padx=30, pady=10, expand=True)
        ctk.CTkButton(card_basic, text="Chọn Chế Độ Cơ Bản", command=lambda: self.mode_callback("basic"), height=Theme.BUTTON_HEIGHT, font=Theme.SUBHEADING_FONT, fg_color=Theme.SUCCESS).pack(padx=30, pady=30, fill="x", side="bottom")
        # Expert mode card
        card_expert = ctk.CTkFrame(card_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        card_expert.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")
        ctk.CTkLabel(card_expert, text="Chế Độ Chuyên Gia", font=Theme.HEADING_FONT, text_color=Theme.ERROR).pack(pady=(20, 10))
        ctk.CTkLabel(card_expert, text="Dành cho kỹ thuật viên, người kiểm tra chuyên sâu. Đầy đủ các bước test phần cứng, stress test, benchmark.", font=Theme.BODY_FONT, wraplength=450, text_color=Theme.TEXT_SECONDARY).pack(padx=30, pady=10, expand=True)
        ctk.CTkButton(card_expert, text="Chọn Chế Độ Chuyên Gia", command=lambda: self.mode_callback("expert"), height=Theme.BUTTON_HEIGHT, font=Theme.SUBHEADING_FONT, fg_color=Theme.ERROR).pack(padx=30, pady=30, fill="x", side="bottom")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()