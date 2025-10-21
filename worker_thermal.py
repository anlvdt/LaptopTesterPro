"""
Worker for Thermal Performance Monitoring
"""
import time
import psutil

def monitor_thermal(queue, duration=60):
    """Monitor thermal performance"""
    try:
        queue.put({'type': 'status', 'message': 'Bắt đầu giám sát nhiệt độ...'})
        
        start_time = time.time()
        max_temp = 0
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            progress = elapsed / duration
            
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Simulate temperature (in real app, use WMI or sensors)
            temp = 35 + (cpu_usage / 100) * 40
            max_temp = max(max_temp, temp)
            
            queue.put({
                'type': 'update',
                'progress': progress,
                'cpu_usage': cpu_usage,
                'temperature': temp,
                'max_temp': max_temp
            })
            
            time.sleep(1)
        
        queue.put({
            'type': 'result',
            'data': {
                'max_temperature': max_temp,
                'duration': duration,
                'stable': max_temp < 85
            }
        })
        queue.put({'type': 'done'})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': str(e)})
        queue.put({'type': 'done'})
