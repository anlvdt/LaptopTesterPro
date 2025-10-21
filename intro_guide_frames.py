# -*- coding: utf-8 -*-
"""
Intro and Guide Frames for LaptopTester
Các màn hình giới thiệu và hướng dẫn chi tiết
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image
import webbrowser
import threading
import time

# Import theme and utilities from main app
try:
    from laptoptester import Theme, get_text, CURRENT_LANG
except ImportError:
    # Fallback theme if import fails
    class Theme:
        BACKGROUND = "#FAFBFC"
        FRAME = "#FFFFFF"
        CARD = "#F8FAFC"
        BORDER = "#E1E5E9"
        TEXT = "#1A202C"
        TEXT_SECONDARY = "#718096"
        ACCENT = "#4299E1"
        SUCCESS = "#38A169"
        WARNING = "#D69E2E"
        ERROR = "#E53E3E"
        TITLE_FONT = ("Segoe UI", 32, "bold")
        HEADING_FONT = ("Segoe UI", 24, "bold")
        SUBHEADING_FONT = ("Segoe UI", 18, "bold")
        BODY_FONT = ("Segoe UI", 14)
        SMALL_FONT = ("Segoe UI", 12)
        CORNER_RADIUS = 12
        PADDING_X = 20
        PADDING_Y = 16
        BUTTON_HEIGHT = 40
        CARD_PADDING = 16
        SECTION_SPACING = 12
        ELEMENT_SPACING = 8
    
    def get_text(key):
        return key
    
    CURRENT_LANG = "vi"

class IntroFrame(ctk.CTkFrame):
    """Màn hình giới thiệu ứng dụng"""
    
    def __init__(self, master, on_continue=None, on_skip=None):
        super().__init__(master, fg_color="transparent")
        self.on_continue = on_continue
        self.on_skip = on_skip
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_container = ctk.CTkScrollableFrame(self, fg_color=Theme.BACKGROUND)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Hero section with gradient background
        hero_frame = ctk.CTkFrame(main_container, fg_color="#667EEA", corner_radius=Theme.CORNER_RADIUS)
        hero_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        # Logo and title
        title_frame = ctk.CTkFrame(hero_frame, fg_color="transparent")
        title_frame.pack(pady=40)
        
        # Large logo/icon
        logo_label = ctk.CTkLabel(title_frame, text="💻", font=("Segoe UI", 80))
        logo_label.pack(pady=(0, 20))
        
        ctk.CTkLabel(title_frame, text="LaptopTester Pro", 
                    font=("Segoe UI", 36, "bold"), text_color="white").pack()
        
        ctk.CTkLabel(title_frame, text="Phần mềm kiểm tra laptop toàn diện hàng đầu Việt Nam", 
                    font=("Segoe UI", 18), text_color="#E2E8F0").pack(pady=(10, 0))
        
        # Version and build info
        version_frame = ctk.CTkFrame(hero_frame, fg_color="transparent")
        version_frame.pack(pady=(0, 30))
        
        ctk.CTkLabel(version_frame, text="Phiên bản 2.0 | Build 2024.12", 
                    font=Theme.BODY_FONT, text_color="#CBD5E0").pack()
        
        # Features overview
        features_frame = ctk.CTkFrame(main_container, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        features_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(features_frame, text="🌟 Tính năng nổi bật", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        # Features grid
        features_grid = ctk.CTkFrame(features_frame, fg_color="transparent")
        features_grid.pack(fill="x", padx=30, pady=(0, 30))
        features_grid.grid_columnconfigure((0, 1), weight=1)
        
        features = [
            ("🎨", "Giao diện hiện đại", "CustomTkinter với animation mượt mà"),
            ("📊", "Kiểm tra toàn diện", "15+ bước kiểm tra từ phần cứng đến phần mềm"),
            ("🔄", "Tự động hóa cao", "Tích hợp các tools chuyên nghiệp"),
            ("📱", "Responsive", "Giao diện thích ứng với nhiều kích thước màn hình"),
            ("🎯", "Báo cáo chi tiết", "Export kết quả dưới nhiều định dạng"),
            ("🔧", "Đa nền tảng", "Hỗ trợ Windows (tối ưu), Linux, macOS")
        ]
        
        for i, (icon, title, desc) in enumerate(features):
            row, col = i // 2, i % 2
            
            feature_card = ctk.CTkFrame(features_grid, fg_color=Theme.CARD, corner_radius=8)
            feature_card.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            # Icon
            ctk.CTkLabel(feature_card, text=icon, font=("Segoe UI", 24)).pack(pady=(15, 5))
            
            # Title
            ctk.CTkLabel(feature_card, text=title, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.TEXT).pack(pady=(0, 5))
            
            # Description
            ctk.CTkLabel(feature_card, text=desc, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=250, 
                        justify="center").pack(pady=(0, 15))
        
        # What's new section
        whats_new_frame = ctk.CTkFrame(main_container, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        whats_new_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(whats_new_frame, text="🆕 Có gì mới trong phiên bản 2.0", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        new_features = [
            "✨ Giao diện hoàn toàn mới với CustomTkinter",
            "🤖 Tích hợp AI phân tích model laptop",
            "📊 Biểu đồ real-time cho thermal monitoring",
            "🎥 Webcam test với phát hiện vật cản",
            "🔊 Audio test với waveform visualization",
            "⚡ Tối ưu hiệu năng và tốc độ test",
            "🌐 Hỗ trợ đa ngôn ngữ (Việt/English)",
            "📱 Responsive design cho nhiều độ phân giải"
        ]
        
        for feature in new_features:
            feature_item = ctk.CTkFrame(whats_new_frame, fg_color="transparent")
            feature_item.pack(fill="x", padx=30, pady=2)
            
            ctk.CTkLabel(feature_item, text=feature, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT).pack(anchor="w")
        
        # System requirements
        requirements_frame = ctk.CTkFrame(main_container, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        requirements_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(requirements_frame, text="💻 Yêu cầu hệ thống", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        req_grid = ctk.CTkFrame(requirements_frame, fg_color="transparent")
        req_grid.pack(fill="x", padx=30, pady=(0, 30))
        req_grid.grid_columnconfigure((0, 1), weight=1)
        
        requirements = [
            ("Hệ điều hành", "Windows 10/11 (khuyến nghị), Linux, macOS"),
            ("Python", "3.8 trở lên"),
            ("RAM", "4GB+ (8GB khuyến nghị)"),
            ("Ổ cứng", "500MB+ dung lượng trống"),
            ("Quyền truy cập", "Administrator (Windows) cho một số tính năng"),
            ("Kết nối", "Internet (cho AI analysis và updates)")
        ]
        
        for i, (label, value) in enumerate(requirements):
            row = i // 2
            col = i % 2
            
            req_item = ctk.CTkFrame(req_grid, fg_color=Theme.CARD, corner_radius=8)
            req_item.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            ctk.CTkLabel(req_item, text=label, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.ACCENT).pack(pady=(15, 5))
            
            ctk.CTkLabel(req_item, text=value, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=300, 
                        justify="center").pack(pady=(0, 15))
        
        # Action buttons
        self.create_action_buttons(main_container)
    
    def create_action_buttons(self, parent):
        """Tạo các nút hành động"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=30)
        
        # Continue button
        continue_btn = ctk.CTkButton(
            button_frame, 
            text="🚀 BẮt ĐẦU SỬ DỤNG", 
            command=self.handle_continue,
            font=("Segoe UI", 16, "bold"), 
            height=55, 
            corner_radius=28,
            fg_color="#16A34A", 
            hover_color="#15803D", 
            text_color="white",
            border_width=2, 
            border_color="white"
        )
        continue_btn.pack(side="left", padx=(0, 20), fill="x", expand=True)
        
        # Skip intro button
        skip_btn = ctk.CTkButton(
            button_frame, 
            text="⏭️ BỎ QUA GIỚI THIỆU", 
            command=self.handle_skip,
            font=("Segoe UI", 14, "bold"), 
            height=45, 
            corner_radius=22,
            fg_color="#6B7280", 
            hover_color="#4B5563", 
            text_color="white"
        )
        skip_btn.pack(side="right", padx=(20, 0))
    
    def handle_continue(self):
        """Xử lý khi nhấn Continue"""
        if self.on_continue:
            self.on_continue()
    
    def handle_skip(self):
        """Xử lý khi nhấn Skip"""
        if self.on_skip:
            self.on_skip()

