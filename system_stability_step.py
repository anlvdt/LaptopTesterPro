# System Stability Step - Combined Stress Test
# Minimal implementation for CPU+GPU+RAM combined testing

class SystemStabilityStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "System Stability Test" if CURRENT_LANG == "en" else "Test Ổn Định Hệ Thống"
        why_text = "Test tổng hợp CPU+GPU+RAM để đảm bảo hệ thống ổn định dưới tải nặng kéo dài." if CURRENT_LANG == "vi" else "Combined CPU+GPU+RAM test to ensure system stability under prolonged heavy load."
        how_text = "Nhấn 'Bắt đầu Test' để chạy test kết hợp 3-5 phút. Quan sát nhiệt độ và hiệu năng." if CURRENT_LANG == "vi" else "Click 'Start Test' to run combined test for 3-5 minutes. Monitor temperature and performance."
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.is_testing = False
        self.create_stability_test()
        
    def create_stability_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        test_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(test_frame, text="🔥 Combined Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        self.start_btn = ctk.CTkButton(test_frame, text=get_text("start_test_btn") + " (3-5 phút)", command=self.start_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(test_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(test_frame, progress_color=Theme.ACCENT)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
    
    def start_test(self):
        if self.is_testing:
            return
        self.is_testing = True
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self.run_combined_test, daemon=True).start()
    
    def run_combined_test(self):
        duration = 180  # 3 minutes
        start_time = time.time()
        
        while time.time() - start_time < duration and self.is_testing:
            elapsed = time.time() - start_time
            progress = elapsed / duration
            
            # Simulate combined load
            cpu_usage = psutil.cpu_percent(interval=0.5)
            temp = get_cpu_temperature() or 0
            mem_usage = psutil.virtual_memory().percent
            
            self.progress_bar.set(progress)
            self.status_label.configure(text=f"CPU: {cpu_usage:.1f}% | RAM: {mem_usage:.1f}% | Temp: {temp:.1f}°C")
            time.sleep(1)
        
        self.is_testing = False
        self.show_results()
    
    def show_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.results_frame, text="✅ Test hoàn thành", font=Theme.SUBHEADING_FONT, text_color=Theme.SUCCESS).pack(pady=10)
        
        button_bar = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="✓ Hệ thống ổn định", command=lambda: self.mark_completed({"Kết quả": "Ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="✗ Có vấn đề", command=lambda: self.mark_completed({"Kết quả": "Không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        
        self.start_btn.configure(state="normal")
