import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main_enhanced_auto.py',
    '--name=LaptopTester',
    '--onefile',
    '--windowed',
    '--icon=assets/icons/logo.png',
    '--add-data=assets;assets',
    '--add-data=bin;bin',
    '--hidden-import=customtkinter',
    '--hidden-import=PIL._tkinter_finder',
    '--collect-all=customtkinter',
    '--noconsole',
    '--clean',
])
