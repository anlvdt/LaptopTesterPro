"""
steps.py - Định nghĩa các bước kiểm tra phần cứng cho LaptopTester
"""
from typing import Callable
import platform
import wmi
import psutil

class TestStep:
    def __init__(self, name: str, description: str, run_func: Callable):
        self.name = name
        self.description = description
        self.run_func = run_func
    def run(self):
        return self.run_func()

# Danh sách các bước sẽ được bổ sung tự động
STEPS = []

def hardware_id_step():
    import platform
    try:
        if platform.system() != "Windows":
            return "Chỉ hỗ trợ Windows."
        import wmi
        c = wmi.WMI()
        system_info = c.Win32_ComputerSystem()[0]
        bios = c.Win32_BIOS()[0]
        cpu = c.Win32_Processor()[0].Name.strip()
        gpus = ", ".join([gpu.Name for gpu in c.Win32_VideoController()])
        disks = ", ".join([d.Model for d in c.Win32_DiskDrive()])
        bios_date_str = bios.ReleaseDate.split('.')[0]
        bios_date = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
        info = (
            f"Model: {system_info.Manufacturer} {system_info.Model}\n"
            f"Serial: {bios.SerialNumber}\n"
            f"CPU: {cpu}\n"
            f"GPU: {gpus}\n"
            f"Ổ cứng: {disks}\n"
            f"Ngày BIOS: {bios_date}"
        )
        return info
    except Exception as e:
        return f"Lỗi lấy thông tin phần cứng: {e}"

STEPS.append(TestStep(
    name="Định danh phần cứng",
    description="Đọc thông tin model, serial, BIOS, CPU, GPU, ổ cứng từ hệ thống.",
    run_func=hardware_id_step
))

def windows_config_step():
    import platform
    import psutil
    try:
        cpu = psutil.cpu_freq()
        cpu_name = platform.processor()
        ram = round(psutil.virtual_memory().total / (1024**3), 2)
        gpus = "Không hỗ trợ trên mọi máy"
        try:
            import wmi
            c = wmi.WMI()
            gpus = ", ".join([gpu.Name for gpu in c.Win32_VideoController()])
            disks = ", ".join([f"{d.Model} ({int(d.Size)//(1024**3)}GB)" for d in c.Win32_DiskDrive() if d.Size])
        except Exception:
            disks = ", ".join([d.device for d in psutil.disk_partitions()])
        os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
        return f"CPU: {cpu_name} ({cpu.current if cpu else 'N/A'} MHz)\nRAM: {ram} GB\nGPU: {gpus}\nDisks: {disks}\nOS: {os_info}"
    except Exception as e:
        return f"Lỗi lấy cấu hình: {e}"

STEPS.append(TestStep(
    name="Cấu hình Windows",
    description="Đọc cấu hình CPU, RAM, GPU, ổ cứng, hệ điều hành từ Windows.",
    run_func=windows_config_step
))

def disk_health_step():
    try:
        import wmi
        c = wmi.WMI()
        drives = c.Win32_DiskDrive()
        if not drives:
            return "Không tìm thấy ổ cứng."
        result = ""
        for d in drives:
            status = d.Status
            model = d.Model
            serial = getattr(d, 'SerialNumber', 'N/A')
            size = int(d.Size)//(1024**3) if d.Size else 'N/A'
            result += f"Model: {model}\nSerial: {serial}\nDung lượng: {size} GB\nTrạng thái: {status}\n---\n"
        return result
    except Exception as e:
        return f"Lỗi đọc S.M.A.R.T: {e}"

STEPS.append(TestStep(
    name="Sức khỏe ổ cứng",
    description="Đọc trạng thái S.M.A.R.T, model, serial, dung lượng từng ổ cứng.",
    run_func=disk_health_step
))

