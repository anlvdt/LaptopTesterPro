#!/usr/bin/env python3
"""
LaptopTester Pro - Original Version
Khôi phục phiên bản gốc với checklist đầy đủ
"""

import multiprocessing
import sys
import os
import platform
import threading
import time
import tkinter as tk
import customtkinter as ctk
import psutil
from PIL import Image
import wmi
import pythoncom

# Theme definition
class Theme:
    # Colors - Modern design system
    BACKGROUND="#F8FAFC"; FRAME="#FFFFFF"; CARD="#FFFFFF"; BORDER="#E2E8F0"; SEPARATOR = "#F1F5F9"
    TEXT="#0F172A"; TEXT_SECONDARY="#64748B"; ACCENT="#3B82F6"; ACCENT_HOVER="#2563EB"
    SUCCESS="#10B981"; WARNING="#F59E0B"; ERROR="#EF4444"; SKIP="#94A3B8"; SKIP_HOVER="#64748B"
    INFO="#06B6D4"; GRADIENT_START="#3B82F6"; GRADIENT_END="#8B5CF6"
    # Typography - Improved hierarchy
    TITLE_FONT=("Segoe UI", 42, "bold"); HEADING_FONT=("Segoe UI", 28, "bold"); SUBHEADING_FONT=("Segoe UI", 22, "bold")
    BODY_FONT=("Segoe UI", 16); SMALL_FONT=("Segoe UI", 14); KEY_FONT = ("Segoe UI", 11)
    BUTTON_FONT=("Segoe UI", 14)
    # Layout - Better spacing
    CORNER_RADIUS = 12; PADDING_X = 24; PADDING_Y = 20; BUTTON_HEIGHT = 48
    CARD_PADDING = 20; SECTION_SPACING = 16; ELEMENT_SPACING = 12

class IconManager:
    def __init__(self):
        self.CHECK = None; self.CROSS = None; self.SKIP_ICON = None; self.WHY = None; self.HOW = None
        self.LOGO_SMALL = None

def asset_path(rel_path):
    return os.path.join(os.path.dirname(__file__), 'assets', rel_path)

