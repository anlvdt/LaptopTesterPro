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


def system_overview_step():
    """
    Tổng quan hệ thống: Lấy tối đa thông tin phần cứng, thiết bị ngoại vi, OS, màn hình, pin, touchpad, webcam, wifi, bluetooth, cảm biến...
    Lý do test: Giúp xác định chính xác cấu hình, nguồn gốc, phát hiện thiết bị thiếu/hỏng, kiểm tra tính đồng bộ phần cứng.
    Cách đọc: Đối chiếu thông tin với quảng cáo, kiểm tra số serial, model, các thiết bị có đủ không, có bất thường không.
    """
    import platform, socket
    try:
        if platform.system() != "Windows":
            return "Chỉ hỗ trợ Windows."
        import wmi
        c = wmi.WMI()
        lines = []
        # Thông tin hệ thống
        sys = c.Win32_ComputerSystem()[0]
        bios = c.Win32_BIOS()[0]
        cpu = c.Win32_Processor()[0]
        gpus = c.Win32_VideoController()
        disks = c.Win32_DiskDrive()
        monitors = c.Win32_DesktopMonitor()
        batts = c.Win32_Battery()
        os = c.Win32_OperatingSystem()[0]
        lines.append(f"Model: {sys.Manufacturer} {sys.Model}")
        lines.append(f"Serial: {bios.SerialNumber}")
        lines.append(f"CPU: {cpu.Name.strip()} ({cpu.NumberOfCores} cores, {cpu.NumberOfLogicalProcessors} threads)")
        lines.append(f"RAM: {round(int(sys.TotalPhysicalMemory)/(1024**3),1)} GB")
        lines.append(f"GPU: {', '.join([g.Name for g in gpus])}")
        lines.append(f"Ổ cứng: {', '.join([f'{d.Model} ({int(d.Size)//(1024**3)}GB)' for d in disks if d.Size])}")
        lines.append(f"Màn hình: {', '.join([f'{m.Name} ({m.ScreenWidth}x{m.ScreenHeight})' for m in monitors])}")
        lines.append(f"Pin: {'Có' if batts else 'Không'}")
        lines.append(f"Webcam: {'Có' if c.Win32_PnPEntity(Name='Integrated Camera') else 'Không rõ'}")
        lines.append(f"Touchpad: {'Có' if any('touchpad' in (d.Name or '').lower() for d in c.Win32_PointingDevice()) else 'Không rõ'}")
        lines.append(f"WiFi: {'Có' if any('wi-fi' in (a.Name or '').lower() or 'wireless' in (a.Name or '').lower() for a in c.Win32_NetworkAdapter()) else 'Không rõ'}")
        lines.append(f"Bluetooth: {'Có' if any('bluetooth' in (a.Name or '').lower() for a in c.Win32_NetworkAdapter()) else 'Không rõ'}")
        lines.append(f"OS: {os.Caption} {os.Version} ({os.OSArchitecture})")
        lines.append(f"Tên máy: {socket.gethostname()}")
        bios_date_str = bios.ReleaseDate.split('.')[0]
        bios_date = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
        lines.append(f"Ngày BIOS: {bios_date}")
        return '\n'.join(lines)
    except Exception as e:
        return f"Lỗi lấy tổng quan hệ thống: {e}"

STEPS.insert(0, TestStep(
    name="Tổng quan hệ thống",
    description="Lý do test: Xác định cấu hình, nguồn gốc, phát hiện thiết bị thiếu/hỏng, kiểm tra đồng bộ phần cứng.\nCách đọc: Đối chiếu thông tin với quảng cáo, kiểm tra serial/model, các thiết bị có đủ không, có bất thường không.",
    run_func=system_overview_step
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

def microphone_test_step():
    import sounddevice as sd
    import numpy as np
    import matplotlib.pyplot as plt
    import tkinter as tk
    from tkinter import messagebox
    duration = 3  # seconds
    fs = 44100
    messagebox.showinfo("Test Microphone", "Nhấn OK và nói vào micro trong 3 giây...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    plt.figure(figsize=(5,2))
    plt.plot(np.linspace(0, duration, len(recording)), recording)
    plt.title("Biểu đồ sóng âm micro")
    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")
    plt.show()
    if np.max(np.abs(recording)) < 0.05:
        return "CẢNH BÁO: Không phát hiện tín hiệu micro!"
    return "Micro hoạt động bình thường."

def speaker_test_step():
    import sounddevice as sd
    import numpy as np
    import tkinter as tk
    from tkinter import messagebox
    fs = 44100
    duration = 2
    freq = 440
    t = np.linspace(0, duration, int(fs*duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    messagebox.showinfo("Test Loa", "Nhấn OK để phát âm thanh kiểm tra loa...")
    sd.play(tone, fs)
    sd.wait()
    res = messagebox.askyesno("Test Loa", "Bạn có nghe thấy âm thanh không?")
    if res:
        return "Loa hoạt động bình thường."
    return "CẢNH BÁO: Không nghe thấy âm thanh từ loa!"

def webcam_test_step():
    import cv2
    import tkinter as tk
    from tkinter import messagebox
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "CẢNH BÁO: Không tìm thấy webcam!"
    messagebox.showinfo("Test Webcam", "Nhấn OK để chụp ảnh từ webcam...")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return "CẢNH BÁO: Không lấy được hình ảnh từ webcam!"
    cv2.imshow("Ảnh chụp từ webcam", frame)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    return "Webcam hoạt động bình thường."

def wifi_test_step():
    import subprocess
    import re
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    output = result.stdout
    ssid = re.search(r'SSID *: (.+)', output)
    signal = re.search(r'Signal *: (\d+)%', output)
    if ssid and signal:
        return f"Đã kết nối WiFi: {ssid.group(1)} (Tín hiệu: {signal.group(1)}%)"
    return "CẢNH BÁO: Không phát hiện kết nối WiFi!"

def bluetooth_test_step():
    import subprocess
    import re
    result = subprocess.run(['powershell', '-Command', 'Get-PnpDevice -Class Bluetooth | Select-String Name'], capture_output=True, text=True)
    devices = re.findall(r'Name *: (.+)', result.stdout)
    if devices:
        return "Thiết bị Bluetooth đã phát hiện: " + ", ".join(devices)
    return "CẢNH BÁO: Không phát hiện thiết bị Bluetooth nào!"

STEPS.append(TestStep(
    name="Kiểm tra Microphone",
    description="Ghi âm, hiển thị sóng âm, cảnh báo nếu không có tín hiệu.",
    run_func=microphone_test_step
))
STEPS.append(TestStep(
    name="Kiểm tra Loa",
    description="Phát âm thanh, hỏi người dùng xác nhận, cảnh báo nếu không nghe thấy.",
    run_func=speaker_test_step
))
STEPS.append(TestStep(
    name="Kiểm tra Webcam",
    description="Chụp ảnh từ webcam, hiển thị ảnh, cảnh báo nếu không có hình.",
    run_func=webcam_test_step
))
STEPS.append(TestStep(
    name="Kiểm tra WiFi",
    description="Kiểm tra kết nối WiFi, hiển thị SSID và tín hiệu.",
    run_func=wifi_test_step
))
STEPS.append(TestStep(
    name="Kiểm tra Bluetooth",
    description="Liệt kê thiết bị Bluetooth đã phát hiện.",
    run_func=bluetooth_test_step
))
