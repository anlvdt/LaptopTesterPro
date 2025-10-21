"""
Missing Steps for LaptopTester
Thêm 3 bước: Kiểm tra ngoại quan, BIOS, và Nhận định phần cứng
"""

# ============================================================================
# BƯỚC 1: KIỂM TRA NGOẠI QUAN (Physical Inspection)
# ============================================================================
class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        why_text = "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp." if CURRENT_LANG == "vi" else "Physical condition reflects how the previous owner used the machine. Cracks, dents, loose hinges or stripped screws may indicate the machine was dropped or underwent unprofessional repairs."
        
        how_text = """**Vỏ máy & Bản lề:**
  • Kiểm tra vết nứt, móp méo ở góc máy (dấu hiệu rơi)
  • Mở/đóng màn hình 10-15 lần, nghe tiếng kêu lạ
  • Bản lề phải chặt, không rơ, giữ được góc mở

**Cổng kết nối:**
  • Cắm sạc và lay nhẹ - không được lỏng
  • Kiểm tra USB, HDMI, audio jack
  • Cổng bị lỏng = thay mainboard (đắt!)

**Ốc vít & Tem:**
  • Ốc không toét đầu (dấu hiệu tháo lắp)
  • Tem bảo hành còn nguyên
  • Serial number khớp với BIOS

**⚠️ ThinkPad đặc biệt:**
  • Kiểm tra tem Lenovo chính hãng
  • Xem sticker dưới đáy có bị bóc
  • ThinkPad doanh nghiệp thường có asset tag""" if CURRENT_LANG == "vi" else """**Body & Hinges:**
  • Check for cracks, dents at corners (drop signs)
  • Open/close screen 10-15 times, listen for strange sounds
  • Hinges must be tight, no wobble, hold angle

**Ports:**
  • Plug charger and wiggle gently - should not be loose
  • Check USB, HDMI, audio jack
  • Loose port = motherboard replacement (expensive!)

**Screws & Seals:**
  • Screws not stripped (sign of disassembly)
  • Warranty seals intact
  • Serial number matches BIOS

**⚠️ ThinkPad specific:**
  • Check genuine Lenovo seal
  • Check bottom sticker not peeled
  • Enterprise ThinkPads usually have asset tags"""
        
        super().__init__(master, "Kiểm Tra Ngoại Hình" if CURRENT_LANG == "vi" else "Physical Inspection", why_text, how_text, **kwargs)
        self.create_inspection_checklist()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
        self.mark_completed({"Kết quả": "Đã hiển thị checklist", "Trạng thái": "Sẵn sàng"}, auto_advance=False)
    
    def create_inspection_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        title_text = "🔍 Checklist Kiểm Tra Ngoại Hình" if CURRENT_LANG == "vi" else "🔍 Physical Inspection Checklist"
        ctk.CTkLabel(checklist_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Exterior checks
        exterior_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        exterior_frame.pack(fill="x", padx=15, pady=10)
        
        exterior_title = "💻 Bên Ngoài:" if CURRENT_LANG == "vi" else "💻 Exterior:"
        ctk.CTkLabel(exterior_frame, text=exterior_title, font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        
        if CURRENT_LANG == "vi":
            exterior_checks = [
                "• Vỏ máy: Kiểm tra vết nứt, rạn nứt, móp méo",
                "• Bản lề màn hình: Mở/đóng nhiều lần, nghe tiếng kêu",
                "• Bàn phím: Kiểm tra phím lỏng, không nhấn",
                "• Touchpad: Bề mặt phẳng, không bị lồi",
                "• Cổng kết nối: USB, HDMI, audio, sạc",
                "• Lỗ thoát khí: Không bị bịt tắc"
            ]
        else:
            exterior_checks = [
                "• Body: Check for cracks, fractures, dents",
                "• Screen hinges: Open/close multiple times, listen for sounds",
                "• Keyboard: Check for loose keys, non-responsive keys",
                "• Touchpad: Surface flat, not bulging",
                "• Ports: USB, HDMI, audio, charger",
                "• Vents: Not blocked"
            ]
        
        for check in exterior_checks:
            ctk.CTkLabel(exterior_frame, text=check, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
        
        # Hardware checks
        hardware_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND)
        hardware_frame.pack(fill="x", padx=15, pady=10)
        
        hardware_title = "🔩 Phần Cứng:" if CURRENT_LANG == "vi" else "🔩 Hardware:"
        ctk.CTkLabel(hardware_frame, text=hardware_title, font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=5)
        
        if CURRENT_LANG == "vi":
            hardware_checks = [
                "• Ốc vít: Kiểm tra các ốc không bị toét, thiếu",
                "• Nhãn dán: Còn nguyên, không bị xóa",
                "• Đèn LED: Hoạt động bình thường",
                "• Lưới thoát khí: Sạch sẽ, không bụi bẩn"
            ]
        else:
            hardware_checks = [
                "• Screws: Check screws not stripped, missing",
                "• Labels: Intact, not erased",
                "• LED lights: Working normally",
                "• Vent grilles: Clean, no dust"
            ]
        
        for check in hardware_checks:
            ctk.CTkLabel(hardware_frame, text=check, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
        
        # Warning signs
        warning_frame = ctk.CTkFrame(checklist_frame, fg_color="#FFF3CD", border_width=1, border_color=Theme.WARNING)
        warning_frame.pack(fill="x", padx=15, pady=10)
        
        warning_title = "⚠️ Dấu Hiệu Cảnh Báo:" if CURRENT_LANG == "vi" else "⚠️ Warning Signs:"
        ctk.CTkLabel(warning_frame, text=warning_title, font=Theme.BODY_FONT, text_color=Theme.WARNING).pack(anchor="w", padx=10, pady=5)
        
        if CURRENT_LANG == "vi":
            warnings = [
                "• Bản lề rất lỏng hoặc kêu kèn kẹt",
                "• Cổng sạc lỏng, không giữ chặt",
                "• Vết nứt gần bản lề (nguy hiểm)",
                "• Mùi lạ (cháy, hóa chất)",
                "• Ốc vít bị toét nhiều (dấu hiệu tháo lắp)"
            ]
        else:
            warnings = [
                "• Hinges very loose or creaking",
                "• Charger port loose, not holding tight",
                "• Cracks near hinges (dangerous)",
                "• Strange smell (burning, chemicals)",
                "• Many stripped screws (sign of disassembly)"
            ]
        
        for warning in warnings:
            ctk.CTkLabel(warning_frame, text=warning, font=Theme.SMALL_FONT, text_color="#856404").pack(anchor="w", padx=20, pady=2)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        question_text = "Dựa trên checklist trên, tình trạng vật lý tổng thể của máy như thế nào?" if CURRENT_LANG == "vi" else "Based on the checklist above, what is the overall physical condition of the machine?"
        ctk.CTkLabel(self.result_container, text=question_text, font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        if CURRENT_LANG == "vi":
            btn_texts = [
                ("✨ Rất tốt - Như mới", "#28a745", {"Kết quả": "Rất tốt - Như mới", "Trạng thái": "Xuất sắc"}),
                ("✅ Tốt - Vết nhỏ", Theme.SUCCESS, {"Kết quả": "Tốt - Có vết sử dụng nhỏ", "Trạng thái": "Tốt"}),
                ("⚠️ Trung bình - Có lỗi nhỏ", Theme.WARNING, {"Kết quả": "Trung bình - Có lỗi nhỏ cần lưu ý", "Trạng thái": "Cảnh báo"}),
                ("❌ Kém - Nhiều vấn đề", Theme.ERROR, {"Kết quả": "Kém - Nhiều vấn đề nghiêm trọng", "Trạng thái": "Lỗi"})
            ]
        else:
            btn_texts = [
                ("✨ Excellent - Like new", "#28a745", {"Kết quả": "Excellent - Like new", "Trạng thái": "Excellent"}),
                ("✅ Good - Minor wear", Theme.SUCCESS, {"Kết quả": "Good - Minor wear marks", "Trạng thái": "Good"}),
                ("⚠️ Fair - Minor issues", Theme.WARNING, {"Kết quả": "Fair - Minor issues to note", "Trạng thái": "Warning"}),
                ("❌ Poor - Many issues", Theme.ERROR, {"Kết quả": "Poor - Many serious issues", "Trạng thái": "Error"})
            ]
        
        for text, color, result in btn_texts:
            btn = ctk.CTkButton(button_bar, text=text, command=lambda r=result: self.handle_result_generic(True, r, {}), 
                              fg_color=color, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
            btn.pack(side="left", padx=5)


# ============================================================================
# BƯỚC 2: KIỂM TRA BIOS (BIOS Check)
# ============================================================================
class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        why_text = "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp." if CURRENT_LANG == "vi" else "BIOS contains fundamental settings. Check to ensure optimal performance and not locked by enterprise features."
        
        how_text = """1. Khởi động lại máy và nhấn liên tục phím để vào BIOS:
   • **Dell/Alienware:** F2 hoặc F12
   • **HP/Compaq:** F10 hoặc ESC
   • **Lenovo/ThinkPad:** F1, F2 hoặc Enter
   • **ASUS:** F2 hoặc Delete
   • **Acer:** F2 hoặc Delete
   • **MSI:** Delete hoặc F2

2. Kiểm tra các mục quan trọng:
   • **CPU Features:** Intel Turbo Boost / AMD Boost phải 'Enabled'
   • **Memory:** XMP/DOCP profile nên bật (nếu có)
   • **Security:** Không có BIOS password lạ
   • **⚠️ CẢNH BÁO:** Tìm 'Computrace' hoặc 'Absolute' - nếu 'Enabled' thì máy có thể bị khóa từ xa!
   • **Boot Order:** Kiểm tra thứ tự khởi động
   • **Secure Boot:** Nên để 'Enabled' cho bảo mật""" if CURRENT_LANG == "vi" else """1. Restart machine and press key repeatedly to enter BIOS:
   • **Dell/Alienware:** F2 or F12
   • **HP/Compaq:** F10 or ESC
   • **Lenovo/ThinkPad:** F1, F2 or Enter
   • **ASUS:** F2 or Delete
   • **Acer:** F2 or Delete
   • **MSI:** Delete or F2

2. Check important items:
   • **CPU Features:** Intel Turbo Boost / AMD Boost must be 'Enabled'
   • **Memory:** XMP/DOCP profile should be enabled (if available)
   • **Security:** No strange BIOS password
   • **⚠️ WARNING:** Look for 'Computrace' or 'Absolute' - if 'Enabled' machine can be remotely locked!
   • **Boot Order:** Check boot sequence
   • **Secure Boot:** Should be 'Enabled' for security"""
        
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS" if CURRENT_LANG == "vi" else "BIOS Settings Check", why_text, how_text, **kwargs)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        question_text = "Các cài đặt trong BIOS có chính xác và an toàn không?" if CURRENT_LANG == "vi" else "Are BIOS settings correct and safe?"
        ctk.CTkLabel(self.result_container, text=question_text, font=Theme.SUBHEADING_FONT, wraplength=900).pack(pady=15)
        
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        yes_text = "Có, mọi cài đặt đều đúng" if CURRENT_LANG == "vi" else "Yes, all settings correct"
        no_text = "Không, có cài đặt sai/bị khóa" if CURRENT_LANG == "vi" else "No, wrong settings/locked"
        
        self.btn_yes = ctk.CTkButton(button_bar, text=yes_text, command=lambda: self.handle_result_generic(True, {"Kết quả": "Cài đặt chính xác", "Trạng thái": "Tốt"}, {}), 
                                     fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_yes.pack(side="left", padx=10)
        
        self.btn_no = ctk.CTkButton(button_bar, text=no_text, command=lambda: self.handle_result_generic(False, {}, {"Kết quả": "Có vấn đề với cài đặt BIOS", "Trạng thái": "Lỗi"}), 
                                    fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, font=Theme.BODY_FONT)
        self.btn_no.pack(side="left", padx=10)


# ============================================================================
# BƯỚC 3: THÊM NHẬN ĐỊNH PHẦN CỨNG VÀO HardwareFingerprintStep
# ============================================================================
def add_hardware_capability_analysis(self, hw_info):
    """
    Thêm function này vào class HardwareFingerprintStep
    Gọi sau khi display_info()
    """
    cpu_name = hw_info.get("CPU", "")
    gpu_name = hw_info.get("GPU", "")
    
    # Xác định tier CPU
    cpu_tier = "unknown"
    if any(x in cpu_name.upper() for x in ["I9", "I7", "RYZEN 9", "RYZEN 7"]):
        cpu_tier = "high"
    elif any(x in cpu_name.upper() for x in ["I5", "RYZEN 5"]):
        cpu_tier = "mid"
    elif any(x in cpu_name.upper() for x in ["I3", "RYZEN 3", "CELERON", "PENTIUM"]):
        cpu_tier = "low"
    
    # Kiểm tra GPU rời
    gpu_dedicated = any(x in gpu_name.upper() for x in ["RTX", "GTX", "RADEON RX", "RADEON PRO"])
    
    # Tạo capabilities
    capabilities = []
    if cpu_tier == "high":
        if CURRENT_LANG == "vi":
            capabilities = [
                {"icon": "🎮", "title": "Gaming & Rendering", "desc": "Phù hợp cho gaming AAA, render 3D, video editing chuyên nghiệp", "color": "#10B981"},
                {"icon": "💼", "title": "Workstation", "desc": "Xử lý đa nhiệm nặng, phát triển phần mềm, máy ảo", "color": "#3B82F6"}
            ]
        else:
            capabilities = [
                {"icon": "🎮", "title": "Gaming & Rendering", "desc": "Suitable for AAA gaming, 3D rendering, professional video editing", "color": "#10B981"},
                {"icon": "💼", "title": "Workstation", "desc": "Heavy multitasking, software development, virtual machines", "color": "#3B82F6"}
            ]
    elif cpu_tier == "mid":
        if CURRENT_LANG == "vi":
            capabilities = [
                {"icon": "🎮", "title": "Gaming Casual", "desc": "Chơi game ở mức trung bình, streaming, content creation", "color": "#F59E0B"},
                {"icon": "💼", "title": "Văn phòng nâng cao", "desc": "Office, lập trình, thiết kế đồ họa 2D, đa nhiệm vừa phải", "color": "#3B82F6"}
            ]
        else:
            capabilities = [
                {"icon": "🎮", "title": "Casual Gaming", "desc": "Mid-level gaming, streaming, content creation", "color": "#F59E0B"},
                {"icon": "💼", "title": "Advanced Office", "desc": "Office, programming, 2D graphics design, moderate multitasking", "color": "#3B82F6"}
            ]
    else:
        if CURRENT_LANG == "vi":
            capabilities = [
                {"icon": "📝", "title": "Văn phòng cơ bản", "desc": "Office, web browsing, email, xem phim", "color": "#94A3B8"},
                {"icon": "🎓", "title": "Học tập", "desc": "Học online, soạn thảo văn bản, nghiên cứu", "color": "#06B6D4"}
            ]
        else:
            capabilities = [
                {"icon": "📝", "title": "Basic Office", "desc": "Office, web browsing, email, video watching", "color": "#94A3B8"},
                {"icon": "🎓", "title": "Education", "desc": "Online learning, document editing, research", "color": "#06B6D4"}
            ]
    
    if gpu_dedicated:
        if CURRENT_LANG == "vi":
            capabilities.insert(0, {"icon": "🎨", "title": "Đồ họa chuyên nghiệp", "desc": "GPU rời mạnh, phù hợp cho CAD, 3D modeling, AI/ML", "color": "#8B5CF6"})
        else:
            capabilities.insert(0, {"icon": "🎨", "title": "Professional Graphics", "desc": "Powerful discrete GPU, suitable for CAD, 3D modeling, AI/ML", "color": "#8B5CF6"})
    
    if not capabilities:
        return
    
    # Hiển thị capabilities
    cap_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
    cap_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(20,10))
    
    title_text = "💡 Khả Năng Sử Dụng Phần Cứng" if CURRENT_LANG == "vi" else "💡 Hardware Capability"
    ctk.CTkLabel(cap_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", pady=(0,10))
    
    for cap in capabilities:
        card = ctk.CTkFrame(cap_frame, fg_color=Theme.FRAME, corner_radius=8, border_width=2, border_color=cap["color"])
        card.pack(fill="x", pady=5)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=12)
        
        ctk.CTkLabel(content, text=f"{cap['icon']} {cap['title']}", font=Theme.BODY_FONT, text_color=cap["color"]).pack(anchor="w")
        ctk.CTkLabel(content, text=cap["desc"], font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, wraplength=700, justify="left").pack(anchor="w", pady=(3,0))


# ============================================================================
# HƯỚNG DẪN TÍCH HỢP
# ============================================================================
"""
CÁCH TÍCH HỢP VÀO main_enhanced_auto.py:

1. Copy 2 class PhysicalInspectionStep và BIOSCheckStep vào file main_enhanced_auto.py
   (đặt sau class BaseStepFrame, trước class HardwareFingerprintStep)

2. Trong class HardwareFingerprintStep, thêm method add_hardware_capability_analysis
   và gọi nó trong display_info():
   
   def display_info(self, hw_info):
       # ... code hiện tại ...
       
       # THÊM DÒNG NÀY:
       self.add_hardware_capability_analysis(hw_info)
       
       self.mark_completed(...)

3. Tìm hàm _get_steps_for_mode() và thêm 2 bước mới vào đầu danh sách:
   
   basic_steps = [
       # THÊM 2 DÒNG NÀY:
       ("Kiểm tra ngoại hình", PhysicalInspectionStep),
       ("Kiểm tra BIOS", BIOSCheckStep),
       
       # Các bước cũ:
       ("Định danh phần cứng", HardwareFingerprintStep),
       ("Bản quyền Windows", LicenseCheckStep),
       ...
   ]

4. Lưu file và chạy lại ứng dụng
"""
