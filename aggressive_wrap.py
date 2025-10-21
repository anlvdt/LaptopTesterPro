#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggressively wrap ALL Vietnamese strings"""
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ'

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

# Backup
with open('main_enhanced_auto_before_aggressive.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Pattern 1: text="Vietnamese" (not already t())
pattern1 = r'(\btext\s*=\s*)("([^"]+)")'
def replace1(match):
    prefix = match.group(1)
    full_str = match.group(2)
    string = match.group(3)
    if 't(' not in prefix and has_vietnamese(string):
        return f'{prefix}t({full_str})'
    return match.group(0)

content = re.sub(pattern1, replace1, content)

# Pattern 2: "title": "Vietnamese" in dict
pattern2 = r'("title":\s*)("([^"]+)")'
def replace2(match):
    prefix = match.group(1)
    full_str = match.group(2)
    string = match.group(3)
    if 't(' not in prefix and has_vietnamese(string):
        return f'{prefix}t({full_str})'
    return match.group(0)

content = re.sub(pattern2, replace2, content)

# Pattern 3: "desc": "Vietnamese" in dict
pattern3 = r'("desc":\s*)("([^"]+)")'
def replace3(match):
    prefix = match.group(1)
    full_str = match.group(2)
    string = match.group(3)
    if 't(' not in prefix and has_vietnamese(string):
        return f'{prefix}t({full_str})'
    return match.group(0)

content = re.sub(pattern3, replace3, content)

# Write
with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Aggressively wrapped all Vietnamese strings")
print("Backup: main_enhanced_auto_before_aggressive.py")