def disk_speed_step():
    import tempfile, os, time
    import psutil
    try:
        test_dir = tempfile.gettempdir()
        file_size_mb = 128
        file_size_bytes = file_size_mb * 1024 * 1024
        chunk_size = 4 * 1024 * 1024
        chunks = file_size_bytes // chunk_size
        test_file_path = os.path.join(test_dir, f"laptoptester_speedtest.tmp")
        data_chunk = os.urandom(chunk_size)
        # Write
        write_start = time.time()
        with open(test_file_path, "wb") as f:
            for _ in range(chunks):
                f.write(data_chunk)
        write_time = time.time() - write_start
        write_speed = file_size_mb / write_time if write_time > 0 else 0
        # Read
        read_start = time.time()
        with open(test_file_path, "rb") as f:
            while f.read(chunk_size):
                pass
        read_time = time.time() - read_start
        read_speed = file_size_mb / read_time if read_time > 0 else 0
        os.remove(test_file_path)
        return f"Ghi: {write_speed:.1f} MB/s, Đọc: {read_speed:.1f} MB/s"
    except Exception as e:
        return f"Lỗi đo tốc độ ổ cứng: {e}"

STEPS.append(TestStep(
    name="Tốc độ ổ cứng",
    description="Đo tốc độ đọc/ghi thực tế của ổ cứng.",
    run_func=disk_speed_step
))

def cpu_stress_step():
    import time, psutil, platform
    import matplotlib.pyplot as plt
    import numpy as np
    import tempfile, os
    usage = []
    for _ in range(10):
        usage.append(psutil.cpu_percent(interval=0.5))
    avg = sum(usage)/len(usage)
    cpu_name = platform.processor()
    cpu_freq = psutil.cpu_freq()
    cpu_count = psutil.cpu_count(logical=True)
    temp = 'N/A'
    try:
        import wmi
        c = wmi.WMI(namespace="root\\wmi")
        temps = c.MSAcpi_ThermalZoneTemperature()
        if temps:
            temp = round(temps[0].CurrentTemperature/10-273.15, 1)
    except Exception:
        pass
    # Vẽ biểu đồ tải CPU
    fig, ax = plt.subplots()
    ax.plot(np.arange(len(usage)), usage, marker='o')
    ax.set_title('Biểu đồ tải CPU')
    ax.set_xlabel('Lần đo')
    ax.set_ylabel('Tải (%)')
    temp_img = os.path.join(tempfile.gettempdir(), 'cpu_chart.png')
    fig.savefig(temp_img)
    plt.close(fig)
    result = f"CPU: {cpu_name}\nSố luồng: {cpu_count}\nXung nhịp: {cpu_freq.current if cpu_freq else 'N/A'} MHz\nTải trung bình: {avg:.1f}%\nNhiệt độ: {temp}°C\nBiểu đồ tải CPU đã lưu: {temp_img}"
    if temp != 'N/A' and isinstance(temp, (int, float)) and temp > 90:
        result += "\nCẢNH BÁO: CPU QUÁ NÓNG!"
    return result

STEPS.append(TestStep(
    name="Kiểm tra CPU",
    description="Đẩy CPU lên tải cao, đo hiệu năng, nhiệt độ, số luồng, xung nhịp, vẽ biểu đồ tải.",
    run_func=cpu_stress_step
))

def battery_step():
    import psutil
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return "Không tìm thấy pin."
        percent = battery.percent
        plugged = battery.power_plugged
        secsleft = battery.secsleft
        if secsleft == psutil.POWER_TIME_UNLIMITED:
            time_left = "Không xác định"
        elif secsleft == psutil.POWER_TIME_UNKNOWN:
            time_left = "Không rõ"
        else:
            hours = secsleft // 3600
            minutes = (secsleft % 3600) // 60
            time_left = f"{hours}h{minutes}m"
        return f"Pin: {percent}% - {'Đang sạc' if plugged else 'Đang xả'}\nThời gian còn lại: {time_left}"
    except Exception as e:
        return f"Lỗi kiểm tra pin: {e}"

STEPS.append(TestStep(
    name="Kiểm tra pin",
    description="Đọc trạng thái pin, phần trăm, thời gian còn lại từ hệ thống.",
    run_func=battery_step
))

def screen_test_step():
    return (
        "1. Quan sát màn hình ở nền trắng, đen, đỏ, xanh lá, xanh dương để phát hiện điểm chết, ám màu, hở sáng.\n"
        "2. Có thể truy cập https://www.eizo.be/monitor-test/ để test online nâng cao.\n"
        "3. Đổi độ sáng, tần số quét để kiểm tra thêm."
    )

