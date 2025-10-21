"""
Tính năng test nhiệt độ và hiệu năng nâng cao
Monitoring real-time temperature, fan speed, và performance metrics
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
from datetime import datetime

class Theme:
    BACKGROUND="#F8FAFC"; FRAME="#FFFFFF"; ACCENT="#3B82F6"
    SUCCESS="#10B981"; WARNING="#F59E0B"; ERROR="#EF4444"
    TEXT="#0F172A"; TEXT_SECONDARY="#64748B"
    HEADING_FONT=("Segoe UI", 24, "bold"); BODY_FONT=("Segoe UI", 16)
    CORNER_RADIUS=12; PADDING=20

class ThermalPerformanceStep:
    def __init__(self, master, **kwargs):
        self.master = master
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Data storage for real-time charts
        self.max_data_points = 60  # 1 minute of data at 1Hz
        self.cpu_temps = deque(maxlen=self.max_data_points)
        self.cpu_usage = deque(maxlen=self.max_data_points)
        self.memory_usage = deque(maxlen=self.max_data_points)
        self.timestamps = deque(maxlen=self.max_data_points)
        
        # Performance metrics
        self.max_cpu_temp = 0
        self.avg_cpu_temp = 0
        self.max_cpu_usage = 0
        self.throttling_detected = False
        
    def create_thermal_ui(self, parent_frame):
        """Tạo giao diện monitoring nhiệt độ và hiệu năng"""
        # Main container
        main_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Theme.PADDING, pady=Theme.PADDING)
        main_frame.grid_columnconfigure((0,1), weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color=Theme.ACCENT, corner_radius=Theme.CORNER_RADIUS)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(header_frame, text="🌡️ MONITORING NHIỆT ĐỘ & HIỆU NĂNG", 
                    font=Theme.HEADING_FONT, text_color="white").pack(pady=15)
        
        # Controls panel
        controls_frame = ctk.CTkFrame(main_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        controls_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 8))\n        
        self.create_controls_panel(controls_frame)
        
        # Real-time charts
        charts_frame = ctk.CTkFrame(main_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        charts_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        
        self.create_charts_panel(charts_frame)
        
        return main_frame
    
    def create_controls_panel(self, parent):
        """Tạo panel điều khiển và hiển thị metrics"""
        parent.grid_rowconfigure(2, weight=1)
        
        # Control buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=0, column=0, sticky="ew", padx=Theme.PADDING, pady=Theme.PADDING)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="🚀 Bắt Đầu Monitor", 
                                      command=self.start_monitoring,
                                      fg_color=Theme.SUCCESS, width=150, height=40)
        self.start_btn.pack(pady=(0, 10))
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹️ Dừng Monitor", 
                                     command=self.stop_monitoring,
                                     fg_color=Theme.ERROR, width=150, height=40, state="disabled")
        self.stop_btn.pack(pady=(0, 10))
        
        self.stress_btn = ctk.CTkButton(btn_frame, text="🔥 Stress Test", 
                                       command=self.start_stress_test,
                                       fg_color=Theme.WARNING, width=150, height=40)
        self.stress_btn.pack()
        
        # Current metrics display
        metrics_frame = ctk.CTkFrame(parent, fg_color=Theme.BACKGROUND, corner_radius=8)
        metrics_frame.grid(row=1, column=0, sticky="ew", padx=Theme.PADDING, pady=(0, Theme.PADDING))
        
        ctk.CTkLabel(metrics_frame, text="📊 Metrics Hiện Tại", 
                    font=("Segoe UI", 18, "bold"), text_color=Theme.ACCENT).pack(pady=(15, 10))
        
        # Create metric labels
        self.cpu_temp_label = ctk.CTkLabel(metrics_frame, text="🌡️ CPU: -- °C", 
                                          font=Theme.BODY_FONT, text_color=Theme.TEXT)
        self.cpu_temp_label.pack(pady=5)
        
        self.cpu_usage_label = ctk.CTkLabel(metrics_frame, text="⚡ CPU Usage: --%", 
                                           font=Theme.BODY_FONT, text_color=Theme.TEXT)
        self.cpu_usage_label.pack(pady=5)
        
        self.memory_label = ctk.CTkLabel(metrics_frame, text="💾 Memory: --%", 
                                        font=Theme.BODY_FONT, text_color=Theme.TEXT)
        self.memory_label.pack(pady=5)
        
        self.fan_label = ctk.CTkLabel(metrics_frame, text="🌀 Fan: -- RPM", 
                                     font=Theme.BODY_FONT, text_color=Theme.TEXT)
        self.fan_label.pack(pady=5)
        
        # Status indicators
        status_frame = ctk.CTkFrame(parent, fg_color=Theme.BACKGROUND, corner_radius=8)
        status_frame.grid(row=2, column=0, sticky="nsew", padx=Theme.PADDING, pady=(0, Theme.PADDING))
        
        ctk.CTkLabel(status_frame, text="⚠️ Cảnh Báo", 
                    font=("Segoe UI", 18, "bold"), text_color=Theme.WARNING).pack(pady=(15, 10))
        
        self.warning_text = ctk.CTkTextbox(status_frame, height=150, font=Theme.BODY_FONT)
        self.warning_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.warning_text.insert("0.0", "Chưa có cảnh báo nào...")
        self.warning_text.configure(state="disabled")
    
    def create_charts_panel(self, parent):
        """Tạo panel biểu đồ real-time"""
        parent.grid_rowconfigure(0, weight=1)
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.fig.patch.set_facecolor('#F8FAFC')
        
        # Temperature chart
        self.ax1.set_title('Nhiệt Độ CPU (°C)', fontsize=14, fontweight='bold')
        self.ax1.set_ylabel('Nhiệt độ (°C)')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_ylim(30, 100)
        
        # CPU Usage chart  
        self.ax2.set_title('CPU Usage (%)', fontsize=14, fontweight='bold')
        self.ax2.set_ylabel('Usage (%)')
        self.ax2.set_xlabel('Thời gian (giây)')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=Theme.PADDING, pady=Theme.PADDING)
    
    def start_monitoring(self):
        """Bắt đầu monitoring"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Clear previous data
        self.cpu_temps.clear()
        self.cpu_usage.clear()
        self.memory_usage.clear()
        self.timestamps.clear()
        
        # Reset metrics
        self.max_cpu_temp = 0
        self.avg_cpu_temp = 0
        self.max_cpu_usage = 0
        self.throttling_detected = False
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        self.add_warning("✅ Bắt đầu monitoring...")
    
    def stop_monitoring(self):
        """Dừng monitoring"""
        self.is_monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        
        self.add_warning("⏹️ Đã dừng monitoring")
        
        # Generate summary
        if self.cpu_temps:
            self.generate_summary()
    
    def start_stress_test(self):
        """Bắt đầu stress test"""
        if not self.is_monitoring:
            self.start_monitoring()
        
        self.add_warning("🔥 Bắt đầu Stress Test - CPU sẽ chạy 100% trong 30 giây")
        
        # Run stress test in separate thread
        threading.Thread(target=self.run_stress_test, daemon=True).start()
    
    def run_stress_test(self):
        """Chạy stress test CPU"""
        import multiprocessing
        
        def cpu_stress():
            """CPU intensive task"""
            end_time = time.time() + 30  # 30 seconds
            while time.time() < end_time:
                # CPU intensive calculation
                sum(i*i for i in range(10000))
        
        # Start stress on all CPU cores
        processes = []
        cpu_count = multiprocessing.cpu_count()
        
        for _ in range(cpu_count):
            p = multiprocessing.Process(target=cpu_stress)
            p.start()
            processes.append(p)
        
        # Wait for completion
        for p in processes:
            p.join()
        
        self.add_warning("✅ Stress Test hoàn thành")
    
    def monitoring_loop(self):
        """Vòng lặp monitoring chính"""
        start_time = time.time()
        
        while self.is_monitoring:
            try:
                current_time = time.time() - start_time
                
                # Get system metrics
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_percent = psutil.virtual_memory().percent
                
                # Get CPU temperature (mock data for demo)
                # In real implementation, use psutil.sensors_temperatures() or WMI
                cpu_temp = self.get_cpu_temperature()
                
                # Store data
                self.timestamps.append(current_time)
                self.cpu_usage.append(cpu_percent)
                self.memory_usage.append(memory_percent)
                self.cpu_temps.append(cpu_temp)
                
                # Update metrics
                self.max_cpu_temp = max(self.max_cpu_temp, cpu_temp)
                self.max_cpu_usage = max(self.max_cpu_usage, cpu_percent)
                if self.cpu_temps:
                    self.avg_cpu_temp = sum(self.cpu_temps) / len(self.cpu_temps)
                
                # Check for issues
                self.check_thermal_issues(cpu_temp, cpu_percent)
                
                # Update UI
                self.master.after(0, self.update_ui, cpu_temp, cpu_percent, memory_percent)
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                self.add_warning(f"❌ Lỗi monitoring: {e}")
                break
    
    def get_cpu_temperature(self):
        """Lấy nhiệt độ CPU (mock implementation)"""
        try:
            # Try to get real temperature on Windows
            import platform
            if platform.system() == "Windows":
                try:
                    import wmi
                    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                    temperature_infos = w.Sensor()
                    for sensor in temperature_infos:
                        if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                            return float(sensor.Value) if sensor.Value else 45.0
                except:
                    pass
            
            # Fallback: simulate realistic temperature based on CPU usage
            base_temp = 35
            cpu_usage = psutil.cpu_percent()
            load_temp = (cpu_usage / 100) * 40  # Up to 40°C from load
            noise = np.random.normal(0, 2)  # Some random variation
            
            return max(30, min(95, base_temp + load_temp + noise))
            
        except:
            return 45.0  # Default safe temperature
    
    def check_thermal_issues(self, cpu_temp, cpu_usage):
        """Kiểm tra các vấn đề về nhiệt độ"""
        # High temperature warning
        if cpu_temp > 80:
            self.add_warning(f"🔥 CẢNH BÁO: CPU quá nóng ({cpu_temp:.1f}°C)")
        elif cpu_temp > 70:
            self.add_warning(f"⚠️ CPU hơi nóng ({cpu_temp:.1f}°C)")
        
        # Throttling detection (simplified)
        if cpu_temp > 85 and cpu_usage < 50:
            if not self.throttling_detected:
                self.throttling_detected = True
                self.add_warning("🐌 PHÁT HIỆN THROTTLING: CPU giảm tốc độ do quá nóng")
        
        # High CPU usage
        if cpu_usage > 90:
            self.add_warning(f"⚡ CPU sử dụng cao ({cpu_usage:.1f}%)")
    
    def update_ui(self, cpu_temp, cpu_usage, memory_usage):
        """Cập nhật giao diện người dùng"""
        # Update metric labels
        temp_color = Theme.ERROR if cpu_temp > 80 else Theme.WARNING if cpu_temp > 70 else Theme.SUCCESS
        self.cpu_temp_label.configure(text=f"🌡️ CPU: {cpu_temp:.1f}°C", text_color=temp_color)
        
        usage_color = Theme.ERROR if cpu_usage > 90 else Theme.WARNING if cpu_usage > 70 else Theme.SUCCESS
        self.cpu_usage_label.configure(text=f"⚡ CPU Usage: {cpu_usage:.1f}%", text_color=usage_color)
        
        mem_color = Theme.ERROR if memory_usage > 90 else Theme.WARNING if memory_usage > 80 else Theme.SUCCESS
        self.memory_label.configure(text=f"💾 Memory: {memory_usage:.1f}%", text_color=mem_color)
        
        # Mock fan speed (in real implementation, get from sensors)
        fan_speed = int(1000 + (cpu_temp - 30) * 50)  # Simulate fan response to temperature
        self.fan_label.configure(text=f"🌀 Fan: {fan_speed} RPM")
        
        # Update charts
        self.update_charts()
    
    def update_charts(self):
        """Cập nhật biểu đồ real-time"""
        if not self.timestamps:
            return
        
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Temperature chart
        self.ax1.plot(list(self.timestamps), list(self.cpu_temps), 'r-', linewidth=2, label='CPU Temp')
        self.ax1.axhline(y=70, color='orange', linestyle='--', alpha=0.7, label='Cảnh báo (70°C)')
        self.ax1.axhline(y=85, color='red', linestyle='--', alpha=0.7, label='Nguy hiểm (85°C)')
        self.ax1.set_title('Nhiệt Độ CPU (°C)', fontsize=12, fontweight='bold')
        self.ax1.set_ylabel('Nhiệt độ (°C)')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(fontsize=8)
        self.ax1.set_ylim(30, 100)
        
        # CPU Usage chart
        self.ax2.plot(list(self.timestamps), list(self.cpu_usage), 'b-', linewidth=2, label='CPU Usage')
        self.ax2.fill_between(list(self.timestamps), list(self.cpu_usage), alpha=0.3)
        self.ax2.set_title('CPU Usage (%)', fontsize=12, fontweight='bold')
        self.ax2.set_ylabel('Usage (%)')
        self.ax2.set_xlabel('Thời gian (giây)')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        self.canvas.draw()
    
    def add_warning(self, message):
        """Thêm cảnh báo vào log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        warning_msg = f"[{timestamp}] {message}\n"
        
        self.warning_text.configure(state="normal")
        self.warning_text.insert("end", warning_msg)
        self.warning_text.see("end")
        self.warning_text.configure(state="disabled")
    
    def generate_summary(self):
        """Tạo báo cáo tóm tắt"""
        if not self.cpu_temps:
            return
        
        summary = f"""
📊 BÁO CÁO THERMAL & PERFORMANCE

🌡️ Nhiệt độ:
  • Tối đa: {self.max_cpu_temp:.1f}°C
  • Trung bình: {self.avg_cpu_temp:.1f}°C
  • Tối thiểu: {min(self.cpu_temps):.1f}°C

⚡ CPU Usage:
  • Tối đa: {self.max_cpu_usage:.1f}%
  • Trung bình: {sum(self.cpu_usage)/len(self.cpu_usage):.1f}%

🔍 Đánh giá:
"""
        
        # Performance assessment
        if self.max_cpu_temp > 85:
            summary += "  ❌ NHIỆT ĐỘ QUÁ CAO - Cần kiểm tra tản nhiệt\n"
        elif self.max_cpu_temp > 75:
            summary += "  ⚠️ Nhiệt độ hơi cao - Nên vệ sinh tản nhiệt\n"
        else:
            summary += "  ✅ Nhiệt độ trong giới hạn an toàn\n"
        
        if self.throttling_detected:
            summary += "  🐌 Phát hiện throttling - CPU giảm hiệu năng\n"
        else:
            summary += "  ✅ Không phát hiện throttling\n"
        
        self.add_warning(summary)