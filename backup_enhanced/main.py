"""
main.py - Điểm khởi động ứng dụng LaptopTester mới
"""
import multiprocessing
import sys
import os
import platform
from laptoptester import App

if __name__ == "__main__":
    multiprocessing.freeze_support()
    if getattr(sys, 'frozen', False):
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            pass
    
    app = App()
    app.mainloop()
