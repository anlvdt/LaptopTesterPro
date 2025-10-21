#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from CAPABILITY_TRANSLATIONS import CAP_TRANS

# Add to lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    new_entries = []
    for vi, en in CAP_TRANS.items():
        vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_esc = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        new_entries.append(f'    "{vi_esc}": "{en_esc}",')
    
    new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
    content = content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
    
    with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added {len(CAP_TRANS)} capability translations")

# Now wrap in main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

# Replace capability titles and descs with t()
replacements = [
    ('{"icon": "📄", "title": "Văn Phòng"', '{"icon": "📄", "title": t("Văn Phòng")'),
    ('"desc": "Office: Word, Excel\\nWeb: Facebook, YouTube\\nPhim: Netflix 1080p"', '"desc": t("Office: Word, Excel\\nWeb: Facebook, YouTube\\nPhim: Netflix 1080p")'),
    ('{"icon": "📚", "title": "Học Tập"', '{"icon": "📚", "title": t("Học Tập")'),
    ('"desc": "Zoom, Teams\\nWord, PPT\\nTra cứu web"', '"desc": t("Zoom, Teams\\nWord, PPT\\nTra cứu web")'),
    ('"title": "Đồ Họa Pro"', '"title": t("Đồ Họa Pro")'),
    ('"desc": "3D: AutoCAD, SolidWorks\\nRender: Blender, V-Ray\\nAI: TensorFlow, PyTorch"', '"desc": t("3D: AutoCAD, SolidWorks\\nRender: Blender, V-Ray\\nAI: TensorFlow, PyTorch")'),
    ('"title": "Gaming 1080p"', '"title": t("Gaming 1080p")'),
    ('"desc": "Game: Esports titles\\nCasual AAA games\\nLight 3D work"', '"desc": t("Game: Esports titles\\nCasual AAA games\\nLight 3D work")'),
]

for old, new in replacements:
    main_content = main_content.replace(old, new)

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(main_content)

print("Wrapped capability texts with t()")
