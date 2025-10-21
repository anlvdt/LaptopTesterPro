#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract all Vietnamese strings and save to file"""

import re
import json

# Read main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all t("...") calls
pattern = r't\("([^"]+)"\)'
matches = re.findall(pattern, content)

# Filter Vietnamese strings
vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vietnamese_chars += vietnamese_chars.upper()

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

vi_strings = [s for s in matches if has_vietnamese(s)]
unique_vi = sorted(set(vi_strings))

# Save to JSON file
with open('vietnamese_strings.json', 'w', encoding='utf-8') as f:
    json.dump(unique_vi, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(unique_vi)} unique Vietnamese strings")
print("Saved to: vietnamese_strings.json")
