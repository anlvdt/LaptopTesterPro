#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace quit_app function
old_quit = '''    def quit_app(self):

        self.clear_window()
        self.destroy()'''

new_quit = '''    def quit_app(self):
        # Open affiliate link when closing app
        try:
            import webbrowser
            webbrowser.open("https://s.shopee.vn/7AUkbxe8uu")
        except:
            pass
        
        self.clear_window()
        self.destroy()'''

content = content.replace(old_quit, new_quit)

# Add protocol handler after show_mode_selection
old_init = '''        self.show_mode_selection()

    def clear_window(self):'''

new_init = '''        # Handle window close button (X)
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.show_mode_selection()

    def clear_window(self):'''

content = content.replace(old_init, new_init)

with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Added affiliate link to quit_app and WM_DELETE_WINDOW protocol")
