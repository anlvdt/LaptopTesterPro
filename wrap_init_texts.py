#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrap texts in __init__ methods"""
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ'

# Pattern: super().__init__(master, "title", "why", "how", **kwargs)
pattern = r'super\(\).__init__\(master,\s*"([^"]+)",\s*\n\s*"([^"]+)",\s*\n\s*"([^"]+)"'

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

def replace_func(match):
    title = match.group(1)
    why = match.group(2)
    how = match.group(3)
    
    # Wrap if has Vietnamese
    title_wrapped = f't("{title}")' if has_vietnamese(title) else f'"{title}"'
    why_wrapped = f't("{why}")' if has_vietnamese(why) else f'"{why}"'
    how_wrapped = f't("{how}")' if has_vietnamese(how) else f'"{how}"'
    
    return f'super().__init__(master, {title_wrapped}, \n            {why_wrapped}, \n            {how_wrapped}'

new_content = re.sub(pattern, replace_func, content)

# Count
count = new_content.count('super().__init__(master, t(') - content.count('super().__init__(master, t(')

# Write
with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Wrapped {count} __init__ texts")
