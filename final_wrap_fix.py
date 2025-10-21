#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final fix - wrap all remaining texts"""
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Ổ cứng in HardDriveHealthStep
content = content.replace('drive_label = t("Ổ cứng:")', 'drive_label = t("Ổ cứng:")')  # Already wrapped
content = content.replace('"Ổ cứng có hoạt động tốt không?"', 't("Ổ cứng có hoạt động tốt không?")')

# Fix 2: Capability labels in HardwareFingerprintStep - wrap title and desc
# Pattern: {"icon": "📄", "title": "Văn Phòng", "desc": "...", "color": "..."}
content = re.sub(
    r'(\{"icon": "[^"]+", "title": )"(Văn Phòng)"',
    r'\1t("\2")',
    content
)
content = re.sub(
    r'(\{"icon": "[^"]+", "title": )"(Học Tập)"',
    r'\1t("\2")',
    content
)
content = re.sub(
    r'(\{"icon": "[^"]+", "title": )"(Văn Phòng & Code)"',
    r'\1t("\2")',
    content
)

# Fix 3: BIOS checklist items - wrap all Vietnamese text in BIOSCheckStep
bios_texts = [
    "Vào BIOS và kiểm tra các thông tin sau:",
    "Ngày sản xuất BIOS (BIOS Date)",
    "Serial Number (SN) - Không thể giả mạo",
    "Model chính xác của máy",
    "Cấu hình CPU, RAM, Storage",
    "Secure Boot: Enabled/Disabled",
    "Virtualization: Enabled/Disabled",
    "SATA Mode: AHCI/RAID",
    "Boot Mode: UEFI/Legacy",
    "Có mật khẩu BIOS không? (Cảnh báo nếu có)",
    "Có khóa xung CPU không? (Undervolting/Throttling)",
]

for text in bios_texts:
    # Wrap if not already wrapped
    old = f'"{text}"'
    new = f't("{text}")'
    # Only replace if it's in a text= context and not already wrapped
    content = re.sub(rf'(\btext=)"{re.escape(text)}"', rf'\1t("{text}")', content)

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied final wrapping fixes")
