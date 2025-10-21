#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test language toggle"""

from lang_wrapper import t, set_language, get_language

print(f"Initial lang: {get_language()}")
result1 = t('Đang tải...')
print(f"Result: {result1}")

set_language("en")
print(f"\nAfter set_language('en'): {get_language()}")
result2 = t('Đang tải...')
print(f"Result: {result2}")

set_language("vi")
print(f"\nAfter set_language('vi'): {get_language()}")
result3 = t('Đang tải...')
print(f"Result: {result3}")
