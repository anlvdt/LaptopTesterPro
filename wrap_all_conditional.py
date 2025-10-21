#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrap all conditional Vietnamese strings"""

import re

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: "Vietnamese text" if CURRENT_LANG == "vi" else "English text"
    pattern = r'"([^"]+)"\s+if\s+CURRENT_LANG\s+==\s+"vi"\s+else\s+"([^"]+)"'
    
    def replace_func(match):
        vi_text = match.group(1)
        en_text = match.group(2)
        # Replace with t() that returns English when CURRENT_LANG == "en"
        return f't("{vi_text}")'
    
    # Replace all occurrences
    new_content = re.sub(pattern, replace_func, content)
    
    # Backup
    with open(filename + '.bak2', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Write new content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Count replacements
    count = len(re.findall(pattern, content))
    print(f"Replaced {count} conditional strings")
    print(f"Backup: {filename}.bak2")

if __name__ == "__main__":
    process_file('main_enhanced_auto.py')
