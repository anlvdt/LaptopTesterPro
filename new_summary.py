def create_simple_summary(self, results):
    # Full container 2-column layout
    scroll_frame = ctk.CTkScrollableFrame(self.action_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True)
    scroll_frame.grid_columnconfigure((0,1), weight=1)
    
    # === HEADER FULL WIDTH ===
    header = ctk.CTkFrame(scroll_frame, fg_color=Theme.ACCENT, corner_radius=8, height=100)
    header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    
    ctk.CTkLabel(header, text="📊 " + get_text("report_title"), font=("Segoe UI", 32, "bold"), text_color="white").pack(pady=(15,5))
    ctk.CTkLabel(header, text=get_text("report_subtitle"), font=("Segoe UI", 18), text_color="white").pack(pady=(0,15))
    
    # === STATS CARDS - 4 COLUMNS ===
    stats_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    stats_container.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    stats_container.grid_columnconfigure((0,1,2,3), weight=1)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")
    failed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Lỗi")
    success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
    
    stats_data = [
        (f"📋 {get_text('total_tests')}", str(total_tests), Theme.INFO),
        (f"✅ {get_text('passed_tests')}", str(passed_tests), Theme.SUCCESS),
        (f"❌ {get_text('failed_tests')}", str(failed_tests), Theme.ERROR),
        (f"📈 {get_text('success_rate')}", f"{success_rate:.0f}%", Theme.ACCENT)
    ]
    
    for i, (label, value, color) in enumerate(stats_data):
        card = ctk.CTkFrame(stats_container, fg_color=Theme.FRAME, corner_radius=8, border_width=2, border_color=color)
        card.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(card, text=label, font=("Segoe UI", 16), text_color=Theme.TEXT_SECONDARY).pack(pady=(10,5))
        ctk.CTkLabel(card, text=value, font=("Segoe UI", 36, "bold"), text_color=color).pack(pady=(0,10))
    
    # === LEFT COLUMN ===
    left_col = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    left_col.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    
    # Overall Assessment
    assessment_color = Theme.SUCCESS if success_rate >= 90 else Theme.WARNING if success_rate >= 70 else Theme.ERROR
    assessment_text = get_text('laptop_good') if success_rate >= 90 else get_text('laptop_warning') if success_rate >= 70 else get_text('laptop_bad')
    recommendation = "recommendation_good" if success_rate >= 90 else "recommendation_warning" if success_rate >= 70 else "recommendation_bad"
    
    assess_frame = ctk.CTkFrame(left_col, fg_color=assessment_color, corner_radius=8)
    assess_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(assess_frame, text=f"🎯 {assessment_text}", font=("Segoe UI", 24, "bold"), text_color="white").pack(pady=(15,5))
    ctk.CTkLabel(assess_frame, text=get_text(recommendation), font=("Segoe UI", 16), text_color="white", wraplength=600).pack(pady=(0,15), padx=15)
    
    # Hardware Capability
    capabilities, cpu_name = self.analyze_hardware_capability(results)
    if capabilities:
        cap_frame = ctk.CTkFrame(left_col, fg_color=Theme.FRAME, corner_radius=8)
        cap_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(cap_frame, text="💡 Khả Năng Sử Dụng", font=("Segoe UI", 20, "bold"), text_color=Theme.ACCENT).pack(pady=10, padx=10, anchor="w")
        if cpu_name:
            ctk.CTkLabel(cap_frame, text=f"CPU: {cpu_name}", font=("Segoe UI", 14), text_color=Theme.TEXT_SECONDARY).pack(padx=10, anchor="w")
        
        for cap in capabilities:
            cap_card = ctk.CTkFrame(cap_frame, fg_color=Theme.BACKGROUND, corner_radius=6, border_width=2, border_color=cap["color"])
            cap_card.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(cap_card, text=f"{cap['icon']} {cap['title']}", font=("Segoe UI", 16, "bold"), text_color=cap["color"]).pack(anchor="w", padx=10, pady=(8,4))
            ctk.CTkLabel(cap_card, text=cap["desc"], font=("Segoe UI", 13), text_color=Theme.TEXT, wraplength=550, justify="left").pack(anchor="w", padx=10, pady=(0,8))
    
    # AI Assessment
    ai_frame = ctk.CTkFrame(left_col, fg_color=Theme.INFO, corner_radius=8)
    ai_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(ai_frame, text="🤖 Đánh Giá AI", font=("Segoe UI", 20, "bold"), text_color="white").pack(pady=(10,5), padx=10, anchor="w")
    ctk.CTkLabel(ai_frame, text="⚠️ Ứng dụng AI có thể có sai sót. Khuyến khích dùng thêm công cụ chuyên nghiệp.", 
                font=("Segoe UI", 12), text_color="#FFE4B5", wraplength=600, justify="left").pack(padx=10, anchor="w")
    ai_assessment = self.generate_ai_assessment(results, success_rate)
    ctk.CTkLabel(ai_frame, text=ai_assessment, font=("Segoe UI", 14), text_color="white", wraplength=600, justify="left").pack(pady=(5,10), padx=10, anchor="w")
    
    # === RIGHT COLUMN ===
    right_col = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    right_col.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    
    # Detailed Results
    results_frame = ctk.CTkFrame(right_col, fg_color=Theme.FRAME, corner_radius=8)
    results_frame.pack(fill="both", expand=True, pady=5)
    ctk.CTkLabel(results_frame, text="📋 Chi Tiết Kết Quả", font=("Segoe UI", 20, "bold"), text_color=Theme.ACCENT).pack(pady=10)
    
    if results:
        categories = {
            f"🔒 {get_text('security_category')}": ["hardware_fingerprint", "license_check"],
            f"⚙️ {get_text('performance_category')}": ["cpu_stress", "gpu_stress", "harddrive_speed", "thermal_test"],
            f"🖥️ {get_text('interface_category')}": ["screen_test", "keyboard_test", "webcam_test", "audio_test"],
            f"🔧 {get_text('hardware_category')}": ["system_info", "harddrive_health", "battery_health", "network_test"]
        }
        
        for category, test_names in categories.items():
            cat_frame = ctk.CTkFrame(results_frame, fg_color=Theme.BACKGROUND, corner_radius=6)
            cat_frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(cat_frame, text=category, font=("Segoe UI", 16, "bold"), text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=(8,4))
            
            for test_name in test_names:
                if test_name in results:
                    result = results[test_name]
                    status = result.get("Trạng thái", "Không rõ")
                    status_colors = {"Tốt": Theme.SUCCESS, "Lỗi": Theme.ERROR, "Cảnh báo": Theme.WARNING, "skip": Theme.SKIP}
                    status_color = status_colors.get(status, Theme.TEXT_SECONDARY)
                    status_icons = {"Tốt": "✅", "Lỗi": "❌", "Cảnh báo": "⚠️", "skip": "⏭️"}
                    status_icon = status_icons.get(status, "❓")
                    
                    result_text = f"{status_icon} {test_name}"
                    if result.get("Kết quả"):
                        result_text += f": {result['Kết quả']}"
                    
                    ctk.CTkLabel(cat_frame, text=result_text, font=("Segoe UI", 13), text_color=status_color, wraplength=550).pack(anchor="w", padx=20, pady=2)
    
    # === PROFESSIONAL TOOLS - FULL WIDTH ===
    tools_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.CARD, corner_radius=8)
    tools_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    ctk.CTkLabel(tools_frame, text=f"🛠️ {get_text('professional_tools')}", font=("Segoe UI", 20, "bold"), text_color=Theme.ACCENT).pack(pady=10)
    ctk.CTkLabel(tools_frame, text="Để xác minh kết quả AI, sử dụng các công cụ chuyên nghiệp:", font=("Segoe UI", 14), text_color=Theme.TEXT_SECONDARY).pack(padx=15)
    
    tools_grid = ctk.CTkFrame(tools_frame, fg_color="transparent")
    tools_grid.pack(fill="x", padx=15, pady=10)
    tools_grid.grid_columnconfigure((0,1,2), weight=1)
    
    tools = [
        ("💾 CrystalDiskInfo", "S.M.A.R.T ổ cứng", "winget install CrystalDewWorld.CrystalDiskInfo", "https://crystalmark.info"),
        ("🌡️ HWiNFO64", "Nhiệt độ & cảm biến", "winget install REALiX.HWiNFO", "https://www.hwinfo.com"),
        ("⚡ CPU-Z", "CPU, RAM, Mainboard", "winget install CPUID.CPU-Z", "https://www.cpuid.com"),
        ("🎮 GPU-Z", "Card đồ họa", "winget install TechPowerUp.GPU-Z", "https://www.techpowerup.com/gpuz"),
        ("🔥 FurMark", "GPU Stress Test", "winget install Geeks3D.FurMark", "https://geeks3d.com/furmark"),
        ("🧠 MemTest86", "Kiểm tra RAM", "Tải từ trang chủ", "https://www.memtest86.com")
    ]
    
    for i, (name, desc, cmd, url) in enumerate(tools):
        tool_card = ctk.CTkFrame(tools_grid, fg_color=Theme.FRAME, corner_radius=6)
        tool_card.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(tool_card, text=name, font=("Segoe UI", 14, "bold"), text_color=Theme.ACCENT).pack(anchor="w", padx=8, pady=(8,2))
        ctk.CTkLabel(tool_card, text=desc, font=("Segoe UI", 11), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=8)
        cmd_frame = ctk.CTkFrame(tool_card, fg_color=Theme.BACKGROUND, corner_radius=4)
        cmd_frame.pack(fill="x", padx=8, pady=5)
        ctk.CTkLabel(cmd_frame, text=cmd, font=("Consolas", 10), text_color=Theme.ACCENT).pack(padx=5, pady=3)
        def open_url(url=url):
            import webbrowser
            webbrowser.open(url)
        ctk.CTkButton(tool_card, text="🌐 Trang chủ", command=open_url, fg_color=Theme.SUCCESS, height=24, font=("Segoe UI", 11)).pack(pady=(0,8))
    
    # === EXPORT BUTTONS - FULL WIDTH ===
    export_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.ACCENT, corner_radius=8)
    export_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    ctk.CTkLabel(export_frame, text=f"💾 {get_text('export_report')}", font=("Segoe UI", 20, "bold"), text_color="white").pack(pady=(10,5))
    
    export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
    export_buttons.pack(pady=(0,10))
    ctk.CTkButton(export_buttons, text=f"📄 {get_text('export_pdf')}", command=self.export_pdf, fg_color="white", text_color=Theme.ACCENT, height=32, font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
    ctk.CTkButton(export_buttons, text=f"📊 {get_text('export_excel')}", command=self.export_excel, fg_color="white", text_color=Theme.ACCENT, height=32, font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
    ctk.CTkButton(export_buttons, text=f"📋 {get_text('copy_text')}", command=self.copy_report, fg_color="white", text_color=Theme.ACCENT, height=32, font=("Segoe UI", 14, "bold")).pack(side="left", padx=5)
