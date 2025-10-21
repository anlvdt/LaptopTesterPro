"""
Disk Benchmark Step - Hoàn chỉnh với worker integration
"""
import multiprocessing
import time
from collections import deque

def run_disk_benchmark(queue, duration, file_size_mb=512):
    """Import và chạy worker từ worker_disk.py"""
    try:
        from worker_disk import run_benchmark
        run_benchmark(queue, duration, file_size_mb)
    except ImportError:
        queue.put({'type': 'error', 'message': 'Không tìm thấy worker_disk.py'})
        queue.put({'type': 'done'})

class HardDriveSpeedStep:
    """
    Bước test tốc độ ổ cứng với:
    - Benchmark đọc/ghi tuần tự
    - Hiển thị real-time speed
    - Phân tích kết quả (SSD/HDD)
    """
    def __init__(self, master, **kwargs):
        # Khởi tạo như BaseStepFrame
        self.test_process = None
        self.queue = multiprocessing.Queue()
        self.is_testing = False
        
        # Data storage for charts
        self.write_speeds = deque(maxlen=100)
        self.read_speeds = deque(maxlen=100)
        
    def start_test(self):
        """Bắt đầu benchmark"""
        if self.is_testing:
            return
        
        self.is_testing = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Clear old data
        self.write_speeds.clear()
        self.read_speeds.clear()
        
        # Start worker process
        self.test_process = multiprocessing.Process(
            target=run_disk_benchmark,
            args=(self.queue, 60, 512),  # 60s duration, 512MB file
            daemon=True
        )
        self.test_process.start()
        self.after(100, self.check_queue)
    
    def check_queue(self):
        """Đọc kết quả từ worker"""
        if not self.is_testing:
            return
        
        try:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                msg_type = msg.get('type')
                
                if msg_type == 'status':
                    self.status_label.configure(text=msg.get('message', ''))
                
                elif msg_type == 'update':
                    progress = msg.get('progress', 0)
                    operation = msg.get('operation', '')
                    speed = msg.get('speed', 0)
                    avg_speed = msg.get('avg_speed', 0)
                    
                    self.progress_bar.set(progress)
                    self.status_label.configure(
                        text=f"{operation}: {speed:.1f} MB/s (Avg: {avg_speed:.1f} MB/s)"
                    )
                    
                    # Store speeds for chart
                    if operation == 'Write':
                        self.write_speeds.append(speed)
                    elif operation == 'Read':
                        self.read_speeds.append(speed)
                    
                    self.update_speed_chart()
                
                elif msg_type == 'result':
                    self.finalize_test(msg)
                
                elif msg_type == 'error':
                    self.status_label.configure(
                        text=f"Lỗi: {msg.get('message', 'Unknown')}",
                        text_color="#f85149"
                    )
                    self.stop_test()
                
                elif msg_type == 'done':
                    self.is_testing = False
                    self.start_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
        
        except Exception as e:
            print(f"Queue error: {e}")
        
        finally:
            if self.is_testing:
                self.after(200, self.check_queue)
    
    def update_speed_chart(self):
        """Vẽ biểu đồ tốc độ real-time"""
        try:
            self.chart_canvas.delete("all")
            width = self.chart_canvas.winfo_width()
            height = self.chart_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                return
            
            # Draw write speeds (top half)
            if self.write_speeds:
                self.draw_speed_line(
                    self.write_speeds, 0, height//2, width,
                    "Write Speed (MB/s)", "#58a6ff"
                )
            
            # Draw read speeds (bottom half)
            if self.read_speeds:
                self.draw_speed_line(
                    self.read_speeds, height//2, height//2, width,
                    "Read Speed (MB/s)", "#238636"
                )
        except:
            pass
    
    def draw_speed_line(self, data, y_offset, height, width, label, color):
        """Vẽ đường biểu đồ tốc độ"""
        if not data or len(data) < 2:
            return
        
        # Background
        self.chart_canvas.create_rectangle(
            0, y_offset, width, y_offset + height,
            fill="#21262d", outline="#30363d"
        )
        
        # Label
        self.chart_canvas.create_text(
            10, y_offset + 10, text=label,
            fill="#f0f6fc", anchor="nw", font=("Arial", 10)
        )
        
        # Data line
        max_speed = max(data) if data else 100
        points = []
        for i, speed in enumerate(data):
            x = (i / (len(data) - 1)) * (width - 20) + 10
            y = y_offset + height - 10 - ((speed / max_speed) * (height - 20))
            points.extend([x, y])
        
        if len(points) >= 4:
            self.chart_canvas.create_line(points, fill=color, width=2, smooth=True)
        
        # Current value
        current = data[-1] if data else 0
        self.chart_canvas.create_text(
            width - 10, y_offset + 10,
            text=f"{current:.1f} MB/s",
            fill=color, anchor="ne", font=("Arial", 12, "bold")
        )
    
    def finalize_test(self, msg):
        """Hiển thị kết quả cuối cùng"""
        result_data = msg.get('data', {})
        write_speed = float(result_data.get('write_speed', 0))
        read_speed = float(result_data.get('read_speed', 0))
        
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Results header
        import customtkinter as ctk
        ctk.CTkLabel(
            self.results_frame,
            text="📊 Kết Quả Benchmark Ổ Cứng",
            font=("Segoe UI", 22, "bold"),
            text_color="#58a6ff"
        ).pack(pady=10)
        
        # Speed metrics
        metrics_frame = ctk.CTkFrame(self.results_frame, fg_color="#161b22")
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            metrics_frame,
            text=f"✍️ Tốc độ Ghi: {write_speed:.2f} MB/s",
            font=("Segoe UI", 20)
        ).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkLabel(
            metrics_frame,
            text=f"📖 Tốc độ Đọc: {read_speed:.2f} MB/s",
            font=("Segoe UI", 20)
        ).pack(anchor="w", padx=15, pady=5)
        
        # Analyze disk type
        disk_type, disk_color, disk_icon = self.analyze_disk_type(write_speed, read_speed)
        
        analysis_frame = ctk.CTkFrame(self.results_frame, fg_color=disk_color)
        analysis_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            analysis_frame,
            text=f"{disk_icon} Phân Tích: {disk_type}",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(pady=10)
        
        # Recommendations
        recommendations = self.get_recommendations(write_speed, read_speed, disk_type)
        for rec in recommendations:
            ctk.CTkLabel(
                analysis_frame,
                text=rec,
                font=("Segoe UI", 18),
                text_color="white"
            ).pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkLabel(analysis_frame, text="", font=("Segoe UI", 14)).pack(pady=5)
        
        # Decision buttons
        button_bar = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        ctk.CTkButton(
            button_bar,
            text="✓ Tốc Độ Tốt",
            command=lambda: self.mark_completed({
                "Kết quả": f"Write: {write_speed:.2f}MB/s, Read: {read_speed:.2f}MB/s ({disk_type})",
                "Trạng thái": "Tốt"
            }, auto_advance=True),
            fg_color="#238636",
            height=32,
            font=("Segoe UI", 19, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_bar,
            text="✗ Tốc Độ Chậm",
            command=lambda: self.mark_completed({
                "Kết quả": f"Write: {write_speed:.2f}MB/s, Read: {read_speed:.2f}MB/s (Chậm)",
                "Trạng thái": "Lỗi"
            }, auto_advance=True),
            fg_color="#f85149",
            height=32,
            font=("Segoe UI", 19, "bold")
        ).pack(side="left", padx=10)
    
    def analyze_disk_type(self, write_speed, read_speed):
        """Phân tích loại ổ cứng dựa trên tốc độ"""
        avg_speed = (write_speed + read_speed) / 2
        
        if avg_speed > 400:
            return "NVMe SSD (PCIe Gen3/4)", "#238636", "🚀"
        elif avg_speed > 200:
            return "SATA SSD", "#238636", "⚡"
        elif avg_speed > 100:
            return "HDD 7200 RPM", "#d29922", "💿"
        else:
            return "HDD 5400 RPM (Chậm)", "#f85149", "🐌"
    
    def get_recommendations(self, write_speed, read_speed, disk_type):
        """Đưa ra khuyến nghị dựa trên kết quả"""
        avg_speed = (write_speed + read_speed) / 2
        
        if avg_speed > 400:
            return [
                "• Tốc độ xuất sắc cho gaming và workstation",
                "• Phù hợp cho video editing 4K, 3D rendering",
                "• Boot Windows trong 5-10 giây"
            ]
        elif avg_speed > 200:
            return [
                "• Tốc độ tốt cho đa số công việc",
                "• Phù hợp cho văn phòng, lập trình, gaming",
                "• Boot Windows trong 10-20 giây"
            ]
        elif avg_speed > 100:
            return [
                "• Tốc độ trung bình, phù hợp văn phòng",
                "• Nên nâng cấp lên SSD để cải thiện",
                "• Boot Windows trong 30-60 giây"
            ]
        else:
            return [
                "• Tốc độ chậm, ảnh hưởng trải nghiệm",
                "• Khuyến nghị nâng cấp SSD ngay",
                "• Boot Windows > 60 giây"
            ]
    
    def stop_test(self):
        """Dừng test"""
        if self.test_process and self.test_process.is_alive():
            self.test_process.terminate()
            self.test_process.join(timeout=2)
        
        self.is_testing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Test đã dừng")
