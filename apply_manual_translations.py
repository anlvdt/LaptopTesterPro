#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Load manual translations
with open('manual_translations.json', 'r', encoding='utf-8') as f:
    manual = json.load(f)

# Read current wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Apply manual translations
for vi, en in manual.items():
    vi_escaped = vi.replace('\\', '\\\\').replace('"', '\\"')
    en_escaped = en.replace('\\', '\\\\').replace('"', '\\"')
    
    # Replace in content
    old_line = f'    "{vi_escaped}": "{vi_escaped}",'
    new_line = f'    "{vi_escaped}": "{en_escaped}",'
    content = content.replace(old_line, new_line)

# Write back
with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Applied {len(manual)} manual translations")
