import time
import math
import multiprocessing
import psutil
import sys
import platform

# Cố gắng import WMI, nếu thất bại thì bỏ qua
try:
    if platform.system() == "Windows":
        import wmi
except ImportError:
    wmi = None

def stress_worker():
    """Hàm worker để tạo tải tính toán nặng cho một lõi CPU."""
    while True:
        try:
            math.sqrt(999999999 * 999999999)
        except:
            # Bỏ qua mọi lỗi và tiếp tục vòng lặp
            pass

def get_cpu_temperature():
    """
    Lấy nhiệt độ CPU. Ưu tiên WMI trên Windows, sau đó là psutil.
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
                temp_celsius = (temp_kelvin / 10) - 273.15
                return int(temp_celsius)
        except Exception:
            # Nếu WMI thất bại, sẽ chuyển sang psutil
            pass

    # Phương pháp 2: psutil (đa nền tảng, kém tin cậy hơn)
    try:
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
            
            # Các key phổ biến cho cảm biến nhiệt độ CPU
            cpu_keys = ['coretemp', 'k10temp', 'cpu_thermal', 'acpitz', 'cpu-thermal', 'Tctl', 'Tdie']
            for key in cpu_keys:
                if key in temps and temps[key]:
                    # Ưu tiên nhiệt độ 'package' (toàn bộ CPU) nếu có
                    package_temp = next((t.current for t in temps[key] if 'package' in t.label.lower() or t.label == ''), None)
                    if package_temp is not None:
                        return int(package_temp)
                    
                    # Nếu không, lấy nhiệt độ trung bình của các lõi
                    core_temps = [t.current for t in temps[key]]
                    return int(sum(core_temps) / len(core_temps)) if core_temps else None
    except Exception:
        # Bỏ qua mọi lỗi từ psutil
        return None
        
    return None

def run_cpu_stress(duration, queue):
    """
    Chạy bài test stress CPU và gửi cập nhật qua queue.
    :param duration: Thời gian test (giây)
    :param queue: Đối tượng multiprocessing.Queue để giao tiếp
    """
    processes = []
    try:
        num_cores = multiprocessing.cpu_count() or 1
        queue.put({'type': 'status', 'message': f"Bắt đầu stress test trên {num_cores} lõi..."})
        
        # Khởi tạo các tiến trình worker để stress mỗi lõi
        processes = [multiprocessing.Process(target=stress_worker, daemon=True) for _ in range(num_cores)]
        for p in processes:
            p.start()

        # Vòng lặp chính để theo dõi và gửi dữ liệu
        for i in range(duration):
            time.sleep(1)
            temp_val = get_cpu_temperature()
            usage = psutil.cpu_percent(interval=None)
            
            update_data = {
                'type': 'update',
                'progress': (i + 1) / duration,
                'usage': usage,
                'temp': temp_val
            }
            queue.put(update_data)
            
        queue.put({'type': 'status', 'message': "Test hoàn thành."})
        queue.put({'type': 'result', 'status': 'OK'})

    except Exception as e:
        queue.put({'type': 'error', 'message': f"Lỗi trong quá trình test CPU: {e}"})
    finally:
        # Dọn dẹp: dừng tất cả các tiến trình worker
        queue.put({'type': 'status', 'message': "Đang dừng các tiến trình..."})
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=1)
        queue.put({'type': 'done'})