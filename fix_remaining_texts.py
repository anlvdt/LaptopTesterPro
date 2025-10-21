#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining untranslated texts"""
import re

# Additional translations
ADDITIONAL_TRANS = {
    # Step 3 - Hard Drive
    "Ổ cứng": "Hard Drive",
    "Dung lượng": "Capacity",
    "Loại": "Type",
    "Nhiệt độ": "Temperature",
    "Trạng thái": "Status",
    
    # BIOS Checklist
    "Vào BIOS và kiểm tra các thông tin sau:": "Enter BIOS and check following info:",
    "Ngày sản xuất BIOS (BIOS Date)": "BIOS manufacture date",
    "Serial Number (SN) - Không thể giả mạo": "Serial Number (SN) - Cannot be faked",
    "Model chính xác của máy": "Exact machine model",
    "Cấu hình CPU, RAM, Storage": "CPU, RAM, Storage configuration",
    "Secure Boot: Enabled/Disabled": "Secure Boot: Enabled/Disabled",
    "Virtualization: Enabled/Disabled": "Virtualization: Enabled/Disabled",
    "SATA Mode: AHCI/RAID": "SATA Mode: AHCI/RAID",
    "Boot Mode: UEFI/Legacy": "Boot Mode: UEFI/Legacy",
    "Có mật khẩu BIOS không? (Cảnh báo nếu có)": "BIOS password set? (Warning if yes)",
    "Có khóa xung CPU không? (Undervolting/Throttling)": "CPU frequency locked? (Undervolting/Throttling)",
    
    # Step 1 - Capability labels (already in dict but need to check)
    "Văn Phòng": "Office",
    "Học Tập": "Study",
    "Văn Phòng & Code": "Office & Code",
}

# Add to lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    new_entries = []
    for vi, en in ADDITIONAL_TRANS.items():
        # Check if already exists
        if f'"{vi}":' not in content:
            vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            en_esc = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            new_entries.append(f'    "{vi_esc}": "{en_esc}",')
    
    if new_entries:
        new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
        content = content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
        
        with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added {len(new_entries)} additional translations")
    else:
        print("All translations already exist")

# Now wrap texts in main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

# Find and wrap "Ổ cứng" in HardDriveHealthStep
main_content = re.sub(r'(\s+text=)"(Ổ cứng)"', r'\1t("\2")', main_content)
main_content = re.sub(r'(\s+text=)"(Dung lượng)"', r'\1t("\2")', main_content)
main_content = re.sub(r'(\s+text=)"(Loại)"', r'\1t("\2")', main_content)
main_content = re.sub(r'(\s+text=)"(Nhiệt độ)"', r'\1t("\2")', main_content)

# Wrap BIOS checklist items
bios_items = [
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

for item in bios_items:
    # Wrap if not already wrapped
    old = f'"{item}"'
    new = f't("{item}")'
    if old in main_content and f't("{item}")' not in main_content:
        main_content = main_content.replace(f'text="{item}"', f'text=t("{item}")')

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(main_content)

print("Wrapped remaining texts with t()")
