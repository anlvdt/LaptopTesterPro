# Wizard Frame - Compact version with full 17 steps
class WizardFrame(ctk.CTkFrame):
    def __init__(self, master, mode, app=None):
        super().__init__(master, fg_color="transparent")
        self.mode = mode
        self.app = app
        self.current_step = 0
        self.all_results = {}
        
        # Define all 17 test steps
        basic_steps = [
            ("Định danh phần cứng", HardwareFingerprintStep),
            ("Bản quyền Windows", LicenseCheckStep),
            ("Cấu hình hệ thống", SystemInfoStep),
            ("Sức khỏe ổ cứng", HardDriveHealthStep),
            ("Kiểm tra màn hình", ScreenTestStep),
            ("Bàn phím & Touchpad", KeyboardTestStep),
            ("Cổng kết nối", PortsConnectivityStep),
            ("Pin laptop", BatteryHealthStep),
            ("Loa & Micro", AudioTestStep),
            ("Webcam", WebcamTestStep),
            ("Mạng & WiFi", NetworkTestStep)
        ]
        
        expert_steps = basic_steps + [
            ("CPU Stress Test", CPUStressTestStep),
            ("GPU Stress Test", GPUStressTestStep),
            ("Kiểm tra RAM", MemoryTestStep),
            ("Kiểm tra nhiệt độ", ThermalTestStep),
            ("Kiểm tra BIOS", BIOSCheckStep),
            ("Kiểm tra ngoại hình", PhysicalInspectionStep)
        ]
        
        self.steps = expert_steps if mode == "expert" else basic_steps
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_navigation()
        self.show_step(0)
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=Theme.ACCENT, height=60)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        header.grid_columnconfigure(1, weight=1)
        
        # Step info
        mode_text = "🔥 Chuyên gia" if self.mode == "expert" else "⚙️ Cơ bản"
        self.step_label = ctk.CTkLabel(header, text="", font=Theme.SUBHEADING_FONT, text_color="white")
        self.step_label.grid(row=0, column=0, padx=16, pady=12)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(header, progress_color="white", fg_color=Theme.ACCENT_HOVER)
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=16, pady=12)
        
        # Mode label
        ctk.CTkLabel(header, text=mode_text, font=Theme.BODY_FONT, 
                    text_color="white").grid(row=0, column=2, padx=16, pady=12)
    
    def create_navigation(self):
        nav_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=50)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 16))
        nav_frame.grid_columnconfigure(1, weight=1)
        
        # Navigation buttons
        self.prev_btn = ctk.CTkButton(nav_frame, text="◀ Trước", command=self.go_previous,
                                     width=80, height=Theme.BUTTON_HEIGHT, fg_color=Theme.SKIP)
        self.prev_btn.grid(row=0, column=0, padx=12, pady=8)
        
        self.skip_btn = ctk.CTkButton(nav_frame, text="⏭ Bỏ qua", command=self.skip_current_step,
                                     fg_color=Theme.WARNING, width=80, height=Theme.BUTTON_HEIGHT)
        self.skip_btn.grid(row=0, column=1, pady=8)
        
        self.next_btn = ctk.CTkButton(nav_frame, text="Tiếp theo ▶", command=self.go_to_next_step,
                                     fg_color=Theme.SUCCESS, width=80, height=Theme.BUTTON_HEIGHT)
        self.next_btn.grid(row=0, column=2, padx=12, pady=8)
        
        self.update_navigation_state()
    
    def show_step(self, step_index):
        # Clear current step
        for widget in self.winfo_children():
            if widget.grid_info().get("row") == 1:
                widget.destroy()
        
        total_steps = len(self.steps)
        if step_index < total_steps:
            step_name, step_class = self.steps[step_index]
            self.step_label.configure(text=f"Bước {step_index + 1}/{total_steps}: {step_name}")
            self.progress_bar.set((step_index + 1) / total_steps)
            
            # Create step frame
            step_frame = step_class(
                self,
                record_result_callback=self.record_result,
                enable_next_callback=self.enable_next,
                go_to_next_step_callback=self.go_to_next_step,
                all_results=self.all_results
            )
            step_frame.grid(row=1, column=0, sticky="nsew")
        else:
            # Show summary
            self.step_label.configure(text=f"🏆 Hoàn thành ({total_steps} bước)")
            self.progress_bar.set(1.0)
            
            summary_frame = SummaryStep(
                self,
                record_result_callback=self.record_result,
                enable_next_callback=self.enable_next,
                go_to_next_step_callback=self.go_to_next_step,
                all_results=self.all_results
            )
            summary_frame.grid(row=1, column=0, sticky="nsew")
        
        self.update_navigation_state()
    
    def record_result(self, step_name, result_data):
        self.all_results[step_name] = result_data
        logger.info(f"Recorded result for {step_name}: {result_data}")
    
    def enable_next(self):
        pass
    
    def go_previous(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
    
    def go_to_next_step(self):
        self.current_step += 1
        self.show_step(self.current_step)
    
    def skip_current_step(self):
        if self.current_step < len(self.steps):
            step_name, _ = self.steps[self.current_step]
            self.record_result(step_name, {"result": "Skipped", "status": "Bỏ qua"})
        self.go_to_next_step()
    
    def update_navigation_state(self):
        # Update button states
        self.prev_btn.configure(state="disabled" if self.current_step <= 0 else "normal")
        self.skip_btn.configure(state="disabled" if self.current_step >= len(self.steps) else "normal")
        
        if self.current_step >= len(self.steps):
            self.next_btn.configure(text="🏠 Về trang chủ", fg_color=Theme.ACCENT,
                                   command=self.go_home)
        else:
            self.next_btn.configure(text="Tiếp theo ▶", fg_color=Theme.SUCCESS,
                                   command=self.go_to_next_step)
    
    def go_home(self):
        if self.app:
            self.app.show_mode_selection()

# Individual Test Frame
class IndividualTestFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=Theme.ACCENT, height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header, text="🔧 " + get_text("individual_test"), 
                    font=Theme.HEADING_FONT, text_color="white").pack(expand=True)
        
        # Test grid
        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # All available tests
        all_tests = [
            ("hardware_fingerprint", "🛡️", "Định danh phần cứng", Theme.INFO),
            ("license_check", "🔑", "Bản quyền Windows", Theme.SUCCESS),
            ("system_info", "💻", "Cấu hình hệ thống", Theme.INFO),
            ("harddrive_health", "💾", "Sức khỏe ổ cứng", Theme.WARNING),
            ("screen_test", "🖥️", "Kiểm tra màn hình", Theme.ACCENT),
            ("keyboard_test", "⌨️", "Bàn phím & Touchpad", Theme.SUCCESS),
            ("ports_test", "🔌", "Cổng kết nối", Theme.INFO),
            ("battery_test", "🔋", "Pin laptop", Theme.WARNING),
            ("audio_test", "🔊", "Loa & Micro", Theme.ACCENT),
            ("webcam_test", "📷", "Webcam", Theme.SUCCESS),
            ("network_test", "📶", "Mạng & WiFi", Theme.INFO),
            ("cpu_stress", "🧠", "CPU Stress Test", Theme.ERROR),
            ("gpu_stress", "🎮", "GPU Stress Test", Theme.ERROR),
            ("memory_test", "🧮", "Kiểm tra RAM", Theme.WARNING),
            ("thermal_test", "🌡️", "Kiểm tra nhiệt độ", Theme.ERROR),
            ("bios_check", "⚙️", "Kiểm tra BIOS", Theme.WARNING),
            ("physical_inspection", "🔍", "Kiểm tra ngoại hình", Theme.INFO)
        ]
        
        # Create grid
        grid_frame = ctk.CTkFrame(content, fg_color="transparent")
        grid_frame.pack(fill="x")
        grid_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, (test_key, icon, name, color) in enumerate(all_tests):
            row, col = i // 3, i % 3
            
            card = ctk.CTkFrame(grid_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            
            # Icon
            icon_label = ctk.CTkLabel(card, text=icon, font=("Segoe UI", 32))
            icon_label.pack(pady=(12, 8))
            
            # Name
            ctk.CTkLabel(card, text=name, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.TEXT, wraplength=150).pack(pady=(0, 8))
            
            # Run button
            ctk.CTkButton(card, text="▶️ Chạy test", font=Theme.SMALL_FONT, 
                         height=32, corner_radius=16, width=120,
                         fg_color=color, text_color="white",
                         command=lambda k=test_key: self.run_individual_test(k)).pack(pady=(0, 12))
    
    def run_individual_test(self, test_key):
        self.mode_callback(f"test_{test_key}")

# Mode Selection Frame
class ModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, mode_callback):
        super().__init__(master, fg_color="transparent")
        self.mode_callback = mode_callback
        self.create_ui()
    
    def create_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with logo
        header = ctk.CTkFrame(main_frame, fg_color=Theme.ACCENT, height=100)
        header.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Logo and title
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(fill="x")
        
        ctk.CTkLabel(title_frame, text="💻", font=("Segoe UI", 48)).pack(side="left")
        
        text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=(16, 0))
        
        ctk.CTkLabel(text_frame, text="LaptopTester Pro", font=Theme.TITLE_FONT, 
                    text_color="white").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="Professional Hardware Testing Suite", 
                    font=Theme.BODY_FONT, text_color="#E2E8F0").pack(anchor="w")
        
        # Tabview for different sections
        self.tabview = ctk.CTkTabview(main_frame, width=800, height=500)
        self.tabview.pack(fill="both", expand=True)
        
        # Overview tab
        self.tabview.add("🏠 " + get_text("overview"))
        self.create_overview_tab()
        
        # Individual tests tab
        self.tabview.add("🔧 " + get_text("individual_test"))
        individual_frame = IndividualTestFrame(self.tabview.tab("🔧 " + get_text("individual_test")), self.mode_callback)
        individual_frame.pack(fill="both", expand=True)
        
        # Mode selection tab
        self.tabview.add("🎯 Chọn chế độ")
        self.create_mode_tab()
        
        # Set default tab
        self.tabview.set("🏠 " + get_text("overview"))
    
    def create_overview_tab(self):
        overview_tab = self.tabview.tab("🏠 " + get_text("overview"))
        
        # Features grid
        features_frame = ctk.CTkFrame(overview_tab, fg_color="transparent")
        features_frame.pack(fill="x", padx=20, pady=20)
        features_frame.grid_columnconfigure((0, 1), weight=1)
        
        features = [
            ("🔍", "Comprehensive Analysis", "17+ detailed hardware & software tests", Theme.SUCCESS),
            ("⚡", "Lightning Fast", "Automated testing with real-time results", Theme.WARNING),
            ("📊", "Professional Reports", "Export detailed analysis reports", Theme.INFO),
            ("🛡️", "Safe & Secure", "Non-destructive testing with safety checks", Theme.ACCENT)
        ]
        
        for i, (icon, title, desc, color) in enumerate(features):
            row, col = i // 2, i % 2
            
            card = ctk.CTkFrame(features_frame, fg_color=Theme.FRAME)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=icon, font=("Segoe UI", 32), text_color=color).pack(pady=(16, 8))
            ctk.CTkLabel(card, text=title, font=Theme.SUBHEADING_FONT, text_color=Theme.TEXT).pack(pady=(0, 4))
            ctk.CTkLabel(card, text=desc, font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY, 
                        wraplength=250, justify="center").pack(pady=(0, 16), padx=16)
        
        # Quick start buttons
        action_frame = ctk.CTkFrame(overview_tab, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=20)
        action_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(action_frame, text="🚀 " + get_text("start_test").upper(),
                     font=Theme.SUBHEADING_FONT, height=50, corner_radius=25,
                     fg_color=Theme.SUCCESS, text_color="white",
                     command=lambda: self.mode_callback("basic")).grid(row=0, column=0, padx=10, sticky="ew")
        
        ctk.CTkButton(action_frame, text="🔧 " + get_text("individual_test").upper(),
                     font=Theme.SUBHEADING_FONT, height=50, corner_radius=25,
                     fg_color=Theme.ACCENT, text_color="white",
                     command=lambda: self.tabview.set("🔧 " + get_text("individual_test"))).grid(row=0, column=1, padx=10, sticky="ew")
    
    def create_mode_tab(self):
        mode_tab = self.tabview.tab("🎯 Chọn chế độ")
        
        # Mode selection cards
        mode_frame = ctk.CTkFrame(mode_tab, fg_color="transparent")
        mode_frame.pack(fill="both", expand=True, padx=20, pady=20)
        mode_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Basic mode card
        basic_card = ctk.CTkFrame(mode_frame, fg_color=Theme.FRAME)
        basic_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(basic_card, text="⚙️", font=("Segoe UI", 64)).pack(pady=20)
        ctk.CTkLabel(basic_card, text=get_text("basic_mode"), font=Theme.HEADING_FONT, 
                    text_color=Theme.ACCENT).pack(pady=10)
        ctk.CTkLabel(basic_card, text="11 bước kiểm tra cơ bản\nDành cho người dùng thông thường\nNhanh chóng và dễ hiểu", 
                    font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(pady=10)
        ctk.CTkButton(basic_card, text="Chọn chế độ cơ bản", 
                     command=lambda: self.mode_callback("basic"),
                     fg_color=Theme.SUCCESS, height=40).pack(pady=20)
        
        # Expert mode card
        expert_card = ctk.CTkFrame(mode_frame, fg_color=Theme.FRAME)
        expert_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(expert_card, text="🔥", font=("Segoe UI", 64)).pack(pady=20)
        ctk.CTkLabel(expert_card, text=get_text("expert_mode"), font=Theme.HEADING_FONT, 
                    text_color=Theme.ERROR).pack(pady=10)
        ctk.CTkLabel(expert_card, text="17 bước kiểm tra toàn diện\nBao gồm stress test nâng cao\nDành cho kỹ thuật viên", 
                    font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, justify="center").pack(pady=10)
        ctk.CTkButton(expert_card, text="Chọn chế độ chuyên gia", 
                     command=lambda: self.mode_callback("expert"),
                     fg_color=Theme.ERROR, height=40).pack(pady=20)

# Main Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=Theme.BACKGROUND)
        self.title(get_text("title"))
        self.state('zoomed')
        self.minsize(1200, 800)
        
        # Try to set icon
        try:
            self.iconbitmap(asset_path("icons/logo.ico"))
        except:
            pass
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.current_frame = None
        
        self.create_header()
        self.show_mode_selection()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        # Logo and title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=16, pady=8)
        
        ctk.CTkLabel(title_frame, text="💻", font=("Segoe UI", 24)).pack(side="left")
        ctk.CTkLabel(title_frame, text="LaptopTester Pro", font=Theme.SUBHEADING_FONT, 
                    text_color=Theme.ACCENT).pack(side="left", padx=(8, 0))
        
        # Controls
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.grid(row=0, column=2, padx=16, pady=8)
        
        # Theme toggle
        theme_text = "🌙" if CURRENT_THEME == "light" else "☀️"
        ctk.CTkButton(controls, text=theme_text, width=32, height=32, 
                     command=self.toggle_theme_and_refresh).pack(side="left", padx=2)
        
        # Language toggle
        lang_text = "🇺🇸" if CURRENT_LANG == "vi" else "🇻🇳"
        ctk.CTkButton(controls, text=lang_text, width=32, height=32, 
                     command=self.toggle_language_and_refresh).pack(side="left", padx=2)
        
        # Exit button
        ctk.CTkButton(controls, text="❌", width=32, height=32, command=self.quit,
                     fg_color=Theme.ERROR).pack(side="left", padx=2)
    
    def toggle_theme_and_refresh(self):
        toggle_theme()
        self.refresh_ui()
    
    def toggle_language_and_refresh(self):
        toggle_language()
        self.title(get_text("title"))
        self.refresh_ui()
    
    def refresh_ui(self):
        # Refresh current frame
        if hasattr(self.current_frame, 'refresh_ui'):
            self.current_frame.refresh_ui()
    
    def show_mode_selection(self):
        self.clear_frame()
        self.current_frame = ModeSelectionFrame(self, self.start_wizard)
        self.current_frame.grid(row=1, column=0, sticky="nsew")
    
    def start_wizard(self, mode):
        if mode.startswith("test_"):
            # Run individual test
            test_key = mode[5:]  # Remove "test_" prefix
            self.run_individual_test(test_key)
        else:
            # Start full wizard
            self.clear_frame()
            self.current_frame = WizardFrame(self, mode, app=self)
            self.current_frame.grid(row=1, column=0, sticky="nsew")
    
    def run_individual_test(self, test_key):
        # Map test keys to classes
        test_map = {
            "hardware_fingerprint": ("Định danh phần cứng", HardwareFingerprintStep),
            "license_check": ("Bản quyền Windows", LicenseCheckStep),
            "system_info": ("Cấu hình hệ thống", SystemInfoStep),
            "harddrive_health": ("Sức khỏe ổ cứng", HardDriveHealthStep),
            "screen_test": ("Kiểm tra màn hình", ScreenTestStep),
            "keyboard_test": ("Bàn phím & Touchpad", KeyboardTestStep),
            "ports_test": ("Cổng kết nối", PortsConnectivityStep),
            "battery_test": ("Pin laptop", BatteryHealthStep),
            "audio_test": ("Loa & Micro", AudioTestStep),
            "webcam_test": ("Webcam", WebcamTestStep),
            "network_test": ("Mạng & WiFi", NetworkTestStep),
            "cpu_stress": ("CPU Stress Test", CPUStressTestStep),
            "gpu_stress": ("GPU Stress Test", GPUStressTestStep),
            "memory_test": ("Kiểm tra RAM", MemoryTestStep),
            "thermal_test": ("Kiểm tra nhiệt độ", ThermalTestStep),
            "bios_check": ("Kiểm tra BIOS", BIOSCheckStep),
            "physical_inspection": ("Kiểm tra ngoại hình", PhysicalInspectionStep)
        }
        
        if test_key in test_map:
            self.clear_frame()
            test_name, test_class = test_map[test_key]
            
            # Create single test frame
            test_frame = ctk.CTkFrame(self, fg_color="transparent")
            test_frame.grid(row=1, column=0, sticky="nsew")
            test_frame.grid_columnconfigure(0, weight=1)
            test_frame.grid_rowconfigure(1, weight=1)
            
            # Header
            header = ctk.CTkFrame(test_frame, fg_color=Theme.ACCENT, height=60)
            header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
            header.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(header, text=f"Test: {test_name}", font=Theme.SUBHEADING_FONT, 
                        text_color="white").grid(row=0, column=0, padx=20, pady=15)
            ctk.CTkButton(header, text="⬅️ Quay lại", command=self.show_mode_selection, 
                         width=100, height=30, fg_color="white", text_color=Theme.ACCENT).grid(row=0, column=2, padx=20, pady=15)
            
            # Test content
            test_instance = test_class(
                test_frame,
                record_result_callback=lambda name, result: logger.info(f"Result: {name} - {result}"),
                enable_next_callback=lambda: None,
                go_to_next_step_callback=lambda: None,
                all_results={}
            )
            test_instance.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
            
            self.current_frame = test_frame
    
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Set initial theme
    ctk.set_appearance_mode(CURRENT_THEME)
    
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()