#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# Read main file
with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all t("...") calls
pattern = r't\("([^"]+)"\)'
matches = re.findall(pattern, content)

# Read VI_TO_EN from lang_wrapper
with open('lang_wrapper.py', 'r', encoding='utf-8') as f:
    wrapper_content = f.read()

# Check which ones are not translated
vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
vietnamese_chars += vietnamese_chars.upper()

def has_vietnamese(text):
    return any(c in vietnamese_chars for c in text)

untranslated = []
for text in set(matches):
    if has_vietnamese(text):
        # Check if in VI_TO_EN
        search = f'"{text}": "'
        if search in wrapper_content:
            # Check if translated (not same as key)
            pattern_check = f'"{re.escape(text)}": "{re.escape(text)}"'
            if re.search(pattern_check, wrapper_content):
                untranslated.append(text)
        else:
            untranslated.append(text)

print(f"Found {len(untranslated)} untranslated strings")

# Save to file
with open('untranslated_strings.txt', 'w', encoding='utf-8') as f:
    for text in sorted(untranslated):
        f.write(f"{text}\n")

print(f"\nSaved all to: untranslated_strings.txt")
