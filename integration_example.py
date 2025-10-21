# Integration Example - How to use the enhanced UI/UX components
import customtkinter as ctk
import tkinter as tk
from ui_improvements import (
    ModernTheme, 
    AnimationHelper, 
    NotificationToast, 
    ProgressIndicator, 
    ModernCard,
    EnhancedReportGenerator,
    EnhancedTestFeatures
)
from enhanced_features import SystemMonitor, BenchmarkSuite, AdvancedDiagnostics
from report_generator import ReportGeneratorFrame

class EnhancedLaptopTesterApp(ctk.CTk):
    """Enhanced version of LaptopTester with modern UI/UX"""
    
    def __init__(self):
        super().__init__()
        
        # Apply modern theme
        self.configure(fg_color=ModernTheme.BACKGROUND)
        self.title("LaptopTester Pro - Enhanced Edition")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Initialize components
        self.setup_ui()
        self.setup_notifications()
        
        # Sample data for demonstration
        self.sample_results = {
            "Định danh phần cứng": {"Kết quả": "Thành công", "Trạng thái": "Tốt"},
            "Kiểm tra màn hình": {"Kết quả": "Hoạt động bình thường", "Trạng thái": "Tốt"},
            "Test CPU": {"Kết quả": "Nhiệt độ cao", "Trạng thái": "Cảnh báo"},
            "Kiểm tra pin": {"Kết quả": "Pin chai", "Trạng thái": "Lỗi"}
        }
    
    def setup_ui(self):
        """Setup main UI with enhanced components"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar with navigation
        self.create_sidebar()
        
        # Main content area
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
    
    def create_sidebar(self):
        """Create modern sidebar with navigation"""
        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            fg_color=ModernTheme.SURFACE,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.sidebar.grid_propagate(False)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(self.sidebar, fg_color=ModernTheme.PRIMARY)
        title_frame.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_LG)
        
        ctk.CTkLabel(
            title_frame,
            text="🔧 LaptopTester Pro",
            font=ModernTheme.FONT_HEADING,
            text_color="white"
        ).pack(pady=ModernTheme.SPACE_MD)
        
        # Navigation buttons
        nav_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("🔍 Quick Test", self.show_quick_test),
            ("📊 System Monitor", self.show_system_monitor),
            ("🏃♂️ Benchmarks", self.show_benchmarks),
            ("🔧 Diagnostics", self.show_diagnostics),
            ("📊 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings)
        ]
        
        self.nav_buttons = {}
        for text, command in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                anchor="w",
                height=ModernTheme.BUTTON_HEIGHT,
                fg_color="transparent",
                text_color=ModernTheme.TEXT,
                hover_color=ModernTheme.PRIMARY,
                font=ModernTheme.FONT_BODY
            )
            btn.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_XS)
            self.nav_buttons[text] = btn
        
        # Quick actions
        quick_frame = ctk.CTkFrame(self.sidebar, fg_color=ModernTheme.BACKGROUND)
        quick_frame.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_LG, side="bottom")
        
        ctk.CTkLabel(
            quick_frame,
            text="⚡ Quick Actions",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.TEXT
        ).pack(pady=(ModernTheme.SPACE_MD, ModernTheme.SPACE_SM))
        
        quick_actions = [
            ("🚀 Start Full Test", self.start_full_test),
            ("📤 Export Last Report", self.export_last_report)
        ]
        
        for text, command in quick_actions:
            ctk.CTkButton(
                quick_frame,
                text=text,
                command=command,
                height=36,
                fg_color=ModernTheme.SUCCESS,
                font=ModernTheme.FONT_CAPTION
            ).pack(fill="x", padx=ModernTheme.SPACE_SM, pady=ModernTheme.SPACE_XS)
    
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=ModernTheme.BACKGROUND,
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Content container
        self.content_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.content_container.grid(row=0, column=0, sticky="nsew", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ctk.CTkFrame(
            self,
            height=40,
            fg_color=ModernTheme.SURFACE,
            corner_radius=0
        )
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_bar.grid_propagate(False)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="✅ Ready",
            font=ModernTheme.FONT_CAPTION,
            text_color=ModernTheme.TEXT_MUTED
        )
        self.status_label.pack(side="left", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
        
        # Progress indicator
        self.progress_indicator = ProgressIndicator(self.status_bar)
        self.progress_indicator.pack(side="right", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
    
    def setup_notifications(self):
        """Setup notification system"""
        self.toast = NotificationToast(self)
    
    def clear_content(self):
        """Clear main content area"""
        for widget in self.content_container.winfo_children():
            widget.destroy()
    
    def update_nav_selection(self, selected_text):
        """Update navigation button selection"""
        for text, btn in self.nav_buttons.items():
            if text == selected_text:
                btn.configure(fg_color=ModernTheme.PRIMARY, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=ModernTheme.TEXT)
    
    def show_dashboard(self):
        """Show dashboard with overview"""
        self.clear_content()
        self.update_nav_selection("🏠 Dashboard")
        
        # Dashboard header
        header_card = ModernCard(
            self.content_container,
            title="🏠 Dashboard",
            description="Tổng quan hệ thống và trạng thái kiểm tra"
        )
        header_card.pack(fill="x", pady=(0, ModernTheme.SPACE_LG))
        
        # Stats grid
        stats_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, ModernTheme.SPACE_LG))
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Sample stats
        stats = [
            ("🔧 Tests Run", "24", ModernTheme.PRIMARY),
            ("✅ Passed", "18", ModernTheme.SUCCESS),
            ("⚠️ Warnings", "4", ModernTheme.WARNING),
            ("❌ Failed", "2", ModernTheme.ERROR)
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_card = ctk.CTkFrame(
                stats_frame,
                fg_color=ModernTheme.SURFACE,
                corner_radius=ModernTheme.RADIUS
            )
            stat_card.grid(row=0, column=i, padx=ModernTheme.SPACE_SM, sticky="ew")
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=ModernTheme.FONT_TITLE,
                text_color=color
            ).pack(pady=(ModernTheme.SPACE_LG, ModernTheme.SPACE_SM))
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(pady=(0, ModernTheme.SPACE_LG))
        
        # Recent activity
        activity_card = ModernCard(
            self.content_container,
            title="📋 Recent Activity",
            description="Hoạt động gần đây"
        )
        activity_card.pack(fill="both", expand=True)
        
        # Sample activity items
        activities = [
            ("✅ System Info Test completed", "2 minutes ago"),
            ("⚠️ CPU temperature warning", "5 minutes ago"),
            ("✅ Display test passed", "8 minutes ago"),
            ("❌ Battery health check failed", "12 minutes ago")
        ]
        
        for activity, time in activities:
            activity_item = ctk.CTkFrame(
                activity_card.content,
                fg_color=ModernTheme.BACKGROUND,
                corner_radius=8
            )
            activity_item.pack(fill="x", pady=ModernTheme.SPACE_XS)
            
            item_frame = ctk.CTkFrame(activity_item, fg_color="transparent")
            item_frame.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
            
            ctk.CTkLabel(
                item_frame,
                text=activity,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT
            ).pack(side="left")
            
            ctk.CTkLabel(
                item_frame,
                text=time,
                font=ModernTheme.FONT_CAPTION,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(side="right")
    
    def show_quick_test(self):
        """Show quick test interface"""
        self.clear_content()
        self.update_nav_selection("🔍 Quick Test")
        
        # Quick test interface
        test_card = ModernCard(
            self.content_container,
            title="🔍 Quick Test",
            description="Kiểm tra nhanh các tính năng cơ bản"
        )
        test_card.pack(fill="both", expand=True)
        
        # Test options
        test_options = [
            ("🖥️ Display Test", "Kiểm tra màn hình", self.run_display_test),
            ("⌨️ Keyboard Test", "Kiểm tra bàn phím", self.run_keyboard_test),
            ("🔊 Audio Test", "Kiểm tra âm thanh", self.run_audio_test),
            ("📷 Camera Test", "Kiểm tra webcam", self.run_camera_test)
        ]
        
        for title, desc, command in test_options:
            option_frame = ctk.CTkFrame(
                test_card.content,
                fg_color=ModernTheme.BACKGROUND,
                corner_radius=ModernTheme.RADIUS
            )
            option_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
            
            info_frame = ctk.CTkFrame(option_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
            
            ctk.CTkLabel(
                info_frame,
                text=title,
                font=ModernTheme.FONT_SUBHEADING,
                text_color=ModernTheme.TEXT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=desc,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w")
            
            ctk.CTkButton(
                option_frame,
                text="▶️ Run",
                command=command,
                width=100,
                height=ModernTheme.BUTTON_HEIGHT,
                fg_color=ModernTheme.PRIMARY
            ).pack(side="right", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
    
    def show_system_monitor(self):
        """Show system monitor"""
        self.clear_content()
        self.update_nav_selection("📊 System Monitor")
        
        # Create system monitor
        monitor = SystemMonitor(self.content_container)
        monitor_frame = monitor.create_monitor_ui()
    
    def show_benchmarks(self):
        """Show benchmark suite"""
        self.clear_content()
        self.update_nav_selection("🏃♂️ Benchmarks")
        
        # Create benchmark suite
        benchmark = BenchmarkSuite(self.content_container)
        benchmark_frame = benchmark.create_benchmark_ui()
    
    def show_diagnostics(self):
        """Show advanced diagnostics"""
        self.clear_content()
        self.update_nav_selection("🔧 Diagnostics")
        
        # Create diagnostics
        diagnostics = AdvancedDiagnostics(self.content_container)
        diag_frame = diagnostics.create_diagnostics_ui()
    
    def show_reports(self):
        """Show reports interface"""
        self.clear_content()
        self.update_nav_selection("📊 Reports")
        
        # Create report generator
        report_generator = ReportGeneratorFrame(self.content_container, self.sample_results)
        report_generator.pack(fill="both", expand=True)
    
    def show_settings(self):
        """Show settings interface"""
        self.clear_content()
        self.update_nav_selection("⚙️ Settings")
        
        settings_card = ModernCard(
            self.content_container,
            title="⚙️ Settings",
            description="Cấu hình ứng dụng"
        )
        settings_card.pack(fill="both", expand=True)
        
        # Sample settings
        settings_options = [
            ("🎨 Theme", "Dark/Light mode toggle"),
            ("🔔 Notifications", "Enable/disable notifications"),
            ("📊 Auto-save reports", "Automatically save test reports"),
            ("🚀 Performance mode", "Optimize for performance")
        ]
        
        for title, desc in settings_options:
            setting_frame = ctk.CTkFrame(
                settings_card.content,
                fg_color=ModernTheme.BACKGROUND
            )
            setting_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
            
            info_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
            
            ctk.CTkLabel(
                info_frame,
                text=title,
                font=ModernTheme.FONT_SUBHEADING,
                text_color=ModernTheme.TEXT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=desc,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w")
            
            ctk.CTkSwitch(
                setting_frame,
                text=""
            ).pack(side="right", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
    
    # Test methods
    def run_display_test(self):
        """Run display test with enhanced features"""
        self.toast.show("Starting display test...", "info")
        self.progress_indicator.start_animation("Running display test")
        
        # Simulate test
        self.after(2000, lambda: self.complete_test("Display test completed successfully!", "success"))
    
    def run_keyboard_test(self):
        """Run enhanced keyboard test"""
        # Create keyboard test window
        EnhancedTestFeatures.create_interactive_keyboard_test(self)
        self.toast.show("Keyboard test started", "info")
    
    def run_audio_test(self):
        """Run audio test"""
        self.toast.show("Audio test not implemented yet", "warning")
    
    def run_camera_test(self):
        """Run camera test"""
        self.toast.show("Camera test not implemented yet", "warning")
    
    def start_full_test(self):
        """Start full test suite"""
        self.toast.show("Full test suite started!", "success")
        self.progress_indicator.start_animation("Running full test suite")
        
        # Simulate full test
        self.after(5000, lambda: self.complete_test("Full test suite completed!", "success"))
    
    def export_last_report(self):
        """Export last report"""
        self.toast.show("Exporting report...", "info")
        # Simulate export
        self.after(1000, lambda: self.toast.show("Report exported successfully!", "success"))
    
    def complete_test(self, message, type):
        """Complete test with notification"""
        self.progress_indicator.stop_animation()
        self.toast.show(message, type)
        self.status_label.configure(text="✅ Test completed")

def main():
    """Run the enhanced application"""
    app = EnhancedLaptopTesterApp()
    app.mainloop()

if __name__ == "__main__":
    main()