class GuideFrame(ctk.CTkFrame):
    """Màn hình hướng dẫn sử dụng"""
    
    def __init__(self, master, on_back=None):
        super().__init__(master, fg_color="transparent")
        self.on_back = on_back
        self.setup_ui()
    
    def setup_ui(self):
        # Header with back button
        header_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80, corner_radius=Theme.CORNER_RADIUS)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame, 
            text="← QUAY LẠI", 
            command=self.handle_back,
            width=120, 
            height=40, 
            font=("Segoe UI", 12, "bold"),
            fg_color="#ED4245", 
            hover_color="#C73E41", 
            text_color="white",
            corner_radius=20, 
            border_width=2, 
            border_color="white"
        )
        back_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(header_frame, text="📖 HƯỚNG DẪN SỬ DỤNG", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=1, pady=20)
        
        # Main content
        main_container = ctk.CTkScrollableFrame(self, fg_color=Theme.BACKGROUND)
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Quick start guide
        self.create_quick_start_section(main_container)
        
        # Detailed guides
        self.create_detailed_guides_section(main_container)
        
        # Tips and tricks
        self.create_tips_section(main_container)
        
        # Troubleshooting
        self.create_troubleshooting_section(main_container)
    
    def create_quick_start_section(self, parent):
        """Tạo phần hướng dẫn nhanh"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="🚀 Bắt đầu nhanh", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        steps = [
            ("1️⃣", "Chọn chế độ", "Basic Mode cho người dùng thông thường, Expert Mode cho chuyên gia"),
            ("2️⃣", "Bắt đầu test", "Chọn 'Test Toàn Diện' hoặc 'Test Từng Phần'"),
            ("3️⃣", "Làm theo hướng dẫn", "Đọc kỹ hướng dẫn ở panel bên trái mỗi bước"),
            ("4️⃣", "Đánh giá kết quả", "Xem báo cáo tổng kết và export nếu cần")
        ]
        
        for icon, title, desc in steps:
            step_frame = ctk.CTkFrame(section_frame, fg_color=Theme.CARD, corner_radius=8)
            step_frame.pack(fill="x", padx=30, pady=8)
            
            content_frame = ctk.CTkFrame(step_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=20, pady=15)
            content_frame.grid_columnconfigure(1, weight=1)
            
            # Icon
            ctk.CTkLabel(content_frame, text=icon, font=("Segoe UI", 24)).grid(row=0, column=0, padx=(0, 15))
            
            # Title and description
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.grid(row=0, column=1, sticky="ew")
            
            ctk.CTkLabel(text_frame, text=title, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.TEXT).pack(anchor="w")
            ctk.CTkLabel(text_frame, text=desc, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=600).pack(anchor="w")
    
    def create_detailed_guides_section(self, parent):
        """Tạo phần hướng dẫn chi tiết"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="📋 Hướng dẫn chi tiết từng bước", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        # Create tabview for different test categories
        guide_tabview = ctk.CTkTabview(section_frame, width=800, height=400)
        guide_tabview.pack(padx=30, pady=(0, 30))
        
        # Basic tests tab
        guide_tabview.add("🔧 Tests Cơ Bản")
        basic_tab = guide_tabview.tab("🔧 Tests Cơ Bản")
        
        basic_tests = [
            ("Định danh phần cứng", "Đọc thông tin từ BIOS, khó làm giả. So sánh với quảng cáo."),
            ("Bản quyền Windows", "Kiểm tra license hợp lệ. Quan trọng cho updates bảo mật."),
            ("Cấu hình hệ thống", "So sánh thông tin Windows với BIOS để phát hiện sai lệch."),
            ("Sức khỏe ổ cứng", "Đọc S.M.A.R.T data để đánh giá độ bền ổ cứng."),
            ("Kiểm tra màn hình", "Test pixel chết, hở sáng, ám màu với các màu chuẩn."),
            ("Bàn phím & Touchpad", "Test từng phím và cử chỉ touchpad với visual feedback."),
            ("Cổng kết nối", "Kiểm tra USB, HDMI, audio, sạc với checklist chi tiết."),
            ("Pin laptop", "Đánh giá sức khỏe pin, chu kỳ sạc, dung lượng thực tế."),
            ("Loa & Micro", "Test âm thanh với waveform, phát hiện rè, méo tiếng."),
            ("Webcam", "Test camera với phát hiện vật cản và đánh giá chất lượng.")
        ]
        
        for test_name, description in basic_tests:
            test_item = ctk.CTkFrame(basic_tab, fg_color=Theme.BACKGROUND, corner_radius=6)
            test_item.pack(fill="x", padx=10, pady=4)
            
            ctk.CTkLabel(test_item, text=f"• {test_name}", font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.ACCENT).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(test_item, text=description, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=700).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Expert tests tab
        guide_tabview.add("🔥 Tests Chuyên Gia")
        expert_tab = guide_tabview.tab("🔥 Tests Chuyên Gia")
        
        expert_tests = [
            ("CPU Stress Test", "Đẩy CPU lên 100% tải để test thermal throttling và ổn định."),
            ("GPU Stress Test", "Test đồ họa nặng để phát hiện artifacts và quá nhiệt GPU."),
            ("Tốc độ ổ cứng", "Benchmark read/write speed thực tế với file test 100MB."),
            ("Thermal Monitor", "Giám sát nhiệt độ real-time với biểu đồ và cảnh báo."),
            ("Kiểm tra BIOS", "Hướng dẫn vào BIOS và kiểm tra các cài đặt quan trọng."),
            ("Kiểm tra ngoại hình", "Checklist chi tiết về tình trạng vật lý và dấu hiệu hư hỏng.")
        ]
        
        for test_name, description in expert_tests:
            test_item = ctk.CTkFrame(expert_tab, fg_color=Theme.BACKGROUND, corner_radius=6)
            test_item.pack(fill="x", padx=10, pady=4)
            
            ctk.CTkLabel(test_item, text=f"🔥 {test_name}", font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.ERROR).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(test_item, text=description, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=700).pack(anchor="w", padx=15, pady=(0, 10))
    
    def create_tips_section(self, parent):
        """Tạo phần mẹo và thủ thuật"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="💡 Mẹo và thủ thuật", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        tips = [
            ("🎯", "Đọc kết quả", "Xanh = Tốt, Vàng = Cảnh báo, Đỏ = Lỗi nghiêm trọng"),
            ("⚡", "Tối ưu test", "Chạy với quyền Admin để có kết quả chính xác nhất"),
            ("🔍", "So sánh thông tin", "Luôn đối chiếu với thông tin quảng cáo của người bán"),
            ("📊", "Export báo cáo", "Lưu kết quả để tham khảo sau hoặc gửi cho chuyên gia"),
            ("🛡️", "An toàn", "Tất cả tests đều non-destructive, không làm hỏng máy"),
            ("🔄", "Test lại", "Có thể chạy lại bất kỳ test nào nếu kết quả không chắc chắn")
        ]
        
        tips_grid = ctk.CTkFrame(section_frame, fg_color="transparent")
        tips_grid.pack(fill="x", padx=30, pady=(0, 30))
        tips_grid.grid_columnconfigure((0, 1), weight=1)
        
        for i, (icon, title, desc) in enumerate(tips):
            row, col = i // 2, i % 2
            
            tip_card = ctk.CTkFrame(tips_grid, fg_color=Theme.CARD, corner_radius=8)
            tip_card.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            ctk.CTkLabel(tip_card, text=icon, font=("Segoe UI", 24)).pack(pady=(15, 5))
            ctk.CTkLabel(tip_card, text=title, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.TEXT).pack(pady=(0, 5))
            ctk.CTkLabel(tip_card, text=desc, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=250, 
                        justify="center").pack(pady=(0, 15))
    
    def create_troubleshooting_section(self, parent):
        """Tạo phần khắc phục sự cố"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="🔧 Khắc phục sự cố", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        issues = [
            ("Import errors", "Cài đặt lại: pip install -r requirements.txt"),
            ("Permission denied", "Chạy với quyền Administrator (Run as Admin)"),
            ("Worker timeouts", "Tăng timeout trong settings hoặc restart app"),
            ("UI not responsive", "Update CustomTkinter: pip install --upgrade customtkinter"),
            ("Camera không hoạt động", "Kiểm tra driver camera và quyền truy cập"),
            ("Audio test lỗi", "Kiểm tra driver âm thanh và microphone permissions"),
            ("Stress test crash", "Giảm thời gian test hoặc kiểm tra thermal throttling"),
            ("BIOS không vào được", "Thử các phím khác: F2, F12, Del, ESC tùy hãng")
        ]
        
        for issue, solution in issues:
            issue_frame = ctk.CTkFrame(section_frame, fg_color=Theme.CARD, corner_radius=8)
            issue_frame.pack(fill="x", padx=30, pady=5)
            
            content_frame = ctk.CTkFrame(issue_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=20, pady=15)
            content_frame.grid_columnconfigure(1, weight=1)
            
            # Problem icon
            ctk.CTkLabel(content_frame, text="❌", font=("Segoe UI", 20)).grid(row=0, column=0, padx=(0, 15))
            
            # Problem and solution
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.grid(row=0, column=1, sticky="ew")
            
            ctk.CTkLabel(text_frame, text=f"Vấn đề: {issue}", font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.ERROR).pack(anchor="w")
            ctk.CTkLabel(text_frame, text=f"Giải pháp: {solution}", font=Theme.BODY_FONT, 
                        text_color=Theme.SUCCESS, wraplength=600).pack(anchor="w")
        
        # Contact support
        support_frame = ctk.CTkFrame(section_frame, fg_color="#E3F2FD", corner_radius=8)
        support_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        ctk.CTkLabel(support_frame, text="📞 Cần hỗ trợ thêm?", 
                    font=Theme.SUBHEADING_FONT, text_color="#1565C0").pack(pady=(15, 10))
        
        ctk.CTkLabel(support_frame, text="Email: support@laptoptester.com | GitHub Issues | Community Forum", 
                    font=Theme.BODY_FONT, text_color="#424242").pack(pady=(0, 15))
    
    def handle_back(self):
        """Xử lý khi nhấn Back"""
        if self.on_back:
            self.on_back()

