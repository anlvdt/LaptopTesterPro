#!/usr/bin/env python3
"""
Benchmark utilities for LaptopTester Pro
Performance comparison and scoring
"""

import psutil
import platform
import subprocess
import time
import threading
from collections import defaultdict

class BenchmarkDatabase:
    """Database of benchmark scores for comparison"""
    
    def __init__(self):
        # CPU benchmark database (approximate scores)
        self.cpu_scores = {
            # Intel processors
            'i9-12900k': 25000, 'i9-11900k': 22000, 'i9-10900k': 20000,
            'i7-12700k': 22000, 'i7-11700k': 19000, 'i7-10700k': 17000,
            'i5-12600k': 18000, 'i5-11600k': 16000, 'i5-10600k': 14000,
            'i3-12100': 12000, 'i3-11100': 10000, 'i3-10100': 9000,
            
            # AMD processors
            'ryzen 9 5950x': 28000, 'ryzen 9 5900x': 24000,
            'ryzen 7 5800x': 20000, 'ryzen 7 5700x': 18000,
            'ryzen 5 5600x': 16000, 'ryzen 5 5500': 14000,
            'ryzen 3 5300x': 12000,
            
            # Older generations
            'i7-9700k': 15000, 'i5-9600k': 12000, 'i3-9100': 8000,
            'ryzen 7 3700x': 17000, 'ryzen 5 3600': 14000,
        }
        
        # GPU benchmark database (3DMark scores)
        self.gpu_scores = {
            # NVIDIA RTX 40 series
            'rtx 4090': 28000, 'rtx 4080': 24000, 'rtx 4070': 20000,
            'rtx 4060': 16000, 'rtx 4050': 12000,
            
            # NVIDIA RTX 30 series
            'rtx 3090': 26000, 'rtx 3080': 22000, 'rtx 3070': 18000,
            'rtx 3060': 14000, 'rtx 3050': 10000,
            
            # NVIDIA GTX series
            'gtx 1660': 8000, 'gtx 1650': 6000, 'gtx 1050': 4000,
            
            # AMD RX series
            'rx 6800 xt': 20000, 'rx 6700 xt': 16000, 'rx 6600': 12000,
            'rx 5700 xt': 14000, 'rx 5600 xt': 12000,
            
            # Integrated graphics
            'intel uhd': 1000, 'intel iris': 2000, 'amd vega': 2500,
        }
    
    def get_cpu_score(self, cpu_name):
        """Get benchmark score for CPU"""
        cpu_lower = cpu_name.lower()
        
        for cpu_key, score in self.cpu_scores.items():
            if cpu_key in cpu_lower:
                return score
        
        # Estimate based on CPU type
        if 'i9' in cpu_lower:
            return 20000
        elif 'i7' in cpu_lower:
            return 16000
        elif 'i5' in cpu_lower:
            return 12000
        elif 'i3' in cpu_lower:
            return 8000
        elif 'ryzen 9' in cpu_lower:
            return 22000
        elif 'ryzen 7' in cpu_lower:
            return 18000
        elif 'ryzen 5' in cpu_lower:
            return 14000
        elif 'ryzen 3' in cpu_lower:
            return 10000
        else:
            return 6000  # Default for unknown CPUs
    
    def get_gpu_score(self, gpu_name):
        """Get benchmark score for GPU"""
        gpu_lower = gpu_name.lower()
        
        for gpu_key, score in self.gpu_scores.items():
            if gpu_key in gpu_lower:
                return score
        
        # Estimate based on GPU type
        if 'rtx' in gpu_lower:
            if '40' in gpu_lower:
                return 20000
            elif '30' in gpu_lower:
                return 16000
            elif '20' in gpu_lower:
                return 12000
            else:
                return 8000
        elif 'gtx' in gpu_lower:
            return 6000
        elif 'rx' in gpu_lower:
            return 10000
        elif any(integrated in gpu_lower for integrated in ['intel', 'uhd', 'iris', 'vega']):
            return 1500
        else:
            return 3000  # Default for unknown GPUs

