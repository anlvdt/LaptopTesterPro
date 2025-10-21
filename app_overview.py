import customtkinter as ctk

class AppOverviewFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        
        # Tạo scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(scroll_frame, text="💻 LaptopTester Pro", font=("Segoe UI", 36, "bold"), text_color="#3B82F6").pack(pady=(20, 10))
        ctk.CTkLabel(scroll_frame, text="Phần mềm kiểm tra laptop toàn diện", font=("Segoe UI", 18), text_color="#64748B").pack(pady=(0, 30))
        
        # Features
        features_frame = ctk.CTkFrame(scroll_frame, fg_color="#FFFFFF", corner_radius=12)
        features_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(features_frame, text="✨ Tính năng nổi bật", font=("Segoe UI", 22, "bold"), text_color="#3B82F6").pack(pady=15, padx=20, anchor="w")
        
        features = [
            "🎨 Giao diện hiện đại với CustomTkinter",
            "📊 Kiểm tra toàn diện 15+ bước test",
            "🔄 Tự động hóa cao với tools chuyên nghiệp",
            "📱 Responsive thích ứng nhiều kích thước",
            "🎯 Báo cáo chi tiết export nhiều định dạng",
            "🔧 Đa nền tảng: Windows, Linux, macOS"
        ]
        
        for feature in features:
            ctk.CTkLabel(features_frame, text=feature, font=("Segoe UI", 16), text_color="#0F172A", anchor="w").pack(pady=5, padx=40, anchor="w")
        
        # Quick start
        quick_frame = ctk.CTkFrame(scroll_frame, fg_color="#E3F2FD", corner_radius=12)
        quick_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(quick_frame, text="🚀 Bắt đầu nhanh", font=("Segoe UI", 22, "bold"), text_color="#1565C0").pack(pady=15, padx=20, anchor="w")
        ctk.CTkLabel(quick_frame, text="Chọn chế độ phù hợp với nhu cầu của bạn:", font=("Segoe UI", 16), text_color="#424242").pack(pady=5, padx=40, anchor="w")
        
        btn_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="🎯 Chế độ Cơ bản", command=lambda: self.mode_callback("basic"), 
                     fg_color="#10B981", hover_color="#059669", height=50, width=200, font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="🔥 Chế độ Chuyên gia", command=lambda: self.mode_callback("expert"), 
                     fg_color="#EF4444", hover_color="#DC2626", height=50, width=200, font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)
