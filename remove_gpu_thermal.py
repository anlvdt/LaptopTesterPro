#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove GPU from thermal test"""

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove GPU from why_text
content = content.replace(
    'why_text = "Giám sát nhiệt độ và hiệu năng real-time của CPU, GPU, RAM giúp phát hiện vấn đề tản nhiệt, throttling và hiệu năng không ổn định."',
    'why_text = "Giám sát nhiệt độ và hiệu năng real-time của CPU, RAM giúp phát hiện vấn đề tản nhiệt, throttling và hiệu năng không ổn định."'
)

content = content.replace(
    'why_text = "Real-time monitoring of CPU, GPU, RAM temperature and performance helps detect cooling issues, throttling and unstable performance."',
    'why_text = "Real-time monitoring of CPU, RAM temperature and performance helps detect cooling issues, throttling and unstable performance."'
)

# 2. Remove GPU usage deque
content = content.replace(
    'self.cpu_usage = deque(maxlen=60)\n        self.gpu_usage = deque(maxlen=60)\n        self.timestamps = deque(maxlen=60)',
    'self.cpu_usage = deque(maxlen=60)\n        self.timestamps = deque(maxlen=60)'
)

# 3. Remove GPU label
content = content.replace(
    '''self.memory_label = ctk.CTkLabel(metrics_frame, text="💾 Memory: --%", font=Theme.BODY_FONT)
        self.memory_label.pack(pady=5)
        self.gpu_label = ctk.CTkLabel(metrics_frame, text="🎮 GPU: --%", font=Theme.BODY_FONT)
        self.gpu_label.pack(pady=5)''',
    '''self.memory_label = ctk.CTkLabel(metrics_frame, text="💾 Memory: --%", font=Theme.BODY_FONT)
        self.memory_label.pack(pady=5)'''
)

# 4. Remove GPU monitoring from loop
old_monitoring = '''            self.timestamps.append(current_time)
                self.cpu_usage.append(cpu_percent)
                self.cpu_temps.append(cpu_temp)
                
                # Get GPU usage if available
                gpu_percent = 0
                try:
                    import subprocess
                    result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                                          capture_output=True, text=True, timeout=1)
                    if result.returncode == 0:
                        gpu_percent = float(result.stdout.strip())
                except:
                    pass
                self.gpu_usage.append(gpu_percent)

                self.after(0, self.update_ui, cpu_temp, cpu_percent, memory_percent, gpu_percent)'''

new_monitoring = '''            self.timestamps.append(current_time)
                self.cpu_usage.append(cpu_percent)
                self.cpu_temps.append(cpu_temp)

                self.after(0, self.update_ui, cpu_temp, cpu_percent, memory_percent)'''

content = content.replace(old_monitoring, new_monitoring)

# 5. Remove GPU parameter from update_ui
content = content.replace(
    'def update_ui(self, cpu_temp, cpu_usage, memory_usage, gpu_usage=0):',
    'def update_ui(self, cpu_temp, cpu_usage, memory_usage):'
)

# 6. Remove GPU label update
content = content.replace(
    '''if hasattr(self, 'memory_label') and self.memory_label.winfo_exists():
            self.memory_label.configure(text=f"💾 Memory: {memory_usage:.1f}%")
        if hasattr(self, 'gpu_label') and self.gpu_label.winfo_exists():
            self.gpu_label.configure(text=f"🎮 GPU: {gpu_usage:.1f}%")''',
    '''if hasattr(self, 'memory_label') and self.memory_label.winfo_exists():
            self.memory_label.configure(text=f"💾 Memory: {memory_usage:.1f}%")'''
)

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Removed GPU from Thermal Monitor")
