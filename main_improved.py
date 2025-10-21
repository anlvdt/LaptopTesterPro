#!/usr/bin/env python3
"""
LaptopTester Pro - Improved UI/UX with Theme & Language Support
"""

import multiprocessing
import sys
import os
import platform
import threading
import time
import json
import tkinter as tk
from tkinter import messagebox

# Core imports
import customtkinter as ctk
import psutil

# Try to import from backup_enhanced
try:
    from backup_enhanced.laptoptester import *
    print("[INFO] Successfully imported from backup_enhanced")
except ImportError as e:
    print(f"[WARNING] Could not import from backup_enhanced: {e}")
    # Fallback imports
    from PIL import Image
    import wmi
    import pythoncom

# --- THEME SYSTEM ---
class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "BACKGROUND": "#F8FAFC",
                "FRAME": "#FFFFFF", 
                "CARD": "#FFFFFF",
                "BORDER": "#E2E8F0",
                "SEPARATOR": "#F1F5F9",
                "TEXT": "#0F172A",
                "TEXT_SECONDARY": "#64748B",
                "ACCENT": "#3B82F6",
                "ACCENT_HOVER": "#2563EB",
                "SUCCESS": "#10B981",
                "WARNING": "#F59E0B", 
                "ERROR": "#EF4444",
                "SKIP": "#94A3B8",
                "INFO": "#06B6D4"
            },
            "dark": {
                "BACKGROUND": "#0F172A",
                "FRAME": "#1E293B",
                "CARD": "#334155", 
                "BORDER": "#475569",
                "SEPARATOR": "#64748B",
                "TEXT": "#F8FAFC",
                "TEXT_SECONDARY": "#CBD5E1",
                "ACCENT": "#60A5FA",
                "ACCENT_HOVER": "#3B82F6",
                "SUCCESS": "#34D399",
                "WARNING": "#FBBF24",
                "ERROR": "#F87171", 
                "SKIP": "#9CA3AF",
                "INFO": "#22D3EE"
            }
        }
        
        # Typography
        self.TITLE_FONT = ("Segoe UI", 42, "bold")
        self.HEADING_FONT = ("Segoe UI", 28, "bold") 
        self.SUBHEADING_FONT = ("Segoe UI", 22, "bold")
        self.BODY_FONT = ("Segoe UI", 16)
        self.SMALL_FONT = ("Segoe UI", 14)
        self.KEY_FONT = ("Segoe UI", 11)
        self.BUTTON_FONT = ("Segoe UI", 14)
        
        # Layout
        self.CORNER_RADIUS = 12
        self.PADDING_X = 24
        self.PADDING_Y = 20
        self.BUTTON_HEIGHT = 48
        self.CARD_PADDING = 20
        self.SECTION_SPACING = 16
        self.ELEMENT_SPACING = 12
    
    def get_color(self, color_name):
        return self.themes[self.current_theme].get(color_name, "#000000")
    
    def switch_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        # Update CustomTkinter appearance mode
        ctk.set_appearance_mode(self.current_theme)
        return self.current_theme
    
    def apply_theme_to_widget(self, widget, **kwargs):
        """Apply current theme colors to a widget"""
        theme_colors = self.themes[self.current_theme]
        
        # Map common properties
        color_mapping = {
            'fg_color': kwargs.get('fg_color', theme_colors.get('FRAME')),
            'text_color': kwargs.get('text_color', theme_colors.get('TEXT')),
            'border_color': kwargs.get('border_color', theme_colors.get('BORDER'))
        }
        
        # Apply colors that exist in the widget
        for prop, color in color_mapping.items():
            if hasattr(widget, 'configure') and color:
                try:
                    widget.configure(**{prop: color})
                except:
                    pass

