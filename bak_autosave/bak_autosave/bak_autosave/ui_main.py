"""
ui_main.py - Giao diện chính của LaptopTester
"""
import customtkinter as ctk
from ai_analyzer import ai_diagnoser
import importlib
import steps

class LaptopTesterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LaptopTester - Dễ dùng cho mọi người")
        self.geometry("700x500")
        self.resizable(False, False)
        self.steps = steps.STEPS
        self.current_step = 0
        self.results = {}
        self.header = ctk.CTkLabel(self, text="Chào mừng bạn đến với LaptopTester!", font=("Segoe UI", 24, "bold"))
        self.header.pack(pady=15)
        self.guide = ctk.CTkLabel(self, text="Chỉ cần bấm nút và làm theo hướng dẫn. Không cần biết công nghệ!", font=("Segoe UI", 16))
        self.guide.pack(pady=5)
        self.result_box = ctk.CTkTextbox(self, font=("Segoe UI", 14), wrap="word", height=200)
        self.result_box.pack(fill="both", expand=True, padx=20, pady=10)
        self.button = ctk.CTkButton(self, text="Bắt đầu kiểm tra", command=self.next_step, font=("Segoe UI", 18), height=50)
        self.button.pack(pady=20)
        self.show_step()

    def show_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.header.configure(text=f"Bước {self.current_step+1}: {step.name}")
            self.guide.configure(text=step.description)
            self.result_box.configure(state="normal")
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", "Hãy đọc kỹ hướng dẫn bên trên rồi bấm nút bên dưới để kiểm tra.")
            self.result_box.configure(state="disabled")
            self.button.configure(text="Kiểm tra bước này", command=self.run_step)
        else:
            self.header.configure(text="Hoàn tất kiểm tra!")
            self.guide.configure(text="Bạn đã hoàn thành tất cả các bước. Xem tổng kết bên dưới.")
            self.show_summary()
            self.button.configure(text="Thoát", command=self.quit)

    def run_step(self):
        step = self.steps[self.current_step]
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", "Đang kiểm tra, vui lòng chờ...")
        self.result_box.update()
        result = step.run()
        self.results[step.name] = result
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", result)
        self.result_box.configure(state="disabled")
        self.button.configure(text="Tiếp tục", command=self.next_step)

    def next_step(self):
        self.current_step += 1
        self.show_step()

    def show_summary(self):
        summary = "--- Tổng kết kiểm tra ---\n"
        for k, v in self.results.items():
            summary += f"{k}: {v}\n"
        ai_summary = ai_diagnoser.analyze_summary(self.results)
        summary += "\n=== ĐÁNH GIÁ AI ===\n"
        for suggestion in ai_summary.get('ai_summary', []):
            if suggestion and 'ai_warning' in suggestion:
                summary += f"- {suggestion['ai_warning']}\n"
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", summary)
        self.result_box.configure(state="disabled")

def run_app():
    app = LaptopTesterApp()
    app.mainloop()
