# -*- coding: utf-8 -*-
"""
Settings and Configuration System for LaptopTester
Hệ thống cài đặt và cấu hình
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from laptoptester import Theme, get_text, CURRENT_LANG, CURRENT_THEME
    from intro_guide_frames import create_home_button
except ImportError:
    class Theme:
        BACKGROUND = "#FAFBFC"
        FRAME = "#FFFFFF"
        ACCENT = "#4299E1"
        SUCCESS = "#38A169"
        WARNING = "#D69E2E"
        ERROR = "#E53E3E"
        TEXT = "#1A202C"
        TEXT_SECONDARY = "#718096"
        HEADING_FONT = ("Segoe UI", 24, "bold")
        SUBHEADING_FONT = ("Segoe UI", 18, "bold")
        BODY_FONT = ("Segoe UI", 14)
        CORNER_RADIUS = 12
        BUTTON_HEIGHT = 40
    
    def get_text(key): return key
    def create_home_button(parent, command, **kwargs): 
        return ctk.CTkButton(parent, text="🏠 HOME", command=command, **kwargs)
    
    CURRENT_LANG = "vi"
    CURRENT_THEME = "dark"

@dataclass
class AppSettings:
    """Application settings data class"""
    # UI Settings
    theme: str = "dark"
    language: str = "vi"
    font_size: int = 14
    window_width: int = 1400
    window_height: int = 900
    
    # Test Settings
    test_timeout: int = 300  # seconds
    auto_advance: bool = True
    skip_warnings: bool = False
    detailed_logging: bool = True
    
    # Performance Settings
    max_cpu_temp: int = 95
    max_gpu_temp: int = 85
    stress_test_duration: int = 120
    benchmark_iterations: int = 3
    
    # Export Settings
    default_export_format: str = "html"
    auto_save_results: bool = True
    export_directory: str = ""
    
    # Advanced Settings
    admin_mode: bool = False
    debug_mode: bool = False
    telemetry_enabled: bool = True
    auto_update: bool = True

class SettingsManager:
    """Settings management class"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.settings = AppSettings()
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Update settings with loaded data
                    for key, value in data.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def reset_to_defaults(self):
        """Reset to default settings"""
        self.settings = AppSettings()
        self.save_settings()
    
    def export_settings(self, filepath: str):
        """Export settings to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
    
    def import_settings(self, filepath: str):
        """Import settings from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key, value in data.items():
                if hasattr(self.settings, key):
                    setattr(self.settings, key, value)
        self.save_settings()

