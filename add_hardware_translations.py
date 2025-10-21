#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add hardware fingerprint translations"""

HARDWARE_TRANS = {
    "Chi tiết": "Details",
    "Code: VS, Android Studio, Docker\nVM: 3-4 máy ảo\n50+ Chrome tabs": "Code: VS, Android Studio, Docker\nVM: 3-4 virtual machines\n50+ Chrome tabs",
    "Hiển thị nhận định khả năng sử dụng phần cứng": "Display hardware capability assessment",
    "Hàm chung phân tích khả năng phần cứng": "Common function to analyze hardware capability",
    "Học Tập": "Study",
    "Văn Phòng": "Office",
    "Văn Phòng & Code": "Office & Code",
    "Zoom, Teams\nWord, PPT\nTra cứu web": "Zoom, Teams\nWord, PPT\nWeb browsing",
    "Đồ Họa Pro": "Pro Graphics",
}

# Read lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to VI_TO_EN
import re
vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    new_entries = []
    for vi, en in HARDWARE_TRANS.items():
        vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_esc = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        new_entries.append(f'    "{vi_esc}": "{en_esc}",')
    
    new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
    content = content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
    
    with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added {len(HARDWARE_TRANS)} hardware translations")
