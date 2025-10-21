# PATCHES CẦN APPLY VÀO main_enhanced_auto.py

# 1. THÊM THỜI GIAN ƯỚC TÍNH CHO MỖI BƯỚC TEST
ESTIMATED_TIMES = {
    "hardware_fingerprint": "30s",
    "license_check": "20s", 
    "system_info": "15s",
    "harddrive_health": "30s",
    "screen_test": "1-2 phut",
    "keyboard_test": "2-3 phut",
    "battery_health": "20s",
    "audio_test": "1-2 phut",
    "webcam_test": "1-2 phut",
    "cpu_stress": "3-5 phut",
    "harddrive_speed": "2-3 phut",
    "gpu_stress": "3-5 phut",
    "network_test": "30s-1 phut",
    "thermal_test": "2-3 phut",
    "system_monitor": "3-5 phut"
}

# 2. THÊM ESC KEY HANDLER VÀO KEYBOARD TEST
# Trong KeyboardTestStep.__init__, thêm:
# self.bind_all("<Escape>", self.on_escape_key)

# def on_escape_key(self, event):
#     if hasattr(self, 'listening') and self.listening:
#         self.listening = False
#         self.mark_completed({"Result": "Stopped by ESC"}, auto_advance=False)

# 3. FIX FN KEYS - IGNORE TRONG KEYBOARD TEST
# Trong KeyboardTestStep.on_key_event, thêm check:
# if 'fn' in key_name_raw.lower() or key_name_raw.startswith('f') and key_name_raw[1:].isdigit():
#     return  # Ignore Fn keys

# 4. THÊM ESC TO STOP CHO CÁC STRESS TEST
# Trong BaseStressTestStep, thêm:
# self.bind_all("<Escape>", lambda e: self.stop_test())

# 5. FIX TEXT ENCODING - Thay thế trong LANG["vi"]
FIXED_VI_TEXTS = {
    "professional_tools": "CONG CU CHUYEN NGHIEP BO SUNG",
    "tools_description": "De kiem tra sau hon, hay su dung cac cong cu chuyen nghiep sau:",
    "install_command": "Lenh cai dat:",
    "homepage": "Trang chu",
    "usage_guide": "HUONG DAN SU DUNG CONG CU",
}
