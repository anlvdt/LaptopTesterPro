import re

with open("main.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all get_text() calls from LANG dictionary
content = re.sub(r'get_text\("([^"]+)"\)', r'"\1"', content)

# Fix specific problematic lines
content = content.replace('get_text("continue")', '"Tiếp tục"')
content = content.replace('get_text("skip")', '"Bỏ qua"')
content = content.replace('get_text("checking")', '"Đang kiểm tra"')
content = content.replace('get_text("ready_to_test")', '"Sẵn sàng test"')

with open("main.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all get_text errors in main.py")