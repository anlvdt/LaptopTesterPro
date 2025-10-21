import time
import sys
import os
import importlib.util
import multiprocessing
import logging

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
logger = logging.getLogger(__name__)

# Import enhanced hardware reader
try:
    from enhanced_hardware_reader_v2 import hardware_reader
except ImportError:
    hardware_reader = None

LHM_READER_PATH = os.path.join(os.path.dirname(__file__), "lhm_reader.py")

# Tái sử dụng LHM_Manager từ worker_cpu.py để tối ưu hóa
class LHM_Manager:
    """Quản lý việc đọc dữ liệu từ LibreHardwareMonitor để tránh import lại nhiều lần."""
    def __init__(self):
        self.lhm_module = None
        self._initialize()

    def _initialize(self):
        """Import và khởi tạo module lhm_reader một lần duy nhất."""
        if not os.path.exists(LHM_READER_PATH):
            logger.warning("lhm_reader.py not found. LHM stats will be unavailable.")
            return
        try:
            spec = importlib.util.spec_from_file_location("lhm_reader", LHM_READER_PATH)
            self.lhm_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.lhm_module)
            logger.info("LHM_Manager for GPU worker initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize LHM_Manager for GPU: {e}")
            self.lhm_module = None

    def get_stats(self):
        """Lấy thông số GPU từ LibreHardwareMonitor nếu có."""
        if not self.lhm_module:
            return {}
        data = self.lhm_module.get_lhm_data()
        _, gpu = self.lhm_module.extract_cpu_gpu_info(data)
        return gpu
        
def run_gpu_stress(duration, queue):
    try:
        import pygame
        import numpy as np
    except ImportError as e:
        queue.put({'type': 'error', 'message': f"Lỗi thiếu thư viện cho test GPU: {e.name}. Hãy chạy 'pip install pygame numpy'"})
        queue.put({'type': 'done'})
        return

    try:
        queue.put({'type': 'status', 'message': "Đang khởi tạo Pygame..."})
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("GPU Stress Test - Nhấn ESC để thoát")
        clock = pygame.time.Clock()
        start_time = time.time()
        particles = []
        frame_count = 0
        
        # Danh sách để thu thập dữ liệu
        fps_readings = []
        temp_readings = []
        clock_readings = []
        power_readings = []

        # Cài đặt font cho OSD
        try:
            font = pygame.font.SysFont("Segoe UI", 24)
            font_small = pygame.font.SysFont("Segoe UI", 18)
        except:
            font = pygame.font.Font(None, 30)
            font_small = pygame.font.Font(None, 24)
        
        queue.put({'type': 'status', 'message': "Đang chạy vòng lặp stress..."})
        
        # Khởi tạo LHM Manager một lần duy nhất
        lhm_manager = LHM_Manager()
        running = True
        
        while running and (time.time() - start_time < duration):
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            current_time = time.time() - start_time
            progress = current_time / duration
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            # Clear screen
            screen.fill((10, 10, 20))
            
            # Get mouse position for particle emission
            mx, my = pygame.mouse.get_pos()
            if not mx and not my: 
                mx, my = screen.get_width()//2, screen.get_height()//2

            # Create new particles
            for _ in range(5):
                particles.append([
                    [mx, my],  # position
                    [np.random.randint(-50, 50) / 10, np.random.randint(0, 50) / 10 - 2],  # velocity
                    np.random.randint(4, 10)  # size
                ])

            # Update and draw particles
            for particle in particles[:]:
                particle[0][0] += particle[1][0]  # x position
                particle[0][1] += particle[1][1]  # y position
                particle[1][1] += 0.1  # gravity
                particle[2] -= 0.05  # size decay
                
                # Remove dead particles
                if particle[2] <= 0 or particle[0][1] > screen.get_height():
                    particles.remove(particle)
                    continue
                
                # Draw particle with color based on age
                color_intensity = min(255, max(0, int(particle[2] * 25.5)))
                color = (color_intensity, color_intensity // 2, 255 - color_intensity)
                pygame.draw.circle(screen, color, 
                                 (int(particle[0][0]), int(particle[0][1])), 
                                 int(particle[2]))

            # Draw geometric patterns for additional GPU load
            for i in range(50):
                x = int(screen.get_width() * (i / 50))
                y = int(screen.get_height() * 0.8 + 50 * np.sin(current_time * 2 + i * 0.1))
                color = (int(128 + 127 * np.sin(current_time + i)), 
                        int(128 + 127 * np.cos(current_time + i)), 
                        255)
                pygame.draw.circle(screen, color, (x, y), 3)

            # Calculate FPS
            frame_count += 1
            fps = clock.get_fps()
            if fps > 0:
                fps_readings.append(fps)

            # Đọc thông số GPU từ Enhanced Hardware Reader hoặc LHM
            temp = None
            clock_speed = None
            power = None
            load = None
            
            # Thử Enhanced Hardware Reader trước
            if hardware_reader:
                try:
                    gpu_info = hardware_reader.get_gpu_info_comprehensive()
                    if gpu_info['devices']:
                        primary_gpu = gpu_info['devices'][0]
                        temp = primary_gpu.get('temperature')
                        clock_speed = primary_gpu.get('clock')
                        power = primary_gpu.get('power')
                        load = primary_gpu.get('load')
                except Exception as e:
                    logger.warning(f"Enhanced hardware reader GPU failed: {e}")
            
            # Fallback to LHM nếu không có dữ liệu
            if temp is None or clock_speed is None:
                lhm_stats = lhm_manager.get_stats()
                if temp is None:
                    temp = lhm_stats.get('temp')
                if clock_speed is None:
                    clock_speed = lhm_stats.get('clock')
                if power is None:
                    power = lhm_stats.get('power')
                if load is None:
                    load = lhm_stats.get('load')

            # Thu thập dữ liệu
            if temp is not None: temp_readings.append(temp)
            if clock_speed is not None: clock_readings.append(clock_speed)
            if power is not None: power_readings.append(power)

            # Draw performance info
            elapsed_text = font.render(f"Thời gian: {current_time:.1f}s / {duration}s", True, (255, 255, 255))
            fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            particles_text = font.render(f"Particles: {len(particles)}", True, (255, 255, 255))
            progress_text = font_small.render(f"Tiến độ: {progress*100:.1f}%", True, (255, 255, 255))
            
            # Hiển thị an toàn hơn
            temp_str = f"{temp:.1f}°C" if temp is not None else "N/A"
            clock_str = f"{clock_speed:.0f} MHz" if clock_speed is not None else "N/A"
            power_str = f"{power:.1f} W" if power is not None else "N/A"
            temp_text = font_small.render(f"GPU Temp: {temp_str}", True, (255, 200, 200))
            clock_text = font_small.render(f"GPU Clock: {clock_str}", True, (200, 255, 200))
            power_text = font_small.render(f"GPU Power: {power_str}", True, (200, 200, 255))
            
            screen.blit(elapsed_text, (10, 10))
            screen.blit(fps_text, (10, 40))
            screen.blit(particles_text, (10, 70))
            screen.blit(progress_text, (10, 100))
            screen.blit(temp_text, (10, 130))
            screen.blit(clock_text, (10, 155))
            screen.blit(power_text, (10, 180))
            
            # Draw progress bar
            bar_width = 300
            bar_height = 10
            bar_x = 10
            bar_y = 200
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))

            pygame.display.flip()
            
            # Send progress update
            if frame_count % 60 == 0:  # Update every second
                queue.put({
                    'type': 'update',
                    'progress': progress,
                    'fps': fps,
                    'particles': len(particles),
                    'frame_count': frame_count
                })

        pygame.quit()
        
        # Calculate results
        avg_fps = sum(fps_readings) / len(fps_readings) if fps_readings else 0
        min_fps = min(fps_readings) if fps_readings else 0
        max_fps = max(fps_readings) if fps_readings else 0

        # Tính toán các thông số GPU
        max_temp = max(temp_readings) if temp_readings else None
        avg_temp = sum(temp_readings) / len(temp_readings) if temp_readings else None
        avg_clock = sum(clock_readings) / len(clock_readings) if clock_readings else None
        max_power = max(power_readings) if power_readings else None
        avg_power = sum(power_readings) / len(power_readings) if power_readings else None
        
        result_data = {
            'duration': current_time,
            'total_frames': frame_count,
            'average_fps': round(avg_fps, 2),
            'min_fps': round(min_fps, 2),
            'max_fps': round(max_fps, 2),
            'max_temp': round(max_temp, 1) if max_temp is not None else None,
            'avg_temp': round(avg_temp, 1) if avg_temp is not None else None,
            'avg_clock': round(avg_clock) if avg_clock is not None else None,
            'max_power': round(max_power, 1) if max_power is not None else None,
            'avg_power': round(avg_power, 1) if avg_power is not None else None,
            'stable_performance': min_fps > 30 and avg_fps > 45
        }
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})

    except Exception as e:
        try:
            pygame.quit()
        except:
            pass
        queue.put({'type': 'error', 'message': f'Lỗi GPU stress test: {str(e)}'})
        queue.put({'type': 'done'})

