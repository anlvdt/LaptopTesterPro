import time
import multiprocessing
import math
import psutil
import platform

def cpu_intensive_task():
    """CPU intensive task for stress testing"""
    while True:
        try:
            # Mathematical operations
            for i in range(1000):
                math.sqrt(i * math.pi)
                math.sin(i) * math.cos(i)
                math.factorial(20)
        except:
            pass

def memory_intensive_task(size_mb=100):
    """Memory intensive task"""
    try:
        # Allocate memory chunks
        memory_chunks = []
        chunk_size = 1024 * 1024  # 1MB chunks
        
        for _ in range(size_mb):
            chunk = bytearray(chunk_size)
            # Fill with random-ish data
            for i in range(0, chunk_size, 1024):
                chunk[i:i+1024] = b'x' * 1024
            memory_chunks.append(chunk)
            time.sleep(0.01)  # Small delay to prevent system freeze
        
        # Keep memory allocated for a while
        time.sleep(10)
        
    except MemoryError:
        pass

def run_stress_test(queue, test_type='cpu', duration=60, intensity='medium'):
    """
    Chạy stress test cho CPU và Memory
    
    Args:
        queue: Queue để gửi kết quả
        test_type: 'cpu', 'memory', hoặc 'combined'
        duration: Thời gian chạy test (giây)
        intensity: 'light', 'medium', 'heavy'
    """
    try:
        cpu_count = multiprocessing.cpu_count()
        
        # Xác định số worker processes dựa trên intensity
        if intensity == 'light':
            cpu_workers = max(1, cpu_count // 2)
            memory_size = 50
        elif intensity == 'medium':
            cpu_workers = cpu_count
            memory_size = 100
        else:  # heavy
            cpu_workers = cpu_count * 2
            memory_size = 200
            
        queue.put({
            'type': 'status', 
            'message': f'Bắt đầu {test_type} stress test ({intensity}) với {cpu_workers} workers trong {duration}s'
        })
        
        workers = []
        start_time = time.time()
        
        # Khởi động CPU workers
        if test_type in ['cpu', 'combined']:
            for i in range(cpu_workers):
                worker = multiprocessing.Process(target=cpu_intensive_task)
                worker.daemon = True
                worker.start()
                workers.append(worker)
                
        # Khởi động Memory worker
        if test_type in ['memory', 'combined']:
            memory_worker = multiprocessing.Process(target=memory_intensive_task, args=(memory_size,))
            memory_worker.daemon = True
            memory_worker.start()
            workers.append(memory_worker)
        
        queue.put({'type': 'status', 'message': f'Đã khởi động {len(workers)} worker processes'})
        
        # Theo dõi hiệu suất
        max_cpu = 0
        max_memory = 0
        max_temp = 0
        cpu_readings = []
        memory_readings = []
        temp_readings = []
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            progress = current_time / duration
            
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_readings.append(cpu_usage)
            max_cpu = max(max_cpu, cpu_usage)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            memory_readings.append(memory_usage)
            max_memory = max(max_memory, memory_usage)
            
            # Temperature (nếu có)
            temp = get_cpu_temperature()
            if temp:
                temp_readings.append(temp)
                max_temp = max(max_temp, temp)
                temp_status = f"🌡️ {temp}°C"
            else:
                temp_status = "🌡️ N/A"
            
            # CPU Frequency
            try:
                cpu_freq = psutil.cpu_freq()
                freq_status = f"⚡ {cpu_freq.current:.0f} MHz" if cpu_freq else "⚡ N/A"
            except:
                freq_status = "⚡ N/A"
                
            # Load average (Unix-like systems)
            try:
                load_avg = os.getloadavg()
                load_status = f"📊 Load: {load_avg[0]:.2f}"
            except:
                load_status = "📊 N/A"
            
            status_message = f'CPU: {cpu_usage:.1f}% | RAM: {memory_usage:.1f}% | {temp_status} | {freq_status}'
            
            queue.put({
                'type': 'update',
                'progress': progress,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'temperature': temp,
                'status': status_message
            })
            
            # Cảnh báo nhiệt độ cao
            if temp and temp > 85:
                queue.put({'type': 'warning', 'message': f'⚠️ Nhiệt độ CPU cao: {temp}°C!'})
            
            # Cảnh báo memory cao
            if memory_usage > 90:
                queue.put({'type': 'warning', 'message': f'⚠️ Sử dụng RAM cao: {memory_usage:.1f}%!'})
        
        # Dừng tất cả workers
        for worker in workers:
            try:
                worker.terminate()
                worker.join(timeout=2)
                if worker.is_alive():
                    worker.kill()
            except:
                pass
        
        # Tính toán kết quả
        avg_cpu = sum(cpu_readings) / len(cpu_readings) if cpu_readings else 0
        avg_memory = sum(memory_readings) / len(memory_readings) if memory_readings else 0
        avg_temp = sum(temp_readings) / len(temp_readings) if temp_readings else None
        
        # Đánh giá độ ổn định
        cpu_stable = max_cpu > 70 and max_cpu < 100  # CPU có thể chạy cao nhưng không 100%
        memory_stable = max_memory < 95  # Memory không quá 95%
        temp_stable = max_temp < 90 if max_temp else True  # Nhiệt độ dưới 90°C
        
        overall_stable = cpu_stable and memory_stable and temp_stable
        
        result_data = {
            'test_type': test_type,
            'intensity': intensity,
            'duration': duration,
            'workers_count': len(workers),
            'max_cpu_usage': max_cpu,
            'avg_cpu_usage': avg_cpu,
            'max_memory_usage': max_memory,
            'avg_memory_usage': avg_memory,
            'max_temperature': max_temp,
            'avg_temperature': avg_temp,
            'cpu_stable': cpu_stable,
            'memory_stable': memory_stable,
            'temperature_stable': temp_stable,
            'overall_stable': overall_stable,
            'performance_score': calculate_performance_score(avg_cpu, max_temp, overall_stable)
        }
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})
        
    except Exception as e:
        # Cleanup workers in case of error
        for worker in workers:
            try:
                worker.terminate()
                worker.kill()
            except:
                pass
        queue.put({'type': 'error', 'message': f'Lỗi stress test: {str(e)}'})
        queue.put({'type': 'done'})

def get_cpu_temperature():
    """Lấy nhiệt độ CPU, tương tự như trong worker_cpu.py"""
    if platform.system() == "Windows":
        try:
            import wmi
            w = wmi.WMI(namespace="root\\wmi")
            temp_info = w.MSAcpi_ThermalZoneTemperature()
            if temp_info:
                temp_kelvin = temp_info[0].CurrentTemperature
                temp_celsius = (temp_kelvin / 10) - 273.15
                return int(temp_celsius)
        except:
            pass

    try:
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for key in ['coretemp', 'k10temp', 'acpi', 'cpu_thermal']:
                    if key in temps and temps[key]:
                        return int(temps[key][0].current)
    except:
        pass
    
    return None

def calculate_performance_score(avg_cpu, max_temp, stable):
    """Tính điểm performance dựa trên các thông số"""
    score = 100
    
    # Trừ điểm cho CPU usage thấp (không tải đủ)
    if avg_cpu < 50:
        score -= (50 - avg_cpu) * 0.5
    
    # Trừ điểm cho nhiệt độ cao
    if max_temp and max_temp > 70:
        score -= (max_temp - 70) * 2
    
    # Trừ điểm nếu không stable
    if not stable:
        score -= 20
    
    return max(0, min(100, score))

import os  # Thêm import này cho getloadavg