class AboutFrame(ctk.CTkFrame):
    """Màn hình thông tin về ứng dụng"""
    
    def __init__(self, master, on_back=None):
        super().__init__(master, fg_color="transparent")
        self.on_back = on_back
        self.setup_ui()
    
    def setup_ui(self):
        # Header with back button
        header_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80, corner_radius=Theme.CORNER_RADIUS)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame, 
            text="← QUAY LẠI", 
            command=self.handle_back,
            width=120, 
            height=40, 
            font=("Segoe UI", 12, "bold"),
            fg_color="#ED4245", 
            hover_color="#C73E41", 
            text_color="white",
            corner_radius=20, 
            border_width=2, 
            border_color="white"
        )
        back_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(header_frame, text="ℹ️ THÔNG TIN ỨNG DỤNG", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=1, pady=20)
        
        # Main content
        main_container = ctk.CTkScrollableFrame(self, fg_color=Theme.BACKGROUND)
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # App info section
        self.create_app_info_section(main_container)
        
        # Team section
        self.create_team_section(main_container)
        
        # License section
        self.create_license_section(main_container)
        
        # Changelog section
        self.create_changelog_section(main_container)
    
    def create_app_info_section(self, parent):
        """Tạo phần thông tin ứng dụng"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        # App logo and basic info
        info_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        info_frame.pack(pady=30)
        
        # Large logo
        ctk.CTkLabel(info_frame, text="💻", font=("Segoe UI", 80)).pack(pady=(0, 20))
        
        ctk.CTkLabel(info_frame, text="LaptopTester Pro", 
                    font=("Segoe UI", 32, "bold"), text_color=Theme.ACCENT).pack()
        
        ctk.CTkLabel(info_frame, text="Phần mềm kiểm tra laptop toàn diện", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=(10, 20))
        
        # Version info
        version_grid = ctk.CTkFrame(section_frame, fg_color="transparent")
        version_grid.pack(fill="x", padx=30, pady=(0, 30))
        version_grid.grid_columnconfigure((0, 1), weight=1)
        
        version_info = [
            ("Phiên bản", "2.0.0"),
            ("Build", "2024.12.15"),
            ("Python", "3.8+"),
            ("Framework", "CustomTkinter"),
            ("Nền tảng", "Windows, Linux, macOS"),
            ("Giấy phép", "Commercial License")
        ]
        
        for i, (label, value) in enumerate(version_info):
            row, col = i // 2, i % 2
            
            info_card = ctk.CTkFrame(version_grid, fg_color=Theme.CARD, corner_radius=8)
            info_card.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            ctk.CTkLabel(info_card, text=label, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.ACCENT).pack(pady=(15, 5))
            ctk.CTkLabel(info_card, text=value, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT).pack(pady=(0, 15))
    
    def create_team_section(self, parent):
        """Tạo phần thông tin team"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="👥 Đội ngũ phát triển", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        team_members = [
            ("🧑‍💻", "Lead Developer", "Phát triển core engine và UI"),
            ("🎨", "UI/UX Designer", "Thiết kế giao diện và trải nghiệm người dùng"),
            ("🔬", "QA Engineer", "Kiểm thử chất lượng và tối ưu hiệu năng"),
            ("📝", "Technical Writer", "Viết tài liệu và hướng dẫn sử dụng")
        ]
        
        team_grid = ctk.CTkFrame(section_frame, fg_color="transparent")
        team_grid.pack(fill="x", padx=30, pady=(0, 30))
        team_grid.grid_columnconfigure((0, 1), weight=1)
        
        for i, (icon, role, desc) in enumerate(team_members):
            row, col = i // 2, i % 2
            
            member_card = ctk.CTkFrame(team_grid, fg_color=Theme.CARD, corner_radius=8)
            member_card.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            ctk.CTkLabel(member_card, text=icon, font=("Segoe UI", 32)).pack(pady=(20, 10))
            ctk.CTkLabel(member_card, text=role, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.TEXT).pack(pady=(0, 5))
            ctk.CTkLabel(member_card, text=desc, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY, wraplength=250, 
                        justify="center").pack(pady=(0, 20))
    
    def create_license_section(self, parent):
        """Tạo phần thông tin giấy phép"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="📄 Giấy phép và bản quyền", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        license_text = """
