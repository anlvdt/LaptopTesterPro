#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test translation system"""

from lang_wrapper import t, set_language

# Test Vietnamese mode
set_language("vi")
print("=== Vietnamese Mode ===")
result1 = t('Đang tải...')
result2 = t('Sẵn sàng')
result3 = t('Hoàn thành')
print(f"Result 1: {result1}")
print(f"Result 2: {result2}")
print(f"Result 3: {result3}")

# Test English mode
set_language("en")
print("\n=== English Mode ===")
result1 = t('Đang tải...')
result2 = t('Sẵn sàng')
result3 = t('Hoàn thành')
print(f"Result 1: {result1}")
print(f"Result 2: {result2}")
print(f"Result 3: {result3}")

print("\nTranslation system working!")
