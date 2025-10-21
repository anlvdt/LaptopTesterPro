#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fix report layout - make it expand to full container
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read file
with open("main_enhanced_auto.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the scrollable frame pack line in create_simple_summary
# Old: scroll_frame.pack(fill="x", padx=20, pady=20)
# New: scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

old_line = '        scroll_frame.pack(fill="x", padx=20, pady=20)'
new_line = '        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)'

if old_line in content:
    content = content.replace(old_line, new_line)
    print("OK: Fixed scroll_frame.pack to use fill='both' and expand=True")
else:
    print("ERROR: Pattern not found")

# Write back
with open("main_enhanced_auto.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done!")
