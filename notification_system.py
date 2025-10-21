# -*- coding: utf-8 -*-
"""
Advanced Notification System for LaptopTester
Hệ thống thông báo nâng cao với toast, alerts và progress
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional, Callable, Dict, Any
import threading
import time
from enum import Enum
from dataclasses import dataclass

try:
    from laptoptester import Theme
except ImportError:
    class Theme:
        BACKGROUND = "#FAFBFC"
        FRAME = "#FFFFFF"
        ACCENT = "#4299E1"
        SUCCESS = "#38A169"
        WARNING = "#D69E2E"
        ERROR = "#E53E3E"
        INFO = "#3182CE"
        TEXT = "#1A202C"
        TEXT_SECONDARY = "#718096"
        HEADING_FONT = ("Segoe UI", 24, "bold")
        SUBHEADING_FONT = ("Segoe UI", 18, "bold")
        BODY_FONT = ("Segoe UI", 14)
        SMALL_FONT = ("Segoe UI", 12)
        CORNER_RADIUS = 12

class NotificationType(Enum):
    """Notification types"""
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"

@dataclass
class NotificationConfig:
    """Notification configuration"""
    title: str
    message: str
    type: NotificationType
    duration: int = 3000  # milliseconds
    show_progress: bool = False
    closable: bool = True
    action_text: Optional[str] = None
    action_callback: Optional[Callable] = None

class ToastNotification(ctk.CTkToplevel):
    """Toast notification popup"""
    
    def __init__(self, parent, config: NotificationConfig):
        super().__init__(parent)
        self.config = config
        self.setup_window()
        self.setup_ui()
        self.animate_in()
        
        if config.duration > 0:
            self.after(config.duration, self.animate_out)
    
    def setup_window(self):
        """Setup window properties"""
        self.withdraw()  # Hide initially
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Always on top
        
        # Position at bottom right
        self.update_idletasks()
        width = 350
        height = 120
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = screen_width - width - 20
        y = screen_height - height - 60
        
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Setup UI elements"""
        # Color scheme based on type
        colors = {
            NotificationType.SUCCESS: {"bg": "#D4EDDA", "border": "#C3E6CB", "text": "#155724", "icon": "✅"},
            NotificationType.WARNING: {"bg": "#FFF3CD", "border": "#FFEAA7", "text": "#856404", "icon": "⚠️"},
            NotificationType.ERROR: {"bg": "#F8D7DA", "border": "#F5C6CB", "text": "#721C24", "icon": "❌"},
            NotificationType.INFO: {"bg": "#D1ECF1", "border": "#BEE5EB", "text": "#0C5460", "icon": "ℹ️"}
        }
        
        color_config = colors[self.config.type]
        
        # Main frame
        main_frame = ctk.CTkFrame(
            self, 
            fg_color=color_config["bg"],
            border_width=2,
            border_color=color_config["border"],
            corner_radius=Theme.CORNER_RADIUS
        )
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Content frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Icon
        icon_label = ctk.CTkLabel(
            content_frame, 
            text=color_config["icon"], 
            font=("Segoe UI", 24),
            text_color=color_config["text"]
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="n")
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=self.config.title,
            font=("Segoe UI", 14, "bold"),
            text_color=color_config["text"]
        )
        title_label.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        
        # Message
        message_label = ctk.CTkLabel(
            content_frame,
            text=self.config.message,
            font=Theme.SMALL_FONT,
            text_color=color_config["text"],
            wraplength=250,
            justify="left"
        )
        message_label.grid(row=1, column=1, sticky="ew")
        
        # Close button
        if self.config.closable:
            close_btn = ctk.CTkButton(
                content_frame,
                text="×",
                width=20,
                height=20,
                font=("Segoe UI", 16, "bold"),
                fg_color="transparent",
                text_color=color_config["text"],
                hover_color=color_config["border"],
                command=self.animate_out
            )
            close_btn.grid(row=0, column=2, padx=(10, 0), sticky="ne")
        
        # Action button
        if self.config.action_text and self.config.action_callback:
            action_btn = ctk.CTkButton(
                content_frame,
                text=self.config.action_text,
                height=25,
                font=Theme.SMALL_FONT,
                fg_color=color_config["text"],
                hover_color=self.darken_color(color_config["text"]),
                command=self.handle_action
            )
            action_btn.grid(row=2, column=1, pady=(10, 0), sticky="e")
        
        # Progress bar
        if self.config.show_progress and self.config.duration > 0:
            self.progress_bar = ctk.CTkProgressBar(
                main_frame,
                height=3,
                progress_color=color_config["text"],
                fg_color=color_config["border"]
            )
            self.progress_bar.pack(fill="x", side="bottom")
            self.progress_bar.set(0)
            self.animate_progress()
    
    def animate_in(self):
        """Animate notification in"""
        self.deiconify()
        self.attributes("-alpha", 0)
        
        def fade_in():
            alpha = 0
            while alpha < 1:
                alpha += 0.1
                try:
                    self.attributes("-alpha", alpha)
                    time.sleep(0.02)
                except:
                    break
        
        threading.Thread(target=fade_in, daemon=True).start()
    
    def animate_out(self):
        """Animate notification out"""
        def fade_out():
            alpha = 1
            while alpha > 0:
                alpha -= 0.1
                try:
                    self.attributes("-alpha", alpha)
                    time.sleep(0.02)
                except:
                    break
            try:
                self.destroy()
            except:
                pass
        
        threading.Thread(target=fade_out, daemon=True).start()
    
    def animate_progress(self):
        """Animate progress bar"""
        if not hasattr(self, 'progress_bar'):
            return
        
        def update_progress():
            start_time = time.time()
            duration_seconds = self.config.duration / 1000
            
            while time.time() - start_time < duration_seconds:
                try:
                    elapsed = time.time() - start_time
                    progress = elapsed / duration_seconds
                    self.progress_bar.set(progress)
                    time.sleep(0.05)
                except:
                    break
        
        threading.Thread(target=update_progress, daemon=True).start()
    
    def handle_action(self):
        """Handle action button click"""
        if self.config.action_callback:
            self.config.action_callback()
        self.animate_out()
    
    def darken_color(self, color: str) -> str:
        """Darken a color for hover effect"""
        # Simple color darkening - in real app, use proper color manipulation
        color_map = {
            "#155724": "#0d3d17",
            "#856404": "#6b5203",
            "#721C24": "#5a161c",
            "#0C5460": "#094349"
        }
        return color_map.get(color, color)

