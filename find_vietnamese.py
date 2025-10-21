#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find remaining Vietnamese text in main.py"""
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find strings with Vietnamese characters
vietnamese_chars = 'ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ'
pattern = f'["\']([^"\'\\n]*[{vietnamese_chars}]+[^"\'\\n]*)["\']'

matches = re.findall(pattern, content)
unique_matches = sorted(set(matches))

with open('vietnamese_found.txt', 'w', encoding='utf-8') as out:
    out.write(f"Found {len(unique_matches)} unique Vietnamese strings:\n")
    out.write("=" * 80 + "\n")
    for i, match in enumerate(unique_matches, 1):
        out.write(f"{i}. {match}\n")

print(f"Found {len(unique_matches)} Vietnamese strings. Saved to vietnamese_found.txt")
