#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import customtkinter as ctk
import main_enhanced_auto
from lang_wrapper import t

main_enhanced_auto.CURRENT_LANG = "vi"

root = ctk.CTk()
root.geometry("400x200")

label = None

def update_ui():
    global label
    if label:
        label.destroy()
    text = t("Tốt")
    label = ctk.CTkLabel(root, text=f"t('Tốt') = {text}", font=("Arial", 20))
    label.pack(pady=20)

def toggle():
    main_enhanced_auto.CURRENT_LANG = "en" if main_enhanced_auto.CURRENT_LANG == "vi" else "vi"
    print(f"Toggled to: {main_enhanced_auto.CURRENT_LANG}")
    update_ui()

update_ui()
btn = ctk.CTkButton(root, text="Toggle Language", command=toggle)
btn.pack(pady=20)

root.mainloop()
