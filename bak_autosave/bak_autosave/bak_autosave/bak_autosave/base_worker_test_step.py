class BaseWorkerTestStep(BaseStepFrame):
    def __init__(self, master, title, why_text, how_text, **kwargs):
        super().__init__(master, title=title, why_text=why_text, how_text=how_text, **kwargs)
        self.worker_process = None
        self.worker_queue = multiprocessing.Queue()
        self.is_testing = False

    def run_worker(self, worker_func, args_tuple=()):
        if self.is_testing: return 
        self.is_testing = True; self._completed = False
        try:
            final_args = (self.worker_queue,) + args_tuple
            self.worker_process = multiprocessing.Process(target=worker_func, args=final_args, daemon=True)
            self.worker_process.start()
            self.after(100, self.check_queue)
        except Exception as e:
            messagebox.showerror("Lỗi Worker", f"Lỗi khởi tạo Process: {e}")
            self.is_testing = False

    def stop_worker(self):
        self.is_testing = False 
        if self.worker_process and self.worker_process.is_alive():
            self.worker_process.terminate()
            self.worker_process.join(timeout=1)
        while not self.worker_queue.empty():
            try: self.worker_queue.get_nowait() # Clear queue
            except Exception: pass

    def check_queue(self):
        if not self.is_testing: return 
        try:
            while not self.worker_queue.empty(): self.handle_message(self.worker_queue.get_nowait())
        except Exception: pass # Ignore queue empty errors
        finally:
            if self.is_testing: self.after(200, self.check_queue)

    def handle_message(self, msg):
        if not self.is_testing: return
        msg_type = msg.get('type')
        try:
            if msg_type == 'error':
                messagebox.showerror("Lỗi Worker", msg.get('message', 'Lỗi không xác định'))
                self.stop_worker()
                self.mark_completed({"Kết quả": "Lỗi Worker", "Trạng thái": "Lỗi", "Chi tiết": msg.get('message', '')})
            elif msg_type == 'update': self.update_ui(msg)
            elif msg_type == 'result': self.finalize_test(msg)
            elif msg_type == 'status':
                if hasattr(self, 'status_label'): self.status_label.configure(text=msg.get('message', ''))
            elif msg_type == 'done':
                self.is_testing = False
                if not self._completed:
                    logger.info(f"Worker for step '{self.title}' finished. Finalizing test.")
                    self.finalize_test({'data': {}})
        except Exception as e: print(f"Error handling message: {e}")

    def update_ui(self, data): pass
    def finalize_test(self, data): pass
    def stop_tasks(self):
        super().stop_tasks()
        self.stop_worker()
