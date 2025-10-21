"""
Màn hình tổng quan ứng dụng LaptopTester
Hiển thị thông tin về ứng dụng, tính năng, chế độ test
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image
import webbrowser

class Theme:
    BACKGROUND="#F0F2F5"; FRAME="#FFFFFF"; ACCENT="#007AFF"; SUCCESS="#34C759"
    TEXT="#1C1C1E"; TEXT_SECONDARY="#6D6D72"; BORDER="#D9D9D9"
    TITLE_FONT=("Segoe UI", 36, "bold"); HEADING_FONT=("Segoe UI", 24, "bold")
    SUBHEADING_FONT=("Segoe UI", 20, "bold"); BODY_FONT=("Segoe UI", 16)
    SMALL_FONT=("Segoe UI", 14); CORNER_RADIUS=16

class AppOverviewFrame(ctk.CTkFrame):
    def __init__(self, master, start_callback, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.start_callback = start_callback
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_main_content()
        self.create_footer()
    
    def create_header(self):
        """Tạo header chuyên nghiệp với logo và giới thiệu"""
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(30,15))
        
        # Main header content
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, pady=20)
        header_content.grid_columnconfigure((0,1), weight=1)
        
        # Left side - Logo và tiêu đề
        left_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=30)
        
        # Logo chuyên nghiệp
        logo_frame = ctk.CTkFrame(left_frame, width=100, height=100, fg_color="#667eea", corner_radius=20)
        logo_frame.pack(pady=(0,15))
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(logo_frame, text="💻", font=("Segoe UI", 48)).pack(expand=True)
        
        # Tiêu đề và slogan
        ctk.CTkLabel(left_frame, text="LaptopTester Pro", font=Theme.TITLE_FONT, text_color=Theme.ACCENT).pack(anchor="w")
        ctk.CTkLabel(left_frame, text="Giải pháp kiểm tra laptop chuyên nghiệp", font=Theme.HEADING_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(5,0))
        ctk.CTkLabel(left_frame, text="Version 2.0 Professional | Build 2024.10", font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", pady=(10,0))
        
        # Right side - Giới thiệu ngắn
        right_frame = ctk.CTkFrame(header_content, fg_color="#F8F9FF", corner_radius=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=30)
        
        ctk.CTkLabel(right_frame, text="🎯 Giới Thiệu LaptopTester", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(20,10))
        
        intro_text = (
            "LaptopTester là phần mềm kiểm tra laptop chuyên nghiệp được phát triển bởi Laptop Lê Ẩn và Gemini AI. "
            "Phần mềm đọc thông tin trực tiếp từ BIOS và firmware để chống lừa đảo cấu hình. "
            "Tính năng lấy cấu hình phần cứng từ BIOS giúp phát hiện thông tin giả mạo trong Windows, "
            "bảo vệ người mua khỏi các thủ đoạn lừa đảo phổ biến trong thị trường laptop cũ."
        )
        
        ctk.CTkLabel(right_frame, text=intro_text, font=Theme.BODY_FONT, text_color=Theme.TEXT, 
                    wraplength=400, justify="left").pack(padx=20, pady=(0,20))
    
    def create_main_content(self):
        """Tạo nội dung chính"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=15)
        main_frame.grid_columnconfigure((0,1), weight=1)
        main_frame.grid_rowconfigure((0,1), weight=1)
        
        # Features panel
        self.create_features_panel(main_frame)
        
        # Test modes panel  
        self.create_modes_panel(main_frame)
        
        # About panel
        self.create_about_panel(main_frame)
        
        # Quick start panel
        self.create_quickstart_panel(main_frame)
    
    def create_features_panel(self, parent):
        """Panel tính năng"""
        features_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        features_frame.grid(row=0, column=0, sticky="nsew", padx=(0,15), pady=(0,15))
        
        ctk.CTkLabel(features_frame, text="🚀 Tính Năng Nổi Bật", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(20,15))
        
        features = [
            "🔍 **Kiểm tra BIOS vs Windows**: Phát hiện thông tin giả mạo",
            "🛡️ **Chống lừa đảo**: Đọc trực tiếp từ phần cứng",
            "⚙️ **15+ Test chuyên sâu**: Từ cơ bản đến nâng cao", 
            "🤖 **AI Phân tích**: Gợi ý thông minh theo model laptop",
            "🎯 **2 Chế độ**: Basic (15p) và Expert (45p)",
            "📊 **Báo cáo PDF**: Xuất kết quả chuyên nghiệp",
            "⚡ **Stress Test**: CPU, GPU, RAM, SSD performance",
            "📈 **Benchmark**: So sánh với chuẩn công nghiệp"
        ]
        
        for feature in features:
            ctk.CTkLabel(features_frame, text=feature, font=Theme.BODY_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=3)
        
        ctk.CTkLabel(features_frame, text="", height=20).pack()  # Spacer
    
    def create_modes_panel(self, parent):
        """Panel chế độ test"""
        modes_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        modes_frame.grid(row=0, column=1, sticky="nsew", padx=(15,0), pady=(0,15))
        
        ctk.CTkLabel(modes_frame, text="🎯 Chế Độ Kiểm Tra", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(20,15))
        
        # Tại sao cần kiểm tra BIOS vs Windows?
        why_bios_frame = ctk.CTkFrame(modes_frame, fg_color="#E3F2FD", corner_radius=12)
        why_bios_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(why_bios_frame, text="🔍 Tại sao cần kiểm tra BIOS vs Windows?", font=Theme.SUBHEADING_FONT, text_color="#1565C0").pack(pady=(15,10))
        
        bios_reasons = [
            "• **BIOS khô giả mạo**: Thông tin từ firmware gốc, không thể chỉnh sửa",
            "• **Windows có thể bị hack**: Driver giả, software fake cấu hình",
            "• **Phát hiện sai lệch**: CPU, RAM, GPU thực tế vs quảng cáo",
            "• **Chống lừa đảo**: Bảo vệ người mua khỏi fake thông tin",
            "• **Kiểm tra toàn diện**: 15+ bước từ phần cứng đến phần mềm"
        ]
        
        for reason in bios_reasons:
            ctk.CTkLabel(why_bios_frame, text=reason, font=Theme.SMALL_FONT, text_color="#0D47A1").pack(anchor="w", padx=20, pady=2)
        
        ctk.CTkLabel(why_bios_frame, text="", height=10).pack()
        
        # Basic mode
        basic_frame = ctk.CTkFrame(modes_frame, fg_color="#E8F5E8", corner_radius=12)
        basic_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(basic_frame, text="🟢 Chế Độ Cơ Bản", font=Theme.SUBHEADING_FONT, text_color=Theme.SUCCESS).pack(pady=(10,5))
        basic_features = ["• 10 bước kiểm tra cơ bản", "• Dành cho người dùng thông thường", "• Thời gian: 15-20 phút", "• Kiểm tra: BIOS, Windows, phần cứng cơ bản"]
        for feature in basic_features:
            ctk.CTkLabel(basic_frame, text=feature, font=Theme.SMALL_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=15, pady=1)
        ctk.CTkLabel(basic_frame, text="", height=5).pack()
        
        # Expert mode  
        expert_frame = ctk.CTkFrame(modes_frame, fg_color="#FFE8E8", corner_radius=12)
        expert_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(expert_frame, text="🔴 Chế Độ Chuyên Gia", font=Theme.SUBHEADING_FONT, text_color="#FF3B30").pack(pady=(10,5))
        expert_features = ["• 15+ bước kiểm tra chuyên sâu", "• Stress test CPU, GPU, RAM", "• Thời gian: 30-45 phút", "• Benchmark và so sánh hiệu năng"]
        for feature in expert_features:
            ctk.CTkLabel(expert_frame, text=feature, font=Theme.SMALL_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=15, pady=1)
        ctk.CTkLabel(expert_frame, text="", height=5).pack()
    
    def create_about_panel(self, parent):
        """Panel thông tin"""
        about_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        about_frame.grid(row=1, column=0, sticky="nsew", padx=(0,15), pady=(15,0))
        
        ctk.CTkLabel(about_frame, text="ℹ️ Thông Tin Nhà Phát Triển", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(20,15))
        
        info_items = [
            ("👨‍💻 Phát triển bởi:", "Laptop Lê Ẩn & Gemini AI"),
            ("📍 Địa chỉ:", "237/1C Tôn Thất Thuyết, P. Vĩnh Hội (P.3, Q.4 cũ), TPHCM"),
            ("📞 Điện thoại:", "0976.896.621"),
            ("📧 Email:", "laptoplean@gmail.com"),
            ("📅 Phiên bản:", "2.0 Professional (Build 2024.10.29)"),
            ("⚖️ Bản quyền:", "Commercial License - All Rights Reserved"),
            ("🎯 Mục đích:", "Kiểm tra laptop cũ chống lừa đảo cấu hình")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=3)
            ctk.CTkLabel(item_frame, text=label, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(item_frame, text=value, font=Theme.SMALL_FONT, text_color=Theme.TEXT).pack(side="right")
        
        # Links
        links_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        links_frame.pack(pady=15)
        
        ctk.CTkButton(links_frame, text="📞 Liên hệ", width=100, height=30, 
                     command=self._show_contact_info).pack(side="left", padx=5)
        ctk.CTkButton(links_frame, text="📖 Hướng dẫn", width=100, height=30,
                     command=self._show_user_guide).pack(side="left", padx=5)
    
    def _show_contact_info(self):
        import tkinter.messagebox as msgbox
        contact_info = (
            "Laptop Lê Ẩn & Gemini AI\n\n"
            "📍 Địa chỉ: 237/1C Tôn Thất Thuyết\n"
            "P. Vĩnh Hội (P.3, Q.4 cũ), TPHCM\n\n"
            "📞 Điện thoại: 0976.896.621\n"
            "📧 Email: laptoplean@gmail.com\n\n"
            "🎯 Chức năng chính:\n"
            "- Kiểm tra laptop cũ chống lừa đảo\n"
            "- Đọc thông tin từ BIOS và phần cứng\n"
            "- Phát hiện sai lệch cấu hình giả mạo\n"
            "- Bảo vệ người mua khỏi rủi ro tài chính"
        )
        msgbox.showinfo("Thông Tin Liên Hệ & Chức Năng", contact_info)
    
    def _show_user_guide(self):
        import tkinter.messagebox as msgbox
        guide_info = (
            "Hướng Dẫn Sử Dụng LaptopTester:\n\n"
            "1. Chọn chế độ phù hợp\n"
            "2. Làm theo hướng dẫn từng bước\n"
            "3. Đọc kết quả theo màu sắc\n"
            "4. Quyết định mua hay không\n\n"
            "Màu sắc kết quả:\n"
            "🟢 Xanh: Tốt, an toàn\n"
            "🟡 Vàng: Cảnh báo, chú ý\n"
            "🔴 Đỏ: Lỗi nghiêm trọng"
        )
        msgbox.showinfo("Hướng Dẫn Sử Dụng", guide_info)
    
    def create_quickstart_panel(self, parent):
        """Panel bắt đầu nhanh"""
        quick_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        quick_frame.grid(row=1, column=1, sticky="nsew", padx=(15,0), pady=(15,0))
        
        ctk.CTkLabel(quick_frame, text="⚡ Bắt Đầu Nhanh", font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(20,15))
        
        # Tại sao cần LaptopTester?
        why_frame = ctk.CTkFrame(quick_frame, fg_color="#FFF3E0", corner_radius=12)
        why_frame.pack(fill="x", padx=20, pady=(0,15))
        
        ctk.CTkLabel(why_frame, text="🤔 Tại sao cần LaptopTester?", font=Theme.SUBHEADING_FONT, text_color="#E65100").pack(pady=(15,10))
        
        reasons = [
            "⚠️ **Chống lừa đảo**: Phát hiện fake RAM, CPU, GPU qua BIOS",
            "🔍 **Kiểm tra sâu**: Phát hiện lỗi ẩn phần cứng, pin chai",
            "💰 **Tiết kiệm**: Tránh mua laptop lỗi giá cao, sửa chữa tốn kém",
            "🛡️ **Bảo vệ**: Đảm bảo đầu tư đúng chỗ, không bị lừa",
            "🎯 **Chuyên nghiệp**: Công cụ của kỹ thuật viên laptop"
        ]
        
        for reason in reasons:
            ctk.CTkLabel(why_frame, text=reason, font=Theme.SMALL_FONT, text_color="#BF360C").pack(anchor="w", padx=20, pady=2)
        
        ctk.CTkLabel(why_frame, text="", height=10).pack()
        
        # Hướng dẫn sử dụng
        steps = [
            "1️⃣ **Chọn chế độ**: Basic (nhanh) hoặc Expert (chi tiết)",
            "2️⃣ **Làm theo hướng dẫn**: Từng bước có giải thích rõ ràng", 
            "3️⃣ **Đọc kết quả**: Màu xanh (tốt), vàng (cảnh báo), đỏ (lỗi)",
            "4️⃣ **Quyết định**: Mua hoặc không dựa trên kết quả"
        ]
        
        for step in steps:
            ctk.CTkLabel(quick_frame, text=step, font=Theme.BODY_FONT, text_color=Theme.TEXT).pack(anchor="w", padx=20, pady=5)
        
        # Action buttons
        action_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        action_frame.pack(pady=20)
        
        # Action buttons với mô tả rõ ràng
        basic_btn_frame = ctk.CTkFrame(action_frame, fg_color="#E8F5E8", corner_radius=8)
        basic_btn_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(basic_btn_frame, text="Người dùng thông thường - 15 phút", font=Theme.SMALL_FONT, text_color="#2E7D32").pack(pady=(8,2))
        ctk.CTkButton(basic_btn_frame, text="🚀 Bắt Đầu Basic Mode", 
                     command=lambda: self.start_callback("basic"),
                     fg_color=Theme.SUCCESS, width=200, height=35, font=Theme.BODY_FONT).pack(pady=(0,8))
        
        expert_btn_frame = ctk.CTkFrame(action_frame, fg_color="#FFEBEE", corner_radius=8)
        expert_btn_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(expert_btn_frame, text="Chuyên gia/Kỹ thuật viên - 45 phút", font=Theme.SMALL_FONT, text_color="#C62828").pack(pady=(8,2))
        ctk.CTkButton(expert_btn_frame, text="🔥 Bắt Đầu Expert Mode", 
                     command=lambda: self.start_callback("expert"),
                     fg_color="#FF3B30", width=200, height=35, font=Theme.BODY_FONT).pack(pady=(0,8))
    
    def create_footer(self):
        """Tạo footer"""
        footer = ctk.CTkFrame(self, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS, height=60)
        footer.grid(row=2, column=0, sticky="ew", padx=30, pady=(15,30))
        
        footer_content = ctk.CTkFrame(footer, fg_color="transparent")
        footer_content.pack(expand=True, fill="both")
        
        ctk.CTkLabel(footer_content, text="© 2024 LaptopTester Pro. All rights reserved.", 
                    font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(expand=True)