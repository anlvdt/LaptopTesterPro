#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add missing translations to lang_wrapper.py"""

import re

# Read main file to find all Vietnamese strings
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

print(f"Found {len(unique_vi)} unique Vietnamese strings")
print("\nAdd these to lang_wrapper.py VI_TO_EN dictionary:\n")

for s in unique_vi[:20]:  # Show first 20
    print(f'    "{s}": "TODO",')

print(f"\n... and {len(unique_vi) - 20} more")
print(f"\nTotal: {len(unique_vi)} translations needed")
