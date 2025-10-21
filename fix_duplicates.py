"""
Script để xóa các step duplicate
"""

import re

# Đọc file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Tìm tất cả vị trí của các step duplicate
pattern = r'(class (?:PhysicalInspectionStep|BIOSCheckStep|CPUStressTestStep|GPUStressTestStep)\(BaseStepFrame\):.*?)(?=class \w+Step\(|class \w+\(ctk\.CTk|$)'

matches = list(re.finditer(pattern, content, re.DOTALL))

print(f"Found {len(matches)} step definitions")

# Nếu có duplicate, xóa các bản sau
if len(matches) > 4:
    # Giữ 4 bản đầu tiên, xóa phần còn lại
    # Tìm vị trí bắt đầu của bản duplicate thứ 5
    start_pos = matches[4].start()
    # Tìm vị trí kết thúc của bản duplicate cuối cùng
    end_pos = matches[-1].end()
    
    # Xóa phần duplicate
    new_content = content[:start_pos] + content[end_pos:]
    
    with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[SUCCESS] Removed duplicate steps from position {start_pos} to {end_pos}")
else:
    print("[INFO] No duplicates found")
