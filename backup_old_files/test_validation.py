#!/usr/bin/env python3
"""
Test Validation Script for LaptopTester Pro
Validates the accuracy and reliability of all test components
"""

import sys
import time
import psutil
import platform
import subprocess
import tempfile
import os
from test_accuracy_fixes import *

class TestValidator:
    def __init__(self):
        self.results = {}
        self.errors = []
        
    def log_result(self, test_name, success, details="", error=""):
        """Log test result"""
        self.results[test_name] = {
            'success': success,
            'details': details,
            'error': error,
            'timestamp': time.time()
        }
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        if error:
            print(f"   Error: {error}")
            self.errors.append(f"{test_name}: {error}")
    
    def validate_cpu_detection(self):
        """Validate CPU detection accuracy"""
        try:
            # Test multiple CPU detection methods
            psutil_cores = psutil.cpu_count(logical=False)
            psutil_threads = psutil.cpu_count(logical=True)
            platform_processor = platform.processor()
            
            # Validate logical consistency
            if psutil_threads < psutil_cores:
                self.log_result("CPU Detection", False, 
                              f"Cores: {psutil_cores}, Threads: {psutil_threads}",
                              "Threads cannot be less than cores")
                return False
            
            # Test CPU frequency detection
            freq_info = psutil.cpu_freq()
            if freq_info and freq_info.current > 0:
                freq_details = f"Current: {freq_info.current}MHz, Max: {freq_info.max}MHz"
            else:
                freq_details = "Frequency detection failed"
            
            self.log_result("CPU Detection", True, 
                          f"Cores: {psutil_cores}, Threads: {psutil_threads}, {freq_details}")
            return True
            
        except Exception as e:
            self.log_result("CPU Detection", False, "", str(e))
            return False
    
    def validate_memory_detection(self):
        """Validate memory detection accuracy"""
        try:
            memory = psutil.virtual_memory()
            
            # Basic sanity checks
            if memory.total < 1024**3:  # Less than 1GB
                self.log_result("Memory Detection", False,
                              f"Total: {memory.total / (1024**3):.2f}GB",
                              "Suspiciously low memory detected")
                return False
            
            if memory.percent > 100:
                self.log_result("Memory Detection", False,
                              f"Usage: {memory.percent}%",
                              "Memory usage over 100%")
                return False
            
            # Test memory consistency
            calculated_used = memory.total - memory.available
            reported_used = memory.used
            
            # Allow 10% variance in memory calculations
            variance = abs(calculated_used - reported_used) / memory.total
            if variance > 0.1:
                self.log_result("Memory Detection", False,
                              f"Total: {memory.total / (1024**3):.2f}GB",
                              f"Memory calculation inconsistency: {variance:.2%}")
                return False
            
            self.log_result("Memory Detection", True,
                          f"Total: {memory.total / (1024**3):.2f}GB, Used: {memory.percent}%")
            return True
            
        except Exception as e:
            self.log_result("Memory Detection", False, "", str(e))
            return False
    
    def validate_disk_detection(self):
        """Validate disk detection accuracy"""
        try:
            partitions = psutil.disk_partitions()
            
            if not partitions:
                self.log_result("Disk Detection", False, "", "No disk partitions found")
                return False
            
            valid_partitions = 0
            total_space = 0
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Sanity checks
                    if usage.total < 1024**2:  # Less than 1MB
                        continue  # Skip very small partitions
                    
                    if usage.used > usage.total:
                        self.log_result("Disk Detection", False,
                                      f"Partition: {partition.device}",
                                      "Used space exceeds total space")
                        return False
                    
                    valid_partitions += 1
                    total_space += usage.total
                    
                except PermissionError:
                    continue  # Skip inaccessible partitions
            
            if valid_partitions == 0:
                self.log_result("Disk Detection", False, "", "No accessible disk partitions")
                return False
            
            self.log_result("Disk Detection", True,
                          f"Found {valid_partitions} partitions, Total: {total_space / (1024**3):.2f}GB")
            return True
            
        except Exception as e:
            self.log_result("Disk Detection", False, "", str(e))
            return False
    
    def validate_temperature_reading(self):
        """Validate temperature sensor accuracy"""
        try:
            temp = get_accurate_cpu_temperature()
            
            if temp is None:
                self.log_result("Temperature Reading", False, "", "No temperature sensors available")
                return False
            
            # Sanity checks for temperature
            if temp < 0 or temp > 150:
                self.log_result("Temperature Reading", False,
                              f"Temperature: {temp}°C",
                              "Temperature outside reasonable range")
                return False
            
            # Test temperature stability (take multiple readings)
            temps = []
            for _ in range(3):
                time.sleep(1)
                t = get_accurate_cpu_temperature()
                if t:
                    temps.append(t)
            
            if len(temps) >= 2:
                temp_variance = max(temps) - min(temps)
                if temp_variance > 20:  # More than 20°C variance in 3 seconds
                    self.log_result("Temperature Reading", False,
                                  f"Temperatures: {temps}",
                                  f"High temperature variance: {temp_variance}°C")
                    return False
            
            self.log_result("Temperature Reading", True,
                          f"Temperature: {temp}°C, Variance: {temp_variance:.1f}°C")
            return True
            
        except Exception as e:
            self.log_result("Temperature Reading", False, "", str(e))
            return False
    
    def validate_battery_detection(self):
        """Validate battery detection accuracy"""
        try:
            battery_info = get_accurate_battery_info()
            
            if 'error' in battery_info:
                # Not an error for desktop systems
                self.log_result("Battery Detection", True, "No battery (desktop system)")
                return True
            
            # Validate battery percentage
            if not (0 <= battery_info['percent'] <= 100):
                self.log_result("Battery Detection", False,
                              f"Charge: {battery_info['percent']}%",
                              "Battery percentage outside valid range")
                return False
            
            # Validate health percentage if available
            if 'health_percent' in battery_info:
                health = battery_info['health_percent']
                if not (0 <= health <= 120):  # Allow up to 120% for new batteries
                    self.log_result("Battery Detection", False,
                                  f"Health: {health}%",
                                  "Battery health outside reasonable range")
                    return False
            
            details = f"Charge: {battery_info['percent']}%"
            if 'health_percent' in battery_info:
                details += f", Health: {battery_info['health_percent']}%"
            
            self.log_result("Battery Detection", True, details)
            return True
            
        except Exception as e:
            self.log_result("Battery Detection", False, "", str(e))
            return False
    
    def validate_stress_test_accuracy(self):
        """Validate stress test measurement accuracy"""
        try:
            # Test CPU usage measurement accuracy
            baseline_cpu = psutil.cpu_percent(interval=1)
            
            # Create light load
            start_time = time.time()
            while time.time() - start_time < 2:
                _ = sum(i * i for i in range(1000))
            
            loaded_cpu = psutil.cpu_percent(interval=1)
            
            # CPU usage should increase under load
            if loaded_cpu <= baseline_cpu:
                self.log_result("Stress Test Accuracy", False,
                              f"Baseline: {baseline_cpu}%, Loaded: {loaded_cpu}%",
                              "CPU usage did not increase under load")
                return False
            
            self.log_result("Stress Test Accuracy", True,
                          f"Baseline: {baseline_cpu}%, Loaded: {loaded_cpu}%")
            return True
            
        except Exception as e:
            self.log_result("Stress Test Accuracy", False, "", str(e))
            return False
    
    def validate_disk_speed_accuracy(self):
        """Validate disk speed test accuracy"""
        try:
            # Create small test file for speed validation
            test_size = 10  # 10MB for quick test
            test_dir = tempfile.gettempdir()
            test_file = os.path.join(test_dir, "speed_validation.tmp")
            
            # Write test
            data = os.urandom(1024 * 1024)  # 1MB of random data
            write_start = time.time()
            
            with open(test_file, "wb") as f:
                for _ in range(test_size):
                    f.write(data)
                f.flush()
                os.fsync(f.fileno())
            
            write_time = time.time() - write_start
            write_speed = test_size / write_time if write_time > 0 else 0
            
            # Read test
            read_start = time.time()
            with open(test_file, "rb") as f:
                while f.read(1024 * 1024):
                    pass
            read_time = time.time() - read_start
            read_speed = test_size / read_time if read_time > 0 else 0
            
            # Cleanup
            os.remove(test_file)
            
            # Validate speeds are reasonable
            if write_speed < 1 or read_speed < 1:  # Less than 1 MB/s
                self.log_result("Disk Speed Accuracy", False,
                              f"Write: {write_speed:.1f}MB/s, Read: {read_speed:.1f}MB/s",
                              "Suspiciously low disk speeds")
                return False
            
            if read_speed < write_speed * 0.5:  # Read much slower than write
                self.log_result("Disk Speed Accuracy", False,
                              f"Write: {write_speed:.1f}MB/s, Read: {read_speed:.1f}MB/s",
                              "Read speed suspiciously slower than write")
                return False
            
            self.log_result("Disk Speed Accuracy", True,
                          f"Write: {write_speed:.1f}MB/s, Read: {read_speed:.1f}MB/s")
            return True
            
        except Exception as e:
            self.log_result("Disk Speed Accuracy", False, "", str(e))
            return False
    
    def validate_system_consistency(self):
        """Validate overall system information consistency"""
        try:
            # Cross-validate system information
            issues = []
            
            # Check OS consistency
            os_name = platform.system()
            os_version = platform.version()
            
            if not os_name or not os_version:
                issues.append("Missing OS information")
            
            # Check architecture consistency
            arch = platform.machine()
            if arch not in ['x86_64', 'AMD64', 'i386', 'i686', 'arm64', 'aarch64']:
                issues.append(f"Unusual architecture: {arch}")
            
            # Check Python version compatibility
            python_version = sys.version_info
            if python_version < (3, 6):
                issues.append(f"Python version too old: {python_version}")
            
            if issues:
                self.log_result("System Consistency", False,
                              f"OS: {os_name} {os_version}, Arch: {arch}",
                              "; ".join(issues))
                return False
            
            self.log_result("System Consistency", True,
                          f"OS: {os_name} {os_version}, Arch: {arch}, Python: {python_version[:2]}")
            return True
            
        except Exception as e:
            self.log_result("System Consistency", False, "", str(e))
            return False
    
    def run_all_validations(self):
        """Run all validation tests"""
        print("🔍 Starting LaptopTester Pro Accuracy Validation...")
        print("=" * 60)
        
        validations = [
            self.validate_cpu_detection,
            self.validate_memory_detection,
            self.validate_disk_detection,
            self.validate_temperature_reading,
            self.validate_battery_detection,
            self.validate_stress_test_accuracy,
            self.validate_disk_speed_accuracy,
            self.validate_system_consistency
        ]
        
        passed = 0
        total = len(validations)
        
        for validation in validations:
            if validation():
                passed += 1
        
        print("=" * 60)
        print(f"📊 Validation Results: {passed}/{total} tests passed")
        
        if self.errors:
            print("\n❌ Errors found:")
            for error in self.errors:
                print(f"   • {error}")
        
        success_rate = (passed / total) * 100
        
        if success_rate >= 90:
            print(f"✅ EXCELLENT: {success_rate:.1f}% accuracy - Tests are highly reliable")
        elif success_rate >= 75:
            print(f"⚠️  GOOD: {success_rate:.1f}% accuracy - Tests are mostly reliable")
        elif success_rate >= 50:
            print(f"⚠️  FAIR: {success_rate:.1f}% accuracy - Some reliability issues")
        else:
            print(f"❌ POOR: {success_rate:.1f}% accuracy - Significant reliability issues")
        
        return success_rate >= 75

if __name__ == "__main__":
    validator = TestValidator()
    success = validator.run_all_validations()
    
    if success:
        print("\n🎉 LaptopTester Pro tests are validated as reliable!")
    else:
        print("\n⚠️  LaptopTester Pro needs accuracy improvements!")
        
    sys.exit(0 if success else 1)