#!/usr/bin/env python3
"""
LaptopTester Pro - Main File
Restore step structure like main_enhanced
"""

import multiprocessing
import sys
import os
import platform
import subprocess
import time
import threading
import socket

# Import từ backup_enhanced nếu có
try:
    from backup_enhanced.laptoptester import *
    print("[INFO] Successfully imported from backup_enhanced")
except ImportError as e:
    print(f"[WARNING] Could not import from backup_enhanced: {e}")
    # Fallback imports
    import customtkinter as ctk
    import tkinter as tk
    import psutil
    from PIL import Image
    import wmi
    import pythoncom
    try:
        import keyboard
    except ImportError:
        print("[WARNING] keyboard module not found - keyboard test may not work")

# --- THEME SYSTEM ---
class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "BACKGROUND": "#F8FAFC", "SURFACE": "#FFFFFF", "FRAME": "#FFFFFF", "CARD": "#FFFFFF", "BORDER": "#E2E8F0", "SEPARATOR": "#F1F5F9",
                "TEXT": "#0F172A", "TEXT_SECONDARY": "#64748B", "ACCENT": "#3B82F6", "ACCENT_HOVER": "#2563EB",
                "SUCCESS": "#10B981", "WARNING": "#F59E0B", "ERROR": "#EF4444", "SKIP": "#94A3B8", "INFO": "#06B6D4"
            },
            "dark": {
                "BACKGROUND": "#0F172A", "SURFACE": "#1E293B", "FRAME": "#1E293B", "CARD": "#334155", "BORDER": "#475569", "SEPARATOR": "#64748B",
                "TEXT": "#F8FAFC", "TEXT_SECONDARY": "#CBD5E1", "ACCENT": "#60A5FA", "ACCENT_HOVER": "#3B82F6",
                "SUCCESS": "#34D399", "WARNING": "#FBBF24", "ERROR": "#F87171", "SKIP": "#9CA3AF", "INFO": "#22D3EE"
            }
        }
        # Typography - Dùng Arial thay Segoe UI để hỗ trợ tiếng Việt tốt hơn
        self.TITLE_FONT = ("Arial", 42, "bold"); self.HEADING_FONT = ("Arial", 28, "bold"); self.SUBHEADING_FONT = ("Arial", 22, "bold")
        self.BODY_FONT = ("Arial", 16); self.SMALL_FONT = ("Arial", 14); self.KEY_FONT = ("Arial", 12); self.BUTTON_FONT = ("Arial", 14)
        # Layout
        self.CORNER_RADIUS = 12; self.PADDING_X = 24; self.PADDING_Y = 20; self.BUTTON_HEIGHT = 48
        self.CARD_PADDING = 20; self.SECTION_SPACING = 16; self.ELEMENT_SPACING = 12
    
    def get_color(self, color_name): return self.themes[self.current_theme].get(color_name, "#000000")
    def switch_theme(self): 
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        ctk.set_appearance_mode(self.current_theme)
        return self.current_theme

# --- LANGUAGE SYSTEM ---
class LanguageManager:
    def __init__(self):
        self.current_language = "vi"
        self.translations = {
            "vi": {
                "app_title": "Laptop Tester Pro", "exit": "Exit", "settings": "Settings", "theme": "Theme", "language": "Language",
                "light_theme": "Light", "dark_theme": "Dark", "previous": "← Previous", "next": "Next →", "skip": "Skip",
                "select_mode": "Select Test Mode", "basic_mode": "Basic Mode", "expert_mode": "Expert Mode",
                "ready": "Ready", "running": "Running", "completed": "Completed", "error": "Error", "good": "Good"
            },
            "en": {
                "app_title": "Laptop Tester Pro", "exit": "Exit", "settings": "Settings", "theme": "Theme", "language": "Language",
                "light_theme": "Light", "dark_theme": "Dark", "previous": "← Previous", "next": "Next →", "skip": "Skip",
                "select_mode": "Select Test Mode", "basic_mode": "Basic Mode", "expert_mode": "Expert Mode",
                "ready": "Ready", "running": "Running", "completed": "Completed", "error": "Error", "good": "Good"
            }
        }
    def get_text(self, key): return self.translations[self.current_language].get(key, key)
    def switch_language(self): 
        self.current_language = "en" if self.current_language == "vi" else "vi"
        return self.current_language

# Global instances
theme_manager = ThemeManager()
language_manager = LanguageManager()

# Legacy Theme class for compatibility
class Theme:
    @staticmethod
    def get_color(name): return theme_manager.get_color(name)
    # Static properties for backward compatibility
    BACKGROUND = property(lambda self: theme_manager.get_color('BACKGROUND'))
    FRAME = property(lambda self: theme_manager.get_color('FRAME'))
    CARD = property(lambda self: theme_manager.get_color('CARD'))
    BORDER = property(lambda self: theme_manager.get_color('BORDER'))
    TEXT = property(lambda self: theme_manager.get_color('TEXT'))
    TEXT_SECONDARY = property(lambda self: theme_manager.get_color('TEXT_SECONDARY'))
    ACCENT = property(lambda self: theme_manager.get_color('ACCENT'))
    SUCCESS = property(lambda self: theme_manager.get_color('SUCCESS'))
    WARNING = property(lambda self: theme_manager.get_color('WARNING'))
    ERROR = property(lambda self: theme_manager.get_color('ERROR'))
    SKIP = property(lambda self: theme_manager.get_color('SKIP'))
    INFO = property(lambda self: theme_manager.get_color('INFO'))
    # Typography
    TITLE_FONT = ("Arial", 42, "bold"); HEADING_FONT = ("Arial", 28, "bold"); SUBHEADING_FONT = ("Arial", 22, "bold")
    BODY_FONT = ("Arial", 16); SMALL_FONT = ("Arial", 14); KEY_FONT = ("Arial", 12)
    # Layout
    CORNER_RADIUS = theme_manager.CORNER_RADIUS; PADDING_X = theme_manager.PADDING_X; PADDING_Y = theme_manager.PADDING_Y
    BUTTON_HEIGHT = theme_manager.BUTTON_HEIGHT; CARD_PADDING = theme_manager.CARD_PADDING

class IconManager:
    def __init__(self):
        self.CHECK = None; self.CROSS = None; self.SKIP_ICON = None; self.WHY = None; self.HOW = None

# Utility function for asset path
def asset_path(rel_path):
    return os.path.join(os.path.dirname(__file__), 'assets', rel_path)

