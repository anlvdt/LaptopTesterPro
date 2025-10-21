"""
bios_detector.py - Enhanced BIOS information detection utility
Provides robust methods to detect BIOS and hardware information with multiple fallback methods
"""

import platform
import subprocess
import os
import time
import logging

try:
    import wmi
    import pythoncom
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

logger = logging.getLogger(__name__)

class BIOSDetector:
    """Enhanced BIOS information detector with multiple fallback methods"""
    
    def __init__(self):
        self.wmi_available = WMI_AVAILABLE and platform.system() == "Windows"
        self.last_error = None
    
    def get_cpu_info(self):
        """Get CPU information using multiple methods"""
        methods = [
            self._get_cpu_wmi,
            self._get_cpu_wmic,
            self._get_cpu_registry,
            self._get_cpu_powershell
        ]
        
        for method in methods:
            try:
                result = method()
                if result and result.strip():
                    logger.info(f"CPU info obtained via {method.__name__}: {result}")
                    return result.strip()
            except Exception as e:
                logger.warning(f"Method {method.__name__} failed: {e}")
                self.last_error = str(e)
                continue
        
        return "Không thể đọc thông tin CPU"
    
    def get_bios_info(self):
        """Get BIOS information using multiple methods"""
        bios_info = {
            'manufacturer': 'N/A',
            'version': 'N/A', 
            'release_date': 'N/A',
            'serial_number': 'N/A'
        }
        
        methods = [
            self._get_bios_wmi,
            self._get_bios_wmic,
            self._get_bios_powershell
        ]
        
        for method in methods:
            try:
                result = method()
                if result:
                    bios_info.update(result)
                    logger.info(f"BIOS info obtained via {method.__name__}")
                    break
            except Exception as e:
                logger.warning(f"BIOS method {method.__name__} failed: {e}")
                continue
        
        return bios_info
    
    def get_system_info(self):
        """Get system information using multiple methods"""
        system_info = {
            'manufacturer': 'N/A',
            'model': 'N/A',
            'serial_number': 'N/A'
        }
        
        methods = [
            self._get_system_wmi,
            self._get_system_wmic,
            self._get_system_powershell
        ]
        
        for method in methods:
            try:
                result = method()
                if result:
                    system_info.update(result)
                    logger.info(f"System info obtained via {method.__name__}")
                    break
            except Exception as e:
                logger.warning(f"System method {method.__name__} failed: {e}")
                continue
        
        return system_info
    
    def _get_cpu_wmi(self):
        """Get CPU info via WMI"""
        if not self.wmi_available:
            raise Exception("WMI not available")
        
        pythoncom.CoInitializeEx(0)
        try:
            c = wmi.WMI()
            processors = c.Win32_Processor()
            if processors and len(processors) > 0:
                cpu = processors[0]
                return getattr(cpu, 'Name', '').strip()
        finally:
            pythoncom.CoUninitialize()
        
        return None
    
    def _get_cpu_wmic(self):
        """Get CPU info via WMIC command"""
        try:
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'name', '/format:value'],
                capture_output=True, text=True, timeout=15, shell=True
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Name='):
                        return line.split('=', 1)[1].strip()
        except Exception as e:
            raise Exception(f"WMIC CPU failed: {e}")
        
        return None
    
    def _get_cpu_registry(self):
        """Get CPU info from Windows Registry"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            winreg.CloseKey(key)
            return cpu_name.strip()
        except Exception as e:
            raise Exception(f"Registry CPU failed: {e}")
    
    def _get_cpu_powershell(self):
        """Get CPU info via PowerShell"""
        try:
            cmd = ['powershell', '-Command', 'Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty Name']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception as e:
            raise Exception(f"PowerShell CPU failed: {e}")
        
        return None
    
    def _get_bios_wmi(self):
        """Get BIOS info via WMI"""
        if not self.wmi_available:
            raise Exception("WMI not available")
        
        pythoncom.CoInitializeEx(0)
        try:
            c = wmi.WMI()
            bios_list = c.Win32_BIOS()
            if bios_list and len(bios_list) > 0:
                bios = bios_list[0]
                
                # Parse BIOS date
                release_date = 'N/A'
                try:
                    bios_date = getattr(bios, 'ReleaseDate', '')
                    if bios_date and len(str(bios_date)) >= 8:
                        bios_date_str = str(bios_date).split('.')[0]
                        if len(bios_date_str) >= 8:
                            release_date = f"{bios_date_str[6:8]}/{bios_date_str[4:6]}/{bios_date_str[:4]}"
                except Exception:
                    pass
                
                return {
                    'manufacturer': getattr(bios, 'Manufacturer', 'N/A'),
                    'version': getattr(bios, 'SMBIOSBIOSVersion', 'N/A'),
                    'release_date': release_date,
                    'serial_number': getattr(bios, 'SerialNumber', 'N/A')
                }
        finally:
            pythoncom.CoUninitialize()
        
        return None
    
    def _get_bios_wmic(self):
        """Get BIOS info via WMIC"""
        try:
            result = subprocess.run(
                ['wmic', 'bios', 'get', 'Manufacturer,SMBIOSBIOSVersion,ReleaseDate,SerialNumber', '/format:csv'],
                capture_output=True, text=True, timeout=15, shell=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:  # Header + data
                    data_line = lines[1].split(',')
                    if len(data_line) >= 4:
                        return {
                            'manufacturer': data_line[1] if len(data_line) > 1 else 'N/A',
                            'version': data_line[4] if len(data_line) > 4 else 'N/A',
                            'release_date': data_line[2] if len(data_line) > 2 else 'N/A',
                            'serial_number': data_line[3] if len(data_line) > 3 else 'N/A'
                        }
        except Exception as e:
            raise Exception(f"WMIC BIOS failed: {e}")
        
        return None
    
    def _get_bios_powershell(self):
        """Get BIOS info via PowerShell"""
        try:
            cmd = ['powershell', '-Command', 
                   'Get-WmiObject -Class Win32_BIOS | Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate,SerialNumber | ConvertTo-Json']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                return {
                    'manufacturer': data.get('Manufacturer', 'N/A'),
                    'version': data.get('SMBIOSBIOSVersion', 'N/A'),
                    'release_date': data.get('ReleaseDate', 'N/A'),
                    'serial_number': data.get('SerialNumber', 'N/A')
                }
        except Exception as e:
            raise Exception(f"PowerShell BIOS failed: {e}")
        
        return None
    
    def _get_system_wmi(self):
        """Get system info via WMI"""
        if not self.wmi_available:
            raise Exception("WMI not available")
        
        pythoncom.CoInitializeEx(0)
        try:
            c = wmi.WMI()
            systems = c.Win32_ComputerSystem()
            if systems and len(systems) > 0:
                system = systems[0]
                return {
                    'manufacturer': getattr(system, 'Manufacturer', 'N/A'),
                    'model': getattr(system, 'Model', 'N/A')
                }
        finally:
            pythoncom.CoUninitialize()
        
        return None
    
    def _get_system_wmic(self):
        """Get system info via WMIC"""
        try:
            result = subprocess.run(
                ['wmic', 'computersystem', 'get', 'Manufacturer,Model', '/format:csv'],
                capture_output=True, text=True, timeout=15, shell=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    data_line = lines[1].split(',')
                    if len(data_line) >= 2:
                        return {
                            'manufacturer': data_line[1] if len(data_line) > 1 else 'N/A',
                            'model': data_line[2] if len(data_line) > 2 else 'N/A'
                        }
        except Exception as e:
            raise Exception(f"WMIC System failed: {e}")
        
        return None
    
    def _get_system_powershell(self):
        """Get system info via PowerShell"""
        try:
            cmd = ['powershell', '-Command', 
                   'Get-WmiObject -Class Win32_ComputerSystem | Select-Object Manufacturer,Model | ConvertTo-Json']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                return {
                    'manufacturer': data.get('Manufacturer', 'N/A'),
                    'model': data.get('Model', 'N/A')
                }
        except Exception as e:
            raise Exception(f"PowerShell System failed: {e}")
        
        return None

# Global instance
bios_detector = BIOSDetector()