import os
import json
import platform
import subprocess
import logging
import importlib.util

logger = logging.getLogger(__name__)

class EnhancedHardwareReader:
    """
    Lớp đọc thông tin phần cứng cải tiến, kết hợp nhiều phương pháp:
    1. LibreHardwareMonitor (LHM) - Độ chính xác cao nhất
    2. WMI (Windows Management Instrumentation) - Backup method
    3. Command line tools (WMIC, PowerShell) - Fallback
    4. Registry reading - Last resort
    """
    
    def __init__(self):
        self.lhm_module = None
        self.lhm_available = False
        self._initialize_lhm()
    
    def _initialize_lhm(self):
        """Khởi tạo LibreHardwareMonitor nếu có"""
        lhm_path = os.path.join(os.path.dirname(__file__), "lhm_reader.py")
        if os.path.exists(lhm_path):
            try:
                spec = importlib.util.spec_from_file_location("lhm_reader", lhm_path)
                self.lhm_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.lhm_module)
                self.lhm_available = True
                logger.info("LibreHardwareMonitor module loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load LHM module: {e}")
                self.lhm_available = False
    
    def get_cpu_info_comprehensive(self):
        """
        Lấy thông tin CPU từ nhiều nguồn và so sánh để đảm bảo độ chính xác
        """
        cpu_info = {
            'name': 'Unknown',
            'cores': 0,
            'threads': 0,
            'base_clock': 0,
            'max_clock': 0,
            'architecture': 'Unknown',
            'manufacturer': 'Unknown',
            'source': 'Unknown'
        }
        
        # Method 1: LibreHardwareMonitor (Highest accuracy)
        if self.lhm_available:
            try:
                lhm_data = self.lhm_module.get_lhm_data()
                if lhm_data:
                    cpu_lhm, _ = self.lhm_module.extract_cpu_gpu_info(lhm_data)
                    if cpu_lhm and any(cpu_lhm.values()):
                        # LHM provides real-time data, extract CPU name from sensors
                        for sensor in lhm_data.get("Sensors", []):
                            if "CPU" in sensor.get("Name", ""):
                                cpu_info['name'] = sensor.get("Name", "").replace("CPU", "").strip()
                                cpu_info['source'] = 'LibreHardwareMonitor'
                                logger.info(f"CPU info from LHM: {cpu_info['name']}")
                                break
            except Exception as e:
                logger.warning(f"LHM CPU detection failed: {e}")
        
        # Method 2: WMI (Windows Management Instrumentation)
        if platform.system() == "Windows" and cpu_info['name'] == 'Unknown':
            try:
                import wmi
                import pythoncom
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    processors = c.Win32_Processor()
                    if processors:
                        cpu = processors[0]
                        cpu_info.update({
                            'name': getattr(cpu, 'Name', 'Unknown').strip(),
                            'cores': getattr(cpu, 'NumberOfCores', 0),
                            'threads': getattr(cpu, 'NumberOfLogicalProcessors', 0),
                            'max_clock': getattr(cpu, 'MaxClockSpeed', 0),
                            'architecture': getattr(cpu, 'Architecture', 'Unknown'),
                            'manufacturer': getattr(cpu, 'Manufacturer', 'Unknown'),
                            'source': 'WMI'
                        })
                        logger.info(f"CPU info from WMI: {cpu_info['name']}")
                finally:
                    pythoncom.CoUninitialize()
            except Exception as e:
                logger.warning(f"WMI CPU detection failed: {e}")
        
        # Method 3: WMIC Command Line
        if cpu_info['name'] == 'Unknown':
            try:
                result = subprocess.run(
                    ['wmic', 'cpu', 'get', 'name,numberofcores,numberoflogicalprocessors,maxclockspeed', '/format:csv'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:]:  # Skip header
                        if line.strip() and ',' in line:
                            parts = line.split(',')
                            if len(parts) >= 5:
                                cpu_info.update({
                                    'name': parts[4].strip() if parts[4].strip() else 'Unknown',
                                    'cores': int(parts[2]) if parts[2].strip().isdigit() else 0,
                                    'threads': int(parts[3]) if parts[3].strip().isdigit() else 0,
                                    'max_clock': int(parts[1]) if parts[1].strip().isdigit() else 0,
                                    'source': 'WMIC'
                                })
                                logger.info(f"CPU info from WMIC: {cpu_info['name']}")
                                break
            except Exception as e:
                logger.warning(f"WMIC CPU detection failed: {e}")
        
        # Method 4: PowerShell (Windows)
        if platform.system() == "Windows" and cpu_info['name'] == 'Unknown':
            try:
                ps_cmd = "Get-WmiObject -Class Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed | ConvertTo-Json"
                result = subprocess.run(
                    ['powershell', '-Command', ps_cmd],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    if isinstance(data, list):
                        data = data[0]
                    cpu_info.update({
                        'name': data.get('Name', 'Unknown').strip(),
                        'cores': data.get('NumberOfCores', 0),
                        'threads': data.get('NumberOfLogicalProcessors', 0),
                        'max_clock': data.get('MaxClockSpeed', 0),
                        'source': 'PowerShell'
                    })
                    logger.info(f"CPU info from PowerShell: {cpu_info['name']}")
            except Exception as e:
                logger.warning(f"PowerShell CPU detection failed: {e}")
        
        # Method 5: cpuinfo library (Cross-platform)
        if cpu_info['name'] == 'Unknown':
            try:
                import cpuinfo
                info = cpuinfo.get_cpu_info()
                cpu_info.update({
                    'name': info.get('brand_raw', 'Unknown'),
                    'cores': info.get('count', 0),
                    'architecture': info.get('arch', 'Unknown'),
                    'source': 'cpuinfo'
                })
                logger.info(f"CPU info from cpuinfo: {cpu_info['name']}")
            except Exception as e:
                logger.warning(f"cpuinfo detection failed: {e}")
        
        return cpu_info
    
    def get_gpu_info_comprehensive(self):
        """
        Lấy thông tin GPU từ nhiều nguồn
        """
        gpu_info = {
            'devices': [],
            'primary': 'Unknown',
            'source': 'Unknown'
        }
        
        # Method 1: LibreHardwareMonitor
        if self.lhm_available:
            try:
                lhm_data = self.lhm_module.get_lhm_data()
                if lhm_data:
                    _, gpu_lhm = self.lhm_module.extract_cpu_gpu_info(lhm_data)
                    if gpu_lhm and any(gpu_lhm.values()):
                        # Extract GPU names from sensors
                        for sensor in lhm_data.get("Sensors", []):
                            sensor_name = sensor.get("Name", "")
                            if any(gpu_keyword in sensor_name for gpu_keyword in ["GPU", "Graphics", "NVIDIA", "AMD", "Intel"]):
                                gpu_name = sensor_name.replace("GPU", "").replace("Graphics", "").strip()
                                if gpu_name and gpu_name not in [g['name'] for g in gpu_info['devices']]:
                                    gpu_info['devices'].append({
                                        'name': gpu_name,
                                        'temperature': gpu_lhm.get('temp'),
                                        'clock': gpu_lhm.get('clock'),
                                        'load': gpu_lhm.get('load')
                                    })
                        if gpu_info['devices']:
                            gpu_info['primary'] = gpu_info['devices'][0]['name']
                            gpu_info['source'] = 'LibreHardwareMonitor'
                            logger.info(f"GPU info from LHM: {len(gpu_info['devices'])} devices")
            except Exception as e:
                logger.warning(f"LHM GPU detection failed: {e}")
        
        # Method 2: WMI
        if platform.system() == "Windows" and not gpu_info['devices']:
            try:
                import wmi
                import pythoncom
                pythoncom.CoInitializeEx(0)
                try:
                    c = wmi.WMI()
                    video_controllers = c.Win32_VideoController()
                    for gpu in video_controllers:
                        gpu_name = getattr(gpu, 'Name', '')
                        if gpu_name and 'Microsoft' not in gpu_name:
                            gpu_info['devices'].append({
                                'name': gpu_name.strip(),
                                'driver_version': getattr(gpu, 'DriverVersion', 'Unknown'),
                                'adapter_ram': getattr(gpu, 'AdapterRAM', 0),
                                'status': getattr(gpu, 'Status', 'Unknown')
                            })
                    if gpu_info['devices']:
                        gpu_info['primary'] = gpu_info['devices'][0]['name']
                        gpu_info['source'] = 'WMI'
                        logger.info(f"GPU info from WMI: {len(gpu_info['devices'])} devices")
                finally:
                    pythoncom.CoUninitialize()
            except Exception as e:
                logger.warning(f"WMI GPU detection failed: {e}")
        
        # Method 3: WMIC
        if not gpu_info['devices']:
            try:
                result = subprocess.run(
                    ['wmic', 'path', 'win32_VideoController', 'get', 'name,driverversion,adapterram', '/format:csv'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:]:  # Skip header
                        if line.strip() and ',' in line:
                            parts = line.split(',')
                            if len(parts) >= 4 and parts[3].strip():
                                gpu_name = parts[3].strip()
                                if 'Microsoft' not in gpu_name:
                                    gpu_info['devices'].append({
                                        'name': gpu_name,
                                        'driver_version': parts[2].strip() if len(parts) > 2 else 'Unknown',
                                        'adapter_ram': parts[1].strip() if len(parts) > 1 else '0'
                                    })
                    if gpu_info['devices']:
                        gpu_info['primary'] = gpu_info['devices'][0]['name']
                        gpu_info['source'] = 'WMIC'
                        logger.info(f"GPU info from WMIC: {len(gpu_info['devices'])} devices")
            except Exception as e:
                logger.warning(f"WMIC GPU detection failed: {e}")
        
        # Method 4: NVIDIA-SMI (for NVIDIA GPUs)
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                nvidia_devices = []
                for line in lines:
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 3:
                            nvidia_devices.append({
                                'name': parts[0],
                                'driver_version': parts[1],
                                'memory_total': f"{parts[2]} MB",
                                'vendor': 'NVIDIA'
                            })
                
                # Merge with existing devices or replace if more detailed
                if nvidia_devices:
                    if not gpu_info['devices']:
                        gpu_info['devices'] = nvidia_devices
                        gpu_info['primary'] = nvidia_devices[0]['name']
                        gpu_info['source'] = 'NVIDIA-SMI'
                    else:
                        # Update existing NVIDIA devices with more details
                        for nvidia_dev in nvidia_devices:
                            for i, existing_dev in enumerate(gpu_info['devices']):
                                if 'NVIDIA' in existing_dev['name'] or 'GeForce' in existing_dev['name'] or 'RTX' in existing_dev['name']:
                                    gpu_info['devices'][i].update(nvidia_dev)
                    logger.info(f"Enhanced GPU info with NVIDIA-SMI: {len(nvidia_devices)} NVIDIA devices")
        except Exception as e:
            logger.debug(f"NVIDIA-SMI not available: {e}")
        
        return gpu_info
    
    def get_comprehensive_hardware_info(self):
        """
        Lấy thông tin phần cứng toàn diện
        """
        return {
            'cpu': self.get_cpu_info_comprehensive(),
            'gpu': self.get_gpu_info_comprehensive(),
            'timestamp': __import__('time').time(),
            'platform': platform.system(),
            'lhm_available': self.lhm_available
        }
    
    def compare_cpu_info(self, bios_cpu, windows_cpu):
        """
        So sánh thông tin CPU từ BIOS và Windows để phát hiện sai lệch
        """
        def normalize_cpu_name(name):
            if not name or name == "Unknown":
                return ""
            name = name.lower().strip()
            # Remove common suffixes and prefixes
            to_remove = ["(r)", "(tm)", "cpu", "@", "ghz", "mhz", "processor", 
                        "with radeon graphics", "with vega graphics", "apu", "mobile"]
            for term in to_remove:
                name = name.replace(term, "")
            return " ".join(name.split())
        
        def extract_cpu_key(normalized_name):
            if not normalized_name:
                return "unknown"
            
            name = normalized_name.lower()
            
            # Intel patterns
            if "intel" in name:
                if "i3" in name: return "intel i3"
                elif "i5" in name: return "intel i5"
                elif "i7" in name: return "intel i7"
                elif "i9" in name: return "intel i9"
                elif "celeron" in name: return "intel celeron"
                elif "pentium" in name: return "intel pentium"
                elif "xeon" in name: return "intel xeon"
                else: return "intel"
            
            # AMD patterns
            elif "amd" in name:
                if "ryzen 3" in name: return "amd ryzen 3"
                elif "ryzen 5" in name: return "amd ryzen 5"
                elif "ryzen 7" in name: return "amd ryzen 7"
                elif "ryzen 9" in name: return "amd ryzen 9"
                elif "ryzen" in name: return "amd ryzen"
                elif "athlon" in name: return "amd athlon"
                elif "fx" in name: return "amd fx"
                else: return "amd"
            
            return "unknown"
        
        # Normalize names
        norm_bios = normalize_cpu_name(bios_cpu)
        norm_windows = normalize_cpu_name(windows_cpu)
        
        # Extract keys
        bios_key = extract_cpu_key(norm_bios)
        windows_key = extract_cpu_key(norm_windows)
        
        # Compare
        exact_match = norm_bios == norm_windows
        contains_match = norm_bios in norm_windows or norm_windows in norm_bios
        key_match = bios_key == windows_key and bios_key != "unknown"
        
        return {
            'match': exact_match or contains_match or key_match,
            'exact_match': exact_match,
            'contains_match': contains_match,
            'key_match': key_match,
            'bios_normalized': norm_bios,
            'windows_normalized': norm_windows,
            'bios_key': bios_key,
            'windows_key': windows_key,
            'confidence': 'high' if exact_match else 'medium' if contains_match or key_match else 'low'
        }

# Singleton instance
hardware_reader = EnhancedHardwareReader()

def get_enhanced_cpu_info():
    """Convenience function to get CPU info"""
    return hardware_reader.get_cpu_info_comprehensive()

def get_enhanced_gpu_info():
    """Convenience function to get GPU info"""
    return hardware_reader.get_gpu_info_comprehensive()

def get_all_hardware_info():
    """Convenience function to get all hardware info"""
    return hardware_reader.get_comprehensive_hardware_info()

if __name__ == "__main__":
    # Test the enhanced hardware reader
    print("Testing Enhanced Hardware Reader...")
    
    cpu_info = get_enhanced_cpu_info()
    print(f"\nCPU Info:")
    print(f"  Name: {cpu_info['name']}")
    print(f"  Cores: {cpu_info['cores']}")
    print(f"  Threads: {cpu_info['threads']}")
    print(f"  Max Clock: {cpu_info['max_clock']} MHz")
    print(f"  Source: {cpu_info['source']}")
    
    gpu_info = get_enhanced_gpu_info()
    print(f"\nGPU Info:")
    print(f"  Primary: {gpu_info['primary']}")
    print(f"  Devices: {len(gpu_info['devices'])}")
    print(f"  Source: {gpu_info['source']}")
    for i, gpu in enumerate(gpu_info['devices']):
        print(f"    GPU {i+1}: {gpu['name']}")
    
    # Test comparison
    comparison = hardware_reader.compare_cpu_info(
        "Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz",
        "Intel Core i7-10750H @ 2.60GHz"
    )
    print(f"\nCPU Comparison Test:")
    print(f"  Match: {comparison['match']}")
    print(f"  Confidence: {comparison['confidence']}")