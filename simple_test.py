import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from laptoptester import CURRENT_LANG, toggle_language, get_text

print("Initial language:", CURRENT_LANG)
print("Basic mode text:", repr(get_text('basic_mode')))

toggle_language()
print("After toggle:", CURRENT_LANG)  
print("Basic mode text:", repr(get_text('basic_mode')))

toggle_language()
print("After toggle back:", CURRENT_LANG)
print("Basic mode text:", repr(get_text('basic_mode')))

print("Language switching works!")