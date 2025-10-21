#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-apply translation wrapper to all Vietnamese strings
"""

import re
import shutil

def apply_translation_fix():
    input_file = 'main_enhanced_auto.py'
    output_file = 'main_enhanced_auto_translated.py'
    backup_file = 'main_enhanced_auto_backup.py'
    
    # Backup original
    shutil.copy(input_file, backup_file)
    print(f"✓ Backup created: {backup_file}")
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Add import at the top (after translator import)
    import_pattern = r'(from translator import translate, translate_dict\n    TRANSLATOR_AVAILABLE = True)'
    import_replacement = r'\1\n    from lang_wrapper import t, set_language as set_wrapper_language'
    content = re.sub(import_pattern, import_replacement, content)
    
    # Step 2: Update fallback imports
    fallback_pattern = r'(def translate\(text\): return text\n    def translate_dict\(data\): return data)'
    fallback_replacement = r'\1\n    def t(text): return text\n    def set_wrapper_language(lang): pass'
    content = re.sub(fallback_pattern, fallback_replacement, content)
    
    # Step 3: Update toggle_language function
    toggle_pattern = r'(def toggle_language\(\):\n    global CURRENT_LANG\n    CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi")'
    toggle_replacement = r'\1\n    if TRANSLATOR_AVAILABLE:\n        set_wrapper_language(CURRENT_LANG)'
    content = re.sub(toggle_pattern, toggle_replacement, content)
    
    # Step 4: Wrap all Vietnamese strings with t()
    # Pattern to find Vietnamese strings
    vietnamese_pattern = r'text="([^"]*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^"]*)"'
    
    def replace_vietnamese(match):
        text = match.group(1)
        # Skip if already wrapped
        if match.group(0).startswith('text=t('):
            return match.group(0)
        return f'text=t("{text}")'
    
    content = re.sub(vietnamese_pattern, replace_vietnamese, content)
    
    # Step 5: Also wrap f-strings with Vietnamese
    fstring_pattern = r'text=f"([^"]*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ][^"]*)"'
    
    def replace_fstring(match):
        text = match.group(1)
        if '{' in text:  # Has variables
            return f'text=t(f"{text}")'
        return f'text=t("{text}")'
    
    content = re.sub(fstring_pattern, replace_fstring, content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Translation applied: {output_file}")
    print(f"\nTo use the fixed version:")
    print(f"1. Review {output_file}")
    print(f"2. If OK: copy {output_file} to {input_file}")
    print(f"3. Backup is at: {backup_file}")

if __name__ == "__main__":
    print("Applying translation fix...")
    apply_translation_fix()
    print("\n✅ Done!")
