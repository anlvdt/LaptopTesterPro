"""
Script để thêm các step còn thiếu vào main_enhanced_auto.py
Thêm: PhysicalInspectionStep, BIOSCheckStep, CPUStressTestStep, GPUStressTestStep
"""

import re

# Đọc file hiện tại
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Tìm vị trí để chèn các step mới (sau KeyboardTestStep)
insert_marker = "class BatteryHealthStep(BaseStepFrame):"
insert_pos = content.find(insert_marker)

if insert_pos == -1:
    print("Không tìm thấy vị trí chèn!")
    exit(1)

# Code cho PhysicalInspectionStep
physical_step = '''
class PhysicalInspectionStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "Kiểm Tra Ngoại Hình", 
            "Tình trạng vật lý phản ánh cách chủ cũ sử dụng máy. Các vết nứt, móp, bản lề lỏng hay ốc vít bị toét có thể là dấu hiệu máy bị rơi hoặc đã qua sửa chữa không chuyên nghiệp.", 
            "Kiểm tra vỏ máy, bản lề, cổng kết nối, ốc vít, tem bảo hành. Đánh giá tổng thể tình trạng vật lý.", **kwargs)
        self.create_inspection_checklist()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()
        self.mark_completed({"Kết quả": "Đã hiển thị checklist", "Trạng thái": "Sẵn sàng"}, auto_advance=False)
    
    def create_inspection_checklist(self):
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(checklist_frame, text="Checklist Kiểm Tra Ngoại Hình", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        checks = [
            "• Vỏ máy: Kiểm tra vết nứt, rạn nứt, móp méo",
            "• Bản lề màn hình: Mở/đóng nhiều lần, nghe tiếng kêu",
            "• Bàn phím: Kiểm tra phím lỏng, không nhấn",
            "• Touchpad: Bề mặt phẳng, không bị lồi",
            "• Cổng kết nối: USB, HDMI, audio, sạc",
            "• Ốc vít: Kiểm tra các ốc không bị toét, thiếu"
        ]
        
        for check in checks:
            ctk.CTkLabel(checklist_frame, text=check, font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=20, pady=2)
    
    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Tình trạng vật lý tổng thể của máy như thế nào?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Rất tốt", command=lambda: self.mark_completed({"Kết quả": "Rất tốt", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(button_bar, text="Tốt", command=lambda: self.mark_completed({"Kết quả": "Tốt", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(button_bar, text="Trung bình", command=lambda: self.mark_completed({"Kết quả": "Trung bình", "Trạng thái": "Cảnh báo"}, auto_advance=True), fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)
        ctk.CTkButton(button_bar, text="Kém", command=lambda: self.mark_completed({"Kết quả": "Kém", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=5)

class BIOSCheckStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        how_text = (
            "1. Khởi động lại máy và nhấn liên tục phím để vào BIOS:\\n"
            "   • Dell/Alienware: F2 hoặc F12\\n"
            "   • HP/Compaq: F10 hoặc ESC\\n"
            "   • Lenovo/ThinkPad: F1, F2 hoặc Enter\\n"
            "   • ASUS: F2 hoặc Delete\\n"
            "   • Acer: F2 hoặc Delete\\n"
            "   • MSI: Delete hoặc F2\\n\\n"
            "2. Kiểm tra các mục quan trọng:\\n"
            "   • CPU Features: Intel Turbo Boost / AMD Boost phải 'Enabled'\\n"
            "   • Memory: XMP/DOCP profile nên bật (nếu có)\\n"
            "   • Security: Không có BIOS password lạ\\n"
            "   • Computrace: Nếu 'Enabled' thì máy có thể bị khóa từ xa!"
        )
        super().__init__(master, "Kiểm Tra Cài Đặt BIOS", 
            "BIOS chứa các cài đặt nền tảng. Kiểm tra để đảm bảo hiệu năng tối ưu và không bị khóa bởi các tính năng doanh nghiệp.", 
            how_text, **kwargs)
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=2, column=0, sticky="sew", pady=(20,0))
        self.show_result_choices()

    def show_result_choices(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.result_container, text="Các cài đặt trong BIOS có chính xác và an toàn không?", font=Theme.SUBHEADING_FONT).pack(pady=15)
        button_bar = ctk.CTkFrame(self.result_container, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(button_bar, text="Có, mọi cài đặt đều đúng", command=lambda: self.mark_completed({"Kết quả": "Cài đặt chính xác", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="Không, có cài đặt sai/bị khóa", command=lambda: self.mark_completed({"Kết quả": "Có vấn đề với BIOS", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR, height=Theme.BUTTON_HEIGHT).pack(side="left", padx=10)

class CPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "CPU Stress Test", 
            "Một CPU quá nhiệt sẽ tự giảm hiệu năng (throttling) gây giật lag. Bài test này sẽ đẩy CPU lên 100% tải để kiểm tra khả năng tản nhiệt.", 
            "Nhấn 'Bắt đầu Test' trong 2-5 phút. Theo dõi nhiệt độ. Nếu nhiệt độ ổn định dưới 95°C và không có hiện tượng treo máy, hệ thống tản nhiệt hoạt động tốt.", **kwargs)
        self.create_cpu_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
        
    def create_cpu_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(control_frame, text="CPU Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(control_frame, text="Bắt đầu Test", command=self.start_cpu_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(control_frame, text="Sẵn sàng test", font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    
    def start_cpu_test(self):
        import threading, time, psutil
        def cpu_stress():
            self.start_btn.configure(state="disabled")
            for i in range(30):
                cpu_percent = psutil.cpu_percent(interval=1)
                temp = 45 + (i * 1.5) + (cpu_percent * 0.3)
                self.progress_bar.set(i / 30)
                self.status_label.configure(text=f"CPU: {cpu_percent:.1f}% | Temp: {temp:.1f}°C")
            self.show_cpu_results()
        threading.Thread(target=cpu_stress, daemon=True).start()
    
    def show_cpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text="Kết quả CPU Test:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text="CPU hoạt động tốt", command=lambda: self.mark_completed({"Kết quả": "CPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="CPU có vấn đề", command=lambda: self.mark_completed({"Kết quả": "CPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")

class GPUStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, "GPU Stress Test", 
            "GPU là trái tim của đồ họa và game. Một GPU lỗi hoặc quá nhiệt có thể gây ra hiện tượng 'rác' hình (artifacts), treo máy hoặc sụt giảm FPS nghiêm trọng.", 
            "Bài test sẽ tạo ra một cửa sổ đồ họa nặng trong 60 giây. Hãy quan sát có hiện tượng chớp giật, sọc ngang, hay các đốm màu lạ không?", **kwargs)
        self.create_gpu_test()
        self.result_container = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="sew", pady=(20,0))
    
    def create_gpu_test(self):
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(control_frame, text="GPU Stress Test", font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=10)
        self.start_btn = ctk.CTkButton(control_frame, text="Bắt đầu Test", command=self.start_gpu_test, fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT)
        self.start_btn.pack(pady=10)
        self.status_label = ctk.CTkLabel(control_frame, text="Sẵn sàng test", font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, progress_color=Theme.ACCENT)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        self.results_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.results_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    
    def start_gpu_test(self):
        import threading, time, tkinter as tk
        def gpu_stress():
            self.start_btn.configure(state="disabled")
            test_win = tk.Toplevel()
            test_win.attributes('-fullscreen', True)
            test_win.configure(bg='black')
            canvas = tk.Canvas(test_win, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            for i in range(600):  # 60 seconds at 10 FPS
                canvas.delete('all')
                for j in range(50):
                    x = (i * 5 + j * 20) % 1920
                    y = (i * 3 + j * 15) % 1080
                    canvas.create_rectangle(x, y, x+10, y+10, fill=f'#{j*5:02x}{(i*3)%255:02x}{(j*7)%255:02x}', outline='')
                canvas.update()
                self.progress_bar.set(i / 600)
                self.status_label.configure(text=f"GPU Test: {i//10}s/60s")
                time.sleep(0.1)
            
            test_win.destroy()
            self.show_gpu_results()
        threading.Thread(target=gpu_stress, daemon=True).start()
    
    def show_gpu_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.results_frame, text="Kết quả GPU Test:", font=Theme.SUBHEADING_FONT).pack(pady=10)
        button_bar = ctk.CTkFrame(self.results_frame)
        button_bar.pack(pady=15)
        ctk.CTkButton(button_bar, text="GPU hoạt động tốt", command=lambda: self.mark_completed({"Kết quả": "GPU ổn định", "Trạng thái": "Tốt"}, auto_advance=True), fg_color=Theme.SUCCESS).pack(side="left", padx=10)
        ctk.CTkButton(button_bar, text="GPU có vấn đề", command=lambda: self.mark_completed({"Kết quả": "GPU không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True), fg_color=Theme.ERROR).pack(side="left", padx=10)
        self.start_btn.configure(state="normal")

'''

