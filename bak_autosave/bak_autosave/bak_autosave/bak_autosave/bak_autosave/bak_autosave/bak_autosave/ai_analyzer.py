# ai_analyzer.py
"""
Module AI cho LaptopTester: Phân tích kết quả test, log, dự đoán lỗi, gợi ý sửa chữa.
Có thể mở rộng dùng mô hình ML hoặc API AI bên ngoài.
"""
import os
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import NotFittedError

# Rule-based + ML hybrid
class LaptopAIDiagnoser:
    def __init__(self):
        self.model = None
        self.scaler = None
        self._init_default_model()

    def _init_default_model(self):
        # Dummy model: always predicts 'OK' (0) or 'Lỗi' (1) randomly
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        X = np.array([[50, 60, 70], [90, 95, 100], [30, 40, 50], [99, 99, 99]])
        y = np.array([0, 1, 0, 1])
        self.scaler = StandardScaler().fit(X)
        self.model.fit(self.scaler.transform(X), y)

    def analyze_cpu(self, cpu_result: dict) -> dict:
        # Rule-based: cảnh báo nếu nhiệt độ > 95 hoặc avg_cpu < 50
        max_temp = cpu_result.get('max_temperature', 0)
        avg_cpu = cpu_result.get('avg_cpu_usage', 0)
        if max_temp and max_temp > 95:
            return {'ai_warning': 'Nhiệt độ CPU quá cao, có thể lỗi tản nhiệt hoặc bụi bẩn.'}
        if avg_cpu and avg_cpu < 50:
            return {'ai_warning': 'CPU không đạt hiệu suất mong đợi, kiểm tra lại phần mềm nền.'}
        # ML: dự đoán lỗi dựa trên các chỉ số
        try:
            X = np.array([[avg_cpu, max_temp, cpu_result.get('max_cpu_usage', 0)]])
            X_scaled = self.scaler.transform(X)
            pred = self.model.predict(X_scaled)[0]
            if pred == 1:
                return {'ai_warning': 'AI dự đoán có thể có lỗi CPU hoặc hiệu năng thấp.'}
        except Exception:
            pass
        return {'ai_warning': 'Không phát hiện vấn đề nghiêm trọng.'}

    def analyze_disk(self, disk_result: dict) -> dict:
        # Rule-based: tốc độ ghi/đọc thấp cảnh báo
        try:
            write = float(disk_result.get('write_speed', 0))
            read = float(disk_result.get('read_speed', 0))
            if write < 100 or read < 100:
                return {'ai_warning': 'Tốc độ ổ cứng thấp, kiểm tra sức khỏe SSD/HDD.'}
        except Exception:
            pass
        return {'ai_warning': 'Ổ cứng hoạt động bình thường.'}

    def analyze_battery(self, battery_result: dict) -> dict:
        # Rule-based: health < 70% cảnh báo
        try:
            health = float(battery_result.get('health', 100))
            if health < 70:
                return {'ai_warning': 'Pin đã chai nhiều, nên cân nhắc thay pin.'}
        except Exception:
            pass
        return {'ai_warning': 'Pin ở mức tốt.'}

    def analyze_summary(self, all_results: dict) -> dict:
        # Tổng hợp các cảnh báo AI
        ai_suggestions = []
        if 'CPU' in all_results:
            ai_suggestions.append(self.analyze_cpu(all_results['CPU']))
        if 'Ổ cứng' in all_results:
            ai_suggestions.append(self.analyze_disk(all_results['Ổ cứng']))
        if 'Pin' in all_results:
            ai_suggestions.append(self.analyze_battery(all_results['Pin']))
        # Có thể mở rộng thêm các phân tích khác
        return {'ai_summary': ai_suggestions}

# Singleton cho toàn app
ai_diagnoser = LaptopAIDiagnoser()
