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

import customtkinter as ctk

# --- THEME & ASSETS ---
class Theme:
    BACKGROUND="#F0F2F5"; FRAME="#FFFFFF"; CARD="#FFFFFF"; BORDER="#D9D9D9"; SEPARATOR = "#E8E8E8"
    TEXT="#1C1C1E"; TEXT_SECONDARY="#6D6D72"; ACCENT="#007AFF"; ACCENT_HOVER="#0056b3"
    SUCCESS="#34C759"; WARNING="#FF9500"; ERROR="#FF3B30"; SKIP="#8E8E93"; SKIP_HOVER="#6D6D72"
    TITLE_FONT=("Segoe UI", 48, "bold"); HEADING_FONT=("Segoe UI", 32, "bold"); SUBHEADING_FONT=("Segoe UI", 24, "bold")
    BODY_FONT=("Segoe UI", 18); SMALL_FONT=("Segoe UI", 15); KEY_FONT = ("Segoe UI", 12)
    CORNER_RADIUS = 16; PADDING_X = 30; PADDING_Y = 25; BUTTON_HEIGHT = 55
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
            if duration > 0 and time.time() > end_time:
                if 'timer_id' in locals() and timer_id:
                    win.after_cancel(timer_id)
                win.destroy()
                self.after(100, self.prompt_for_more_tests)
                return
            win.configure(fg_color=colors[color_index % len(colors)]); color_index += 1
            if duration > 0:
                timer_id = win.after(2000, change_color)
        def close_window(event=None):
            if 'timer_id' in locals() and timer_id:
                win.after_cancel(timer_id)
            if win.winfo_exists(): win.destroy()
            self.after(100, self.prompt_for_more_tests)
        win.bind("<Escape>", close_window)
        if duration == 0: win.bind("<Button-1>", change_color); win.bind("<Right>", change_color)
        change_color()

    def update_ui(self, status, color, result_data):
        self.status_label.configure(text=status, text_color=color)
        self.mark_completed(result_data, auto_advance=False)

    def __init__(self, master, **kwargs):
        super().__init__(master, "Bản Quyền Windows", "Một máy tính có bản quyền Windows hợp lệ đảm bảo bạn nhận được các bản cập nhật bảo mật quan trọng và tránh các rủi ro pháp lý.", "Ứng dụng sẽ tự động chạy lệnh kiểm tra trạng thái kích hoạt của Windows. Kết quả sẽ hiển thị bên dưới.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
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
            except (subprocess.CalledProcessError, FileNotFoundError):
                status, color, result_data = "Lỗi khi chạy lệnh kiểm tra", Theme.ERROR, {"Kết quả": "Lỗi khi chạy lệnh kiểm tra", "Trạng thái": "Lỗi"}
        else:
            status, color, result_data = "Chỉ hỗ trợ Windows", Theme.SKIP, {"Kết quả": "Chỉ hỗ trợ Windows", "Trạng thái": "Bỏ qua"}
        if self.winfo_exists():
            self.after(0, self.update_ui, status, color, result_data)

    def update_ui(self, status, color, result_data):
        self.status_label.configure(text=status, text_color=color)
        self.mark_completed(result_data, auto_advance=False)


# --- Canonical BaseStepFrame from backup ---
class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, title=title, why_text=why_text, how_text=how_text, **kwargs)
        self.worker_process = None

        self.worker_queue = multiprocessing.Queue()
        self.is_testing = False

    def run_worker(self, worker_func, args_tuple=()):
        if self.is_testing: return 
        self.is_testing = True; self._completed = False
        try:
            final_args = (self.worker_queue,) + args_tuple
            self.worker_process = multiprocessing.Process(target=worker_func, args=final_args, daemon=True)
            self.worker_process.start()
            self.after(100, self.check_queue)
        except Exception as e:
            messagebox.showerror("Lỗi Worker", f"Lỗi khởi tạo Process: {e}")
            self.is_testing = False

    def stop_worker(self):
        self.is_testing = False 
        if self.worker_process and self.worker_process.is_alive():
            self.worker_process.terminate()
            self.worker_process.join(timeout=1)
        while not self.worker_queue.empty():
            try: self.worker_queue.get_nowait() # Clear queue
            except Exception: pass

    def check_queue(self):
        if not self.is_testing: return 
        try:
            while not self.worker_queue.empty(): self.handle_message(self.worker_queue.get_nowait())
        except Exception: pass # Ignore queue empty errors
        finally:
            if self.is_testing: self.after(200, self.check_queue)

    def handle_message(self, msg):
        if not self.is_testing: return
        msg_type = msg.get('type')
        try:
            if msg_type == 'error':
                messagebox.showerror("Lỗi Worker", msg.get('message', 'Lỗi không xác định'))
                self.stop_worker()
                self.mark_completed({"Kết quả": "Lỗi Worker", "Trạng thái": "Lỗi", "Chi tiết": msg.get('message', '')})
            elif msg_type == 'update': self.update_ui(msg)
            elif msg_type == 'result': self.finalize_test(msg)
            elif msg_type == 'status':
                if hasattr(self, 'status_label'): self.status_label.configure(text=msg.get('message', ''))
            elif msg_type == 'done':
                self.is_testing = False
                if not self._completed:
                    logger.info(f"Worker for step '{self.title}' finished. Finalizing test.")
                    self.finalize_test({'data': {}})
        except Exception as e: print(f"Error handling message: {e}")

    def update_ui(self, data): pass
    def finalize_test(self, data): pass
    def stop_tasks(self):
        super().stop_tasks()
        self.stop_worker()
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, title=title, why_text=why_text, how_text=how_text, **kwargs)
        self.worker_process = None
        self.worker_queue = multiprocessing.Queue()
        self.is_testing = False

    def run_worker(self, worker_func, args_tuple=()):
        if self.is_testing: return 
        self.is_testing = True; self._completed = False
        try:
            final_args = (self.worker_queue,) + args_tuple
            self.worker_process = multiprocessing.Process(target=worker_func, args=final_args, daemon=True)
            self.worker_process.start()
            self.after(100, self.check_queue)
        except Exception as e:
            messagebox.showerror("Lỗi Worker", f"Lỗi khởi tạo Process: {e}")
            self.is_testing = False

    def stop_worker(self):
        self.is_testing = False 
        if self.worker_process and self.worker_process.is_alive():
            self.worker_process.terminate()
            self.worker_process.join(timeout=1)
        while not self.worker_queue.empty():
            try: self.worker_queue.get_nowait() # Clear queue
            except Exception: pass

    def check_queue(self):
        if not self.is_testing: return 
        try:
            while not self.worker_queue.empty(): self.handle_message(self.worker_queue.get_nowait())
        except Exception: pass # Ignore queue empty errors
        finally:
            if self.is_testing: self.after(200, self.check_queue)

    def handle_message(self, msg):
        if not self.is_testing: return
        msg_type = msg.get('type')
        try:
            if msg_type == 'error':
                messagebox.showerror("Lỗi Worker", msg.get('message', 'Lỗi không xác định'))
                self.stop_worker()
                self.mark_completed({"Kết quả": "Lỗi Worker", "Trạng thái": "Lỗi", "Chi tiết": msg.get('message', '')})
            elif msg_type == 'update': self.update_ui(msg)
            elif msg_type == 'result': self.finalize_test(msg)
            elif msg_type == 'status':
                if hasattr(self, 'status_label'): self.status_label.configure(text=msg.get('message', ''))
            elif msg_type == 'done':
                self.is_testing = False
                if not self._completed:
                    logger.info(f"Worker for step '{self.title}' finished. Finalizing test.")
                    self.finalize_test({'data': {}})
        except Exception as e: print(f"Error handling message: {e}")

    def update_ui(self, data): pass
    def finalize_test(self, data): pass
    def stop_tasks(self):
        super().stop_tasks()
        self.stop_worker()
    def __init__(self, master, **kwargs):
        super().__init__(master, "Định Danh Phần Cứng", "Đây là bước quan trọng nhất để chống lừa đảo. Các thông tin dưới đây được đọc trực tiếp từ BIOS và linh kiện phần cứng. Chúng **cực kỳ khó làm giả** từ bên trong Windows.", "Hãy so sánh các thông tin 'vàng' này với cấu hình mà người bán quảng cáo. Nếu có bất kỳ sự sai lệch nào, hãy đặt câu hỏi và kiểm tra thật kỹ.", **kwargs)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(0, weight=1)
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

class HardDriveHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Sức Khỏe Ổ Cứng (S.M.A.R.T)", "Ổ cứng sắp hỏng là mối rủi ro mất dữ liệu cực lớn. Bước này đọc 'báo cáo y tế' (S.M.A.R.T.) của ổ cứng để đánh giá độ bền.", "Chú ý đến mục 'Trạng thái'. 'Tốt' là bình thường. 'Lỗi/Cảnh báo' là rủi ro cao. Bước tiếp theo sẽ kiểm tra tốc độ thực tế.", **kwargs)
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
        if self.after_id: self.after_cancel(self.after_id); self.after_id = None

class KeyboardVisualTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bàn phím & Touchpad", "Một phím bị liệt, kẹt, hoặc touchpad bị loạn/mất cử chỉ đa điểm sẽ làm gián đoạn hoàn toàn công việc.", "**Bàn phím:** Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ sáng lên màu xanh dương, và chuyển sang xanh lá khi được nhả ra.\n**Touchpad:**\n   1. Dùng 1 ngón tay vẽ lên vùng màu xám để kiểm tra điểm chết cảm ứng.\n   2. **Quan trọng:** Dùng 2 ngón tay để cuộn lên/xuống và chụm/mở để thu phóng.", **kwargs)
    def create_key_widget(self, parent, text, grid_opts):
        key = ctk.CTkLabel(parent, text=text.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
        key.grid(**grid_opts)
        self.key_widgets[text.lower()] = key
        return key
    def populate_keyboard_visual(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(5, weight=1)
        row1 = ctk.CTkFrame(parent, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=(10, 5))
        keys_r1 = ['esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'delete']
        for i, k in enumerate(keys_r1):
            row1.grid_columnconfigure(i, weight=1)
            self.create_key_widget(row1, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 5})
        row2 = ctk.CTkFrame(parent, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        keys_r2 = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace']
        for i, k in enumerate(keys_r2):
            row2.grid_columnconfigure(i, weight=2 if i < 13 else 3)
            self.create_key_widget(row2, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row3 = ctk.CTkFrame(parent, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=5)
        keys_r3 = ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']
        for i, k in enumerate(keys_r3):
            row3.grid_columnconfigure(i, weight=3 if i == 0 or i == 13 else 2)
            self.create_key_widget(row3, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row4 = ctk.CTkFrame(parent, fg_color="transparent")
        row4.pack(fill="x", padx=10, pady=5)
        keys_r4 = ['caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter']
        for i, k in enumerate(keys_r4):
            row4.grid_columnconfigure(i, weight=4 if i == 0 or i == 12 else 2)
            self.create_key_widget(row4, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row5 = ctk.CTkFrame(parent, fg_color="transparent")
        row5.pack(fill="x", padx=10, pady=5)
        keys_r5 = ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift']
        for i, k in enumerate(keys_r5):
            row5.grid_columnconfigure(i, weight=5 if i == 0 or i == 11 else 2)
            self.create_key_widget(row5, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row6 = ctk.CTkFrame(parent, fg_color="transparent")
        row6.pack(fill="x", padx=10, pady=(5, 10))
        keys_r6 = ['ctrl', 'fn', 'windows', 'alt', 'space', 'right alt', 'right ctrl', 'left', 'up', 'down', 'right']
        weights = [2, 1, 2, 2, 12, 2, 2, 1, 1, 1, 1]
        for i, k in enumerate(keys_r6):
            row6.grid_columnconfigure(i, weight=weights[i])
            self.create_key_widget(row6, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
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
        if self.winfo_exists():
            self.after(0, self._update_key_ui, event.name, event.event_type)
    def _update_key_ui(self, key_name_raw, event_type):
        key_name = key_name_raw.lower()
        key_map = { 'left shift': 'shift', 'right shift': 'right shift', 'left ctrl': 'ctrl', 'right ctrl': 'right ctrl', 'left alt': 'alt', 'alt gr': 'right alt', 'left windows': 'windows', 'caps lock': 'caps lock', 'page up': 'page up', 'page down': 'page down', 'print screen': 'print screen', 'delete': 'delete', 'insert': 'insert', 'home': 'home', 'end': 'end', 'num lock': 'num lock' }
        mapped_key = key_map.get(key_name, key_name)
        widget = self.key_widgets.get(mapped_key)
        if not widget: return
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
            if "root" in str(e).lower():
                messagebox.showwarning("Yêu cầu quyền Admin", "Không thể bắt sự kiện bàn phím do thiếu quyền Admin/root. Vui lòng chạy lại ứng dụng với quyền quản trị viên.")
    def stop_tasks(self):
        super().stop_tasks()
        try:
            keyboard.unhook_all()
        except Exception: pass

class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = ("1. Khởi động lại máy và nhấn liên tục phím để vào BIOS (thường là **F2, DEL, F10, F12** tùy hãng).\n"
                    "2. Kiểm tra các mục sau:\n"
                    "   • **CPU Features:** Đảm bảo Intel Turbo Boost / AMD Core Performance Boost đang 'Enabled'.\n"
                    "   • **Memory:** Kiểm tra XMP/DOCP profile có được bật không (nếu có).\n"
                    "   • **Security:** Đảm bảo không có mật khẩu BIOS lạ.\n"
                    "   • **CẢNH BÁO:** Tìm các mục có tên **Computrace** hoặc **Absolute Persistence**. Nếu đang 'Enabled' hoặc 'Activated', hãy cẩn thận vì máy có thể bị khóa từ xa.")
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS", "BIOS là nơi chứa các cài đặt nền tảng của máy. Kiểm tra BIOS để đảm bảo các tính năng quan trọng không bị tắt và máy không bị khóa bởi các tính năng chống trộm của doanh nghiệp.", how_text, **kwargs)
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

class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra Ngoại Hình", "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp.", "**Bên ngoài:**\n  • Kiểm tra các vết trầy xước, cấn, móp ở các góc và mặt máy.\n  • Mở ra gập vào nhiều lần, lắng nghe **tiếng kêu lạ** và cảm nhận **độ rơ, lỏng lẻo của bản lề**.\n  • Cắm sạc và lay nhẹ để kiểm tra **độ lỏng của cổng sạc**.\n  • Nhìn kỹ các con ốc xem có bị **toét đầu, mất ốc** hay không.\n**Bên trong (Nếu có thể):**\n  • Soi tìm dấu hiệu oxy hóa, bụi bẩn, lông thú cưng tích tụ.", **kwargs)
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


class SummaryStep(BaseStepFrame):
    def __init__(self, master, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results):
        super().__init__(master, fg_color="transparent")
        # ...existing code...
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra GPU & Tản nhiệt", "GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng.", "Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 90 giây. Hãy quan sát:\n  • Có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?\n  • Máy có bị treo hoặc tự khởi động lại không?\n  • **Khuyến nghị:** Dùng phần mềm như HWMonitor để theo dõi nhiệt độ GPU song song.", **kwargs)
        # ...existing code...
    def __init__(self, master, **kwargs):
        super().__init__(master, "Microphone", "Micro tốt là điều kiện bắt buộc cho họp và học online. Cần đảm bảo mic thu âm rõ ràng, không bị rè.", "1. Nhấn 'Bắt đầu ghi âm' và nói vài câu. Theo dõi cột sóng âm bên dưới.\n2. Sau 5 giây, nhấn 'Phát lại' để nghe lại.\n3. Dựa vào chất lượng nghe lại để đánh giá.", **kwargs)
        self.recording_data = []
        self.stream = None
        self.is_recording = False
        self.fs = 44100
        self.duration = 5
        self.temp_file_obj = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self.temp_file = self.temp_file_obj.name
        # ...existing code...
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bàn phím & Touchpad", "Một phím bị liệt, kẹt, hoặc touchpad bị loạn/mất cử chỉ đa điểm sẽ làm gián đoạn hoàn toàn công việc.", "**Bàn phím:** Gõ lần lượt tất cả các phím. Phím bạn gõ sẽ sáng lên màu xanh dương, và chuyển sang xanh lá khi được nhả ra.\n**Touchpad:**\n   1. Dùng 1 ngón tay vẽ lên vùng màu xám để kiểm tra điểm chết cảm ứng.\n   2. **Quan trọng:** Dùng 2 ngón tay để cuộn lên/xuống và chụm/mở để thu phóng.", **kwargs)
        
        self.action_frame.grid_rowconfigure(1, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.key_widgets = {}
        self.pressed_keys = set()
        
        self.canvas = ctk.CTkCanvas(self.action_frame, bg=Theme.FRAME, height=120, highlightthickness=1, highlightbackground=Theme.BORDER)
        self.canvas.grid(row=0, column=0, sticky="ew", pady=(20, 15), padx=20)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        
        keyboard_frame = ctk.CTkFrame(self.action_frame, fg_color="#DCE4E8", corner_radius=Theme.CORNER_RADIUS)
        keyboard_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,15))
        self.populate_keyboard_visual(keyboard_frame)

        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="s", pady=(0, 20))
        self.show_result_choices()

        self.start_listening()
    def create_key_widget(self, parent, text, grid_opts):
        key = ctk.CTkLabel(parent, text=text.upper(), font=Theme.KEY_FONT, fg_color=Theme.FRAME, text_color=Theme.TEXT_SECONDARY, corner_radius=4)
        key.grid(**grid_opts)
        self.key_widgets[text.lower()] = key
        return key
    def populate_keyboard_visual(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(5, weight=1)
        row1 = ctk.CTkFrame(parent, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=(10, 5))
        keys_r1 = ['esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'delete']
        for i, k in enumerate(keys_r1):
            row1.grid_columnconfigure(i, weight=1)
            self.create_key_widget(row1, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 5})
        row2 = ctk.CTkFrame(parent, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        keys_r2 = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace']
        for i, k in enumerate(keys_r2):
            row2.grid_columnconfigure(i, weight=2 if i < 13 else 3)
            self.create_key_widget(row2, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row3 = ctk.CTkFrame(parent, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=5)
        keys_r3 = ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']
        for i, k in enumerate(keys_r3):
            row3.grid_columnconfigure(i, weight=3 if i == 0 or i == 13 else 2)
            self.create_key_widget(row3, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row4 = ctk.CTkFrame(parent, fg_color="transparent")
        row4.pack(fill="x", padx=10, pady=5)
        keys_r4 = ['caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter']
        for i, k in enumerate(keys_r4):
            row4.grid_columnconfigure(i, weight=4 if i == 0 or i == 12 else 2)
            self.create_key_widget(row4, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row5 = ctk.CTkFrame(parent, fg_color="transparent")
        row5.pack(fill="x", padx=10, pady=5)
        keys_r5 = ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift']
        for i, k in enumerate(keys_r5):
            row5.grid_columnconfigure(i, weight=5 if i == 0 or i == 11 else 2)
            self.create_key_widget(row5, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        row6 = ctk.CTkFrame(parent, fg_color="transparent")
        row6.pack(fill="x", padx=10, pady=(5, 10))
        keys_r6 = ['ctrl', 'fn', 'windows', 'alt', 'space', 'right alt', 'right ctrl', 'left', 'up', 'down', 'right']
        weights = [2, 1, 2, 2, 12, 2, 2, 1, 1, 1, 1]
        for i, k in enumerate(keys_r6):
            row6.grid_columnconfigure(i, weight=weights[i])
            self.create_key_widget(row6, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
    def __init__(self, master, title, why_text, how_text, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results):
        super().__init__(master, title, why_text, how_text, record_result_callback, enable_next_callback, go_to_next_step_callback, icon_manager, all_results)
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

class HardDriveSpeedStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tốc Độ Ổ Cứng (Thực tế)", "Tốc độ đọc/ghi thực tế ảnh hưởng trực tiếp đến tốc độ khởi động, mở ứng dụng và sao chép file.", "Ứng dụng sẽ tạo một file tạm 256MB, ghi dữ liệu ngẫu nhiên vào đó, sau đó đọc lại để đo tốc độ tuần tự. Kết quả sẽ phản ánh hiệu năng của SSD/HDD.", **kwargs)
        self.start_button.configure(image=self.icon_manager.HDD, compound="left")
        benchmarks = {"CrystalDiskMark": "https://crystalmark.info/en/software/crystaldiskmark/"}
        self.create_external_benchmark_box(self.action_frame, 5, 0, benchmarks)

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
        self.chart_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.chart_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 10))
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.canvas = ctk.CTkCanvas(self.chart_frame, bg=Theme.FRAME, highlightthickness=1, highlightbackground=Theme.SEPARATOR, height=250)
        self.canvas.pack(fill="both", expand=True)
        self.chart_frame.grid_remove()
        self.temp_data = deque(maxlen=self.TEST_DURATION + 5)
        self.usage_data = deque(maxlen=self.TEST_DURATION + 5)
        self.max_temp = 0
        benchmarks = {
            "Cinebench": "https://www.maxon.net/en/cinebench",
            "Prime95": "https://www.mersenne.org/download/"
        }
        self.create_external_benchmark_box(self.action_frame, 5, 0, benchmarks)

    def start_test(self):
        self.temp_data.clear(); self.usage_data.clear(); self.max_temp = 0
        self.chart_frame.grid()
        self.after(100, self.draw_chart) 
        self.run_worker(run_cpu_stress_test, (self.queue, self.TEST_DURATION))

    def update_ui(self, data):
        temp = data.get('temp')
        usage = data.get('usage')
        if temp is not None:
            self.temp_data.append(temp)
            if temp > self.max_temp: self.max_temp = temp
        else:
            self.temp_data.append(-1) 
        self.usage_data.append(usage if usage is not None else -1)
        self.status_label.configure(text=f"Tải: {usage or 'N/A'}% | Nhiệt độ: {temp or 'N/A'}°C | Cao nhất: {self.max_temp}°C")
        self.draw_chart()

    def draw_chart(self):
        if not self.winfo_exists(): return
        self.canvas.delete("all")
        w = self.canvas.winfo_width(); h = self.canvas.winfo_height()
        if w <  50 or h < 50: return
        PAD_L, PAD_R, PAD_T, PAD_B = 40, 40, 20, 30
        chart_w, chart_h = w - PAD_L - PAD_R, h - PAD_T - PAD_B
        # Draw Y-axis grid & labels
        for i in range(6):
            y = PAD_T + i * (chart_h / 5)
            val = 100 - i * 20
            self.canvas.create_line(PAD_L, y, w - PAD_R, y, fill=Theme.SEPARATOR, dash=(2, 2))
            self.canvas.create_text(PAD_L - 5, y, text=f"{val}%", anchor="e", fill=Theme.ACCENT)
            self.canvas.create_text(w - PAD_R + 5, y, text=f"{val+20}°C", anchor="w", fill=Theme.ERROR)
        # Legend
        self.canvas.create_rectangle(PAD_L, h - PAD_B + 10, PAD_L + 15, h - PAD_B + 20, fill=Theme.ACCENT, outline="")
        self.canvas.create_text(PAD_L + 20, h - PAD_B + 15, text="Tải CPU", anchor="w", fill=Theme.TEXT_SECONDARY)
        self.canvas.create_rectangle(PAD_L + 100, h - PAD_B + 10, PAD_L + 115, h - PAD_B + 20, fill=Theme.ERROR, outline="")
        self.canvas.create_text(PAD_L + 120, h - PAD_B + 15, text="Nhiệt độ", anchor="w", fill=Theme.TEXT_SECONDARY)
        def get_points(data, max_val):
            points = []
            if len(data) < 2: return []
            step = chart_w / (self.TEST_DURATION - 1) if self.TEST_DURATION > 1 else chart_w
            for i, val in enumerate(data):
                if val is None or val < 0: continue
                x = PAD_L + (i * step)
                y = PAD_T + chart_h - (val / max_val * chart_h)
                points.extend([x, y])
            return points
        self.canvas.create_line(get_points(self.usage_data, 100), fill=Theme.ACCENT, width=2)
        self.canvas.create_line(get_points(self.temp_data, 120), fill=Theme.ERROR, width=2)

    def finalize_test(self, msg):
        self.chart_frame.grid_remove()
        details = f"Thời gian test: {len(self.temp_data)} giây.\nNhiệt độ tối đa ghi nhận: {self.max_temp}°C."
        is_ok = self.max_temp > 0 and self.max_temp < 98
        result_data = {"Kết quả": f"Nhiệt độ tối đa: {self.max_temp}°C", "Trạng thái": "Tốt" if is_ok else "Lỗi", "Chi tiết": details}
        self.mark_completed(result_data)
        self.status_label.configure(text=f"Test hoàn thành. Nhiệt độ tối đa: {self.max_temp}°C")

class GPUStressTestStep(BaseStressTestStep):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra GPU & Tản nhiệt", "GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng.", "Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 90 giây. Hãy quan sát:\n  • Có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?\n  • Máy có bị treo hoặc tự khởi động lại không?\n  • **Khuyến nghị:** Dùng phần mềm như HWMonitor để theo dõi nhiệt độ GPU song song.", **kwargs)
        self.TEST_DURATION = 90
        self.start_button.configure(image=self.icon_manager.GPU, compound="left")
        benchmarks = {
            "FurMark": "https://geeks3d.com/furmark/",
            "3DMark": "https://www.3dmark.com/"
        }
        self.create_external_benchmark_box(self.action_frame, 5, 0, benchmarks)

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

class SystemStabilityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Test Độ Ổn Định", "Chức năng đang được phát triển.", "Chức năng này sẽ kiểm tra độ ổn định của hệ thống.", **kwargs)
        ctk.CTkLabel(self.action_frame, text="Chức năng này chưa được thực hiện.").pack(pady=20, padx=20)
        self.mark_completed({"Kết quả": "Chưa thực hiện", "Trạng thái": "Bỏ qua"})

class WarrantyCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra Bảo Hành", "Chức năng đang được phát triển.", "Chức năng này sẽ giúp bạn kiểm tra thông tin bảo hành.", **kwargs)
        ctk.CTkLabel(self.action_frame, text="Chức năng này chưa được thực hiện.").pack(pady=20, padx=20)
        self.mark_completed({"Kết quả": "Chưa thực hiện", "Trạng thái": "Bỏ qua"})

class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tổng Kết", "", "", **kwargs)
        self.title = "Tổng Kết"
    def display_summary(self, results):
        for widget in self.action_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.action_frame, text="Báo cáo tổng kết", font=Theme.HEADING_FONT).pack(pady=20)
        
        text_box = ctk.CTkTextbox(self.action_frame, font=Theme.BODY_FONT, wrap="word")
        text_box.pack(fill="both", expand=True, padx=20, pady=10)

        summary_text = ""
        for step, result in results.items():
            summary_text += f"--- {step} ---\n"
            summary_text += f"  Kết quả: {result.get('Kết quả', 'N/A')}\n"
            summary_text += f"  Trạng thái: {result.get('Trạng thái', 'N/A')}\n"
            if result.get('Chi tiết'):
                summary_text += f"  Chi tiết: {result.get('Chi tiết', 'N/A')}\n"
            summary_text += "\n"
        
        text_box.insert("0.0", summary_text)
        text_box.configure(state="disabled")
        # Phân tích AI tổng hợp
        ai_summary = ai_analyzer.ai_diagnoser.analyze_summary(results)
        summary_text += "\n=== ĐÁNH GIÁ AI ===\n"
        for suggestion in ai_summary.get('ai_summary', []):
            if suggestion and 'ai_warning' in suggestion:
                summary_text += f"- {suggestion['ai_warning']}\n"
        summary_text += "\n"
        text_box.configure(state="normal")
        text_box.insert("end", summary_text)
        text_box.configure(state="disabled")

# --- UI FRAMES ---

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

        basic_software = [HardwareFingerprintStep, SystemInfoStep, LicenseCheckStep, HardDriveHealthStep] 
        basic_hardware = [ScreenTestStep, KeyboardVisualTestStep, PortsConnectivityStep, BatteryHealthStep, SpeakerTestStep, MicrophoneTestStep, WebcamTestStep]
        expert_intro = [ResearchGuideStep] 
        expert_performance = [HardDriveSpeedStep, CPUStressTestStep, GPUStressTestStep, SystemStabilityStep] 
        expert_final = [BIOSCheckStep]
        common_final = [WarrantyCheckStep, PhysicalInspectionStep]

        self.steps_classes = [WelcomeStep]
        if mode == "expert":
            self.steps_classes += expert_intro + basic_software + basic_hardware + expert_performance + expert_final + common_final
        else:
            self.steps_classes += basic_software + basic_hardware + common_final
        self.steps_classes.append(SummaryStep)

        self.total_steps = len(self.steps_classes); self.steps_cache = {}; self.current_frame = None
        self.go_to_step(0); self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

    def enable_next_button(self): self.next_button.configure(state="normal")

    def go_to_step(self, step_index):
        if not (0 <= step_index < self.total_steps): return
        if self.current_frame is not None:
            if hasattr(self.current_frame, 'stop_tasks'): self.current_frame.stop_tasks()
            self.current_frame.grid_forget()
            self.current_frame.pack_forget()

        self.current_step_index = step_index
        step_class = self.steps_classes[step_index]
        
        common_args = {"master": self.steps_container, "record_result_callback": self.record_result, "enable_next_callback": self.enable_next_button, "go_to_next_step_callback": self.go_to_next_step, "icon_manager": self.icon_manager, "all_results": self.test_results}
        
        if step_index not in self.steps_cache:
            if step_class == SummaryStep:
                common_args["master"] = self
            self.steps_cache[step_index] = step_class(**common_args)
        
        self.current_frame = self.steps_cache[step_index]
        
        if isinstance(self.current_frame, SummaryStep):
            self.steps_container.grid_forget()
            self.current_frame.grid(row=1, column=0, sticky="nsew")
            self.current_frame.display_summary(self.test_results)
        else:
            self.steps_container.grid(row=1, column=0, sticky="nsew")
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            if hasattr(self.current_frame, 'on_show'): self.current_frame.on_show()
            
        progress_val = (step_index + 1) / self.total_steps; self.progress_header.set(progress_val)
        self.step_title_main.configure(text=self.current_frame.title); self.step_title_sub.configure(text=f"Bước {step_index + 1} trên {self.total_steps}")
        self.prev_button.configure(state="normal" if self.current_step_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_frame.is_ready_to_proceed() else "disabled")
        
        is_skippable = not isinstance(self.current_frame, (WelcomeStep, SummaryStep, ResearchGuideStep))
        self.skip_button.grid() if is_skippable else self.skip_button.grid_remove()
        
        if isinstance(self.current_frame, SummaryStep):
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
        self.title("Laptop Tester Pro"); self.state('zoomed'); self.minsize(1400, 900)
        try: self.iconbitmap(asset_path("icons/logo.ico"))
        except: print("Cảnh báo: Không tìm thấy file logo.ico")
        self.icon_manager = IconManager()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(0, weight=1)
        self.current_main_frame = None
        self.show_mode_selection()

    def clear_window(self): 
        if self.current_main_frame:
            if hasattr(self.current_main_frame, 'cleanup'): self.current_main_frame.cleanup()
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


# --- MAIN BLOCK ---
if __name__ == "__main__":
    multiprocessing.freeze_support()
    if getattr(sys, 'frozen', False):
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            pass
        
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
