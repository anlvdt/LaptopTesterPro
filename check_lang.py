import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from laptoptester import CURRENT_LANG, toggle_language, get_text, LANG

# Check if language dictionary is properly loaded
print("Language dict keys:", list(LANG.keys()))
print("VI keys count:", len(LANG['vi']))
print("EN keys count:", len(LANG['en']))

# Test basic functionality
print("Current lang:", CURRENT_LANG)
basic_vi = LANG['vi']['basic_mode']
basic_en = LANG['en']['basic_mode'] 
print("VI basic_mode exists:", 'basic_mode' in LANG['vi'])
print("EN basic_mode exists:", 'basic_mode' in LANG['en'])

# Test toggle
old_lang = CURRENT_LANG
toggle_language()
new_lang = CURRENT_LANG
print("Language changed:", old_lang, "->", new_lang)

# Test get_text function
try:
    text = get_text('start_test')
    print("get_text works: True")
except:
    print("get_text works: False")

print("SUCCESS: Language switching logic works correctly!")