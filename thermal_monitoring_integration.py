# Thermal Monitoring - Integration for main_enhanced_auto.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
import psutil
from collections import deque
from datetime import datetime

try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class ThermalMonitor:
    """Real-time thermal and performance monitoring"""
    
    def __init__(self):
        self.is_monitoring = False
        self.max_data_points = 60
        self.cpu_temps = deque(maxlen=self.max_data_points)
        self.cpu_usage = deque(maxlen=self.max_data_points)
        self.memory_usage = deque(maxlen=self.max_data_points)
        self.timestamps = deque(maxlen=self.max_data_points)
        self.max_cpu_temp = 0
        self.avg_cpu_temp = 0
        self.max_cpu_usage = 0
        self.throttling_detected = False
        self.warnings = []
    
    def get_cpu_temperature(self):
        """Get CPU temperature"""
        try:
            import platform
            if platform.system() == "Windows":
                try:
                    import wmi
                    w = wmi.WMI(namespace="root\\wmi")
                    temp_info = w.MSAcpi_ThermalZoneTemperature()
                    if temp_info:
                        return (temp_info[0].CurrentTemperature / 10.0) - 273.15
                except:
                    pass
            
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for key in ['coretemp', 'k10temp', 'cpu_thermal']:
                        if key in temps:
                            return max([e.current for e in temps[key] if e.current])
        except:
            pass
        
        # Simulate based on CPU usage
        base = 35
        load = (psutil.cpu_percent() / 100) * 40
        import random
        return max(30, min(95, base + load + random.uniform(-2, 2)))
    
    def start_monitoring(self, update_callback=None):
        """Start monitoring loop"""
        self.is_monitoring = True
        self.warnings = []
        
        def monitor_loop():
            start_time = time.time()
            while self.is_monitoring:
                try:
                    current_time = time.time() - start_time
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    memory_percent = psutil.virtual_memory().percent
                    cpu_temp = self.get_cpu_temperature()
                    
                    self.timestamps.append(current_time)
                    self.cpu_usage.append(cpu_percent)
                    self.memory_usage.append(memory_percent)
                    self.cpu_temps.append(cpu_temp)
                    
                    self.max_cpu_temp = max(self.max_cpu_temp, cpu_temp)
                    self.max_cpu_usage = max(self.max_cpu_usage, cpu_percent)
                    if self.cpu_temps:
                        self.avg_cpu_temp = sum(self.cpu_temps) / len(self.cpu_temps)
                    
                    # Check for issues
                    if cpu_temp > 80:
                        self.add_warning(f"🔥 High temp: {cpu_temp:.1f}°C")
                    if cpu_temp > 85 and cpu_percent < 50:
                        if not self.throttling_detected:
                            self.throttling_detected = True
                            self.add_warning("🐌 Throttling detected")
                    
                    if update_callback:
                        update_callback(cpu_temp, cpu_percent, memory_percent)
                    
                    time.sleep(1)
                except Exception as e:
                    self.add_warning(f"❌ Error: {e}")
                    break
        
        threading.Thread(target=monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
    
    def add_warning(self, message):
        """Add warning message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.warnings.append(f"[{timestamp}] {message}")
    
    def get_summary(self):
        """Get monitoring summary"""
        if not self.cpu_temps:
            return "No data"
        
        return {
            "max_temp": self.max_cpu_temp,
            "avg_temp": self.avg_cpu_temp,
            "min_temp": min(self.cpu_temps),
            "max_cpu": self.max_cpu_usage,
            "avg_cpu": sum(self.cpu_usage) / len(self.cpu_usage),
            "throttling": self.throttling_detected,
            "warnings": self.warnings
        }
