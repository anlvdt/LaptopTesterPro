#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from lang_wrapper import t, set_language, get_language

print(f"Initial: {get_language()}")
r1 = t("Tốt")
print(f"t('Tốt') = {r1}")

set_language("en")
print(f"\nAfter en: {get_language()}")
r2 = t("Tốt")
print(f"t('Tốt') = {r2}")
