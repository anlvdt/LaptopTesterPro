#!/usr/bin/env python3
"""
LaptopTester Pro - Modern Beautiful UI
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import time

# Modern Theme System
class ModernTheme:
    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "light": {
                "bg": "#FFFFFF", "surface": "#F8FAFC", "card": "#FFFFFF", 
                "primary": "#6366F1", "primary_hover": "#4F46E5", "secondary": "#64748B",
                "success": "#10B981", "warning": "#F59E0B", "error": "#EF4444",
                "text": "#1E293B", "text_muted": "#64748B", "border": "#E2E8F0"
            },
            "dark": {
                "bg": "#0F172A", "surface": "#1E293B", "card": "#334155",
                "primary": "#818CF8", "primary_hover": "#6366F1", "secondary": "#64748B", 
                "success": "#34D399", "warning": "#FBBF24", "error": "#F87171",
                "text": "#F1F5F9", "text_muted": "#94A3B8", "border": "#475569"
            }
        }
    
    def get(self, key): return self.themes[self.current_theme][key]
    def toggle(self): 
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self.current_theme)

theme = ModernTheme()

class ModernCard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.get("card"), corner_radius=16, 
                        border_width=1, border_color=theme.get("border"), **kwargs)

class ModernButton(ctk.CTkButton):
    def __init__(self, parent, style="primary", **kwargs):
        colors = {
            "primary": (theme.get("primary"), theme.get("primary_hover")),
            "success": (theme.get("success"), "#059669"),
            "warning": (theme.get("warning"), "#D97706"),
            "error": (theme.get("error"), "#DC2626"),
            "ghost": ("transparent", theme.get("surface"))
        }
        color, hover = colors.get(style, colors["primary"])
        
        super().__init__(parent, fg_color=color, hover_color=hover, 
                        corner_radius=12, height=48, font=("Segoe UI", 14, "bold"),
                        border_width=1 if style=="ghost" else 0,
                        border_color=theme.get("border") if style=="ghost" else None, **kwargs)

class GradientFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.get("primary"), corner_radius=20, **kwargs)

class ModernModeCard(ModernCard):
    def __init__(self, parent, title, description, icon, color, command):
        super().__init__(parent)
        self.configure(width=320, height=280)
        
        # Icon area with gradient background
        icon_frame = GradientFrame(self, width=80, height=80)
        icon_frame.pack(pady=(30, 20))
        
        icon_label = ctk.CTkLabel(icon_frame, text=icon, font=("Segoe UI", 32), 
                                 text_color="white")
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = ctk.CTkLabel(self, text=title, font=("Segoe UI", 24, "bold"),
                                  text_color=theme.get("text"))
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(self, text=description, font=("Segoe UI", 14),
                                 text_color=theme.get("text_muted"), wraplength=280)
        desc_label.pack(pady=(0, 20), padx=20)
        
        # Button
        btn = ModernButton(self, text=f"Chọn {title}", style=color, command=command)
        btn.pack(pady=(0, 30), padx=30, fill="x")

class ModernHeader(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=theme.get("surface"), height=80, corner_radius=0)
        self.app = app
        
        # Logo and title
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(side="left", padx=30, pady=20)
        
        logo = ctk.CTkLabel(logo_frame, text="💻", font=("Segoe UI", 28))
        logo.pack(side="left", padx=(0, 15))
        
        title = ctk.CTkLabel(logo_frame, text="LaptopTester Pro", 
                           font=("Segoe UI", 24, "bold"), text_color=theme.get("primary"))
        title.pack(side="left")
        
        # Controls
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(side="right", padx=30, pady=20)
        
        # Theme toggle
        theme_btn = ModernButton(controls, text="🌙" if theme.current_theme=="light" else "☀️", 
                               style="ghost", width=50, command=self.toggle_theme)
        theme_btn.pack(side="right", padx=5)
        
        # Language toggle  
        lang_btn = ModernButton(controls, text="EN", style="ghost", width=50, 
                              command=self.toggle_language)
        lang_btn.pack(side="right", padx=5)
        
        self.theme_btn = theme_btn
        self.lang_btn = lang_btn
    
    def toggle_theme(self):
        theme.toggle()
        self.theme_btn.configure(text="🌙" if theme.current_theme=="light" else "☀️")
        self.app.refresh_ui()
    
    def toggle_language(self):
        current = self.lang_btn.cget("text")
        new_lang = "VI" if current == "EN" else "EN"
        self.lang_btn.configure(text=new_lang)

class ModernModeSelection(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, fg_color="transparent")
        self.callback = callback
        
        # Hero section
        hero = ctk.CTkFrame(self, fg_color="transparent", height=200)
        hero.pack(fill="x", pady=(40, 60))
        
        title = ctk.CTkLabel(hero, text="Chọn Chế Độ Kiểm Tra", 
                           font=("Segoe UI", 42, "bold"), text_color=theme.get("text"))
        title.pack(pady=(20, 10))
        
        subtitle = ctk.CTkLabel(hero, text="Lựa chọn phù hợp với nhu cầu và trình độ của bạn",
                              font=("Segoe UI", 18), text_color=theme.get("text_muted"))
        subtitle.pack()
        
        # Mode cards container
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(expand=True, fill="both", padx=60)
        
        cards_frame = ctk.CTkFrame(cards_container, fg_color="transparent")
        cards_frame.pack(expand=True)
        cards_frame.grid_columnconfigure((0,1), weight=1)
        
        # Basic mode card
        basic_card = ModernModeCard(
            cards_frame,
            title="Cơ Bản", 
            description="Dành cho người dùng thông thường\nKiểm tra nhanh các tính năng chính",
            icon="🎯",
            color="success",
            command=lambda: self.callback("basic")
        )
        basic_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Expert mode card  
        expert_card = ModernModeCard(
            cards_frame,
            title="Chuyên Gia",
            description="Dành cho kỹ thuật viên\nKiểm tra toàn diện và chuyên sâu", 
            icon="🔥",
            color="warning",
            command=lambda: self.callback("expert")
        )
        expert_card.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

class ModernTestStep(ModernCard):
    def __init__(self, parent, title, description, icon="⚡"):
        super().__init__(parent)
        self.configure(height=120)
        
        # Content frame
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        content.grid_columnconfigure(1, weight=1)
        
        # Icon
        icon_label = ctk.CTkLabel(content, text=icon, font=("Segoe UI", 32))
        icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 20), sticky="w")
        
        # Title
        title_label = ctk.CTkLabel(content, text=title, font=("Segoe UI", 18, "bold"),
                                  text_color=theme.get("text"), anchor="w")
        title_label.grid(row=0, column=1, sticky="ew")
        
        # Description
        desc_label = ctk.CTkLabel(content, text=description, font=("Segoe UI", 14),
                                 text_color=theme.get("text_muted"), anchor="w")
        desc_label.grid(row=1, column=1, sticky="ew")
        
        # Status indicator
        self.status = ctk.CTkLabel(content, text="⏳", font=("Segoe UI", 20))
        self.status.grid(row=0, column=2, rowspan=2, padx=(20, 0))
    
    def set_status(self, status):
        icons = {"pending": "⏳", "running": "🔄", "success": "✅", "error": "❌", "skip": "⏭️"}
        self.status.configure(text=icons.get(status, "⏳"))

class ModernWizard(ctk.CTkFrame):
    def __init__(self, parent, mode, app):
        super().__init__(parent, fg_color="transparent")
        self.mode = mode
        self.app = app
        self.current_step = 0
        
        # Steps data
        self.steps = [
            ("Kiểm tra ngoại hình", "Kiểm tra tình trạng vật lý của laptop", "🔍"),
            ("Kiểm tra BIOS", "Xác minh cài đặt BIOS và bảo mật", "⚙️"),
            ("Định danh phần cứng", "Thu thập thông tin phần cứng chi tiết", "🔧"),
            ("Bản quyền Windows", "Kiểm tra tính hợp lệ của Windows", "🪟"),
            ("Cấu hình hệ thống", "Phân tích thông số hệ thống", "📊"),
            ("Sức khỏe ổ cứng", "Đánh giá tình trạng ổ cứng", "💾"),
            ("Kiểm tra màn hình", "Test chất lượng hiển thị", "🖥️"),
            ("Bàn phím & Touchpad", "Kiểm tra thiết bị nhập liệu", "⌨️"),
            ("Cổng kết nối", "Test các cổng USB, HDMI, Audio", "🔌"),
            ("Pin laptop", "Đánh giá sức khỏe pin", "🔋"),
            ("Loa & Micro", "Kiểm tra hệ thống âm thanh", "🔊"),
            ("Webcam", "Test camera và chất lượng hình ảnh", "📷"),
            ("Mạng & WiFi", "Kiểm tra kết nối mạng", "📶")
        ]
        
        if mode == "expert":
            self.steps.extend([
                ("CPU Stress Test", "Kiểm tra hiệu năng và ổn định CPU", "🚀"),
                ("GPU Stress Test", "Test hiệu năng đồ họa", "🎮"),
                ("Tốc độ ổ cứng", "Benchmark tốc độ đọc/ghi", "⚡"),
                ("Thermal Monitor", "Giám sát nhiệt độ hệ thống", "🌡️")
            ])
        
        self.create_ui()
        # Không tự động chạy demo nữa
    
    def create_ui(self):
        # Header with progress
        header = ModernCard(self, height=100)
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=20)
        header_content.grid_columnconfigure(1, weight=1)
        
        # Mode badge
        mode_badge = ctk.CTkLabel(header_content, 
                                 text=f"🎯 Chế độ {'Chuyên gia' if self.mode=='expert' else 'Cơ bản'}",
                                 font=("Segoe UI", 14, "bold"), 
                                 text_color=theme.get("primary"))
        mode_badge.grid(row=0, column=0, sticky="w")
        
        # Progress info
        self.progress_label = ctk.CTkLabel(header_content, text="Bước 1/13: Chuẩn bị kiểm tra",
                                          font=("Segoe UI", 18, "bold"), text_color=theme.get("text"))
        self.progress_label.grid(row=0, column=1, sticky="ew", padx=20)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(header_content, height=8, corner_radius=4,
                                              progress_color=theme.get("primary"))
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.progress_bar.set(0)
        
        # Steps container
        steps_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        steps_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Create step cards
        self.step_cards = []
        for i, (title, desc, icon) in enumerate(self.steps):
            card = ModernTestStep(steps_container, title, desc, icon)
            card.pack(fill="x", pady=5)
            self.step_cards.append(card)
        
        # Navigation
        nav = ModernCard(self, height=80)
        nav.pack(fill="x", padx=30, pady=(0, 30))
        
        nav_content = ctk.CTkFrame(nav, fg_color="transparent")
        nav_content.pack(fill="both", expand=True, padx=30, pady=15)
        nav_content.grid_columnconfigure(1, weight=1)
        
        self.prev_btn = ModernButton(nav_content, text="← Trước", style="ghost", 
                                   width=120, state="disabled")
        self.prev_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.skip_btn = ModernButton(nav_content, text="Bỏ qua", style="ghost", width=100)
        self.skip_btn.grid(row=0, column=1, padx=10)
        
        self.next_btn = ModernButton(nav_content, text="Bắt đầu →", width=120, 
                                   command=lambda: self.run_step(self.current_step))
        self.next_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Initialize current step
        self.current_step = 0
    
    def run_step(self, step_index):
        """Chạy một bước kiểm tra cụ thể"""
        if step_index >= len(self.steps):
            return
            
        # Update current step
        self.current_step = step_index
        progress = (step_index + 1) / len(self.steps)
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"Bước {step_index+1}/{len(self.steps)}: {self.steps[step_index][0]}")
        
        # Set step as running
        self.step_cards[step_index].set_status("running")
        
        # Disable next button during test
        self.next_btn.configure(state="disabled", text="Đang kiểm tra...")
        
        # Simulate test (replace with real test logic)
        def complete_step():
            time.sleep(2)  # Simulate test time
            if hasattr(self, 'step_cards'):
                self.step_cards[step_index].set_status("success")
                
                # Move to next step or complete
                if step_index < len(self.steps) - 1:
                    self.current_step += 1
                    self.next_btn.configure(state="normal", text="Tiếp theo →")
                else:
                    self.progress_label.configure(text="✅ Hoàn thành tất cả kiểm tra!")
                    self.next_btn.configure(text="Hoàn thành", state="disabled")
                    messagebox.showinfo("Hoàn thành", "Tất cả kiểm tra đã hoàn thành!")
        
        threading.Thread(target=complete_step, daemon=True).start()

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=theme.get("bg"))
        
        self.title("LaptopTester Pro - Modern UI")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Set appearance
        ctk.set_appearance_mode(theme.current_theme)
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        self.header = ModernHeader(self, self)
        self.header.pack(fill="x")
        
        # Main content
        self.main_frame = ctk.CTkFrame(self, fg_color=theme.get("surface"))
        self.main_frame.pack(fill="both", expand=True)
        
        # Show mode selection
        self.show_mode_selection()
    
    def show_mode_selection(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Show mode selection
        self.mode_selection = ModernModeSelection(self.main_frame, self.start_test)
        self.mode_selection.pack(fill="both", expand=True)
    
    def start_test(self, mode):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Show wizard
        self.wizard = ModernWizard(self.main_frame, mode, self)
        self.wizard.pack(fill="both", expand=True)
    
    def refresh_ui(self):
        """Refresh UI colors after theme change"""
        self.configure(fg_color=theme.get("bg"))
        self.main_frame.configure(fg_color=theme.get("surface"))
        
        # Recreate current view
        if hasattr(self, 'wizard'):
            mode = self.wizard.mode
            self.start_test(mode)
        else:
            self.show_mode_selection()

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()