#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ'

# Find: "string with vietnamese" not preceded by t(
pattern = r'(?<!t\()("([^"]*[' + vietnamese_chars + r'][^"]*)")'

matches = re.findall(pattern, content)
print(f"Found {len(matches)} Vietnamese strings not wrapped")

# Show first 10
for i, (full, text) in enumerate(matches[:10], 1):
    print(f"{i}. {text[:50]}...")