class PerformanceAnalyzer:
    """Analyze system performance and provide recommendations"""
    
    def __init__(self):
        self.benchmark_db = BenchmarkDatabase()
    
    def analyze_system_performance(self, cpu_name, gpu_name, ram_gb):
        """Comprehensive system performance analysis"""
        
        # Get benchmark scores
        cpu_score = self.benchmark_db.get_cpu_score(cpu_name)
        gpu_score = self.benchmark_db.get_gpu_score(gpu_name)
        
        # Calculate RAM score
        ram_score = min(ram_gb * 1000, 32000)  # Max 32GB consideration
        
        # Overall system score (weighted average)
        overall_score = (cpu_score * 0.4 + gpu_score * 0.4 + ram_score * 0.2)
        
        # Performance tier classification
        if overall_score >= 20000:
            tier = "High-End Gaming/Workstation"
            tier_color = "success"
        elif overall_score >= 15000:
            tier = "Mid-High Gaming/Creative"
            tier_color = "info"
        elif overall_score >= 10000:
            tier = "Mid-Range Gaming/Office"
            tier_color = "warning"
        elif overall_score >= 6000:
            tier = "Entry Gaming/Office"
            tier_color = "warning"
        else:
            tier = "Basic Office/Web"
            tier_color = "error"
        
        # Usage recommendations
        recommendations = self.get_usage_recommendations(overall_score, cpu_score, gpu_score, ram_gb)
        
        # Bottleneck analysis
        bottlenecks = self.analyze_bottlenecks(cpu_score, gpu_score, ram_gb)
        
        return {
            "overall_score": int(overall_score),
            "cpu_score": cpu_score,
            "gpu_score": gpu_score,
            "ram_score": int(ram_score),
            "tier": tier,
            "tier_color": tier_color,
            "recommendations": recommendations,
            "bottlenecks": bottlenecks
        }
    
    def get_usage_recommendations(self, overall_score, cpu_score, gpu_score, ram_gb):
        """Get usage recommendations based on performance"""
        recommendations = []
        
        # Gaming recommendations
        if gpu_score >= 15000:
            recommendations.append("✅ 1440p Gaming (High-Ultra settings)")
        elif gpu_score >= 10000:
            recommendations.append("✅ 1080p Gaming (High settings)")
        elif gpu_score >= 6000:
            recommendations.append("✅ 1080p Gaming (Medium settings)")
        elif gpu_score >= 3000:
            recommendations.append("⚠️ 1080p Gaming (Low settings)")
        else:
            recommendations.append("❌ Not suitable for modern gaming")
        
        # Creative work recommendations
        if cpu_score >= 18000 and ram_gb >= 16:
            recommendations.append("✅ 4K Video Editing")
        elif cpu_score >= 12000 and ram_gb >= 8:
            recommendations.append("✅ 1080p Video Editing")
        elif cpu_score >= 8000:
            recommendations.append("✅ Photo Editing")
        
        # Programming recommendations
        if cpu_score >= 15000 and ram_gb >= 16:
            recommendations.append("✅ Heavy Development (Docker, VMs)")
        elif cpu_score >= 10000 and ram_gb >= 8:
            recommendations.append("✅ Web Development")
        elif cpu_score >= 6000:
            recommendations.append("✅ Basic Programming")
        
        # Office work
        if overall_score >= 6000:
            recommendations.append("✅ Office Work (Excel, Word, PowerPoint)")
        
        return recommendations
    
    def analyze_bottlenecks(self, cpu_score, gpu_score, ram_gb):
        """Analyze system bottlenecks"""
        bottlenecks = []
        
        # CPU vs GPU balance
        if cpu_score < gpu_score * 0.6:
            bottlenecks.append("🔴 CPU bottleneck - Consider CPU upgrade")
        elif gpu_score < cpu_score * 0.6:
            bottlenecks.append("🔴 GPU bottleneck - Consider GPU upgrade")
        
        # RAM analysis
        if ram_gb < 8:
            bottlenecks.append("🔴 RAM bottleneck - Upgrade to 8GB+ recommended")
        elif ram_gb < 16 and (cpu_score > 15000 or gpu_score > 15000):
            bottlenecks.append("🟡 RAM limitation - 16GB recommended for high-end system")
        
        # Performance balance
        if not bottlenecks:
            bottlenecks.append("✅ Well-balanced system configuration")
        
        return bottlenecks

