# Enhanced frequency lock detection with scenario analysis
freq_locked = False
lock_scenario = "normal"
if max_freq and min_freq:
    freq_variation = ((max_freq - min_freq) / max_freq) * 100
    freq_locked = freq_variation < 5  # Less than 5% variation indicates locked frequency
    
    # Analyze lock scenario
    if freq_locked:
        base_freq = result_data.get('baseline_freq', 0)
        if min_freq < base_freq * 0.7:  # Locked at very low frequency
            lock_scenario = "power_saving_aggressive"
        elif min_freq < max_freq * 0.8:  # Locked below normal boost
            lock_scenario = "thermal_protection"
        elif max_temp and max_temp > 90:  # High temp + lock = thermal issue
            lock_scenario = "thermal_emergency"
        else:
            lock_scenario = "manufacturer_limit"

# Frequency lock analysis with scenario-specific recommendations
if freq_locked:
    if lock_scenario == "thermal_emergency":
        lock_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.ERROR)
        lock_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(lock_frame, text="🚨 CẢNH BÁO: KHÓA XUNG DO QUÁ NHIỆT", font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=10)
        
        warning_frame = ctk.CTkFrame(lock_frame, fg_color="transparent")
        warning_frame.pack(fill="x", padx=15, pady=(0,15))
        
        ctk.CTkLabel(warning_frame, text="⚠️ NGUY HIỂM: CPU bị khóa xung để tự bảo vệ khỏi hư hỏng!", font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
        ctk.CTkLabel(warning_frame, text="• Nhiệt độ quá cao có thể làm hỏng CPU vĩnh viễn", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(warning_frame, text="• CẦN XỬ LÝ NGAY: Vệ sinh tản nhiệt, thay keo tản nhiệt", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(warning_frame, text="• KHÔNG NÊN mở khóa xung khi chưa sửa tản nhiệt", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        
    elif lock_scenario == "power_saving_aggressive":
        lock_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.WARNING)
        lock_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(lock_frame, text="🔋 KHÓA XUNG TIẾT KIỆM ĐIỆN", font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=10)
        
        info_frame = ctk.CTkFrame(lock_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=(0,15))
        
        ctk.CTkLabel(info_frame, text="📊 Phân tích: CPU bị khóa ở tần số rất thấp để tiết kiệm pin", font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="• Có thể do chế độ tiết kiệm pin cực mạnh", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text="• Hiệu năng sẽ giảm đáng kể", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        
        ctk.CTkLabel(info_frame, text="💡 Khuyến nghị: NÊN mở khóa để có hiệu năng tốt hơn", font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="• Windows: Chuyển sang High Performance mode", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text="• Gõ 'powercfg.cpl' → Chọn 'High Performance'", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        
    elif lock_scenario == "manufacturer_limit":
        lock_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.INFO)
        lock_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(lock_frame, text="🏭 KHÓA XUNG CỦA NHÀ SẢN XUẤT", font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=10)
        
        info_frame = ctk.CTkFrame(lock_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=(0,15))
        
        ctk.CTkLabel(info_frame, text="📊 Phân tích: Nhà sản xuất cố định tần số để ổn định", font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="• Thường thấy trên laptop văn phòng", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text="• Giúp tiết kiệm pin và giảm nhiệt", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        
        ctk.CTkLabel(info_frame, text="💡 Khuyến nghị: Có thể mở khóa nếu cần hiệu năng cao", font=Theme.BODY_FONT, text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="• Kiểm tra BIOS: CPU Frequency → Auto/Dynamic", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(info_frame, text="• Lưu ý: Pin sẽ hết nhanh hơn", font=Theme.SMALL_FONT, text_color="white").pack(anchor="w", padx=20)