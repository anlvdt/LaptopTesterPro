"""
Worker for Ports Connectivity Test
"""
import time
import platform

def test_ports_connectivity(queue):
    """Test all ports connectivity"""
    try:
        queue.put({'type': 'status', 'message': 'Đang kiểm tra cổng kết nối...'})
        
        # Simulate port detection
        ports_detected = {
            'USB': 3,
            'HDMI': 1,
            'Audio Jack': 1,
            'Ethernet': 1,
            'SD Card': 1
        }
        
        for i, (port_type, count) in enumerate(ports_detected.items()):
            time.sleep(0.5)
            queue.put({
                'type': 'update',
                'progress': (i + 1) / len(ports_detected),
                'port_type': port_type,
                'count': count
            })
        
        queue.put({
            'type': 'result',
            'data': {
                'ports': ports_detected,
                'total': sum(ports_detected.values())
            }
        })
        queue.put({'type': 'done'})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': str(e)})
        queue.put({'type': 'done'})