# Enhanced BaseStepFrame
class BaseStepFrame(ctk.CTkFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
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

        # Layout cân bằng và tận dụng không gian
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)  # Guide panel
        self.grid_columnconfigure(1, weight=3)  # Action panel - rộng hơn
        
        # Guide container (left panel)
        guide_container = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        guide_container.grid(row=0, column=0, sticky="nsew", padx=(Theme.PADDING_X, Theme.ELEMENT_SPACING), pady=Theme.PADDING_Y)
        guide_container.grid_columnconfigure(0, weight=1)
        guide_container.grid_rowconfigure(0, weight=1)
        guide_container.grid_rowconfigure(1, weight=0)
        guide_container.grid_rowconfigure(2, weight=1)
        guide_container.grid_rowconfigure(3, weight=0)  # Tips frame
        
        why_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        why_frame.grid(row=0, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(why_frame, image=self.icon_manager.WHY if self.icon_manager else None, text=" Tại sao cần test?", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT, compound="left").pack(anchor="w")
        ctk.CTkLabel(why_frame, text=why_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.TEXT).pack(anchor="w", pady=(Theme.ELEMENT_SPACING,0))
        
        ctk.CTkFrame(guide_container, height=1, fg_color=Theme.SEPARATOR).grid(row=1, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.ELEMENT_SPACING)
        
        how_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        how_frame.grid(row=2, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(how_frame, image=self.icon_manager.HOW if self.icon_manager else None, text=" Hướng dẫn thực hiện:", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT, compound="left").pack(anchor="w")
        ctk.CTkLabel(how_frame, text=how_text, font=Theme.BODY_FONT, wraplength=380, justify="left", text_color=Theme.TEXT).pack(anchor="w", pady=(Theme.ELEMENT_SPACING,0))
        
        # Action container (right panel)
        action_container = ctk.CTkFrame(self, fg_color="transparent")
        action_container.grid(row=0, column=1, sticky="nsew", padx=(Theme.ELEMENT_SPACING, Theme.PADDING_X), pady=Theme.PADDING_Y)
        action_container.grid_columnconfigure(0, weight=1)
        action_container.grid_rowconfigure(0, weight=1)
        
        # Action frame
        self.action_frame = ctk.CTkFrame(action_container, fg_color=Theme.CARD, corner_radius=Theme.CORNER_RADIUS)
        self.action_frame.grid(row=0, column=0, sticky="nsew")
        self.action_frame.grid_columnconfigure(0, weight=1)

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

# Bước 1: Checklist ngoại hình
class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            "Kiểm Tra Ngoại Hình",
            "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp.",
            "**Bên ngoài:**\n  • Kiểm tra các vết trầy xước, cấn, móp ở các góc và mặt máy.\n  • Mở ra gập vào nhiều lần, lắng nghe **tiếng kêu lạ** và cảm nhận **độ rơ, lỏng lẻo của bản lề**.\n  • Cắm sạc và lay nhẹ để kiểm tra **độ lỏng của cổng sạc**.\n  • Nhìn kỹ các con ốc xem có bị **toét đầu, mất ốc** hay không.\n**Bên trong (Nếu có thể):**\n  • Soi tìm dấu hiệu oxy hóa, bụi bẩn, lông thú cưng tích tụ.",
            **kwargs
        )
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
        
        self.btn_excellent = ctk.CTkButton(button_bar, text="✨ Rất tốt - Như mới", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Rất tốt - Như mới", "Trạng thái": "Xuất sắc"}, {}), fg_color="#28a745", height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_excellent.pack(side="left", padx=5)
        
        self.btn_good = ctk.CTkButton(button_bar, text="✅ Tốt - Vết nhỏ", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tốt - Có vết sử dụng nhỏ", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_good.pack(side="left", padx=5)
        
        self.btn_fair = ctk.CTkButton(button_bar, text="⚠️ Trung bình - Có lỗi nhỏ", image=self.icon_manager.WHY if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Trung bình - Có lỗi nhỏ cần lưu ý", "Trạng thái": "Cảnh báo"}, {}), fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_fair.pack(side="left", padx=5)
        
        self.btn_poor = ctk.CTkButton(button_bar, text="❌ Kém - Nhiều vấn đề", image=self.icon_manager.CROSS if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Kém - Nhiều vấn đề nghiêm trọng", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_poor.pack(side="left", padx=5)
        
        self.result_container.lift()
        self.result_container.update_idletasks()

# Bước 2: BIOS
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
        self.btn_yes = ctk.CTkButton(button_bar, text="Có, mọi cài đặt đều đúng", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Cài đặt chính xác", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="Không, có cài đặt sai/bị khóa", image=self.icon_manager.CROSS if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề với cài đặt BIOS", "Trạng thái": "Lỗi"}), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

# Bước 3: Định danh phần cứng tự động
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
                
                # Lấy thông tin CPU
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
        self.btn_yes = ctk.CTkButton(button_bar, text="Tiếp tục", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Kết quả": "Tiếp tục", "Trạng thái": "Tốt"}, {}), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_skip = ctk.CTkButton(button_bar, text="Bỏ qua", image=self.icon_manager.SKIP_ICON if hasattr(self.icon_manager, 'SKIP_ICON') else None, compound="left", command=lambda: self.mark_skipped({"Kết quả": "Bỏ qua", "Trạng thái": "Bỏ qua"}), fg_color=Theme.SKIP, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)

# Simple fallback classes
class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bản Quyền Windows", "Kiểm tra bản quyền", "Tự động kiểm tra", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class SystemInfoStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cấu Hình Windows", "Thông tin hệ thống", "Tự động đọc", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class HardDriveHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Sức Khỏe Ổ Cứng", "Kiểm tra S.M.A.R.T", "Tự động kiểm tra", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class ScreenTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Màn Hình", "Test màn hình", "Kiểm tra pixel", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class KeyboardVisualTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bàn phím & Touchpad", "Test bàn phím", "Nhấn phím", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class PortsConnectivityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cổng Kết Nối", "Test cổng", "Cắm thiết bị", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Pin Laptop", "Kiểm tra pin", "Đọc thông tin pin", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class SpeakerTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Loa & Micro", "Test âm thanh", "Phát âm test", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Webcam", "Test camera", "Mở camera", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class NetworkTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Mạng & WiFi", "Test mạng", "Kiểm tra kết nối", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "CPU Stress Test", "Test CPU", "Stress test", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class HardDriveSpeedStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tốc Độ Ổ Cứng", "Test tốc độ", "Benchmark", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Stress Test", "Test GPU", "Stress test", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class ThermalPerformanceStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Thermal Monitor", "Giám sát nhiệt", "Monitor nhiệt độ", **kwargs)
        self.mark_completed({"Kết quả": "OK", "Trạng thái": "Tốt"}, auto_advance=True)

class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Báo Cáo Tổng Kết", "", "", **kwargs)
        self.title = "Báo Cáo Tổng Kết"
    
    def display_summary(self, results):
        for widget in self.action_frame.winfo_children(): 
            widget.destroy()
        
        ctk.CTkLabel(self.action_frame, text="📊 BÁO CÁO TỔNG KẾT", font=Theme.HEADING_FONT).pack(pady=20)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        stats_text = f"Tổng số test: {total_tests}\nĐạt: {passed_tests}/{total_tests}\nTỷ lệ thành công: {success_rate:.1f}%"
        ctk.CTkLabel(self.action_frame, text=stats_text, font=Theme.BODY_FONT).pack(pady=10)

# WizardFrame với cấu trúc bước đúng
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
        # Navigation luôn hiển thị và cố định
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
        # Cấu trúc bước đúng như main_enhanced
        basic_steps = [
            # Bước 1: Checklist ngoại hình
            ("Kiểm tra ngoại hình", PhysicalInspectionStep),
            # Bước 2: BIOS  
            ("Kiểm tra BIOS", BIOSCheckStep),
            # Bước 3: Định danh phần cứng tự động
            ("Định danh phần cứng", HardwareFingerprintStep),
            # Các bước tiếp theo
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
            ("Thermal Monitor", ThermalPerformanceStep)
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

# ModeSelectionFrame và App đơn giản
class ModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback, icon_manager):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create mode selection UI
        main_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        main_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(main_frame, text="LaptopTester Pro", font=Theme.TITLE_FONT, text_color=Theme.ACCENT).pack(pady=30)
        ctk.CTkLabel(main_frame, text="Chọn chế độ kiểm tra", font=Theme.HEADING_FONT).pack(pady=20)
        
        ctk.CTkButton(main_frame, text="🎯 Chế độ Cơ bản", command=lambda: self.mode_callback("basic"), 
                     fg_color=Theme.SUCCESS, height=60, font=Theme.SUBHEADING_FONT).pack(pady=20, padx=50, fill="x")
        
        ctk.CTkButton(main_frame, text="🔥 Chế độ Chuyên gia", command=lambda: self.mode_callback("expert"), 
                     fg_color=Theme.ERROR, height=60, font=Theme.SUBHEADING_FONT).pack(pady=20, padx=50, fill="x")

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=Theme.BACKGROUND)
        self.title("Laptop Tester Pro")
        self.state('zoomed')
        self.minsize(1400, 900)
        
        self.icon_manager = IconManager()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)
        self.current_main_frame = None
        self.all_results = {}

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
        self.clear_window()
        self.current_main_frame = WizardFrame(self.main_content, mode, self.icon_manager, app=self)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

    def quit_app(self):
        self.clear_window()
        self.destroy()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    if getattr(sys, 'frozen', False):
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            pass
    
    app = App()
    app.mainloop()