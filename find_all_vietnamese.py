#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find ALL string literals
pattern = r'"([^"]{3,})"'
matches = re.findall(pattern, content)

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vietnamese_chars += vietnamese_chars.upper()

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

vi_strings = [s for s in set(matches) if has_vietnamese(s)]

print(f"Found {len(vi_strings)} Vietnamese strings (not wrapped with t())")

# Save
with open('all_vietnamese_strings.txt', 'w', encoding='utf-8') as f:
    for text in sorted(vi_strings):
        f.write(f"{text}\n")

print("Saved to all_vietnamese_strings.txt")
