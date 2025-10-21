#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from MEGA_TRANSLATIONS import MEGA

# Read lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find VI_TO_EN dict
vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    # Add MEGA translations
    new_entries = []
    for vi, en in MEGA.items():
        vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_esc = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        new_entries.append(f'    "{vi_esc}": "{en_esc}",')
    
    new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
    content = content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
    
    with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added {len(MEGA)} MEGA translations")
