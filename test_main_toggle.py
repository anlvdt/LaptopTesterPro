#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Import main to initialize CURRENT_LANG
import main_enhanced_auto

# Import t after main
from lang_wrapper import t

print(f"Initial CURRENT_LANG: {main_enhanced_auto.CURRENT_LANG}")
print(f"t('Tốt') = {t('Tốt')}")

# Toggle
main_enhanced_auto.CURRENT_LANG = "en"
print(f"\nAfter toggle to en: {main_enhanced_auto.CURRENT_LANG}")
print(f"t('Tốt') = {t('Tốt')}")

# Toggle back
main_enhanced_auto.CURRENT_LANG = "vi"
print(f"\nAfter toggle to vi: {main_enhanced_auto.CURRENT_LANG}")
print(f"t('Tốt') = {t('Tốt')}")