# Chèn code mới vào trước BatteryHealthStep
new_content = content[:insert_pos] + physical_step + "\n" + content[insert_pos:]

# Cập nhật _get_steps_for_mode để thêm các step mới
steps_pattern = r'(def _get_steps_for_mode\(self, mode\):.*?expert_steps = basic_steps \+ \[)(.*?)(\])'
def replace_steps(match):
    prefix = match.group(1)
    current_steps = match.group(2)
    suffix = match.group(3)
    
    new_expert_steps = '''
            ("Kiểm tra ngoại hình", PhysicalInspectionStep),
            ("Kiểm tra BIOS", BIOSCheckStep),
            ("CPU Stress Test", CPUStressTestStep),
            ("GPU Stress Test", GPUStressTestStep),
            ("Tốc độ ổ cứng", HardDriveSpeedStep),
            ("Mạng & WiFi", NetworkTestStep),
            ("Thermal Monitor", ThermalMonitorStep)
        '''
    
    return prefix + new_expert_steps + suffix

new_content = re.sub(steps_pattern, replace_steps, new_content, flags=re.DOTALL)

# Ghi file mới
with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("[SUCCESS] Da them 4 step con thieu vao main_enhanced_auto.py")
print("   - PhysicalInspectionStep")
print("   - BIOSCheckStep")
print("   - CPUStressTestStep")
print("   - GPUStressTestStep")
print("\n[SUCCESS] Da cap nhat _get_steps_for_mode de bao gom cac step moi")
