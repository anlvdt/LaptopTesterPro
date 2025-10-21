"""
ui_main.py - Giao diện chính của LaptopTester
"""
import customtkinter as ctk
from ai_analyzer import ai_diagnoser
import importlib
import steps
import tkinter as tk
import threading
import os
from PIL import Image

class LaptopTesterApp(ctk.CTk):
    # ...existing code...
    def _load_icon(self, name, size=(22,22)):
        icon_path = os.path.join('assets', 'icons', f'{name}.png')
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize(size)
            return ctk.CTkImage(light_image=img, size=size)
        return None

    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("dark" if mode=="Light" else "light")

    def __init__(self):
        super().__init__()
        # Khởi tạo biến progress sau khi đã có root window
        self.progress_var = tk.DoubleVar(master=self, value=0)
        # Theme hiện đại, màu sắc nhất quán
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.title("LaptopTester - All-in-one Test")
        self.geometry("980x700")
        self.minsize(700, 480)
        self.resizable(True, True)
        self.bind('<Configure>', self._on_resize)

    def _on_resize(self, event):
        w, h = event.width, event.height
        # Điều chỉnh font và padding khi cửa sổ nhỏ
        widgets = ["header", "guide", "result_box", "ai_box", "button", "export_btn", "progress_bar"]
        if not all(hasattr(self, wname) for wname in widgets):
            return
        if w < 800:
            self.header.configure(font=("Segoe UI", 18, "bold"))
            self.guide.configure(font=("Segoe UI", 10))
            self.result_box.configure(font=("Segoe UI", 10))
            self.ai_box.configure(font=("Segoe UI", 9, "italic"))
            self.button.configure(font=("Segoe UI", 11, "bold"), height=32)
            self.export_btn.configure(font=("Segoe UI", 9), height=24)
            self.progress_bar.configure(width=180, height=8)
        else:
            self.header.configure(font=("Segoe UI", 26, "bold"))
            self.guide.configure(font=("Segoe UI", 13))
            self.result_box.configure(font=("Segoe UI", 13))
            self.ai_box.configure(font=("Segoe UI", 12, "italic"))
            self.button.configure(font=("Segoe UI", 15, "bold"), height=44)
            self.export_btn.configure(font=("Segoe UI", 12), height=34)
            self.progress_bar.configure(width=420, height=16)
        # Đảm bảo STEPS luôn đầy đủ khi khởi tạo
        if not steps.STEPS or len(steps.STEPS) < 3:
            import importlib
            importlib.reload(steps)
        self.steps = steps.STEPS
        self.current_step = 0
        self.results = {}
        # Sidebar nâng cấp
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color="#181c24", corner_radius=0, border_width=0)
        self.sidebar.pack(side="left", fill="y")
        logo = ctk.CTkLabel(self.sidebar, text="LaptopTester", font=("Segoe UI", 26, "bold"), text_color="#1faaff")
        logo.pack(pady=(28,16))
        self.theme_btn = ctk.CTkButton(self.sidebar, text="🌙/☀", width=48, height=40, command=self.toggle_theme, fg_color="#23272e", hover_color="#1faaff", corner_radius=12, font=("Segoe UI", 16, "bold"))
        self.theme_btn.pack(pady=(0,22))
        self.theme_btn.bind("<Enter>", lambda e: self._show_temp_tooltip(self.theme_btn, "Chuyển đổi giao diện sáng/tối"))
        self.theme_btn.bind("<Leave>", lambda e: self._hide_tooltip())
        self.step_buttons = []
        self.status_icons = []
        for idx, step in enumerate(self.steps):
            icon = self._load_icon(f"step{idx+1}", size=(28,28))
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{idx+1}. {step.name}",
                width=190,
                height=44,
                anchor="w",
                image=icon,
                compound="left",
                corner_radius=16,
                fg_color="#23272e",
                hover_color="#1faaff",
                text_color="#fff",
                font=("Segoe UI", 14, "bold"),
                command=lambda i=idx: self.goto_step(i)
            )
            btn.pack(pady=6, padx=18, fill="x")
            btn.bind("<Enter>", lambda e, i=idx: self._show_tooltip(i))
            btn.bind("<Leave>", lambda e: self._hide_tooltip())
            btn.bind("<FocusIn>", lambda e, i=idx: self._show_tooltip(i))
            btn.bind("<FocusOut>", lambda e: self._hide_tooltip())
            btn.configure(takefocus=True)
            self.step_buttons.append(btn)
            icon_lbl = ctk.CTkLabel(self.sidebar, text="", width=22, fg_color="#181c24")
            icon_lbl.place(x=200, y=110+idx*56)
            icon_lbl.bind("<Enter>", lambda e, i=idx: self._show_temp_tooltip(icon_lbl, f"Trạng thái bước {idx+1}"))
            icon_lbl.bind("<Leave>", lambda e: self._hide_tooltip())
            self.status_icons.append(icon_lbl)
    def _show_temp_tooltip(self, widget, text):
        if self.tooltip:
            self.tooltip.destroy()
        x = widget.winfo_rootx() + 60
        y = widget.winfo_rooty() + 10
        self.tooltip = tk.Toplevel(self)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"220x36+{x}+{y}")
        self.tooltip.configure(bg="#222")
        label = tk.Label(self.tooltip, text=text, bg="#222", fg="#fff", font=("Segoe UI", 10), wraplength=210, justify="left")
        label.pack(padx=8, pady=6)
    # Panel chính nâng cấp
        self.main_frame = ctk.CTkFrame(self, fg_color="#f7fafd")
        self.main_frame.pack(side="left", fill="both", expand=True)
        self.header = ctk.CTkLabel(self.main_frame, text="LAPTOP TESTER", font=("Segoe UI", 26, "bold"), text_color="#1faaff")
        self.header.pack(pady=(32,8))
        self.guide = ctk.CTkLabel(self.main_frame, text="Chọn bước test ở sidebar hoặc bấm nút để kiểm tra tuần tự.", font=("Segoe UI", 13), text_color="#222")
        self.guide.pack(pady=(0,14))
        self.result_box = ctk.CTkTextbox(self.main_frame, font=("Segoe UI", 13), wrap="word", height=140, fg_color="#fff", text_color="#222")
        self.result_box.pack(fill="both", expand=True, padx=18, pady=(0,12))
        self.ai_box = ctk.CTkTextbox(self.main_frame, font=("Segoe UI", 12, "italic"), wrap="word", height=44, fg_color="#eaf6ff", text_color="#005a9e")
        self.ai_box.pack(fill="x", padx=18, pady=(0,8))
        self.button = ctk.CTkButton(self.main_frame, text="Bắt đầu kiểm tra", command=self.next_step, font=("Segoe UI", 15, "bold"), height=44, corner_radius=12, fg_color="#1faaff", hover_color="#005a9e", text_color="#fff")
        self.button.pack(pady=(0,12))
        self.export_btn = ctk.CTkButton(self.main_frame, text="Xuất PDF", command=self.export_report, font=("Segoe UI", 12), height=34, corner_radius=10, fg_color="#23272e", hover_color="#1faaff", text_color="#fff")
        self.export_btn.pack(pady=(0,10))
        self.status_label = ctk.CTkLabel(self.main_frame, text="Trạng thái: Chưa hoàn thành", font=("Segoe UI", 11), text_color="#888")
        self.status_label.pack(pady=(0,8))
        self.status_labels = []
        for idx in range(len(self.steps)):
            lbl = ctk.CTkLabel(self.sidebar, text="", font=("Segoe UI", 11), text_color="#888", fg_color="#23272e")
            lbl.pack(pady=0, padx=16, anchor="w")
            self.status_labels.append(lbl)
        # DEBUG: Thêm label test vào sidebar và main_frame trước khi gọi self.show_step()
        self.debug_label_main = ctk.CTkLabel(self.main_frame, text="[DEBUG] Main frame", text_color="#f00")
        self.debug_label_main.pack(pady=10)
        self.debug_label_sidebar = ctk.CTkLabel(self.sidebar, text="[DEBUG] Sidebar", text_color="#0f0")
        self.debug_label_sidebar.pack(pady=10)
        self.show_step()
    def _show_tooltip(self, idx):
        if self.tooltip:
            self.tooltip.destroy()
        x = self.sidebar.winfo_rootx() + 200
        y = self.sidebar.winfo_rooty() + 70 + idx*38
        self.tooltip = tk.Toplevel(self)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"300x60+{x}+{y}")
        self.tooltip.configure(bg="#222")
        desc = self.steps[idx].description
        label = tk.Label(self.tooltip, text=desc, bg="#222", fg="#fff", font=("Segoe UI", 10), wraplength=290, justify="left")
        label.pack(padx=8, pady=6)

    def _hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        self.status_labels = []
        for idx in range(len(self.steps)):
            lbl = ctk.CTkLabel(self.sidebar, text="", font=("Segoe UI", 10), text_color="#888", fg_color="#23272e")
            lbl.pack(pady=0, padx=10, anchor="w")
            self.status_labels.append(lbl)
    # ...existing code...
    def export_report(self):
        # Sidebar tối giản rõ rệt
        self.sidebar = ctk.CTkFrame(self, width=120, fg_color="#222")
        self.sidebar.pack(side="left", fill="y")
        logo = ctk.CTkLabel(self.sidebar, text="LaptopTester", font=("Arial", 14, "bold"), text_color="#00bfff")
        logo.pack(pady=(10,6))
        self.step_buttons = []
        for idx, step in enumerate(self.steps):
            btn = ctk.CTkButton(self.sidebar, text=f"{idx+1}", width=36, height=36, corner_radius=18, fg_color="#444", hover_color="#00bfff", text_color="#fff", font=("Arial", 12, "bold"), command=lambda i=idx: self.goto_step(i))
            btn.pack(pady=4)
            self.step_buttons.append(btn)

        # Panel phải tối giản
        self.main_frame = ctk.CTkFrame(self, fg_color="#f5f6fa")
        self.main_frame.pack(side="left", fill="both", expand=True)
        self.header = ctk.CTkLabel(self.main_frame, text="LAPTOP TESTER", font=("Arial", 22, "bold"), text_color="#005a9e")
        self.header.pack(pady=(18,4))
        self.guide = ctk.CTkLabel(self.main_frame, text="Chọn bước test ở sidebar hoặc bấm nút để kiểm tra tuần tự.", font=("Arial", 12), text_color="#222")
        self.guide.pack(pady=(0,8))
        self.result_box = ctk.CTkTextbox(self.main_frame, font=("Arial", 12), wrap="word", height=120, fg_color="#fff", text_color="#222")
        self.result_box.pack(fill="both", expand=True, padx=12, pady=(0,8))
        self.button = ctk.CTkButton(self.main_frame, text="Bắt đầu kiểm tra", command=self.next_step, font=("Arial", 13, "bold"), height=36, corner_radius=10, fg_color="#00bfff", hover_color="#005a9e", text_color="#fff")
        self.button.pack(pady=(0,8))
        self.export_btn = ctk.CTkButton(self.main_frame, text="Xuất PDF", command=self.export_report, font=("Arial", 11), height=28, corner_radius=8, fg_color="#222", hover_color="#00bfff", text_color="#fff")
        self.export_btn.pack(pady=(0,8))
        self.status_label = ctk.CTkLabel(self.main_frame, text="Trạng thái: Chưa hoàn thành", font=("Arial", 10), text_color="#888")
        self.status_label.pack(pady=(0,4))
        self.tooltip = None
        self.show_step()

    def update_main_panel(self):
        # Hiệu ứng fade out panel chính
        try:
            for alpha in range(100, 0, -20):
                self.main_frame.update()
                self.main_frame.winfo_toplevel().attributes('-alpha', alpha/100)
                self.after(10)
        except Exception:
            pass
        # Cập nhật panel phải khi chuyển bước
        step = self.steps[self.current_step]
        self.header.configure(text=f"Bước {self.current_step+1}: {step.name}")
        self.guide.configure(text=step.description)
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", "Hãy đọc kỹ hướng dẫn bên trên rồi bấm nút bên dưới để kiểm tra.")
        self.result_box.configure(state="disabled")
        self.ai_box.configure(state="normal")
        self.ai_box.delete("0.0", "end")
        self.ai_box.insert("0.0", "")
        self.ai_box.configure(state="disabled")
        self.button.configure(state="normal", text="Kiểm tra bước này", command=self.run_step)
        self.status_label.configure(text=f"Trạng thái: Đang kiểm tra bước {self.current_step+1}/{len(self.steps)}")
        # Cập nhật progress bar
        progress = (self.current_step) / max(1, len(self.steps)-1)
        self.progress_var.set(progress)
        # Hiệu ứng fade in panel chính
        try:
            for alpha in range(0, 101, 20):
                self.main_frame.update()
                self.main_frame.winfo_toplevel().attributes('-alpha', alpha/100)
                self.after(10)
            self.main_frame.winfo_toplevel().attributes('-alpha', 1.0)
        except Exception:
            pass

    def run_step(self):
        import matplotlib.pyplot as plt
        import os
        import tempfile
        import threading
        step = self.steps[self.current_step]
        # Hiệu ứng loading rõ ràng
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", "⏳ Đang kiểm tra, vui lòng chờ...")
        self.result_box.configure(state="disabled")
        self.ai_box.configure(state="normal")
        self.ai_box.delete("0.0", "end")
        self.ai_box.insert("0.0", "")
        self.ai_box.configure(state="disabled")
        self.button.configure(state="disabled", text="Đang kiểm tra...")
        self.status_label.configure(text=f"Trạng thái: Đang kiểm tra bước {self.current_step+1}/{len(self.steps)}")
        self.update_status_labels()
        # Module test màn hình trực tiếp
        if 'màn hình' in step.name.lower():
            self.run_screen_test()
            self.button.configure(state="normal", text="Tiếp tục", command=self.next_step)
            return
        # Module test bàn phím trực tiếp
        if 'bàn phím' in step.name.lower():
            self.run_keyboard_test()
            self.button.configure(state="normal", text="Tiếp tục", command=self.next_step)
            return

        def do_test():
            result = step.run()
            self.results[step.name] = result
            def update_ui():
                self.result_box.configure(state="normal")
                self.result_box.delete("0.0", "end")
                # Thêm icon trạng thái vào kết quả
                icon = ""
                if isinstance(result, str):
                    if any(x in result.lower() for x in ["tốt", "ok", "đạt", "passed", "hoạt động tốt"]):
                        icon = "✔ "
                    elif any(x in result.lower() for x in ["liệt", "fail", "lỗi", "chưa nhấn", "cảnh báo"]):
                        icon = "⚠ "
                    elif any(x in result.lower() for x in ["không đạt", "hỏng", "error"]):
                        icon = "✖ "
                if isinstance(result, str) and 'cpu_chart.png' in result:
                    img_path = os.path.join(tempfile.gettempdir(), 'cpu_chart.png')
                    if os.path.exists(img_path):
                        from PIL import Image
                        img = Image.open(img_path)
                        img = img.resize((300, 120))
                        img_tk = ctk.CTkImage(light_image=img, size=(300,120))
                        img_label = ctk.CTkLabel(self.result_frame, image=img_tk, text="")
                        img_label.image = img_tk
                        img_label.pack(side="bottom", pady=5)
                    self.result_box.insert("0.0", icon + result)
                else:
                    self.result_box.insert("0.0", icon + str(result))
                self.result_box.configure(state="disabled")
                ai_msg = ""
                if 'CPU' in step.name.upper():
                    ai_msg = ai_diagnoser.analyze_cpu({'avg_cpu_usage': self._extract_avg_cpu(result), 'max_temperature': self._extract_temp(result)})
                elif 'Ổ cứng' in step.name or 'Disk' in step.name:
                    ai_msg = ai_diagnoser.analyze_disk({'write_speed': self._extract_speed(result, 'Ghi'), 'read_speed': self._extract_speed(result, 'Đọc')})
                elif 'Pin' in step.name:
                    ai_msg = ai_diagnoser.analyze_battery({'health': self._extract_battery_health(result)})
                if ai_msg and isinstance(ai_msg, dict) and 'ai_warning' in ai_msg:
                    self.ai_box.configure(state="normal")
                    self.ai_box.delete("0.0", "end")
                    self.ai_box.insert("0.0", f"AI cảnh báo: {ai_msg['ai_warning']}")
                    self.ai_box.configure(state="disabled")
                else:
                    self.ai_box.configure(state="normal")
                    self.ai_box.delete("0.0", "end")
                    self.ai_box.insert("0.0", "")
                    self.ai_box.configure(state="disabled")
                self.button.configure(state="normal", text="Tiếp tục", command=self.next_step)
                self.update_status_labels()
                # Nếu đã hoàn thành tất cả các bước, lưu lịch sử test
                if self.current_step == len(self.steps) - 1:
                    self.save_test_history()
            self.after(100, update_ui)
        t = threading.Thread(target=do_test)
        t.start()

    def save_test_history(self):
        import json
        import datetime
        history_file = os.path.join(os.path.dirname(__file__), 'test_history.json')
        entry = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results': self.results.copy()
        }
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            data.append(entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi lưu lịch sử test: {e}")

    def run_screen_test(self):
        # Hiển thị các màu cơ bản, chuyển đổi nhanh
        win = tk.Toplevel(self)
        win.title("Test màn hình trực tiếp")
        win.geometry("700x400")
        colors = [
            ("Trắng", "#FFFFFF"),
            ("Đen", "#000000"),
            ("Đỏ", "#FF0000"),
            ("Xanh lá", "#00FF00"),
            ("Xanh dương", "#0000FF"),
            ("Vàng", "#FFFF00"),
            ("Tím", "#800080")
        ]
        idx = [0]
        frame = tk.Frame(win, bg=colors[0][1])
        frame.pack(fill="both", expand=True)
        label = tk.Label(frame, text=colors[0][0], font=("Segoe UI", 32), bg=colors[0][1], fg="#222")
        label.pack(pady=10)
        def next_color():
            idx[0] = (idx[0]+1)%len(colors)
            frame.config(bg=colors[idx[0]][1])
            label.config(text=colors[idx[0]][0], bg=colors[idx[0]][1])
        btn = tk.Button(frame, text="Chuyển màu", font=("Segoe UI", 16), command=next_color)
        btn.pack(pady=20)
        win.transient(self)
        win.grab_set()
        win.wait_window()
        self.results[self.steps[self.current_step].name] = "Đã test trực tiếp các màu cơ bản."
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", "Đã test trực tiếp các màu cơ bản.")
        self.result_box.configure(state="disabled")
        self.button.configure(text="Tiếp tục", command=self.next_step)
        self.update_status_labels()

    def run_keyboard_test(self):
        # Hiển thị phím nhấn, phát hiện phím liệt
        win = tk.Toplevel(self)
        win.title("Test bàn phím trực tiếp")
        win.geometry("700x300")
        pressed = set()
        keys = [chr(i) for i in range(65,91)] + [str(i) for i in range(10)]
        key_labels = {}
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)
        def on_key(event):
            k = event.keysym.upper()
            if k in key_labels:
                key_labels[k].config(bg="#8f8")
                pressed.add(k)
        win.bind("<Key>", on_key)
        row = 0
        col = 0
        for k in keys:
            lbl = tk.Label(frame, text=k, width=4, height=2, relief="ridge", bg="#eee", font=("Segoe UI", 14))
            lbl.grid(row=row, column=col, padx=2, pady=2)
            key_labels[k] = lbl
            col += 1
            if (col >= 10 and row == 0) or (col >= 13):
                row += 1
                col = 0
        def finish():
            missed = [k for k in keys if k not in pressed]
            msg = "Tất cả phím đều hoạt động tốt." if not missed else f"Phím chưa nhấn/khả năng liệt: {', '.join(missed)}"
            self.results[self.steps[self.current_step].name] = msg
            self.result_box.configure(state="normal")
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", msg)
            self.result_box.configure(state="disabled")
            win.destroy()
            self.button.configure(text="Tiếp tục", command=self.next_step)
            self.update_status_labels()
        btn = tk.Button(frame, text="Kết thúc test", font=("Segoe UI", 14), command=finish)
        btn.grid(row=row+1, column=0, columnspan=13, pady=10)
        win.transient(self)
        win.grab_set()
        win.wait_window()
    def update_status_labels(self):
        for idx, lbl in enumerate(self.status_labels):
            icon_lbl = self.status_icons[idx]
            if self.steps[idx].name in self.results:
                lbl.configure(text="✔ Đã test", text_color="#0a0", font=("Segoe UI", 10, "bold"))
                icon_lbl.configure(text="✔", text_color="#0a0")
                self.step_buttons[idx].configure(fg_color="#1e2b1e")
            elif idx == self.current_step:
                lbl.configure(text="→ Đang chọn", text_color="#00bfff", font=("Segoe UI", 10, "bold"))
                icon_lbl.configure(text="⏳", text_color="#00bfff")
                self.step_buttons[idx].configure(fg_color="#003366")
            else:
                lbl.configure(text="", text_color="#888", font=("Segoe UI", 10))
                icon_lbl.configure(text="", text_color="#888")
                self.step_buttons[idx].configure(fg_color="#2d323b")

    def _extract_avg_cpu(self, text):
        import re
        m = re.search(r'Tải trung bình: ([\d\.]+)%', text)
        return float(m.group(1)) if m else 0
    def _extract_temp(self, text):
        import re
        m = re.search(r'Nhiệt độ: ([\d\.]+)', text)
        return float(m.group(1)) if m else 0
    def _extract_speed(self, text, key):
        import re
        m = re.search(rf'{key}: ([\d\.]+)', text)
        return float(m.group(1)) if m else 0
    def _extract_battery_health(self, text):
        import re
        m = re.search(r'Pin: ([\d\.]+)%', text)
        return float(m.group(1)) if m else 100

    def next_step(self):
        self.current_step += 1
        self.show_step()
        # Cập nhật progress bar khi chuyển bước
        progress = (self.current_step) / max(1, len(self.steps)-1)
        self.progress_var.set(progress)

    def show_summary(self):
        summary = "\n==============================\n"
        summary += "      🏁  TỔNG KẾT KIỂM TRA  🏁\n"
        summary += "==============================\n\n"
        for k, v in self.results.items():
            icon = ""
            vstr = str(v)
            if any(x in vstr.lower() for x in ["tốt", "ok", "đạt", "passed", "hoạt động tốt"]):
                icon = "✔ "
            elif any(x in vstr.lower() for x in ["liệt", "fail", "lỗi", "chưa nhấn", "cảnh báo"]):
                icon = "⚠ "
            elif any(x in vstr.lower() for x in ["không đạt", "hỏng", "error"]):
                icon = "✖ "
            summary += f"{icon}{k}: {v}\n"
        ai_summary = ai_diagnoser.analyze_summary(self.results)
        summary += "\n=== ĐÁNH GIÁ AI ===\n"
        for suggestion in ai_summary.get('ai_summary', []):
            if suggestion and 'ai_warning' in suggestion:
                summary += f"- {suggestion['ai_warning']}\n"
        summary += "\n==============================\n"
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", summary)
        self.result_box.configure(state="disabled")

def run_app():
    app = LaptopTesterApp()
    app.mainloop()
