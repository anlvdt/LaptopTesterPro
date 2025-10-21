# Sửa lỗi GPU Stress Test và Combined Test

## Ngày: 14/10/2025

## Các vấn đề đã được sửa:

### 1. ✅ Thêm chế độ dừng test cho GPU Stress Test

**Vấn đề:** GPU Stress Test không có nút dừng hoạt động.

**Giải pháp:**
- Nút "Dừng Test" đã có sẵn trong `BaseStressTestStep` (class cha).
- Sửa phương thức `stop_test()` trong `GPUStressTestStep` để:
  - Gọi `super().stop_test()` để thực hiện cleanup chuẩn
  - Gửi signal 'stop' qua queue đến worker process
  - Cleanup pygame khi cần thiết
- Thêm kiểm tra signal 'stop' trong `run_gpu_stress()` worker để dừng vòng lặp khi nhận được signal

**File thay đổi:** `main_enhanced_auto.py`
- Line ~2830-2850: Sửa phương thức `stop_test()` trong class `GPUStressTestStep`
- Line ~800-810: Thêm kiểm tra queue trong `run_gpu_stress()` để nhận signal dừng

### 2. ✅ Dịch phần thời gian test trong Combined Test

**Vấn đề:** Phần hiển thị thời gian trong Combined Stress Test (SystemStabilityStep) chưa được dịch.

**Giải pháp:**
- Sửa phương thức `run_combined_test()` để hiển thị thời gian bằng tiếng Việt/tiếng Anh
- Format: "Thời gian: Xs / Ys" (tiếng Việt) hoặc "Time: Xs / Ys" (tiếng Anh)
- Bao gồm CPU%, RAM%, và Nhiệt độ (đã được dịch)

**File thay đổi:** `main_enhanced_auto.py`
- Line ~4615-4630: Sửa phương thức `run_combined_test()` trong class `SystemStabilityStep`

### 3. ✅ Dịch các label trong GPU Stress Test window

**Vấn đề:** Các label "Thời gian:", "Tiến độ:" trong cửa sổ pygame chưa được dịch.

**Giải pháp:**
- Thêm các key dịch vào LANG dictionary (tiếng Việt và tiếng Anh)
- Sử dụng hàm `t()` để dịch các label trong `run_gpu_stress()`
- Các label đã dịch:
  - "Thời gian:" → "Time:"
  - "Tiến độ:" → "Progress:"
  - "GPU Stress Test - Nhấn ESC để thoát" → "GPU Stress Test - Press ESC to exit"
  - "Test đã dừng bởi người dùng (ESC)" → "Test stopped by user (ESC)"
  - và nhiều label khác

**File thay đổi:** `main_enhanced_auto.py`
- Line ~320-340: Thêm các key dịch vào LANG["vi"]
- Line ~375-395: Thêm các key dịch vào LANG["en"]
- Line ~770-780: Sử dụng `t()` trong `run_gpu_stress()`

## Chi tiết kỹ thuật:

### Cơ chế dừng GPU Stress Test:
1. Người dùng nhấn nút "Dừng Test" → gọi `stop_test()`
2. `stop_test()` gửi signal `{'type': 'stop'}` vào queue
3. Worker process `run_gpu_stress()` kiểm tra queue trong vòng lặp chính
4. Khi nhận signal 'stop', worker thoát vòng lặp và cleanup pygame
5. Parent class `BaseStressTestStep.stop_test()` terminate worker process nếu cần

### Hiển thị thời gian trong Combined Test:
```python
if CURRENT_LANG == "vi":
    status_text = f"Thời gian: {time_elapsed}s / {time_total}s | CPU: {cpu_usage:.1f}% | RAM: {mem_usage:.1f}% | Nhiệt độ: {temp:.1f}°C"
else:
    status_text = f"Time: {time_elapsed}s / {time_total}s | CPU: {cpu_usage:.1f}% | RAM: {mem_usage:.1f}% | Temp: {temp:.1f}°C"
```

## Testing:

### Test GPU Stress:
1. Chạy GPU Stress Test
2. Nhấn nút "Dừng Test" hoặc ESC trong cửa sổ pygame
3. Kiểm tra test dừng ngay lập tức
4. Kiểm tra các label hiển thị bằng tiếng Việt (nếu chọn tiếng Việt)

### Test Combined Stress:
1. Chạy System Stability Test (Combined Test)
2. Kiểm tra hiển thị thời gian: "Thời gian: Xs / 180s"
3. Kiểm tra hiển thị CPU%, RAM%, Nhiệt độ

## Lưu ý:
- Tất cả các thay đổi đều tương thích ngược (backward compatible)
- Không ảnh hưởng đến các test step khác
- Nút "Dừng Test" luôn hiển thị và hoạt động cho tất cả stress test
