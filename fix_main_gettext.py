import re

with open("main.py", 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'get_text\("([^"]+)"\)', r'"\1"', content)

with open("main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed get_text errors in main.py")