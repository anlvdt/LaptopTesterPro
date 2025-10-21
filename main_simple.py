#!/usr/bin/env python3
"""
LaptopTester Pro - Main File Simple
"""

import multiprocessing
import sys
import os

# Import từ backup_enhanced
try:
    from backup_enhanced.laptoptester import *
    print("[INFO] Successfully imported from backup_enhanced")
    
    if __name__ == "__main__":
        multiprocessing.freeze_support()
        if getattr(sys, 'frozen', False):
            try:
                os.chdir(sys._MEIPASS)
            except Exception:
                pass
        
        import customtkinter as ctk
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        try:
            app = App()
            app.mainloop()
        except Exception as e:
            print(f"Error starting application: {e}")
            import traceback
            traceback.print_exc()
            
except ImportError as e:
    print(f"[ERROR] Could not import from backup_enhanced: {e}")
    print("Please ensure backup_enhanced/laptoptester.py exists and is complete")
    sys.exit(1)
