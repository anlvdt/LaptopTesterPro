"""
Tính năng test mạng và WiFi mới cho LaptopTester
Kiểm tra kết nối mạng, tốc độ WiFi, và độ ổn định
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time
import subprocess
import socket
import requests
from datetime import datetime

class Theme:
    BACKGROUND="#F8FAFC"; FRAME="#FFFFFF"; ACCENT="#3B82F6"
    SUCCESS="#10B981"; WARNING="#F59E0B"; ERROR="#EF4444"
    TEXT="#0F172A"; TEXT_SECONDARY="#64748B"
    HEADING_FONT=("Segoe UI", 24, "bold"); BODY_FONT=("Segoe UI", 16)
    CORNER_RADIUS=12; PADDING=20

class NetworkTestStep:
    def __init__(self, master, **kwargs):
        self.master = master
        self.test_results = {}
        self.is_testing = False
        
    def create_network_test_ui(self, parent_frame):
        """Tạo giao diện test mạng"""
        # Main container
        main_frame = ctk.CTkFrame(parent_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        main_frame.pack(fill="both", expand=True, padx=Theme.PADDING, pady=Theme.PADDING)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color=Theme.ACCENT, corner_radius=8)
        header_frame.pack(fill="x", padx=Theme.PADDING, pady=(Theme.PADDING, 15))
        
        ctk.CTkLabel(header_frame, text="🌐 KIỂM TRA MẠNG & WIFI", 
                    font=Theme.HEADING_FONT, text_color="white").pack(pady=15)
        
        # Test controls
        controls_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=Theme.PADDING, pady=(0, 15))
        
        self.start_btn = ctk.CTkButton(controls_frame, text="🚀 Bắt Đầu Test Mạng", 
                                      command=self.start_network_test, 
                                      fg_color=Theme.SUCCESS, width=200, height=40)
        self.start_btn.pack(side="left", padx=(0, 10))
        
        self.stop_btn = ctk.CTkButton(controls_frame, text="⏹️ Dừng Test", 
                                     command=self.stop_network_test,
                                     fg_color=Theme.ERROR, width=120, height=40, state="disabled")
        self.stop_btn.pack(side="left")
        
        # Status display
        self.status_label = ctk.CTkLabel(main_frame, text="Sẵn sàng test mạng", 
                                        font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
        self.status_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame, progress_color=Theme.ACCENT)
        self.progress_bar.pack(fill="x", padx=Theme.PADDING, pady=(0, 15))
        self.progress_bar.set(0)
        
        # Results area
        self.results_frame = ctk.CTkScrollableFrame(main_frame, fg_color=Theme.BACKGROUND, 
                                                   corner_radius=8, height=300)
        self.results_frame.pack(fill="both", expand=True, padx=Theme.PADDING, pady=(0, Theme.PADDING))
        
        return main_frame
    
    def start_network_test(self):
        """Bắt đầu test mạng"""
        if self.is_testing:
            return
            
        self.is_testing = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Start test in background thread
        threading.Thread(target=self.run_network_tests, daemon=True).start()
    
    def stop_network_test(self):
        """Dừng test mạng"""
        self.is_testing = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="Test đã bị dừng", text_color=Theme.WARNING)
    
    def run_network_tests(self):
        """Chạy các test mạng"""
        tests = [
            ("Kiểm tra kết nối Internet", self.test_internet_connection),
            ("Kiểm tra DNS", self.test_dns_resolution),
            ("Test tốc độ mạng", self.test_network_speed),
            ("Kiểm tra WiFi", self.test_wifi_info),
            ("Test ping đến server", self.test_ping_latency),
            ("Kiểm tra cổng mạng", self.test_network_ports)
        ]
        
        total_tests = len(tests)
        
        for i, (test_name, test_func) in enumerate(tests):
            if not self.is_testing:
                break
                
            self.update_status(f"Đang chạy: {test_name}...")
            self.progress_bar.set((i + 0.5) / total_tests)
            
            try:
                result = test_func()
                self.display_test_result(test_name, result)
            except Exception as e:
                self.display_test_result(test_name, {"status": "error", "message": str(e)})
            
            self.progress_bar.set((i + 1) / total_tests)
            time.sleep(0.5)  # Small delay between tests
        
        if self.is_testing:
            self.update_status("Hoàn thành tất cả test mạng!")
            self.stop_network_test()
    
    def test_internet_connection(self):
        """Test kết nối Internet"""
        try:
            # Test multiple endpoints
            endpoints = [
                ("Google", "8.8.8.8"),
                ("Cloudflare", "1.1.1.1"),
                ("OpenDNS", "208.67.222.222")
            ]
            
            results = []
            for name, ip in endpoints:
                try:
                    socket.create_connection((ip, 53), timeout=3)
                    results.append(f"✅ {name}: Kết nối OK")
                except:
                    results.append(f"❌ {name}: Không kết nối được")
            
            # Test HTTP connection
            try:
                response = requests.get("https://www.google.com", timeout=5)
                if response.status_code == 200:
                    results.append("✅ HTTP: Kết nối web OK")
                else:
                    results.append(f"⚠️ HTTP: Status {response.status_code}")
            except:
                results.append("❌ HTTP: Không thể kết nối web")
            
            return {
                "status": "success" if "❌" not in str(results) else "warning",
                "details": results
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Lỗi test Internet: {e}"}
    
    def test_dns_resolution(self):
        """Test phân giải DNS"""
        try:
            domains = ["google.com", "facebook.com", "youtube.com", "github.com"]
            results = []
            
            for domain in domains:
                try:
                    start_time = time.time()
                    socket.gethostbyname(domain)
                    resolve_time = (time.time() - start_time) * 1000
                    results.append(f"✅ {domain}: {resolve_time:.1f}ms")
                except:
                    results.append(f"❌ {domain}: Không phân giải được")
            
            return {
                "status": "success" if "❌" not in str(results) else "error",
                "details": results
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Lỗi test DNS: {e}"}
    
    def test_network_speed(self):
        """Test tốc độ mạng đơn giản"""
        try:
            # Download test với file nhỏ
            test_url = "https://httpbin.org/bytes/1048576"  # 1MB
            
            start_time = time.time()
            response = requests.get(test_url, timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                download_time = end_time - start_time
                file_size_mb = len(response.content) / (1024 * 1024)
                speed_mbps = (file_size_mb * 8) / download_time  # Convert to Mbps
                
                return {
                    "status": "success",
                    "details": [
                        f"📊 Tốc độ download: {speed_mbps:.2f} Mbps",
                        f"⏱️ Thời gian: {download_time:.2f}s",
                        f"📦 Dung lượng test: {file_size_mb:.1f} MB"
                    ]
                }
            else:
                return {"status": "error", "message": "Không thể test tốc độ"}
                
        except Exception as e:
            return {"status": "error", "message": f"Lỗi test tốc độ: {e}"}
    
    def test_wifi_info(self):
        """Lấy thông tin WiFi"""
        try:
            import platform
            results = []
            
            if platform.system() == "Windows":
                # Get WiFi info on Windows
                try:
                    cmd = 'netsh wlan show profiles'
                    output = subprocess.check_output(cmd, shell=True, text=True)
                    profiles = [line.split(':')[1].strip() for line in output.split('\n') 
                               if 'All User Profile' in line]
                    
                    results.append(f"📶 Số mạng WiFi đã lưu: {len(profiles)}")
                    
                    # Get current connection
                    cmd = 'netsh wlan show interfaces'
                    output = subprocess.check_output(cmd, shell=True, text=True)
                    
                    for line in output.split('\n'):
                        if 'SSID' in line and 'BSSID' not in line:
                            ssid = line.split(':')[1].strip()
                            results.append(f"🔗 Mạng hiện tại: {ssid}")
                        elif 'Signal' in line:
                            signal = line.split(':')[1].strip()
                            results.append(f"📡 Cường độ tín hiệu: {signal}")
                        elif 'Channel' in line:
                            channel = line.split(':')[1].strip()
                            results.append(f"📻 Kênh: {channel}")
                    
                except subprocess.CalledProcessError:
                    results.append("⚠️ Không thể lấy thông tin WiFi chi tiết")
            else:
                results.append("ℹ️ Chỉ hỗ trợ chi tiết trên Windows")
            
            return {
                "status": "success",
                "details": results if results else ["ℹ️ Không có thông tin WiFi"]
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Lỗi lấy thông tin WiFi: {e}"}
    
    def test_ping_latency(self):
        """Test ping đến các server"""
        try:
            servers = [
                ("Google DNS", "8.8.8.8"),
                ("Cloudflare", "1.1.1.1"),
                ("FPT", "210.245.31.130"),
                ("VNPT", "203.162.4.191")
            ]
            
            results = []
            
            for name, ip in servers:
                try:
                    if platform.system() == "Windows":
                        cmd = f"ping -n 3 {ip}"
                    else:
                        cmd = f"ping -c 3 {ip}"
                    
                    output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                    
                    # Parse ping results
                    if "Average" in output or "avg" in output:
                        # Extract average ping time
                        lines = output.split('\n')
                        for line in lines:
                            if 'Average' in line or 'avg' in line:
                                # Windows: Average = XXXms, Linux: avg/XXX.XXX
                                if 'Average' in line:
                                    ping_time = line.split('=')[1].strip().replace('ms', '')
                                else:
                                    ping_time = line.split('/')[1]
                                results.append(f"🏓 {name}: {ping_time}ms")
                                break
                    else:
                        results.append(f"✅ {name}: Kết nối OK")
                        
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    results.append(f"❌ {name}: Timeout/Không kết nối được")
            
            return {
                "status": "success" if results else "error",
                "details": results
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Lỗi test ping: {e}"}
    
    def test_network_ports(self):
        """Test các cổng mạng quan trọng"""
        try:
            ports_to_test = [
                (80, "HTTP"),
                (443, "HTTPS"),
                (53, "DNS"),
                (22, "SSH"),
                (21, "FTP"),
                (25, "SMTP")
            ]
            
            results = []
            test_host = "google.com"
            
            for port, service in ports_to_test:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((test_host, port))
                    sock.close()
                    
                    if result == 0:
                        results.append(f"✅ Port {port} ({service}): Mở")
                    else:
                        results.append(f"❌ Port {port} ({service}): Đóng/Chặn")
                        
                except:
                    results.append(f"⚠️ Port {port} ({service}): Không test được")
            
            return {
                "status": "success",
                "details": results
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Lỗi test ports: {e}"}
    
    def update_status(self, message):
        """Cập nhật trạng thái"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
    
    def display_test_result(self, test_name, result):
        """Hiển thị kết quả test"""
        # Create result card
        result_card = ctk.CTkFrame(self.results_frame, fg_color=Theme.FRAME, corner_radius=8)
        result_card.pack(fill="x", padx=10, pady=5)
        
        # Status color
        status = result.get("status", "unknown")
        status_colors = {
            "success": Theme.SUCCESS,
            "warning": Theme.WARNING, 
            "error": Theme.ERROR
        }
        status_color = status_colors.get(status, Theme.TEXT_SECONDARY)
        
        # Header
        header_frame = ctk.CTkFrame(result_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(header_frame, text=test_name, font=("Segoe UI", 16, "bold"), 
                    text_color=Theme.TEXT).pack(side="left")
        
        status_text = {"success": "✅ Thành công", "warning": "⚠️ Cảnh báo", "error": "❌ Lỗi"}.get(status, "❓ Không rõ")
        ctk.CTkLabel(header_frame, text=status_text, font=Theme.BODY_FONT, 
                    text_color=status_color).pack(side="right")
        
        # Details
        if "details" in result:
            for detail in result["details"]:
                ctk.CTkLabel(result_card, text=f"  {detail}", font=Theme.BODY_FONT, 
                            text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=15, pady=2)
        
        if "message" in result:
            ctk.CTkLabel(result_card, text=f"  {result['message']}", font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=15, pady=2)
        
        # Add some spacing
        ctk.CTkLabel(result_card, text="", height=5).pack()
        
        # Store result
        self.test_results[test_name] = result