class RealTimeBenchmark:
    """Real-time performance monitoring and benchmarking"""
    
    def __init__(self):
        self.monitoring = False
        self.data_points = defaultdict(list)
    
    def start_monitoring(self, duration=60, callback=None):
        """Start real-time performance monitoring"""
        self.monitoring = True
        self.data_points.clear()
        
        def monitor_loop():
            start_time = time.time()
            
            while self.monitoring and (time.time() - start_time) < duration:
                # Collect performance data
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Try to get temperature
                temp = self.get_cpu_temperature()
                
                # Try to get frequency
                freq = self.get_cpu_frequency()
                
                timestamp = time.time() - start_time
                
                # Store data
                self.data_points['timestamp'].append(timestamp)
                self.data_points['cpu_percent'].append(cpu_percent)
                self.data_points['memory_percent'].append(memory.percent)
                self.data_points['memory_available'].append(memory.available / (1024**3))  # GB
                
                if temp:
                    self.data_points['temperature'].append(temp)
                
                if freq:
                    self.data_points['frequency'].append(freq)
                
                # Callback for real-time updates
                if callback:
                    callback({
                        'timestamp': timestamp,
                        'cpu_percent': cpu_percent,
                        'memory_percent': memory.percent,
                        'temperature': temp,
                        'frequency': freq
                    })
                
                time.sleep(1)
            
            self.monitoring = False
        
        threading.Thread(target=monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
    
    def get_cpu_temperature(self):
        """Get CPU temperature if available"""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if 'coretemp' in name.lower() or 'cpu' in name.lower():
                            for entry in entries:
                                if entry.current:
                                    return entry.current
            return None
        except:
            return None
    
    def get_cpu_frequency(self):
        """Get current CPU frequency"""
        try:
            freq = psutil.cpu_freq()
            return freq.current if freq else None
        except:
            return None
    
    def get_benchmark_summary(self):
        """Get summary of monitoring session"""
        if not self.data_points['cpu_percent']:
            return None
        
        summary = {
            'duration': max(self.data_points['timestamp']) if self.data_points['timestamp'] else 0,
            'avg_cpu': sum(self.data_points['cpu_percent']) / len(self.data_points['cpu_percent']),
            'max_cpu': max(self.data_points['cpu_percent']),
            'avg_memory': sum(self.data_points['memory_percent']) / len(self.data_points['memory_percent']),
            'max_memory': max(self.data_points['memory_percent']),
        }
        
        if self.data_points['temperature']:
            summary['avg_temp'] = sum(self.data_points['temperature']) / len(self.data_points['temperature'])
            summary['max_temp'] = max(self.data_points['temperature'])
        
        if self.data_points['frequency']:
            summary['avg_freq'] = sum(self.data_points['frequency']) / len(self.data_points['frequency'])
            summary['min_freq'] = min(self.data_points['frequency'])
        
        return summary

def compare_with_market(cpu_name, gpu_name, ram_gb):
    """Compare system with market standards"""
    analyzer = PerformanceAnalyzer()
    analysis = analyzer.analyze_system_performance(cpu_name, gpu_name, ram_gb)
    
    # Market comparison
    current_year = 2024
    
    if analysis['overall_score'] >= 20000:
        market_position = "Top 10% - Flagship performance"
    elif analysis['overall_score'] >= 15000:
        market_position = "Top 25% - High-end performance"
    elif analysis['overall_score'] >= 10000:
        market_position = "Top 50% - Above average performance"
    elif analysis['overall_score'] >= 6000:
        market_position = "Average - Mainstream performance"
    else:
        market_position = "Below average - Entry-level performance"
    
    analysis['market_position'] = market_position
    
    return analysis