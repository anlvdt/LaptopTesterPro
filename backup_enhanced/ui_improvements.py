# UI/UX Improvements for LaptopTester
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import json
import os
from datetime import datetime

class ModernTheme:
    """Enhanced theme with better spacing and modern design"""
    # Colors - Refined palette
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    ERROR = "#EF4444"
    SURFACE = "#FFFFFF"
    BACKGROUND = "#F8FAFC"
    CARD = "#FFFFFF"
    BORDER = "#E2E8F0"
    TEXT = "#0F172A"
    TEXT_MUTED = "#64748B"
    
    # Spacing - Consistent system
    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 16
    SPACE_LG = 24
    SPACE_XL = 32
    SPACE_2XL = 48
    
    # Typography
    FONT_TITLE = ("Segoe UI", 32, "bold")
    FONT_HEADING = ("Segoe UI", 24, "bold")
    FONT_SUBHEADING = ("Segoe UI", 18, "bold")
    FONT_BODY = ("Segoe UI", 14)
    FONT_CAPTION = ("Segoe UI", 12)
    
    # Layout
    RADIUS = 12
    BUTTON_HEIGHT = 44
    INPUT_HEIGHT = 40

class AnimationHelper:
    """Smooth animations for better UX"""
    
    @staticmethod
    def fade_in(widget, duration=300, steps=20):
        """Fade in animation"""
        def animate():
            for i in range(steps + 1):
                alpha = i / steps
                try:
                    widget.configure(fg_color=ModernTheme.SURFACE)
                    widget.update()
                    time.sleep(duration / 1000 / steps)
                except:
                    break
        threading.Thread(target=animate, daemon=True).start()
    
    @staticmethod
    def slide_in(widget, direction="left", duration=300):
        """Slide in animation"""
        def animate():
            original_x = widget.winfo_x()
            start_x = original_x - 100 if direction == "left" else original_x + 100
            
            for i in range(21):
                progress = i / 20
                current_x = start_x + (original_x - start_x) * progress
                try:
                    widget.place(x=current_x)
                    widget.update()
                    time.sleep(duration / 1000 / 20)
                except:
                    break
        threading.Thread(target=animate, daemon=True).start()

