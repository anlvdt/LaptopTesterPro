import time
import math
import multiprocessing
import sys
import platform
import importlib.util
import os
import logging

import psutil

# Cố gắng import WMI, nếu thất bại thì bỏ qua
try:
    if platform.system() == "Windows":
        import wmi
except ImportError:
    wmi = None

# Import enhanced hardware reader
try:
    from enhanced_hardware_reader_v2 import hardware_reader
except ImportError:
    hardware_reader = None

LHM_READER_PATH = os.path.join(os.path.dirname(__file__), "lhm_reader.py")
logger = logging.getLogger(__name__)

def stress_worker():
    """
    Hàm worker để tạo tải tính toán nặng cho một lõi CPU.
    Sử dụng vòng lặp với biến thay đổi để tránh bị trình biên dịch tối ưu hóa.
    """
    x = 0
    while True:
        try:
            x += 0.0001
            math.sqrt(x * math.pi)
        except (OverflowError, ValueError):
            # Reset x nếu nó quá lớn hoặc quá nhỏ
            x = 0
        except Exception:
            # Bỏ qua các lỗi không mong muốn khác và tiếp tục
            pass # pragma: no cover

def get_cpu_temperature():
    """
    Lấy nhiệt độ CPU chính xác hơn.
    1. Ưu tiên WMI trên Windows.
    2. Sau đó là psutil.
       - Với psutil, sẽ lấy nhiệt độ CAO NHẤT từ tất cả các cảm biến CPU.
    3. Sử dụng round() thay vì int() để giữ độ chính xác.
    4. Thêm logging để gỡ lỗi.

    Trả về nhiệt độ Celsius hoặc None nếu không thể đọc.
    """
    # Phương pháp 1: WMI (chỉ dành cho Windows, đáng tin cậy hơn)
    if platform.system() == "Windows" and wmi:
        try:
            w = wmi.WMI(namespace="root\\wmi")
            temp_info = w.MSAcpi_ThermalZoneTemperature()
            if temp_info:
                # Nhiệt độ được trả về ở dạng deci-Kelvin
                temp_kelvin = temp_info[0].CurrentTemperature
                temp_celsius = (temp_kelvin / 10.0) - 273.15
                return round(temp_celsius, 1)
        except Exception as e:
            logger.warning(f"WMI temperature read failed: {e}. Falling back to psutil.")
            pass

    # Phương pháp 2: psutil (đa nền tảng, kém tin cậy hơn)
    try:
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
            
            # Tìm nhiệt độ cao nhất từ tất cả các cảm biến CPU có thể
            cpu_temps = []
            for key in ['coretemp', 'k10temp', 'acpi', 'cpu_thermal']:
                if key in temps:
                    for entry in temps[key]:
                        if entry.current is not None:
                            cpu_temps.append(entry.current)
            
            if cpu_temps:
                # Trả về nhiệt độ cao nhất, làm tròn đến 1 chữ số thập phân
                return round(max(cpu_temps), 1)

    except Exception as e:
        logger.error(f"psutil temperature read failed: {e}")
    
    return None

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
            logger.info("LHM_Manager initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize LHM_Manager: {e}")
            self.lhm_module = None

    def get_stats(self):
        """Lấy thông số CPU từ LibreHardwareMonitor nếu có."""
        if not self.lhm_module:
            return {}
        data = self.lhm_module.get_lhm_data()
        cpu, _ = self.lhm_module.extract_cpu_gpu_info(data)
        return cpu

