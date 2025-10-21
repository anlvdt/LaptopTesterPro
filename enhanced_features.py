# Enhanced Features for LaptopTester
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import json
import os
import subprocess
import psutil
import platform
from datetime import datetime
from ui_improvements import ModernTheme, ModernCard, ProgressIndicator, NotificationToast

class SystemMonitor:
    """Real-time system monitoring with charts"""
    
    def __init__(self, parent):
        self.parent = parent
        self.is_monitoring = False
        self.data_points = {
            'cpu': [],
            'memory': [],
            'temperature': [],
            'timestamps': []
        }
        self.max_points = 60  # 1 minute of data
        
    def create_monitor_ui(self):
        """Create monitoring interface"""
        monitor_frame = ModernCard(
            self.parent,
            title="📊 System Monitor",
            description="Giám sát hệ thống real-time"
        )
        monitor_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Control buttons
        control_frame = ctk.CTkFrame(monitor_frame.content, fg_color="transparent")
        control_frame.pack(fill="x", pady=ModernTheme.SPACE_MD)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶️ Bắt đầu Monitor",
            command=self.start_monitoring,
            fg_color=ModernTheme.SUCCESS,
            height=ModernTheme.BUTTON_HEIGHT
        )
        self.start_btn.pack(side="left", padx=(0, ModernTheme.SPACE_SM))
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ Dừng Monitor", 
            command=self.stop_monitoring,
            fg_color=ModernTheme.ERROR,
            height=ModernTheme.BUTTON_HEIGHT,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=ModernTheme.SPACE_SM)
        
        # Stats display
        stats_frame = ctk.CTkFrame(monitor_frame.content, fg_color=ModernTheme.BACKGROUND)
        stats_frame.pack(fill="x", pady=ModernTheme.SPACE_MD)
        stats_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # CPU usage
        self.cpu_label = ctk.CTkLabel(
            stats_frame,
            text="CPU: 0%",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.PRIMARY
        )
        self.cpu_label.grid(row=0, column=0, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
        
        # Memory usage
        self.memory_label = ctk.CTkLabel(
            stats_frame,
            text="RAM: 0%",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.WARNING
        )
        self.memory_label.grid(row=0, column=1, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
        
        # Temperature
        self.temp_label = ctk.CTkLabel(
            stats_frame,
            text="Temp: --°C",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.ERROR
        )
        self.temp_label.grid(row=0, column=2, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
        
        # Chart area
        self.chart_frame = ctk.CTkFrame(monitor_frame.content, fg_color=ModernTheme.SURFACE, height=200)
        self.chart_frame.pack(fill="x", pady=ModernTheme.SPACE_MD)
        
        # Create canvas for simple charts
        self.chart_canvas = tk.Canvas(
            self.chart_frame,
            bg="white",
            height=180,
            highlightthickness=0
        )
        self.chart_canvas.pack(fill="both", expand=True, padx=ModernTheme.SPACE_SM, pady=ModernTheme.SPACE_SM)
        
        return monitor_frame
    
    def start_monitoring(self):
        """Start system monitoring"""
        self.is_monitoring = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    # Get system stats
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory_percent = psutil.virtual_memory().percent
                    
                    # Mock temperature (real implementation would use sensors)
                    temp = 45 + (cpu_percent * 0.5)  # Simulate temperature based on CPU
                    
                    # Update data
                    current_time = datetime.now()
                    self.data_points['cpu'].append(cpu_percent)
                    self.data_points['memory'].append(memory_percent)
                    self.data_points['temperature'].append(temp)
                    self.data_points['timestamps'].append(current_time)
                    
                    # Keep only recent data
                    if len(self.data_points['cpu']) > self.max_points:
                        for key in self.data_points:
                            self.data_points[key] = self.data_points[key][-self.max_points:]
                    
                    # Update UI
                    self.parent.after(0, self.update_display, cpu_percent, memory_percent, temp)
                    
                except Exception as e:
                    print(f"Monitor error: {e}")
                    break
        
        threading.Thread(target=monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.is_monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def update_display(self, cpu, memory, temp):
        """Update display with current values"""
        # Update labels
        self.cpu_label.configure(text=f"CPU: {cpu:.1f}%")
        self.memory_label.configure(text=f"RAM: {memory:.1f}%")
        self.temp_label.configure(text=f"Temp: {temp:.1f}°C")
        
        # Update chart
        self.draw_chart()
    
    def draw_chart(self):
        """Draw simple line chart"""
        if not self.data_points['cpu']:
            return
        
        self.chart_canvas.delete("all")
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Draw grid
        for i in range(0, 101, 25):
            y = height - (i * height / 100)
            self.chart_canvas.create_line(0, y, width, y, fill="#E0E0E0", width=1)
            self.chart_canvas.create_text(5, y, text=f"{i}%", anchor="w", font=("Arial", 8))
        
        # Draw CPU line
        if len(self.data_points['cpu']) > 1:
            points = []
            for i, value in enumerate(self.data_points['cpu']):
                x = (i / max(1, len(self.data_points['cpu']) - 1)) * width
                y = height - (value * height / 100)
                points.extend([x, y])
            
            if len(points) >= 4:
                self.chart_canvas.create_line(points, fill=ModernTheme.PRIMARY, width=2, smooth=True)
        
        # Draw Memory line
        if len(self.data_points['memory']) > 1:
            points = []
            for i, value in enumerate(self.data_points['memory']):
                x = (i / max(1, len(self.data_points['memory']) - 1)) * width
                y = height - (value * height / 100)
                points.extend([x, y])
            
            if len(points) >= 4:
                self.chart_canvas.create_line(points, fill=ModernTheme.WARNING, width=2, smooth=True)

class BenchmarkSuite:
    """Comprehensive benchmark suite"""
    
    def __init__(self, parent):
        self.parent = parent
        self.results = {}
        
    def create_benchmark_ui(self):
        """Create benchmark interface"""
        benchmark_frame = ModernCard(
            self.parent,
            title="🏃‍♂️ Benchmark Suite",
            description="Bộ test hiệu năng toàn diện"
        )
        benchmark_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Benchmark options
        benchmarks = [
            ("CPU Performance", "Test hiệu năng CPU", self.run_cpu_benchmark),
            ("Memory Speed", "Test tốc độ RAM", self.run_memory_benchmark),
            ("Disk I/O", "Test tốc độ ổ cứng", self.run_disk_benchmark),
            ("Graphics", "Test hiệu năng đồ họa", self.run_graphics_benchmark),
            ("Network", "Test tốc độ mạng", self.run_network_benchmark)
        ]
        
        for name, description, callback in benchmarks:
            bench_frame = ctk.CTkFrame(benchmark_frame.content, fg_color=ModernTheme.BACKGROUND)
            bench_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
            
            # Info
            info_frame = ctk.CTkFrame(bench_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
            
            ctk.CTkLabel(
                info_frame,
                text=name,
                font=ModernTheme.FONT_SUBHEADING,
                text_color=ModernTheme.TEXT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=description,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w")
            
            # Run button
            ctk.CTkButton(
                bench_frame,
                text="▶️ Chạy Test",
                command=callback,
                fg_color=ModernTheme.PRIMARY,
                width=120,
                height=ModernTheme.BUTTON_HEIGHT
            ).pack(side="right", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
        
        # Results area
        self.results_frame = ctk.CTkScrollableFrame(
            benchmark_frame.content,
            fg_color=ModernTheme.BACKGROUND,
            height=200
        )
        self.results_frame.pack(fill="both", expand=True, pady=ModernTheme.SPACE_MD)
        
        return benchmark_frame
    
    def run_cpu_benchmark(self):
        """Run CPU benchmark"""
        self.show_benchmark_progress("CPU Performance", "Đang test hiệu năng CPU...")
        
        def cpu_test():
            import math
            start_time = time.time()
            
            # CPU intensive calculation
            result = 0
            for i in range(1000000):
                result += math.sqrt(i) * math.sin(i)
            
            end_time = time.time()
            duration = end_time - start_time
            score = int(1000000 / duration)  # Operations per second
            
            self.parent.after(0, self.show_benchmark_result, "CPU Performance", f"{score:,} ops/sec", duration)
        
        threading.Thread(target=cpu_test, daemon=True).start()
    
    def run_memory_benchmark(self):
        """Run memory benchmark"""
        self.show_benchmark_progress("Memory Speed", "Đang test tốc độ RAM...")
        
        def memory_test():
            import array
            start_time = time.time()
            
            # Memory allocation and access test
            data = array.array('i', range(1000000))
            total = sum(data)
            
            end_time = time.time()
            duration = end_time - start_time
            speed = int(len(data) * 4 / duration / 1024 / 1024)  # MB/s
            
            self.parent.after(0, self.show_benchmark_result, "Memory Speed", f"{speed:,} MB/s", duration)
        
        threading.Thread(target=memory_test, daemon=True).start()
    
    def run_disk_benchmark(self):
        """Run disk I/O benchmark"""
        self.show_benchmark_progress("Disk I/O", "Đang test tốc độ ổ cứng...")
        
        def disk_test():
            import tempfile
            import os
            
            # Write test
            test_data = b'0' * (10 * 1024 * 1024)  # 10MB
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                # Write speed
                start_time = time.time()
                with open(temp_path, 'wb') as f:
                    f.write(test_data)
                    f.flush()
                    os.fsync(f.fileno())
                write_time = time.time() - start_time
                write_speed = len(test_data) / write_time / 1024 / 1024
                
                # Read speed
                start_time = time.time()
                with open(temp_path, 'rb') as f:
                    _ = f.read()
                read_time = time.time() - start_time
                read_speed = len(test_data) / read_time / 1024 / 1024
                
                result = f"Write: {write_speed:.1f} MB/s, Read: {read_speed:.1f} MB/s"
                
            finally:
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            self.parent.after(0, self.show_benchmark_result, "Disk I/O", result, write_time + read_time)
        
        threading.Thread(target=disk_test, daemon=True).start()
    
    def run_graphics_benchmark(self):
        """Run graphics benchmark"""
        self.show_benchmark_progress("Graphics", "Đang test hiệu năng đồ họa...")
        
        def graphics_test():
            # Simple graphics test using tkinter
            test_window = tk.Toplevel()
            test_window.geometry("400x300")
            test_window.title("Graphics Benchmark")
            
            canvas = tk.Canvas(test_window, bg="black")
            canvas.pack(fill="both", expand=True)
            
            start_time = time.time()
            frames = 0
            
            def draw_frame():
                nonlocal frames
                canvas.delete("all")
                
                # Draw moving objects
                for i in range(50):
                    x = (frames * 2 + i * 10) % 400
                    y = (frames + i * 5) % 300
                    canvas.create_oval(x, y, x+10, y+10, fill=f"#{i*5:02x}{(frames*3)%255:02x}{(i*7)%255:02x}")
                
                frames += 1
                
                if frames < 300:  # Run for 300 frames
                    test_window.after(1, draw_frame)
                else:
                    end_time = time.time()
                    duration = end_time - start_time
                    fps = frames / duration
                    test_window.destroy()
                    self.parent.after(0, self.show_benchmark_result, "Graphics", f"{fps:.1f} FPS", duration)
            
            draw_frame()
        
        threading.Thread(target=graphics_test, daemon=True).start()
    
    def run_network_benchmark(self):
        """Run network benchmark"""
        self.show_benchmark_progress("Network", "Đang test tốc độ mạng...")
        
        def network_test():
            try:
                import urllib.request
                import time
                
                # Test download speed with a small file
                test_url = "http://httpbin.org/bytes/1048576"  # 1MB
                
                start_time = time.time()
                with urllib.request.urlopen(test_url, timeout=10) as response:
                    data = response.read()
                end_time = time.time()
                
                duration = end_time - start_time
                speed = len(data) / duration / 1024 / 1024  # MB/s
                
                result = f"{speed:.2f} MB/s"
                
            except Exception as e:
                result = f"Lỗi: {str(e)}"
                duration = 0
            
            self.parent.after(0, self.show_benchmark_result, "Network", result, duration)
        
        threading.Thread(target=network_test, daemon=True).start()
    
    def show_benchmark_progress(self, test_name, message):
        """Show benchmark progress"""
        progress_frame = ctk.CTkFrame(self.results_frame, fg_color=ModernTheme.SURFACE)
        progress_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
        
        ctk.CTkLabel(
            progress_frame,
            text=f"🔄 {test_name}: {message}",
            font=ModernTheme.FONT_BODY,
            text_color=ModernTheme.PRIMARY
        ).pack(padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
    
    def show_benchmark_result(self, test_name, result, duration):
        """Show benchmark result"""
        # Clear progress
        for widget in self.results_frame.winfo_children():
            if "🔄" in widget.winfo_children()[0].cget("text"):
                widget.destroy()
        
        # Add result
        result_frame = ctk.CTkFrame(self.results_frame, fg_color=ModernTheme.SUCCESS)
        result_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
        
        ctk.CTkLabel(
            result_frame,
            text=f"✅ {test_name}: {result} ({duration:.2f}s)",
            font=ModernTheme.FONT_BODY,
            text_color="white"
        ).pack(padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
        
        self.results[test_name] = {"result": result, "duration": duration}

class AdvancedDiagnostics:
    """Advanced system diagnostics"""
    
    def __init__(self, parent):
        self.parent = parent
        
    def create_diagnostics_ui(self):
        """Create diagnostics interface"""
        diag_frame = ModernCard(
            self.parent,
            title="🔍 Advanced Diagnostics",
            description="Chẩn đoán hệ thống nâng cao"
        )
        diag_frame.pack(fill="both", expand=True, padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Diagnostic categories
        categories = [
            ("System Health", "Kiểm tra sức khỏe hệ thống", self.check_system_health),
            ("Hardware Info", "Thông tin phần cứng chi tiết", self.get_hardware_info),
            ("Driver Status", "Trạng thái driver", self.check_drivers),
            ("Security Scan", "Quét bảo mật cơ bản", self.security_scan),
            ("Performance Analysis", "Phân tích hiệu năng", self.analyze_performance)
        ]
        
        for name, description, callback in categories:
            cat_frame = ctk.CTkFrame(diag_frame.content, fg_color=ModernTheme.BACKGROUND)
            cat_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
            
            # Info
            info_frame = ctk.CTkFrame(cat_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
            
            ctk.CTkLabel(
                info_frame,
                text=name,
                font=ModernTheme.FONT_SUBHEADING,
                text_color=ModernTheme.TEXT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=description,
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w")
            
            # Scan button
            ctk.CTkButton(
                cat_frame,
                text="🔍 Quét",
                command=callback,
                fg_color=ModernTheme.PRIMARY,
                width=100,
                height=ModernTheme.BUTTON_HEIGHT
            ).pack(side="right", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_MD)
        
        # Results area
        self.diag_results = ctk.CTkTextbox(
            diag_frame.content,
            font=ModernTheme.FONT_BODY,
            height=300,
            fg_color=ModernTheme.SURFACE
        )
        self.diag_results.pack(fill="both", expand=True, pady=ModernTheme.SPACE_MD)
        
        return diag_frame
    
    def check_system_health(self):
        """Check overall system health"""
        self.diag_results.delete("0.0", "end")
        self.diag_results.insert("0.0", "🔍 Đang kiểm tra sức khỏe hệ thống...\n\n")
        
        def health_check():
            results = []
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent < 80:
                results.append(f"✅ CPU: {cpu_percent:.1f}% - Bình thường")
            else:
                results.append(f"⚠️ CPU: {cpu_percent:.1f}% - Cao")
            
            # Memory usage
            memory = psutil.virtual_memory()
            if memory.percent < 80:
                results.append(f"✅ RAM: {memory.percent:.1f}% - Bình thường")
            else:
                results.append(f"⚠️ RAM: {memory.percent:.1f}% - Cao")
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent < 90:
                results.append(f"✅ Ổ cứng: {disk_percent:.1f}% - Bình thường")
            else:
                results.append(f"⚠️ Ổ cứng: {disk_percent:.1f}% - Gần đầy")
            
            # Running processes
            process_count = len(psutil.pids())
            results.append(f"📊 Tiến trình đang chạy: {process_count}")
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            results.append(f"⏰ Thời gian hoạt động: {str(uptime).split('.')[0]}")
            
            result_text = "\n".join(results)
            self.parent.after(0, lambda: self.update_diag_results("System Health", result_text))
        
        threading.Thread(target=health_check, daemon=True).start()
    
    def get_hardware_info(self):
        """Get detailed hardware information"""
        self.diag_results.delete("0.0", "end")
        self.diag_results.insert("0.0", "🔍 Đang thu thập thông tin phần cứng...\n\n")
        
        def hardware_info():
            results = []
            
            # CPU info
            results.append(f"🖥️ CPU: {platform.processor()}")
            results.append(f"   Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
            
            # Memory info
            memory = psutil.virtual_memory()
            results.append(f"💾 RAM: {memory.total // (1024**3)} GB total")
            results.append(f"   Available: {memory.available // (1024**3)} GB")
            
            # Disk info
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    results.append(f"💿 {partition.device}: {usage.total // (1024**3)} GB")
                except:
                    pass
            
            # Network interfaces
            interfaces = psutil.net_if_addrs()
            results.append(f"🌐 Network interfaces: {len(interfaces)}")
            
            result_text = "\n".join(results)
            self.parent.after(0, lambda: self.update_diag_results("Hardware Info", result_text))
        
        threading.Thread(target=hardware_info, daemon=True).start()
    
    def check_drivers(self):
        """Check driver status (Windows only)"""
        self.diag_results.delete("0.0", "end")
        
        if platform.system() != "Windows":
            self.update_diag_results("Driver Status", "❌ Chỉ hỗ trợ trên Windows")
            return
        
        self.diag_results.insert("0.0", "🔍 Đang kiểm tra driver...\n\n")
        
        def driver_check():
            try:
                # Use PowerShell to get driver info
                cmd = 'powershell "Get-WmiObject Win32_PnPEntity | Where-Object {$_.ConfigManagerErrorCode -ne 0} | Select-Object Name, ConfigManagerErrorCode"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    if result.stdout.strip():
                        results = f"⚠️ Drivers có vấn đề:\n{result.stdout}"
                    else:
                        results = "✅ Tất cả drivers hoạt động bình thường"
                else:
                    results = "❌ Không thể kiểm tra drivers"
                
            except Exception as e:
                results = f"❌ Lỗi kiểm tra drivers: {str(e)}"
            
            self.parent.after(0, lambda: self.update_diag_results("Driver Status", results))
        
        threading.Thread(target=driver_check, daemon=True).start()
    
    def security_scan(self):
        """Basic security scan"""
        self.diag_results.delete("0.0", "end")
        self.diag_results.insert("0.0", "🔍 Đang quét bảo mật cơ bản...\n\n")
        
        def security_check():
            results = []
            
            # Check for suspicious processes
            suspicious_names = ['bitcoin', 'miner', 'trojan', 'virus', 'malware']
            processes = [p.info for p in psutil.process_iter(['pid', 'name'])]
            
            suspicious_found = False
            for proc in processes:
                proc_name = proc['name'].lower()
                if any(sus in proc_name for sus in suspicious_names):
                    results.append(f"⚠️ Tiến trình đáng nghi: {proc['name']} (PID: {proc['pid']})")
                    suspicious_found = True
            
            if not suspicious_found:
                results.append("✅ Không phát hiện tiến trình đáng nghi")
            
            # Check network connections
            connections = psutil.net_connections()
            external_connections = [c for c in connections if c.status == 'ESTABLISHED' and c.raddr]
            results.append(f"🌐 Kết nối mạng đang hoạt động: {len(external_connections)}")
            
            # Check startup programs (Windows)
            if platform.system() == "Windows":
                try:
                    import winreg
                    startup_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                               "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
                    startup_count = winreg.QueryInfoKey(startup_key)[1]
                    results.append(f"🚀 Chương trình khởi động: {startup_count}")
                    winreg.CloseKey(startup_key)
                except:
                    results.append("❌ Không thể kiểm tra chương trình khởi động")
            
            result_text = "\n".join(results)
            self.parent.after(0, lambda: self.update_diag_results("Security Scan", result_text))
        
        threading.Thread(target=security_check, daemon=True).start()
    
    def analyze_performance(self):
        """Analyze system performance"""
        self.diag_results.delete("0.0", "end")
        self.diag_results.insert("0.0", "🔍 Đang phân tích hiệu năng...\n\n")
        
        def performance_analysis():
            results = []
            
            # CPU performance over time
            cpu_samples = []
            for _ in range(5):
                cpu_samples.append(psutil.cpu_percent(interval=1))
            
            avg_cpu = sum(cpu_samples) / len(cpu_samples)
            max_cpu = max(cpu_samples)
            
            results.append(f"🖥️ CPU Performance:")
            results.append(f"   Trung bình: {avg_cpu:.1f}%")
            results.append(f"   Cao nhất: {max_cpu:.1f}%")
            
            if avg_cpu < 50:
                results.append("   ✅ Hiệu năng tốt")
            elif avg_cpu < 80:
                results.append("   ⚠️ Hiệu năng trung bình")
            else:
                results.append("   ❌ Hiệu năng kém")
            
            # Memory analysis
            memory = psutil.virtual_memory()
            results.append(f"\n💾 Memory Analysis:")
            results.append(f"   Sử dụng: {memory.percent:.1f}%")
            results.append(f"   Available: {memory.available // (1024**2)} MB")
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                results.append(f"\n💿 Disk I/O:")
                results.append(f"   Read: {disk_io.read_bytes // (1024**2)} MB")
                results.append(f"   Write: {disk_io.write_bytes // (1024**2)} MB")
            
            result_text = "\n".join(results)
            self.parent.after(0, lambda: self.update_diag_results("Performance Analysis", result_text))
        
        threading.Thread(target=performance_analysis, daemon=True).start()
    
    def update_diag_results(self, category, results):
        """Update diagnostics results"""
        self.diag_results.delete("0.0", "end")
        self.diag_results.insert("0.0", f"📊 {category}\n{'='*50}\n\n{results}")

# Export classes
__all__ = ['SystemMonitor', 'BenchmarkSuite', 'AdvancedDiagnostics']