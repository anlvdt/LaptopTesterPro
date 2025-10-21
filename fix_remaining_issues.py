#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining translation and display issues"""

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix BIOSCheckStep translations
old_bios = '''class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = "Xem checklist bên dưới để kiểm tra từng mục trong BIOS"
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS", 
            "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp.", 
            how_text, **kwargs)'''

new_bios = '''class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        if CURRENT_LANG == "vi":
            why_text = "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp."
            how_text = "Khởi động lại máy và nhấn phím (F2/F10/Del) để vào BIOS. Xem checklist bên dưới để kiểm tra từng mục. Nhấn ESC để thoát BIOS khi xong."
        else:
            why_text = "BIOS contains fundamental settings. Check to ensure optimal performance and not locked by enterprise features."
            how_text = "Restart and press key (F2/F10/Del) to enter BIOS. Check each item in checklist below. Press ESC to exit BIOS when done."
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS" if CURRENT_LANG == "vi" else "BIOS Settings Check", 
            why_text, how_text, **kwargs)'''

content = content.replace(old_bios, new_bios)

# 2. Fix duplicate CPUStressTestStep (line 3023) - add translations
old_cpu_dup = '''class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "CPU Stress Test", 
            t("Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt."), 
            t("Nhấn 'Bắt đầu Test' trong 2-5 phút. Theo dõi nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt."), **kwargs)'''

new_cpu_dup = '''class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        if CURRENT_LANG == "vi":
            why_text = "Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt."
            how_text = "Nhấn 'Bắt đầu Test' để chạy test 30 giây. Theo dõi nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt."
        else:
            why_text = "An overheating CPU will throttle performance causing lag. This test pushes CPU to 100% load to check cooling capability."
            how_text = "Click 'Start Test' to run 30-second test. Monitor temperature. If temperature stays below 95°C without freezing, cooling system works well."
        super().__init__(master, "CPU Stress Test", why_text, how_text, **kwargs)'''

content = content.replace(old_cpu_dup, new_cpu_dup)

# 3. Fix duplicate GPUStressTestStep (line 3068) - add translations
old_gpu_dup = '''class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Stress Test", 
            t("GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng."), 
            t("Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 60 giây. Hãy quan sát có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?"), **kwargs)'''

new_gpu_dup = '''class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        if CURRENT_LANG == "vi":
            why_text = "GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng."
            how_text = "Nhấn 'Bắt đầu Test' để tạo cửa sổ đồ họa nặng trong 60 giây. Quan sát có hiện tượng chớp giật, sọc ngang, hay đốm màu lạ không?"
        else:
            why_text = "GPU is the heart of graphics and gaming. A faulty or overheating GPU can cause artifacts, freezing or severe FPS drops."
            how_text = "Click 'Start Test' to create heavy graphics window for 60 seconds. Watch for flickering, lines, or color artifacts."
        super().__init__(master, "GPU Stress Test", why_text, how_text, **kwargs)'''

content = content.replace(old_gpu_dup, new_gpu_dup)

# 4. Fix HDD speed test status translations
old_hdd_status = '''            queue.put({'type': 'update', 'progress': progress, 'operation': 'Write', 'speed': chunk_speed, 'avg_speed': avg_speed})'''
new_hdd_status = '''            operation_text = "Ghi" if CURRENT_LANG == "vi" else "Write"
            queue.put({'type': 'update', 'progress': progress, 'operation': operation_text, 'speed': chunk_speed, 'avg_speed': avg_speed})'''
content = content.replace(old_hdd_status, new_hdd_status)

old_hdd_read = '''            queue.put({'type': 'update', 'progress': progress, 'operation': 'Read', 'speed': chunk_speed, 'avg_speed': avg_speed})'''
new_hdd_read = '''            operation_text = "Đọc" if CURRENT_LANG == "vi" else "Read"
            queue.put({'type': 'update', 'progress': progress, 'operation': operation_text, 'speed': chunk_speed, 'avg_speed': avg_speed})'''
content = content.replace(old_hdd_read, new_hdd_read)

# 5. Add stop button to duplicate CPU test (line 3032)
old_cpu_test_ui = '''    def create_cpu_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(control_frame, text="CPU Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(control_frame, text=t("Bắt đầu Test"), command=self.start_cpu_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(control_frame, text=t("Sẵn sàng test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)'''

new_cpu_test_ui = '''    def create_cpu_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(control_frame, text="CPU Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        
        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        self.start_btn = ctk.CTkButton(btn_frame, text=get_text("start_test_btn"), command=self.start_cpu_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(btn_frame, text=get_text("stop_test_btn"), command=self.stop_cpu_test, fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(control_frame, text=get_text("ready_to_test"), font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)'''

content = content.replace(old_cpu_test_ui, new_cpu_test_ui)

# Add stop function for duplicate CPU test
old_cpu_start = '''    def start_cpu_test(self):
        import threading, time, psutil
        def cpu_stress():
            self.start_btn.configure(state="disabled")
            for i in range(30):'''

new_cpu_start = '''    def start_cpu_test(self):
        import threading, time, psutil
        self.is_testing = True
        def cpu_stress():
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            for i in range(30):
                if not self.is_testing:
                    break'''

content = content.replace(old_cpu_start, new_cpu_start)

# Add stop method after start_cpu_test
old_show_cpu = '''    def show_cpu_results(self):'''
new_show_cpu = '''    def stop_cpu_test(self):
        self.is_testing = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text=get_text("finished"))
    
    def show_cpu_results(self):'''

content = content.replace(old_show_cpu, new_show_cpu)

# Fix end of cpu_stress to enable buttons
old_cpu_end = '''            self.show_cpu_results()
        threading.Thread(target=cpu_stress, daemon=True).start()'''

new_cpu_end = '''            self.is_testing = False
            self.after(0, self.show_cpu_results)
        threading.Thread(target=cpu_stress, daemon=True).start()'''

content = content.replace(old_cpu_end, new_cpu_end)

# Fix show_cpu_results to reset buttons
old_cpu_results = '''    def show_cpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text=t("Kết quả CPU Test:"), font=Theme.SUBHEADING_FONT).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text=t("CPU hoạt động tốt"), command=lambda: self.mark_completed({"Kết quả": "CPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text=t("CPU có vấn đề"), command=lambda: self.mark_completed({"Kết quả": "CPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")'''

new_cpu_results = '''    def show_cpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        result_text = "Kết quả CPU Test:" if CURRENT_LANG == "vi" else "CPU Test Results:"
        ctk.CTkLabel(self.results_frame, text=result_text, font=Theme.SUBHEADING_FONT).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        good_text = "CPU hoạt động tốt" if CURRENT_LANG == "vi" else "CPU works well"
        bad_text = "CPU có vấn đề" if CURRENT_LANG == "vi" else "CPU has issues"
        ctk.CTkButton(button_bar, text=good_text, command=lambda: self.mark_completed({"Kết quả": "CPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text=bad_text, command=lambda: self.mark_completed({"Kết quả": "CPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")'''

content = content.replace(old_cpu_results, new_cpu_results)

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Fixed:")
print("1. BIOS check translations")
print("2. Duplicate CPU/GPU test translations")
print("3. HDD speed test status translations")
print("4. Added stop button to duplicate CPU test")
print("5. Thermal GPU data already added in previous fix")