def run_gpu_info_check(queue):
    """Thu thập thông tin GPU cơ bản với Enhanced Hardware Reader"""
    try:
        import platform
        
        gpu_info = {
            'platform': platform.system(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor()
        }
        
        # Sử dụng Enhanced Hardware Reader trước
        if hardware_reader:
            try:
                enhanced_gpu_info = hardware_reader.get_gpu_info_comprehensive()
                if enhanced_gpu_info['devices']:
                    gpu_info['gpus'] = enhanced_gpu_info['devices']
                    gpu_info['source'] = enhanced_gpu_info['source']
                    gpu_info['enhanced'] = True
                else:
                    gpu_info['gpus'] = [{'name': 'No GPU detected by Enhanced Reader'}]
            except Exception as e:
                logger.warning(f"Enhanced GPU info failed: {e}")
                gpu_info['enhanced_error'] = str(e)
        
        # Fallback to WMI nếu chưa có thông tin
        if 'gpus' not in gpu_info and platform.system() == "Windows":
            try:
                import wmi
                c = wmi.WMI()
                gpus = []
                for gpu in c.Win32_VideoController():
                    if gpu.Name and 'Microsoft' not in gpu.Name:
                        gpus.append({
                            'name': gpu.Name,
                            'driver_version': gpu.DriverVersion,
                            'adapter_ram': gpu.AdapterRAM,
                            'status': gpu.Status,
                            'source': 'WMI Fallback'
                        })
                gpu_info['gpus'] = gpus
                gpu_info['source'] = 'WMI Fallback'
            except ImportError:
                gpu_info['gpus'] = [{'name': 'WMI not available', 'note': 'Install pywin32 for detailed GPU info'}]
        
        queue.put({'type': 'result', 'data': gpu_info})
        queue.put({'type': 'done'})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': f'Lỗi thu thập thông tin GPU: {str(e)}'})
        queue.put({'type': 'done'})