"""
Enhanced Hardware Reader v2 - Cải thiện việc đọc thông tin CPU và GPU
Kết hợp nhiều phương pháp để lấy thông tin chính xác nhất
"""

import os
import platform
import subprocess
import json
import logging
import importlib.util
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class EnhancedHardwareReader:
    def __init__(self):
        self.lhm_module = None
        self._initialize_lhm()
        
    def _initialize_lhm(self):
        """Khởi tạo LibreHardwareMonitor module nếu có"""
        lhm_path = os.path.join(os.path.dirname(__file__), "lhm_reader.py")
        if os.path.exists(lhm_path):
            try:
                spec = importlib.util.spec_from_file_location("lhm_reader", lhm_path)
                self.lhm_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.lhm_module)
                logger.info("LHM module initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LHM module: {e}")
                self.lhm_module = None
    
    def get_cpu_info_comprehensive(self) -> Dict[str, Any]:
        """
        Lấy thông tin CPU từ nhiều nguồn và kết hợp để có kết quả chính xác nhất
        """
        cpu_info = {
            'name': 'Unknown',
            'cores': 0,
            'threads': 0,
            'max_clock': 0,
            'current_clock': 0,
            'temperature': None,
            'load': None,
            'power': None,
            'source': 'Unknown',
            'raw_data': {}
        }
        
        methods_tried = []
        
        # Method 1: LibreHardwareMonitor (most accurate for real-time data)
        if self.lhm_module:
            try:
                lhm_data = self.lhm_module.get_lhm_data()
                if lhm_data:
                    cpu_lhm, _ = self.lhm_module.extract_cpu_gpu_info(lhm_data)
                    if cpu_lhm:
                        cpu_info.update({
                            'current_clock': cpu_lhm.get('clock', 0),
                            'temperature': cpu_lhm.get('temp'),
                            'load': cpu_lhm.get('load'),
                            'power': cpu_lhm.get('power'),
                            'source': 'LibreHardwareMonitor'
                        })
                        cpu_info['raw_data']['lhm'] = cpu_lhm
                        methods_tried.append('LHM')
                        logger.info("Got CPU real-time data from LHM")
            except Exception as e:
                logger.warning(f"LHM CPU read failed: {e}")
        
        # Method 2: WMI (Windows Management Instrumentation) - best for static info
        if platform.system() == "Windows":
            try:
                import wmi
                import pythoncom
                pythoncom.CoInitializeEx(0)
                
                try:
                    c = wmi.WMI()
                    processors = c.Win32_Processor()
                    
                    if processors and len(processors) > 0:
                        cpu = processors[0]
                        cpu_name = getattr(cpu, 'Name', '').strip()
                        cores = getattr(cpu, 'NumberOfCores', 0)
                        threads = getattr(cpu, 'NumberOfLogicalProcessors', 0)
                        max_clock = getattr(cpu, 'MaxClockSpeed', 0)
                        
                        if cpu_name and cpu_info['name'] == 'Unknown':
                            cpu_info['name'] = cpu_name
                        if cores > 0:
                            cpu_info['cores'] = cores
                        if threads > 0:
                            cpu_info['threads'] = threads
                        if max_clock > 0:
                            cpu_info['max_clock'] = max_clock
                        
                        if cpu_info['source'] == 'Unknown':
                            cpu_info['source'] = 'WMI'
                        
                        cpu_info['raw_data']['wmi'] = {
                            'name': cpu_name,
                            'cores': cores,
                            'threads': threads,
                            'max_clock': max_clock
                        }
                        methods_tried.append('WMI')
                        logger.info(f"Got CPU static info from WMI: {cpu_name}")
                        
                finally:
                    pythoncom.CoUninitialize()
                    
            except ImportError:
                logger.warning("WMI not available (pywin32 not installed)")
            except Exception as e:
                logger.warning(f"WMI CPU read failed: {e}")
        
        # Method 3: psutil (cross-platform)
        try:
            import psutil
            
            # CPU frequency
            if hasattr(psutil, 'cpu_freq'):
                freq = psutil.cpu_freq()
                if freq and cpu_info['current_clock'] == 0:
                    cpu_info['current_clock'] = freq.current
                if freq and cpu_info['max_clock'] == 0:
                    cpu_info['max_clock'] = freq.max
            
            # CPU count
            if cpu_info['cores'] == 0:
                cpu_info['cores'] = psutil.cpu_count(logical=False) or 0
            if cpu_info['threads'] == 0:
                cpu_info['threads'] = psutil.cpu_count(logical=True) or 0
            
            # CPU load
            if cpu_info['load'] is None:
                cpu_info['load'] = psutil.cpu_percent(interval=0.1)
            
            # Temperature (if available)
            if hasattr(psutil, 'sensors_temperatures') and cpu_info['temperature'] is None:
                temps = psutil.sensors_temperatures()
                if temps:
                    for key in ['coretemp', 'k10temp', 'acpi', 'cpu_thermal']:
                        if key in temps:
                            for entry in temps[key]:
                                if entry.current is not None:
                                    cpu_info['temperature'] = entry.current
                                    break
                            if cpu_info['temperature'] is not None:
                                break
            
            if cpu_info['source'] == 'Unknown':
                cpu_info['source'] = 'psutil'
            
            cpu_info['raw_data']['psutil'] = {
                'cores': psutil.cpu_count(logical=False),
                'threads': psutil.cpu_count(logical=True),
                'load': psutil.cpu_percent(interval=0)
            }
            methods_tried.append('psutil')
            logger.info("Got CPU info from psutil")
            
        except ImportError:
            logger.warning("psutil not available")
        except Exception as e:
            logger.warning(f"psutil CPU read failed: {e}")
        
        # Method 4: cpuinfo library (detailed CPU info)
        try:
            import cpuinfo
            cpu_data = cpuinfo.get_cpu_info()
            
            if cpu_info['name'] == 'Unknown' and 'brand_raw' in cpu_data:
                cpu_info['name'] = cpu_data['brand_raw']
            elif cpu_info['name'] == 'Unknown' and 'brand' in cpu_data:
                cpu_info['name'] = cpu_data['brand']
            
            if cpu_info['max_clock'] == 0 and 'hz_advertised_friendly' in cpu_data:
                # Parse frequency from string like "2.4 GHz"
                freq_str = cpu_data['hz_advertised_friendly']
                try:
                    if 'GHz' in freq_str:
                        freq_val = float(freq_str.replace('GHz', '').strip())
                        cpu_info['max_clock'] = freq_val * 1000  # Convert to MHz
                    elif 'MHz' in freq_str:
                        freq_val = float(freq_str.replace('MHz', '').strip())
                        cpu_info['max_clock'] = freq_val
                except:
                    pass
            
            if cpu_info['source'] == 'Unknown':
                cpu_info['source'] = 'cpuinfo'
            
            cpu_info['raw_data']['cpuinfo'] = cpu_data
            methods_tried.append('cpuinfo')
            logger.info(f"Got CPU info from cpuinfo: {cpu_data.get('brand_raw', 'N/A')}")
            
        except ImportError:
            logger.warning("cpuinfo not available")
        except Exception as e:
            logger.warning(f"cpuinfo CPU read failed: {e}")
        
        # Method 5: Command line fallback (Windows)
        if platform.system() == "Windows" and cpu_info['name'] == 'Unknown':
            try:
                result = subprocess.run(['wmic', 'cpu', 'get', 'name'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and line != 'Name':
                            cpu_info['name'] = line
                            cpu_info['source'] = 'WMIC'
                            methods_tried.append('WMIC')
                            logger.info(f"Got CPU name from WMIC: {line}")
                            break
            except Exception as e:
                logger.warning(f"WMIC CPU read failed: {e}")
        
        # Update source to show combined methods
        if len(methods_tried) > 1:
            cpu_info['source'] = f"Combined ({'+'.join(methods_tried)})"
        
        logger.info(f"CPU info collection complete. Methods: {methods_tried}")
        return cpu_info
    
    def get_gpu_info_comprehensive(self) -> Dict[str, Any]:
        """
        Lấy thông tin GPU từ nhiều nguồn và kết hợp để có kết quả chính xác nhất
        """
        gpu_info = {
            'devices': [],
            'primary_gpu': None,
            'source': 'Unknown',
            'raw_data': {}
        }
        
        methods_tried = []
        
        # Method 1: LibreHardwareMonitor (real-time data)
        if self.lhm_module:
            try:
                lhm_data = self.lhm_module.get_lhm_data()
                if lhm_data:
                    _, gpu_lhm = self.lhm_module.extract_cpu_gpu_info(lhm_data)
                    if gpu_lhm:
                        # Add real-time data to primary GPU if we have devices
                        if gpu_info['devices']:
                            gpu_info['devices'][0].update({
                                'temperature': gpu_lhm.get('temp'),
                                'clock': gpu_lhm.get('clock'),
                                'load': gpu_lhm.get('load'),
                                'power': gpu_lhm.get('power')
                            })
                        gpu_info['raw_data']['lhm'] = gpu_lhm
                        methods_tried.append('LHM')
                        logger.info("Got GPU real-time data from LHM")
            except Exception as e:
                logger.warning(f"LHM GPU read failed: {e}")
        
        # Method 2: WMI (Windows Management Instrumentation)
        if platform.system() == "Windows":
            try:
                import wmi
                import pythoncom
                pythoncom.CoInitializeEx(0)
                
                try:
                    c = wmi.WMI()
                    gpus = c.Win32_VideoController()
                    
                    wmi_devices = []
                    for gpu in gpus:
                        gpu_name = getattr(gpu, 'Name', '')
                        if gpu_name and gpu_name.strip() and 'Microsoft' not in gpu_name:
                            device_info = {
                                'name': gpu_name.strip(),
                                'driver_version': getattr(gpu, 'DriverVersion', ''),
                                'adapter_ram': getattr(gpu, 'AdapterRAM', 0),
                                'status': getattr(gpu, 'Status', ''),
                                'device_id': getattr(gpu, 'DeviceID', ''),
                                'pnp_device_id': getattr(gpu, 'PNPDeviceID', ''),
                                'source': 'WMI'
                            }
                            
                            # Convert adapter RAM to readable format
                            if device_info['adapter_ram'] and str(device_info['adapter_ram']).isdigit():
                                ram_bytes = int(device_info['adapter_ram'])
                                if ram_bytes > 0:
                                    ram_mb = ram_bytes // (1024 * 1024)
                                    if ram_mb > 0:
                                        device_info['memory_total'] = f"{ram_mb} MB"
                            
                            wmi_devices.append(device_info)
                    
                    if wmi_devices:
                        gpu_info['devices'] = wmi_devices
                        gpu_info['primary_gpu'] = wmi_devices[0]
                        gpu_info['source'] = 'WMI'
                        gpu_info['raw_data']['wmi'] = wmi_devices
                        methods_tried.append('WMI')
                        logger.info(f"Got {len(wmi_devices)} GPU(s) from WMI")
                        
                finally:
                    pythoncom.CoUninitialize()
                    
            except ImportError:
                logger.warning("WMI not available (pywin32 not installed)")
            except Exception as e:
                logger.warning(f"WMI GPU read failed: {e}")
        
        # Method 3: nvidia-ml-py (NVIDIA GPUs)
        try:
            import pynvml
            pynvml.nvmlInit()
            
            device_count = pynvml.nvmlDeviceGetCount()
            nvidia_devices = []
            
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                
                # Basic info
                name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
                memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                # Temperature
                try:
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                except:
                    temp = None
                
                # Utilization
                try:
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_util = util.gpu
                    memory_util = util.memory
                except:
                    gpu_util = None
                    memory_util = None
                
                # Clock speeds
                try:
                    graphics_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                    memory_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
                except:
                    graphics_clock = None
                    memory_clock = None
                
                device_info = {
                    'name': name,
                    'memory_total': f"{memory_info.total // (1024**2)} MB",
                    'memory_used': f"{memory_info.used // (1024**2)} MB",
                    'memory_free': f"{memory_info.free // (1024**2)} MB",
                    'temperature': temp,
                    'load': gpu_util,
                    'memory_load': memory_util,
                    'clock': graphics_clock,
                    'memory_clock': memory_clock,
                    'source': 'NVIDIA-ML'
                }
                
                nvidia_devices.append(device_info)
            
            if nvidia_devices:
                # Merge with existing devices or replace
                if not gpu_info['devices']:
                    gpu_info['devices'] = nvidia_devices
                    gpu_info['primary_gpu'] = nvidia_devices[0]
                    gpu_info['source'] = 'NVIDIA-ML'
                else:
                    # Update existing devices with NVIDIA data
                    for i, nvidia_dev in enumerate(nvidia_devices):
                        if i < len(gpu_info['devices']):
                            gpu_info['devices'][i].update(nvidia_dev)
                
                gpu_info['raw_data']['nvidia'] = nvidia_devices
                methods_tried.append('NVIDIA-ML')
                logger.info(f"Got {len(nvidia_devices)} NVIDIA GPU(s)")
            
            pynvml.nvmlShutdown()
            
        except ImportError:
            logger.info("NVIDIA-ML not available (pynvml not installed)")
        except Exception as e:
            logger.warning(f"NVIDIA-ML GPU read failed: {e}")
        
        # Method 4: Command line fallback (Windows)
        if platform.system() == "Windows" and not gpu_info['devices']:
            try:
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    wmic_devices = []
                    for line in lines:
                        line = line.strip()
                        if line and line != 'Name' and 'Microsoft' not in line:
                            device_info = {
                                'name': line,
                                'source': 'WMIC'
                            }
                            wmic_devices.append(device_info)
                    
                    if wmic_devices:
                        gpu_info['devices'] = wmic_devices
                        gpu_info['primary_gpu'] = wmic_devices[0]
                        gpu_info['source'] = 'WMIC'
                        methods_tried.append('WMIC')
                        logger.info(f"Got {len(wmic_devices)} GPU(s) from WMIC")
                        
            except Exception as e:
                logger.warning(f"WMIC GPU read failed: {e}")
        
        # Update source to show combined methods
        if len(methods_tried) > 1:
            gpu_info['source'] = f"Combined ({'+'.join(methods_tried)})"
        
        logger.info(f"GPU info collection complete. Methods: {methods_tried}")
        return gpu_info
    
    def compare_cpu_info(self, cpu1_name: str, cpu2_name: str) -> Dict[str, Any]:
        """
        So sánh thông tin CPU từ hai nguồn khác nhau
        """
        def normalize_cpu_name(name: str) -> str:
            if not name or name == "N/A":
                return ""
            name = name.lower().strip()
            # Remove common suffixes and prefixes
            to_remove = ["(r)", "(tm)", "cpu", "@", "ghz", "mhz", "processor", 
                        "with radeon graphics", "with vega graphics", "apu", "mobile"]
            for term in to_remove: 
                name = name.replace(term, "")
            # Clean up extra spaces
            return " ".join(name.split())
        
        def extract_cpu_key(normalized_name: str) -> str:
            """Extract key CPU identifier like 'intel i5', 'amd ryzen 5', etc."""
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
        norm1 = normalize_cpu_name(cpu1_name)
        norm2 = normalize_cpu_name(cpu2_name)
        
        # Extract keys
        key1 = extract_cpu_key(norm1)
        key2 = extract_cpu_key(norm2)
        
        # Compare
        exact_match = norm1 == norm2
        contains_match = norm1 in norm2 or norm2 in norm1
        key_match = key1 == key2 and key1 != "unknown"
        
        # Calculate confidence
        confidence = 0
        if exact_match:
            confidence = 100
        elif contains_match:
            confidence = 85
        elif key_match:
            confidence = 70
        else:
            confidence = 0
        
        return {
            'match': exact_match or contains_match or key_match,
            'confidence': confidence,
            'bios_normalized': norm1,
            'windows_normalized': norm2,
            'bios_key': key1,
            'windows_key': key2,
            'exact_match': exact_match,
            'contains_match': contains_match,
            'key_match': key_match
        }

# Create global instance
hardware_reader = EnhancedHardwareReader()

# Test function
def test_hardware_reader():
    """Test function to verify hardware reader functionality"""
    print("=== Enhanced Hardware Reader Test ===")
    
    # Test CPU info
    print("\n--- CPU Information ---")
    cpu_info = hardware_reader.get_cpu_info_comprehensive()
    print(f"Name: {cpu_info['name']}")
    print(f"Cores: {cpu_info['cores']}")
    print(f"Threads: {cpu_info['threads']}")
    print(f"Max Clock: {cpu_info['max_clock']} MHz")
    print(f"Current Clock: {cpu_info['current_clock']} MHz")
    print(f"Temperature: {cpu_info['temperature']}°C")
    print(f"Load: {cpu_info['load']}%")
    print(f"Source: {cpu_info['source']}")
    
    # Test GPU info
    print("\n--- GPU Information ---")
    gpu_info = hardware_reader.get_gpu_info_comprehensive()
    print(f"Source: {gpu_info['source']}")
    print(f"Number of devices: {len(gpu_info['devices'])}")
    
    for i, device in enumerate(gpu_info['devices']):
        print(f"\nGPU {i+1}:")
        print(f"  Name: {device['name']}")
        print(f"  Memory: {device.get('memory_total', 'N/A')}")
        print(f"  Temperature: {device.get('temperature', 'N/A')}°C")
        print(f"  Load: {device.get('load', 'N/A')}%")
        print(f"  Clock: {device.get('clock', 'N/A')} MHz")
    
    # Test CPU comparison
    print("\n--- CPU Comparison Test ---")
    test_cpu1 = "Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz"
    test_cpu2 = "Intel Core i7-10750H"
    comparison = hardware_reader.compare_cpu_info(test_cpu1, test_cpu2)
    print(f"CPU1: {test_cpu1}")
    print(f"CPU2: {test_cpu2}")
    print(f"Match: {comparison['match']}")
    print(f"Confidence: {comparison['confidence']}%")
    print(f"Normalized 1: {comparison['bios_normalized']}")
    print(f"Normalized 2: {comparison['windows_normalized']}")

if __name__ == "__main__":
    test_hardware_reader()