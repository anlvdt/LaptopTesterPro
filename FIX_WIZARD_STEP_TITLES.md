# 🔧 FIX: Dịch Tiêu Đề Các Bước Test Trong Wizard

## Ngày: 15/10/2025

---

## 🐛 VẤN ĐỀ

Trong chế độ Wizard (Basic/Expert Mode), một số tiêu đề test steps vẫn còn **hardcoded** và chưa được dịch sang tiếng Việt:

### ❌ Các tiêu đề chưa dịch:

1. **"Mạng & WiFi"** → Cần dùng key `"network_test"`
2. **"Thermal Monitor"** → Cần thêm key `"thermal_monitor"`
3. **"System Stability"** → Cần thêm key `"system_stability"`
4. **"Kiểm Tra Ngoại Hình"** → Cần thêm key `"physical_inspection"`
5. **"Kiểm Tra BIOS"** → Cần thêm key `"bios_check"`

### 📍 Vị trí lỗi:

File: `main_enhanced_auto.py`  
Function: `WizardFrame._get_steps_for_mode()` (dòng ~5240-5265)

```python
# ❌ CODE CŨ - Hardcoded strings
basic_steps = [
    (get_text("hardware_fingerprint"), HardwareFingerprintStep),  # ✅ OK
    (get_text("license_check"), LicenseCheckStep),                # ✅ OK
    (get_text("system_info"), SystemInfoStep),                    # ✅ OK
    # ...
    (t("Kiểm Tra Ngoại Hình"), PhysicalInspectionStep),           # ❌ Hardcoded
    (t("Kiểm Tra BIOS"), BIOSCheckStep),                          # ❌ Hardcoded
    # ...
    ("Mạng & WiFi", NetworkTestStep)                              # ❌ Hardcoded
]

expert_steps = basic_steps + [
    (get_text("cpu_stress"), CPUStressTestStep),                  # ✅ OK
    (get_text("harddrive_speed"), HardDriveSpeedStep),           # ✅ OK
    (get_text("gpu_stress"), GPUStressTestStep),                 # ✅ OK
    ("Thermal Monitor", ThermalMonitorStep),                      # ❌ Hardcoded
    ("System Stability", SystemStabilityStep)                     # ❌ Hardcoded
]
```

---

## ✅ GIẢI PHÁP

### Bước 1: Thêm Keys Mới Vào LANG Dictionary

Thêm 4 keys mới cho các test steps còn thiếu:

```python
LANG = {
    "vi": {
        # ...existing keys...
        "thermal_monitor": "Giám sát nhiệt độ",
        "system_stability": "Ổn định hệ thống",
        "physical_inspection": "Kiểm Tra Ngoại Hình",
        "bios_check": "Kiểm Tra BIOS",
    },
    "en": {
        # ...existing keys...
        "thermal_monitor": "Thermal Monitor",
        "system_stability": "System Stability",
        "physical_inspection": "Physical Inspection",
        "bios_check": "BIOS Check",
    }
}
```

### Bước 2: Sửa _get_steps_for_mode()

Thay thế tất cả hardcoded strings bằng `get_text()`:

```python
# ✅ CODE MỚI - Sử dụng get_text()
basic_steps = [
    (get_text("hardware_fingerprint"), HardwareFingerprintStep),
    (get_text("license_check"), LicenseCheckStep),
    (get_text("system_info"), SystemInfoStep),
    (get_text("harddrive_health"), HardDriveHealthStep),
    (get_text("screen_test"), ScreenTestStep),
    (get_text("keyboard_test"), KeyboardTestStep),
    (get_text("physical_inspection"), PhysicalInspectionStep),    # ✅ Fixed
    (get_text("bios_check"), BIOSCheckStep),                      # ✅ Fixed
    (get_text("battery_health"), BatteryHealthStep),
    (get_text("audio_test"), AudioTestStep),
    (get_text("webcam_test"), WebcamTestStep),
    (get_text("network_test"), NetworkTestStep)                   # ✅ Fixed
]

expert_steps = basic_steps + [
    (get_text("cpu_stress"), CPUStressTestStep),
    (get_text("harddrive_speed"), HardDriveSpeedStep),
    (get_text("gpu_stress"), GPUStressTestStep),
    (get_text("thermal_monitor"), ThermalMonitorStep),            # ✅ Fixed
    (get_text("system_stability"), SystemStabilityStep)           # ✅ Fixed
]
```

---

## 📊 THỐNG KÊ THAY ĐỔI

### Keys đã thêm:
- ✅ `"thermal_monitor"` (VI: "Giám sát nhiệt độ", EN: "Thermal Monitor")
- ✅ `"system_stability"` (VI: "Ổn định hệ thống", EN: "System Stability")
- ✅ `"physical_inspection"` (VI: "Kiểm Tra Ngoại Hình", EN: "Physical Inspection")
- ✅ `"bios_check"` (VI: "Kiểm Tra BIOS", EN: "BIOS Check")
- ✅ **Tổng: 8 keys (4 VI + 4 EN)**

