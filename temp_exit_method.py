    def confirm_exit(self):
        exit_text = "Hoàn thành kiểm tra!\n\nBạn có muốn thoát ứng dụng không?" if CURRENT_LANG == "vi" else "Testing completed!\n\nDo you want to exit the application?"
        title_text = "Hoàn thành" if CURRENT_LANG == "vi" else "Completed"
        
        result = messagebox.askyesno(title_text, exit_text)
        if result:
            self.app.quit_app() if self.app else None