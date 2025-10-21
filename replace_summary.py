#!/usr/bin/env python3
# Script to replace create_simple_summary function

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('new_summary.py', 'r', encoding='utf-8') as f:
    new_function = f.read()

# Find start and end of create_simple_summary
start_idx = None
end_idx = None
indent_level = 0

for i, line in enumerate(lines):
    if 'def create_simple_summary(self, results):' in line:
        start_idx = i
        continue
    
    if start_idx is not None and end_idx is None:
        if line.strip() and not line[0].isspace():
            # Found next function at root level
            end_idx = i
            break
        elif line.strip().startswith('def ') and line[0:4] == '    ':
            # Found next method at same indentation level
            end_idx = i
            break

if start_idx and end_idx:
    # Replace the function - add proper indentation
    indented_function = '\n'.join('    ' + line if line.strip() else line for line in new_function.split('\n'))
    new_lines = lines[:start_idx] + [indented_function + '\n'] + lines[end_idx:]
    
    with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"OK Replaced create_simple_summary (lines {start_idx+1} to {end_idx})")
else:
    print("ERROR Could not find function boundaries")
