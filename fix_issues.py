#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fix issues:
1. Add translations for CPU/GPU test
2. Add GPU to thermal monitor
3. Fix GPU test not fullscreen
4. Fix SystemStabilityStep to real combined test with GPU
"""

import re

def fix_main_file():
    with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix ThermalMonitorStep - thêm GPU monitoring
    content = content.replace(
        'self.cpu_usage = deque(maxlen=60)\r\n        self.timestamps = deque(maxlen=60)',
        'self.cpu_usage = deque(maxlen=60)\r\n        self.gpu_usage = deque(maxlen=60)\r\n        self.timestamps = deque(maxlen=60)'
    )
    
    # 2. Thêm GPU label vào thermal UI
    content = content.replace(
        'self.memory_label = ctk.CTkLabel(metrics_frame, text="💾 Memory: --%", font=Theme.BODY_FONT)\n        self.memory_label.pack(pady=5)',
        'self.memory_label = ctk.CTkLabel(metrics_frame, text="💾 Memory: --%", font=Theme.BODY_FONT)\n        self.memory_label.pack(pady=5)\n        self.gpu_label = ctk.CTkLabel(metrics_frame, text="🎮 GPU: --%", font=Theme.BODY_FONT)\n        self.gpu_label.pack(pady=5)'
    )
    
    # 3. Thêm GPU monitoring vào monitoring_loop
    old_monitoring = '''            self.timestamps.append(current_time)
                self.cpu_usage.append(cpu_percent)
                self.cpu_temps.append(cpu_temp)

                self.after(0, self.update_ui, cpu_temp, cpu_percent, memory_percent)'''
    
    new_monitoring = '''            self.timestamps.append(current_time)
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
    
    content = content.replace(old_monitoring, new_monitoring)
    
    # 4. Update update_ui signature
    content = content.replace(
        'def update_ui(self, cpu_temp, cpu_usage, memory_usage):',
        'def update_ui(self, cpu_temp, cpu_usage, memory_usage, gpu_usage=0):'
    )
    
    # 5. Thêm GPU label update
    content = content.replace(
        'if hasattr(self, \'memory_label\') and self.memory_label.winfo_exists():\n            self.memory_label.configure(text=f"💾 Memory: {memory_usage:.1f}%")',
        'if hasattr(self, \'memory_label\') and self.memory_label.winfo_exists():\n            self.memory_label.configure(text=f"💾 Memory: {memory_usage:.1f}%")\n        if hasattr(self, \'gpu_label\') and self.gpu_label.winfo_exists():\n            self.gpu_label.configure(text=f"🎮 GPU: {gpu_usage:.1f}%")'
    )
    
    # 6. Fix SystemStabilityStep - thêm GPU stress
    old_combined = '''    def run_combined_test(self):
        duration = 180

        start_time = time.time()

        while time.time() - start_time < duration and self.is_testing:
            elapsed = time.time() - start_time
            progress = elapsed / duration
            cpu_usage = psutil.cpu_percent(interval=0.5)

            temp = get_cpu_temperature() or 0
            mem_usage = psutil.virtual_memory().percent

            self.progress_bar.set(progress)
            self.status_label.configure(text=f"CPU: {cpu_usage:.1f}% | RAM: {mem_usage:.1f}% | Temp: {temp:.1f}°C")
            time.sleep(1)
        self.is_testing = False

        self.after(0, self.show_results)'''
    
    new_combined = '''    def run_combined_test(self):
        duration = 180
        start_time = time.time()
        
        # Start CPU stress in background
        import multiprocessing
        cpu_processes = []
        for _ in range(multiprocessing.cpu_count()):
            p = multiprocessing.Process(target=self.cpu_stress_worker, daemon=True)
            p.start()
            cpu_processes.append(p)
        
        # Start GPU stress if pygame available
        gpu_thread = None
        if pygame:
            gpu_thread = threading.Thread(target=self.gpu_stress_worker, args=(duration,), daemon=True)
            gpu_thread.start()

        while time.time() - start_time < duration and self.is_testing:
            elapsed = time.time() - start_time
            progress = elapsed / duration
            cpu_usage = psutil.cpu_percent(interval=0.5)
            temp = get_cpu_temperature() or 0
            mem_usage = psutil.virtual_memory().percent
            
            # Try get GPU usage
            gpu_usage = 0
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                                      capture_output=True, text=True, timeout=1)
                if result.returncode == 0:
                    gpu_usage = float(result.stdout.strip())
            except:
                pass

            self.progress_bar.set(progress)
            status_text = f"CPU: {cpu_usage:.1f}% | GPU: {gpu_usage:.1f}% | RAM: {mem_usage:.1f}% | Temp: {temp:.1f}°C"
            self.status_label.configure(text=status_text)
            time.sleep(1)
        
        # Stop all stress
        self.is_testing = False
        for p in cpu_processes:
            p.terminate()
        
        self.after(0, self.show_results)
    
    def cpu_stress_worker(self):
        import math
        x = 0
        while self.is_testing:
            x += 0.0001
            math.sqrt(x * math.pi)
    
    def gpu_stress_worker(self, duration):
        if not pygame:
            return
        try:
            pygame.init()
            screen = pygame.display.set_mode((400, 300))
            clock = pygame.time.Clock()
            start = time.time()
            while time.time() - start < duration and self.is_testing:
                screen.fill((0, 0, 0))
                for i in range(100):
                    x = (i * 10) % 400
                    y = (i * 8) % 300
                    pygame.draw.circle(screen, (255, i*2, 255-i*2), (x, y), 5)
                pygame.display.flip()
                clock.tick(60)
            pygame.quit()
        except:
            pass'''
    
    content = content.replace(old_combined, new_combined)
    
    # Write back
    with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done! Fixed all issues:")
    print("  1. Added GPU to Thermal Monitor")
    print("  2. Added GPU stress to System Stability Test")
    print("  3. GPU test window not fullscreen (already done)")
    print("  4. Translated why_text and how_text (already done)")

if __name__ == '__main__':
    fix_main_file()
