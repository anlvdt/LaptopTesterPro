import customtkinter as ctk
import platform
import threading
import os
import subprocess
from PIL import Image
import time
from tkinter import messagebox, filedialog
import webbrowser
import socket
import locale
import re
import tempfile
import numpy as np
import math
import multiprocessing
import sys
from collections import deque

# --- KIỂM TRA THƯ VIỆN & XỬ LÝ LỖI KHỞI ĐỘNG ---
try:
    if platform.system() == "Windows":
        import pythoncom, wmi, pywifi
        from pywifi import const
    import psutil, cv2, pygame, keyboard, sounddevice as sd
    from scipy.io.wavfile import write as write_wav, read as read_wav
    from bs4 import BeautifulSoup
except ImportError as e:
    requirements_content = "customtkinter\npsutil\nPillow\nopencv-python\npygame\nkeyboard\nsounddevice\nscipy\nbeautifulsoup4\nnumpy\npywifi; platform_system == 'Windows'\npywin32; platform_system == 'Windows'\nWMI; platform_system == 'Windows'"
    instructions = f"Không tìm thấy thư viện quan trọng: '{e.name}'.\n\nHãy tạo file 'requirements.txt' và dán nội dung sau vào:\n\n{requirements_content}\n\nSau đó chạy lệnh: pip install -r requirements.txt"
    print("="*50 + "\nNỘI DUNG CHO FILE requirements.txt:\n" + requirements_content + "\n" + "="*50)
    root = ctk.CTk(); root.withdraw(); messagebox.showerror("Lỗi Thiếu Thư Viện", instructions); root.destroy(); exit()

# --- IMPORT WORKER SCRIPTS ---
# Giả định các file worker nằm cùng thư mục
try:
    from worker_cpu import run_cpu_stress
    from worker_gpu import run_gpu_stress
    from worker_disk import run_benchmark as run_disk_benchmark
except ImportError as e:
    messagebox.showerror("Lỗi Worker", f"Không tìm thấy file worker cần thiết: {e.name}.py. Vui lòng đảm bảo các file worker_*.py nằm cùng thư mục với laptoptester.py.")
    exit()

# --- THEME & ASSETS ---
class Theme:
    BACKGROUND="#F0F2F5"; FRAME="#FFFFFF"; CARD="#FFFFFF"; BORDER="#D9D9D9"; SEPARATOR = "#E8E8E8"
    TEXT="#1C1C1E"; TEXT_SECONDARY="#6D6D72"; ACCENT="#007AFF"; ACCENT_HOVER="#0056b3"
    SUCCESS="#34C759"; WARNING="#FF9500"; ERROR="#FF3B30"; SKIP="#8E8E93"; SKIP_HOVER="#6D6D72"
    TITLE_FONT=("Segoe UI", 48, "bold"); HEADING_FONT=("Segoe UI", 32, "bold"); SUBHEADING_FONT=("Segoe UI", 24, "bold")
    BODY_FONT=("Segoe UI", 18); SMALL_FONT=("Segoe UI", 15)
    CORNER_RADIUS = 16; PADDING_X = 30; PADDING_Y = 25; BUTTON_HEIGHT = 55

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def asset_path(relative_path): return os.path.join(BASE_DIR, "assets", relative_path)

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