class NotificationToast:
    """Modern toast notifications"""
    
    def __init__(self, parent):
        self.parent = parent
        self.toasts = []
    
    def show(self, message, type="info", duration=3000):
        """Show toast notification"""
        colors = {
            "info": ModernTheme.PRIMARY,
            "success": ModernTheme.SUCCESS,
            "warning": ModernTheme.WARNING,
            "error": ModernTheme.ERROR
        }
        
        toast = ctk.CTkFrame(
            self.parent,
            fg_color=colors.get(type, ModernTheme.PRIMARY),
            corner_radius=ModernTheme.RADIUS,
            width=300,
            height=60
        )
        
        # Position toast
        y_offset = len(self.toasts) * 70 + ModernTheme.SPACE_LG
        toast.place(x=self.parent.winfo_width() - 320, y=y_offset)
        
        # Toast content
        ctk.CTkLabel(
            toast,
            text=message,
            font=ModernTheme.FONT_BODY,
            text_color="white",
            wraplength=280
        ).pack(expand=True, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
        
        self.toasts.append(toast)
        
        # Auto remove
        def remove_toast():
            time.sleep(duration / 1000)
            try:
                toast.destroy()
                self.toasts.remove(toast)
            except:
                pass
        
        threading.Thread(target=remove_toast, daemon=True).start()

class ProgressIndicator:
    """Enhanced progress indicator with animations"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        self.container = ctk.CTkFrame(self.parent, fg_color="transparent")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.container,
            width=400,
            height=8,
            progress_color=ModernTheme.PRIMARY
        )
        self.progress_bar.pack(pady=ModernTheme.SPACE_SM)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.container,
            text="Sẵn sàng",
            font=ModernTheme.FONT_CAPTION,
            text_color=ModernTheme.TEXT_MUTED
        )
        self.status_label.pack()
        
        # Animated dots
        self.dots_label = ctk.CTkLabel(
            self.container,
            text="",
            font=ModernTheme.FONT_CAPTION,
            text_color=ModernTheme.PRIMARY
        )
        self.dots_label.pack()
        
        self.is_animating = False
    
    def start_animation(self, message="Đang xử lý"):
        """Start loading animation"""
        self.is_animating = True
        self.status_label.configure(text=message)
        
        def animate_dots():
            dots = 0
            while self.is_animating:
                dot_text = "." * (dots % 4)
                try:
                    self.dots_label.configure(text=dot_text)
                    self.parent.update()
                    time.sleep(0.5)
                    dots += 1
                except:
                    break
        
        threading.Thread(target=animate_dots, daemon=True).start()
    
    def stop_animation(self):
        """Stop loading animation"""
        self.is_animating = False
        self.dots_label.configure(text="")
    
    def set_progress(self, value, status=""):
        """Update progress"""
        self.progress_bar.set(value)
        if status:
            self.status_label.configure(text=status)
    
    def pack(self, **kwargs):
        self.container.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.container.grid(**kwargs)

class ModernCard:
    """Reusable card component"""
    
    def __init__(self, parent, title="", description="", icon=None):
        self.container = ctk.CTkFrame(
            parent,
            fg_color=ModernTheme.CARD,
            corner_radius=ModernTheme.RADIUS,
            border_width=1,
            border_color=ModernTheme.BORDER
        )
        
        # Header
        if title or icon:
            header = ctk.CTkFrame(self.container, fg_color="transparent")
            header.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=(ModernTheme.SPACE_LG, ModernTheme.SPACE_SM))
            
            if icon:
                icon_label = ctk.CTkLabel(header, image=icon, text="")
                icon_label.pack(side="left", padx=(0, ModernTheme.SPACE_SM))
            
            if title:
                title_label = ctk.CTkLabel(
                    header,
                    text=title,
                    font=ModernTheme.FONT_SUBHEADING,
                    text_color=ModernTheme.TEXT
                )
                title_label.pack(side="left")
        
        # Description
        if description:
            desc_label = ctk.CTkLabel(
                self.container,
                text=description,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED,
                wraplength=400,
                justify="left"
            )
            desc_label.pack(anchor="w", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_MD))
        
        # Content area
        self.content = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_LG))
    
    def pack(self, **kwargs):
        self.container.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.container.grid(**kwargs)

class EnhancedReportGenerator:
    """Advanced report generation with charts and analytics"""
    
    def __init__(self, results_data):
        self.results = results_data
        self.charts_data = {}
    
    def generate_summary_stats(self):
        """Generate summary statistics"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() 
                          if r.get("Trạng thái") == "Tốt")
        failed_tests = sum(1 for r in self.results.values() 
                          if r.get("Trạng thái") == "Lỗi")
        warnings = sum(1 for r in self.results.values() 
                      if r.get("Trạng thái") == "Cảnh báo")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warnings,
            "success_rate": success_rate
        }
    
    def create_visual_report(self, parent):
        """Create visual report with charts"""
        stats = self.generate_summary_stats()
        
        # Report container
        report_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=ModernTheme.BACKGROUND,
            corner_radius=0
        )
        report_frame.pack(fill="both", expand=True)
        
        # Header
        header_card = ModernCard(
            report_frame,
            title="📊 Báo Cáo Kiểm Tra Laptop",
            description=f"Tổng hợp kết quả kiểm tra - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        header_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Summary stats
        stats_frame = ctk.CTkFrame(report_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_LG))
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Stat cards
        stat_items = [
            ("📋 Tổng Test", str(stats["total"]), ModernTheme.PRIMARY),
            ("✅ Đạt", f"{stats['passed']}/{stats['total']}", ModernTheme.SUCCESS),
            ("⚠️ Cảnh Báo", str(stats["warnings"]), ModernTheme.WARNING),
            ("❌ Lỗi", str(stats["failed"]), ModernTheme.ERROR)
        ]
        
        for i, (label, value, color) in enumerate(stat_items):
            stat_card = ctk.CTkFrame(
                stats_frame,
                fg_color=ModernTheme.CARD,
                corner_radius=ModernTheme.RADIUS,
                border_width=1,
                border_color=ModernTheme.BORDER
            )
            stat_card.grid(row=0, column=i, padx=ModernTheme.SPACE_SM, pady=0, sticky="ew")
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=ModernTheme.FONT_CAPTION,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(pady=(ModernTheme.SPACE_MD, ModernTheme.SPACE_XS))
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=ModernTheme.FONT_HEADING,
                text_color=color
            ).pack(pady=(0, ModernTheme.SPACE_MD))
        
        # Success rate indicator
        rate_card = ModernCard(
            report_frame,
            title="📈 Tỷ Lệ Thành Công",
            description=f"Hệ thống đạt {stats['success_rate']:.1f}% các test cơ bản"
        )
        rate_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_LG))
        
        # Progress bar for success rate
        rate_progress = ctk.CTkProgressBar(
            rate_card.content,
            width=400,
            height=12,
            progress_color=ModernTheme.SUCCESS if stats['success_rate'] > 80 else ModernTheme.WARNING
        )
        rate_progress.set(stats['success_rate'] / 100)
        rate_progress.pack(pady=ModernTheme.SPACE_MD)
        
        # Detailed results
        details_card = ModernCard(
            report_frame,
            title="📋 Chi Tiết Kết Quả",
            description="Kết quả từng bước kiểm tra"
        )
        details_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_LG))
        
        for step_name, result in self.results.items():
            self.create_result_item(details_card.content, step_name, result)
        
        # Recommendations
        self.create_recommendations(report_frame, stats)
        
        return report_frame
    
    def create_result_item(self, parent, step_name, result):
        """Create individual result item"""
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=ModernTheme.BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=ModernTheme.BORDER
        )
        item_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
        
        # Status colors
        status = result.get("Trạng thái", "Không rõ")
        status_colors = {
            "Tốt": ModernTheme.SUCCESS,
            "Lỗi": ModernTheme.ERROR,
            "Cảnh báo": ModernTheme.WARNING,
            "Bỏ qua": ModernTheme.TEXT_MUTED
        }
        status_color = status_colors.get(status, ModernTheme.TEXT_MUTED)
        
        # Status icons
        status_icons = {
            "Tốt": "✅",
            "Lỗi": "❌",
            "Cảnh báo": "⚠️",
            "Bỏ qua": "⏭️"
        }
        status_icon = status_icons.get(status, "❓")
        
        # Header
        header = ctk.CTkFrame(item_frame, fg_color="transparent")
        header.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
        
        ctk.CTkLabel(
            header,
            text=f"{status_icon} {step_name}",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.TEXT
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=status,
            font=ModernTheme.FONT_BODY,
            text_color=status_color
        ).pack(side="right")
        
        # Result details
        if result.get("Kết quả"):
            ctk.CTkLabel(
                item_frame,
                text=f"Kết quả: {result['Kết quả']}",
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=(0, ModernTheme.SPACE_SM))
        
        if result.get("Chi tiết"):
            detail_text = result["Chi tiết"]
            if len(detail_text) > 100:
                detail_text = detail_text[:100] + "..."
            
            ctk.CTkLabel(
                item_frame,
                text=f"Chi tiết: {detail_text}",
                font=ModernTheme.FONT_CAPTION,
                text_color=ModernTheme.TEXT_MUTED,
                wraplength=600
            ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=(0, ModernTheme.SPACE_MD))
    
    def create_recommendations(self, parent, stats):
        """Create recommendations based on results"""
        recommendations = []
        
        if stats["failed"] > 0:
            recommendations.append("🔧 Có lỗi nghiêm trọng cần khắc phục trước khi sử dụng")
        
        if stats["warnings"] > 0:
            recommendations.append("⚠️ Có cảnh báo cần theo dõi trong quá trình sử dụng")
        
        if stats["success_rate"] > 90:
            recommendations.append("✨ Laptop trong tình trạng rất tốt, an toàn để sử dụng")
        elif stats["success_rate"] > 70:
            recommendations.append("👍 Laptop hoạt động ổn định với một số lưu ý nhỏ")
        else:
            recommendations.append("⚠️ Laptop có nhiều vấn đề, cần cân nhắc kỹ trước khi mua")
        
        if recommendations:
            rec_card = ModernCard(
                parent,
                title="💡 Khuyến Nghị",
                description="Đánh giá tổng thể và khuyến nghị sử dụng"
            )
            rec_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_LG))
            
            for rec in recommendations:
                rec_item = ctk.CTkFrame(
                    rec_card.content,
                    fg_color=ModernTheme.BACKGROUND,
                    corner_radius=8
                )
                rec_item.pack(fill="x", pady=ModernTheme.SPACE_XS)
                
                ctk.CTkLabel(
                    rec_item,
                    text=rec,
                    font=ModernTheme.FONT_BODY,
                    text_color=ModernTheme.TEXT,
                    wraplength=600
                ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)

