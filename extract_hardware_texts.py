#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# Read main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find HardwareFingerprintStep class (around line 1027-1458)
start = 1026
end = 1458
class_content = ''.join(lines[start:end])

# Find all strings
pattern = r'"([^"]{5,})"'
matches = re.findall(pattern, class_content)

# Filter Vietnamese
vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vietnamese_chars += vietnamese_chars.upper()

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

vi_texts = [t for t in set(matches) if has_vietnamese(t)]

print(f"Found {len(vi_texts)} Vietnamese strings in HardwareFingerprintStep")

# Save
with open('hardware_vi_texts.txt', 'w', encoding='utf-8') as f:
    for text in sorted(vi_texts):
        f.write(f"{text}\n")

print(f"\nSaved to: hardware_vi_texts.txt")
