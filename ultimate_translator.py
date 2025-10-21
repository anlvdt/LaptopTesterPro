#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ultimate translator - Find and translate ALL Vietnamese texts"""
import re

# Read main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ'

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

# Find ALL string literals with Vietnamese
pattern = r'"([^"]{3,})"'
matches = re.findall(pattern, content)

vi_strings = {}
for s in set(matches):
    if has_vietnamese(s):
        vi_strings[s] = s  # Will translate later

print(f"Found {len(vi_strings)} unique Vietnamese strings")

# Read existing translations
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    wrapper = f.read()

# Filter out already translated
new_strings = {}
for vi in vi_strings:
    if f'"{vi}":' not in wrapper:
        new_strings[vi] = vi

print(f"Need to translate: {len(new_strings)} new strings")

# Save to file for manual translation
with open('strings_to_translate.txt', 'w', encoding='utf-8') as f:
    for i, vi in enumerate(sorted(new_strings.keys()), 1):
        f.write(f'{i}. "{vi}"\n')

print(f"Saved to strings_to_translate.txt")
print(f"\nTotal Vietnamese strings in code: {len(vi_strings)}")
print(f"Already translated: {len(vi_strings) - len(new_strings)}")
print(f"Need translation: {len(new_strings)}")
