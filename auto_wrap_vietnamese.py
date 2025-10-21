#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Wrap Vietnamese Strings
Tự động wrap tất cả Vietnamese strings với t() function
"""

import re
import sys

def has_vietnamese(text):
    """Check if text contains Vietnamese characters"""
    vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
    vietnamese_chars += vietnamese_chars.upper()
    return any(c in vietnamese_chars for c in text)

def wrap_vietnamese_strings(content):
    """Wrap all Vietnamese strings with t()"""
    
    # Pattern to find text="..." or text='...'
    pattern = r'(text\s*=\s*)(["\']((?:[^"\'\\]|\\.)*?)["\'])'
    
    def replace_func(match):
        prefix = match.group(1)
        full_string = match.group(2)
        string_content = match.group(3)
        
        # Check if already wrapped with t()
        if 't(' in prefix or 't (' in prefix:
            return match.group(0)
        
        # Check if contains Vietnamese
        if has_vietnamese(string_content):
            quote = full_string[0]
            return f'{prefix}t({quote}{string_content}{quote})'
        
        return match.group(0)
    
    # Replace all matches
    result = re.sub(pattern, replace_func, content)
    
    return result

def main():
    input_file = 'main_enhanced_auto.py'
    output_file = 'main_enhanced_auto_wrapped.py'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Wrapping Vietnamese strings...")
    wrapped_content = wrap_vietnamese_strings(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(wrapped_content)
    
    # Count changes
    original_count = content.count('text=')
    wrapped_count = wrapped_content.count('t("') + wrapped_content.count("t('")
    
    print(f"\nDone!")
    print(f"Total text= occurrences: {original_count}")
    print(f"Wrapped with t(): {wrapped_count}")
    print(f"\nOutput saved to: {output_file}")

if __name__ == "__main__":
    main()
