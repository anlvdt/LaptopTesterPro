#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrap all checklist items with t()"""
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: "✓ text" in list
pattern = r'(\s+)("✓[^"]+"|"⚠️[^"]+")'

def replace_func(match):
    indent = match.group(1)
    string = match.group(2)
    # Wrap with t()
    return f'{indent}t({string})'

new_content = re.sub(pattern, replace_func, content)

# Count
count = new_content.count('t("✓') - content.count('t("✓')
count += new_content.count('t("⚠️') - content.count('t("⚠️')

# Write
with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Wrapped {count} checklist items")