Copyright © 2024 LaptopTester Team. All rights reserved.

Phần mềm này được bảo vệ bởi luật bản quyền. Việc sử dụng, sao chép, 
phân phối hoặc chỉnh sửa phần mềm này cần có sự cho phép bằng văn bản 
từ LaptopTester Team.

Để sử dụng cho mục đích thương mại, vui lòng liên hệ:
📧 licensing@laptoptester.com
📱 Hotline: 1900-xxxx-xxx

Phần mềm được cung cấp "như hiện tại" mà không có bất kỳ bảo đảm nào.
        """
        
        license_display = ctk.CTkTextbox(section_frame, height=200, font=Theme.BODY_FONT, 
                                        fg_color=Theme.BACKGROUND, text_color=Theme.TEXT)
        license_display.pack(fill="x", padx=30, pady=(0, 30))
        license_display.insert("0.0", license_text.strip())
        license_display.configure(state="disabled")
    
    def create_changelog_section(self, parent):
        """Tạo phần changelog"""
        section_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        section_frame.pack(fill="x", pady=(0, Theme.SECTION_SPACING))
        
        ctk.CTkLabel(section_frame, text="📋 Lịch sử cập nhật", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        changelog_data = [
            ("v2.0.0", "2024-12-15", [
                "Giao diện hoàn toàn mới với CustomTkinter",
                "Tích hợp AI phân tích model laptop", 
                "Thêm thermal monitoring real-time",
                "Cải thiện webcam và audio tests",
                "Hỗ trợ đa ngôn ngữ"
            ]),
            ("v1.5.2", "2024-11-20", [
                "Sửa lỗi stress test trên một số CPU",
                "Cải thiện độ chính xác battery test",
                "Thêm hỗ trợ cho GPU mới"
            ]),
            ("v1.5.0", "2024-10-15", [
                "Thêm GPU stress test",
                "Cải thiện UI/UX",
                "Tối ưu hiệu năng"
            ])
        ]
        
        for version, date, changes in changelog_data:
            version_frame = ctk.CTkFrame(section_frame, fg_color=Theme.CARD, corner_radius=8)
            version_frame.pack(fill="x", padx=30, pady=8)
            
            # Version header
            header_frame = ctk.CTkFrame(version_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=(15, 10))
            header_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(header_frame, text=version, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.ACCENT).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(header_frame, text=date, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY).grid(row=0, column=1, sticky="e")
            
            # Changes list
            for change in changes:
                change_frame = ctk.CTkFrame(version_frame, fg_color="transparent")
                change_frame.pack(fill="x", padx=20, pady=2)
                
                ctk.CTkLabel(change_frame, text=f"• {change}", font=Theme.BODY_FONT, 
                            text_color=Theme.TEXT).pack(anchor="w")
            
            # Add bottom padding
            ctk.CTkFrame(version_frame, fg_color="transparent", height=10).pack()
    
    def handle_back(self):
        """Xử lý khi nhấn Back"""
        if self.on_back:
            self.on_back()

# Utility function to create home button
def create_home_button(parent, command, **kwargs):
    """Tạo nút Home chuẩn để quay về màn hình chính"""
    default_kwargs = {
        "text": "🏠 TRANG CHỦ",
        "font": ("Segoe UI", 12, "bold"),
        "width": 140,
        "height": 40,
        "fg_color": "#5865F2",
        "hover_color": "#4752C4",
        "text_color": "white",
        "corner_radius": 20,
        "border_width": 2,
        "border_color": "white",
        "command": command
    }
    default_kwargs.update(kwargs)
    
    return ctk.CTkButton(parent, **default_kwargs)

if __name__ == "__main__":
    # Test the frames
    app = ctk.CTk()
    app.title("Test Intro/Guide Frames")
    app.geometry("1200x800")
    
    def show_intro():
        frame = IntroFrame(app, on_continue=show_guide, on_skip=lambda: print("Skipped"))
        frame.pack(fill="both", expand=True)
    
    def show_guide():
        for widget in app.winfo_children():
            widget.destroy()
        frame = GuideFrame(app, on_back=show_intro)
        frame.pack(fill="both", expand=True)
    
    show_intro()
    app.mainloop()