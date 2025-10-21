import subprocess
import platform
import time
import psutil
import os

def run_hardware_monitor(queue, duration=30):
    """
    Theo dõi phần cứng hệ thống trong thời gian thực
    """
    if platform.system() != "Windows":
        queue.put({'type': 'error', 'message': 'Hardware Monitor chỉ hỗ trợ Windows'})
        queue.put({'type': 'done'})
        return

    try:
        # Kiểm tra LibreHardwareMonitor
        lhm_path = os.path.join(os.path.dirname(__file__), 'bin', 'LibreHardwareMonitor', 'LibreHardwareMonitor.exe')
        
        if not os.path.exists(lhm_path):
            queue.put({'type': 'status', 'message': 'LibreHardwareMonitor không tìm thấy. Sử dụng psutil thay thế...'})
            return run_psutil_monitor(queue, duration)
        
        # Khởi động LibreHardwareMonitor
        queue.put({'type': 'status', 'message': 'Đang khởi động LibreHardwareMonitor...'})
        
        # Chạy LHM ở chế độ minimal
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_MINIMIZE
        
        lhm_process = subprocess.Popen([lhm_path, '/minimized'], startupinfo=startupinfo)
        time.sleep(3)  # Đợi LHM khởi động
        
        queue.put({'type': 'status', 'message': 'Đang thu thập dữ liệu phần cứng...'})
        
        # Theo dõi trong thời gian chỉ định
        start_time = time.time()
        readings = []
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            progress = current_time / duration
            
            # Thu thập dữ liệu cơ bản từ psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            
            # Thông tin network
            network = psutil.net_io_counters()
            
            reading = {
                'timestamp': current_time,
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_read_mb_per_s': (disk_io.read_bytes / (1024**2)) if disk_io else 0,
                'disk_write_mb_per_s': (disk_io.write_bytes / (1024**2)) if disk_io else 0,
                'network_sent_mb': (network.bytes_sent / (1024**2)) if network else 0,
                'network_recv_mb': (network.bytes_recv / (1024**2)) if network else 0
            }
            
            readings.append(reading)
            
            queue.put({
                'type': 'update',
                'progress': progress,
                'cpu': cpu_percent,
                'memory': memory.percent,
                'data': reading
            })
        
        # Đóng LibreHardwareMonitor
        try:
            lhm_process.terminate()
            lhm_process.wait(timeout=5)
        except:
            lhm_process.kill()
        
        # Tính toán kết quả
        if readings:
            avg_cpu = sum(r['cpu_percent'] for r in readings) / len(readings)
            avg_memory = sum(r['memory_percent'] for r in readings) / len(readings)
            max_cpu = max(r['cpu_percent'] for r in readings)
            max_memory = max(r['memory_percent'] for r in readings)
            
            result_data = {
                'duration': duration,
                'readings_count': len(readings),
                'avg_cpu_percent': avg_cpu,
                'avg_memory_percent': avg_memory,
                'max_cpu_percent': max_cpu,
                'max_memory_percent': max_memory,
                'system_stable': max_cpu < 90 and max_memory < 90,
                'readings': readings[-10:]  # Chỉ giữ 10 reading cuối
            }
        else:
            result_data = {'error': 'Không thu thập được dữ liệu'}
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})

    except Exception as e:
        queue.put({'type': 'error', 'message': f'Lỗi Hardware Monitor: {str(e)}'})
        queue.put({'type': 'done'})

def run_psutil_monitor(queue, duration=30):
    """
    Fallback monitor sử dụng chỉ psutil
    """
    try:
        queue.put({'type': 'status', 'message': 'Đang theo dõi hệ thống với psutil...'})
        
        start_time = time.time()
        readings = []
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            progress = current_time / duration
            
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            # Memory info
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk info
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network info
            network = psutil.net_io_counters()
            
            # Temperature (if available)
            temp = None
            try:
                temps = psutil.sensors_temperatures()
                if temps and 'coretemp' in temps:
                    temp = temps['coretemp'][0].current
            except:
                pass
            
            reading = {
                'timestamp': current_time,
                'cpu_percent': cpu_percent,
                'cpu_freq_mhz': cpu_freq.current if cpu_freq else None,
                'cpu_count': cpu_count,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_available_gb': memory.available / (1024**3),
                'swap_percent': swap.percent,
                'disk_usage_percent': (disk_usage.used / disk_usage.total) * 100,
                'disk_read_count': disk_io.read_count if disk_io else 0,
                'disk_write_count': disk_io.write_count if disk_io else 0,
                'network_sent_mb': network.bytes_sent / (1024**2) if network else 0,
                'network_recv_mb': network.bytes_recv / (1024**2) if network else 0,
                'temperature_c': temp
            }
            
            readings.append(reading)
            
            queue.put({
                'type': 'update',
                'progress': progress,
                'cpu': cpu_percent,
                'memory': memory.percent,
                'temperature': temp,
                'data': reading
            })
            
        # Tính toán kết quả
        if readings:
            result_data = {
                'duration': duration,
                'readings_count': len(readings),
                'avg_cpu': sum(r['cpu_percent'] for r in readings) / len(readings),
                'max_cpu': max(r['cpu_percent'] for r in readings),
                'avg_memory': sum(r['memory_percent'] for r in readings) / len(readings),
                'max_memory': max(r['memory_percent'] for r in readings),
                'avg_temp': sum(r['temperature_c'] for r in readings if r['temperature_c']) / len([r for r in readings if r['temperature_c']]) if any(r['temperature_c'] for r in readings) else None,
                'system_health': 'Good' if max(r['cpu_percent'] for r in readings) < 80 and max(r['memory_percent'] for r in readings) < 85 else 'Warning'
            }
        else:
            result_data = {'error': 'Không thu thập được dữ liệu'}
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})

    except Exception as e:
        queue.put({'type': 'error', 'message': f'Lỗi PSUtil Monitor: {str(e)}'})
        queue.put({'type': 'done'})