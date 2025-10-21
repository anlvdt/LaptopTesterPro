#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrap ALL Vietnamese strings with t()"""
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vietnamese_chars += vietnamese_chars.upper()

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

# Pattern: text="..." or text='...' (not already wrapped)
pattern = r'(\btext\s*=\s*)(["\'])([^"\']+)\2'

def replace_func(match):
    prefix = match.group(1)
    quote = match.group(2)
    string = match.group(3)
    
    # Skip if already wrapped
    if 't(' in prefix or 't (' in prefix:
        return match.group(0)
    
    # Only wrap if has Vietnamese
    if has_vietnamese(string):
        return f'{prefix}t({quote}{string}{quote})'
    
    return match.group(0)

new_content = re.sub(pattern, replace_func, content)

# Count changes
count = new_content.count('text=t(') - content.count('text=t(')

# Backup
with open('main_enhanced_auto_before_wrap_all.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Write
with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Wrapped {count} Vietnamese strings")
print("Backup: main_enhanced_auto_before_wrap_all.py")
