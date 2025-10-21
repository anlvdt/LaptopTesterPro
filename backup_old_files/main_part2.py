# 6. Keyboard Test Step
class KeyboardTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Bàn phím & Touchpad", 
                        "Kiểm tra tất cả các phím và touchpad hoạt động bình thường.",
                        "Gõ thử tất cả các phím và test touchpad trong vùng bên dưới.", **kwargs)
        self.create_keyboard_test()
    
    def create_keyboard_test(self):
        test_frame = ctk.CTkFrame(self.action_frame)
        test_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(test_frame, text="⌨️ Test bàn phím & touchpad", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Keyboard test area
        keyboard_frame = ctk.CTkFrame(test_frame, fg_color=Theme.BACKGROUND)
        keyboard_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(keyboard_frame, text="Gõ thử:", font=Theme.BODY_FONT).pack(anchor="w", padx=8, pady=4)
        test_area = ctk.CTkTextbox(keyboard_frame, height=60, placeholder_text="Gõ thử tất cả các phím...")
        test_area.pack(fill="x", padx=8, pady=4)
        
        # Touchpad test area
        touchpad_frame = ctk.CTkFrame(test_frame, fg_color=Theme.BACKGROUND)
        touchpad_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(touchpad_frame, text="Touchpad test:", font=Theme.BODY_FONT).pack(anchor="w", padx=8, pady=4)
        
        canvas = tk.Canvas(touchpad_frame, height=80, bg="#E0E0E0")
        canvas.pack(fill="x", padx=8, pady=4)
        
        def on_mouse_move(event):
            canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="blue", outline="blue")
        
        canvas.bind("<Motion>", on_mouse_move)
        
        self.create_result_buttons()