# --- LANGUAGE SYSTEM ---
class LanguageManager:
    def __init__(self):
        self.current_language = "vi"
        self.translations = {
            "vi": {
                # UI Elements
                "app_title": "Laptop Tester Pro",
                "exit": "Thoát",
                "settings": "Cài đặt",
                "theme": "Giao diện",
                "language": "Ngôn ngữ",
                "light_theme": "Sáng",
                "dark_theme": "Tối",
                
                # Navigation
                "previous": "← Trước",
                "next": "Tiếp theo →",
                "skip": "Bỏ qua",
                "complete": "Hoàn thành",
                
                # Mode Selection
                "select_mode": "Chọn Chế Độ Kiểm Tra",
                "basic_mode": "Chế Độ Cơ Bản",
                "expert_mode": "Chế Độ Chuyên Gia",
                "basic_desc": "Dành cho mọi người dùng.\nNhanh chóng, an toàn và dễ hiểu.",
                "expert_desc": "Dành cho kỹ thuật viên.\nĐầy đủ các bước test chuyên sâu.",
                
                # Test Steps
                "physical_inspection": "Kiểm Tra Ngoại Hình",
                "bios_check": "Kiểm Tra BIOS",
                "hardware_fingerprint": "Định Danh Phần Cứng",
                "license_check": "Bản Quyền Windows",
                "system_info": "Cấu Hình Hệ Thống",
                "hard_drive_health": "Sức Khỏe Ổ Cứng",
                "screen_test": "Kiểm Tra Màn Hình",
                "keyboard_test": "Bàn Phím & Touchpad",
                "ports_test": "Cổng Kết Nối",
                "battery_test": "Pin Laptop",
                "speaker_test": "Loa & Micro",
                "webcam_test": "Webcam",
                "network_test": "Mạng & WiFi",
                "cpu_stress": "CPU Stress Test",
                "gpu_stress": "GPU Stress Test",
                "disk_speed": "Tốc Độ Ổ Cứng",
                "thermal_test": "Thermal Monitor",
                
                # Status
                "ready": "Sẵn sàng",
                "running": "Đang chạy",
                "completed": "Hoàn thành",
                "error": "Lỗi",
                "good": "Tốt",
                "warning": "Cảnh báo",
                "skipped": "Bỏ qua",
                
                # Actions
                "start_test": "Bắt đầu Test",
                "stop_test": "Dừng Test",
                "yes": "Có",
                "no": "Không",
                "continue": "Tiếp tục",
                
                # Messages
                "test_completed": "Test đã hoàn thành",
                "no_issues_found": "Không phát hiện vấn đề",
                "issues_found": "Phát hiện vấn đề",
                "loading": "Đang tải...",
                "processing": "Đang xử lý...",
            },
            "en": {
                # UI Elements
                "app_title": "Laptop Tester Pro",
                "exit": "Exit",
                "settings": "Settings",
                "theme": "Theme",
                "language": "Language",
                "light_theme": "Light",
                "dark_theme": "Dark",
                
                # Navigation
                "previous": "← Previous",
                "next": "Next →",
                "skip": "Skip",
                "complete": "Complete",
                
                # Mode Selection
                "select_mode": "Select Test Mode",
                "basic_mode": "Basic Mode",
                "expert_mode": "Expert Mode",
                "basic_desc": "For all users.\nQuick, safe and easy to understand.",
                "expert_desc": "For technicians.\nComprehensive deep testing.",
                
                # Test Steps
                "physical_inspection": "Physical Inspection",
                "bios_check": "BIOS Check",
                "hardware_fingerprint": "Hardware Fingerprint",
                "license_check": "Windows License",
                "system_info": "System Configuration",
                "hard_drive_health": "Hard Drive Health",
                "screen_test": "Display Test",
                "keyboard_test": "Keyboard & Touchpad",
                "ports_test": "Ports Connectivity",
                "battery_test": "Battery Health",
                "speaker_test": "Speaker & Microphone",
                "webcam_test": "Webcam Test",
                "network_test": "Network & WiFi",
                "cpu_stress": "CPU Stress Test",
                "gpu_stress": "GPU Stress Test",
                "disk_speed": "Hard Drive Speed",
                "thermal_test": "Thermal Monitor",
                
                # Status
                "ready": "Ready",
                "running": "Running",
                "completed": "Completed",
                "error": "Error",
                "good": "Good",
                "warning": "Warning",
                "skipped": "Skipped",
                
                # Actions
                "start_test": "Start Test",
                "stop_test": "Stop Test",
                "yes": "Yes",
                "no": "No",
                "continue": "Continue",
                
                # Messages
                "test_completed": "Test completed",
                "no_issues_found": "No issues found",
                "issues_found": "Issues found",
                "loading": "Loading...",
                "processing": "Processing...",
            }
        }
    
    def get_text(self, key):
        return self.translations[self.current_language].get(key, key)
    
    def switch_language(self):
        self.current_language = "en" if self.current_language == "vi" else "vi"
        return self.current_language

# Global instances
theme_manager = ThemeManager()
language_manager = LanguageManager()

# --- IMPROVED BASE CLASSES ---
class ThemedFrame(ctk.CTkFrame):
    """Base frame that automatically applies theme"""
    def __init__(self, master, **kwargs):
        # Apply theme colors
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = theme_manager.get_color('FRAME')
        super().__init__(master, **kwargs)
        self.update_theme()
    
    def update_theme(self):
        """Update colors when theme changes"""
        self.configure(fg_color=theme_manager.get_color('FRAME'))

class ThemedLabel(ctk.CTkLabel):
    """Label that automatically applies theme"""
    def __init__(self, master, **kwargs):
        if 'text_color' not in kwargs:
            kwargs['text_color'] = theme_manager.get_color('TEXT')
        super().__init__(master, **kwargs)
    
    def update_theme(self):
        self.configure(text_color=theme_manager.get_color('TEXT'))

