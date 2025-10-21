"""
Fix minimal cho buoc 6 - lay CPU, GPU, RAM
"""

import os
import sys
import platform

sys.path.insert(0, os.path.dirname(__file__))

def get_system_info():
    info = {}
    
    # RAM
    try:
        import psutil
        memory = psutil.virtual_memory()
        ram_gb = round(memory.total / (1024**3), 2)
        info["RAM"] = f"{ram_gb} GB"
        print(f"RAM: {info['RAM']}")
    except Exception as e:
        info["RAM"] = f"Error: {e}"
        print(f"RAM Error: {e}")
    
    # CPU
    try:
        from enhanced_hardware_reader_v2 import hardware_reader
        cpu_info = hardware_reader.get_cpu_info_comprehensive()
        if cpu_info['name'] != 'Unknown':
            info["CPU"] = cpu_info['name']
            print(f"CPU: {info['CPU']}")
        else:
            raise Exception("Unknown CPU")
    except Exception as e:
        print(f"Enhanced CPU failed: {e}")
        try:
            import wmi
            import pythoncom
            pythoncom.CoInitializeEx(0)
            c = wmi.WMI()
            processors = c.Win32_Processor()
            if processors:
                cpu_name = getattr(processors[0], 'Name', '').strip()
                if cpu_name:
                    info["CPU"] = cpu_name
                    print(f"CPU (WMI): {info['CPU']}")
                else:
                    info["CPU"] = "CPU name empty"
            else:
                info["CPU"] = "No CPU found"
            pythoncom.CoUninitialize()
        except Exception as e2:
            info["CPU"] = f"WMI Error: {e2}"
            print(f"WMI CPU Error: {e2}")
    
    # GPU
    try:
        from enhanced_hardware_reader_v2 import hardware_reader
        gpu_info = hardware_reader.get_gpu_info_comprehensive()
        if gpu_info['devices']:
            gpu_names = [gpu['name'] for gpu in gpu_info['devices']]
            info["GPU"] = ", ".join(gpu_names)
            print(f"GPU: {info['GPU']}")
        else:
            raise Exception("No GPU devices")
    except Exception as e:
        print(f"Enhanced GPU failed: {e}")
        try:
            import wmi
            import pythoncom
            pythoncom.CoInitializeEx(0)
            c = wmi.WMI()
            gpus = c.Win32_VideoController()
            gpu_names = []
            for gpu in gpus:
                gpu_name = getattr(gpu, 'Name', '')
                if gpu_name and 'Microsoft' not in gpu_name:
                    gpu_names.append(gpu_name.strip())
            if gpu_names:
                info["GPU"] = ", ".join(gpu_names)
                print(f"GPU (WMI): {info['GPU']}")
            else:
                info["GPU"] = "No GPU found"
            pythoncom.CoUninitialize()
        except Exception as e2:
            info["GPU"] = f"WMI Error: {e2}"
            print(f"WMI GPU Error: {e2}")
    
    return info

if __name__ == "__main__":
    print("Testing Step 6 Hardware Detection...")
    print("=" * 50)
    
    info = get_system_info()
    
    print("\nResults:")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Check success
    success = True
    if "Error" in info.get("RAM", ""):
        success = False
    if "Error" in info.get("CPU", "") or info.get("CPU") == "No CPU found":
        success = False  
    if "Error" in info.get("GPU", "") or info.get("GPU") == "No GPU found":
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: All hardware detected!")
        print("Step 6 should work now")
    else:
        print("FAILED: Some hardware not detected")
    print("=" * 50)
    
    input("\nPress Enter to exit...")