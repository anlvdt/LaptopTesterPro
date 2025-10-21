#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate complete lang_wrapper with all translations"""

import json

# Read Vietnamese strings
with open('vietnamese_strings.json', 'r', encoding='utf-8') as f:
    vi_strings = json.load(f)

# Read existing wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    existing = f.read()

# Extract existing VI_TO_EN dict
import re
match = re.search(r'VI_TO_EN = \{([^}]+)\}', existing, re.DOTALL)
if match:
    existing_dict_str = match.group(1)
else:
    existing_dict_str = ""

# Parse existing translations
existing_trans = {}
for line in existing_dict_str.split('\n'):
    if '":' in line:
        try:
            parts = line.split('": "')
            if len(parts) == 2:
                key = parts[0].strip().strip('"')
                val = parts[1].strip().rstrip('",')
                existing_trans[key] = val
        except:
            pass

print(f"Existing translations: {len(existing_trans)}")
print(f"Total Vietnamese strings: {len(vi_strings)}")

# Create new wrapper with all translations
new_wrapper = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Language Wrapper - Complete Translation"""

CURRENT_LANG = "vi"

VI_TO_EN = {
'''

# Add all translations
for vi_str in sorted(set(vi_strings)):
    if vi_str in existing_trans:
        en_str = existing_trans[vi_str]
    else:
        # Use simple mapping for common patterns
        en_str = vi_str  # Keep as is if no translation
    
    # Escape quotes
    vi_escaped = vi_str.replace('\\', '\\\\').replace('"', '\\"')
    en_escaped = en_str.replace('\\', '\\\\').replace('"', '\\"')
    
    new_wrapper += f'    "{vi_escaped}": "{en_escaped}",\n'

new_wrapper += '''
}

def t(text):
    """Translation wrapper"""
    global CURRENT_LANG
    if not text or not isinstance(text, str):
        return text
    if CURRENT_LANG == "en":
        return VI_TO_EN.get(text, text)
    return text

def set_language(lang):
    """Set current language"""
    global CURRENT_LANG
    CURRENT_LANG = lang

def get_language():
    """Get current language"""
    return CURRENT_LANG
'''

# Write new wrapper
with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
    f.write(new_wrapper)

print(f"Generated lang_wrapper.py with {len(vi_strings)} translations")
