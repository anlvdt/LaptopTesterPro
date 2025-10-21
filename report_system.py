# -*- coding: utf-8 -*-
"""
Professional Report Generation System for LaptopTester
Hệ thống tạo báo cáo chuyên nghiệp
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
from datetime import datetime
import os
from typing import Dict, List, Any, Optional
import threading

try:
    from laptoptester import Theme, get_text
    from intro_guide_frames import create_home_button
except ImportError:
    class Theme:
        BACKGROUND = "#FAFBFC"
        FRAME = "#FFFFFF"
        ACCENT = "#4299E1"
        SUCCESS = "#38A169"
        WARNING = "#D69E2E"
        ERROR = "#E53E3E"
        TEXT = "#1A202C"
        TEXT_SECONDARY = "#718096"
        HEADING_FONT = ("Segoe UI", 24, "bold")
        SUBHEADING_FONT = ("Segoe UI", 18, "bold")
        BODY_FONT = ("Segoe UI", 14)
        CORNER_RADIUS = 12
        BUTTON_HEIGHT = 40
    
    def get_text(key): return key
    def create_home_button(parent, command, **kwargs): 
        return ctk.CTkButton(parent, text="🏠 HOME", command=command, **kwargs)

class ReportGenerator:
    """Professional report generator"""
    
    def __init__(self):
        self.templates = {
            "basic": "Báo cáo cơ bản",
            "detailed": "Báo cáo chi tiết", 
            "executive": "Báo cáo điều hành",
            "technical": "Báo cáo kỹ thuật"
        }
    
    def generate_html_report(self, results: Dict[str, Any], template: str = "detailed") -> str:
        """Tạo báo cáo HTML"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Calculate summary stats
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LaptopTester - Báo Cáo Kiểm Tra</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8fafc; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px 12px 0 0; }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }}
        .stat-card {{ background: #f8fafc; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #4299e1; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #2d3748; }}
        .stat-label {{ color: #718096; margin-top: 5px; }}
        .results {{ padding: 0 30px 30px; }}
        .test-item {{ background: #f8fafc; margin: 10px 0; padding: 20px; border-radius: 8px; border-left: 4px solid #e2e8f0; }}
        .test-item.success {{ border-left-color: #38a169; }}
        .test-item.warning {{ border-left-color: #d69e2e; }}
        .test-item.error {{ border-left-color: #e53e3e; }}
        .test-name {{ font-weight: bold; font-size: 1.1em; margin-bottom: 10px; }}
        .test-status {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.9em; font-weight: bold; }}
        .status-good {{ background: #c6f6d5; color: #22543d; }}
        .status-warning {{ background: #faf089; color: #744210; }}
        .status-error {{ background: #fed7d7; color: #742a2a; }}
        .footer {{ text-align: center; padding: 20px; color: #718096; border-top: 1px solid #e2e8f0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💻 LaptopTester Pro</h1>
            <p>Báo cáo kiểm tra laptop toàn diện - {timestamp}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">{total_tests}</div>
                <div class="stat-label">Tổng số test</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{passed_tests}</div>
                <div class="stat-label">Test đạt</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{success_rate:.1f}%</div>
                <div class="stat-label">Tỷ lệ thành công</div>
            </div>
        </div>
        
        <div class="results">
            <h2>📋 Chi tiết kết quả</h2>
        """
        
        for test_name, result in results.items():
            status = result.get("Trạng thái", "Không rõ")
            result_text = result.get("Kết quả", "N/A")
            details = result.get("Chi tiết", "")
            
            css_class = "success" if status == "Tốt" else "warning" if status == "Cảnh báo" else "error"
            status_class = "status-good" if status == "Tốt" else "status-warning" if status == "Cảnh báo" else "status-error"
            
            html_content += f"""
            <div class="test-item {css_class}">
                <div class="test-name">{test_name}</div>
                <span class="test-status {status_class}">{status}</span>
                <p><strong>Kết quả:</strong> {result_text}</p>
                {f'<p><strong>Chi tiết:</strong> {details}</p>' if details else ''}
            </div>
            """
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>Báo cáo được tạo bởi LaptopTester Pro | © 2024 LaptopTester Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content
    
    def export_json(self, results: Dict[str, Any], filepath: str):
        """Xuất JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "results": results,
            "summary": {
                "total_tests": len(results),
                "passed_tests": sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt"),
                "success_rate": (sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt")/len(results)*100) if results else 0
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    def export_csv(self, results: Dict[str, Any], filepath: str):
        """Xuất CSV"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Test Name", "Status", "Result", "Details"])
            
            for test_name, result in results.items():
                writer.writerow([
                    test_name,
                    result.get("Trạng thái", "N/A"),
                    result.get("Kết quả", "N/A"),
                    result.get("Chi tiết", "")
                ])

class ReportFrame(ctk.CTkFrame):
    """Report generation and export frame"""
    
    def __init__(self, master, results: Dict[str, Any], on_back=None):
        super().__init__(master, fg_color="transparent")
        self.results = results
        self.on_back = on_back
        self.report_generator = ReportGenerator()
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, height=80, corner_radius=Theme.CORNER_RADIUS)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        if self.on_back:
            back_btn = create_home_button(header_frame, command=self.on_back, text="← QUAY LẠI", width=120, height=40)
            back_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(header_frame, text="📊 BÁO CÁO & XUẤT DỮ LIỆU", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).grid(row=0, column=1, pady=20)
        
        # Main content
        main_container = ctk.CTkScrollableFrame(self, fg_color=Theme.BACKGROUND)
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Summary section
        self.create_summary_section(main_container)
        
        # Export options
        self.create_export_section(main_container)
        
        # Preview section
        self.create_preview_section(main_container)
    
    def create_summary_section(self, parent):
        """Tạo phần tóm tắt"""
        summary_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(summary_frame, text="📈 Tóm tắt kết quả", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(summary_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=30, pady=(0, 30))
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r.get("Trạng thái") == "Tốt")
        warning_tests = sum(1 for r in self.results.values() if r.get("Trạng thái") == "Cảnh báo")
        failed_tests = sum(1 for r in self.results.values() if r.get("Trạng thái") == "Lỗi")
        success_rate = (passed_tests/total_tests*100) if total_tests > 0 else 0
        
        stats = [
            ("📋", "Tổng Test", str(total_tests), Theme.ACCENT),
            ("✅", "Đạt", str(passed_tests), Theme.SUCCESS),
            ("⚠️", "Cảnh báo", str(warning_tests), Theme.WARNING),
            ("❌", "Lỗi", str(failed_tests), Theme.ERROR)
        ]
        
        for i, (icon, label, value, color) in enumerate(stats):
            stat_card = ctk.CTkFrame(stats_grid, fg_color=Theme.BACKGROUND, corner_radius=8)
            stat_card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(stat_card, text=icon, font=("Segoe UI", 24)).pack(pady=(15, 5))
            ctk.CTkLabel(stat_card, text=value, font=("Segoe UI", 28, "bold"), 
                        text_color=color).pack()
            ctk.CTkLabel(stat_card, text=label, font=Theme.BODY_FONT, 
                        text_color=Theme.TEXT_SECONDARY).pack(pady=(0, 15))
        
        # Success rate
        rate_frame = ctk.CTkFrame(summary_frame, fg_color="#E3F2FD", corner_radius=8)
        rate_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        ctk.CTkLabel(rate_frame, text=f"🎯 Tỷ lệ thành công: {success_rate:.1f}%", 
                    font=Theme.SUBHEADING_FONT, text_color="#1565C0").pack(pady=15)
    
    def create_export_section(self, parent):
        """Tạo phần xuất báo cáo"""
        export_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        export_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(export_frame, text="💾 Xuất báo cáo", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        # Export options grid
        export_grid = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_grid.pack(fill="x", padx=30, pady=(0, 30))
        export_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        # HTML Report
        html_card = ctk.CTkFrame(export_grid, fg_color=Theme.BACKGROUND, corner_radius=8)
        html_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(html_card, text="🌐", font=("Segoe UI", 32)).pack(pady=(20, 10))
        ctk.CTkLabel(html_card, text="Báo cáo HTML", font=Theme.SUBHEADING_FONT).pack()
        ctk.CTkLabel(html_card, text="Báo cáo web đầy đủ với biểu đồ", 
                    font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY, 
                    wraplength=200, justify="center").pack(pady=10)
        ctk.CTkButton(html_card, text="Xuất HTML", command=self.export_html,
                     fg_color=Theme.SUCCESS, height=Theme.BUTTON_HEIGHT).pack(pady=(0, 20))
        
        # JSON Export
        json_card = ctk.CTkFrame(export_grid, fg_color=Theme.BACKGROUND, corner_radius=8)
        json_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(json_card, text="📄", font=("Segoe UI", 32)).pack(pady=(20, 10))
        ctk.CTkLabel(json_card, text="Dữ liệu JSON", font=Theme.SUBHEADING_FONT).pack()
        ctk.CTkLabel(json_card, text="Dữ liệu thô để phân tích", 
                    font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY,
                    wraplength=200, justify="center").pack(pady=10)
        ctk.CTkButton(json_card, text="Xuất JSON", command=self.export_json,
                     fg_color=Theme.ACCENT, height=Theme.BUTTON_HEIGHT).pack(pady=(0, 20))
        
        # CSV Export
        csv_card = ctk.CTkFrame(export_grid, fg_color=Theme.BACKGROUND, corner_radius=8)
        csv_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(csv_card, text="📊", font=("Segoe UI", 32)).pack(pady=(20, 10))
        ctk.CTkLabel(csv_card, text="Bảng tính CSV", font=Theme.SUBHEADING_FONT).pack()
        ctk.CTkLabel(csv_card, text="Mở bằng Excel/Sheets", 
                    font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY,
                    wraplength=200, justify="center").pack(pady=10)
        ctk.CTkButton(csv_card, text="Xuất CSV", command=self.export_csv,
                     fg_color=Theme.WARNING, height=Theme.BUTTON_HEIGHT).pack(pady=(0, 20))
    
    def create_preview_section(self, parent):
        """Tạo phần xem trước"""
        preview_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        preview_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(preview_frame, text="👁️ Xem trước báo cáo", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=(30, 20))
        
        # Preview content
        preview_content = ctk.CTkScrollableFrame(preview_frame, height=400)
        preview_content.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        for test_name, result in self.results.items():
            status = result.get("Trạng thái", "Không rõ")
            result_text = result.get("Kết quả", "N/A")
            
            # Status color
            status_colors = {"Tốt": Theme.SUCCESS, "Cảnh báo": Theme.WARNING, "Lỗi": Theme.ERROR}
            status_color = status_colors.get(status, Theme.TEXT_SECONDARY)
            
            # Result item
            result_item = ctk.CTkFrame(preview_content, fg_color=Theme.BACKGROUND, corner_radius=8)
            result_item.pack(fill="x", pady=5)
            
            item_content = ctk.CTkFrame(result_item, fg_color="transparent")
            item_content.pack(fill="x", padx=20, pady=15)
            item_content.grid_columnconfigure(1, weight=1)
            
            # Status indicator
            status_indicator = ctk.CTkFrame(item_content, fg_color=status_color, width=4, height=40, corner_radius=2)
            status_indicator.grid(row=0, column=0, padx=(0, 15), sticky="ns")
            
            # Content
            content_frame = ctk.CTkFrame(item_content, fg_color="transparent")
            content_frame.grid(row=0, column=1, sticky="ew")
            
            ctk.CTkLabel(content_frame, text=test_name, font=Theme.SUBHEADING_FONT, 
                        text_color=Theme.TEXT).pack(anchor="w")
            ctk.CTkLabel(content_frame, text=f"Trạng thái: {status} | Kết quả: {result_text}", 
                        font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(anchor="w")
    
    def export_html(self):
        """Xuất báo cáo HTML"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Lưu báo cáo HTML"
        )
        
        if filepath:
            try:
                html_content = self.report_generator.generate_html_report(self.results)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Thành công", f"Đã xuất báo cáo HTML: {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất HTML: {e}")
    
    def export_json(self):
        """Xuất dữ liệu JSON"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Lưu dữ liệu JSON"
        )
        
        if filepath:
            try:
                self.report_generator.export_json(self.results, filepath)
                messagebox.showinfo("Thành công", f"Đã xuất JSON: {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất JSON: {e}")
    
    def export_csv(self):
        """Xuất bảng tính CSV"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Lưu bảng tính CSV"
        )
        
        if filepath:
            try:
                self.report_generator.export_csv(self.results, filepath)
                messagebox.showinfo("Thành công", f"Đã xuất CSV: {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất CSV: {e}")

if __name__ == "__main__":
    # Test report system
    app = ctk.CTk()
    app.title("Report System Test")
    app.geometry("1200x800")
    
    # Sample results
    sample_results = {
        "Định danh phần cứng": {"Trạng thái": "Tốt", "Kết quả": "Đã lấy thông tin", "Chi tiết": "CPU: Intel i5, RAM: 8GB"},
        "Kiểm tra màn hình": {"Trạng thái": "Tốt", "Kết quả": "Không có pixel chết"},
        "Kiểm tra pin": {"Trạng thái": "Cảnh báo", "Kết quả": "Pin chai 75%"},
        "Kiểm tra ổ cứng": {"Trạng thái": "Lỗi", "Kết quả": "Có bad sector"}
    }
    
    frame = ReportFrame(app, sample_results)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()