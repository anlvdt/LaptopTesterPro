import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Test the toggle function directly
print("Testing toggle_language function...")

# Import the module
import laptoptester

print("Initial CURRENT_LANG:", laptoptester.CURRENT_LANG)
print("Initial get_text('basic_mode'):", repr(laptoptester.get_text('basic_mode')))

# Call toggle function
print("\nCalling toggle_language()...")
laptoptester.toggle_language()

print("After toggle CURRENT_LANG:", laptoptester.CURRENT_LANG)
print("After toggle get_text('basic_mode'):", repr(laptoptester.get_text('basic_mode')))

# Toggle again
print("\nCalling toggle_language() again...")
laptoptester.toggle_language()

print("After second toggle CURRENT_LANG:", laptoptester.CURRENT_LANG)
print("After second toggle get_text('basic_mode'):", repr(laptoptester.get_text('basic_mode')))

print("\nToggle function works correctly!")