class SettingsFrame(ctk.CTkFrame):
    """Settings configuration frame"""
    
    def __init__(self, master, settings_manager: SettingsManager, on_back=None, on_settings_changed=None):
        super().__init__(master, fg_color="transparent")
        self.settings_manager = settings_manager
        self.on_back = on_back
        self.on_settings_changed = on_settings_changed
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80, corner_radius=Theme.CORNER_RADIUS)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        if self.on_back:
            back_btn = create_home_button(header_frame, command=self.on_back, text="← QUAY LẠI", width=120, height=40)
            back_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(header_frame, text="⚙️ CÀI ĐẶT ỨNG DỤNG", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=1, pady=20)
        
        # Main content with tabs
        self.tabview = ctk.CTkTabview(self, width=1000, height=600)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create tabs
        self.create_ui_settings_tab()
        self.create_test_settings_tab()
        self.create_performance_settings_tab()
        self.create_export_settings_tab()
        self.create_advanced_settings_tab()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_ui_settings_tab(self):
        """Create UI settings tab"""
        self.tabview.add("🎨 Giao Diện")
        ui_tab = self.tabview.tab("🎨 Giao Diện")
        
        # Theme settings
        theme_frame = ctk.CTkFrame(ui_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(theme_frame, text="🌓 Chủ đề giao diện", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        self.theme_var = tk.StringVar(value=self.settings_manager.settings.theme)
        theme_options = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_options.pack(pady=10)
        
        ctk.CTkRadioButton(theme_options, text="🌙 Chế độ tối", variable=self.theme_var, 
                          value="dark", font=Theme.BODY_FONT).pack(side="left", padx=20)
        ctk.CTkRadioButton(theme_options, text="☀️ Chế độ sáng", variable=self.theme_var, 
                          value="light", font=Theme.BODY_FONT).pack(side="left", padx=20)
        
        # Language settings
        lang_frame = ctk.CTkFrame(ui_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        lang_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(lang_frame, text="🌐 Ngôn ngữ", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        self.language_var = tk.StringVar(value=self.settings_manager.settings.language)
        lang_options = ctk.CTkFrame(lang_frame, fg_color="transparent")
        lang_options.pack(pady=10)
        
        ctk.CTkRadioButton(lang_options, text="🇻🇳 Tiếng Việt", variable=self.language_var, 
                          value="vi", font=Theme.BODY_FONT).pack(side="left", padx=20)
        ctk.CTkRadioButton(lang_options, text="🇺🇸 English", variable=self.language_var, 
                          value="en", font=Theme.BODY_FONT).pack(side="left", padx=20)
        
        # Font size
        font_frame = ctk.CTkFrame(ui_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        font_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(font_frame, text="📝 Kích thước chữ", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        self.font_size_var = tk.IntVar(value=self.settings_manager.settings.font_size)
        font_slider = ctk.CTkSlider(font_frame, from_=10, to=20, number_of_steps=10, variable=self.font_size_var)
        font_slider.pack(pady=10)
        
        self.font_size_label = ctk.CTkLabel(font_frame, text=f"Kích thước: {self.font_size_var.get()}px", font=Theme.BODY_FONT)
        self.font_size_label.pack(pady=(0, 20))
        
        font_slider.configure(command=self.update_font_size_label)
    
    def create_test_settings_tab(self):
        """Create test settings tab"""
        self.tabview.add("🧪 Kiểm Tra")
        test_tab = self.tabview.tab("🧪 Kiểm Tra")
        
        # Test timeout
        timeout_frame = ctk.CTkFrame(test_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        timeout_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(timeout_frame, text="⏱️ Thời gian chờ test (giây)", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        self.timeout_var = tk.IntVar(value=self.settings_manager.settings.test_timeout)
        timeout_entry = ctk.CTkEntry(timeout_frame, textvariable=self.timeout_var, width=100)
        timeout_entry.pack(pady=(0, 20))
        
        # Auto advance
        auto_frame = ctk.CTkFrame(test_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        auto_frame.pack(fill="x", padx=20, pady=10)
        
        self.auto_advance_var = tk.BooleanVar(value=self.settings_manager.settings.auto_advance)
        ctk.CTkCheckBox(auto_frame, text="🔄 Tự động chuyển bước sau khi hoàn thành", 
                       variable=self.auto_advance_var, font=Theme.BODY_FONT).pack(pady=20)
        
        # Skip warnings
        warning_frame = ctk.CTkFrame(test_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        warning_frame.pack(fill="x", padx=20, pady=10)
        
        self.skip_warnings_var = tk.BooleanVar(value=self.settings_manager.settings.skip_warnings)
        ctk.CTkCheckBox(warning_frame, text="⚠️ Bỏ qua cảnh báo không quan trọng", 
                       variable=self.skip_warnings_var, font=Theme.BODY_FONT).pack(pady=20)
        
        # Detailed logging
        logging_frame = ctk.CTkFrame(test_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        logging_frame.pack(fill="x", padx=20, pady=10)
        
        self.detailed_logging_var = tk.BooleanVar(value=self.settings_manager.settings.detailed_logging)
        ctk.CTkCheckBox(logging_frame, text="📝 Ghi log chi tiết", 
                       variable=self.detailed_logging_var, font=Theme.BODY_FONT).pack(pady=20)
    
    def create_performance_settings_tab(self):
        """Create performance settings tab"""
        self.tabview.add("⚡ Hiệu Năng")
        perf_tab = self.tabview.tab("⚡ Hiệu Năng")
        
        # Temperature limits
        temp_frame = ctk.CTkFrame(perf_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        temp_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(temp_frame, text="🌡️ Giới hạn nhiệt độ", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        temp_grid = ctk.CTkFrame(temp_frame, fg_color="transparent")
        temp_grid.pack(pady=10)
        temp_grid.grid_columnconfigure((0, 1), weight=1)
        
        # CPU temp
        ctk.CTkLabel(temp_grid, text="CPU tối đa (°C):", font=Theme.BODY_FONT).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.max_cpu_temp_var = tk.IntVar(value=self.settings_manager.settings.max_cpu_temp)
        ctk.CTkEntry(temp_grid, textvariable=self.max_cpu_temp_var, width=80).grid(row=0, column=1, padx=20, pady=5)
        
        # GPU temp
        ctk.CTkLabel(temp_grid, text="GPU tối đa (°C):", font=Theme.BODY_FONT).grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.max_gpu_temp_var = tk.IntVar(value=self.settings_manager.settings.max_gpu_temp)
        ctk.CTkEntry(temp_grid, textvariable=self.max_gpu_temp_var, width=80).grid(row=1, column=1, padx=20, pady=5, sticky="w")
        
        # Stress test duration
        stress_frame = ctk.CTkFrame(perf_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        stress_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(stress_frame, text="⏱️ Thời gian stress test (giây)", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        self.stress_duration_var = tk.IntVar(value=self.settings_manager.settings.stress_test_duration)
        stress_slider = ctk.CTkSlider(stress_frame, from_=30, to=600, number_of_steps=19, variable=self.stress_duration_var)
        stress_slider.pack(pady=10)
        
        self.stress_label = ctk.CTkLabel(stress_frame, text=f"Thời gian: {self.stress_duration_var.get()}s", font=Theme.BODY_FONT)
        self.stress_label.pack(pady=(0, 20))
        
        stress_slider.configure(command=self.update_stress_label)
    
    def create_export_settings_tab(self):
        """Create export settings tab"""
        self.tabview.add("💾 Xuất Dữ Liệu")
        export_tab = self.tabview.tab("💾 Xuất Dữ Liệu")
        
        # Default format
        format_frame = ctk.CTkFrame(export_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        format_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(format_frame, text="📄 Định dạng mặc định", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        self.export_format_var = tk.StringVar(value=self.settings_manager.settings.default_export_format)
        format_options = ctk.CTkFrame(format_frame, fg_color="transparent")
        format_options.pack(pady=10)
        
        formats = [("HTML", "html"), ("JSON", "json"), ("CSV", "csv")]
        for text, value in formats:
            ctk.CTkRadioButton(format_options, text=text, variable=self.export_format_var, 
                              value=value, font=Theme.BODY_FONT).pack(side="left", padx=20)
        
        # Auto save
        auto_save_frame = ctk.CTkFrame(export_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        auto_save_frame.pack(fill="x", padx=20, pady=10)
        
        self.auto_save_var = tk.BooleanVar(value=self.settings_manager.settings.auto_save_results)
        ctk.CTkCheckBox(auto_save_frame, text="💾 Tự động lưu kết quả", 
                       variable=self.auto_save_var, font=Theme.BODY_FONT).pack(pady=20)
        
        # Export directory
        dir_frame = ctk.CTkFrame(export_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        dir_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(dir_frame, text="📁 Thư mục xuất mặc định", font=Theme.SUBHEADING_FONT).pack(pady=(20, 10))
        
        dir_select_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_select_frame.pack(fill="x", padx=20, pady=(0, 20))
        dir_select_frame.grid_columnconfigure(0, weight=1)
        
        self.export_dir_var = tk.StringVar(value=self.settings_manager.settings.export_directory)
        dir_entry = ctk.CTkEntry(dir_select_frame, textvariable=self.export_dir_var)
        dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ctk.CTkButton(dir_select_frame, text="Chọn", command=self.select_export_directory, 
                     width=80).grid(row=0, column=1)
    
    def create_advanced_settings_tab(self):
        """Create advanced settings tab"""
        self.tabview.add("🔧 Nâng Cao")
        advanced_tab = self.tabview.tab("🔧 Nâng Cao")
        
        # Admin mode
        admin_frame = ctk.CTkFrame(advanced_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        admin_frame.pack(fill="x", padx=20, pady=10)
        
        self.admin_mode_var = tk.BooleanVar(value=self.settings_manager.settings.admin_mode)
        ctk.CTkCheckBox(admin_frame, text="👑 Chế độ quản trị viên (cần khởi động lại)", 
                       variable=self.admin_mode_var, font=Theme.BODY_FONT).pack(pady=20)
        
        # Debug mode
        debug_frame = ctk.CTkFrame(advanced_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        debug_frame.pack(fill="x", padx=20, pady=10)
        
        self.debug_mode_var = tk.BooleanVar(value=self.settings_manager.settings.debug_mode)
        ctk.CTkCheckBox(debug_frame, text="🐛 Chế độ debug (hiển thị thông tin kỹ thuật)", 
                       variable=self.debug_mode_var, font=Theme.BODY_FONT).pack(pady=20)
        
        # Telemetry
        telemetry_frame = ctk.CTkFrame(advanced_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        telemetry_frame.pack(fill="x", padx=20, pady=10)
        
        self.telemetry_var = tk.BooleanVar(value=self.settings_manager.settings.telemetry_enabled)
        ctk.CTkCheckBox(telemetry_frame, text="📊 Gửi dữ liệu sử dụng ẩn danh (giúp cải thiện sản phẩm)", 
                       variable=self.telemetry_var, font=Theme.BODY_FONT).pack(pady=20)
        
        # Auto update
        update_frame = ctk.CTkFrame(advanced_tab, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        update_frame.pack(fill="x", padx=20, pady=10)
        
        self.auto_update_var = tk.BooleanVar(value=self.settings_manager.settings.auto_update)
        ctk.CTkCheckBox(update_frame, text="🔄 Tự động kiểm tra cập nhật", 
                       variable=self.auto_update_var, font=Theme.BODY_FONT).pack(pady=20)
    
    def create_action_buttons(self):
        """Create action buttons"""
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=10)
        
        # Save button
        ctk.CTkButton(action_frame, text="💾 LƯU CÀI ĐẶT", command=self.save_settings,
                     fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, 
                     font=Theme.SUBHEADING_FONT).pack(side="left", padx=(0, 10))
        
        # Reset button
        ctk.CTkButton(action_frame, text="🔄 ĐẶT LẠI", command=self.reset_settings,
                     fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT,
                     font=Theme.SUBHEADING_FONT).pack(side="left", padx=10)
        
        # Import/Export buttons
        ctk.CTkButton(action_frame, text="📥 NHẬP", command=self.import_settings,
                     fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(side="right", padx=10)
        
        ctk.CTkButton(action_frame, text="📤 XUẤT", command=self.export_settings,
                     fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(side="right")
    
    def update_font_size_label(self, value):
        """Update font size label"""
        self.font_size_label.configure(text=f"Kích thước: {int(value)}px")
    
    def update_stress_label(self, value):
        """Update stress test duration label"""
        self.stress_label.configure(text=f"Thời gian: {int(value)}s")
    
    def select_export_directory(self):
        """Select export directory"""
        directory = filedialog.askdirectory(title="Chọn thư mục xuất mặc định")
        if directory:
            self.export_dir_var.set(directory)
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Update settings object
            self.settings_manager.settings.theme = self.theme_var.get()
            self.settings_manager.settings.language = self.language_var.get()
            self.settings_manager.settings.font_size = self.font_size_var.get()
            self.settings_manager.settings.test_timeout = self.timeout_var.get()
            self.settings_manager.settings.auto_advance = self.auto_advance_var.get()
            self.settings_manager.settings.skip_warnings = self.skip_warnings_var.get()
            self.settings_manager.settings.detailed_logging = self.detailed_logging_var.get()
            self.settings_manager.settings.max_cpu_temp = self.max_cpu_temp_var.get()
            self.settings_manager.settings.max_gpu_temp = self.max_gpu_temp_var.get()
            self.settings_manager.settings.stress_test_duration = self.stress_duration_var.get()
            self.settings_manager.settings.default_export_format = self.export_format_var.get()
            self.settings_manager.settings.auto_save_results = self.auto_save_var.get()
            self.settings_manager.settings.export_directory = self.export_dir_var.get()
            self.settings_manager.settings.admin_mode = self.admin_mode_var.get()
            self.settings_manager.settings.debug_mode = self.debug_mode_var.get()
            self.settings_manager.settings.telemetry_enabled = self.telemetry_var.get()
            self.settings_manager.settings.auto_update = self.auto_update_var.get()
            
            # Save to file
            self.settings_manager.save_settings()
            
            # Notify callback
            if self.on_settings_changed:
                self.on_settings_changed(self.settings_manager.settings)
            
            messagebox.showinfo("Thành công", "Đã lưu cài đặt thành công!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cài đặt: {e}")
    
    def reset_settings(self):
        """Reset to default settings"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đặt lại tất cả cài đặt về mặc định?"):
            self.settings_manager.reset_to_defaults()
            self.refresh_ui()
            messagebox.showinfo("Thành công", "Đã đặt lại cài đặt về mặc định!")
    
    def export_settings(self):
        """Export settings to file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Xuất cài đặt"
        )
        
        if filepath:
            try:
                self.settings_manager.export_settings(filepath)
                messagebox.showinfo("Thành công", f"Đã xuất cài đặt: {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất cài đặt: {e}")
    
    def import_settings(self):
        """Import settings from file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Nhập cài đặt"
        )
        
        if filepath:
            try:
                self.settings_manager.import_settings(filepath)
                self.refresh_ui()
                messagebox.showinfo("Thành công", f"Đã nhập cài đặt từ: {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể nhập cài đặt: {e}")
    
    def refresh_ui(self):
        """Refresh UI with current settings"""
        settings = self.settings_manager.settings
        
        self.theme_var.set(settings.theme)
        self.language_var.set(settings.language)
        self.font_size_var.set(settings.font_size)
        self.timeout_var.set(settings.test_timeout)
        self.auto_advance_var.set(settings.auto_advance)
        self.skip_warnings_var.set(settings.skip_warnings)
        self.detailed_logging_var.set(settings.detailed_logging)
        self.max_cpu_temp_var.set(settings.max_cpu_temp)
        self.max_gpu_temp_var.set(settings.max_gpu_temp)
        self.stress_duration_var.set(settings.stress_test_duration)
        self.export_format_var.set(settings.default_export_format)
        self.auto_save_var.set(settings.auto_save_results)
        self.export_dir_var.set(settings.export_directory)
        self.admin_mode_var.set(settings.admin_mode)
        self.debug_mode_var.set(settings.debug_mode)
        self.telemetry_var.set(settings.telemetry_enabled)
        self.auto_update_var.set(settings.auto_update)

if __name__ == "__main__":
    # Test settings system
    app = ctk.CTk()
    app.title("Settings System Test")
    app.geometry("1200x800")
    
    settings_manager = SettingsManager()
    
    def on_settings_changed(settings):
        print(f"Settings changed: {settings}")
    
    frame = SettingsFrame(app, settings_manager, on_settings_changed=on_settings_changed)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()