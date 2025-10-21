# Network Test Step - Integration for main_enhanced_auto.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
import subprocess
import socket

try:
    import requests
except ImportError:
    requests = None

class NetworkTestStep:
    """Network and WiFi testing step"""
    
    def __init__(self, master, **kwargs):
        self.master = master
        self.test_results = {}
        self.is_testing = False
        self.record_result = kwargs.get("record_result_callback")
        self.go_to_next_step_callback = kwargs.get("go_to_next_step_callback")
        
    def test_internet_connection(self):
        """Test Internet connectivity"""
        try:
            endpoints = [("Google", "8.8.8.8"), ("Cloudflare", "1.1.1.1")]
            results = []
            for name, ip in endpoints:
                try:
                    socket.create_connection((ip, 53), timeout=3)
                    results.append(f"✅ {name}: OK")
                except:
                    results.append(f"❌ {name}: Failed")
            
            if requests:
                try:
                    response = requests.get("https://www.google.com", timeout=5)
                    results.append("✅ HTTP: OK" if response.status_code == 200 else f"⚠️ HTTP: {response.status_code}")
                except:
                    results.append("❌ HTTP: Failed")
            
            return {"status": "success" if "❌" not in str(results) else "warning", "details": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def test_dns_resolution(self):
        """Test DNS resolution"""
        try:
            domains = ["google.com", "facebook.com", "github.com"]
            results = []
            for domain in domains:
                try:
                    start = time.time()
                    socket.gethostbyname(domain)
                    ms = (time.time() - start) * 1000
                    results.append(f"✅ {domain}: {ms:.1f}ms")
                except:
                    results.append(f"❌ {domain}: Failed")
            return {"status": "success" if "❌" not in str(results) else "error", "details": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def test_network_speed(self):
        """Test network speed"""
        if not requests:
            return {"status": "error", "message": "requests library not available"}
        try:
            url = "https://httpbin.org/bytes/1048576"
            start = time.time()
            response = requests.get(url, timeout=30)
            duration = time.time() - start
            
            if response.status_code == 200:
                size_mb = len(response.content) / (1024 * 1024)
                speed_mbps = (size_mb * 8) / duration
                return {"status": "success", "details": [f"📊 Speed: {speed_mbps:.2f} Mbps", f"⏱️ Time: {duration:.2f}s"]}
            return {"status": "error", "message": "Cannot test speed"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def test_wifi_info(self):
        """Get WiFi information"""
        try:
            import platform
            results = []
            if platform.system() == "Windows":
                try:
                    output = subprocess.check_output('netsh wlan show interfaces', shell=True, text=True)
                    for line in output.split('\n'):
                        if 'SSID' in line and 'BSSID' not in line:
                            results.append(f"🔗 {line.strip()}")
                        elif 'Signal' in line:
                            results.append(f"📡 {line.strip()}")
                except:
                    results.append("⚠️ Cannot get WiFi details")
            else:
                results.append("ℹ️ Windows only")
            return {"status": "success", "details": results if results else ["ℹ️ No WiFi info"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def test_ping_latency(self):
        """Test ping to servers"""
        try:
            servers = [("Google", "8.8.8.8"), ("Cloudflare", "1.1.1.1")]
            results = []
            for name, ip in servers:
                try:
                    cmd = f"ping -n 3 {ip}" if platform.system() == "Windows" else f"ping -c 3 {ip}"
                    output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                    if "Average" in output:
                        for line in output.split('\n'):
                            if 'Average' in line:
                                ping = line.split('=')[1].strip().replace('ms', '')
                                results.append(f"🏓 {name}: {ping}ms")
                                break
                    else:
                        results.append(f"✅ {name}: OK")
                except:
                    results.append(f"❌ {name}: Timeout")
            return {"status": "success", "details": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}
