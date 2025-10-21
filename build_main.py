"""
Build Main - Final Entry Point for v2.7.9
"""
import sys
import os
import multiprocessing
import customtkinter

# Set dark mode globally before App initialization
customtkinter.set_appearance_mode("Dark")

# Fix frozen paths
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# Support multiprocessing in frozen app
multiprocessing.freeze_support()

from main_enhanced_auto import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