class ProgressDialog(ctk.CTkToplevel):
    """Progress dialog for long operations"""
    
    def __init__(self, parent, title: str, message: str, cancelable: bool = True):
        super().__init__(parent)
        self.title_text = title
        self.message_text = message
        self.cancelable = cancelable
        self.cancelled = False
        self.cancel_callback: Optional[Callable] = None
        
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Setup window properties"""
        self.title(self.title_text)
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(self.master)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 200
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 100
        self.geometry(f"400x200+{x}+{y}")
    
    def setup_ui(self):
        """Setup UI elements"""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=self.title_text,
            font=Theme.SUBHEADING_FONT,
            text_color=Theme.ACCENT
        )
        title_label.pack(pady=(20, 10))
        
        # Message
        self.message_label = ctk.CTkLabel(
            main_frame,
            text=self.message_text,
            font=Theme.BODY_FONT,
            text_color=Theme.TEXT,
            wraplength=350
        )
        self.message_label.pack(pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            width=300,
            height=20,
            progress_color=Theme.ACCENT
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        
        # Progress text
        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="0%",
            font=Theme.BODY_FONT,
            text_color=Theme.TEXT_SECONDARY
        )
        self.progress_label.pack()
        
        # Cancel button
        if self.cancelable:
            self.cancel_btn = ctk.CTkButton(
                main_frame,
                text="Hủy",
                command=self.cancel_operation,
                fg_color=Theme.ERROR,
                height=Theme.BUTTON_HEIGHT
            )
            self.cancel_btn.pack(pady=(20, 10))
    
    def update_progress(self, progress: float, message: Optional[str] = None):
        """Update progress (0.0 to 1.0)"""
        try:
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"{int(progress * 100)}%")
            
            if message:
                self.message_label.configure(text=message)
            
            self.update()
        except:
            pass
    
    def cancel_operation(self):
        """Cancel the operation"""
        self.cancelled = True
        if self.cancel_callback:
            self.cancel_callback()
        self.destroy()
    
    def set_cancel_callback(self, callback: Callable):
        """Set cancel callback"""
        self.cancel_callback = callback
    
    def is_cancelled(self) -> bool:
        """Check if operation was cancelled"""
        return self.cancelled

class NotificationManager:
    """Centralized notification management"""
    
    def __init__(self, parent):
        self.parent = parent
        self.active_toasts = []
        self.max_toasts = 5
    
    def show_toast(self, title: str, message: str, type: NotificationType = NotificationType.INFO, 
                   duration: int = 3000, action_text: Optional[str] = None, 
                   action_callback: Optional[Callable] = None):
        """Show toast notification"""
        config = NotificationConfig(
            title=title,
            message=message,
            type=type,
            duration=duration,
            show_progress=True,
            action_text=action_text,
            action_callback=action_callback
        )
        
        # Limit number of active toasts
        if len(self.active_toasts) >= self.max_toasts:
            oldest = self.active_toasts.pop(0)
            try:
                oldest.destroy()
            except:
                pass
        
        toast = ToastNotification(self.parent, config)
        self.active_toasts.append(toast)
        
        # Remove from list when destroyed
        def on_destroy():
            if toast in self.active_toasts:
                self.active_toasts.remove(toast)
        
        toast.bind("<Destroy>", lambda e: on_destroy())
        
        return toast
    
    def show_success(self, title: str, message: str, **kwargs):
        """Show success notification"""
        return self.show_toast(title, message, NotificationType.SUCCESS, **kwargs)
    
    def show_warning(self, title: str, message: str, **kwargs):
        """Show warning notification"""
        return self.show_toast(title, message, NotificationType.WARNING, **kwargs)
    
    def show_error(self, title: str, message: str, **kwargs):
        """Show error notification"""
        return self.show_toast(title, message, NotificationType.ERROR, **kwargs)
    
    def show_info(self, title: str, message: str, **kwargs):
        """Show info notification"""
        return self.show_toast(title, message, NotificationType.INFO, **kwargs)
    
    def show_progress_dialog(self, title: str, message: str, cancelable: bool = True) -> ProgressDialog:
        """Show progress dialog"""
        return ProgressDialog(self.parent, title, message, cancelable)
    
    def clear_all_toasts(self):
        """Clear all active toasts"""
        for toast in self.active_toasts[:]:
            try:
                toast.destroy()
            except:
                pass
        self.active_toasts.clear()

class NotificationTestFrame(ctk.CTkFrame):
    """Test frame for notification system"""
    
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.notification_manager = NotificationManager(master)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup test UI"""
        # Title
        ctk.CTkLabel(self, text="🔔 Notification System Test", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=30)
        
        # Toast buttons
        toast_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        toast_frame.pack(fill="x", padx=50, pady=20)
        
        ctk.CTkLabel(toast_frame, text="Toast Notifications", 
                    font=Theme.SUBHEADING_FONT).pack(pady=20)
        
        button_grid = ctk.CTkFrame(toast_frame, fg_color="transparent")
        button_grid.pack(pady=20)
        button_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Toast buttons
        ctk.CTkButton(button_grid, text="✅ Success", command=self.show_success_toast,
                     fg_color=Theme.SUCCESS).grid(row=0, column=0, padx=10, pady=10)
        
        ctk.CTkButton(button_grid, text="⚠️ Warning", command=self.show_warning_toast,
                     fg_color=Theme.WARNING).grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkButton(button_grid, text="❌ Error", command=self.show_error_toast,
                     fg_color=Theme.ERROR).grid(row=0, column=2, padx=10, pady=10)
        
        ctk.CTkButton(button_grid, text="ℹ️ Info", command=self.show_info_toast,
                     fg_color=Theme.INFO).grid(row=0, column=3, padx=10, pady=10)
        
        # Progress dialog
        progress_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        progress_frame.pack(fill="x", padx=50, pady=20)
        
        ctk.CTkLabel(progress_frame, text="Progress Dialog", 
                    font=Theme.SUBHEADING_FONT).pack(pady=20)
        
        ctk.CTkButton(progress_frame, text="🔄 Show Progress Dialog", 
                     command=self.show_progress_test,
                     fg_color=Theme.ACCENT, height=40).pack(pady=20)
        
        # Clear button
        ctk.CTkButton(self, text="🗑️ Clear All Notifications", 
                     command=self.notification_manager.clear_all_toasts,
                     fg_color="#6B7280").pack(pady=20)
    
    def show_success_toast(self):
        self.notification_manager.show_success(
            "Test Completed", 
            "All tests passed successfully!",
            action_text="View Report",
            action_callback=lambda: print("View report clicked")
        )
    
    def show_warning_toast(self):
        self.notification_manager.show_warning(
            "Warning Detected", 
            "Some tests completed with warnings. Please review the results."
        )
    
    def show_error_toast(self):
        self.notification_manager.show_error(
            "Test Failed", 
            "Critical error detected during hardware test. Check system immediately."
        )
    
    def show_info_toast(self):
        self.notification_manager.show_info(
            "Information", 
            "Test is running in background. Please wait for completion."
        )
    
    def show_progress_test(self):
        """Show progress dialog test"""
        dialog = self.notification_manager.show_progress_dialog(
            "Running Tests", 
            "Initializing hardware tests...", 
            cancelable=True
        )
        
        def simulate_progress():
            for i in range(101):
                if dialog.is_cancelled():
                    break
                
                progress = i / 100
                messages = [
                    "Initializing hardware tests...",
                    "Testing CPU performance...",
                    "Checking memory integrity...",
                    "Validating storage devices...",
                    "Finalizing test results..."
                ]
                
                message_index = min(int(progress * len(messages)), len(messages) - 1)
                dialog.update_progress(progress, messages[message_index])
                
                time.sleep(0.05)
            
            if not dialog.is_cancelled():
                dialog.destroy()
                self.notification_manager.show_success("Complete", "All tests completed successfully!")
        
        threading.Thread(target=simulate_progress, daemon=True).start()

if __name__ == "__main__":
    # Test notification system
    app = ctk.CTk()
    app.title("Notification System Test")
    app.geometry("800x600")
    
    frame = NotificationTestFrame(app)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()