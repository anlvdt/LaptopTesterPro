#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_gettext_in_dict():
    with open("laptoptester.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all get_text() calls from LANG dictionary
    content = re.sub(r'get_text\("([^"]+)"\)', r'"\1"', content)
    
    with open("laptoptester.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed get_text errors in LANG dictionary")

if __name__ == "__main__":
    fix_gettext_in_dict()