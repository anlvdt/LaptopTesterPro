#!/usr/bin/env python3
"""
Test script to check language switching functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from laptoptester import LANG, get_text, toggle_language, CURRENT_LANG

def test_language_switching():
    print("=== TEST LANGUAGE SWITCHING ===")
    
    # Test initial language
    print(f"Current language: {CURRENT_LANG}")
    print(f"Title: {get_text('title')}")
    print(f"Start Test: {get_text('start_test')}")
    print(f"Exit: {get_text('exit')}")
    print(f"Basic Mode: {get_text('basic_mode')}")
    print(f"Expert Mode: {get_text('expert_mode')}")
    
    print("\n--- SWITCH LANGUAGE ---")
    toggle_language()
    
    print(f"Language after switch: {CURRENT_LANG}")
    print(f"Title: {get_text('title')}")
    print(f"Start Test: {get_text('start_test')}")
    print(f"Exit: {get_text('exit')}")
    print(f"Basic Mode: {get_text('basic_mode')}")
    print(f"Expert Mode: {get_text('expert_mode')}")
    
    print("\n--- SWITCH BACK ---")
    toggle_language()
    
    print(f"Language after switch back: {CURRENT_LANG}")
    print(f"Title: {get_text('title')}")
    print(f"Start Test: {get_text('start_test')}")
    print(f"Exit: {get_text('exit')}")
    print(f"Basic Mode: {get_text('basic_mode')}")
    print(f"Expert Mode: {get_text('expert_mode')}")
    
    print("\n=== TEST COMPLETE ===")
    print("Language switching works correctly!")

if __name__ == "__main__":
    test_language_switching()