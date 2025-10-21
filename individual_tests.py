"""
Individual Component Tests - Test từng thành phần riêng lẻ
Cho phép test nhanh từng phần cứng mà không cần chạy toàn bộ wizard
"""
import customtkinter as ctk
import multiprocessing
from tkinter import messagebox

# Import các bước test
try:
    from main_enhanced_auto import (
        Theme, IconManager, 
        HardwareFingerprintStep, LicenseCheckStep, SystemInfoStep,
        HardDriveHealthStep, ScreenTestStep, KeyboardTestStep,
        BatteryHealthStep, AudioTestStep, WebcamTestStep,
        NetworkTestStep, CPUStressTestStep, GPUStressTestStep
    )
    from disk_benchmark_step import HardDriveSpeedStep
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports
    Theme = None

class IndividualTestsApp(ctk.CTk):
    """Ứng dụng test từng thành phần riêng lẻ"""
    
    def __init__(self):
        super().__init__()
        
        self.title("LaptopTester - Individual Tests")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        
        self.icon_manager = IconManager() if IconManager else None
        self.all_results = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Header
        header = ctk.CTkFrame(self, fg_color="#161b22", height=80)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="🔧 Individual Component Tests",
            font=("Segoe UI", 28, "bold"),
            text_color="#58a6ff"
        ).pack(pady=20)
        
        # Main content
        content = ctk.CTkFrame(self, fg_color="#0d1117")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Test categories
        self.create_test_grid(content)
    
    def create_test_grid(self, parent):
        """Tạo lưới các nút test"""
        # Grid layout
        parent.grid_columnconfigure((0, 1, 2), weight=1)
        
        tests = [
            # Row 0 - Hardware Info
            ("💻 Hardware Fingerprint", HardwareFingerprintStep, 0, 0, "#58a6ff"),
            ("🔑 Windows License", LicenseCheckStep, 0, 1, "#238636"),
            ("⚙️ System Info", SystemInfoStep, 0, 2, "#d29922"),
            
            # Row 1 - Storage
            ("💿 HDD Health", HardDriveHealthStep, 1, 0, "#8b5cf6"),
            ("⚡ HDD Speed", HardDriveSpeedStep, 1, 1, "#f85149"),
            ("🖥️ Screen Test", ScreenTestStep, 1, 2, "#06b6d4"),
            
            # Row 2 - Input/Output
            ("⌨️ Keyboard & Mouse", KeyboardTestStep, 2, 0, "#10b981"),
            ("🔋 Battery Health", BatteryHealthStep, 2, 1, "#f59e0b"),
            ("🔊 Audio Test", AudioTestStep, 2, 2, "#ec4899"),
            
            # Row 3 - Connectivity
            ("📷 Webcam Test", WebcamTestStep, 3, 0, "#3b82f6"),
            ("🌐 Network Test", NetworkTestStep, 3, 1, "#14b8a6"),
            ("", None, 3, 2, ""),  # Empty slot
            
            # Row 4 - Stress Tests
            ("🔥 CPU Stress", CPUStressTestStep, 4, 0, "#ef4444"),
            ("🎮 GPU Stress", GPUStressTestStep, 4, 1, "#a855f7"),
            ("", None, 4, 2, ""),  # Empty slot
        ]
        
        for test_name, test_class, row, col, color in tests:
            if test_class:
                self.create_test_button(parent, test_name, test_class, row, col, color)
    
    def create_test_button(self, parent, name, test_class, row, col, color):
        """Tạo nút test"""
        btn = ctk.CTkButton(
            parent,
            text=name,
            command=lambda: self.run_test(name, test_class),
            fg_color=color,
            hover_color=self.darken_color(color),
            height=80,
            font=("Segoe UI", 18, "bold"),
            corner_radius=12
        )
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
    
    def darken_color(self, hex_color):
        """Làm tối màu cho hover effect"""
        if not hex_color or hex_color == "":
            return "#21262d"
        
        # Remove # and convert to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Darken by 20%
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def run_test(self, test_name, test_class):
        """Chạy test riêng lẻ"""
        # Create test window
        test_window = ctk.CTkToplevel(self)
        test_window.title(f"LaptopTester - {test_name}")
        test_window.geometry("1400x900")
        
        # Make it modal
        test_window.transient(self)
        test_window.grab_set()
        
        # Header
        header = ctk.CTkFrame(test_window, fg_color="#161b22", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text=test_name,
            font=("Segoe UI", 24, "bold"),
            text_color="#58a6ff"
        ).pack(side="left", padx=20, pady=15)
        
        ctk.CTkButton(
            header,
            text="✕ Đóng",
            command=test_window.destroy,
            fg_color="#f85149",
            hover_color="#cf222e",
            width=100,
            height=40,
            font=("Segoe UI", 16, "bold")
        ).pack(side="right", padx=20, pady=10)
        
        # Test content
        content = ctk.CTkFrame(test_window, fg_color="#0d1117")
        content.pack(fill="both", expand=True)
        
        try:
            # Create test step
            test_step = test_class(
                content,
                record_result_callback=self.record_result,
                enable_next_callback=lambda: None,
                go_to_next_step_callback=lambda: None,
                icon_manager=self.icon_manager,
                all_results=self.all_results
            )
            test_step.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Call on_show if exists
            if hasattr(test_step, 'on_show'):
                test_step.on_show()
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể khởi tạo test:\n{str(e)}")
            test_window.destroy()
    
    def record_result(self, step_name, result_data):
        """Lưu kết quả test"""
        self.all_results[step_name] = result_data
        print(f"[Result] {step_name}: {result_data}")

def main():
    """Main entry point"""
    multiprocessing.freeze_support()
    
    try:
        app = IndividualTestsApp()
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
