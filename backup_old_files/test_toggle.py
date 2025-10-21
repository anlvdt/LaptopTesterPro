import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Test the toggle function directly
print("Testing toggle_language function...")

# Import the module
import laptoptester

print("Initial CURRENT_LANG:", laptoptester.CURRENT_LANG)

# Call toggle function
print("Calling toggle_language()...")
laptoptester.toggle_language()

print("After toggle CURRENT_LANG:", laptoptester.CURRENT_LANG)

# Toggle again
print("Calling toggle_language() again...")
laptoptester.toggle_language()

print("After second toggle CURRENT_LANG:", laptoptester.CURRENT_LANG)

# Test if language actually changes
if laptoptester.CURRENT_LANG == "vi":
    print("SUCCESS: Language switching works!")
else:
    print("ERROR: Language not switching properly")

# Test get_text function
try:
    text_vi = laptoptester.LANG['vi']['basic_mode']
    text_en = laptoptester.LANG['en']['basic_mode']
    print("VI text exists:", len(text_vi) > 0)
    print("EN text exists:", len(text_en) > 0)
    print("Texts are different:", text_vi != text_en)
except Exception as e:
    print("Error accessing language dict:", e)