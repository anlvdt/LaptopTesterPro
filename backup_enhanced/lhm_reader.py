import os
import json
import time
import subprocess

def get_lhm_data(timeout=5):
    """Chạy LibreHardwareMonitor.exe --report và đọc dữ liệu JSON nếu có."""
    lhm_dir = os.path.join(os.path.dirname(__file__), "bin", "LibreHardwareMonitor")
    exe_path = os.path.join(lhm_dir, "LibreHardwareMonitor.exe")
    report_path = os.path.join(lhm_dir, "report.json")
    if not os.path.exists(exe_path):
        return None
    # Xóa report cũ
    if os.path.exists(report_path):
        try: os.remove(report_path)
        except: pass
    # Chạy LHM ở chế độ report
    try:
        subprocess.run([exe_path, "--report", report_path], timeout=timeout)
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
    except Exception as e:
        print(f"Lỗi chạy LibreHardwareMonitor: {e}")
    return None

def extract_cpu_gpu_info(lhm_json):
    """Trích xuất thông số CPU/GPU từ JSON của LHM."""
    cpu = {}
    gpu = {}
    if not lhm_json:
        return cpu, gpu
    sensors = lhm_json.get("Sensors", [])
    for s in sensors:
        name = s.get("Name", "")
        typ = s.get("Type", "")
        val = s.get("Value", None)
        if "CPU" in name:
            if typ == "Temperature":
                cpu['temp'] = val
            elif typ == "Clock":
                cpu['clock'] = val
            elif typ == "Power":
                cpu['power'] = val
            elif typ == "Load":
                cpu['load'] = val
        if "GPU" in name or "Graphics" in name:
            if typ == "Temperature":
                gpu['temp'] = val
            elif typ == "Clock":
                gpu['clock'] = val
            elif typ == "Power":
                gpu['power'] = val
            elif typ == "Load":
                gpu['load'] = val
    return cpu, gpu

if __name__ == "__main__":
    data = get_lhm_data()
    cpu, gpu = extract_cpu_gpu_info(data)
    print("CPU:", cpu)
    print("GPU:", gpu)
