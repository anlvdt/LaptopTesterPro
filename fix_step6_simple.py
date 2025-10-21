"""
Fix đơn giản cho bước 6 - đảm bảo lấy được CPU, GPU, RAM
"""

import os
import sys
import platform

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def get_system_info_simple():
    """Lấy thông tin hệ thống đơn giản nhưng chính xác"""
    info = {}
    
    # 1. RAM - luôn hoạt động
    try:
        import psutil
        memory = psutil.virtual_memory()
        ram_gb = round(memory.total / (1024**3), 2)
        info["RAM"] = f"{ram_gb} GB (Tổng cộng)"
        print(f"✓ RAM: {info['RAM']}")
    except Exception as e:
        info["RAM"] = f"Lỗi đọc RAM: {e}"
        print(f"✗ RAM: {info['RAM']}")
    
    # 2. CPU - thử nhiều phương pháp
    info["CPU"] = "Không xác định"
    
    # Phương pháp 1: Enhanced Hardware Reader v2
    try:
        from enhanced_hardware_reader_v2 import hardware_reader
        cpu_info = hardware_reader.get_cpu_info_comprehensive()
        if cpu_info['name'] != 'Unknown':
            cpu_details = cpu_info['name']
            if cpu_info['cores'] > 0:
                cpu_details += f" ({cpu_info['cores']} cores"
                if cpu_info['threads'] > 0:
                    cpu_details += f", {cpu_info['threads']} threads"
                cpu_details += ")"
            if cpu_info['max_clock'] > 0:
                cpu_details += f" @ {cpu_info['max_clock']} MHz"
            cpu_details += f" [Enhanced v2: {cpu_info['source']}]"
            info["CPU"] = cpu_details
            print(f"✓ CPU (Enhanced v2): {info['CPU']}")
        else:
            raise Exception("Enhanced reader returned Unknown")
    except Exception as e:
        print(f"✗ Enhanced CPU detection failed: {e}")
        
        # Phương pháp 2: WMI fallback
        if platform.system() == "Windows":
            try:
                import wmi
                import pythoncom
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    processors = c.Win32_Processor()
                    if processors and len(processors) > 0:
                        cpu_name = getattr(processors[0], 'Name', '').strip()
                        if cpu_name:
                            info["CPU"] = f"{cpu_name} [WMI Fallback]"
                            print(f"✓ CPU (WMI): {info['CPU']}")
                        else:
                            info["CPU"] = "Tên CPU trống"
                    else:
                        info["CPU"] = "Không tìm thấy CPU trong WMI"
                finally:
                    pythoncom.CoUninitialize()
            except Exception as e2:
                info["CPU"] = f"Lỗi WMI CPU: {e2}"
                print(f"✗ WMI CPU: {info['CPU']}")
        else:
            info["CPU"] = "Chỉ hỗ trợ Windows"
    
    # 3. GPU - thử nhiều phương pháp
    info["GPU"] = "Không xác định"
    
    # Phương pháp 1: Enhanced Hardware Reader v2
    try:
        from enhanced_hardware_reader_v2 import hardware_reader
        gpu_info = hardware_reader.get_gpu_info_comprehensive()
        if gpu_info['devices']:
            gpu_details = []
            for i, gpu in enumerate(gpu_info['devices']):
                gpu_detail = f"GPU {i+1}: {gpu['name']}"
                if gpu.get('memory_total'):
                    gpu_detail += f" ({gpu['memory_total']})"
                gpu_details.append(gpu_detail)
            info["GPU"] = "\\n".join(gpu_details) + f" [Enhanced v2: {gpu_info['source']}]"
            print(f"✓ GPU (Enhanced v2): Found {len(gpu_info['devices'])} devices")
        else:
            raise Exception("Enhanced reader returned no GPU devices")
    except Exception as e:
        print(f"✗ Enhanced GPU detection failed: {e}")
        
        # Phương pháp 2: WMI fallback
        if platform.system() == "Windows":
            try:
                import wmi
                import pythoncom
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    gpus = c.Win32_VideoController()
                    gpu_names = []
                    for gpu in gpus:
                        gpu_name = getattr(gpu, 'Name', '')
                        if gpu_name and gpu_name.strip() and 'Microsoft' not in gpu_name:
                            gpu_names.append(gpu_name.strip())
                    if gpu_names:
                        info["GPU"] = "\\n".join(gpu_names) + " [WMI Fallback]"
                        print(f"✓ GPU (WMI): Found {len(gpu_names)} devices")
                    else:
                        info["GPU"] = "Không tìm thấy GPU"
                finally:
                    pythoncom.CoUninitialize()
            except Exception as e2:
                info["GPU"] = f"Lỗi WMI GPU: {e2}"
                print(f"✗ WMI GPU: {info['GPU']}")
        else:
            info["GPU"] = "Chỉ hỗ trợ Windows"
    
    # 4. Ổ cứng
    info["Ổ cứng"] = "Không xác định"
    if platform.system() == "Windows":
        try:
            import wmi
            import pythoncom
            pythoncom.CoInitializeEx(0)
            try:
                c = wmi.WMI()
                drives = c.Win32_DiskDrive()
                disk_details = []
                for drive in drives:
                    try:
                        model = getattr(drive, 'Model', '')
                        size = getattr(drive, 'Size', None)
                        if model and model.strip():
                            if size and str(size).isdigit():
                                size_gb = round(int(size) / (1024**3))
                                disk_details.append(f"- {model.strip()} ({size_gb} GB)")
                            else:
                                disk_details.append(f"- {model.strip()}")
                    except Exception:
                        continue
                info["Ổ cứng"] = "\\n".join(disk_details) if disk_details else "Không tìm thấy ổ cứng"
                print(f"✓ Ổ cứng: Found {len(disk_details)} drives")
            finally:
                pythoncom.CoUninitialize()
        except Exception as e:
            info["Ổ cứng"] = f"Lỗi đọc ổ cứng: {e}"
            print(f"✗ Ổ cứng: {info['Ổ cứng']}")
    else:
        info["Ổ cứng"] = "Chỉ hỗ trợ Windows"
    
    return info

def test_fix():
    """Test fix"""
    print("=" * 60)
    print("TESTING STEP 6 FIX")
    print("=" * 60)
    
    info = get_system_info_simple()
    
    print("\\nKết quả:")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Kiểm tra xem có lấy được thông tin không
    success = True
    if "Lỗi" in info.get("RAM", "") or "Không xác định" in info.get("RAM", ""):
        success = False
        print("\\n✗ RAM detection failed")
    
    if "Không xác định" in info.get("CPU", ""):
        success = False
        print("\\n✗ CPU detection failed")
    
    if "Không xác định" in info.get("GPU", ""):
        success = False
        print("\\n✗ GPU detection failed")
    
    if success:
        print("\\n✓ All hardware detection successful!")
        print("✓ Step 6 should work correctly now")
    else:
        print("\\n✗ Some hardware detection failed")
        print("Please check the error messages above")
    
    return success

if __name__ == "__main__":
    print("Testing Step 6 Fix...")
    success = test_fix()
    
    if success:
        print("\\n" + "=" * 60)
        print("SUCCESS - Step 6 fix is working!")
        print("You can now run main_enhanced.py")
        print("=" * 60)
    else:
        print("\\n" + "=" * 60)
        print("FAILED - Step 6 fix needs more work")
        print("=" * 60)
    
    input("\\nPress Enter to exit...")