STEPS.append(TestStep(
    name="Kiểm tra màn hình",
    description="Hướng dẫn kiểm tra điểm chết, ám màu, hở sáng, test online.",
    run_func=screen_test_step
))

def keyboard_test_step():
    import tkinter as tk
    from tkinter import simpledialog
    root = tk.Tk()
    root.withdraw()
    msg = (
        "Hãy gõ thử tất cả các phím trên bàn phím. Nếu phát hiện phím không hoạt động, hãy ghi chú lại.\n"
        "Bạn có thể dùng https://keyboard-test.space/ để kiểm tra online.\n"
        "Sau khi kiểm tra, nhập tên các phím liệt (nếu có, cách nhau bởi dấu phẩy):"
    )
    result = simpledialog.askstring("Test bàn phím", msg)
    if result:
        return f"Các phím liệt: {result}"
    return "Không phát hiện phím liệt."

STEPS.append(TestStep(
    name="Kiểm tra bàn phím",
    description="Kiểm tra phím cứng, hướng dẫn test online, nhập phím liệt nếu có.",
    run_func=keyboard_test_step
))

def physical_inspect_step():
    return (
        "1. Kiểm tra vỏ máy, bản lề, ốc vít, cổng kết nối.\n"
        "2. Quan sát dấu hiệu rơi móp, nứt, trầy xước.\n"
        "3. Kiểm tra bản lề có lỏng, phát ra tiếng kêu lạ không."
    )

STEPS.append(TestStep(
    name="Kiểm tra ngoại hình",
    description="Hướng dẫn kiểm tra vật lý tổng thể laptop.",
    run_func=physical_inspect_step
))

def bios_check_step():
    return (
        "1. Khởi động vào BIOS (F2, DEL, F10, F12 tùy máy).\n"
        "2. Kiểm tra các mục: Computrace/Absolute Persistence, mật khẩu lạ, XMP/DOCP, Turbo Boost.\n"
        "3. Đảm bảo không có mục bảo mật bất thường, không bị khóa từ xa."
    )

STEPS.append(TestStep(
    name="Kiểm tra BIOS",
    description="Hướng dẫn kiểm tra các cài đặt BIOS quan trọng, bảo mật, hiệu năng.",
    run_func=bios_check_step
))

def summary_step():
    return (
        "Tổng kết toàn bộ các bước kiểm tra.\n"
        "- Nên lưu lại kết quả từng bước.\n"
        "- Có thể xuất báo cáo hoặc chụp màn hình.\n"
        "- Đọc kỹ đánh giá AI để phát hiện bất thường tiềm ẩn."
    )

STEPS.append(TestStep(
    name="Tổng kết",
    description="Tổng hợp kết quả, nhắc xuất báo cáo, lưu ý AI.",
    run_func=summary_step
))

def gpu_test_step():
    try:
        import wmi
        import pygame
        import time
        c = wmi.WMI()
        gpus = [gpu for gpu in c.Win32_VideoController() if 'Microsoft' not in gpu.Name]
        if not gpus:
            return "Không phát hiện GPU rời."
        info = "\n".join([f"{gpu.Name} - VRAM: {int(getattr(gpu, 'AdapterRAM', 0))//(1024**2)} MB" for gpu in gpus])
        # Đo FPS cơ bản bằng pygame
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        clock = pygame.time.Clock()
        fps_list = []
        start = time.time()
        while time.time() - start < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "Đã thoát test GPU."
            screen.fill((0,0,0))
            pygame.draw.circle(screen, (255,0,0), (320,240), 100)
            pygame.display.flip()
            fps = clock.get_fps()
            if fps > 0:
                fps_list.append(fps)
            clock.tick(60)
        pygame.quit()
        avg_fps = sum(fps_list)/len(fps_list) if fps_list else 0
        return f"GPU phát hiện: {info}\nFPS trung bình (test đơn giản): {avg_fps:.1f}"
    except Exception as e:
        return f"Lỗi kiểm tra GPU: {e}"

STEPS.insert(5, TestStep(
    name="Kiểm tra GPU",
    description="Kiểm tra card đồ họa, đo FPS cơ bản, cảnh báo nếu không có GPU rời.",
    run_func=gpu_test_step
))