class EnhancedTestFeatures:
    """Enhanced test features with better UX"""
    
    @staticmethod
    def create_interactive_keyboard_test(parent):
        """Enhanced keyboard test with visual feedback"""
        test_frame = ctk.CTkFrame(parent, fg_color=ModernTheme.CARD)
        test_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Title
        ctk.CTkLabel(
            test_frame,
            text="⌨️ Test Bàn Phím Tương Tác",
            font=ModernTheme.FONT_HEADING,
            text_color=ModernTheme.TEXT
        ).pack(pady=ModernTheme.SPACE_LG)
        
        # Instructions
        instructions = ctk.CTkLabel(
            test_frame,
            text="Nhấn các phím trên bàn phím. Phím được nhấn sẽ sáng lên màu xanh.",
            font=ModernTheme.FONT_BODY,
            text_color=ModernTheme.TEXT_MUTED
        )
        instructions.pack(pady=(0, ModernTheme.SPACE_LG))
        
        # Keyboard layout
        keyboard_frame = ctk.CTkFrame(test_frame, fg_color=ModernTheme.BACKGROUND)
        keyboard_frame.pack(padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Create virtual keyboard
        key_widgets = {}
        pressed_keys = set()
        
        # Key rows
        key_rows = [
            ['Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'],
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Win', 'Menu', 'Ctrl']
        ]
        
        for row_idx, keys in enumerate(key_rows):
            row_frame = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
            row_frame.pack(pady=2)
            
            for key in keys:
                key_btn = ctk.CTkLabel(
                    row_frame,
                    text=key,
                    width=40 if key != 'Space' else 200,
                    height=30,
                    fg_color=ModernTheme.BORDER,
                    text_color=ModernTheme.TEXT,
                    corner_radius=4,
                    font=ModernTheme.FONT_CAPTION
                )
                key_btn.pack(side="left", padx=1)
                key_widgets[key.lower()] = key_btn
        
        # Key event handling
        def on_key_press(event):
            key = event.keysym.lower()
            if key in key_widgets:
                key_widgets[key].configure(fg_color=ModernTheme.SUCCESS)
                pressed_keys.add(key)
        
        def on_key_release(event):
            key = event.keysym.lower()
            if key in key_widgets:
                key_widgets[key].configure(fg_color=ModernTheme.PRIMARY)
        
        # Bind events
        parent.bind("<KeyPress>", on_key_press)
        parent.bind("<KeyRelease>", on_key_release)
        parent.focus_set()
        
        # Results
        results_frame = ctk.CTkFrame(test_frame, fg_color=ModernTheme.BACKGROUND)
        results_frame.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        pressed_label = ctk.CTkLabel(
            results_frame,
            text="Phím đã nhấn: 0",
            font=ModernTheme.FONT_BODY,
            text_color=ModernTheme.TEXT
        )
        pressed_label.pack(pady=ModernTheme.SPACE_SM)
        
        # Update counter
        def update_counter():
            pressed_label.configure(text=f"Phím đã nhấn: {len(pressed_keys)}")
            parent.after(100, update_counter)
        
        update_counter()
        
        return test_frame
    
    @staticmethod
    def create_advanced_display_test(parent):
        """Advanced display test with multiple patterns"""
        test_frame = ctk.CTkFrame(parent, fg_color=ModernTheme.CARD)
        test_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Title
        ctk.CTkLabel(
            test_frame,
            text="🖥️ Test Màn Hình Nâng Cao",
            font=ModernTheme.FONT_HEADING,
            text_color=ModernTheme.TEXT
        ).pack(pady=ModernTheme.SPACE_LG)
        
        # Test patterns
        patterns = [
            ("Solid Colors", "Test màu đơn sắc"),
            ("Gradient", "Test chuyển màu"),
            ("Pixel Test", "Test điểm ảnh"),
            ("Geometry", "Test hình học"),
            ("Text Clarity", "Test độ rõ chữ")
        ]
        
        for pattern_name, description in patterns:
            pattern_btn = ctk.CTkButton(
                test_frame,
                text=f"{pattern_name}\n{description}",
                height=60,
                font=ModernTheme.FONT_BODY,
                fg_color=ModernTheme.PRIMARY,
                hover_color=ModernTheme.PRIMARY_HOVER,
                command=lambda p=pattern_name: EnhancedTestFeatures.run_display_pattern(p)
            )
            pattern_btn.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_SM)
        
        return test_frame
    
    @staticmethod
    def run_display_pattern(pattern_name):
        """Run specific display test pattern"""
        # Create fullscreen test window
        test_window = tk.Toplevel()
        test_window.attributes('-fullscreen', True)
        test_window.attributes('-topmost', True)
        test_window.configure(bg='black')
        
        # Instructions
        instruction_label = tk.Label(
            test_window,
            text=f"Test Pattern: {pattern_name}\nNhấn ESC để thoát",
            font=("Segoe UI", 16),
            fg="white",
            bg="black"
        )
        instruction_label.pack(pady=20)
        
        # Pattern canvas
        canvas = tk.Canvas(
            test_window,
            bg='black',
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        
        # Pattern implementations
        if pattern_name == "Solid Colors":
            EnhancedTestFeatures.draw_solid_colors(canvas)
        elif pattern_name == "Gradient":
            EnhancedTestFeatures.draw_gradient(canvas)
        elif pattern_name == "Pixel Test":
            EnhancedTestFeatures.draw_pixel_test(canvas)
        elif pattern_name == "Geometry":
            EnhancedTestFeatures.draw_geometry(canvas)
        elif pattern_name == "Text Clarity":
            EnhancedTestFeatures.draw_text_clarity(canvas)
        
        # Close on ESC
        def close_test(event=None):
            test_window.destroy()
        
        test_window.bind('<Escape>', close_test)
        test_window.focus_set()
    
    @staticmethod
    def draw_solid_colors(canvas):
        """Draw solid color patterns"""
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFFFF', '#000000', '#FFFF00', '#FF00FF', '#00FFFF']
        current_color = [0]
        
        def next_color():
            canvas.configure(bg=colors[current_color[0]])
            current_color[0] = (current_color[0] + 1) % len(colors)
            canvas.after(2000, next_color)
        
        next_color()
    
    @staticmethod
    def draw_gradient(canvas):
        """Draw gradient patterns"""
        def update_gradient():
            canvas.delete("all")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            for i in range(width):
                color_val = int(255 * i / width)
                color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"
                canvas.create_line(i, 0, i, height, fill=color, width=1)
            
            canvas.after(100, update_gradient)
        
        canvas.after(100, update_gradient)
    
    @staticmethod
    def draw_pixel_test(canvas):
        """Draw pixel test pattern"""
        def update_pixels():
            canvas.delete("all")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Checkerboard pattern
            for x in range(0, width, 2):
                for y in range(0, height, 2):
                    if (x + y) % 4 == 0:
                        canvas.create_rectangle(x, y, x+2, y+2, fill="white", outline="")
            
            canvas.after(100, update_pixels)
        
        canvas.after(100, update_pixels)
    
    @staticmethod
    def draw_geometry(canvas):
        """Draw geometric patterns"""
        def update_geometry():
            canvas.delete("all")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Draw concentric circles
            center_x, center_y = width // 2, height // 2
            for i in range(10):
                radius = (i + 1) * 30
                color = "white" if i % 2 == 0 else "black"
                canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    outline=color, width=2
                )
            
            canvas.after(100, update_geometry)
        
        canvas.after(100, update_geometry)
    
    @staticmethod
    def draw_text_clarity(canvas):
        """Draw text clarity test"""
        def update_text():
            canvas.delete("all")
            canvas.configure(bg="white")
            
            # Different font sizes
            sizes = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32]
            y_pos = 50
            
            for size in sizes:
                canvas.create_text(
                    100, y_pos,
                    text=f"Font size {size}px - The quick brown fox jumps over the lazy dog",
                    font=("Segoe UI", size),
                    fill="black",
                    anchor="w"
                )
                y_pos += size + 10
        
        canvas.after(100, update_text)

# Export classes for use in main application
__all__ = [
    'ModernTheme',
    'AnimationHelper', 
    'NotificationToast',
    'ProgressIndicator',
    'ModernCard',
    'EnhancedReportGenerator',
    'EnhancedTestFeatures'
]