class ThemedButton(ctk.CTkButton):
    """Button that automatically applies theme"""
    def __init__(self, master, **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = theme_manager.get_color('ACCENT')
        if 'hover_color' not in kwargs:
            kwargs['hover_color'] = theme_manager.get_color('ACCENT_HOVER')
        super().__init__(master, **kwargs)
    
    def update_theme(self):
        self.configure(
            fg_color=theme_manager.get_color('ACCENT'),
            hover_color=theme_manager.get_color('ACCENT_HOVER')
        )

# --- SETTINGS PANEL ---
class SettingsPanel(ctk.CTkToplevel):
    def __init__(self, parent, on_change_callback=None):
        super().__init__(parent)
        self.on_change_callback = on_change_callback
        
        self.title(language_manager.get_text("settings"))
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center on parent
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ThemedFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ThemedLabel(main_frame, 
                                 text=language_manager.get_text("settings"),
                                 font=theme_manager.HEADING_FONT)
        title_label.pack(pady=(0, 20))
        
        # Theme section
        theme_frame = ThemedFrame(main_frame)
        theme_frame.pack(fill="x", pady=10)
        
        ThemedLabel(theme_frame, 
                   text=language_manager.get_text("theme"),
                   font=theme_manager.SUBHEADING_FONT).pack(anchor="w", padx=10, pady=5)
        
        theme_buttons_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_buttons_frame.pack(fill="x", padx=10, pady=5)
        
        light_btn = ThemedButton(theme_buttons_frame,
                               text=language_manager.get_text("light_theme"),
                               command=self.switch_to_light,
                               width=80)
        light_btn.pack(side="left", padx=5)
        
        dark_btn = ThemedButton(theme_buttons_frame,
                              text=language_manager.get_text("dark_theme"),
                              command=self.switch_to_dark,
                              width=80)
        dark_btn.pack(side="left", padx=5)
        
        # Language section
        lang_frame = ThemedFrame(main_frame)
        lang_frame.pack(fill="x", pady=10)
        
        ThemedLabel(lang_frame,
                   text=language_manager.get_text("language"),
                   font=theme_manager.SUBHEADING_FONT).pack(anchor="w", padx=10, pady=5)
        
        lang_buttons_frame = ctk.CTkFrame(lang_frame, fg_color="transparent")
        lang_buttons_frame.pack(fill="x", padx=10, pady=5)
        
        vi_btn = ThemedButton(lang_buttons_frame,
                            text="Tiếng Việt",
                            command=self.switch_to_vietnamese,
                            width=100)
        vi_btn.pack(side="left", padx=5)
        
        en_btn = ThemedButton(lang_buttons_frame,
                            text="English",
                            command=self.switch_to_english,
                            width=100)
        en_btn.pack(side="left", padx=5)
        
        # Close button
        close_btn = ThemedButton(main_frame,
                               text=language_manager.get_text("exit"),
                               command=self.destroy,
                               fg_color=theme_manager.get_color('ERROR'))
        close_btn.pack(pady=20)
    
    def switch_to_light(self):
        if theme_manager.current_theme != "light":
            theme_manager.switch_theme()
            self.refresh_ui()
    
    def switch_to_dark(self):
        if theme_manager.current_theme != "dark":
            theme_manager.switch_theme()
            self.refresh_ui()
    
    def switch_to_vietnamese(self):
        if language_manager.current_language != "vi":
            language_manager.switch_language()
            self.refresh_ui()
    
    def switch_to_english(self):
        if language_manager.current_language != "en":
            language_manager.switch_language()
            self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh UI after theme/language change"""
        if self.on_change_callback:
            self.on_change_callback()
        
        # Refresh this window
        self.destroy()
        # Parent will handle recreating if needed

# --- IMPROVED MODE SELECTION ---
class ImprovedModeSelectionFrame(ThemedFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = ThemedFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        
        title_label = ThemedLabel(header_frame,
                                 text=language_manager.get_text("select_mode"),
                                 font=theme_manager.TITLE_FONT)
        title_label.pack(pady=(0, 10))
        
        # Mode cards
        cards_frame = ThemedFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        cards_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Basic mode card
        basic_card = self.create_mode_card(
            cards_frame,
            title=language_manager.get_text("basic_mode"),
            description=language_manager.get_text("basic_desc"),
            button_text=language_manager.get_text("basic_mode"),
            button_color=theme_manager.get_color('SUCCESS'),
            command=lambda: self.mode_callback("basic")
        )
        basic_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Expert mode card
        expert_card = self.create_mode_card(
            cards_frame,
            title=language_manager.get_text("expert_mode"),
            description=language_manager.get_text("expert_desc"),
            button_text=language_manager.get_text("expert_mode"),
            button_color=theme_manager.get_color('ERROR'),
            command=lambda: self.mode_callback("expert")
        )
        expert_card.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    
    def create_mode_card(self, parent, title, description, button_text, button_color, command):
        card = ThemedFrame(parent, corner_radius=theme_manager.CORNER_RADIUS)
        
        # Title
        title_label = ThemedLabel(card, text=title, font=theme_manager.HEADING_FONT,
                                 text_color=theme_manager.get_color('ACCENT'))
        title_label.pack(pady=(30, 15))
        
        # Description
        desc_label = ThemedLabel(card, text=description, font=theme_manager.BODY_FONT,
                                text_color=theme_manager.get_color('TEXT_SECONDARY'),
                                wraplength=400)
        desc_label.pack(padx=30, pady=15, expand=True)
        
        # Button
        button = ctk.CTkButton(card, text=button_text, command=command,
                              height=theme_manager.BUTTON_HEIGHT,
                              font=theme_manager.SUBHEADING_FONT,
                              fg_color=button_color)
        button.pack(padx=30, pady=30, fill="x", side="bottom")
        
        return card
    
    def update_theme(self):
        """Update all child widgets when theme changes"""
        super().update_theme()
        # Recursively update all children
        self.update_children_theme(self)
    
    def update_children_theme(self, widget):
        """Recursively update theme for all children"""
        for child in widget.winfo_children():
            if hasattr(child, 'update_theme'):
                child.update_theme()
            self.update_children_theme(child)

# --- IMPROVED APP CLASS ---
class ImprovedApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=theme_manager.get_color('BACKGROUND'))
        
        self.title(language_manager.get_text("app_title"))
        self.state('zoomed')
        self.minsize(1400, 900)
        
        # Set initial appearance mode
        ctk.set_appearance_mode(theme_manager.current_theme)
        
        self.current_main_frame = None
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)
        
        # Header
        self.create_header()
        
        # Main content
        self.main_content = ThemedFrame(self, fg_color=theme_manager.get_color('BACKGROUND'))
        self.main_content.grid(row=1, column=0, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)
        
        # Show initial screen
        self.show_mode_selection()
    
    def create_header(self):
        self.header = ThemedFrame(self, height=70, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title_label = ThemedLabel(self.header,
                                      text=language_manager.get_text("app_title"),
                                      font=theme_manager.HEADING_FONT,
                                      text_color=theme_manager.get_color('ACCENT'))
        self.title_label.grid(row=0, column=1, sticky="w", padx=20, pady=15)
        
        # Settings button
        self.settings_btn = ThemedButton(self.header,
                                       text=language_manager.get_text("settings"),
                                       command=self.show_settings,
                                       width=100)
        self.settings_btn.grid(row=0, column=2, padx=10, pady=15)
        
        # Exit button
        self.exit_btn = ctk.CTkButton(self.header,
                                     text=language_manager.get_text("exit"),
                                     command=self.quit_app,
                                     fg_color=theme_manager.get_color('ERROR'),
                                     width=80)
        self.exit_btn.grid(row=0, column=3, padx=(0, 20), pady=15)
    
    def show_settings(self):
        settings = SettingsPanel(self, self.on_settings_change)
    
    def on_settings_change(self):
        """Called when theme or language changes"""
        # Update app colors
        self.configure(fg_color=theme_manager.get_color('BACKGROUND'))
        
        # Update header
        self.header.configure(fg_color=theme_manager.get_color('FRAME'))
        self.title_label.configure(
            text=language_manager.get_text("app_title"),
            text_color=theme_manager.get_color('ACCENT')
        )
        self.settings_btn.configure(text=language_manager.get_text("settings"))
        self.exit_btn.configure(text=language_manager.get_text("exit"))
        
        # Update main content
        self.main_content.configure(fg_color=theme_manager.get_color('BACKGROUND'))
        
        # Refresh current frame
        if self.current_main_frame:
            if hasattr(self.current_main_frame, 'update_theme'):
                self.current_main_frame.update_theme()
            else:
                # Recreate the frame if it doesn't support theme updates
                self.show_mode_selection()
    
    def clear_window(self):
        if self.current_main_frame:
            self.current_main_frame.destroy()
        self.current_main_frame = None
    
    def show_mode_selection(self):
        self.clear_window()
        self.current_main_frame = ImprovedModeSelectionFrame(self.main_content, self.start_wizard)
        self.current_main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
    
    def start_wizard(self, mode):
        # For now, just show a message
        messagebox.showinfo(
            language_manager.get_text("app_title"),
            f"Starting {mode} mode...\n(Full implementation would go here)"
        )
        
        # In full implementation, this would create the wizard
        # self.clear_window()
        # self.current_main_frame = WizardFrame(self.main_content, mode, ...)
    
    def quit_app(self):
        self.clear_window()
        self.destroy()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Set initial CustomTkinter appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    try:
        app = ImprovedApp()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()