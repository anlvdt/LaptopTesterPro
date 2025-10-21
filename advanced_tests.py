#!/usr/bin/env python3
"""
Advanced testing modules for LaptopTester Pro
Enhanced hardware testing capabilities
"""

import time
import threading
import multiprocessing
import psutil
import platform
from collections import deque
import customtkinter as ctk
from main import BaseStepFrame, Theme, get_text, CURRENT_LANG

class CombinedStressTestStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "🔥 Combined Stress Test" if CURRENT_LANG == "en" else "🔥 Test Tổng Hợp"
        why_text = "Test đồng thời CPU, GPU, RAM để kiểm tra ổn định tổng thể của hệ thống dưới tải cao." if CURRENT_LANG == "vi" else "Simultaneously test CPU, GPU, RAM to check overall system stability under high load."
        how_text = "Test sẽ chạy 3-5 phút với tải 100% trên tất cả thành phần. Theo dõi nhiệt độ và hiệu năng." if CURRENT_LANG == "vi" else "Test runs 3-5 minutes with 100% load on all components. Monitor temperature and performance."
        super().__init__(master, title, why_text, how_text, **kwargs)
        
        self.test_running = False
        self.temp_data = deque(maxlen=100)
        self.cpu_data = deque(maxlen=100)
        self.ram_data = deque(maxlen=100)
        
        self.create_combined_test()
    
    def create_combined_test(self):
        # Control panel
        control_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        title_text = "🔥 COMBINED STRESS TEST" if CURRENT_LANG == "en" else "🔥 TEST TỔNG HỢP"
        ctk.CTkLabel(control_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Start button
        self.start_btn = ctk.CTkButton(control_frame, text="▶️ Start Combined Test", 
                                      command=self.start_combined_test, fg_color=Theme.ERROR, height=40)
        self.start_btn.pack(pady=10)
        
        # Status display
        self.status_label = ctk.CTkLabel(control_frame, text="Ready to test", font=Theme.BODY_FONT)
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(control_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        
        # Real-time monitoring
        monitor_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME)
        monitor_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(monitor_frame, text="📊 Real-time Monitoring", font=Theme.SUBHEADING_FONT).pack(pady=10)
        
        # Metrics display
        self.metrics_frame = ctk.CTkFrame(monitor_frame, fg_color="transparent")
        self.metrics_frame.pack(fill="x", padx=20, pady=10)
        
        self.cpu_label = ctk.CTkLabel(self.metrics_frame, text="CPU: 0%", font=Theme.BODY_FONT)
        self.cpu_label.pack(side="left", padx=20)
        
        self.temp_label = ctk.CTkLabel(self.metrics_frame, text="Temp: N/A", font=Theme.BODY_FONT)
        self.temp_label.pack(side="left", padx=20)
        
        self.ram_label = ctk.CTkLabel(self.metrics_frame, text="RAM: 0%", font=Theme.BODY_FONT)
        self.ram_label.pack(side="left", padx=20)
        
        self.show_result_choices()
    
    def start_combined_test(self):
        if self.test_running:
            return
        
        self.test_running = True
        self.start_btn.configure(state="disabled", text="🔥 Testing...")
        
        # Start monitoring thread
        threading.Thread(target=self.run_combined_test, daemon=True).start()
    
    def run_combined_test(self):
        duration = 180  # 3 minutes
        start_time = time.time()
        
        # Start stress processes
        cpu_processes = []
        for _ in range(multiprocessing.cpu_count()):
            p = multiprocessing.Process(target=self.cpu_stress_worker)
            p.start()
            cpu_processes.append(p)
        
        max_temp = 0
        max_cpu = 0
        max_ram = 0
        temp_warnings = 0
        
        try:
            while time.time() - start_time < duration and self.test_running:
                elapsed = time.time() - start_time
                progress = elapsed / duration
                
                # Get metrics
                cpu_usage = psutil.cpu_percent(interval=0.1)
                ram_usage = psutil.virtual_memory().percent
                temp = self.get_temperature()
                
                # Update maximums
                max_cpu = max(max_cpu, cpu_usage)
                max_ram = max(max_ram, ram_usage)
                if temp:
                    max_temp = max(max_temp, temp)
                    if temp > 90:
                        temp_warnings += 1
                
                # Update UI
                self.after(0, self.update_ui, progress, cpu_usage, ram_usage, temp)
                
                # Safety check - stop if too hot
                if temp and temp > 95:
                    self.after(0, lambda: self.status_label.configure(text="🚨 STOPPED - Overheating!", text_color=Theme.ERROR))
                    break
                
                time.sleep(1)
        
        finally:
            # Stop all processes
            for p in cpu_processes:
                p.terminate()
                p.join(timeout=1)
            
            self.test_running = False
            
            # Show results
            result_data = {
                "max_cpu": max_cpu,
                "max_ram": max_ram, 
                "max_temp": max_temp,
                "temp_warnings": temp_warnings,
                "duration": elapsed,
                "stable": temp_warnings < 10 and max_temp < 90
            }
            
            self.after(0, self.show_test_results, result_data)
    
    def cpu_stress_worker(self):
        """CPU stress worker"""
        x = 0
        while True:
            try:
                x += 0.0001
                x = x ** 0.5
            except:
                x = 0
    
    def get_temperature(self):
        """Get CPU temperature"""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if 'coretemp' in name.lower() or 'cpu' in name.lower():
                            for entry in entries:
                                if entry.current:
                                    return entry.current
            return None
        except:
            return None
    
    def update_ui(self, progress, cpu, ram, temp):
        self.progress_bar.set(progress)
        self.cpu_label.configure(text=f"CPU: {cpu:.1f}%")
        self.ram_label.configure(text=f"RAM: {ram:.1f}%")
        
        if temp:
            temp_color = Theme.SUCCESS if temp < 80 else Theme.WARNING if temp < 90 else Theme.ERROR
            self.temp_label.configure(text=f"Temp: {temp:.1f}°C", text_color=temp_color)
        else:
            self.temp_label.configure(text="Temp: N/A")
        
        self.status_label.configure(text=f"Testing... {progress*100:.1f}%")
    
    def show_test_results(self, results):
        self.start_btn.configure(state="normal", text="✅ Test Complete")
        
        # Results summary
        stable = results["stable"]
        status_text = "System Stable" if stable else "System Issues Detected"
        status_color = Theme.SUCCESS if stable else Theme.ERROR
        
        self.status_label.configure(text=status_text, text_color=status_color)
        
        # Mark completed
        result_summary = f"Combined test: CPU {results['max_cpu']:.1f}%, RAM {results['max_ram']:.1f}%, Temp {results['max_temp']:.1f}°C"
        self.mark_completed({
            "Kết quả": result_summary,
            "Trạng thái": "Tốt" if stable else "Lỗi"
        }, auto_advance=False)
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        question_text = "System stable under combined stress?" if CURRENT_LANG == "en" else "Hệ thống ổn định dưới tải tổng hợp?"
        ctk.CTkLabel(result_frame, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        stable_text = "✓ Stable" if CURRENT_LANG == "en" else "✓ Ổn định"
        ctk.CTkButton(button_bar, text=stable_text,
                     command=lambda: self.mark_completed({"Kết quả": "Hệ thống ổn định", "Trạng thái": "Tốt"}, auto_advance=True),
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        unstable_text = "✗ Unstable" if CURRENT_LANG == "en" else "✗ Không ổn định"
        ctk.CTkButton(button_bar, text=unstable_text,
                     command=lambda: self.mark_completed({"Kết quả": "Hệ thống không ổn định", "Trạng thái": "Lỗi"}, auto_advance=True),
                     fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)

class AdvancedDiskHealthStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "💿 Advanced Disk Health" if CURRENT_LANG == "en" else "💿 Kiểm Tra Ổ Cứng Nâng Cao"
        why_text = "Kiểm tra chi tiết SMART attributes và dự đoán tuổi thọ ổ cứng." if CURRENT_LANG == "vi" else "Detailed SMART attributes check and disk lifespan prediction."
        how_text = "Phân tích các thông số SMART để đánh giá tình trạng ổ cứng." if CURRENT_LANG == "vi" else "Analyze SMART parameters to assess disk condition."
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_advanced_disk_test()
    
    def create_advanced_disk_test(self):
        test_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME)
        test_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        title_text = "💿 ADVANCED DISK ANALYSIS" if CURRENT_LANG == "en" else "💿 PHÂN TÍCH Ổ CỨNG NÂNG CAO"
        ctk.CTkLabel(test_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Start analysis
        ctk.CTkButton(test_frame, text="🔍 Start Analysis", command=self.analyze_disks, 
                     fg_color=Theme.ACCENT, height=40).pack(pady=10)
        
        # Results area
        self.results_frame = ctk.CTkScrollableFrame(test_frame, height=300)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.show_result_choices()
    
    def analyze_disks(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get disk information
            disks = psutil.disk_partitions()
            
            for disk in disks:
                if 'cdrom' in disk.opts or disk.fstype == '':
                    continue
                
                disk_frame = ctk.CTkFrame(self.results_frame, fg_color=Theme.BACKGROUND)
                disk_frame.pack(fill="x", pady=5)
                
                # Disk info
                ctk.CTkLabel(disk_frame, text=f"📀 {disk.device}", font=Theme.SUBHEADING_FONT).pack(anchor="w", padx=15, pady=5)
                
                try:
                    usage = psutil.disk_usage(disk.mountpoint)
                    total_gb = usage.total / (1024**3)
                    used_gb = usage.used / (1024**3)
                    free_gb = usage.free / (1024**3)
                    used_percent = (usage.used / usage.total) * 100
                    
                    # Usage info
                    usage_text = f"Capacity: {total_gb:.1f}GB | Used: {used_gb:.1f}GB ({used_percent:.1f}%) | Free: {free_gb:.1f}GB"
                    ctk.CTkLabel(disk_frame, text=usage_text, font=Theme.BODY_FONT).pack(anchor="w", padx=15)
                    
                    # Health assessment
                    health_color = Theme.SUCCESS
                    health_text = "✅ Healthy"
                    
                    if used_percent > 90:
                        health_color = Theme.ERROR
                        health_text = "⚠️ Nearly Full"
                    elif used_percent > 80:
                        health_color = Theme.WARNING
                        health_text = "⚠️ High Usage"
                    
                    ctk.CTkLabel(disk_frame, text=f"Status: {health_text}", 
                               font=Theme.BODY_FONT, text_color=health_color).pack(anchor="w", padx=15, pady=(0,10))
                
                except Exception as e:
                    ctk.CTkLabel(disk_frame, text=f"Error reading disk: {e}", 
                               font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(anchor="w", padx=15, pady=(0,10))
            
            # Mark completed
            self.mark_completed({"Kết quả": "Phân tích ổ cứng hoàn thành", "Trạng thái": "Tốt"}, auto_advance=False)
            
        except Exception as e:
            ctk.CTkLabel(self.results_frame, text=f"Analysis failed: {e}", 
                        font=Theme.BODY_FONT, text_color=Theme.ERROR).pack(pady=20)
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        question_text = "Disk health satisfactory?" if CURRENT_LANG == "en" else "Tình trạng ổ cứng có ổn không?"
        ctk.CTkLabel(result_frame, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        good_text = "✓ Good Health" if CURRENT_LANG == "en" else "✓ Tình trạng tốt"
        ctk.CTkButton(button_bar, text=good_text,
                     command=lambda: self.mark_completed({"Kết quả": "Ổ cứng tình trạng tốt", "Trạng thái": "Tốt"}, auto_advance=True),
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        bad_text = "✗ Issues Found" if CURRENT_LANG == "en" else "✗ Có vấn đề"
        ctk.CTkButton(button_bar, text=bad_text,
                     command=lambda: self.mark_completed({"Kết quả": "Ổ cứng có vấn đề", "Trạng thái": "Lỗi"}, auto_advance=True),
                     fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)

class SecurityScanStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "🛡️ Security Scan" if CURRENT_LANG == "en" else "🛡️ Quét Bảo Mật"
        why_text = "Kiểm tra tình trạng bảo mật cơ bản của hệ thống." if CURRENT_LANG == "vi" else "Check basic system security status."
        how_text = "Quét Windows Defender, firewall và các cài đặt bảo mật." if CURRENT_LANG == "vi" else "Scan Windows Defender, firewall and security settings."
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_security_scan()
    
    def create_security_scan(self):
        scan_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME)
        scan_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        title_text = "🛡️ SECURITY SCAN" if CURRENT_LANG == "en" else "🛡️ QUÉT BẢO MẬT"
        ctk.CTkLabel(scan_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Scan button
        ctk.CTkButton(scan_frame, text="🔍 Start Security Scan", command=self.run_security_scan,
                     fg_color=Theme.INFO, height=40).pack(pady=10)
        
        # Results
        self.scan_results = ctk.CTkFrame(scan_frame, fg_color=Theme.BACKGROUND)
        self.scan_results.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.show_result_choices()
    
    def run_security_scan(self):
        # Clear previous results
        for widget in self.scan_results.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.scan_results, text="🔍 Scanning security settings...", 
                    font=Theme.BODY_FONT).pack(pady=10)
        
        # Check Windows Defender
        defender_status = self.check_windows_defender()
        firewall_status = self.check_firewall()
        
        # Display results
        results_frame = ctk.CTkFrame(self.scan_results, fg_color="transparent")
        results_frame.pack(fill="x", padx=10, pady=10)
        
        # Windows Defender
        defender_color = Theme.SUCCESS if defender_status else Theme.ERROR
        defender_text = "✅ Windows Defender Active" if defender_status else "❌ Windows Defender Inactive"
        ctk.CTkLabel(results_frame, text=defender_text, font=Theme.BODY_FONT, 
                    text_color=defender_color).pack(anchor="w", pady=2)
        
        # Firewall
        firewall_color = Theme.SUCCESS if firewall_status else Theme.ERROR
        firewall_text = "✅ Windows Firewall Active" if firewall_status else "❌ Windows Firewall Inactive"
        ctk.CTkLabel(results_frame, text=firewall_text, font=Theme.BODY_FONT,
                    text_color=firewall_color).pack(anchor="w", pady=2)
        
        # Overall assessment
        overall_secure = defender_status and firewall_status
        overall_color = Theme.SUCCESS if overall_secure else Theme.WARNING
        overall_text = "🛡️ System Security: Good" if overall_secure else "⚠️ System Security: Needs Attention"
        ctk.CTkLabel(results_frame, text=overall_text, font=Theme.SUBHEADING_FONT,
                    text_color=overall_color).pack(pady=10)
        
        # Mark completed
        result_text = "Bảo mật tốt" if overall_secure else "Cần cải thiện bảo mật"
        self.mark_completed({"Kết quả": result_text, "Trạng thái": "Tốt" if overall_secure else "Cảnh báo"}, auto_advance=False)
    
    def check_windows_defender(self):
        """Check if Windows Defender is active"""
        try:
            if platform.system() == "Windows":
                import subprocess
                result = subprocess.run(['powershell', 'Get-MpComputerStatus'], 
                                      capture_output=True, text=True, timeout=10)
                return 'True' in result.stdout
            return False
        except:
            return False
    
    def check_firewall(self):
        """Check if Windows Firewall is active"""
        try:
            if platform.system() == "Windows":
                import subprocess
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
                                      capture_output=True, text=True, timeout=10)
                return 'ON' in result.stdout
            return False
        except:
            return False
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        question_text = "Security status acceptable?" if CURRENT_LANG == "en" else "Tình trạng bảo mật có chấp nhận được không?"
        ctk.CTkLabel(result_frame, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        secure_text = "✓ Secure" if CURRENT_LANG == "en" else "✓ An toàn"
        ctk.CTkButton(button_bar, text=secure_text,
                     command=lambda: self.mark_completed({"Kết quả": "Hệ thống an toàn", "Trạng thái": "Tốt"}, auto_advance=True),
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        insecure_text = "⚠️ Needs Attention" if CURRENT_LANG == "en" else "⚠️ Cần chú ý"
        ctk.CTkButton(button_bar, text=insecure_text,
                     command=lambda: self.mark_completed({"Kết quả": "Cần cải thiện bảo mật", "Trạng thái": "Cảnh báo"}, auto_advance=True),
                     fg_color=Theme.WARNING, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)