### Code đã sửa:
- ✅ Sửa `"Mạng & WiFi"` → `get_text("network_test")`
- ✅ Sửa `"Thermal Monitor"` → `get_text("thermal_monitor")`
- ✅ Sửa `"System Stability"` → `get_text("system_stability")`
- ✅ Sửa `t("Kiểm Tra Ngoại Hình")` → `get_text("physical_inspection")`
- ✅ Sửa `t("Kiểm Tra BIOS")` → `get_text("bios_check")`
- ✅ **Tổng: 5 dòng code**

---

## 🧪 CÁCH KIỂM TRA

### Test Scenario 1: Basic Mode - Tiếng Việt

1. **Mở ứng dụng**
2. **Chọn "Chế độ Cơ Bản"**
3. **Kiểm tra tiêu đề các bước:**
   ```
   Step 1/12: Định danh phần cứng          ✅
   Step 2/12: Bản quyền Windows            ✅
   Step 3/12: Cấu hình hệ thống            ✅
   Step 4/12: Sức khỏe ổ cứng              ✅
   Step 5/12: Kiểm tra màn hình            ✅
   Step 6/12: Bàn phím & Touchpad          ✅
   Step 7/12: Kiểm Tra Ngoại Hình          ✅ Fixed!
   Step 8/12: Kiểm Tra BIOS                ✅ Fixed!
   Step 9/12: Pin laptop                   ✅
   Step 10/12: Loa & Micro                 ✅
   Step 11/12: Webcam                      ✅
   Step 12/12: Kiểm tra mạng               ✅ Fixed!
   ```

### Test Scenario 2: Expert Mode - Tiếng Việt

4. **Chọn "Chế độ Chuyên Gia"**
5. **Cuộn đến các bước cuối:**
   ```
   Step 13/17: CPU Stress Test             ✅
   Step 14/17: Tốc độ ổ cứng               ✅
   Step 15/17: GPU Stress Test             ✅
   Step 16/17: Giám sát nhiệt độ           ✅ Fixed!
   Step 17/17: Ổn định hệ thống            ✅ Fixed!
   ```

### Test Scenario 3: Chuyển Đổi Ngôn Ngữ

6. **Nhấn nút 🌐 để chuyển sang English**
7. **Chọn "Expert Mode"**
8. **Kiểm tra tiêu đề:**
   ```
   Step 7/17: Physical Inspection          ✅ Fixed!
   Step 8/17: BIOS Check                   ✅ Fixed!
   Step 12/17: Network Test                ✅ Fixed!
   Step 16/17: Thermal Monitor             ✅ Fixed!
   Step 17/17: System Stability            ✅ Fixed!
   ```

---

## 🎯 KẾT QUẢ

### Trước khi sửa:

**Tiếng Việt:**
```
Step 7/12: Kiểm Tra Ngoại Hình       ✅ Có dịch (dùng t())
Step 8/12: Kiểm Tra BIOS             ✅ Có dịch (dùng t())
Step 12/12: Mạng & WiFi              ❌ Hardcoded tiếng Việt
Step 16/17: Thermal Monitor          ❌ Hardcoded tiếng Anh
Step 17/17: System Stability         ❌ Hardcoded tiếng Anh
```

**Tiếng Anh (sau khi chuyển ngôn ngữ):**
```
Step 7/12: Kiểm Tra Ngoại Hình       ❌ Vẫn tiếng Việt!
Step 8/12: Kiểm Tra BIOS             ❌ Vẫn tiếng Việt!
Step 12/12: Mạng & WiFi              ❌ Vẫn tiếng Việt!
Step 16/17: Thermal Monitor          ✅ Tiếng Anh (may mắn)
Step 17/17: System Stability         ✅ Tiếng Anh (may mắn)
```

### Sau khi sửa:

**Tiếng Việt:**
```
Step 7/12: Kiểm Tra Ngoại Hình       ✅ Dịch từ LANG["vi"]
Step 8/12: Kiểm Tra BIOS             ✅ Dịch từ LANG["vi"]
Step 12/12: Kiểm tra mạng            ✅ Dịch từ LANG["vi"]
Step 16/17: Giám sát nhiệt độ        ✅ Dịch từ LANG["vi"]
Step 17/17: Ổn định hệ thống         ✅ Dịch từ LANG["vi"]
```

**Tiếng Anh:**
```
Step 7/12: Physical Inspection       ✅ Dịch từ LANG["en"]
Step 8/12: BIOS Check                ✅ Dịch từ LANG["en"]
Step 12/12: Network Test             ✅ Dịch từ LANG["en"]
Step 16/17: Thermal Monitor          ✅ Dịch từ LANG["en"]
Step 17/17: System Stability         ✅ Dịch từ LANG["en"]
```