# --- LỚP FRAME CƠ SỞ CHO MỖI BƯỚC ---
class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results):
        super().__init__(master, fg_color="transparent")
        
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        
        self.title = title; self.record_result = record_result_callback; self.enable_next_callback = enable_next_callback
        self.go_to_next_step_callback = go_to_next_step_callback; self._completed, self._skipped = False, False
        self.icon_manager = icon_manager; self.all_results = all_results; self.after_id = None
        
        guide_container = ctk.CTkFrame(self, fg_color=Theme.FRAME, width=450, corner_radius=0)
        guide_container.grid(row=0, column=0, sticky="nsw"); guide_container.grid_propagate(False)
        guide_container.grid_columnconfigure(0, weight=1)
        
        why_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        why_frame.grid(row=0, column=0, sticky="ew", padx=Theme.PADDING_X, pady=Theme.PADDING_Y)
        ctk.CTkLabel(why_frame, image=self.icon_manager.WHY, text=" Tại sao cần test?", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT, compound="left").pack(anchor="w")
        ctk.CTkLabel(why_frame, text=why_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.TEXT).pack(anchor="w", pady=(15,0))

        ctk.CTkFrame(guide_container, height=1, fg_color=Theme.SEPARATOR).grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_X, pady=15)

        how_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        how_frame.grid(row=2, column=0, sticky="ew", padx=Theme.PADDING_X, pady=Theme.PADDING_Y)
        ctk.CTkLabel(how_frame, image=self.icon_manager.HOW, text=" Hướng dẫn thực hiện:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT, compound="left").pack(anchor="w")
        ctk.CTkLabel(how_frame, text=how_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.TEXT).pack(anchor="w", pady=(15,0))

        action_container = ctk.CTkFrame(self, fg_color="transparent")
        action_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        action_container.grid_columnconfigure(0, weight=1); action_container.grid_rowconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(action_container, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS)
        self.action_frame.grid(row=0, column=0, sticky="nsew")
        
    def on_show(self): pass 
    def is_ready_to_proceed(self): return self._completed or self._skipped
    def mark_completed(self, result_data, auto_advance=False):
        self._completed = True; self._skipped = False; self.record_result(self.title, result_data); self.enable_next_callback()
        if auto_advance: self.after_id = self.after(500, self.go_to_next_step_callback)
    def mark_skipped(self, result_data): 
        self._skipped = True; self._completed = False; self.record_result(self.title, result_data)
        self.enable_next_callback()
    def handle_result_generic(self, is_ok, ok_data, bad_data, auto_advance_on_ok=False):
        if hasattr(self, 'btn_yes'): self.btn_yes.configure(state="disabled")
        if hasattr(self, 'btn_no'): self.btn_no.configure(state="disabled")
        result = ok_data if is_ok else bad_data
        if is_ok:
            if hasattr(self, 'btn_yes'): self.btn_yes.configure(fg_color=Theme.ACCENT)
            self.mark_completed(result, auto_advance=auto_advance_on_ok)
        else:
            if hasattr(self, 'btn_no'): self.btn_no.configure(fg_color=Theme.WARNING)
            self.mark_completed(result)
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


# --- CÁC BƯỚC KIỂM TRA ---
class WelcomeStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Chào mừng", "Quy trình này sẽ hướng dẫn bạn kiểm tra toàn diện một chiếc laptop cũ theo kinh nghiệm của các chuyên gia.", "Các bước tiếp theo sẽ bao gồm từ nghiên cứu, kiểm tra phần mềm, phần cứng, cho đến các bài test chuyên sâu.", **kwargs)
        self.action_frame.grid_columnconfigure(0, weight=1); self.action_frame.grid_rowconfigure(0, weight=1)
        center_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent"); center_frame.grid(row=0, column=0, sticky="nsew")
        center_frame.grid_columnconfigure(0, weight=1); center_frame.grid_rowconfigure(0, weight=1)
        inner_frame = ctk.CTkFrame(center_frame, fg_color="transparent"); inner_frame.grid(row=0, column=0)
        try:
            logo_image = ctk.CTkImage(Image.open(asset_path("icons/logo.png")), size=(256, 256))
            ctk.CTkLabel(inner_frame, text="", image=logo_image).pack(pady=(15, 20))
        except Exception: print("Cảnh báo: Không tìm thấy file logo.png")
        ctk.CTkLabel(inner_frame, text="Sản phẩm được phát triển bởi Laptop Lê Ẩn và Gemini", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(0, 20))
        self.mark_completed({"Kết quả": "Sẵn sàng", "Trạng thái": "Tốt"}, auto_advance=False)

class ResearchGuideStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Nghiên Cứu", "Đây là bước quan trọng nhất. Một chiếc máy dù hoạt động hoàn hảo nhưng khó sửa chữa, khó nâng cấp và có nhiều lỗi cố hữu sẽ không phải là một khoản đầu tư tốt về lâu dài.", "Hãy dành thời gian nghiên cứu các yếu tố sau về model máy bạn định mua:\n  • Khả năng Sửa chữa: Bàn phím, màn hình có dễ thay thế không? Chi phí là bao nhiêu?\n  • Khả năng Nâng cấp: Máy có RAM hàn hay không? Có bao nhiêu khe cắm SSD/HDD?\n  • Điểm yếu Cố hữu: Model này có hay bị lỗi bản lề, lỗi cổng sạc, quá nhiệt không?", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        button_bar = ctk.CTkFrame(self.action_frame, fg_color="transparent"); button_bar.grid(row=0, column=0)
        ctk.CTkButton(button_bar, text="Tìm Video Sửa Chữa trên YouTube", command=self.open_youtube_search, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(button_bar, text="Tìm Các Lỗi Phổ Biến trên Google", command=self.open_google_search, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).pack(pady=10, padx=20, fill="x")
        self.mark_completed({"Kết quả": "Đã xem hướng dẫn", "Trạng thái": "Tốt"}, auto_advance=False)

    def get_model_from_results(self):
        sys_info = self.all_results.get("Định Danh Phần Cứng", {}).get("Chi tiết", "laptop")
        try:
            for line in sys_info.splitlines():
                if "model laptop:" in line.lower(): return line.split(":")[-1].strip()
            return "laptop"
        except (IndexError, KeyError): return "laptop"

    def open_youtube_search(self): webbrowser.open(f"https://www.youtube.com/results?search_query={self.get_model_from_results().replace(' ', '+')}+disassembly+repair")
    def open_google_search(self): webbrowser.open(f"https://www.google.com/search?q={self.get_model_from_results().replace(' ', '+')}+common+problems")

class HardwareFingerprintStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Định Danh Phần Cứng", "Đây là bước quan trọng nhất để chống lừa đảo. Các thông tin dưới đây được đọc trực tiếp từ BIOS và linh kiện phần cứng. Chúng **cực kỳ khó làm giả** từ bên trong Windows.", "Hãy so sánh các thông tin 'vàng' này với cấu hình mà người bán quảng cáo. Nếu có bất kỳ sự sai lệch nào, hãy đặt câu hỏi và kiểm tra thật kỹ.", **kwargs)
        self.action_frame.grid_columnconfigure(0, weight=1); self.action_frame.grid_rowconfigure(0, weight=1)
        self.info_labels = {}
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.pack(pady=20, padx=20, fill="x"); self.loading_spinner.start()
        self.container = ctk.CTkFrame(self.action_frame, fg_color="transparent"); self.container.grid_columnconfigure(1, weight=1)
        self.info_items = ["Model Laptop", "Serial Number", "CPU", "GPU", "Model Ổ Cứng", "Ngày BIOS"]
        for item in self.info_items:
            row_frame = ctk.CTkFrame(self.container, fg_color="transparent")
            ctk.CTkLabel(row_frame, image=self.icon_manager.SHIELD, text="").pack(side="left", padx=(0, 10))
            ctk.CTkLabel(row_frame, text=f"{item}:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(side="left", padx=(0, 15))
            self.info_labels[item] = ctk.CTkLabel(row_frame, text="", justify="left", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=900)
            self.info_labels[item].pack(side="left"); row_frame.pack(anchor="w", pady=10, padx=20)
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
                hw_info["Serial Number"] = bios.SerialNumber
                bios_date_str = bios.ReleaseDate.split('.')[0]
                hw_info["Ngày BIOS"] = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
                hw_info["CPU"] = c.Win32_Processor()[0].Name.strip()
                hw_info["GPU"] = "\n".join([gpu.Name for gpu in c.Win32_VideoController()])
                hw_info["Model Ổ Cứng"] = "\n".join([d.Model for d in c.Win32_DiskDrive()])
            except Exception as e: hw_info = {k: f"Lỗi WMI: {e}" for k in self.info_items}
            finally: pythoncom.CoUninitialize()
        else: hw_info = {k: "Chỉ hỗ trợ Windows" for k in self.info_items}
        if self.winfo_exists(): self.after(0, self.display_info, hw_info)

    def display_info(self, hw_info):
        full_details = ""
        self.loading_spinner.pack_forget(); self.container.pack(fill="x", padx=20, pady=10)
        for key, value in hw_info.items():
            if key in self.info_labels: self.info_labels[key].configure(text=value)
            full_details += f"  - {key}: {value}\n"
        self.mark_completed({"Kết quả": "Đã lấy định danh phần cứng", "Trạng thái": "Tốt", "Chi tiết": f"Thông tin định danh phần cứng:\n{full_details}"}, auto_advance=False)

class SystemInfoStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cấu Hình Windows", "Bước này hiển thị thông tin cấu hình mà Windows nhận diện và tự động so sánh với thông tin từ BIOS để phát hiện sai lệch.", "Đối chiếu thông tin dưới đây với bước trước và với thông tin quảng cáo. Nếu mọi thứ khớp, chọn 'Cấu hình khớp'.", **kwargs)
        
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        self.container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
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
        self.result_container.grid(row=1, column=0, sticky="s", pady=(20,0))
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
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for key, value in info.items():
            if key in self.info_labels: self.info_labels[key].configure(text=value)
            self.full_info_text += f"{key}: {value}\n"
        
        self.perform_comparison()
        
        ctk.CTkLabel(self.result_container, text="Sau khi đối chiếu, cấu hình có khớp không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, Cấu hình khớp", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Khớp", "Trạng thái": "Tốt", "Chi tiết": self.full_info_text}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có sai lệch", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Không khớp", "Trạng thái": "Lỗi", "Chi tiết": self.full_info_text}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="Sao chép", command=self.copy_to_clipboard, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).pack(side="left", padx=10)

    def normalize_cpu_name(self, name):
        name = name.lower()
        to_remove = ["(r)", "(tm)", "cpu", "@", "ghz", "with radeon graphics", "with vega graphics"]
        for term in to_remove: name = name.replace(term, "")
        return " ".join(name.split())

    def perform_comparison(self):
        hw_data = self.all_results.get("Định Danh Phần Cứng", {}); hw_details = hw_data.get("Chi tiết", "")
        cpu_bios, cpu_win = "N/A", "N/A"
        for line in hw_details.splitlines():
            if "- cpu:" in line.lower(): cpu_bios = line.split(":", 1)[1].strip()
        for line in self.full_info_text.splitlines():
            if "cpu:" in line.lower(): cpu_win = line.split(":", 1)[1].strip()

        norm_bios = self.normalize_cpu_name(cpu_bios); norm_win = self.normalize_cpu_name(cpu_win)
        match = norm_bios in norm_win or norm_win in norm_bios
        
        ctk.CTkLabel(self.comparison_frame, text=f"CPU (BIOS): {cpu_bios}", font=Theme.BODY_FONT, wraplength=800, justify="left").pack(anchor="w")
        ctk.CTkLabel(self.comparison_frame, text=f"CPU (Windows): {cpu_win}", font=Theme.BODY_FONT, wraplength=800, justify="left").pack(anchor="w")
        result_label = ctk.CTkLabel(self.comparison_frame, font=Theme.BODY_FONT)
        if match: result_label.configure(text="Kết quả: Khớp", text_color=Theme.SUCCESS)
        else: result_label.configure(text="Cảnh báo: Có sai lệch", text_color=Theme.ERROR)
        result_label.pack(anchor="w")

    def copy_to_clipboard(self): self.clipboard_clear(); self.clipboard_append(self.full_info_text)

class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bản Quyền Windows", "Một máy tính có bản quyền Windows hợp lệ đảm bảo bạn nhận được các bản cập nhật bảo mật quan trọng và tránh các rủi ro pháp lý.", "Ứng dụng sẽ tự động chạy lệnh kiểm tra trạng thái kích hoạt của Windows. Kết quả sẽ hiển thị bên dưới.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(self.action_frame, text="Đang kiểm tra...", font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT_SECONDARY)
        self.status_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        threading.Thread(target=self.check_license, daemon=True).start()

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
            except (subprocess.CalledProcessError, FileNotFoundError): status, color = "Lỗi khi chạy lệnh kiểm tra", Theme.ERROR
        else: status, color, result_data = "Chỉ hỗ trợ Windows", Theme.SKIP, {"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"}
        if self.winfo_exists(): self.after(0, self.update_ui, status, color, result_data)

    def update_ui(self, status, color, result_data):
        self.status_label.configure(text=status, text_color=color)
        self.mark_completed(result_data, auto_advance=False)

class HardDriveHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Sức Khỏe Ổ Cứng (S.M.A.R.T)", "Ổ cứng sắp hỏng là một rủi ro mất dữ liệu cực lớn. Bước này đọc 'báo cáo y tế' (S.M.A.R.T.) của ổ cứng để đánh giá độ bền.", "Chú ý đến mục 'Trạng thái'. 'Tốt' là bình thường. 'Lỗi/Cảnh báo' là rủi ro cao. Bước tiếp theo sẽ kiểm tra tốc độ thực tế.", **kwargs)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=Theme.ACCENT)
        self.loading_spinner.pack(pady=20, padx=20, fill="x"); self.loading_spinner.start()
        self.drive_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
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
        self.loading_spinner.pack_forget(); self.drive_container.pack(fill='x', expand=True, padx=20, pady=10)
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
        
        ok_data = {"Kết quả": "Tốt", "Trạng thái": "Tốt", "Chi tiết": full_details}
        bad_data = {"Kết quả": "Có ổ cứng lỗi", "Trạng thái": "Lỗi", "Chi tiết": full_details}
        
        if not drives_info or "Chỉ hỗ trợ Windows" in drives_info[0]["Trạng thái"]:
             self.mark_completed({"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"}, auto_advance=False)
        elif has_error: self.mark_completed(bad_data, auto_advance=False)
        else: self.mark_completed(ok_data, auto_advance=False)

class ScreenTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Màn Hình", "Màn hình là một trong những linh kiện đắt tiền và dễ hỏng nhất. Lỗi điểm chết, hở sáng, ám màu hay 'ung thư panel' (chớp giật ở cạnh viền) là những vấn đề nghiêm trọng.", "1. **Test Nhanh:** Dùng các nút bên dưới để hiển thị các bài test khác nhau. Nhấn phím [ESC] để thoát.\n2. **Test Nâng cao:** Dùng 'Test Chuyên Sâu 5 Phút' để tự lặp lại màu, giúp phát hiện lỗi chớp giật. Mở 'Web Test' để xem các bài test phức tạp hơn.\n3. **Quan trọng:** Trong lúc test, hãy chỉnh độ sáng lên/xuống mức cao nhất/thấp nhất và đổi tần số quét (60Hz, 120Hz...).", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        self.button_bar_container = ctk.CTkFrame(self.action_frame, fg_color="transparent"); self.button_bar_container.grid(row=0, column=0, sticky="nsew")
        self.button_bar_container.grid_rowconfigure(0, weight=1); self.button_bar_container.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self.button_bar_container, fg_color="transparent"); center_frame.grid(row=0, column=0)
        
        self.button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); self.button_bar.pack(pady=10)
        ctk.CTkButton(self.button_bar, text="Test Màu cơ bản", command=self.run_color_test, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_bar, text="Test Gradient", command=self.run_gradient_test, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_bar, text="Test Chuyên Sâu (5 Phút)", command=lambda: self.run_color_test(duration=300), height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.WARNING, text_color=Theme.TEXT).pack(side="left", padx=10, pady=10)
        web_test_button = ctk.CTkButton(self.button_bar, text="Mở Web Test (EIZO)", command=self.open_eizo, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        web_test_button.pack(side="left", padx=10, pady=10)
        self.web_test_done_button = ctk.CTkButton(center_frame, text="Tôi đã test xong trên web", command=self.prompt_for_more_tests, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)

        self.result_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_frame.grid(row=0, column=0, sticky="nsew"); self.result_frame.grid_remove()

    def _create_fullscreen_window(self):
        win = ctk.CTkToplevel(self); win.attributes("-topmost", True); win.attributes("-fullscreen", True); win.focus_force(); return win
    def open_eizo(self): webbrowser.open("https://www.eizo.be/monitor-test/"); self.web_test_done_button.pack(pady=20)
    def prompt_for_more_tests(self):
        self.web_test_done_button.pack_forget()
        if not messagebox.askyesno("Tiếp tục Test?", "Bạn có muốn thực hiện bài test màn hình khác không?"): self.show_result_choices()
    def run_gradient_test(self):
        win = self._create_fullscreen_window()
        screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
        gradient = np.linspace(0, 255, screen_w, dtype=np.uint8)
        gradient_image_data = np.tile(gradient, (screen_h, 1))
        img = Image.fromarray(gradient_image_data, mode='L'); ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(screen_w, screen_h))
        label = ctk.CTkLabel(win, text="", image=ctk_img); label.pack(expand=True, fill="both")
        win.bind("<Escape>", lambda e: win.destroy() or self.after(100, self.prompt_for_more_tests))

    def run_color_test(self, duration=0):
        win = self._create_fullscreen_window()
        colors = ["white", "black", "red", "green", "blue"]; color_index = 0
        end_time = time.time() + duration if duration > 0 else 0; timer_id = None
        def change_color(event=None):
            nonlocal color_index, timer_id
            if not win.winfo_exists(): return
            if duration > 0 and time.time() > end_time: close_window(); return
            win.configure(fg_color=colors[color_index % len(colors)]); color_index += 1
            if duration > 0: timer_id = win.after(2000, change_color)
        def close_window(event=None):
            if timer_id: win.after_cancel(timer_id)
            if win.winfo_exists(): win.destroy()
            self.after(100, self.prompt_for_more_tests)
        win.bind("<Escape>", close_window)
        if duration == 0: win.bind("<Button-1>", change_color); win.bind("<Right>", change_color)
        change_color()

    def show_result_choices(self):
        if self.result_frame.winfo_viewable(): return
        self.button_bar_container.grid_remove()
        self.result_frame.grid()
        self.result_frame.grid_rowconfigure(0, weight=1); self.result_frame.grid_columnconfigure(0, weight=1)
        center_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent"); center_frame.grid(row=0, column=0)
        ctk.CTkLabel(center_frame, text="Bạn có phát hiện điểm chết, hở sáng, ám màu hay chớp giật bất thường không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Không, màn hình bình thường", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Bình thường", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Có, tôi thấy vấn đề", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class KeyboardTouchpadStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bàn phím & Touchpad", "Một phím bị liệt, kẹt, hoặc touchpad bị loạn/mất cử chỉ đa điểm sẽ làm gián đoạn hoàn toàn công việc.", "**Bàn phím:** Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ được đánh dấu trong checklist bên dưới.\n**Touchpad:**\n   1. Dùng 1 ngón tay vẽ lên vùng màu xám để kiểm tra điểm chết cảm ứng.\n   2. **Quan trọng:** Đặt 2 ngón tay lên vùng vẽ và thử **cuộn lên/xuống** và **chụm/mở để thu phóng**.", **kwargs)
        
        self.action_frame.grid_rowconfigure(1, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.is_listening = False
        self.key_labels = {}
        
        self.canvas = ctk.CTkCanvas(self.action_frame, bg=Theme.FRAME, height=150, highlightthickness=1, highlightbackground=Theme.BORDER)
        self.canvas.grid(row=0, column=0, sticky="ew", pady=(20, 15), padx=20)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        
        key_container = ctk.CTkScrollableFrame(self.action_frame, label_text="Checklist các phím cần kiểm tra", label_font=Theme.BODY_FONT)
        key_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))

        self.populate_keyboard(key_container)

        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="s", pady=(0, 20))
        self.show_result_choices()
        self.start_listening()

    def populate_keyboard(self, parent):
        container_frame = ctk.CTkFrame(parent, fg_color="transparent")
        container_frame.pack(fill="x", expand=True)
        main_keys_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        main_keys_frame.grid(row=0, column=0, sticky="new")
        numpad_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        numpad_frame.grid(row=0, column=1, sticky="new", padx=(20, 0))
        container_frame.grid_columnconfigure(0, weight=3)
        container_frame.grid_columnconfigure(1, weight=1)

        main_keys_layout = {
            "Hàng phím chức năng (F)": ['esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'],
            "Hàng phím số": ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace'],
            "Hàng phím trên (QWERTY)": ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            "Hàng phím giữa (HOME)": ['caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter'],
            "Hàng phím dưới": ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift'],
            "Hàng phím điều khiển": ['ctrl', 'fn', 'windows', 'alt', 'space', 'right alt', 'right ctrl'],
            "Cụm phím điều hướng & chức năng": ['print screen', 'insert', 'delete', 'home', 'end', 'page up', 'page down', 'up', 'down', 'left', 'right']
        }
        
        numpad_keys_layout = {
            "Cụm phím số (Numpad)": [
                'num lock', 'numpad /', 'numpad *', 'numpad -', 'numpad 7', 'numpad 8', 'numpad 9', 'numpad +',
                'numpad 4', 'numpad 5', 'numpad 6', 'numpad 1', 'numpad 2', 'numpad 3', 'numpad enter',
                'numpad 0', 'numpad .'
            ]
        }
        
        self.create_key_section(main_keys_frame, main_keys_layout, 4)
        self.create_key_section(numpad_frame, numpad_keys_layout, 2)

    def create_key_section(self, parent, layout, cols):
        parent.grid_columnconfigure(0, weight=1)
        row_counter = 0
        for title, keys in layout.items():
            ctk.CTkLabel(parent, text=title, font=(*Theme.SMALL_FONT, "bold"), text_color=Theme.ACCENT).grid(row=row_counter, column=0, sticky="w", pady=(10, 5))
            row_counter += 1
            
            key_grid = ctk.CTkFrame(parent, fg_color="transparent")
            key_grid.grid(row=row_counter, column=0, sticky="ew")
            row_counter += 1
            
            for i, key_name in enumerate(keys):
                frame = ctk.CTkFrame(key_grid, fg_color="transparent")
                frame.grid(row=i//cols, column=i%cols, padx=10, pady=2, sticky="w")
                key_grid.grid_columnconfigure(i%cols, weight=1)

                status_label = ctk.CTkLabel(frame, text="✖", text_color=Theme.ERROR, font=("Segoe UI", 16, "bold"))
                status_label.pack(side="left")
                
                key_label_text = key_name.replace("numpad ", "Numpad ").title()
                key_label = ctk.CTkLabel(frame, text=key_label_text, font=Theme.SMALL_FONT)
                key_label.pack(side="left", padx=(5, 0))
                
                self.key_labels[key_name.lower()] = status_label

    def draw_on_canvas(self, event): 
        self.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, fill=Theme.ACCENT, outline=Theme.ACCENT)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.result_container, text="Bàn phím và Touchpad có hoạt động tốt không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, tất cả đều tốt", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Hoạt động tốt", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có lỗi", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có lỗi", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

    def on_key_event(self, event):
        if self.winfo_exists() and event.event_type == 'down':
             self.after(0, self._update_key_ui, event.name)

    def _update_key_ui(self, key_name_raw):
        key_name = key_name_raw.lower()
        key_map = { 'left shift': 'shift', 'left ctrl': 'ctrl', 'left alt': 'alt', 'left windows': 'windows', 'alt gr': 'right alt', 'caps lock': 'caps lock', 'page up': 'page up', 'page down': 'page down', 'print screen': 'print screen', 'delete': 'delete', 'insert': 'insert', 'home': 'home', 'end': 'end', 'num lock': 'num lock' }
        mapped_key = key_map.get(key_name, key_name)

        if mapped_key in self.key_labels:
            self.key_labels[mapped_key].configure(text="✔", text_color=Theme.SUCCESS)

    def start_listening(self):
        if not self.is_listening:
            try:
                keyboard.hook(self.on_key_event, suppress=False)
                self.is_listening = True
            except Exception as e:
                print(f"Lỗi: Không thể hook bàn phím: {e}")
                if "root" in str(e).lower():
                    messagebox.showwarning("Yêu cầu quyền Admin", "Không thể bắt sự kiện bàn phím do thiếu quyền Admin/root. Vui lòng chạy lại ứng dụng với quyền quản trị viên để test bàn phím.")

    def stop_listening(self):
        if self.is_listening:
            try: keyboard.unhook_all()
            except Exception as e: print(f"Lỗi khi unhook bàn phím: {e}")
            self.is_listening = False

    def stop_tasks(self):
        super().stop_tasks()
        self.stop_listening()

class PortsConnectivityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cổng & Kết nối", "Các cổng kết nối, Wi-Fi, Bluetooth là những thành phần thiết yếu. Một cổng hỏng sẽ gây nhiều phiền toái.", "**Tự động:** Trạng thái Wi-Fi và Ping được cập nhật bên dưới.\n**Thủ công:** Lần lượt cắm thiết bị vào các cổng (LAN, USB, HDMI, Audio, Thẻ SD) và đánh dấu vào checkbox tương ứng để xác nhận.\n**Nâng cao:** Nhấn 'Quét Mạng Wi-Fi' để kiểm tra khả năng thu sóng của card mạng.", **kwargs)
        self.action_frame.grid_columnconfigure(1, weight=1); self.action_frame.grid_rowconfigure(0, weight=1); self.update_timer_id = None
        
        left_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent"); left_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        status_container = ctk.CTkFrame(left_frame, fg_color=Theme.FRAME); status_container.pack(fill="both", expand=True, pady=5)
        ctk.CTkLabel(status_container, text="Trạng Thái Mạng", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(15, 10), anchor="w", padx=20)
        self.wifi_status_label = ctk.CTkLabel(status_container, text="Wi-Fi: Đang kiểm tra...", font=Theme.BODY_FONT); self.wifi_status_label.pack(pady=(0, 10), padx=20, anchor="w")
        self.ping_status_label = ctk.CTkLabel(status_container, text="Ping Internet: Đang kiểm tra...", font=Theme.BODY_FONT); self.ping_status_label.pack(pady=(0, 5), padx=20, anchor="w")
        self.gateway_ping_label = ctk.CTkLabel(status_container, text="Ping Gateway: Đang kiểm tra...", font=Theme.BODY_FONT); self.gateway_ping_label.pack(pady=(0, 20), padx=20, anchor="w")
        
        button_container = ctk.CTkFrame(left_frame, fg_color="transparent"); button_container.pack(fill="x", pady=5); button_container.grid_columnconfigure((0,1), weight=1)
        ctk.CTkButton(button_container, text="Mở Cài đặt Bluetooth", command=self.open_bluetooth_settings, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).grid(row=0, column=0, sticky="ew", padx=(0,5))
        if platform.system() == "Windows": ctk.CTkButton(button_container, text="Quét Mạng Wi-Fi", image=self.icon_manager.WIFI, command=self.scan_wifi_networks, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT).grid(row=0, column=1, sticky="ew", padx=(5,0))
        
        right_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME); right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        ctk.CTkLabel(right_frame, text="Checklist Cổng Kết Nối", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(15, 10), anchor="w", padx=20)
        self.port_vars = {}
        ports = ["Cổng LAN", "Tất cả cổng USB", "Cổng HDMI/DisplayPort", "Jack Audio 3.5mm", "Khe đọc thẻ SD"]
        for port in ports:
            var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(right_frame, text=port, variable=var, onvalue="on", offvalue="off", font=Theme.BODY_FONT, command=self.check_completion)
            cb.pack(anchor="w", padx=20, pady=12); self.port_vars[port] = {"var": var, "cb": cb}
        self.update_info()

    def on_show(self): self.update_info()

    def update_info(self):
        self.check_wifi_lan()
        threading.Thread(target=self.check_ping, args=("google.com", self.ping_status_label, "Internet"), daemon=True).start()
        threading.Thread(target=self.check_gateway_ping, daemon=True).start()
        if self.winfo_exists(): self.update_timer_id = self.after(10000, self.update_info)

    def check_ping(self, host, label, name):
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', host]
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            output = subprocess.check_output(command, startupinfo=startupinfo, universal_newlines=True, timeout=5, stderr=subprocess.DEVNULL)
            match = re.search(r'time[=<]([\d\.]+)\s*ms', output)
            if match:
                ping_time = float(match.group(1)); color = Theme.SUCCESS if ping_time < 100 else Theme.WARNING
                if self.winfo_exists(): self.after(0, label.configure, {"text": f"Ping {name}: {ping_time:.0f}ms", "text_color": color})
            else: raise ValueError("Không phân tích được ping")
        except subprocess.TimeoutExpired:
            if self.winfo_exists(): self.after(0, label.configure, {"text": f"Ping {name}: Timeout", "text_color": Theme.ERROR})
        except Exception: 
            if self.winfo_exists(): self.after(0, label.configure, {"text": f"Ping {name}: Lỗi", "text_color": Theme.ERROR})

    def get_default_gateway(self):
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output("ipconfig", text=True, stderr=subprocess.DEVNULL)
                match = re.search(r"Default Gateway . . . . . . . . . . : ([\d\.]+)", output)
                return match.group(1) if match else None
            else:
                output = subprocess.check_output("ip route | grep default", shell=True, text=True, stderr=subprocess.DEVNULL)
                return output.split()[2]
        except: return None

    def check_gateway_ping(self):
        gateway = self.get_default_gateway()
        if gateway: self.check_ping(gateway, self.gateway_ping_label, "Gateway")
        else: self.after(0, self.gateway_ping_label.configure, {"text": "Ping Gateway: Không tìm thấy", "text_color": Theme.WARNING})

    def scan_wifi_networks(self):
        scan_window = ctk.CTkToplevel(self); scan_window.title("Kết quả quét Wi-Fi"); scan_window.geometry("600x700"); scan_window.attributes("-topmost", True)
        ctk.CTkLabel(scan_window, text="Quét Wi-Fi giúp kiểm tra độ nhạy của card mạng.\nCard tốt sẽ thấy nhiều mạng, kể cả mạng yếu.", font=Theme.BODY_FONT, justify="left").pack(pady=10, padx=20, anchor="w")
        ctk.CTkLabel(scan_window, text="Cường độ tín hiệu (dBm): Gần 0 là tốt nhất.\n-30 đến -60: Tốt | -70 đến -80: Trung bình | Dưới -80: Yếu", font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, justify="left").pack(pady=(0,10), padx=20, anchor="w")
        status_label = ctk.CTkLabel(scan_window, text="Đang quét, vui lòng đợi...", font=Theme.BODY_FONT); status_label.pack(pady=20)
        results_frame = ctk.CTkScrollableFrame(scan_window, label_text="Các mạng tìm thấy", label_font=Theme.BODY_FONT)
        def do_scan():
            try:
                wifi = pywifi.PyWiFi(); ifaces = wifi.interfaces()
                if not ifaces: status_label.configure(text="Lỗi: Không tìm thấy card Wi-Fi.", text_color=Theme.ERROR); return
                iface = ifaces[0]; iface.scan(); time.sleep(5); scan_results = iface.scan_results()
                status_label.pack_forget(); results_frame.pack(expand=True, fill="both", padx=10, pady=10)
                if not scan_results: ctk.CTkLabel(results_frame, text="Không tìm thấy mạng Wi-Fi nào.").pack(); return
                sorted_results = sorted(scan_results, key=lambda x: x.signal, reverse=True)
                for res in sorted_results:
                    net_frame = ctk.CTkFrame(results_frame, fg_color=Theme.FRAME); net_frame.pack(fill="x", pady=4, padx=4)
                    ctk.CTkLabel(net_frame, text=res.ssid, font=Theme.BODY_FONT).pack(anchor="w", side="left", padx=10)
                    ctk.CTkLabel(net_frame, text=f"{res.signal} dBm", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="e", side="right", padx=10)
            except Exception as e: status_label.configure(text=f"Lỗi khi quét Wi-Fi:\n{e}", text_color=Theme.ERROR)
        threading.Thread(target=do_scan, daemon=True).start()
        
    def check_wifi_lan(self):
        try:
            interfaces = psutil.net_if_addrs(); stats = psutil.net_if_stats(); lan_found = False
            for name, addrs in interfaces.items():
                if ("ethernet" in name.lower() or "lan" in name.lower()) and any(addr.family == socket.AF_INET for addr in addrs):
                    if name in stats and stats[name].isup:
                        self.port_vars["Cổng LAN"]["var"].set("on"); self.port_vars["Cổng LAN"]["cb"].select()
                        self.port_vars["Cổng LAN"]["cb"].configure(state="disabled", text="Cổng LAN (Đã kết nối ✔)"); lan_found = True; break
            if not lan_found and self.port_vars["Cổng LAN"]["cb"].cget("state") == "disabled":
                self.port_vars["Cổng LAN"]["cb"].configure(state="normal", text="Cổng LAN"); self.port_vars["Cổng LAN"]["cb"].deselect()
            wifi_status, wifi_color = "Không tìm thấy card Wi-Fi", Theme.ERROR
            for name, stat_data in stats.items():
                if "wi-fi" in name.lower() or "wlan" in name.lower():
                    wifi_status = "Hoạt động tốt" if stat_data.isup else "Đã tắt hoặc lỗi Driver"
                    wifi_color = Theme.SUCCESS if stat_data.isup else Theme.WARNING; break
            self.wifi_status_label.configure(text=f"Wi-Fi: {wifi_status}", text_color=wifi_color)
        except Exception as e: print(f"Lỗi khi kiểm tra kết nối mạng: {e}")
        self.check_completion()
        
    def open_bluetooth_settings(self):
        if platform.system() == "Windows": subprocess.run("start ms-settings:bluetooth", shell=True, check=False)
        
    def check_completion(self):
        if all(var["var"].get() == "on" for var in self.port_vars.values()):
            details = f"Wi-Fi: {self.wifi_status_label.cget('text')}\n{self.ping_status_label.cget('text')}\nCác cổng kết nối đã được kiểm tra thủ công."
            self.mark_completed({"Kết quả": "Hoạt động tốt", "Trạng thái": "Tốt", "Chi tiết": details}, auto_advance=False)
            
    def stop_tasks(self):
        super().stop_tasks()
        if self.update_timer_id: self.after_cancel(self.update_timer_id); self.update_timer_id = None