def run_cpu_stress_test(queue, duration_seconds=60):
    """
    Chạy CPU stress test với monitoring chi tiết.
    """
    try:
        # Thông tin CPU ban đầu
        cpu_count = multiprocessing.cpu_count()
        queue.put({'type': 'status', 'message': f'Phát hiện {cpu_count} lõi CPU. Bắt đầu stress test...'})
        
        # Đo baseline trước khi test
        time.sleep(1)
        baseline_cpu = psutil.cpu_percent(interval=1)
        baseline_temp = get_cpu_temperature()
        
        queue.put({'type': 'baseline', 'data': {
            'cpu_cores': cpu_count,
            'baseline_cpu': baseline_cpu,
            'baseline_temp': baseline_temp
        }})
        
        # Bắt đầu stress workers
        workers = []
        for i in range(cpu_count):
            try:
                worker = multiprocessing.Process(target=stress_worker)
                worker.daemon = True
                worker.start()
                workers.append(worker)
                queue.put({'type': 'worker_started', 'worker_id': i})
            except Exception as e:
                queue.put({'type': 'error', 'message': f'Lỗi khởi động worker {i}: {str(e)}'})
        
        if not workers:
            raise Exception("Không thể khởi động worker processes")
        
        queue.put({'type': 'status', 'message': f'Đã khởi động {len(workers)} processes'})
        
        # Khởi tạo LHM Manager và Enhanced Hardware Reader
        lhm_manager = LHM_Manager()
        
        # Monitoring loop
        start_time = time.time()
        max_temp = 0
        max_cpu_usage = 0
        temp_readings = []
        cpu_readings = []
        
        while time.time() - start_time < duration_seconds:
            current_time = time.time() - start_time
            progress = current_time / duration_seconds
            
            # Đọc CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_readings.append(cpu_usage)
            max_cpu_usage = max(max_cpu_usage, cpu_usage)
            
            # Đọc nhiệt độ, tần số, power từ Enhanced Hardware Reader hoặc LHM
            temp = None
            clock = None
            power = None
            load = None
            
            # Thử Enhanced Hardware Reader trước
            if hardware_reader:
                try:
                    cpu_info = hardware_reader.get_cpu_info_comprehensive()
                    temp = cpu_info.get('temperature')
                    clock = cpu_info.get('current_clock')
                    power = cpu_info.get('power')
                    load = cpu_info.get('load')
                except Exception as e:
                    logger.warning(f"Enhanced hardware reader failed: {e}")
            
            # Fallback to LHM nếu không có dữ liệu
            if temp is None or clock is None:
                lhm_stats = lhm_manager.get_stats()
                if temp is None:
                    temp = lhm_stats.get('temp') or get_cpu_temperature()
                if clock is None:
                    clock = lhm_stats.get('clock')
                if power is None:
                    power = lhm_stats.get('power')
                if load is None:
                    load = lhm_stats.get('load')
            if temp is not None:
                temp_readings.append(temp)
                max_temp = max(max_temp, temp)
                temp_status = f"🌡️ {temp:.1f}°C"
            else:
                temp_status = "🌡️ N/A"
            freq_status = f"⚡ {clock:.0f} MHz" if clock else "⚡ N/A"
            power_status = f"🔋 {power:.1f}W" if power is not None else ""
            
            # Gửi cập nhật
            queue.put({
                'type': 'update',
                'progress': progress,
                'cpu_usage': cpu_usage,
                'temperature': temp,
                'clock': clock,
                'power': power,
                'status': f'CPU: {cpu_usage:.1f}% | {temp_status} | {freq_status} {power_status}'
            })
            
            # Cảnh báo
            if temp and temp > 90:
                queue.put({'type': 'warning', 'message': f'⚠️ Nhiệt độ CPU rất cao: {temp:.1f}°C!'})
            if power and power > 60:
                queue.put({'type': 'warning', 'message': f'⚠️ Công suất CPU cao: {power:.1f}W'})
            if clock and clock < 1000 and cpu_usage > 50:
                queue.put({'type': 'warning', 'message': f'⚠️ CPU có thể đang throttling (xung nhịp thấp khi tải cao)'})

        # Dừng tất cả workers
        for worker in workers:
            worker.terminate()
            worker.join(timeout=1)
        
        # Tính toán kết quả
        avg_cpu = sum(cpu_readings) / len(cpu_readings) if cpu_readings else 0
        avg_temp = sum(temp_readings) / len(temp_readings) if temp_readings else None
        
        result_data = {
            'duration': duration_seconds,
            'cpu_cores': cpu_count,
            'max_cpu_usage': max_cpu_usage,
            'avg_cpu_usage': round(avg_cpu, 2),
            'max_temperature': round(max_temp, 1) if max_temp > 0 else None,
            'avg_temperature': round(avg_temp, 1) if avg_temp is not None else None,
            'stable': max_cpu_usage > 80 and (max_temp < 90 if max_temp else True)
        }
        
        queue.put({'type': 'result', 'data': result_data})
        queue.put({'type': 'done'})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': f'Lỗi CPU stress test: {str(e)}'})
        queue.put({'type': 'done'})