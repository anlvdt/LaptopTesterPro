#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update individual test mode with all tests and proper translations"""

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update all_tests list with complete tests and proper descriptions
old_tests = '''        # All available tests
        all_tests = [
            (get_text("hardware_fingerprint"), HardwareFingerprintStep, "🔍", "Kiểm tra thông tin phần cứng từ BIOS"),

            (get_text("license_check"), LicenseCheckStep, "🔑", "Kiểm tra bản quyền Windows"),
            (get_text("system_info"), SystemInfoStep, "💻", "Thông tin cấu hình hệ thống"),
            (get_text("harddrive_health"), HardDriveHealthStep, "💿", "Sức khỏe ổ cứng (S.M.A.R.T)"),

            (get_text("screen_test"), ScreenTestStep, "🖥️", "Kiểm tra màn hình"),
            (get_text("keyboard_test"), KeyboardTestStep, "⌨️", "Bàn phím & Touchpad"),
            (get_text("battery_health"), BatteryHealthStep, "🔋", "Sức khỏe pin"),

            (get_text("audio_test"), AudioTestStep, "🔊", "Loa & Micro"),
            (get_text("webcam_test"), WebcamTestStep, "📷", "Webcam"),

            (get_text("network_test"), NetworkTestStep, "🌐", "Kết nối mạng"),
            (get_text("cpu_stress"), CPUStressTestStep, "🔥", "CPU Stress Test"),
            (get_text("gpu_stress"), GPUStressTestStep, "🎮", "GPU Stress Test"),

            (get_text("harddrive_speed"), HardDriveSpeedStep, "⚡", "Tốc độ ổ cứng"),
            (get_text("thermal_test"), ThermalMonitorStep, "🌡️", "Nhiệt độ & Hiệu năng"),

        ]'''

new_tests = '''        # All available tests with translations
        if CURRENT_LANG == "vi":
            all_tests = [
                (get_text("hardware_fingerprint"), HardwareFingerprintStep, "🔍", "Định danh phần cứng từ BIOS"),
                (get_text("license_check"), LicenseCheckStep, "🔑", "Kiểm tra bản quyền Windows"),
                (get_text("system_info"), SystemInfoStep, "💻", "Thông tin cấu hình hệ thống"),
                (get_text("harddrive_health"), HardDriveHealthStep, "💿", "Sức khỏe ổ cứng (S.M.A.R.T)"),
                (get_text("screen_test"), ScreenTestStep, "🖥️", "Kiểm tra màn hình"),
                (get_text("keyboard_test"), KeyboardTestStep, "⌨️", "Bàn phím & Touchpad"),
                ("Kiểm Tra Ngoại Hình", PhysicalInspectionStep, "👁️", "Kiểm tra vỏ máy, bản lề, cổng"),
                ("Kiểm Tra BIOS", BIOSCheckStep, "⚙️", "Cài đặt BIOS và bảo mật"),
                (get_text("battery_health"), BatteryHealthStep, "🔋", "Sức khỏe pin và dung lượng"),
                (get_text("audio_test"), AudioTestStep, "🔊", "Loa & Micro"),
                (get_text("webcam_test"), WebcamTestStep, "📷", "Webcam"),
                (get_text("network_test"), NetworkTestStep, "🌐", "Kết nối mạng & WiFi"),
                (get_text("cpu_stress"), CPUStressTestStep, "🔥", "CPU Stress Test"),
                (get_text("gpu_stress"), GPUStressTestStep, "🎮", "GPU Stress Test"),
                (get_text("harddrive_speed"), HardDriveSpeedStep, "⚡", "Tốc độ đọc/ghi ổ cứng"),
                ("Thermal Monitor", ThermalMonitorStep, "🌡️", "Giám sát nhiệt độ CPU/RAM"),
                ("System Stability", SystemStabilityStep, "🔥", "Test ổn định tổng hợp"),
            ]
        else:
            all_tests = [
                (get_text("hardware_fingerprint"), HardwareFingerprintStep, "🔍", "Hardware fingerprint from BIOS"),
                (get_text("license_check"), LicenseCheckStep, "🔑", "Windows license check"),
                (get_text("system_info"), SystemInfoStep, "💻", "System configuration info"),
                (get_text("harddrive_health"), HardDriveHealthStep, "💿", "Hard drive health (S.M.A.R.T)"),
                (get_text("screen_test"), ScreenTestStep, "🖥️", "Screen test"),
                (get_text("keyboard_test"), KeyboardTestStep, "⌨️", "Keyboard & Touchpad"),
                ("Physical Inspection", PhysicalInspectionStep, "👁️", "Check case, hinges, ports"),
                ("BIOS Check", BIOSCheckStep, "⚙️", "BIOS settings and security"),
                (get_text("battery_health"), BatteryHealthStep, "🔋", "Battery health and capacity"),
                (get_text("audio_test"), AudioTestStep, "🔊", "Speakers & Microphone"),
                (get_text("webcam_test"), WebcamTestStep, "📷", "Webcam"),
                (get_text("network_test"), NetworkTestStep, "🌐", "Network & WiFi connection"),
                (get_text("cpu_stress"), CPUStressTestStep, "🔥", "CPU Stress Test"),
                (get_text("gpu_stress"), GPUStressTestStep, "🎮", "GPU Stress Test"),
                (get_text("harddrive_speed"), HardDriveSpeedStep, "⚡", "Hard drive read/write speed"),
                ("Thermal Monitor", ThermalMonitorStep, "🌡️", "Monitor CPU/RAM temperature"),
                ("System Stability", SystemStabilityStep, "🔥", "Combined stability test"),
            ]'''

content = content.replace(old_tests, new_tests)

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Updated individual test mode:")
print("- Added PhysicalInspectionStep")
print("- Added BIOSCheckStep")
print("- Added SystemStabilityStep")
print("- Added proper translations for all tests")
print("- Total: 17 tests available")
