#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto translate ALL Vietnamese strings"""
import re

# Read main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all t("...") calls
pattern = r't\("([^"]+)"\)'
matches = re.findall(pattern, content)

# Read existing VI_TO_EN
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    wrapper = f.read()

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vietnamese_chars += vietnamese_chars.upper()

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

# Find untranslated
untranslated = []
for text in set(matches):
    if has_vietnamese(text):
        search = f'"{text}":'
        if search not in wrapper:
            untranslated.append(text)

print(f"Found {len(untranslated)} untranslated strings")

# Simple auto-translate using common patterns
AUTO_TRANS = {}
for vi in untranslated:
    # Keep as-is for now, will add manually
    AUTO_TRANS[vi] = vi

# Save to file for manual translation
with open('need_translation.txt', 'w', encoding='utf-8') as f:
    for text in sorted(untranslated):
        f.write(f'"{text}": "TODO",\n')

print(f"Saved to need_translation.txt - {len(untranslated)} strings need translation")
