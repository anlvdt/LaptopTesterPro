#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Wrap Vietnamese Strings - Fixed Version
Chỉ wrap các string đơn giản, không wrap string phức tạp có if/else
"""

import re

def has_vietnamese(text):
    """Check if text contains Vietnamese characters"""
    vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
    vietnamese_chars += vietnamese_chars.upper()
    return any(c in vietnamese_chars for c in text)

def wrap_vietnamese_strings(content):
    """Wrap only simple Vietnamese strings with t()"""
    
    # Pattern: text="simple string" (không có if/else trong cùng dòng)
    pattern = r'(\btext\s*=\s*)(["\']((?:[^"\'\\]|\\.)*?)["\'])(?!\s+if\b)'
    
    def replace_func(match):
        prefix = match.group(1)
        full_string = match.group(2)
        string_content = match.group(3)
        
        # Skip if already wrapped
        if 't(' in prefix or 't (' in prefix:
            return match.group(0)
        
        # Skip if string is too long (likely complex)
        if len(string_content) > 200:
            return match.group(0)
        
        # Skip if contains special patterns
        if '\\u' in string_content or '{' in string_content:
            return match.group(0)
        
        # Only wrap if contains Vietnamese
        if has_vietnamese(string_content):
            quote = full_string[0]
            return f'{prefix}t({quote}{string_content}{quote})'
        
        return match.group(0)
    
    result = re.sub(pattern, replace_func, content)
    return result

def main():
    input_file = 'main_enhanced_auto.py'
    output_file = 'main_enhanced_auto.py'
    backup_file = 'main_enhanced_auto_before_wrap.py'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    print(f"Creating backup: {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Wrapping simple Vietnamese strings...")
    wrapped_content = wrap_vietnamese_strings(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(wrapped_content)
    
    # Count changes
    wrapped_count = wrapped_content.count('text=t(')
    
    print(f"\nDone!")
    print(f"Wrapped simple strings: {wrapped_count}")
    print(f"Backup saved to: {backup_file}")

if __name__ == "__main__":
    main()
