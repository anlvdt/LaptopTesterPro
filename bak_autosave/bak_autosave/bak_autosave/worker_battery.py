import subprocess
import platform
import re
import psutil
import time
from bs4 import BeautifulSoup

def get_battery_realtime_info():
    """Lấy thông tin pin thời gian thực"""
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return None
        
        return {
            'percent': battery.percent,
            'plugged': battery.power_plugged,
            'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
        }
    except Exception:
        return None

def analyze_battery_performance(queue):
    """Phân tích hiệu năng pin trong thời gian thực"""
    try:
        queue.put({'type': 'status', 'message': 'Đang phân tích hiệu năng pin...'})
        
        measurements = []
        for i in range(10):  # 10 measurements over 30 seconds
            battery_info = get_battery_realtime_info()
            if battery_info:
                measurements.append({
                    'time': time.time(),
                    'percent': battery_info['percent'],
                    'plugged': battery_info['plugged']
                })
            time.sleep(3)
            queue.put({'type': 'progress', 'value': (i + 1) * 10})
        
        # Analyze discharge rate
        if len(measurements) >= 2:
            first, last = measurements[0], measurements[-1]
            time_diff = last['time'] - first['time']  # seconds
            percent_diff = first['percent'] - last['percent']
            
            if not last['plugged'] and percent_diff > 0:
                discharge_rate = (percent_diff / time_diff) * 3600  # %/hour
                estimated_life = last['percent'] / discharge_rate if discharge_rate > 0 else 999
                
                queue.put({'type': 'battery_performance', 'data': {
                    'discharge_rate': f"{discharge_rate:.2f}%/giờ",
                    'estimated_life': f"{estimated_life:.1f} giờ",
                    'current_percent': last['percent'],
                    'status': 'Đang xả pin' if not last['plugged'] else 'Đang sạc'
                }})
            else:
                queue.put({'type': 'battery_performance', 'data': {
                    'discharge_rate': 'N/A (Đang sạc)',
                    'estimated_life': 'N/A',
                    'current_percent': last['percent'],
                    'status': 'Đang sạc'
                }})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': f'Lỗi phân tích hiệu năng: {str(e)}'})

def run_battery_report(queue, report_path):
    """
    Chạy powercfg, phân tích báo cáo chi tiết và gửi kết quả qua queue.
    """
    if platform.system() != "Windows":
        queue.put({'type': 'error', 'message': 'Chỉ hỗ trợ Windows'})
        queue.put({'type': 'done'})
        return

    try:
        queue.put({'type': 'status', 'message': 'Đang tạo báo cáo pin...'})
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(
            f'powercfg /batteryreport /output "{report_path}" /duration 0',
            check=True, shell=False, capture_output=True, text=False, startupinfo=startupinfo
        )

        queue.put({'type': 'status', 'message': 'Đang phân tích báo cáo...'})
        
        with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')

        def get_info(key_text, is_numeric=False):
            try:
                tag = soup.find(lambda t: t.name == 'td' and key_text in t.text)
                value = tag.find_next_sibling('td').text.strip()
                if is_numeric:
                    return int(re.search(r'[\d,]+', value).group().replace(',', ''))
                return value
            except (AttributeError, ValueError):
                return "N/A"

        # Basic battery info
        data = {
            'name': get_info('NAME'),
            'manufacturer': get_info('MANUFACTURER'),
            'serial_number': get_info('SERIAL NUMBER'),
            'chemistry': get_info('CHEMISTRY'),
            'design_capacity': get_info('DESIGN CAPACITY', is_numeric=True),
            'full_charge_capacity': get_info('FULL CHARGE CAPACITY', is_numeric=True),
            'cycle_count': get_info('CYCLE COUNT', is_numeric=True),
        }

        # Calculate battery health
        if isinstance(data['design_capacity'], int) and isinstance(data['full_charge_capacity'], int) and data['design_capacity'] > 0:
            health = (data['full_charge_capacity'] / data['design_capacity']) * 100
            data['health'] = f"{health:.2f}"
            
            # Determine health status
            if health >= 90:
                data['health_status'] = "Tuyệt vời"
                data['health_color'] = "green"
            elif health >= 80:
                data['health_status'] = "Tốt"
                data['health_color'] = "lightgreen"
            elif health >= 70:
                data['health_status'] = "Khá"
                data['health_color'] = "yellow"
            elif health >= 50:
                data['health_status'] = "Yếu"
                data['health_color'] = "orange"
            else:
                data['health_status'] = "Rất yếu"
                data['health_color'] = "red"
        else:
            data['health'] = "N/A"
            data['health_status'] = "Không xác định"
            data['health_color'] = "gray"
        
        # Get recent usage data
        try:
            usage_table = soup.find('table', id='usage')
            if usage_table:
                rows = usage_table.find_all('tr')[1:6]  # Last 5 entries
                usage_data = []
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        usage_data.append({
                            'date': cells[0].text.strip(),
                            'active_time': cells[1].text.strip(),
                            'discharge': cells[2].text.strip()
                        })
                data['recent_usage'] = usage_data
        except:
            data['recent_usage'] = []
            
        queue.put({'type': 'result', 'data': data})

    except Exception as e:
        queue.put({'type': 'error', 'message': f"Lỗi khi phân tích pin: {e}"})
    finally:
        queue.put({'type': 'done'})