class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Sức khỏe & Độ chai Pin", "Pin laptop sẽ bị chai theo thời gian. Báo cáo này cho thấy sự khác biệt giữa dung lượng thiết kế ban đầu và dung lượng sạc đầy hiện tại, từ đó biết chính xác độ chai pin.", "Nhấn nút 'Phân Tích Pin' để ứng dụng tự động tạo, đọc và phân tích tình trạng pin cho bạn.", **kwargs)
        self.report_path = os.path.join(tempfile.gettempdir(), "battery-report.html")
        self.action_frame.grid_rowconfigure(2, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)

        self.report_button = ctk.CTkButton(self.action_frame, text="Phân Tích Pin", command=self.run_battery_analysis, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.status_label = ctk.CTkLabel(self.action_frame, text="", font=Theme.BODY_FONT)
        
        if platform.system() == "Windows":
            self.report_button.grid(row=0, column=0, pady=(20,10), padx=20, sticky="ew")
            self.status_label.grid(row=1, column=0, pady=5, padx=20)
        else:
            ctk.CTkLabel(self.action_frame, text="Tính năng này chỉ hỗ trợ trên Windows.", font=Theme.SUBHEADING_FONT).grid(row=0, column=0, pady=20, padx=20)
            self.mark_completed({"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"})

        self.results_display_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_display_frame.grid(row=2, column=0, sticky="n", pady=15, padx=20)
        self.results_display_frame.grid_columnconfigure(1, weight=1)

    def run_battery_analysis(self):
        self.report_button.configure(state="disabled", text="Đang phân tích...")
        self.status_label.configure(text="")
        for w in self.results_display_frame.winfo_children(): w.destroy()
        threading.Thread(target=self._analysis_thread, daemon=True).start()

    def _analysis_thread(self):
        try:
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run( f"powercfg /batteryreport /output \"{self.report_path}\" /duration 0", check=True, shell=False, capture_output=True, text=False, startupinfo=startupinfo)
            with open(self.report_path, 'r', encoding='utf-8', errors='ignore') as f: soup = BeautifulSoup(f, 'html.parser')

            def get_info(key_text, is_capacity=True):
                try:
                    key_tag = soup.find(lambda tag: tag.name == 'td' and key_text in tag.text)
                    value_tag = key_tag.find_next_sibling('td')
                    if is_capacity: return int(re.search(r'[\d,]+', value_tag.text).group().replace(',', ''))
                    return value_tag.text.strip()
                except (AttributeError, ValueError): return None

            design_cap = get_info('DESIGN CAPACITY'); full_charge_cap = get_info('FULL CHARGE CAPACITY')
            cycle_count = get_info('CYCLE COUNT', is_capacity=False); chemistry = get_info('CHEMISTRY', is_capacity=False)
            manufacturer = get_info('MANUFACTURER', is_capacity=False)
            if design_cap is None or full_charge_cap is None or design_cap == 0: raise ValueError("Không thể tìm thấy thông tin dung lượng trong báo cáo.")
            health_percent = (full_charge_cap / design_cap) * 100
            details = [ f"Dung lượng thiết kế: {design_cap:,} mWh", f"Dung lượng sạc đầy: {full_charge_cap:,} mWh", f"Sức khỏe còn lại: {health_percent:.2f}%", f"Số chu kỳ sạc: {cycle_count or 'Không rõ'}", f"Loại pin: {chemistry or 'Không rõ'}", f"Nhà sản xuất: {manufacturer or 'Không rõ'}" ]
            is_ok = health_percent >= 80
            final_result = { "Kết quả": f"Pin còn tốt ({health_percent:.2f}%)" if is_ok else f"Pin đã chai ({health_percent:.2f}%)", "Trạng thái": "Tốt" if is_ok else "Lỗi", "Chi tiết": "\n".join(details) }
            if self.winfo_exists(): self.after(0, self.update_ui, details, health_percent, final_result, None)
        except (subprocess.CalledProcessError, FileNotFoundError):
            error_msg = "Lỗi: Không thể tạo báo cáo pin. Hãy thử chạy ứng dụng với quyền Admin."
            if self.winfo_exists(): self.after(0, self.update_ui, None, None, None, error_msg)
        except Exception as e:
            error_msg = f"Lỗi khi phân tích báo cáo: {e}"
            if self.winfo_exists(): self.after(0, self.update_ui, None, None, None, error_msg)

    def update_ui(self, details_list, health, result_data, error_msg):
        self.report_button.configure(state="normal", text="Phân Tích Lại")
        if error_msg:
            self.status_label.configure(text=error_msg, text_color=Theme.ERROR)
            self.mark_completed({"Kết quả": "Lỗi phân tích", "Trạng thái": "Lỗi", "Chi tiết": error_msg}); return
        for widget in self.results_display_frame.winfo_children(): widget.destroy()
        for i, detail_text in enumerate(details_list):
            key, value = detail_text.split(":", 1)
            is_health_row = "Sức khỏe còn lại" in key
            key_label = ctk.CTkLabel(self.results_display_frame, text=f"{key}:", font=Theme.SUBHEADING_FONT if is_health_row else Theme.BODY_FONT, text_color=Theme.TEXT if is_health_row else Theme.TEXT_SECONDARY)
            key_label.grid(row=i, column=0, sticky="w", pady=6)
            value_label = ctk.CTkLabel(self.results_display_frame, text=value.strip(), font=Theme.SUBHEADING_FONT if is_health_row else Theme.BODY_FONT)
            value_label.grid(row=i, column=1, sticky="w", pady=6, padx=(15, 0))
            if is_health_row: value_label.configure(text_color=Theme.SUCCESS if health >= 80 else Theme.ERROR)
        self.mark_completed(result_data, auto_advance=False)

class SpeakerTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Loa", "Loa rè, vỡ tiếng hoặc chỉ hoạt động một bên sẽ ảnh hưởng lớn đến trải nghiệm. Kiểm tra ở âm lượng cao là rất quan trọng.", "1. **Chỉnh âm lượng của Windows lên mức cao nhất.**\n2. Nhấn 'Phát Âm Thanh' bên dưới.\n3. Lắng nghe cẩn thận để kiểm tra kênh trái/phải và xem loa có bị rè, vỡ tiếng ở âm lượng cao không.", **kwargs)
        self.results_shown = False
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        
        center_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent"); center_frame.grid(row=0, column=0, padx=20, pady=20)
        
        button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); button_bar.pack(anchor="w", pady=10)
        self.play_button = ctk.CTkButton(button_bar, text="Phát Âm Thanh", command=self.play_sound, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        self.play_button.pack(side="left", padx=(0, 10))
        self.stop_button = ctk.CTkButton(button_bar, text="Dừng Âm Thanh", command=self.stop_sound, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, state="disabled")
        self.stop_button.pack(side="left")
        self.status_label = ctk.CTkLabel(center_frame, text="", font=Theme.BODY_FONT)
        self.status_label.pack(anchor="w", pady=10)
        self.audio_file = asset_path("stereo_test.mp3")
        
        self.init_mixer()
        
        if not os.path.exists(self.audio_file):
            self.play_button.configure(state="disabled")
            self.status_label.configure(text=f"Lỗi: Không tìm thấy file âm thanh tại {self.audio_file}", text_color=Theme.WARNING)

        self.result_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_frame.grid(row=1, column=0, sticky="s", pady=(0, 20)); self.result_frame.grid_remove()

    def init_mixer(self):
        try:
            pygame.mixer.quit()
            pygame.mixer.init()
        except Exception as e:
            self.play_button.configure(state="disabled")
            self.status_label.configure(text=f"Lỗi khởi tạo âm thanh: {e}", text_color=Theme.ERROR)
            self.mark_completed({"Kết quả": f"Lỗi khởi tạo âm thanh", "Trạng thái": "Lỗi", "Chi tiết": str(e)}, auto_advance=False)

    def play_sound(self):
        if not pygame.mixer.get_init():
            self.init_mixer()
            if not pygame.mixer.get_init(): return
                
        self.play_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Đang phát...", text_color=Theme.ACCENT)
        threading.Thread(target=self._play_logic, daemon=True).start()

    def stop_sound(self):
        if pygame.mixer.get_init(): pygame.mixer.music.stop()
        self.status_label.configure(text="Đã dừng.", text_color=Theme.TEXT_SECONDARY)
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.show_result_choices()

    def _play_logic(self):
        try:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            if self.winfo_exists(): self.after(0, self.on_play_finish)
        except Exception as e:
            if self.winfo_exists(): self.after(0, self.on_play_error, str(e))

    def on_play_finish(self):
        if not self.winfo_exists(): return
        self.status_label.configure(text="Đã phát xong.", text_color=Theme.SUCCESS)
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.show_result_choices()

    def on_play_error(self, error_msg):
        if not self.winfo_exists(): return
        self.status_label.configure(text=f"Lỗi: {error_msg}", text_color=Theme.ERROR)
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.show_result_choices()

    def show_result_choices(self):
        if self.results_shown: return
        self.results_shown = True
        self.result_frame.grid()
        ctk.CTkLabel(self.result_frame, text="Loa có hoạt động tốt, âm thanh trong và phát đúng kênh không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, loa bình thường", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Bình thường", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, loa có vấn đề", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề (rè/mất tiếng)", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class MicrophoneTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Microphone", "Micro tốt là điều kiện bắt buộc cho họp và học online. Cần đảm bảo mic thu âm rõ ràng, không bị rè.", "1. Nhấn 'Bắt đầu ghi âm' và nói vài câu. Theo dõi cột sóng âm bên dưới.\n2. Sau 5 giây, nhấn 'Phát lại' để nghe lại.\n3. Dựa vào chất lượng nghe lại để đánh giá.", **kwargs)
        self.recording_data = []
        self.stream = None
        self.is_recording = False
        self.fs = 44100
        self.duration = 5
        self.temp_file_obj = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self.temp_file = self.temp_file_obj.name
        
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        center_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent"); center_frame.grid(row=0, column=0, padx=20, pady=20)
        
        button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); button_bar.pack(anchor="w", pady=10)
        self.record_button = ctk.CTkButton(button_bar, text="Bắt đầu ghi âm", command=self.start_recording, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        self.record_button.pack(side="left", padx=(0, 10))
        self.play_button = ctk.CTkButton(button_bar, text="Phát lại", command=self.play_recording, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, state="disabled")
        self.play_button.pack(side="left")
        
        self.status_label = ctk.CTkLabel(center_frame, text="", font=Theme.BODY_FONT); self.status_label.pack(anchor="w", pady=(10, 5))

        self.volume_meter = ctk.CTkProgressBar(center_frame, progress_color=Theme.SUCCESS); self.volume_meter.set(0); self.volume_meter.pack(fill="x", anchor="w", pady=5)
        
        self.result_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_frame.grid(row=1, column=0, sticky="s", pady=(0,20)); self.result_frame.grid_remove()

    def __del__(self):
        self.cleanup_temp_file()

    def cleanup_temp_file(self):
        try:
            if self.temp_file_obj: self.temp_file_obj.close()
            if self.temp_file and os.path.exists(self.temp_file):
                os.unlink(self.temp_file); self.temp_file = None
        except Exception as e: print(f"Lỗi khi dọn dẹp file mic tạm: {e}")

    def _audio_callback(self, indata, frames, time, status):
        if status: print(status)
        self.recording_data.append(indata.copy())
        if self.is_recording and self.winfo_exists():
            volume_norm = np.linalg.norm(indata) * 10
            self.after(0, self.volume_meter.set, min(1.0, volume_norm))

    def start_recording(self):
        self.record_button.configure(state="disabled"); self.play_button.configure(state="disabled")
        self.status_label.configure(text=f"Đang ghi âm trong {self.duration} giây...", text_color=Theme.ACCENT)
        self.recording_data = []
        
        try:
            self.is_recording = True
            self.stream = sd.InputStream(callback=self._audio_callback, samplerate=self.fs, channels=1, dtype='float32')
            self.stream.start()
            self.after(self.duration * 1000, self.stop_recording)
        except Exception as e: self.on_record_error(str(e))

    def stop_recording(self):
        if not self.is_recording: return
        self.is_recording = False
        if self.stream: self.stream.stop(); self.stream.close(); self.stream = None
        self.volume_meter.set(0)
        if not self.recording_data: self.on_record_error("Không thu được dữ liệu âm thanh."); return

        try:
            recording_np = np.concatenate(self.recording_data, axis=0)
            write_wav(self.temp_file, self.fs, (recording_np * 32767).astype(np.int16))
            self.on_record_finish()
        except Exception as e: self.on_record_error(f"Lỗi khi lưu file: {e}")

    def on_record_finish(self):
        if not self.winfo_exists(): return
        self.status_label.configure(text="Đã ghi xong. Nhấn 'Phát lại' để nghe.", text_color=Theme.SUCCESS)
        self.record_button.configure(state="normal"); self.play_button.configure(state="normal")
        self.show_result_choices()

    def on_record_error(self, error_msg):
        if not self.winfo_exists(): return
        self.status_label.configure(text=f"Lỗi ghi âm: {error_msg}. Hãy chắc chắn micro được kết nối.", text_color=Theme.ERROR)
        self.record_button.configure(state="normal"); self.is_recording = False
        self.show_result_choices()

    def play_recording(self):
        try:
            samplerate, data = read_wav(self.temp_file); sd.play(data, samplerate); sd.wait()
        except Exception as e: messagebox.showerror("Lỗi Phát Lại", f"Không thể phát lại file ghi âm: {e}")

    def show_result_choices(self):
        for widget in self.result_frame.winfo_children(): widget.destroy()
        self.result_frame.grid()
        ctk.CTkLabel(self.result_frame, text="Âm thanh thu từ micro có rõ ràng và không bị rè không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_frame, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, micro tốt", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Thu âm tốt", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, micro bị rè/nhỏ", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Rè hoặc nhỏ", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

    def stop_tasks(self):
        super().stop_tasks()
        if self.is_recording: self.stop_recording()
        self.cleanup_temp_file()

class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Webcam", "Webcam là công cụ không thể thiếu cho việc học và làm việc từ xa. Webcam mờ, nhiễu hoặc không hoạt động là một trở ngại lớn.", "1. Nhấn 'Bắt đầu Test'.\n2. Hình ảnh từ webcam sẽ hiện ra.\n3. Kiểm tra xem hình ảnh có rõ nét, màu sắc trung thực và không bị giật, lag không.", **kwargs)
        self.running = False; self.cap = None
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent"); center_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        center_frame.grid_rowconfigure(0, weight=1); center_frame.grid_columnconfigure(0, weight=1)

        self.webcam_container = ctk.CTkFrame(center_frame, fg_color="black", corner_radius=Theme.CORNER_RADIUS); self.webcam_container.grid(row=0, column=0, pady=(0, 15), sticky="nsew")
        self.webcam_label = ctk.CTkLabel(self.webcam_container, text="Hình ảnh webcam sẽ hiển thị ở đây", font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT_SECONDARY); self.webcam_label.pack(padx=10, pady=10, expand=True)
        self.status_label = ctk.CTkLabel(center_frame, text="", font=Theme.SMALL_FONT); self.status_label.grid(row=1, column=0, pady=5)
        
        button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); button_bar.grid(row=2, column=0, pady=10)
        self.start_button = ctk.CTkButton(button_bar, text="Bắt đầu Test", command=self.start_webcam, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER); self.start_button.pack(side="left", padx=10)
        self.stop_button = ctk.CTkButton(button_bar, text="Dừng Test", command=self.stop_webcam, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, state="disabled"); self.stop_button.pack(side="left", padx=10)
        
        self.result_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        self.result_frame.grid(row=3, column=0, sticky="s", pady=(20,0)); self.result_frame.grid_remove()

    def start_webcam(self):
        if not self.running:
            self.running = True; self.start_button.configure(state="disabled"); self.stop_button.configure(state="normal")
            self.result_frame.grid_remove()
            if hasattr(self, 'btn_yes'): self.btn_yes.configure(state="normal", fg_color=Theme.SUCCESS)
            if hasattr(self, 'btn_no'): self.btn_no.configure(state="normal", fg_color=Theme.ERROR)
            self.status_label.configure(text="Đang mở camera...", text_color=Theme.ACCENT)
            threading.Thread(target=self.update_webcam_feed, daemon=True).start()

    def stop_webcam(self):
        self.running = False; self.stop_button.configure(state="disabled")

    def stop_tasks(self):
        super().stop_tasks(); self.running = False; time.sleep(0.1) 
        if self.cap and self.cap.isOpened():
            try: self.cap.release()
            except Exception: pass
        self.cap = None

    def update_webcam_feed(self):
        try:
            if self.cap: self.cap.release()
            backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY
            self.cap = cv2.VideoCapture(0, backend)
            if not self.cap or not self.cap.isOpened(): raise ConnectionError("Không tìm thấy webcam hoặc không thể truy cập.")
            source_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)); source_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if self.winfo_exists(): self.after(0, self.status_label.configure, {"text": f"Độ phân giải thực: {source_w}x{source_h}", "text_color": Theme.TEXT_SECONDARY})
            
            while self.running:
                ret, frame = self.cap.read()
                if not ret or not self.winfo_exists(): break
                self.after(0, self.update_image, frame); time.sleep(1/30)
                
        except (IOError, ConnectionError, Exception) as e:
            if self.winfo_exists(): self.after(0, self.on_test_error, str(e))
        finally:
            if self.cap: self.cap.release(); self.cap = None
            self.running = False
            if self.winfo_exists(): self.after(0, self.on_test_finish)
            
    def update_image(self, frame):
        if not self.running or not self.winfo_exists(): return
        
        container_h = self.webcam_container.winfo_height() - 20; container_w = self.webcam_container.winfo_width() - 20
        if container_h <= 0 or container_w <= 0: return

        source_h, source_w, _ = frame.shape
        aspect_ratio = source_w / source_h if source_h > 0 else 1.77
        new_w, new_h = container_w, int(container_w / aspect_ratio)
        if new_h > container_h: new_h, new_w = container_h, int(container_h * aspect_ratio)
        new_w, new_h = max(1, int(new_w)), max(1, int(new_h))

        if new_w > 0 and new_h > 0:
            resized_frame = cv2.resize(frame, (new_w, new_h))
            img = Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
            self.webcam_label.configure(image=ctk_img, text="")

    def on_test_error(self, message):
        self.status_label.configure(text=message, text_color=Theme.ERROR); self.result_frame.grid_remove() 
        self.mark_completed({"Kết quả": "Không thể mở camera", "Trạng thái": "Lỗi", "Chi tiết": message})
        self.start_button.configure(state="normal")

    def on_test_finish(self):
        self.webcam_label.configure(image=None, text="Hình ảnh webcam sẽ hiển thị ở đây"); self.stop_button.configure(state="disabled")
        self.status_label.configure(text="")
        
        if not self._completed:
            self.start_button.configure(state="disabled")
            self.result_frame.grid()
            ctk.CTkLabel(self.result_frame, text="Hình ảnh từ webcam có rõ nét và ổn định không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
            button_bar = ctk.CTkFrame(self.result_frame, fg_color="transparent"); button_bar.pack(pady=15)

            def custom_handle_result(is_ok, ok_data, bad_data):
                self.handle_result_generic(is_ok, ok_data, bad_data); self.start_button.configure(state="normal")

            self.btn_yes = ctk.CTkButton(button_bar, text="Có, webcam tốt", image=self.icon_manager.CHECK, compound="left", command=lambda: custom_handle_result(True, {"Kết quả": "Hoạt động tốt", "Trạng thái": "Tốt", "Chi tiết": self.status_label.cget("text")}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
            self.btn_yes.pack(side="left", padx=10)
            self.btn_no = ctk.CTkButton(button_bar, text="Không, webcam mờ/lỗi", image=self.icon_manager.CROSS, compound="left", command=lambda: custom_handle_result(False, {}, {"Kết quả": "Mờ hoặc lỗi", "Trạng thái": "Lỗi", "Chi tiết": self.status_label.cget("text")}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
            self.btn_no.pack(side="left", padx=10)
        else: self.start_button.configure(state="normal")

# --- LỚP CHA CHO CÁC BÀI STRESS TEST ---
class BaseStressTestStep(BaseStepFrame):
    def __init__(self, master, title, why_text, how_text, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results):
        super().__init__(master, title, why_text, how_text, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results)
        
        self.test_process = None
        self.queue = multiprocessing.Queue()
        self.is_testing = False
        
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(2, weight=1)

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
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)

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
        try:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                self.handle_message(msg)
        except Exception as e:
            print(f"Lỗi đọc queue: {e}")
        finally:
            if self.is_testing:
                self.after(100, self.check_queue)

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
        while not self.queue.empty():
            try: self.queue.get_nowait()
            except: break
        self.queue.close()


class HardDriveSpeedStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tốc Độ Ổ Cứng (Thực tế)", "Tốc độ đọc/ghi thực tế ảnh hưởng trực tiếp đến tốc độ khởi động, mở ứng dụng và sao chép file.", "Ứng dụng sẽ tạo một file tạm 256MB, ghi dữ liệu ngẫu nhiên vào đó, sau đó đọc lại để đo tốc độ tuần tự. Kết quả sẽ phản ánh hiệu năng của SSD/HDD.", **kwargs)
        self.start_button.configure(image=self.icon_manager.HDD, compound="left")

    def start_test(self):
        self.run_worker(run_disk_benchmark, (self.queue, 256))

    def update_ui(self, data):
        operation = data.get('operation', '')
        if operation:
            self.status_label.configure(text=f"Đang thực hiện: {operation}...")

    def finalize_test(self, msg):
        data = msg.get('data', {})
        write_speed = data.get('write_speed', 'N/A')
        read_speed = data.get('read_speed', 'N/A')

        result_text = f"Tốc độ Ghi: {write_speed} MB/s\nTốc độ Đọc: {read_speed} MB/s"
        ctk.CTkLabel(self.results_frame, text=result_text, font=Theme.SUBHEADING_FONT, justify="left").pack(anchor="w")
        
        details = f"Tốc độ ghi tuần tự: {write_speed} MB/s\nTốc độ đọc tuần tự: {read_speed} MB/s"
        try:
            is_ok = float(write_speed) > 150 and float(read_speed) > 150
        except (ValueError, TypeError):
            is_ok = False
        
        result_data = {
            "Kết quả": f"Ghi: {write_speed} MB/s, Đọc: {read_speed} MB/s",
            "Trạng thái": "Tốt" if is_ok else "Lỗi",
            "Chi tiết": details
        }
        self.mark_completed(result_data)


class CPUStressTestStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra CPU & Tản Nhiệt", "Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt của máy.", "Nhấn 'Bắt đầu Test' trong 2-5 phút. Theo dõi biểu đồ nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt.", **kwargs)
        
        self.TEST_DURATION = 120
        self.start_button.configure(image=self.icon_manager.CPU, compound="left")
        
        self.chart_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, border_width=1, border_color=Theme.BORDER)
        self.chart_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        self.chart_frame.grid_remove()
        
        self.canvas = ctk.CTkCanvas(self.chart_frame, bg=Theme.FRAME, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.temp_data = deque(maxlen=self.TEST_DURATION)
        self.usage_data = deque(maxlen=self.TEST_DURATION)
        self.max_temp = 0

    def start_test(self):
        self.temp_data.clear(); self.usage_data.clear(); self.max_temp = 0
        self.chart_frame.grid()
        self.run_worker(run_cpu_stress, (self.TEST_DURATION, self.queue))

    def update_ui(self, data):
        temp = data.get('temp')
        usage = data.get('usage')
        
        if temp is not None:
            self.temp_data.append(temp)
            if temp > self.max_temp: self.max_temp = temp
        else:
            self.temp_data.append(0)

        if usage is not None:
            self.usage_data.append(usage)

        self.status_label.configure(text=f"Usage: {usage or 'N/A'}% | Temp: {temp or 'N/A'}°C | Max Temp: {self.max_temp}°C")
        self.draw_chart()

    def draw_chart(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 10 or h < 10: return

        for i in range(1, 5):
            y = h * i / 5
            self.canvas.create_line(0, y, w, y, fill=Theme.SEPARATOR)
            self.canvas.create_text(15, y, text=f"{100 - i*20}%", anchor="w", fill=Theme.TEXT_SECONDARY)
        self.canvas.create_text(w-30, h-10, text="Thời gian", anchor="e", fill=Theme.TEXT_SECONDARY)

        def get_points(data, max_val):
            points = []
            if not data: return points
            step = w / (self.TEST_DURATION - 1) if self.TEST_DURATION > 1 else w
            for i, val in enumerate(data):
                x = i * step
                y = h - (val / max_val * h) if val is not None and max_val > 0 else h
                points.extend([x, y])
            return points

        if len(self.usage_data) > 1:
            self.canvas.create_line(get_points(self.usage_data, 100), fill=Theme.ACCENT, width=2, tags="usage_line")
        if len(self.temp_data) > 1:
            self.canvas.create_line(get_points(self.temp_data, 110), fill=Theme.ERROR, width=2, tags="temp_line")

    def finalize_test(self, msg):
        details = f"Thời gian test: {self.TEST_DURATION} giây.\nNhiệt độ tối đa ghi nhận: {self.max_temp}°C."
        is_ok = self.max_temp > 0 and self.max_temp < 98
        
        result_data = {
            "Kết quả": f"Nhiệt độ tối đa: {self.max_temp}°C",
            "Trạng thái": "Tốt" if is_ok else "Lỗi",
            "Chi tiết": details
        }
        self.mark_completed(result_data)
        self.status_label.configure(text=f"Test hoàn thành. Nhiệt độ tối đa: {self.max_temp}°C")


class GPUStressTestStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra GPU & Tản nhiệt", "GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng.", "Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 90 giây. Hãy quan sát:\n  • Có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?\n  • Máy có bị treo hoặc tự khởi động lại không?\n  • **Khuyến nghị:** Dùng phần mềm như HWMonitor để theo dõi nhiệt độ GPU song song.", **kwargs)
        self.TEST_DURATION = 90
        self.start_button.configure(image=self.icon_manager.GPU, compound="left")

    def start_test(self):
        self.run_worker(run_gpu_stress, (self.TEST_DURATION, self.queue))

    def finalize_test(self, msg):
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.results_frame.winfo_children(): widget.destroy()
        
        ctk.CTkLabel(self.results_frame, text="Trong quá trình test, GPU có hoạt động ổn định không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.results_frame, fg_color="transparent"); button_bar.pack(pady=15)
        
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, hoạt động ổn định", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Ổn định, không lỗi hình", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có lỗi (treo, rác hình)", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Không ổn định, có lỗi hình", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class WarrantyCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Thông Tin Bảo Hành", "Biết được tình trạng bảo hành của máy giúp bạn yên tâm hơn. Bảo hành hãng và bảo hành cửa hàng có chất lượng rất khác nhau.", "1. Số Serial của máy đã được đọc tự động bên dưới.\n2. Nhấn vào nút tương ứng với hãng sản xuất để mở trang kiểm tra bảo hành.", **kwargs)
        
        self.action_frame.grid_rowconfigure(2, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        
        serial = "Không tìm thấy"
        try:
            details_text = self.all_results.get("Định Danh Phần Cứng", {}).get("Chi tiết", "")
            for line in details_text.splitlines():
                if "serial number:" in line.lower(): serial = line.split(":")[-1].strip(); break
        except Exception as e: print(f"Lỗi khi trích xuất serial: {e}")
            
        ctk.CTkLabel(self.action_frame, text="Serial Number:", font=Theme.SUBHEADING_FONT).grid(row=0, column=0, sticky="w", padx=20, pady=(20,0))
        serial_entry = ctk.CTkEntry(self.action_frame, font=Theme.BODY_FONT, height=50); serial_entry.insert(0, serial)
        serial_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 20))
        
        brands_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        brands_frame.grid(row=2, column=0, sticky="nsew", padx=20)
        brands = { "Dell": "https://www.dell.com/support/home/", "HP": "https://support.hp.com/us-en/check-warranty", "Lenovo": "https://pcsupport.lenovo.com/warranty-lookup", "Asus": "https://www.asus.com/support/warranty-status-inquiry/", "Acer": "https://www.acer.com/us-en/support/warranty", "MSI": "https://us.msi.com/support/warranty" }
        for i, (brand, url) in enumerate(brands.items()):
            btn = ctk.CTkButton(brands_frame, text=brand, command=lambda u=url, s=serial: webbrowser.open(u+s), height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
            btn.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
            brands_frame.grid_columnconfigure(i%3, weight=1)

        self.result_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_frame.grid(row=3, column=0, sticky="s", pady=(20, 20))
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.result_frame, text="Bạn đã kiểm tra thông tin bảo hành của máy chưa?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_frame, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Đã kiểm tra", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Đã kiểm tra", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Bỏ qua", image=self.icon_manager.SKIP_ICON, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Không kiểm tra", "Trạng thái": "Bỏ qua"}), fg_color=Theme.SKIP, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra Ngoại Hình", "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp.", "**Bên ngoài:**\n  • Kiểm tra các vết trầy xước, cấn, móp ở các góc và mặt máy.\n  • Mở ra gập vào nhiều lần, lắng nghe **tiếng kêu lạ** và cảm nhận **độ rơ, lỏng lẻo của bản lề**.\n  • Cắm sạc và lay nhẹ để kiểm tra **độ lỏng của cổng sạc**.\n  • Nhìn kỹ các con ốc xem có bị **toét đầu, mất ốc** hay không.\n**Bên trong (Nếu có thể):**\n  • Soi tìm dấu hiệu oxy hóa, bụi bẩn, lông thú cưng tích tụ.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.result_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_frame.grid(row=0, column=0, sticky="nsew"); self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_frame.winfo_children(): widget.destroy()
        self.result_frame.grid_rowconfigure(0, weight=1); self.result_frame.grid_columnconfigure(0, weight=1)
        center_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent"); center_frame.grid(row=0, column=0)
        ctk.CTkLabel(center_frame, text="Tình trạng vật lý tổng thể của máy có tốt không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, máy cứng cáp, không dấu hiệu lạ", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tốt, không dấu hiệu bất thường", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có vấn đề (bản lề, móp...)", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có dấu hiệu bất thường", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = ("1. Khởi động lại máy và nhấn liên tục phím để vào BIOS (thường là **F2, DEL, F10, F12** tùy hãng).\n"
                    "2. Kiểm tra các mục sau:\n"
                    "   • **CPU Features:** Đảm bảo Intel Turbo Boost / AMD Core Performance Boost đang 'Enabled'.\n"
                    "   • **Memory:** Kiểm tra XMP/DOCP profile có được bật không (nếu có).\n"
                    "   • **Security:** Đảm bảo không có mật khẩu BIOS lạ.\n"
                    "   • **CẢNH BÁO:** Tìm các mục có tên **Computrace** hoặc **Absolute Persistence**. Nếu đang 'Enabled' hoặc 'Activated', hãy cẩn thận vì máy có thể bị khóa từ xa.")
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS", "BIOS là nơi chứa các cài đặt nền tảng của máy. Kiểm tra BIOS để đảm bảo các tính năng quan trọng không bị tắt và máy không bị khóa bởi các tính năng chống trộm của doanh nghiệp.", how_text, **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)

        self.result_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_frame.grid(row=0, column=0, sticky="nsew"); self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_frame.winfo_children(): widget.destroy()
        self.result_frame.grid_rowconfigure(0, weight=1); self.result_frame.grid_columnconfigure(0, weight=1)
        center_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent"); center_frame.grid(row=0, column=0)
        ctk.CTkLabel(center_frame, text="Các cài đặt trong BIOS có chính xác và an toàn không?", font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(center_frame, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, mọi cài đặt đều đúng", image=self.icon_manager.CHECK, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Cài đặt chính xác", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có cài đặt sai/bị khóa", image=self.icon_manager.CROSS, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề với cài đặt BIOS", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

class SystemStabilityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Phân Tích Lỗi Hệ Thống", "Event Viewer của Windows ghi lại mọi sự kiện quan trọng. Ứng dụng sẽ tự động quét và lọc ra các lỗi nghiêm trọng, giúp bạn phát hiện vấn đề tiềm ẩn.", "Nhấn 'Bắt đầu Quét' để tìm 50 sự kiện lỗi hệ thống gần nhất. Lỗi 'Critical' (ID 41) cho thấy máy đã bị tắt đột ngột. Nhiều lỗi 'Error' có thể là dấu hiệu của driver không ổn định.", **kwargs)
        self.action_frame.grid_rowconfigure(2, weight=1); self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.start_button = ctk.CTkButton(self.action_frame, text="Bắt đầu Quét Lịch Sử Lỗi", command=self.start_scan, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        if platform.system() != "Windows":
            self.start_button.configure(state="disabled", text="Chỉ hỗ trợ Windows")
            self.mark_completed({"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"})

        self.start_button.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
        self.status_label = ctk.CTkLabel(self.action_frame, text="Sẵn sàng để quét.", font=Theme.BODY_FONT)
        self.status_label.grid(row=1, column=0, pady=5, padx=20)
        
        self.results_frame = ctk.CTkScrollableFrame(self.action_frame, label_text="Các lỗi nghiêm trọng tìm thấy", label_font=Theme.BODY_FONT)
        self.results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10,20))
        self.results_frame.grid_remove()

    def start_scan(self):
        self.start_button.configure(state="disabled", text="Đang quét...")
        self.status_label.configure(text="Đang truy vấn Event Viewer, vui lòng đợi...")
        for widget in self.results_frame.winfo_children(): widget.destroy()
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        try:
            command = 'wevtutil qe System /q:"*[System[(Level=1 or Level=2)]]" /c:50 /rd:true /f:text'
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore', startupinfo=startupinfo)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0: raise IOError(f"Lỗi khi chạy wevtutil: {stderr}")
            events = self.parse_event_log(stdout)
            self.after(0, self.display_results, events)

        except Exception as e:
            self.after(0, self.status_label.configure, {"text": f"Lỗi: {e}", "text_color": Theme.ERROR})
            self.after(0, self.mark_completed, {"Kết quả": "Lỗi khi quét", "Trạng thái": "Lỗi", "Chi tiết": str(e)})

    def parse_event_log(self, log_text):
        events = []; current_event = {}
        for line in log_text.splitlines():
            line = line.strip()
            if not line and current_event: events.append(current_event); current_event = {}; continue
            parts = line.split(':', 1)
            if len(parts) == 2: key, value = parts; current_event[key.strip()] = value.strip()
        if current_event: events.append(current_event)
        return events

    def display_results(self, events):
        self.start_button.configure(state="normal", text="Quét Lại")
        self.status_label.configure(text=f"Hoàn thành. Tìm thấy {len(events)} lỗi nghiêm trọng trong 50 sự kiện gần nhất.")
        self.results_frame.grid()

        if not events:
            ctk.CTkLabel(self.results_frame, text="Tuyệt vời! Không tìm thấy lỗi hệ thống nghiêm trọng.", font=Theme.BODY_FONT, text_color=Theme.SUCCESS).pack(pady=20)
        
        explanation_text = "Lưu ý: Không phải tất cả các lỗi 'Error' đều đáng lo ngại. Nhiều lỗi chỉ là tạm thời hoặc do một dịch vụ khởi động chậm. Hãy chú ý đến các lỗi lặp đi lặp lại nhiều lần hoặc các lỗi 'Critical', đặc biệt là Event ID 41."
        ctk.CTkLabel(self.results_frame, text=explanation_text, font=Theme.SMALL_FONT, wraplength=1000, justify="left", text_color=Theme.TEXT_SECONDARY).pack(pady=(5, 15), fill="x", padx=10)

        for event in events:
            level = event.get("Level", "Unknown"); event_id = event.get('Event ID', 'N/A')
            is_critical = "Critical" in level; color = Theme.ERROR if is_critical else Theme.WARNING
            card = ctk.CTkFrame(self.results_frame, fg_color=Theme.FRAME, border_width=2, border_color=color)
            card.pack(fill="x", pady=5, padx=5)
            header = ctk.CTkFrame(card, fg_color="transparent"); header.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(header, text=f"Level: {level}", font=Theme.BODY_FONT, text_color=color).pack(side="left")
            ctk.CTkLabel(header, text=f"Date: {event.get('Date', 'N/A')}", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(side="right")
            source_text = f"Source: {event.get('Source', 'N/A')} (ID: {event_id})"
            ctk.CTkLabel(card, text=source_text, font=Theme.BODY_FONT, justify="left").pack(anchor="w", padx=10, pady=(0,5))
            if event_id == '41':
                desc_text = "Mô tả: Lỗi này cho thấy hệ thống đã khởi động lại mà không tắt hoàn toàn trước đó (ví dụ: mất điện, treo máy, nhấn giữ nút nguồn)."
                ctk.CTkLabel(card, text=desc_text, font=Theme.SMALL_FONT, text_color=Theme.ERROR, justify="left", wraplength=1000).pack(anchor="w", padx=10, pady=(0,10))

        details = "\n".join([f"- {e.get('Date')}: {e.get('Source')} (Level: {e.get('Level')}, ID: {e.get('Event ID')})" for e in events])
        has_critical = any("Critical" in e.get("Level", "") for e in events); is_ok = not has_critical and len(events) < 5
        result = { "Kết quả": "Lịch sử lỗi sạch" if is_ok else "Có lỗi hệ thống", "Trạng thái": "Tốt" if is_ok else "Lỗi", "Chi tiết": details if details else "Không có lỗi nghiêm trọng." }
        self.mark_completed(result)

class SummaryStep(ctk.CTkFrame):
    def __init__(self, master, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results):
        super().__init__(master, fg_color="transparent")
        self.title = "Tổng Kết & Báo Cáo"; self._completed = True; self.icon_manager = icon_manager
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS, border_width=1, border_color=Theme.BORDER)
        container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        container.grid_columnconfigure(0, weight=1); container.grid_rowconfigure(2, weight=1)
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=Theme.PADDING_X, pady=Theme.PADDING_Y)
        ctk.CTkLabel(header_frame, text=self.title, font=Theme.HEADING_FONT, text_color=Theme.TEXT).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Đây là bản tổng hợp kết quả của tất cả bài test.", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w")
        self.recommendation_frame = ctk.CTkFrame(container, fg_color="transparent", border_width=2, corner_radius=Theme.CORNER_RADIUS)
        self.recommendation_frame.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING_X, pady=(0, Theme.PADDING_Y))
        self.recommendation_text = ctk.CTkLabel(self.recommendation_frame, text="", font=Theme.SUBHEADING_FONT, wraplength=1100)
        self.recommendation_text.pack(padx=20, pady=15)
        self.summary_frame = ctk.CTkScrollableFrame(container, fg_color=Theme.BACKGROUND, corner_radius=0)
        self.summary_frame.grid(row=2, column=0, sticky="nsew", padx=Theme.PADDING_X, pady=10)
        self.summary_frame.grid_columnconfigure(0, weight=1)

    def is_ready_to_proceed(self): return True

    def _generate_recommendation(self, results):
        critical_errors, warnings = [], []
        CRITICAL_TESTS = [ "Định Danh Phần Cứng", "Cấu Hình Windows", "Sức Khỏe Ổ Cứng (S.M.A.R.T)", "Tốc Độ Ổ Cứng (Thực tế)", "Màn Hình", "Phân Tích Lỗi Hệ Thống", "Kiểm Tra CPU & Tản Nhiệt", "Kiểm Tra GPU & Tản nhiệt", "Kiểm Tra Ngoại Hình" ]
        for title, data in results.items():
            if data.get("Trạng thái") == "Lỗi":
                if title in CRITICAL_TESTS: critical_errors.append(title)
                else: warnings.append(title)

        if critical_errors:
            text = f"KHÔNG KHUYẾN NGHỊ: Phát hiện {len(critical_errors)} lỗi nghiêm trọng ở các mục: {', '.join(critical_errors)}. Cần kiểm tra kỹ lưỡng trước khi quyết định."
            color = Theme.ERROR
        elif warnings:
            text = f"CÂN NHẮC: Máy hoạt động tốt ở các mục chính nhưng có {len(warnings)} vấn đề ở phần cứng phụ: {', '.join(warnings)}. Có thể thương lượng giá."
            color = Theme.WARNING
        else:
            text = "TÌNH TRẠNG XUẤT SẮC: Máy đã vượt qua tất cả các bài kiểm tra quan trọng. Đây là một lựa chọn tốt."
            color = Theme.SUCCESS
        self.recommendation_frame.configure(border_color=color); self.recommendation_text.configure(text=text)

    def display_summary(self, results):
        self.results_data = results
        for widget in self.summary_frame.winfo_children(): widget.destroy()
        if not results: return
        self._generate_recommendation(results)
        
        filtered_results = {title: data for title, data in results.items() if title not in ["Chào mừng", "Nghiên Cứu"]}
        statuses = [data.get("Trạng thái") for data in filtered_results.values()]
        passed, failed, skipped, total_tests = statuses.count("Tốt"), statuses.count("Lỗi"), statuses.count("Bỏ qua"), len(statuses)

        summary_header = ctk.CTkFrame(self.summary_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        summary_header.pack(fill="x", padx=10, pady=(0, 15))
        summary_header.grid_columnconfigure((0,1,2), weight=1)
        ctk.CTkLabel(summary_header, text=f"{passed}/{total_tests}", font=Theme.TITLE_FONT, text_color=Theme.SUCCESS).grid(row=0, column=0, pady=(20, 5)); ctk.CTkLabel(summary_header, text="VƯỢT QUA", font=Theme.BODY_FONT, text_color=Theme.SUCCESS).grid(row=1, column=0, pady=(0, 20))
        ctk.CTkLabel(summary_header, text=f"{failed}/{total_tests}", font=Theme.TITLE_FONT, text_color=Theme.ERROR).grid(row=0, column=1, pady=(20, 5)); ctk.CTkLabel(summary_header, text="CÓ LỖI", font=Theme.BODY_FONT, text_color=Theme.ERROR).grid(row=1, column=1, pady=(0, 20))
        ctk.CTkLabel(summary_header, text=f"{skipped}/{total_tests}", font=Theme.TITLE_FONT, text_color=Theme.SKIP).grid(row=0, column=2, pady=(20, 5)); ctk.CTkLabel(summary_header, text="BỎ QUA", font=Theme.BODY_FONT, text_color=Theme.SKIP).grid(row=1, column=2, pady=(0, 20))

        for step_title, data in results.items():
            if step_title in ["Chào mừng", "Nghiên Cứu"]: continue
            card = ctk.CTkFrame(self.summary_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS); card.pack(fill="x", padx=10, pady=6); card.grid_columnconfigure(2, weight=1)
            status = data.get("Trạng thái", "N/A")
            color_map = {"Tốt": Theme.SUCCESS, "Lỗi": Theme.ERROR, "Bỏ qua": Theme.SKIP}; icon_map = {"Tốt": self.icon_manager.CHECK, "Lỗi": self.icon_manager.CROSS, "Bỏ qua": self.icon_manager.SKIP_ICON}
            status_color, status_icon = color_map.get(status, Theme.TEXT_SECONDARY), icon_map.get(status)
            
            ctk.CTkFrame(card, width=10, fg_color=status_color, corner_radius=0).grid(row=0, column=0, rowspan=3, sticky="ns", padx=(0,15))
            ctk.CTkLabel(card, image=status_icon, text=f" {step_title}", font=Theme.SUBHEADING_FONT, compound="left").grid(row=0, column=1, padx=(0,20), pady=15, sticky="w")
            ctk.CTkLabel(card, text=f"Kết quả: {data.get('Kết quả', 'N/A')}", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).grid(row=1, column=1, columnspan=2, padx=(0,20), pady=(0, 15), sticky="w")
            ctk.CTkLabel(card, text=status, font=Theme.SUBHEADING_FONT, text_color=status_color).grid(row=0, column=3, padx=20, pady=15, sticky="e")
            details = data.get("Chi tiết", "").strip()
            if details:
                def toggle(label, button):
                    if label.winfo_viewable(): label.grid_remove(); button.configure(text="Xem chi tiết")
                    else: label.grid(); button.configure(text="Ẩn chi tiết")
                
                detail_lbl = ctk.CTkLabel(card, text=details, font=Theme.SMALL_FONT, justify="left", wraplength=900, anchor="w");
                detail_lbl.grid(row=2, column=1, columnspan=3, padx=(0,20), pady=(0, 15), sticky="w"); detail_lbl.grid_remove()
                
                detail_btn = ctk.CTkButton(card, text="Xem chi tiết", font=Theme.SMALL_FONT, fg_color="transparent", text_color=Theme.ACCENT, width=120)
                detail_btn.configure(command=lambda l=detail_lbl, b=detail_btn: toggle(l, b)); detail_btn.grid(row=0, column=2, sticky="e")
                
        export_button = ctk.CTkButton(self.summary_frame, text="Xuất Báo Cáo (.html)", image=self.icon_manager.EXPORT, command=self.export_report_html, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        export_button.pack(fill="x", padx=10, pady=20)

    def export_report_html(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Documents", "*.html")], title="Lưu báo cáo kiểm tra")
        if not file_path: return
        hw_details = self.results_data.get('Định Danh Phần Cứng', {}).get('Chi tiết', ''); sys_details = self.results_data.get('Cấu Hình Windows', {}).get('Chi tiết', '')
        def find_detail(text, keyword):
            for line in text.split('\n'):
                if keyword in line.lower(): return line.split(':', 1)[1].strip()
            return 'N/A'
        
        html_content = f"""
        <!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Báo cáo kiểm tra Laptop</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; background-color: #f9f9f9; color: #333; }}
            .container {{ max-width: 1000px; margin: 20px auto; background-color: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
            h1, h2 {{ color: #007AFF; border-bottom: 2px solid #007AFF; padding-bottom: 10px; }} .header p {{ font-size: 1.1em; color: #555; }}
            .recommendation {{ padding: 20px; border-radius: 8px; margin: 20px 0; font-size: 1.2em; font-weight: bold; border-left: 5px solid; }}
            .rec-SUCCESS {{ border-color: #34C759; background-color: #eaf8ee; color: #2b6b43; }} .rec-ERROR {{ border-color: #FF3B30; background-color: #ffebee; color: #c62828; }}
            .rec-WARNING {{ border-color: #FF9500; background-color: #fff8e1; color: #e65100; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }} th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }} .details {{ font-size: 0.9em; color: #666; white-space: pre-wrap; margin-top: 8px; padding-left: 10px; border-left: 3px solid #eee;}}
            .status-cell span {{ padding: 5px 12px; border-radius: 15px; color: #fff; font-weight: bold; }}
            .status-Tốt-cell span {{ background-color: #34C759; }} .status-Lỗi-cell span {{ background-color: #FF3B30; }} .status-Bỏ-qua-cell span {{ background-color: #8E8E93; }}
        </style></head><body><div class="container">
            <div class="header"><h1>BÁO CÁO KIỂM TRA LAPTOP</h1><p>Báo cáo được tạo bởi Laptop Tester Pro vào lúc {time.strftime('%H:%M:%S, %d/%m/%Y')}</p></div>
            <h2>Đánh giá tổng thể</h2><div class="recommendation rec-{self.recommendation_frame.cget('border_color')}">{self.recommendation_text.cget("text")}</div>
            <h2>Thông số hệ thống</h2><table>
                <tr><th>Mục</th><th>Thông số</th></tr> <tr><td>Model</td><td>{find_detail(hw_details, 'model laptop')}</td></tr>
                <tr><td>Serial</td><td>{find_detail(hw_details, 'serial number')}</td></tr> <tr><td>CPU</td><td>{find_detail(sys_details, 'cpu')}</td></tr>
                <tr><td>RAM</td><td>{find_detail(sys_details, 'ram')}</td></tr> <tr><td>GPU</td><td>{find_detail(sys_details, 'gpu').replace('<br>', ', ')}</td></tr>
                <tr><td>Ổ cứng</td><td>{find_detail(sys_details, 'ổ cứng').replace('<br>', ', ')}</td></tr>
            </table><h2>Kết quả chi tiết</h2><table><tr><th>Hạng mục</th><th>Kết quả</th><th>Trạng thái</th></tr>
        """
        for step, data in self.results_data.items():
            if step in ["Chào mừng", "Nghiên Cứu"]: continue
            status_class = data.get('Trạng thái', 'N/A').replace(' ', '-')
            html_content += f"""
            <tr><td><strong>{step}</strong></td><td>{data.get('Kết quả', 'N/A')}
                {f"<div class='details'>{data['Chi tiết'].strip()}</div>" if 'Chi tiết' in data and data.get('Chi tiết') else ''}
            </td><td class="status-cell status-{status_class}-cell"><span>{data.get('Trạng thái', 'N/A')}</span></td></tr>
            """
        html_content += "</table></div></body></html>"
        try:
            with open(file_path, "w", encoding="utf-8") as f: f.write(html_content)
            messagebox.showinfo("Thành công", f"Báo cáo đã được lưu tại:\n{file_path}")
        except Exception as e: messagebox.showerror("Lỗi", f"Không thể lưu báo cáo: {e}")

    def stop_tasks(self): pass

# --- CÁC LỚP GIAO DIỆN CHÍNH ---
class HoverCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs); self.bind("<Enter>", self.on_enter); self.bind("<Leave>", self.on_leave)
    def on_enter(self, event): self.configure(border_color=Theme.ACCENT)
    def on_leave(self, event): self.configure(border_color=Theme.BORDER)

class ModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback, icon_manager):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        header_frame = ctk.CTkFrame(self, fg_color="transparent"); header_frame.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        ctk.CTkLabel(header_frame, text="Chào mừng bạn đến với Laptop Tester Pro", font=Theme.TITLE_FONT, text_color=Theme.TEXT).pack(pady=(0, 10))
        ctk.CTkLabel(header_frame, text="Vui lòng chọn chế độ kiểm tra phù hợp với bạn", font=Theme.HEADING_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=(0, 20))
        card_container = ctk.CTkFrame(self, fg_color="transparent"); card_container.grid(row=1, column=0, sticky="n"); card_container.grid_columnconfigure((0, 1), weight=1)
        card_basic = HoverCard(card_container, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS, border_width=2, border_color=Theme.BORDER)
        card_basic.grid(row=0, column=0, padx=20, pady=15, sticky="ns"); card_basic.grid_propagate(False); card_basic.configure(width=500, height=550)
        ctk.CTkLabel(card_basic, text="", image=icon_manager.BASIC_MODE).pack(pady=(40, 20))
        ctk.CTkLabel(card_basic, text="Kiểm Tra Cơ Bản", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(padx=60, pady=(0, 15))
        ctk.CTkLabel(card_basic, text="Dành cho mọi người dùng.\nNhanh chóng, an toàn và dễ hiểu, tập trung vào các chức năng chính.", font=Theme.BODY_FONT, wraplength=450, text_color=Theme.TEXT_SECONDARY).pack(padx=30, pady=10, expand=True)
        ctk.CTkButton(card_basic, text="Chọn Chế Độ Cơ Bản", command=lambda: self.mode_callback("basic"), height=Theme.BUTTON_HEIGHT, font=Theme.SUBHEADING_FONT, fg_color=Theme.SUCCESS).pack(padx=30, pady=30, fill="x", side="bottom")
        card_expert = HoverCard(card_container, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS, border_width=2, border_color=Theme.BORDER)
        card_expert.grid(row=0, column=1, padx=20, pady=15, sticky="ns"); card_expert.grid_propagate(False); card_expert.configure(width=500, height=550)
        ctk.CTkLabel(card_expert, text="", image=icon_manager.EXPERT_MODE).pack(pady=(40, 20))
        ctk.CTkLabel(card_expert, text="Kiểm Tra Chuyên Gia", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(padx=60, pady=(0, 15))
        ctk.CTkLabel(card_expert, text="Dành cho người dùng kỹ thuật.\nTích hợp các bài test chuyên sâu, chẩn đoán hiệu năng và sự ổn định của hệ thống.", font=Theme.BODY_FONT, wraplength=450, text_color=Theme.TEXT_SECONDARY).pack(padx=30, pady=10, expand=True)
        ctk.CTkButton(card_expert, text="Chọn Chế Độ Chuyên Gia", command=lambda: self.mode_callback("expert"), height=Theme.BUTTON_HEIGHT, font=Theme.SUBHEADING_FONT, fg_color=Theme.ACCENT).pack(padx=30, pady=30, fill="x", side="bottom")

class WizardFrame(ctk.CTkFrame):
    def __init__(self, master, mode, icon_manager):
        super().__init__(master, fg_color="transparent")
        self.app = master; self.test_results = {}; self.current_step_index = -1; self.icon_manager = icon_manager
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        
        title_container = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=0)
        title_container.grid(row=0, column=0, sticky="ew"); title_container.grid_columnconfigure(0, weight=1)
        self.step_title_main = ctk.CTkLabel(title_container, text="", font=Theme.HEADING_FONT, text_color=Theme.TEXT)
        self.step_title_main.grid(row=0, column=0, sticky="w", padx=Theme.PADDING_X, pady=(15, 0))
        self.step_title_sub = ctk.CTkLabel(title_container, text="", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
        self.step_title_sub.grid(row=1, column=0, sticky="w", padx=Theme.PADDING_X, pady=(0, 15))
        self.progress_header = ctk.CTkProgressBar(title_container, progress_color=Theme.ACCENT, fg_color=Theme.SEPARATOR)
        self.progress_header.grid(row=2, column=0, sticky="ew"); self.progress_header.set(0)

        self.steps_container = ctk.CTkFrame(self, fg_color="transparent")
        self.steps_container.grid(row=1, column=0, sticky="nsew")
        self.steps_container.grid_columnconfigure(0, weight=1); self.steps_container.grid_rowconfigure(0, weight=1)
        
        nav_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=0, border_color=Theme.SEPARATOR, border_width=1)
        nav_frame.grid(row=2, column=0, sticky="ew"); nav_frame.grid_columnconfigure(2, weight=1)
        
        self.home_button = ctk.CTkButton(nav_frame, text="Về Menu Chính", image=icon_manager.HOME, compound="left", command=self.app.show_mode_selection, width=200, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color="#DBDFE3", text_color=Theme.TEXT, hover_color="#C8CCCF")
        self.home_button.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        self.prev_button = ctk.CTkButton(nav_frame, text=" Quay Lại", image=icon_manager.ARROW_LEFT, compound="left", command=self.go_to_prev_step, width=170, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color="#DBDFE3", text_color=Theme.TEXT, hover_color="#C8CCCF")
        self.prev_button.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=15)
        self.skip_button = ctk.CTkButton(nav_frame, text=" Bỏ Qua", image=icon_manager.SKIP_ARROW, compound="left", command=self.skip_step, width=170, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.SKIP, hover_color=Theme.SKIP_HOVER)
        self.skip_button.grid(row=0, column=3, sticky="e", padx=(0, 10), pady=15)
        self.next_button = ctk.CTkButton(nav_frame, text="Tiếp Tục ", image=icon_manager.ARROW_RIGHT, compound="right", command=self.go_to_next_step, width=170, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT, fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        self.next_button.grid(row=0, column=4, sticky="e", padx=20, pady=15)
        
        basic_sw = [WelcomeStep, HardwareFingerprintStep, SystemInfoStep, LicenseCheckStep, HardDriveHealthStep]
        basic_hw = [ScreenTestStep, KeyboardTouchpadStep, PortsConnectivityStep, BatteryHealthStep, SpeakerTestStep, MicrophoneTestStep, WebcamTestStep]
        expert_pre = [ResearchGuideStep]
        expert_adv = [HardDriveSpeedStep, CPUStressTestStep, GPUStressTestStep, SystemStabilityStep]
        expert_final = [WarrantyCheckStep, PhysicalInspectionStep, BIOSCheckStep]

        if mode == "expert":
            self.steps_classes = expert_pre + basic_sw[1:] + basic_hw + expert_adv + expert_final + [SummaryStep]
        else:
            self.steps_classes = basic_sw + basic_hw + [WarrantyCheckStep, PhysicalInspectionStep, SummaryStep]

        self.total_steps = len(self.steps_classes); self.steps_cache = {}; self.current_frame = None
        self.go_to_step(0); self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

    def enable_next_button(self): self.next_button.configure(state="normal")

    def go_to_step(self, step_index):
        if not (0 <= step_index < self.total_steps): return
        
        if self.current_frame is not None:
            if hasattr(self.current_frame, 'stop_tasks'):
                self.current_frame.stop_tasks()
            
            if isinstance(self.current_frame, SummaryStep):
                self.current_frame.grid_forget()
            else:
                self.current_frame.pack_forget()

        self.current_step_index = step_index
        step_class = self.steps_classes[step_index]
        is_summary_step = (step_class == SummaryStep)
        
        # Consistent argument passing for all step constructors
        common_args = {
            "master": self if is_summary_step else self.steps_container,
            "record_result_callback": self.record_result,
            "enable_next_callback": self.enable_next_button,
            "go_to_next_step_callback": self.go_to_next_step,
            "icon_manager": self.icon_manager,
            "all_results": self.test_results
        }
        
        if step_index not in self.steps_cache:
            self.steps_cache[step_index] = step_class(**common_args)
        
        self.current_frame = self.steps_cache[step_index]
        
        if is_summary_step:
            self.steps_container.grid_remove() 
            self.current_frame.grid(row=1, column=0, sticky="nsew") 
            self.current_frame.display_summary(self.test_results)
        else:
            self.steps_container.grid() 
            self.current_frame.pack(expand=True, fill="both")
            if hasattr(self.current_frame, 'on_show'):
                self.current_frame.on_show()
            
        progress_val = (step_index + 1) / self.total_steps; self.progress_header.set(progress_val)
        self.step_title_main.configure(text=self.current_frame.title); self.step_title_sub.configure(text=f"Bước {step_index + 1} trên {self.total_steps}")
        self.prev_button.configure(state="normal" if self.current_step_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_frame.is_ready_to_proceed() else "disabled")
        
        is_skippable = not isinstance(self.current_frame, (WelcomeStep, SummaryStep, ResearchGuideStep))
        self.skip_button.grid() if is_skippable else self.skip_button.grid_remove()
        
        if is_summary_step:
            self.next_button.configure(text="Kết Thúc", image=None, compound="left", command=self.app.quit_app)
        else:
            self.next_button.configure(text="Tiếp Tục ", image=self.icon_manager.ARROW_RIGHT, compound="right", command=self.go_to_next_step)

    def go_to_next_step(self): self.go_to_step(self.current_step_index + 1)
    def go_to_prev_step(self): self.go_to_step(self.current_step_index - 1)
    def skip_step(self):
        self.current_frame.mark_skipped({"Kết quả": "Đã bỏ qua", "Trạng thái": "Bỏ qua"})
        self.go_to_next_step()
    def record_result(self, step_title, result_data): self.test_results[step_title] = result_data
    def on_closing(self):
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn đóng ứng dụng không?"):
            self.app.quit_app()
    def cleanup(self):
        for step in self.steps_cache.values():
            if hasattr(step, 'stop_tasks'):
                step.stop_tasks()

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=Theme.BACKGROUND)
        self.title("Laptop Tester Pro - Ultimate Edition (Fixed)"); self.state('zoomed'); self.minsize(1400, 900)
        
        try: self.iconbitmap(asset_path("icons/logo.ico"))
        except: print("Cảnh báo: Không tìm thấy file logo.ico")

        self.icon_manager = IconManager()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(0, weight=1)
        self.current_main_frame = None
        self.show_mode_selection()

    def clear_window(self):
        if self.current_main_frame:
            if hasattr(self.current_main_frame, 'cleanup'):
                self.current_main_frame.cleanup()
            self.current_main_frame.destroy()
        self.current_main_frame = None

    def show_mode_selection(self):
        self.clear_window()
        self.current_main_frame = ModeSelectionFrame(self, self.start_wizard, self.icon_manager)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    def start_wizard(self, mode):
        self.clear_window()
        self.current_main_frame = WizardFrame(self, mode, self.icon_manager)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew")

    def quit_app(self):
        self.clear_window()
        self.destroy()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
        
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    if platform.system() == "Windows":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit_app)
    app.mainloop()