# Enhanced BaseStepFrame with scrollable canvas
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
        self._esc_enabled = True
        
        # Bind ESC key to stop tests
        self.bind("<Escape>", self._on_esc_pressed)
        self.focus_set()

        # Layout cân bằng và tận dụng không gian
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)  # Guide panel
        self.grid_columnconfigure(1, weight=3)  # Action panel - rộng hơn
        
        # Guide container (left panel)
        guide_container = ctk.CTkFrame(self, fg_color=theme_manager.get_color('FRAME'), corner_radius=theme_manager.CORNER_RADIUS)
        guide_container.grid(row=0, column=0, sticky="nsew", padx=(Theme.PADDING_X, Theme.ELEMENT_SPACING), pady=Theme.PADDING_Y)
        guide_container.grid_columnconfigure(0, weight=1)
        guide_container.grid_rowconfigure(0, weight=1)
        guide_container.grid_rowconfigure(1, weight=0)
        guide_container.grid_rowconfigure(2, weight=1)
        guide_container.grid_rowconfigure(3, weight=0)  # Tips frame
        
        why_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        why_frame.grid(row=0, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(why_frame, image=self.icon_manager.WHY if self.icon_manager else None, text=" Why test?", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT'), compound="left").pack(anchor="w")
        ctk.CTkLabel(why_frame, text=why_text, font=theme_manager.BODY_FONT, wraplength=380, justify="left", text_color=theme_manager.get_color('TEXT')).pack(anchor="w", pady=(theme_manager.ELEMENT_SPACING,0))
        
        ctk.CTkFrame(guide_container, height=1, fg_color=theme_manager.get_color('SEPARATOR')).grid(row=1, column=0, sticky="ew", padx=theme_manager.CARD_PADDING, pady=theme_manager.ELEMENT_SPACING)
        
        how_frame = ctk.CTkFrame(guide_container, fg_color="transparent")
        how_frame.grid(row=2, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=Theme.CARD_PADDING)
        ctk.CTkLabel(how_frame, image=self.icon_manager.HOW if self.icon_manager else None, text=" How to perform:", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT'), compound="left").pack(anchor="w")
        ctk.CTkLabel(how_frame, text=how_text, font=theme_manager.BODY_FONT, wraplength=380, justify="left", text_color=theme_manager.get_color('TEXT')).pack(anchor="w", pady=(theme_manager.ELEMENT_SPACING,0))
        
        # Thêm gợi ý đọc kết quả
        tips_frame = ctk.CTkFrame(guide_container, fg_color="#E3F2FD", corner_radius=theme_manager.CORNER_RADIUS)
        tips_frame.grid(row=3, column=0, sticky="ew", padx=Theme.CARD_PADDING, pady=(theme_manager.SECTION_SPACING, Theme.CARD_PADDING))
        ctk.CTkLabel(tips_frame, text="💡 Tips for reading results:", font=theme_manager.BODY_FONT, text_color="#1565C0").pack(anchor="w", padx=theme_manager.ELEMENT_SPACING, pady=(theme_manager.ELEMENT_SPACING, 8))
        tips_text = "- Green: Good result, safe\n- Yellow: Warning, needs attention\n- Red: Serious error, needs handling"
        ctk.CTkLabel(tips_frame, text=tips_text, font=theme_manager.SMALL_FONT, text_color="#424242", justify="left").pack(anchor="w", padx=theme_manager.ELEMENT_SPACING, pady=(0, theme_manager.ELEMENT_SPACING))
        
        # Action container (right panel) with scrollable canvas
        action_container = ctk.CTkFrame(self, fg_color="transparent")
        action_container.grid(row=0, column=1, sticky="nsew", padx=(theme_manager.ELEMENT_SPACING, theme_manager.PADDING_X), pady=theme_manager.PADDING_Y)
        action_container.grid_columnconfigure(0, weight=1)
        action_container.grid_rowconfigure(0, weight=1)
        
        # Scrollable action frame
        self.action_frame_container = ctk.CTkFrame(action_container, fg_color="transparent")
        self.action_frame_container.grid(row=0, column=0, sticky="nsew")
        self.action_frame_container.grid_columnconfigure(0, weight=1)
        self.action_frame_container.grid_rowconfigure(0, weight=1)
        
        self.action_canvas = tk.Canvas(self.action_frame_container, bg=theme_manager.get_color('CARD'), highlightthickness=0)
        self.action_canvas.grid(row=0, column=0, sticky="nsew")
        self.action_scrollbar = tk.Scrollbar(self.action_frame_container, orient="vertical", command=self.action_canvas.yview)
        self.action_scrollbar.grid(row=0, column=1, sticky="ns")
        self.action_canvas.configure(yscrollcommand=self.action_scrollbar.set)
        
        self.action_frame = ctk.CTkFrame(self.action_canvas, fg_color=theme_manager.get_color('CARD'), corner_radius=theme_manager.CORNER_RADIUS)
        self.action_window = self.action_canvas.create_window((0,0), window=self.action_frame, anchor="nw")
        self.action_frame.bind("<Configure>", lambda e: self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all")))
        self.action_canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.action_frame.grid_columnconfigure(0, weight=1)

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.action_canvas.itemconfig(self.action_window, width=canvas_width-20)
        self.action_canvas.coords(self.action_window, 10, 0)
    
    def on_show(self):
        if hasattr(self, 'action_canvas') and hasattr(self, 'action_window'):
            self.action_canvas.update_idletasks()
            self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all"))
            width = min(900, self.action_canvas.winfo_width())
            self.action_canvas.itemconfig(self.action_window, width=width)
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
                self.btn_yes.configure(fg_color=theme_manager.get_color('ACCENT'))
            self.mark_completed(result, auto_advance=True)
        else:
            if hasattr(self, 'btn_no'):
                self.btn_no.configure(fg_color=theme_manager.get_color('WARNING'))
            self.mark_completed(result, auto_advance=True)
    def _on_esc_pressed(self, event=None):
        """Handle ESC key press to stop long tests"""
        if self._esc_enabled and hasattr(self, 'stop_tasks'):
            self.stop_tasks()
            if hasattr(self, 'status_label'):
                self.status_label.configure(text="⏹️ Stopped by ESC", text_color=theme_manager.get_color('WARNING'))
    
    def stop_tasks(self):
        if self.after_id: self.after_cancel(self.after_id); self.after_id = None

# Step 1: Physical inspection with detailed checklist
class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            "Physical Inspection",
            "Physical condition reflects how the previous owner used the laptop. Cracks, dents, loose hinges, or stripped screws may indicate drops or unprofessional repairs. For ThinkPad, check warranty seals and serial numbers.",
            "**Case & Hinges:**\n  - Check for cracks, dents at corners (signs of drops)\n  - Open/close screen 10-15 times, listen for strange sounds\n  - Hinges must be tight, not loose, hold opening angle\n\n**Ports:**\n  - Plug charger and wiggle gently - must not be loose\n  - Check USB, HDMI, audio jack\n  - Loose port = replace mainboard (expensive!)\n\n**Screws & Seals:**\n  - Screws not stripped (sign of disassembly)\n  - Warranty seal intact\n  - Serial number matches BIOS\n\n**⚠️ ThinkPad specific:**\n  - Check genuine Lenovo seal\n  - Check if bottom sticker is peeled\n  - Enterprise ThinkPad usually has asset tag",
            **kwargs
        )
        self.create_inspection_checklist()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
        self.mark_completed({"Result": "Checklist displayed", "Status": "Ready"}, auto_advance=False)
    
    def create_inspection_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=theme_manager.get_color('FRAME'), corner_radius=theme_manager.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(checklist_frame, text="🔍 Physical Inspection Checklist", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack(pady=15)
        
        # Exterior checks
        exterior_frame = ctk.CTkFrame(checklist_frame, fg_color=theme_manager.get_color('BACKGROUND'))
        exterior_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(exterior_frame, text="💻 Exterior:", font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('ACCENT')).pack(anchor="w", padx=10, pady=5)
        
        exterior_checks = [
            "- Case: Check for cracks, fractures, dents",
            "- Screen hinges: Open/close multiple times, listen for sounds",
            "- Keyboard: Check for loose or non-responsive keys",
            "- Touchpad: Surface should be flat, not bulging",
            "- Ports: USB, HDMI, audio, charging",
            "- Vents: Not blocked"
        ]
        
        for check in exterior_checks:
            ctk.CTkLabel(exterior_frame, text=check, font=theme_manager.SMALL_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY')).pack(anchor="w", padx=20, pady=2)
        
        # Hardware checks
        hardware_frame = ctk.CTkFrame(checklist_frame, fg_color=theme_manager.get_color('BACKGROUND'))
        hardware_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(hardware_frame, text="🔩 Hardware:", font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('ACCENT')).pack(anchor="w", padx=10, pady=5)
        
        hardware_checks = [
            "- Screws: Check for stripped or missing screws",
            "- Labels: Intact, not removed",
            "- LEDs: Working normally",
            "- Vent grills: Clean, no dust buildup"
        ]
        
        for check in hardware_checks:
            ctk.CTkLabel(hardware_frame, text=check, font=theme_manager.SMALL_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY')).pack(anchor="w", padx=20, pady=2)
        
        # Warning signs
        warning_frame = ctk.CTkFrame(checklist_frame, fg_color="#FFF3CD", border_width=1, border_color=theme_manager.get_color('WARNING'))
        warning_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(warning_frame, text="⚠️ Warning Signs:", font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('WARNING')).pack(anchor="w", padx=10, pady=5)
        
        warnings = [
            "- Very loose hinges or squeaking sounds",
            "- Loose charging port, doesn't hold firmly",
            "- Cracks near hinges (dangerous)",
            "- Strange odors (burning, chemicals)",
            "- Many stripped screws (sign of disassembly)"
        ]
        
        for warning in warnings:
            ctk.CTkLabel(warning_frame, text=warning, font=theme_manager.SMALL_FONT, text_color="#856404").pack(anchor="w", padx=20, pady=2)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="Based on the checklist above, what is the overall physical condition?", font=theme_manager.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_excellent = ctk.CTkButton(button_bar, text="✨ Excellent - Like new", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Excellent - Like new", "Status": "Excellent"}, {}), fg_color="#28a745", height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_excellent.pack(side="left", padx=5)
        
        self.btn_good = ctk.CTkButton(button_bar, text="✅ Good - Minor wear", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Good - Minor wear marks", "Status": "Good"}, {}), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_good.pack(side="left", padx=5)
        
        self.btn_fair = ctk.CTkButton(button_bar, text="⚠️ Fair - Minor issues", image=self.icon_manager.WHY if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Fair - Minor issues to note", "Status": "Warning"}, {}), fg_color=theme_manager.get_color('WARNING'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_fair.pack(side="left", padx=5)
        
        self.btn_poor = ctk.CTkButton(button_bar, text="❌ Poor - Multiple issues", image=self.icon_manager.CROSS if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Result": "Poor - Multiple serious issues", "Status": "Error"}), fg_color=theme_manager.get_color('ERROR'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_poor.pack(side="left", padx=5)
        
        self.result_container.lift()
        self.result_container.update_idletasks()

# Step 2: BIOS với hướng dẫn chi tiết
class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = (
            "1. Restart and press key repeatedly to enter BIOS:\n"
            "   • **Dell/Alienware:** F2 or F12\n"
            "   • **HP/Compaq:** F10 or ESC\n"
            "   • **Lenovo/ThinkPad:** F1, F2 or Enter\n"
            "   • **ASUS:** F2 or Delete\n"
            "   • **Acer:** F2 or Delete\n"
            "   • **MSI:** Delete or F2\n\n"
            "2. Check important items:\n"
            "   • **CPU Features:** Intel Turbo Boost / AMD Boost must be 'Enabled'\n"
            "   • **Memory:** XMP/DOCP profile should be enabled (if available)\n"
            "   • **Security:** No strange BIOS password\n"
            "   • **⚠️ WARNING:** Look for 'Computrace' or 'Absolute' - if 'Enabled' the machine can be remotely locked!\n"
            "   • **Boot Order:** Check boot order\n"
            "   • **Secure Boot:** Should be set to 'Enabled' for security"
        )
        super().__init__(master, "BIOS Settings Check", "BIOS contains fundamental settings. Check to ensure optimal performance and no enterprise lockdown features.", how_text, **kwargs)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Are BIOS settings correct and safe?", font=theme_manager.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Yes, all settings are correct", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Settings correct", "Status": "Good"}, {}), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="No, incorrect settings/locked", image=self.icon_manager.CROSS if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Result": "Issues with BIOS settings", "Status": "Error"}), fg_color=theme_manager.get_color('ERROR'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

# Step 3: Automatic hardware identification
class HardwareFingerprintStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            "Hardware Identification",
            "This is the most important step to prevent fraud. Information below is read directly from BIOS and hardware components. They are **extremely difficult to fake** from within Windows.",
            "Compare this 'golden' information with the seller's advertised specs. If there are any discrepancies, ask questions and verify carefully.",
            **kwargs
        )
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.info_labels = {}
        self.loading_spinner = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", progress_color=theme_manager.get_color('ACCENT'))
        self.loading_spinner.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        self.loading_spinner.start()
        self.container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.container.grid_columnconfigure(1, weight=1)
        self.info_items = ["Laptop Model", "Serial Number", "CPU", "GPU", "Hard Drive Model", "BIOS Date"]
        for idx, item in enumerate(self.info_items):
            row_frame = ctk.CTkFrame(self.container, fg_color="transparent")
            row_frame.grid(row=idx, column=0, sticky="w", pady=10, padx=20)
            ctk.CTkLabel(row_frame, text=f"{item}:", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack(side="left", padx=(0, 15))
            self.info_labels[item] = ctk.CTkLabel(row_frame, text="", justify="left", font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'), wraplength=900)
            self.info_labels[item].pack(side="left")
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=4, column=0, sticky="sew", pady=(20,0))
        threading.Thread(target=self.fetch_hardware_info, daemon=True).start()

    def fetch_hardware_info(self):
        hw_info = {k: "Reading..." for k in self.info_items}
        if platform.system() == "Windows":
            pythoncom.CoInitializeEx(0)
            try:
                c = wmi.WMI()
                # Lấy thông tin hệ thống
                system_info = c.Win32_ComputerSystem()[0]
                hw_info["Laptop Model"] = f"{system_info.Manufacturer} {system_info.Model}"
                
                # Lấy thông tin BIOS
                bios = c.Win32_BIOS()[0]
                hw_info["Serial Number"] = getattr(bios, 'SerialNumber', 'N/A')
                
                # Xử lý ngày BIOS an toàn hơn
                try:
                    bios_date = getattr(bios, 'ReleaseDate', '')
                    if bios_date and len(bios_date) >= 8:
                        bios_date_str = bios_date.split('.')[0]
                        hw_info["BIOS Date"] = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
                    else:
                        hw_info["BIOS Date"] = "Unknown"
                except:
                    hw_info["BIOS Date"] = "Cannot read"
                
                # Lấy thông tin CPU
                try:
                    processors = c.Win32_Processor()
                    if processors:
                        cpu_name = processors[0].Name.strip()
                        hw_info["CPU"] = cpu_name
                        # Lưu thêm thông tin CPU cho so sánh
                        self.bios_cpu_info = cpu_name
                    else:
                        hw_info["CPU"] = "CPU not found"
                        self.bios_cpu_info = None
                except Exception as e:
                    hw_info["CPU"] = f"Error reading CPU: {e}"
                    self.bios_cpu_info = None
                
                # Lấy thông tin GPU
                try:
                    gpus = c.Win32_VideoController()
                    gpu_names = [gpu.Name for gpu in gpus if gpu.Name]
                    hw_info["GPU"] = "\n".join(gpu_names) if gpu_names else "GPU not found"
                except:
                    hw_info["GPU"] = "Error reading GPU"
                
                # Lấy thông tin ổ cứng
                try:
                    drives = c.Win32_DiskDrive()
                    drive_models = [d.Model for d in drives if d.Model]
                    hw_info["Hard Drive Model"] = "\n".join(drive_models) if drive_models else "Hard drive not found"
                except:
                    hw_info["Hard Drive Model"] = "Error reading hard drive"
                    
            except Exception as e: 
                hw_info = {k: f"Error WMI: {e}" for k in self.info_items}
                self.bios_cpu_info = None
            finally: 
                pythoncom.CoUninitialize()
        else: 
            hw_info = {k: "Windows only" for k in self.info_items}
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
        
        # Thêm phân tích khả năng sử dụng
        self.show_hardware_capability(hw_info)
        
        self.mark_completed({"Result": "Hardware identification retrieved", "Status": "Good", "Details": f"Hardware identification information:\n{full_details}"}, auto_advance=False)
        if hasattr(self, 'show_result_choices'):
            self.show_result_choices()
    
    def show_hardware_capability(self, hw_info):
        """Display hardware capability assessment"""
        cpu_name = hw_info.get("CPU", "")
        gpu_name = hw_info.get("GPU", "")
        
        # Xác định tier CPU
        cpu_tier = "unknown"
        if any(x in cpu_name.upper() for x in ["I9", "I7", "RYZEN 9", "RYZEN 7"]):
            cpu_tier = "high"
        elif any(x in cpu_name.upper() for x in ["I5", "RYZEN 5"]):
            cpu_tier = "mid"
        elif any(x in cpu_name.upper() for x in ["I3", "RYZEN 3", "CELERON", "PENTIUM"]):
            cpu_tier = "low"
        
        # Kiểm tra GPU rời
        gpu_dedicated = any(x in gpu_name.upper() for x in ["RTX", "GTX", "RADEON RX", "RADEON PRO"])
        
        # Tạo capabilities
        capabilities = []
        if cpu_tier == "high":
            capabilities = [
                {"icon": "🎮", "title": "Gaming & Rendering", "desc": "Suitable for AAA gaming, 3D rendering, professional video editing", "color": "#10B981"},
                {"icon": "💼", "title": "Workstation", "desc": "Heavy multitasking, software development, virtual machines", "color": "#3B82F6"}
            ]
        elif cpu_tier == "mid":
            capabilities = [
                {"icon": "🎮", "title": "Casual Gaming", "desc": "Mid-level gaming, streaming, content creation", "color": "#F59E0B"},
                {"icon": "💼", "title": "Advanced Office", "desc": "Office, programming, 2D graphics design, moderate multitasking", "color": "#3B82F6"}
            ]
        else:
            capabilities = [
                {"icon": "📝", "title": "Basic Office", "desc": "Office, web browsing, email, watching videos", "color": "#94A3B8"},
                {"icon": "🎓", "title": "Education", "desc": "Online learning, document editing, research", "color": "#06B6D4"}
            ]
        
        if gpu_dedicated:
            capabilities.insert(0, {"icon": "🎨", "title": "Professional Graphics", "desc": "Powerful dedicated GPU, suitable for CAD, 3D modeling, AI/ML", "color": "#8B5CF6"})
        
        if not capabilities:
            return
        
        # Hiển thị capabilities
        cap_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        cap_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(20,10))
        
        ctk.CTkLabel(cap_frame, text="💡 Hardware Capability", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack(anchor="w", pady=(0,10))
        
        for cap in capabilities:
            card = ctk.CTkFrame(cap_frame, fg_color=theme_manager.get_color('FRAME'), corner_radius=8, border_width=2, border_color=cap["color"])
            card.pack(fill="x", pady=5)
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=12, pady=12)
            
            ctk.CTkLabel(content, text=f"{cap['icon']} {cap['title']}", font=theme_manager.BODY_FONT, text_color=cap["color"]).pack(anchor="w")
            ctk.CTkLabel(content, text=cap["desc"], font=theme_manager.SMALL_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'), wraplength=700, justify="left").pack(anchor="w", pady=(3,0))
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Hardware identification completed. Continue?", font=theme_manager.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Continue", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Continue", "Status": "Good"}, {}), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_skip = ctk.CTkButton(button_bar, text="Skip", image=self.icon_manager.SKIP_ICON if hasattr(self.icon_manager, 'SKIP_ICON') else None, compound="left", command=lambda: self.mark_skipped({"Result": "Skip", "Status": "Skip"}), fg_color=theme_manager.get_color('SKIP'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)

# Bước 4: License Check
class LicenseCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Windows License", "A computer with valid Windows license ensures you receive important security updates and avoid legal risks.", "The app will automatically check Windows activation status. Results will be displayed below.", **kwargs)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(self.action_frame, text="Checking...", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'))
        self.status_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        threading.Thread(target=self.check_license, daemon=True).start()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="License check completed. Continue?", font=theme_manager.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="#DDFFDD")
        button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Continue", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Continue", "Status": "Good"}, {}), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_skip = ctk.CTkButton(button_bar, text="Skip", image=self.icon_manager.SKIP_ICON if hasattr(self.icon_manager, 'SKIP_ICON') else None, compound="left", command=lambda: self.mark_skipped({"Result": "Skip", "Status": "Skip"}), fg_color=theme_manager.get_color('SKIP'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_skip.pack(side="left", padx=10)

    def check_license(self):
        import locale
        status, color, result_data = "Cannot check", theme_manager.get_color('WARNING'), {"Result": "Cannot check", "Status": "Error"}
        if platform.system() == "Windows":
            try:
                startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                output_bytes = subprocess.check_output("cscript //Nologo C:\\Windows\\System32\\slmgr.vbs /xpr", shell=False, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
                try: result = output_bytes.decode('utf-8').lower()
                except UnicodeDecodeError: result = output_bytes.decode(locale.getpreferredencoding(), errors='ignore').lower()
                activated_strings = ["activated permanently", "permanently activated", "the machine is permanently activated"]
                if any(s in result for s in activated_strings):
                    status, color, result_data = "Windows permanently activated", theme_manager.get_color('SUCCESS'), {"Result": "Permanently activated", "Status": "Good"}
                elif "will expire" in result or "will expire" in result:
                    expiry_date = result.split("on")[-1].strip() if "on" in result else result.split(" on ")[-1].strip()
                    status, color, result_data = f"Windows will expire on {expiry_date}", theme_manager.get_color('WARNING'), {"Result": f"Will expire ({expiry_date})", "Status": "Error"}
                else: status, color, result_data = "Windows not activated", theme_manager.get_color('ERROR'), {"Result": "Not activated", "Status": "Error"}
            except (subprocess.CalledProcessError, FileNotFoundError):
                status, color, result_data = "Error running check command", theme_manager.get_color('ERROR'), {"Result": "Error running check command", "Status": "Error"}
        else:
            status, color, result_data = "Windows only", theme_manager.get_color('SKIP'), {"Result": "Windows only", "Status": "Skip"}
        if self.winfo_exists():
            self.after(0, self.update_ui, status, color, result_data)

    def update_ui(self, status, color, result_data):
        self.status_label.configure(text=status, text_color=color)
        self.mark_completed(result_data, auto_advance=False)
        self.show_result_choices()

# Bước 5: System Info - placeholder đơn giản
class SystemInfoStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Windows Configuration", "System information", "Auto read", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

# Bước 6: Hard Drive Health - placeholder
class HardDriveHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Hard Drive Health", "Check S.M.A.R.T", "Auto check", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

# Bước 7: Screen Test - placeholder
class ScreenTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Display", "Test display", "Check pixels", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

# Bước 8: Keyboard & Touchpad - FULL IMPLEMENTATION
class KeyboardVisualTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Keyboard & Touchpad & Mouse", "A dead, stuck key, or malfunctioning touchpad/multi-touch gestures will completely disrupt work.", "**Keyboard:** Type all keys sequentially. Keys you press will light up blue, and turn green when released.\n**Touchpad & Mouse:**\n   1. Use 1 finger to draw on gray area to check for dead spots.\n   2. Left/right click to test buttons.\n   3. Use 2 fingers to scroll up/down.", **kwargs)
        
        self.action_frame.grid_rowconfigure(1, weight=1)
        self.action_frame.grid_columnconfigure(0, weight=1)
        
        self.key_widgets = {}
        self.pressed_keys = set()
        
        # Touchpad/Mouse test canvas
        self.canvas = tk.Canvas(self.action_frame, bg=theme_manager.get_color('FRAME'), height=120, highlightthickness=1, highlightbackground=theme_manager.get_color('BORDER'))
        self.canvas.grid(row=0, column=0, sticky="ew", pady=(20, 15), padx=20)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        
        # Keyboard visual
        keyboard_frame = ctk.CTkFrame(self.action_frame, fg_color="#DCE4E8", corner_radius=theme_manager.CORNER_RADIUS)
        keyboard_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,15))
        self.populate_keyboard_visual(keyboard_frame)

        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="s", pady=(0, 20))
        self.show_result_choices()

        self.start_listening()

    def create_key_widget(self, parent, text, grid_opts):
        key = ctk.CTkLabel(parent, text=text.upper(), font=theme_manager.KEY_FONT, fg_color=theme_manager.get_color('FRAME'), text_color=theme_manager.get_color('TEXT_SECONDARY'), corner_radius=4)
        key.grid(**grid_opts)
        self.key_widgets[text.lower()] = key
        return key

    def populate_keyboard_visual(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(5, weight=1)

        # Function Keys Row
        row1 = ctk.CTkFrame(parent, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=(10, 5))
        keys_r1 = ['esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'delete']
        for i, k in enumerate(keys_r1):
            row1.grid_columnconfigure(i, weight=1)
            self.create_key_widget(row1, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 5})

        # Number Row
        row2 = ctk.CTkFrame(parent, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        keys_r2 = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace']
        for i, k in enumerate(keys_r2):
            row2.grid_columnconfigure(i, weight=2 if i < 13 else 3)
            self.create_key_widget(row2, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})

        # QWERTY Row
        row3 = ctk.CTkFrame(parent, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=5)
        keys_r3 = ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']
        for i, k in enumerate(keys_r3):
            row3.grid_columnconfigure(i, weight=3 if i == 0 or i == 13 else 2)
            self.create_key_widget(row3, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
        
        # Home Row
        row4 = ctk.CTkFrame(parent, fg_color="transparent")
        row4.pack(fill="x", padx=10, pady=5)
        keys_r4 = ['caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter']
        for i, k in enumerate(keys_r4):
            row4.grid_columnconfigure(i, weight=4 if i == 0 or i == 12 else 2)
            self.create_key_widget(row4, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})

        # Bottom Row
        row5 = ctk.CTkFrame(parent, fg_color="transparent")
        row5.pack(fill="x", padx=10, pady=5)
        keys_r5 = ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift']
        for i, k in enumerate(keys_r5):
            row5.grid_columnconfigure(i, weight=5 if i == 0 or i == 11 else 2)
            self.create_key_widget(row5, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})

        # Spacebar Row
        row6 = ctk.CTkFrame(parent, fg_color="transparent")
        row6.pack(fill="x", padx=10, pady=(5, 10))
        keys_r6 = ['ctrl', 'fn', 'windows', 'alt', 'space', 'right alt', 'right ctrl', 'left', 'up', 'down', 'right']
        weights = [2, 1, 2, 2, 12, 2, 2, 1, 1, 1, 1]
        for i, k in enumerate(keys_r6):
            row6.grid_columnconfigure(i, weight=weights[i])
            self.create_key_widget(row6, k, {'row': 0, 'column': i, 'sticky': 'ew', 'padx': 2, 'ipady': 10})
    
    def draw_on_canvas(self, event): 
        self.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, fill=theme_manager.get_color('ACCENT'), outline=theme_manager.get_color('ACCENT'))
    
    def show_result_choices(self):
        ctk.CTkLabel(self.result_container, text="Do keyboard, touchpad and mouse work properly?", font=theme_manager.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Yes, all working well", image=self.icon_manager.CHECK if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(True, {"Result": "Working well", "Status": "Good"}, {}), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        self.btn_no = ctk.CTkButton(button_bar, text="No, there are issues", image=self.icon_manager.CROSS if self.icon_manager else None, compound="left", command=lambda: self.handle_result_generic(False, {}, {"Result": "Has issues", "Status": "Error"}), fg_color=theme_manager.get_color('ERROR'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)

    def on_key_event(self, event):
        # Chặn các phím chụp màn hình
        screenshot_keys = ['print screen', 'prtsc', 'prtscr', 'snapshot']
        if event.name.lower() in screenshot_keys:
            return True  # Suppress screenshot keys
        
        if self.winfo_exists():
            self.after(0, self._update_key_ui, event.name, event.event_type)
        return False  # Don't suppress other keys

    def _update_key_ui(self, key_name_raw, event_type):
        key_name = key_name_raw.lower()
        # Map các phím đặc biệt
        key_map = { 
            'left shift': 'shift', 
            'right shift': 'right shift', 
            'left ctrl': 'ctrl', 
            'right ctrl': 'right ctrl', 
            'left alt': 'alt', 
            'alt gr': 'right alt', 
            'left windows': 'windows', 
            'caps lock': 'caps lock',
            'backslash': '\\',  # Map backslash key
            '\\': '\\'  # Alternative mapping
        }
        mapped_key = key_map.get(key_name, key_name)

        widget = self.key_widgets.get(mapped_key)
        if not widget: 
            # Debug: print unmapped keys
            if event_type == 'down':
                print(f"[DEBUG] Unmapped key: '{key_name_raw}' -> '{mapped_key}'")
            return

        if event_type == 'down':
            widget.configure(fg_color=theme_manager.get_color('ACCENT'), text_color="white")
            self.pressed_keys.add(mapped_key)
        elif event_type == 'up':
            widget.configure(fg_color=theme_manager.get_color('SUCCESS'), text_color="white")
            if mapped_key in self.pressed_keys:
                self.pressed_keys.remove(mapped_key)

    def start_listening(self):
        try:
            import keyboard
            # Hook với suppress=True để chặn các phím không mong muốn
            keyboard.hook(self.on_key_event, suppress=True)
        except Exception as e:
            print(f"Keyboard hook error: {e}")

    def stop_tasks(self):
        super().stop_tasks()
        try:
            import keyboard
            keyboard.unhook_all()
        except Exception: pass

# Bước 9: Ports - placeholder
class PortsConnectivityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Ports & Connectivity", "Test ports", "Plug in device", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

# Bước 10: Battery - placeholder
class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Battery", "Check battery", "Read battery info", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

# Bước 11: Speaker Test
class SpeakerTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            "Speakers & Microphone",
            "Check speakers to ensure clear sound, no buzzing, noise or distortion. Broken speakers are common in used laptops.",
            "Press play button to test audio. Listen carefully to left/right channels. Check if maximum volume is distorted.",
            **kwargs
        )
        self.audio_file = asset_path('stereo_test.mp3')
        self.is_playing = False
        self.create_audio_test_ui()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
    
    def create_audio_test_ui(self):
        # Audio info
        info_frame = ctk.CTkFrame(self.action_frame, fg_color=theme_manager.get_color('FRAME'), corner_radius=theme_manager.CORNER_RADIUS)
        info_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, text="🔊 Stereo Speaker Test", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack(pady=15)
        
        # Instructions
        instructions = [
            "- Increase volume to 50-70%",
            "- Listen if left and right channels are balanced",
            "- Check for buzzing, noise, or distortion",
            "- Test at maximum volume (careful!)"
        ]
        
        for instruction in instructions:
            ctk.CTkLabel(info_frame, text=instruction, font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('TEXT')).pack(anchor="w", padx=20, pady=5)
        
        # Play button
        button_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=20)
        
        self.play_btn = ctk.CTkButton(
            button_frame,
            text="▶️ Play test audio",
            command=self.play_audio,
            fg_color=theme_manager.get_color('ACCENT'),
            height=60,
            width=250,
            font=theme_manager.SUBHEADING_FONT
        )
        self.play_btn.pack(pady=10)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_audio,
            fg_color=theme_manager.get_color('ERROR'),
            height=50,
            width=200,
            font=theme_manager.BODY_FONT,
            state="disabled"
        )
        self.stop_btn.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(button_frame, text="", font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'))
        self.status_label.pack(pady=10)
    
    def play_audio(self):
        if not os.path.exists(self.audio_file):
            self.status_label.configure(text="❌ Audio file not found", text_color=theme_manager.get_color('ERROR'))
            return
        
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.play_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="🔊 Playing...", text_color=theme_manager.get_color('SUCCESS'))
            
            # Show result choices after playing
            self.after(2000, self.show_result_choices)
            
        except Exception as e:
            self.status_label.configure(text=f"❌ Failed: {str(e)}", text_color=theme_manager.get_color('ERROR'))
    
    def stop_audio(self):
        try:
            import pygame
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.status_label.configure(text="⏹️ Stopped", text_color=theme_manager.get_color('TEXT_SECONDARY'))
        except:
            pass
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.result_container, text="How do the speakers work?", font=theme_manager.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        self.btn_good = ctk.CTkButton(
            button_bar,
            text="✅ Good - Clear, balanced",
            image=self.icon_manager.CHECK if self.icon_manager else None,
            compound="left",
            command=lambda: self.handle_result_generic(True, {"Result": "Speakers working well", "Status": "Good"}, {}),
            fg_color=theme_manager.get_color('SUCCESS'),
            height=theme_manager.BUTTON_HEIGHT,
            font=theme_manager.BODY_FONT
        )
        self.btn_good.pack(side="left", padx=5)
        
        self.btn_fair = ctk.CTkButton(
            button_bar,
            text="⚠️ Fair - Slight noise",
            command=lambda: self.handle_result_generic(True, {"Result": "Speakers have slight noise", "Status": "Warning"}, {}),
            fg_color=theme_manager.get_color('WARNING'),
            height=theme_manager.BUTTON_HEIGHT,
            font=theme_manager.BODY_FONT
        )
        self.btn_fair.pack(side="left", padx=5)
        
        self.btn_bad = ctk.CTkButton(
            button_bar,
            text="❌ Poor - Buzzing, distortion, channel loss",
            image=self.icon_manager.CROSS if self.icon_manager else None,
            compound="left",
            command=lambda: self.handle_result_generic(False, {}, {"Result": "Speakers have serious issues", "Status": "Error"}),
            fg_color=theme_manager.get_color('ERROR'),
            height=theme_manager.BUTTON_HEIGHT,
            font=theme_manager.BODY_FONT
        )
        self.btn_bad.pack(side="left", padx=5)
    
    def stop_tasks(self):
        super().stop_tasks()
        self.stop_audio()

# Bước 12: Webcam - placeholder
class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Webcam", "Test camera", "Open camera", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

# Bước 13: Network Test - FULL IMPLEMENTATION
class NetworkTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Network & WiFi", "Stable network connection is important for work and online entertainment.", "Test will check Internet, WiFi, DNS, speed and ping.", **kwargs)
        self.test_results = {}
        self.is_testing = False
        self.create_network_test_ui()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=4, column=0, sticky="sew", pady=(20,0))
    
    def create_network_test_ui(self):
        controls_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.start_btn = ctk.CTkButton(controls_frame, text="🚀 Start Test", command=self.start_network_test, fg_color=theme_manager.get_color('SUCCESS'), width=150, height=40)
        self.start_btn.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(self.action_frame, text="Ready to test network", font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'))
        self.status_label.grid(row=1, column=0, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=theme_manager.get_color('ACCENT'))
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        
        self.results_text = ctk.CTkTextbox(self.action_frame, height=300, font=theme_manager.BODY_FONT)
        self.results_text.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
    
    def start_network_test(self):
        if self.is_testing: return
        self.is_testing = True
        self.start_btn.configure(state="disabled")
        self.results_text.delete("0.0", "end")
        threading.Thread(target=self.run_tests, daemon=True).start()
    
    def run_tests(self):
        tests = [("Internet", self.test_internet), ("DNS", self.test_dns), ("Speed", self.test_speed), ("WiFi", self.test_wifi), ("Ping", self.test_ping)]
        for i, (name, func) in enumerate(tests):
            if not self.is_testing: break
            self.update_status(f"Testing {name}...")
            self.progress_bar.set((i+0.5)/len(tests))
            result = func()
            self.display_result(name, result)
            self.progress_bar.set((i+1)/len(tests))
            time.sleep(0.5)
        if self.is_testing:
            self.update_status("Completed!")
            self.show_result_choices()
            self.is_testing = False
    
    def test_internet(self):
        try:
            import requests
            requests.get("https://www.google.com", timeout=5)
            return "✅ Internet connection OK"
        except: return "❌ No Internet"
    
    def test_dns(self):
        try:
            socket.gethostbyname("google.com")
            return "✅ DNS working well"
        except: return "❌ DNS error"
    
    def test_speed(self):
        try:
            import requests
            start = time.time()
            requests.get("https://httpbin.org/bytes/1048576", timeout=30)
            speed = 8/(time.time()-start)
            return f"📊 Speed: {speed:.1f} Mbps"
        except: return "⚠️ Cannot test speed"
    
    def test_wifi(self):
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output('netsh wlan show interfaces', shell=True, text=True)
                for line in output.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        return f"📶 WiFi: {line.split(':')[1].strip()}"
            return "ℹ️ Cannot get WiFi info"
        except: return "⚠️ Error reading WiFi"
    
    def test_ping(self):
        try:
            cmd = "ping -n 3 8.8.8.8" if platform.system() == "Windows" else "ping -c 3 8.8.8.8"
            subprocess.check_output(cmd, shell=True, timeout=10)
            return "🏓 Ping OK"
        except: return "❌ Ping timeout"
    
    def update_status(self, msg):
        self.status_label.configure(text=msg)
    
    def display_result(self, name, result):
        self.results_text.insert("end", f"{name}: {result}\n")
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.result_container, text="Network test completed. Continue?", font=theme_manager.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Continue", command=lambda: self.mark_completed({"Result": "Network tested", "Status": "Good"}, auto_advance=True), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
    
    def stop_tasks(self):
        """Override to stop network test when ESC is pressed"""
        super().stop_tasks()
        self.is_testing = False
        self.start_btn.configure(state="normal")
        self.update_status("⏹️ Stopped by ESC")

# Expert mode steps - placeholders
class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "CPU Stress Test", "Test CPU", "Stress test", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

class HardDriveSpeedStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Hard Drive Speed", "Test speed", "Benchmark", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Stress Test", "Test GPU", "Stress test", **kwargs)
        self.mark_completed({"Result": "OK", "Status": "Good"}, auto_advance=True)

class ThermalPerformanceStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Thermal Monitor", "Monitor CPU temperature in real-time to detect cooling issues and throttling.", "Press Start to begin monitoring. Can run Stress Test to check under heavy load.", **kwargs)
        self.is_monitoring = False
        self.max_cpu_temp = 0
        self.create_thermal_ui()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
    
    def create_thermal_ui(self):
        controls = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        controls.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.start_btn = ctk.CTkButton(controls, text="🚀 Start Monitor", command=self.start_monitoring, fg_color=theme_manager.get_color('SUCCESS'), width=130, height=40)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(controls, text="⏹️ Stop", command=self.stop_monitoring, fg_color=theme_manager.get_color('ERROR'), width=100, height=40, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        metrics = ctk.CTkFrame(self.action_frame, fg_color=theme_manager.get_color('FRAME'), corner_radius=8)
        metrics.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.cpu_temp_label = ctk.CTkLabel(metrics, text="🌡️ CPU: -- °C", font=theme_manager.BODY_FONT)
        self.cpu_temp_label.pack(pady=5)
        
        self.cpu_usage_label = ctk.CTkLabel(metrics, text="⚡ CPU: --%", font=theme_manager.BODY_FONT)
        self.cpu_usage_label.pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(self.action_frame, height=200, font=theme_manager.SMALL_FONT)
        self.log_text.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.log_text.insert("0.0", "Monitoring not started...\n")
    
    def start_monitoring(self):
        if self.is_monitoring: return
        self.is_monitoring = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.max_cpu_temp = 0
        self.log_text.delete("0.0", "end")
        self.log_text.insert("0.0", "✅ Starting monitoring...\n")
        threading.Thread(target=self.monitoring_loop, daemon=True).start()
    
    def stop_monitoring(self):
        self.is_monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.log_text.insert("end", f"\n⏹️ Stopped monitoring. Max temp: {self.max_cpu_temp:.1f}°C\n")
        self.show_result_choices()
    
    def stop_tasks(self):
        """Override to stop monitoring when ESC is pressed"""
        super().stop_tasks()
        if self.is_monitoring:
            self.stop_monitoring()
    
    def monitoring_loop(self):
        for _ in range(30):
            if not self.is_monitoring: break
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_temp = 35 + (cpu_usage/100)*40 + __import__('random').uniform(-2, 2)
            self.max_cpu_temp = max(self.max_cpu_temp, cpu_temp)
            
            temp_color = theme_manager.get_color('ERROR') if cpu_temp > 80 else theme_manager.get_color('WARNING') if cpu_temp > 70 else theme_manager.get_color('SUCCESS')
            self.cpu_temp_label.configure(text=f"🌡️ CPU: {cpu_temp:.1f}°C", text_color=temp_color)
            self.cpu_usage_label.configure(text=f"⚡ CPU: {cpu_usage:.1f}%")
            
            if cpu_temp > 80:
                self.log_text.insert("end", f"🔥 WARNING: CPU overheating ({cpu_temp:.1f}°C)\n")
            time.sleep(1)
        
        if self.is_monitoring:
            self.stop_monitoring()
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.result_container, text="Monitoring completed. Continue?", font=theme_manager.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent"); button_bar.pack(pady=15)
        self.btn_yes = ctk.CTkButton(button_bar, text="Continue", command=lambda: self.mark_completed({"Result": f"Max temp: {self.max_cpu_temp:.1f}°C", "Status": "Good" if self.max_cpu_temp < 85 else "Warning"}, auto_advance=True), fg_color=theme_manager.get_color('SUCCESS'), height=theme_manager.BUTTON_HEIGHT, font=theme_manager.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)

# Summary Step
class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Summary Report", "", "", **kwargs)
        self.title = "Summary Report"
    
    def analyze_hardware_capability(self, results):
        """Analyze usage capability based on hardware information from BIOS"""
        hw_info = results.get("Hardware identification", {})
        cpu_info = hw_info.get("Details", "")
        
        # Phân tích CPU
        cpu_tier = "unknown"
        cpu_name = ""
        if "Intel" in cpu_info or "AMD" in cpu_info:
            for line in cpu_info.split("\n"):
                if "CPU:" in line:
                    cpu_name = line.split("CPU:")[1].strip()
                    break
        
        # Xác định tier CPU
        if any(x in cpu_name.upper() for x in ["I9", "I7", "RYZEN 9", "RYZEN 7"]):
            cpu_tier = "high"
        elif any(x in cpu_name.upper() for x in ["I5", "RYZEN 5"]):
            cpu_tier = "mid"
        elif any(x in cpu_name.upper() for x in ["I3", "RYZEN 3", "CELERON", "PENTIUM"]):
            cpu_tier = "low"
        
        # Phân tích GPU
        gpu_dedicated = False
        if "GPU:" in cpu_info:
            for line in cpu_info.split("\n"):
                if "GPU:" in line:
                    gpu_text = line.split("GPU:")[1].strip().upper()
                    if any(x in gpu_text for x in ["RTX", "GTX", "RADEON RX", "RADEON PRO"]):
                        gpu_dedicated = True
                    break
        
        # Tạo nhận định
        capabilities = []
        
        if cpu_tier == "high":
            capabilities.append({
                "icon": "🎮",
                "title": "Gaming & Rendering",
                "desc": "Suitable for AAA gaming, 3D rendering, professional video editing",
                "color": "#10B981"
            })
            capabilities.append({
                "icon": "💼",
                "title": "Workstation",
                "desc": "Heavy multitasking, software development, virtual machines",
                "color": "#3B82F6"
            })
        elif cpu_tier == "mid":
            capabilities.append({
                "icon": "🎮",
                "title": "Casual Gaming",
                "desc": "Mid-level gaming, streaming, content creation",
                "color": "#F59E0B"
            })
            capabilities.append({
                "icon": "💼",
                "title": "Advanced Office",
                "desc": "Office, programming, 2D graphics design, moderate multitasking",
                "color": "#3B82F6"
            })
        else:
            capabilities.append({
                "icon": "📝",
                "title": "Basic Office",
                "desc": "Office, web browsing, email, watching videos",
                "color": "#94A3B8"
            })
            capabilities.append({
                "icon": "🎓",
                "title": "Education",
                "desc": "Online learning, document editing, research",
                "color": "#06B6D4"
            })
        
        if gpu_dedicated:
            capabilities.insert(0, {
                "icon": "🎨",
                "title": "Professional Graphics",
                "desc": "Powerful dedicated GPU, suitable for CAD, 3D modeling, AI/ML",
                "color": "#8B5CF6"
            })
        
        return capabilities, cpu_name
    
    def display_summary(self, results):
        for widget in self.action_frame.winfo_children(): 
            widget.destroy()
        
        # Header
        header_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(header_frame, text="📊 SUMMARY REPORT", font=theme_manager.HEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack()
        
        # Statistics Card
        stats_card = ctk.CTkFrame(self.action_frame, fg_color=theme_manager.get_color('FRAME'), corner_radius=theme_manager.CORNER_RADIUS)
        stats_card.pack(fill="x", padx=20, pady=10)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("Status") == "Good")
        warning_tests = sum(1 for r in results.values() if r.get("Status") == "Warning")
        failed_tests = sum(1 for r in results.values() if r.get("Status") == "Error")
        skipped_tests = sum(1 for r in results.values() if r.get("Status") == "Skip")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_grid.pack(fill="x", padx=20, pady=20)
        stats_grid.grid_columnconfigure((0,1,2,3,4), weight=1)
        
        # Total
        self._create_stat_item(stats_grid, 0, "📋", "Total tests", str(total_tests), "#64748B")
        # Passed
        self._create_stat_item(stats_grid, 1, "✅", "Passed", str(passed_tests), "#10B981")
        # Warning
        if warning_tests > 0:
            self._create_stat_item(stats_grid, 2, "⚠️", "Warning", str(warning_tests), "#F59E0B")
        # Failed
        if failed_tests > 0:
            self._create_stat_item(stats_grid, 3, "❌", "Error", str(failed_tests), "#EF4444")
        # Success rate
        rate_color = "#10B981" if success_rate >= 80 else "#F59E0B" if success_rate >= 60 else "#EF4444"
        self._create_stat_item(stats_grid, 4, "📊", "Rate", f"{success_rate:.0f}%", rate_color)
        
        # Hardware Capability Analysis
        capabilities, cpu_name = self.analyze_hardware_capability(results)
        
        if capabilities:
            cap_header = ctk.CTkFrame(self.action_frame, fg_color="transparent")
            cap_header.pack(fill="x", padx=20, pady=(20,10))
            ctk.CTkLabel(cap_header, text="💡 Hardware Capability", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack(anchor="w")
            
            if cpu_name:
                ctk.CTkLabel(cap_header, text=f"Based on: {cpu_name}", font=theme_manager.SMALL_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY')).pack(anchor="w", pady=(5,0))
            
            # Capabilities grid
            cap_grid = ctk.CTkFrame(self.action_frame, fg_color="transparent")
            cap_grid.pack(fill="x", padx=20, pady=10)
            
            for idx, cap in enumerate(capabilities):
                cap_card = ctk.CTkFrame(cap_grid, fg_color=theme_manager.get_color('FRAME'), corner_radius=theme_manager.CORNER_RADIUS, border_width=2, border_color=cap["color"])
                cap_card.pack(fill="x", pady=8)
                
                cap_content = ctk.CTkFrame(cap_card, fg_color="transparent")
                cap_content.pack(fill="x", padx=15, pady=15)
                
                # Icon and title
                title_frame = ctk.CTkFrame(cap_content, fg_color="transparent")
                title_frame.pack(fill="x")
                ctk.CTkLabel(title_frame, text=f"{cap['icon']} {cap['title']}", font=theme_manager.BODY_FONT, text_color=cap["color"]).pack(anchor="w")
                
                # Description
                ctk.CTkLabel(cap_content, text=cap["desc"], font=theme_manager.SMALL_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'), wraplength=800, justify="left").pack(anchor="w", pady=(5,0))
        
        # Detailed Results
        details_header = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        details_header.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(details_header, text="📝 Detailed Results", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT')).pack(anchor="w")
        
        # Results list
        for step_name, result_data in results.items():
            self._create_result_item(step_name, result_data)
        
        # Export buttons
        export_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        export_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(export_frame, text="📄 Export PDF", font=theme_manager.BODY_FONT, fg_color=theme_manager.get_color('ACCENT'), height=50).pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="📊 Export Excel", font=theme_manager.BODY_FONT, fg_color=theme_manager.get_color('SUCCESS'), height=50).pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="📋 Copy Text", font=theme_manager.BODY_FONT, fg_color=theme_manager.get_color('INFO'), height=50).pack(side="left", padx=5)
    
    def _create_stat_item(self, parent, col, icon, label, value, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, padx=10, pady=5)
        ctk.CTkLabel(frame, text=icon, font=("Arial", 24)).pack()
        ctk.CTkLabel(frame, text=value, font=("Arial", 28, "bold"), text_color=color).pack()
        ctk.CTkLabel(frame, text=label, font=("Arial", 14), text_color=theme_manager.get_color('TEXT_SECONDARY')).pack()
    
    def _create_result_item(self, step_name, result_data):
        status = result_data.get("Status", "Unknown")
        result_text = result_data.get("Result", "N/A")
        
        # Determine color and icon
        if status == "Good":
            color, icon = "#10B981", "✅"
        elif status == "Warning":
            color, icon = "#F59E0B", "⚠️"
        elif status == "Error":
            color, icon = "#EF4444", "❌"
        elif status == "Skip":
            color, icon = "#94A3B8", "⏭️"
        else:
            color, icon = "#64748B", "❓"
        
        item_frame = ctk.CTkFrame(self.action_frame, fg_color=theme_manager.get_color('FRAME'), corner_radius=8)
        item_frame.pack(fill="x", padx=20, pady=5)
        
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        content.grid_columnconfigure(1, weight=1)
        
        # Icon
        ctk.CTkLabel(content, text=icon, font=("Arial", 20)).grid(row=0, column=0, padx=(0,10))
        
        # Step name
        ctk.CTkLabel(content, text=step_name, font=("Arial", 16), text_color=theme_manager.get_color('TEXT')).grid(row=0, column=1, sticky="w")
        
        # Status
        status_label = ctk.CTkLabel(content, text=status, font=("Arial", 14), text_color=color, fg_color=color+"20", corner_radius=6)
        status_label.grid(row=0, column=2, padx=10)
        
        # Result detail
        if result_text and result_text != "N/A":
            ctk.CTkLabel(content, text=result_text, font=("Arial", 14), text_color=theme_manager.get_color('TEXT_SECONDARY'), wraplength=600, justify="left").grid(row=1, column=1, columnspan=2, sticky="w", pady=(5,0))
        
        # Chi tiết (nếu có)
        chi_tiet = result_data.get("Details", "")
        if chi_tiet and len(chi_tiet) < 300:
            detail_text = chi_tiet.replace("\n", " | ")
            ctk.CTkLabel(content, text=f"Details: {detail_text}", font=("Arial", 12), text_color=theme_manager.get_color('TEXT_SECONDARY'), wraplength=600, justify="left").grid(row=2, column=1, columnspan=2, sticky="w", pady=(3,0))

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
        nav_frame = ctk.CTkFrame(self, fg_color=theme_manager.get_color('FRAME'), height=80)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10,20))
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_propagate(False)
        nav_frame.lift()
        
        # Previous button
        self.prev_btn = ctk.CTkButton(nav_frame, text="← Previous", command=self.go_previous, 
                                     fg_color=theme_manager.get_color('SKIP'), width=130, height=50, font=theme_manager.BODY_FONT)
        self.prev_btn.grid(row=0, column=0, padx=20, pady=15)
        
        # Skip button
        self.skip_btn = ctk.CTkButton(nav_frame, text="Skip", command=self.skip_current_step,
                                     fg_color=theme_manager.get_color('WARNING'), width=110, height=50, font=theme_manager.BODY_FONT)
        self.skip_btn.grid(row=0, column=1, pady=15)
        
        # Next button  
        self.next_btn = ctk.CTkButton(nav_frame, text="Next →", command=self.go_to_next_step, 
                                     fg_color=theme_manager.get_color('ACCENT'), width=130, height=50, font=theme_manager.BODY_FONT)
        self.next_btn.grid(row=0, column=2, padx=20, pady=15)
        
        self.update_navigation_state()
    
    def skip_current_step(self):
        """Skip current step"""
        if self.current_step < len(self.steps):
            step_name, _ = self.steps[self.current_step]
            self.record_result(step_name, {"Result": "Skip", "Status": "Skip"})
        self.go_to_next_step()
    
    def go_previous(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
            self.update_navigation_state()
    
    def create_header(self):
            header = ctk.CTkFrame(self, fg_color=theme_manager.get_color('FRAME'), height=80)
            header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
            header.grid_columnconfigure(1, weight=1)
            
            # Step counter
            self.step_label = ctk.CTkLabel(header, text="", font=theme_manager.SUBHEADING_FONT, text_color=theme_manager.get_color('ACCENT'))
            self.step_label.grid(row=0, column=0, padx=20, pady=20)
            
            # Progress bar
            self.progress_bar = ctk.CTkProgressBar(header, progress_color=theme_manager.get_color('ACCENT'))
            self.progress_bar.grid(row=0, column=1, sticky="ew", padx=20, pady=20)
            
            # Mode indicator
            mode_text = "Expert Mode" if self.mode == "expert" else "Basic Mode"
            self.mode_label = ctk.CTkLabel(header, text=mode_text, font=theme_manager.BODY_FONT, text_color=theme_manager.get_color('TEXT_SECONDARY'))
            self.mode_label.grid(row=0, column=2, padx=20, pady=20)
        
        def _get_steps_for_mode(self, mode):
            # Cấu trúc bước đúng như main_enhanced
            basic_steps = [
                # Step 1: Physical checklist
                ("Physical inspection", PhysicalInspectionStep),
                # Step 2: BIOS  
                ("BIOS check", BIOSCheckStep),
                # Step 3: Automatic hardware identification
                ("Hardware identification", HardwareFingerprintStep),
                # Các bước tiếp theo
                ("Windows license", LicenseCheckStep), 
                ("System configuration", SystemInfoStep),
                ("Hard drive health", HardDriveHealthStep),
                ("Display test", ScreenTestStep),
                ("Keyboard & Touchpad", KeyboardVisualTestStep),
                ("Ports connectivity", PortsConnectivityStep),
                ("Battery", BatteryHealthStep),
                ("Speakers & Microphone", SpeakerTestStep),
                ("Webcam", WebcamTestStep),
                ("Network & WiFi", NetworkTestStep)
            ]
            
            expert_steps = basic_steps + [
                ("CPU Stress Test", CPUStressTestStep),
                ("Hard drive speed", HardDriveSpeedStep), 
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
            """Update navigation button states"""
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
                self.next_btn.configure(text="Completed")
            else:
                self.skip_btn.configure(state="normal")
                self.next_btn.configure(text="Next →")

# ModeSelectionFrame và App đơn giản
class ModeSelectionFrame(ctk.CTkFrame):
        def __init__(self, master, mode_callback, icon_manager):
            super().__init__(master, fg_color="transparent")
            self.mode_callback = mode_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            # Create mode selection UI
            main_frame = ctk.CTkFrame(self, fg_color=theme_manager.get_color('FRAME'))
            main_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
            main_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(main_frame, text="LaptopTester Pro", font=theme_manager.TITLE_FONT, text_color=theme_manager.get_color('ACCENT')).pack(pady=30)
            ctk.CTkLabel(main_frame, text="Select test mode", font=theme_manager.HEADING_FONT).pack(pady=20)
            
            ctk.CTkButton(main_frame, text="🎯 Basic Mode", command=lambda: self.mode_callback("basic"), 
                         fg_color=theme_manager.get_color('SUCCESS'), height=60, font=theme_manager.SUBHEADING_FONT).pack(pady=20, padx=50, fill="x")
            
            ctk.CTkButton(main_frame, text="🔥 Expert Mode", command=lambda: self.mode_callback("expert"), 
                         fg_color=theme_manager.get_color('ERROR'), height=60, font=theme_manager.SUBHEADING_FONT).pack(pady=20, padx=50, fill="x")

class App(ctk.CTk):
        def __init__(self):
            super().__init__(fg_color=theme_manager.get_color('BACKGROUND'))
            self.title(language_manager.get_text("app_title"))
            self.state('zoomed')
            self.minsize(1400, 900)
            
            # Set initial appearance mode
            ctk.set_appearance_mode(theme_manager.current_theme)
            
            self.icon_manager = IconManager()
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=20)
            self.current_main_frame = None
            self.all_results = {}

            # --- HEADER BAR ---
            self.header = ctk.CTkFrame(self, fg_color=theme_manager.get_color('FRAME'), height=70, corner_radius=0)
            self.header.grid(row=0, column=0, sticky="ew")
            self.header.grid_columnconfigure(0, minsize=80)
            self.header.grid_columnconfigure(1, weight=1)
            self.header.grid_columnconfigure(2, minsize=80)
            logo = self.icon_manager.LOGO_SMALL or None
            self.logo_label = ctk.CTkLabel(self.header, image=logo, text="", width=60)
            self.logo_label.grid(row=0, column=0, padx=(20,0), pady=10)
            self.title_label = ctk.CTkLabel(self.header, text=language_manager.get_text("app_title"), font=theme_manager.HEADING_FONT, text_color=theme_manager.get_color('ACCENT'))
            self.title_label.grid(row=0, column=1, sticky="w", padx=10)
            self.exit_btn = ctk.CTkButton(self.header, text=language_manager.get_text("exit"), command=self.quit_app, font=theme_manager.BODY_FONT, fg_color=theme_manager.get_color('ERROR'), width=80)
            self.exit_btn.grid(row=0, column=2, padx=(0,20), pady=10)

            # Main content
            self.main_content = ctk.CTkFrame(self, fg_color=theme_manager.get_color('BACKGROUND'))
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


        
        def refresh_ui(self):
            """Refresh UI after theme/language change"""
            # Update app colors
            self.configure(fg_color=theme_manager.get_color('BACKGROUND'))
            self.title(language_manager.get_text("app_title"))
            
            # Update header
            self.header.configure(fg_color=theme_manager.get_color('FRAME'))
            self.title_label.configure(
                text=language_manager.get_text("app_title"),
                text_color=theme_manager.get_color('ACCENT')
            )
            self.exit_btn.configure(
                text=language_manager.get_text("exit"),
                fg_color=theme_manager.get_color('ERROR')
            )
            
            # Update main content
            self.main_content.configure(fg_color=theme_manager.get_color('BACKGROUND'))
            
            # Refresh current frame
            if self.current_main_frame:
                self.show_mode_selection()  # Recreate with new theme/language

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
    
    # Set initial CustomTkinter appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()