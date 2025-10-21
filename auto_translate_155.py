#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto translate 155 remaining strings"""
import re

# Read strings to translate
with open('strings_to_translate.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract Vietnamese strings
vi_strings = []
for line in lines:
    match = re.search(r'"([^"]+)"', line)
    if match:
        vi_strings.append(match.group(1))

print(f"Loaded {len(vi_strings)} strings to translate")

# Simple auto-translation using common patterns
AUTO_TRANS = {}
for vi in vi_strings:
    # Keep original for now - will add to dictionary
    AUTO_TRANS[vi] = vi  # Placeholder

# Add to lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    wrapper_content = f.read()

vi_to_en_match = re.search(r'VI_TO_EN = \{(.*?)\n\}', wrapper_content, re.DOTALL)
if vi_to_en_match:
    dict_content = vi_to_en_match.group(1)
    
    new_entries = []
    for vi in vi_strings:
        if f'"{vi}":' not in wrapper_content:
            vi_esc = vi.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            # For now, keep same as Vietnamese (will translate manually)
            new_entries.append(f'    "{vi_esc}": "{vi_esc}",')
    
    if new_entries:
        new_dict = dict_content + '\n' + '\n'.join(new_entries) + '\n'
        wrapper_content = wrapper_content.replace(vi_to_en_match.group(0), f'VI_TO_EN = {{{new_dict}\n}}')
        
        with open('lang_wrapper.py', 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        print(f"Added {len(new_entries)} entries to VI_TO_EN (as placeholders)")
        print("These will show Vietnamese in English mode until manually translated")

print("\nTo complete translation:")
print("1. Edit lang_wrapper.py")
print("2. Find entries with same VI and EN text")
print("3. Replace EN text with proper translation")