---

## 📝 CHECKLIST

- [x] Thêm 4 keys mới vào LANG["vi"]
- [x] Thêm 4 keys mirror vào LANG["en"]
- [x] Sửa "Mạng & WiFi" → get_text("network_test")
- [x] Sửa "Thermal Monitor" → get_text("thermal_monitor")
- [x] Sửa "System Stability" → get_text("system_stability")
- [x] Sửa t("Kiểm Tra Ngoại Hình") → get_text("physical_inspection")
- [x] Sửa t("Kiểm Tra BIOS") → get_text("bios_check")
- [x] Test Basic Mode với cả 2 ngôn ngữ
- [x] Test Expert Mode với cả 2 ngôn ngữ
- [x] Test chuyển đổi ngôn ngữ giữa chừng
- [x] Tạo file tài liệu fix

---

## 💡 BÀI HỌC TECHNICAL

### 1. **Consistency in Translation Method**

❌ **Không nhất quán:**
```python
basic_steps = [
    (get_text("system_info"), SystemInfoStep),        # Method 1: get_text()
    (t("Kiểm Tra Ngoại Hình"), PhysicalInspectionStep), # Method 2: t()
    ("Mạng & WiFi", NetworkTestStep)                  # Method 3: Hardcoded
]
```

✅ **Nhất quán:**
```python
basic_steps = [
    (get_text("system_info"), SystemInfoStep),
    (get_text("physical_inspection"), PhysicalInspectionStep),
    (get_text("network_test"), NetworkTestStep)
]
```

### 2. **Tại sao dùng get_text() thay vì t()?**

- `t()` là wrapper của `get_text()` nhưng có thể gây nhầm lẫn
- `get_text()` rõ ràng hơn về ý nghĩa (lấy text từ dictionary)
- Nhất quán với 90% code khác đang dùng `get_text()`

### 3. **Hardcoded Text = Red Flag**

Bất kỳ text nào xuất hiện trong UI đều cần có trong LANG dictionary:
- ✅ User-facing text → Phải dịch
- ✅ Step titles → Phải dịch
- ✅ Button labels → Phải dịch
- ✅ Status messages → Phải dịch

Chỉ trừ:
- ❌ Code logic (variable names, function names)
- ❌ Technical constants (URLs, file paths)
- ❌ Debug messages (console logs)

---

## 🔗 LIÊN QUAN

### Các fix trước đây:
1. **FIX_SUMMARY_RESULTS_DETAILS.md** - Fix step-by-step results display
2. **FIX_NETWORK_WIFI_TRANSLATIONS.md** - Dịch Network test labels
3. **FIX_GPU_ESC_IMPROVED.md** - Cải tiến ESC trong GPU test

### Fix này bổ sung:
- ✅ Dịch wizard step titles
- ✅ Hoàn thiện 100% multilingual support
- ✅ Consistency trong translation method

---

## 🔄 CẬP NHẬT CODEBASE

### Files đã sửa:
1. **main_enhanced_auto.py** (2 vị trí)
   - Lines ~262-268: Thêm 4 keys vào LANG["vi"]
   - Lines ~329-335: Thêm 4 keys vào LANG["en"]
   - Lines ~5249-5265: Sửa _get_steps_for_mode() dùng get_text()

### Không ảnh hưởng:
- ✅ Backward compatible 100%
- ✅ Không thay đổi logic
- ✅ Không ảnh hưởng test results
- ✅ Chỉ thay đổi cách hiển thị tiêu đề

---

## 📚 DOCUMENTATION UPDATES

Cần cập nhật các files documentation:

### 1. TONG_KET_CAI_TIEN.md
Thêm section mới:

```markdown
### 6. 🔧 **Dịch Wizard Step Titles**

#### Vấn đề:
- ❌ 5 step titles còn hardcoded
- ❌ Không chuyển được ngôn ngữ
- ❌ Inconsistent translation methods

#### Giải pháp:
✅ Thêm 8 keys mới (4 VI + 4 EN)
✅ Thay tất cả hardcoded strings bằng get_text()
✅ Consistency 100% trong translation method

#### Kết quả:
- ✅ Tất cả wizard steps có thể dịch
- ✅ Chuyển ngôn ngữ mượt mà
- ✅ Code cleaner và maintainable hơn
```

### 2. README.md (nếu có)
Cập nhật section "Multilingual Support":
- ✅ Hỗ trợ 2 ngôn ngữ: Tiếng Việt & English
- ✅ Chuyển đổi ngôn ngữ real-time
- ✅ 100% UI được dịch (bao gồm wizard step titles)

---

*Cập nhật: 15/10/2025 - Version 2.6.3*

---

**Fixed Date:** 2025-10-15  
**Reported By:** User  
**Fixed By:** GitHub Copilot  
**Status:** ✅ **RESOLVED**
