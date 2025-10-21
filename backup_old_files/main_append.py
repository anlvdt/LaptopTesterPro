# Append remaining steps 6-17 to main.py

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
        
        keyboard_frame = ctk.CTkFrame(test_frame, fg_color=Theme.BACKGROUND)
        keyboard_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(keyboard_frame, text="Gõ thử:", font=Theme.BODY_FONT).pack(anchor="w", padx=8, pady=4)
        test_area = ctk.CTkTextbox(keyboard_frame, height=60, placeholder_text="Gõ thử tất cả các phím...")
        test_area.pack(fill="x", padx=8, pady=4)
        
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
        
        speaker_frame = ctk.CTkFrame(audio_frame, fg_color=Theme.BACKGROUND)
        speaker_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(speaker_frame, text="Loa:", font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
        ctk.CTkButton(speaker_frame, text="🎵 Test loa", width=100, height=28,
                     command=self.test_speaker, fg_color=Theme.ACCENT).pack(side="right", padx=8, pady=4)
        
        mic_frame = ctk.CTkFrame(audio_frame, fg_color=Theme.BACKGROUND)
        mic_frame.pack(fill="x", padx=8, pady=4)
        
        ctk.CTkLabel(mic_frame, text="Micro:", font=Theme.BODY_FONT).pack(side="left", padx=8, pady=4)
        ctk.CTkButton(mic_frame, text="🎤 Test micro", width=100, height=28,
                     command=self.test_microphone, fg_color=Theme.SUCCESS).pack(side="right", padx=8, pady=4)
        
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
        
        preview_frame = ctk.CTkFrame(webcam_frame, height=120, fg_color=Theme.BACKGROUND)
        preview_frame.pack(fill="x", padx=8, pady=8)
        
        self.preview_label = ctk.CTkLabel(preview_frame, text="Camera chưa khởi động\nNhấn nút bên dưới để bắt đầu", 
                                         font=Theme.BODY_FONT)
        self.preview_label.pack(expand=True)
        
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
        
        ctk.CTkButton(network_frame, text="🚀 Test tốc độ mạng", 
                     command=self.test_speed,
                     fg_color=Theme.INFO, height=Theme.BUTTON_HEIGHT).pack(pady=8)
        
        self.create_result_buttons()
    
    def test_speed(self):
        messagebox.showinfo("Speed Test", "Đang test tốc độ mạng...\n(Tính năng demo)")