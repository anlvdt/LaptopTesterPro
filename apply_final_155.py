#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from FINAL_155_TRANSLATIONS import FINAL_TRANS

# Add to lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    new_entries = []
    for vi, en in FINAL_TRANS.items():
        if f'"{vi}":' not in content:
            vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            en_esc = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            new_entries.append(f'    "{vi_esc}": "{en_esc}",')
    
    if new_entries:
        new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
        content = content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
        
        with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added {len(new_entries)} final translations")
    else:
        print("All already exist")
