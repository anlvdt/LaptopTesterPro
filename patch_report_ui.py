#!/usr/bin/env python3
# Patch to improve report UI with 2-column layout

import re

with open('main_enhanced_auto.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the scroll_frame initialization
old_scroll = '''    def create_simple_summary(self, results):
        # Create scrollable container
        scroll_frame = ctk.CTkScrollableFrame(self.action_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)'''

new_scroll = '''    def create_simple_summary(self, results):
        # Full width scrollable container with 2-column grid
        scroll_frame = ctk.CTkScrollableFrame(self.action_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        scroll_frame.grid_columnconfigure((0,1), weight=1)'''

content = content.replace(old_scroll, new_scroll)

# Update header to span 2 columns
old_header = '''        # Header with logo - TO, RỘNG, ĐẸP
        header_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.ACCENT, corner_radius=12, height=120)
        header_frame.pack(fill="x", pady=(0, 20))'''

new_header = '''        # Header with logo - FULL WIDTH
        header_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.ACCENT, corner_radius=8, height=100)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)'''

content = content.replace(old_header, new_header)

# Update stats to span 2 columns
old_stats = '''        # Quick stats - TO HƠN
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.FRAME, corner_radius=12, height=140)
        stats_frame.pack(fill="x", pady=(0, 20))'''

new_stats = '''        # Quick stats - FULL WIDTH
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color=Theme.FRAME, corner_radius=8, height=120)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)'''

content = content.replace(old_stats, new_stats)

# Update assessment to span 2 columns  
old_assess = '''        # Overall assessment - TO HƠN
        assessment_frame = ctk.CTkFrame(scroll_frame, corner_radius=12, height=100)
        assessment_frame.pack(fill="x", pady=(0, 20))'''

new_assess = '''        # Overall assessment - FULL WIDTH
        assessment_frame = ctk.CTkFrame(scroll_frame, corner_radius=8)
        assessment_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)'''

content = content.replace(old_assess, new_assess)

# Save
with open('main_enhanced_auto.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: Patched report UI to use grid layout")