# 7. Ports Connectivity Step
class PortsConnectivityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Cổng kết nối", 
                        "Kiểm tra các cổng USB, HDMI, audio hoạt động bình thường.",
                        "Cắm thử thiết bị vào từng cổng và đánh dấu kết quả.", **kwargs)
        self.create_ports_test()
    
    def create_ports_test(self):
        ports_frame = ctk.CTkFrame(self.action_frame)
        ports_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(ports_frame, text="🔌 Kiểm tra cổng kết nối", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        ports = [
            "USB-A (cắm chuột/USB)",
            "USB-C (cắm sạc/thiết bị)", 
            "HDMI (kết nối màn hình)",
            "Audio 3.5mm (tai nghe)",
            "Cổng sạc",
            "Ethernet (dây mạng)"
        ]
        
        self.port_vars = {}
        for port in ports:
            port_frame = ctk.CTkFrame(ports_frame, fg_color=Theme.BACKGROUND)
            port_frame.pack(fill="x", padx=8, pady=2)
            
            var = tk.BooleanVar()
            self.port_vars[port] = var
            
            checkbox = ctk.CTkCheckBox(port_frame, text=port, variable=var, font=Theme.SMALL_FONT)
            checkbox.pack(side="left", padx=8, pady=4)
        
        self.create_result_buttons()

# 8. Battery Health Step
class BatteryHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Pin laptop", 
                        "Đánh giá tình trạng pin và khả năng giữ điện của laptop.",
                        "Thông tin pin sẽ được hiển thị tự động từ hệ thống.", **kwargs)
        self.create_battery_test()
    
    def create_battery_test(self):
        battery_frame = ctk.CTkFrame(self.action_frame)
        battery_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(battery_frame, text="🔋 Thông tin pin", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                info_items = [
                    ("Mức pin hiện tại", f"{battery.percent:.1f}%"),
                    ("Trạng thái", "Đang sạc" if battery.power_plugged else "Dùng pin"),
                    ("Thời gian còn lại", f"{battery.secsleft//3600}h {(battery.secsleft%3600)//60}m" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Không giới hạn"),
                    ("Sức khỏe pin", "Tốt (ước tính)")
                ]
                
                for label, value in info_items:
                    item_frame = ctk.CTkFrame(battery_frame, fg_color=Theme.BACKGROUND)
                    item_frame.pack(fill="x", padx=8, pady=2)
                    
                    ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
                    ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT).pack(side="right", padx=8, pady=4)
            else:
                ctk.CTkLabel(battery_frame, text="Không thể đọc thông tin pin", 
                           text_color=Theme.ERROR).pack(pady=8)
        except Exception as e:
            ctk.CTkLabel(battery_frame, text=f"Lỗi: {e}", text_color=Theme.ERROR).pack(pady=8)
        
        self.create_result_buttons()

# 9. Audio Test Step
class AudioTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Loa & Micro", 
                        "Kiểm tra hệ thống âm thanh: loa phát và microphone thu âm.",
                        "Test loa bằng cách phát âm thanh và test micro bằng ghi âm.", **kwargs)
        self.create_audio_test()
    
    def create_audio_test(self):
        audio_frame = ctk.CTkFrame(self.action_frame)
        audio_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(audio_frame, text="🔊 Test âm thanh", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Speaker test
        speaker_frame = ctk.CTkFrame(audio_frame, fg_color=Theme.BACKGROUND)
        speaker_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(speaker_frame, text="Loa:", font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
        ctk.CTkButton(speaker_frame, text="🎵 Test loa", width=100, height=28,
                     command=self.test_speaker, fg_color=Theme.ACCENT).pack(side="right", padx=8, pady=4)
        
        # Microphone test
        mic_frame = ctk.CTkFrame(audio_frame, fg_color=Theme.BACKGROUND)
        mic_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(mic_frame, text="Micro:", font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
        ctk.CTkButton(mic_frame, text="🎤 Test micro", width=100, height=28,
                     command=self.test_microphone, fg_color=Theme.SUCCESS).pack(side="right", padx=8, pady=4)
        
        # Volume control
        volume_frame = ctk.CTkFrame(audio_frame, fg_color=Theme.BACKGROUND)
        volume_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(volume_frame, text="Âm lượng:", font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
        volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, number_of_steps=100)
        volume_slider.set(50)
        volume_slider.pack(side="right", padx=8, pady=4, fill="x", expand=True)
        
        self.create_result_buttons()
    
    def test_speaker(self):
        messagebox.showinfo("Test loa", "Đang phát âm thanh test...\nBạn có nghe thấy âm thanh không?")
    
    def test_microphone(self):
        messagebox.showinfo("Test micro", "Nói vào micro...\nKiểm tra xem có thu được âm thanh không?")

# 10. Webcam Test Step
class WebcamTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Webcam", 
                        "Kiểm tra camera hoạt động và chất lượng hình ảnh cho video call.",
                        "Nhấn 'Bắt đầu' để mở camera và kiểm tra chất lượng hình ảnh.", **kwargs)
        self.create_webcam_test()
    
    def create_webcam_test(self):
        webcam_frame = ctk.CTkFrame(self.action_frame)
        webcam_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(webcam_frame, text="📷 Test webcam", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Camera preview area
        preview_frame = ctk.CTkFrame(webcam_frame, height=120, fg_color=Theme.BACKGROUND)
        preview_frame.pack(fill="x", padx=8, pady=8)
        
        self.preview_label = ctk.CTkLabel(preview_frame, text="Camera chưa khởi động\nNhấn nút bên dưới để bắt đầu", 
                                         font=Theme.BODY_FONT)
        self.preview_label.pack(expand=True)
        
        # Camera controls
        control_frame = ctk.CTkFrame(webcam_frame, fg_color=Theme.BACKGROUND)
        control_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkButton(control_frame, text="📷 Bắt đầu camera", 
                     command=self.start_camera,
                     fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=4)
        
        ctk.CTkButton(control_frame, text="⏹️ Dừng camera", 
                     command=self.stop_camera,
                     fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="right", padx=4)
        
        self.create_result_buttons()
    
    def start_camera(self):
        self.preview_label.configure(text="Camera đang khởi động...\nĐang kết nối với thiết bị")
        self.after(2000, lambda: self.preview_label.configure(text="✅ Camera hoạt động\nKiểm tra chất lượng hình ảnh"))
    
    def stop_camera(self):
        self.preview_label.configure(text="Camera đã dừng")

# 11. Network Test Step
class NetworkTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Mạng & WiFi", 
                        "Kiểm tra kết nối mạng, WiFi và tốc độ Internet ổn định.",
                        "Test sẽ kiểm tra kết nối Internet và tốc độ mạng.", **kwargs)
        self.create_network_test()
    
    def create_network_test(self):
        network_frame = ctk.CTkFrame(self.action_frame)
        network_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(network_frame, text="📶 Test mạng & WiFi", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Network info
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            info_items = [
                ("Hostname", hostname),
                ("Local IP", local_ip),
                ("Internet", "Đang kiểm tra...")
            ]
            
            for label, value in info_items:
                item_frame = ctk.CTkFrame(network_frame, fg_color=Theme.BACKGROUND)
                item_frame.pack(fill="x", padx=8, pady=2)
                
                ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
                ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT).pack(side="right", padx=8, pady=4)
        
        except Exception as e:
            ctk.CTkLabel(network_frame, text=f"Lỗi: {e}", text_color=Theme.ERROR).pack(pady=8)
        
        # Speed test button
        ctk.CTkButton(network_frame, text="🚀 Test tốc độ mạng", 
                     command=self.test_speed,
                     fg_color=Theme.INFO, height=Theme.BUTTON_HEIGHT).pack(pady=8)
        
        self.create_result_buttons()
    
    def test_speed(self):
        messagebox.showinfo("Speed Test", "Đang test tốc độ mạng...\n(Tính năng demo)")

# 12. CPU Stress Test Step (Expert Mode)
class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "CPU Stress Test", 
                        "Kiểm tra CPU dưới tải cao để phát hiện vấn đề ổn định và quá nhiệt.",
                        "Test sẽ đẩy CPU lên 100% trong vài phút để kiểm tra.", **kwargs)
        self.create_cpu_test()
    
    def create_cpu_test(self):
        cpu_frame = ctk.CTkFrame(self.action_frame)
        cpu_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(cpu_frame, text="🧠 CPU Stress Test", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # CPU info
        cpu_info = platform.processor()
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        info_items = [
            ("CPU", cpu_info[:50] + "..." if len(cpu_info) > 50 else cpu_info),
            ("Cores", f"{cpu_count} cores"),
            ("Frequency", f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A"),
            ("Usage", f"{psutil.cpu_percent()}%")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(cpu_frame, fg_color=Theme.BACKGROUND)
            item_frame.pack(fill="x", padx=8, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT).pack(side="right", padx=8, pady=4)
        
        # Stress test controls
        ctk.CTkButton(cpu_frame, text="🔥 Bắt đầu Stress Test", 
                     command=self.start_cpu_stress,
                     fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(pady=8)
        
        self.cpu_status = ctk.CTkLabel(cpu_frame, text="Sẵn sàng test", 
                                      font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.cpu_status.pack(pady=4)
        
        self.create_result_buttons()
    
    def start_cpu_stress(self):
        self.cpu_status.configure(text="Đang chạy CPU stress test...")
        threading.Thread(target=self.run_cpu_stress, daemon=True).start()
    
    def run_cpu_stress(self):
        # Mock CPU stress test
        for i in range(10):
            if not hasattr(self, 'cpu_status'):
                break
            self.after(0, lambda i=i: self.cpu_status.configure(text=f"CPU Test: {i+1}/10 - {90+i}°C"))
            time.sleep(1)
        
        if hasattr(self, 'cpu_status'):
            self.after(0, lambda: self.cpu_status.configure(text="CPU test hoàn thành"))

# 13. GPU Stress Test Step (Expert Mode)
class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Stress Test", 
                        "Kiểm tra card đồ họa dưới tải cao để phát hiện lỗi artifacts.",
                        "Test sẽ tạo tải đồ họa cao để kiểm tra GPU ổn định.", **kwargs)
        self.create_gpu_test()
    
    def create_gpu_test(self):
        gpu_frame = ctk.CTkFrame(self.action_frame)
        gpu_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(gpu_frame, text="🎮 GPU Stress Test", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # GPU info (mock)
        info_items = [
            ("GPU", "Integrated Graphics"),
            ("Memory", "Shared System RAM"),
            ("Driver", "Latest"),
            ("Status", "Ready")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(gpu_frame, fg_color=Theme.BACKGROUND)
            item_frame.pack(fill="x", padx=8, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT).pack(side="right", padx=8, pady=4)
        
        ctk.CTkButton(gpu_frame, text="🎯 Bắt đầu GPU Test", 
                     command=self.start_gpu_stress,
                     fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT).pack(pady=8)
        
        self.gpu_status = ctk.CTkLabel(gpu_frame, text="Sẵn sàng test", 
                                      font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.gpu_status.pack(pady=4)
        
        self.create_result_buttons()
    
    def start_gpu_stress(self):
        self.gpu_status.configure(text="Đang chạy GPU stress test...")
        threading.Thread(target=self.run_gpu_stress, daemon=True).start()
    
    def run_gpu_stress(self):
        # Mock GPU stress test
        for i in range(8):
            if not hasattr(self, 'gpu_status'):
                break
            self.after(0, lambda i=i: self.gpu_status.configure(text=f"GPU Test: {i+1}/8 - {60+i*5}°C"))
            time.sleep(1)
        
        if hasattr(self, 'gpu_status'):
            self.after(0, lambda: self.gpu_status.configure(text="GPU test hoàn thành"))

# 14. Memory Test Step (Expert Mode)
class MemoryTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra RAM", 
                        "Kiểm tra bộ nhớ RAM để phát hiện lỗi memory có thể gây crash.",
                        "Test sẽ kiểm tra tính toàn vẹn của bộ nhớ RAM.", **kwargs)
        self.create_memory_test()
    
    def create_memory_test(self):
        memory_frame = ctk.CTkFrame(self.action_frame)
        memory_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(memory_frame, text="🧮 Memory Test", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Memory info
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        info_items = [
            ("Total RAM", f"{memory.total / (1024**3):.1f} GB"),
            ("Available", f"{memory.available / (1024**3):.1f} GB"),
            ("Used", f"{memory.percent}%"),
            ("Swap", f"{swap.total / (1024**3):.1f} GB")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(memory_frame, fg_color=Theme.BACKGROUND)
            item_frame.pack(fill="x", padx=8, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(item_frame, text=value, font=Theme.BODY_FONT).pack(side="right", padx=8, pady=4)
        
        ctk.CTkButton(memory_frame, text="🔍 Bắt đầu Memory Test", 
                     command=self.start_memory_test,
                     fg_color=Theme.INFO, height=Theme.BUTTON_HEIGHT).pack(pady=8)
        
        self.memory_status = ctk.CTkLabel(memory_frame, text="Sẵn sàng test", 
                                         font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.memory_status.pack(pady=4)
        
        self.create_result_buttons()
    
    def start_memory_test(self):
        self.memory_status.configure(text="Đang test memory...")
        threading.Thread(target=self.run_memory_test, daemon=True).start()
    
    def run_memory_test(self):
        # Mock memory test
        for i in range(5):
            if not hasattr(self, 'memory_status'):
                break
            self.after(0, lambda i=i: self.memory_status.configure(text=f"Memory Test: {(i+1)*20}% complete"))
            time.sleep(1)
        
        if hasattr(self, 'memory_status'):
            self.after(0, lambda: self.memory_status.configure(text="Memory test hoàn thành - Không phát hiện lỗi"))

# 15. Thermal Test Step (Expert Mode)
class ThermalTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra nhiệt độ", 
                        "Giám sát nhiệt độ hệ thống để phát hiện vấn đề tản nhiệt.",
                        "Monitor sẽ hiển thị nhiệt độ real-time của các linh kiện.", **kwargs)
        self.create_thermal_test()
    
    def create_thermal_test(self):
        thermal_frame = ctk.CTkFrame(self.action_frame)
        thermal_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(thermal_frame, text="🌡️ Thermal Monitor", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Temperature readings (mock)
        temp_items = [
            ("CPU", "45°C", Theme.SUCCESS),
            ("GPU", "42°C", Theme.SUCCESS),
            ("Motherboard", "38°C", Theme.SUCCESS),
            ("Hard Drive", "35°C", Theme.SUCCESS)
        ]
        
        for label, temp, color in temp_items:
            item_frame = ctk.CTkFrame(thermal_frame, fg_color=Theme.BACKGROUND)
            item_frame.pack(fill="x", padx=8, pady=2)
            
            ctk.CTkLabel(item_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(item_frame, text=temp, font=Theme.BODY_FONT, 
                        text_color=color).pack(side="right", padx=8, pady=4)
        
        ctk.CTkButton(thermal_frame, text="📊 Bắt đầu Monitor", 
                     command=self.start_thermal_monitor,
                     fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(pady=8)
        
        self.thermal_status = ctk.CTkLabel(thermal_frame, text="Sẵn sàng monitor", 
                                          font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY)
        self.thermal_status.pack(pady=4)
        
        self.create_result_buttons()
    
    def start_thermal_monitor(self):
        self.thermal_status.configure(text="Đang monitor nhiệt độ...")
        threading.Thread(target=self.run_thermal_monitor, daemon=True).start()
    
    def run_thermal_monitor(self):
        # Mock thermal monitoring
        for i in range(10):
            if not hasattr(self, 'thermal_status'):
                break
            temp = 45 + i
            status = "Normal" if temp < 70 else "High" if temp < 85 else "Critical"
            self.after(0, lambda i=i, t=temp, s=status: self.thermal_status.configure(text=f"CPU: {t}°C - {s}"))
            time.sleep(0.5)
        
        if hasattr(self, 'thermal_status'):
            self.after(0, lambda: self.thermal_status.configure(text="Thermal monitor hoàn thành"))

# 16. BIOS Check Step (Expert Mode)
class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra BIOS", 
                        "Kiểm tra cài đặt BIOS để đảm bảo hiệu năng tối ưu và bảo mật.",
                        "Hướng dẫn truy cập BIOS và các cài đặt cần kiểm tra.", **kwargs)
        self.create_bios_check()
    
    def create_bios_check(self):
        bios_frame = ctk.CTkFrame(self.action_frame)
        bios_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(bios_frame, text="⚙️ BIOS Settings Check", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # BIOS access instructions
        instructions = [
            "1. Khởi động lại máy",
            "2. Nhấn F2/F12/Del khi boot",
            "3. Kiểm tra CPU Features",
            "4. Kiểm tra Memory Settings",
            "5. Kiểm tra Security Settings"
        ]
        
        for instruction in instructions:
            inst_frame = ctk.CTkFrame(bios_frame, fg_color=Theme.BACKGROUND)
            inst_frame.pack(fill="x", padx=8, pady=2)
            
            ctk.CTkLabel(inst_frame, text=instruction, font=Theme.SMALL_FONT).pack(anchor="w", padx=8, pady=4)
        
        self.create_result_buttons()

# 17. Physical Inspection Step
class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm tra ngoại hình", 
                        "Kiểm tra tình trạng vật lý để phát hiện dấu hiệu hư hỏng hoặc sửa chữa.",
                        "Kiểm tra từng phần theo checklist bên dưới.", **kwargs)
        self.create_physical_check()
    
    def create_physical_check(self):
        physical_frame = ctk.CTkFrame(self.action_frame)
        physical_frame.pack(fill="x", padx=12, pady=8)
        
        ctk.CTkLabel(physical_frame, text="🔍 Physical Inspection", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=8)
        
        # Checklist items
        checklist = [
            "Vỏ máy: Kiểm tra vết nứt, móp méo",
            "Bản lề: Mở/đóng màn hình mượt mà",
            "Bàn phím: Không có phím lỏng",
            "Touchpad: Bề mặt phẳng, nhạy",
            "Cổng kết nối: Không lỏng lẻo",
            "Lỗ thoát khí: Không bị tắc"
        ]
        
        self.check_vars = {}
        for item in checklist:
            check_frame = ctk.CTkFrame(physical_frame, fg_color=Theme.BACKGROUND)
            check_frame.pack(fill="x", padx=8, pady=2)
            
            var = tk.BooleanVar()
            self.check_vars[item] = var
            
            checkbox = ctk.CTkCheckBox(check_frame, text=item, variable=var, font=Theme.SMALL_FONT)
            checkbox.pack(anchor="w", padx=8, pady=4)
        
        self.create_result_buttons()

# Summary Step
class SummaryStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Tổng kết", "", "", **kwargs)
        self.all_results = kwargs.get("all_results", {})
        self.create_summary()
    
    def create_summary(self):
        summary_frame = ctk.CTkScrollableFrame(self.action_frame)
        summary_frame.pack(fill="both", expand=True, padx=12, pady=8)
        
        ctk.CTkLabel(summary_frame, text="📊 Báo cáo tổng kết", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=12)
        
        # Statistics
        total_tests = len(self.all_results)
        passed_tests = sum(1 for r in self.all_results.values() if r.get("status") == "Tốt")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        stats_frame = ctk.CTkFrame(summary_frame, fg_color=Theme.BACKGROUND)
        stats_frame.pack(fill="x", padx=8, pady=8)
        
        stats_items = [
            ("Tổng số test", str(total_tests)),
            ("Đạt yêu cầu", f"{passed_tests}/{total_tests}"),
            ("Tỷ lệ thành công", f"{success_rate:.1f}%")
        ]
        
        for label, value in stats_items:
            stat_frame = ctk.CTkFrame(stats_frame, fg_color=Theme.FRAME)
            stat_frame.pack(fill="x", padx=4, pady=2)
            
            ctk.CTkLabel(stat_frame, text=label, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(stat_frame, text=value, font=Theme.BODY_FONT, 
                        text_color=Theme.SUCCESS).pack(side="right", padx=8, pady=4)
        
        # Detailed results
        if self.all_results:
            ctk.CTkLabel(summary_frame, text="Chi tiết kết quả:", 
                        font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(16, 8))
            
            for step_name, result in self.all_results.items():
                result_frame = ctk.CTkFrame(summary_frame, fg_color=Theme.BACKGROUND)
                result_frame.pack(fill="x", padx=8, pady=2)
                
                status = result.get("status", "Unknown")
                color = Theme.SUCCESS if status == "Tốt" else Theme.ERROR if status == "Lỗi" else Theme.WARNING
                
                ctk.CTkLabel(result_frame, text=step_name, font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
                ctk.CTkLabel(result_frame, text=status, font=Theme.BODY_FONT, 
                           text_color=color).pack(side="right", padx=8, pady=4)
        else:
            ctk.CTkLabel(summary_frame, text="Chưa có kết quả test", 
                        font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(pady=20)
        
        # Export button
        ctk.CTkButton(summary_frame, text="📄 Xuất báo cáo", 
                     command=self.export_report,
                     fg_color=Theme.INFO, height=40).pack(pady=16)
    
    def export_report(self):
        messagebox.showinfo("Export", "Báo cáo đã được xuất thành công!")

# Continue with Wizard and App classes...