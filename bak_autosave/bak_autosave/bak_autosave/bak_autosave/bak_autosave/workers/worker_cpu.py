"""
workers/worker_cpu.py - Worker kiểm tra CPU
"""
import psutil
import time

def cpu_stress_test(duration=10):
    usage = []
    for _ in range(duration):
        usage.append(psutil.cpu_percent(interval=1))
    return {
        "max_cpu_usage": max(usage),
        "avg_cpu_usage": sum(usage)/len(usage),
        "max_temperature": 98  # demo, có thể lấy từ sensors
    }
