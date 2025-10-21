# Advanced Report Generator for LaptopTester
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from ui_improvements import ModernTheme, ModernCard

class ReportGeneratorFrame(ctk.CTkFrame):
    """Advanced report generator with multiple export formats"""
    
    def __init__(self, parent, results_data):
        super().__init__(parent, fg_color=ModernTheme.BACKGROUND)
        self.results = results_data
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_report_content()
        self.create_export_controls()
    
    def create_header(self):
        """Create report header"""
        header_frame = ctk.CTkFrame(self, fg_color=ModernTheme.PRIMARY, corner_radius=ModernTheme.RADIUS)
        header_frame.grid(row=0, column=0, sticky="ew", padx=ModernTheme.SPACE_LG, pady=(ModernTheme.SPACE_LG, ModernTheme.SPACE_MD))
        
        # Title and timestamp
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=ModernTheme.SPACE_XL, pady=ModernTheme.SPACE_LG)
        
        ctk.CTkLabel(
            title_frame,
            text="📊 BÁO CÁO KIỂM TRA LAPTOP",
            font=ModernTheme.FONT_TITLE,
            text_color="white"
        ).pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            font=ModernTheme.FONT_SUBHEADING,
            text_color="white"
        ).pack(side="right")
        
        # Summary stats
        stats = self.calculate_summary_stats()
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=ModernTheme.SPACE_XL, pady=(0, ModernTheme.SPACE_LG))
        
        stat_items = [
            ("Tổng Test", str(stats["total"])),
            ("Đạt", f"{stats['passed']}/{stats['total']}"),
            ("Tỷ Lệ", f"{stats['success_rate']:.1f}%")
        ]
        
        for i, (label, value) in enumerate(stat_items):
            stat_container = ctk.CTkFrame(stats_frame, fg_color="rgba(255,255,255,0.1)", corner_radius=8)
            stat_container.pack(side="left", padx=(0, ModernTheme.SPACE_MD) if i < len(stat_items)-1 else 0)
            
            ctk.CTkLabel(
                stat_container,
                text=label,
                font=ModernTheme.FONT_CAPTION,
                text_color="rgba(255,255,255,0.8)"
            ).pack(padx=ModernTheme.SPACE_MD, pady=(ModernTheme.SPACE_SM, 0))
            
            ctk.CTkLabel(
                stat_container,
                text=value,
                font=ModernTheme.FONT_SUBHEADING,
                text_color="white"
            ).pack(padx=ModernTheme.SPACE_MD, pady=(0, ModernTheme.SPACE_SM))
    
    def create_report_content(self):
        """Create main report content"""
        content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=ModernTheme.SURFACE,
            corner_radius=ModernTheme.RADIUS
        )
        content_frame.grid(row=1, column=0, sticky="nsew", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_MD))
        
        # Executive Summary
        self.create_executive_summary(content_frame)
        
        # Detailed Results
        self.create_detailed_results(content_frame)
        
        # Recommendations
        self.create_recommendations(content_frame)
        
        # Technical Details
        self.create_technical_details(content_frame)
    
    def create_executive_summary(self, parent):
        """Create executive summary section"""
        summary_card = ModernCard(
            parent,
            title="📋 Tóm Tắt Điều Hành",
            description="Đánh giá tổng quan về tình trạng laptop"
        )
        summary_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        stats = self.calculate_summary_stats()
        
        # Overall assessment
        if stats["success_rate"] >= 90:
            assessment = "✅ XUẤT SẮC"
            assessment_color = ModernTheme.SUCCESS
            assessment_desc = "Laptop trong tình trạng rất tốt, hoạt động ổn định và an toàn để sử dụng."
        elif stats["success_rate"] >= 75:
            assessment = "✅ TỐT"
            assessment_color = ModernTheme.SUCCESS
            assessment_desc = "Laptop hoạt động tốt với một số lưu ý nhỏ cần theo dõi."
        elif stats["success_rate"] >= 60:
            assessment = "⚠️ TRUNG BÌNH"
            assessment_color = ModernTheme.WARNING
            assessment_desc = "Laptop có một số vấn đề cần khắc phục trước khi sử dụng lâu dài."
        else:
            assessment = "❌ KÉM"
            assessment_color = ModernTheme.ERROR
            assessment_desc = "Laptop có nhiều vấn đề nghiêm trọng, không khuyến nghị mua."
        
        # Assessment display
        assessment_frame = ctk.CTkFrame(summary_card.content, fg_color=assessment_color, corner_radius=ModernTheme.RADIUS)
        assessment_frame.pack(fill="x", pady=ModernTheme.SPACE_MD)
        
        ctk.CTkLabel(
            assessment_frame,
            text=f"ĐÁNH GIÁ TỔNG THỂ: {assessment}",
            font=ModernTheme.FONT_HEADING,
            text_color="white"
        ).pack(pady=ModernTheme.SPACE_MD)
        
        ctk.CTkLabel(
            summary_card.content,
            text=assessment_desc,
            font=ModernTheme.FONT_BODY,
            text_color=ModernTheme.TEXT,
            wraplength=600
        ).pack(pady=ModernTheme.SPACE_MD)
        
        # Key findings
        findings_frame = ctk.CTkFrame(summary_card.content, fg_color=ModernTheme.BACKGROUND)
        findings_frame.pack(fill="x", pady=ModernTheme.SPACE_MD)
        
        ctk.CTkLabel(
            findings_frame,
            text="🔍 Phát Hiện Chính:",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.TEXT
        ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=(ModernTheme.SPACE_MD, ModernTheme.SPACE_SM))
        
        # Critical issues
        critical_issues = [name for name, result in self.results.items() 
                          if result.get("Trạng thái") == "Lỗi"]
        
        if critical_issues:
            ctk.CTkLabel(
                findings_frame,
                text=f"❌ Lỗi nghiêm trọng: {len(critical_issues)} vấn đề",
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.ERROR
            ).pack(anchor="w", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_XS)
        
        # Warnings
        warnings = [name for name, result in self.results.items() 
                   if result.get("Trạng thái") == "Cảnh báo"]
        
        if warnings:
            ctk.CTkLabel(
                findings_frame,
                text=f"⚠️ Cảnh báo: {len(warnings)} vấn đề",
                font=ModernTheme.FONT_BODY,
                text_color=ModernTheme.WARNING
            ).pack(anchor="w", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_XS)
        
        # Passed tests
        passed_tests = [name for name, result in self.results.items() 
                       if result.get("Trạng thái") == "Tốt"]
        
        ctk.CTkLabel(
            findings_frame,
            text=f"✅ Test đạt: {len(passed_tests)} mục",
            font=ModernTheme.FONT_BODY,
            text_color=ModernTheme.SUCCESS
        ).pack(anchor="w", padx=ModernTheme.SPACE_LG, pady=(ModernTheme.SPACE_XS, ModernTheme.SPACE_MD))
    
    def create_detailed_results(self, parent):
        """Create detailed results section"""
        results_card = ModernCard(
            parent,
            title="📊 Kết Quả Chi Tiết",
            description="Kết quả từng bước kiểm tra"
        )
        results_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Group results by category
        categories = {
            "Phần cứng": ["Định danh phần cứng", "Cấu hình hệ thống", "Sức khỏe ổ cứng", "CPU Stress Test", "GPU Stress Test"],
            "Giao diện": ["Kiểm tra màn hình", "Bàn phím & Touchpad", "Webcam", "Loa & Micro"],
            "Kết nối": ["Cổng kết nối", "Mạng & WiFi"],
            "Hệ thống": ["Bản quyền Windows", "Kiểm tra BIOS", "Pin laptop", "Kiểm tra ngoại hình"]
        }
        
        for category_name, test_names in categories.items():
            category_results = {name: result for name, result in self.results.items() 
                              if name in test_names}
            
            if not category_results:
                continue
            
            # Category header
            cat_frame = ctk.CTkFrame(results_card.content, fg_color=ModernTheme.BACKGROUND)
            cat_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
            
            ctk.CTkLabel(
                cat_frame,
                text=f"📁 {category_name}",
                font=ModernTheme.FONT_SUBHEADING,
                text_color=ModernTheme.PRIMARY
            ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
            
            # Category results
            for test_name, result in category_results.items():
                self.create_result_item(cat_frame, test_name, result)
    
    def create_result_item(self, parent, test_name, result):
        """Create individual result item"""
        item_frame = ctk.CTkFrame(parent, fg_color=ModernTheme.SURFACE, corner_radius=8)
        item_frame.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_XS)
        
        # Status colors and icons
        status = result.get("Trạng thái", "Không rõ")
        status_config = {
            "Tốt": ("✅", ModernTheme.SUCCESS),
            "Lỗi": ("❌", ModernTheme.ERROR),
            "Cảnh báo": ("⚠️", ModernTheme.WARNING),
            "Bỏ qua": ("⏭️", ModernTheme.TEXT_MUTED)
        }
        
        icon, color = status_config.get(status, ("❓", ModernTheme.TEXT_MUTED))
        
        # Header
        header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
        
        ctk.CTkLabel(
            header_frame,
            text=f"{icon} {test_name}",
            font=ModernTheme.FONT_BODY,
            text_color=ModernTheme.TEXT
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_frame,
            text=status,
            font=ModernTheme.FONT_BODY,
            text_color=color
        ).pack(side="right")
        
        # Details
        if result.get("Kết quả"):
            ctk.CTkLabel(
                item_frame,
                text=f"Kết quả: {result['Kết quả']}",
                font=ModernTheme.FONT_CAPTION,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=(0, ModernTheme.SPACE_SM))
    
    def create_recommendations(self, parent):
        """Create recommendations section"""
        rec_card = ModernCard(
            parent,
            title="💡 Khuyến Nghị",
            description="Đề xuất dựa trên kết quả kiểm tra"
        )
        rec_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        stats = self.calculate_summary_stats()
        recommendations = []
        
        # Generate recommendations based on results
        if stats["failed"] > 0:
            recommendations.append({
                "type": "critical",
                "title": "🔧 Khắc Phục Lỗi Nghiêm Trọng",
                "description": f"Có {stats['failed']} lỗi nghiêm trọng cần được khắc phục ngay lập tức trước khi sử dụng laptop."
            })
        
        if stats["warnings"] > 0:
            recommendations.append({
                "type": "warning",
                "title": "⚠️ Theo Dõi Cảnh Báo",
                "description": f"Có {stats['warnings']} cảnh báo cần được theo dõi trong quá trình sử dụng."
            })
        
        if stats["success_rate"] > 90:
            recommendations.append({
                "type": "success",
                "title": "✨ Laptop Chất Lượng Cao",
                "description": "Laptop trong tình trạng xuất sắc, an toàn để sử dụng cho mọi mục đích."
            })
        elif stats["success_rate"] > 70:
            recommendations.append({
                "type": "info",
                "title": "👍 Laptop Ổn Định",
                "description": "Laptop hoạt động tốt, phù hợp cho công việc văn phòng và giải trí."
            })
        else:
            recommendations.append({
                "type": "warning",
                "title": "⚠️ Cần Cân Nhắc Kỹ",
                "description": "Laptop có nhiều vấn đề, cần đánh giá kỹ lưỡng trước khi quyết định mua."
            })
        
        # Maintenance recommendations
        recommendations.append({
            "type": "info",
            "title": "🔧 Bảo Trì Định Kỳ",
            "description": "Thực hiện vệ sinh laptop, cập nhật driver và kiểm tra sức khỏe hệ thống định kỳ."
        })
        
        # Display recommendations
        for rec in recommendations:
            rec_colors = {
                "critical": ModernTheme.ERROR,
                "warning": ModernTheme.WARNING,
                "success": ModernTheme.SUCCESS,
                "info": ModernTheme.PRIMARY
            }
            
            rec_frame = ctk.CTkFrame(
                rec_card.content,
                fg_color=rec_colors.get(rec["type"], ModernTheme.PRIMARY),
                corner_radius=8
            )
            rec_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
            
            ctk.CTkLabel(
                rec_frame,
                text=rec["title"],
                font=ModernTheme.FONT_SUBHEADING,
                text_color="white"
            ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=(ModernTheme.SPACE_SM, 0))
            
            ctk.CTkLabel(
                rec_frame,
                text=rec["description"],
                font=ModernTheme.FONT_BODY,
                text_color="white",
                wraplength=600
            ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=(0, ModernTheme.SPACE_SM))
    
    def create_technical_details(self, parent):
        """Create technical details section"""
        tech_card = ModernCard(
            parent,
            title="🔧 Chi Tiết Kỹ Thuật",
            description="Thông tin kỹ thuật và metadata"
        )
        tech_card.pack(fill="x", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_LG)
        
        # Test environment
        env_frame = ctk.CTkFrame(tech_card.content, fg_color=ModernTheme.BACKGROUND)
        env_frame.pack(fill="x", pady=ModernTheme.SPACE_SM)
        
        ctk.CTkLabel(
            env_frame,
            text="🖥️ Môi Trường Test:",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.TEXT
        ).pack(anchor="w", padx=ModernTheme.SPACE_MD, pady=ModernTheme.SPACE_SM)
        
        import platform
        import psutil
        
        env_details = [
            f"Hệ điều hành: {platform.system()} {platform.release()}",
            f"Phiên bản Python: {platform.python_version()}",
            f"Thời gian test: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Tổng thời gian: ~{len(self.results) * 2} phút (ước tính)"
        ]
        
        for detail in env_details:
            ctk.CTkLabel(
                env_frame,
                text=f"• {detail}",
                font=ModernTheme.FONT_CAPTION,
                text_color=ModernTheme.TEXT_MUTED
            ).pack(anchor="w", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_XS)
    
    def create_export_controls(self):
        """Create export controls"""
        export_frame = ctk.CTkFrame(self, fg_color=ModernTheme.SURFACE, corner_radius=ModernTheme.RADIUS)
        export_frame.grid(row=2, column=0, sticky="ew", padx=ModernTheme.SPACE_LG, pady=(0, ModernTheme.SPACE_LG))
        
        ctk.CTkLabel(
            export_frame,
            text="📤 Xuất Báo Cáo",
            font=ModernTheme.FONT_SUBHEADING,
            text_color=ModernTheme.TEXT
        ).pack(side="left", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_MD)
        
        # Export buttons
        button_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=ModernTheme.SPACE_LG, pady=ModernTheme.SPACE_MD)
        
        export_options = [
            ("📄 PDF", self.export_pdf),
            ("📊 Excel", self.export_excel),
            ("💾 JSON", self.export_json),
            ("📋 Text", self.export_text)
        ]
        
        for text, command in export_options:
            ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                fg_color=ModernTheme.PRIMARY,
                hover_color=ModernTheme.PRIMARY_HOVER,
                width=100,
                height=ModernTheme.BUTTON_HEIGHT
            ).pack(side="left", padx=ModernTheme.SPACE_SM)
    
    def calculate_summary_stats(self):
        """Calculate summary statistics"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() 
                          if r.get("Trạng thái") == "Tốt")
        failed_tests = sum(1 for r in self.results.values() 
                          if r.get("Trạng thái") == "Lỗi")
        warnings = sum(1 for r in self.results.values() 
                      if r.get("Trạng thái") == "Cảnh báo")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warnings,
            "success_rate": success_rate
        }
    
    def export_pdf(self):
        """Export report as PDF"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Lưu báo cáo PDF"
            )
            
            if not filename:
                return
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor(ModernTheme.PRIMARY)
            )
            
            story.append(Paragraph("📊 BÁO CÁO KIỂM TRA LAPTOP", title_style))
            story.append(Paragraph(f"Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Summary
            stats = self.calculate_summary_stats()
            summary_data = [
                ['Tổng số test', str(stats["total"])],
                ['Test đạt', f"{stats['passed']}/{stats['total']}"],
                ['Tỷ lệ thành công', f"{stats['success_rate']:.1f}%"],
                ['Lỗi nghiêm trọng', str(stats["failed"])],
                ['Cảnh báo', str(stats["warnings"])]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(ModernTheme.PRIMARY)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Detailed results
            story.append(Paragraph("Chi tiết kết quả:", styles['Heading2']))
            
            for test_name, result in self.results.items():
                status = result.get("Trạng thái", "Không rõ")
                result_text = result.get("Kết quả", "")
                
                story.append(Paragraph(f"<b>{test_name}</b>: {status}", styles['Normal']))
                if result_text:
                    story.append(Paragraph(f"Kết quả: {result_text}", styles['Normal']))
                story.append(Spacer(1, 10))
            
            doc.build(story)
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo PDF: {filename}")
            
        except ImportError:
            messagebox.showerror("Lỗi", "Cần cài đặt reportlab: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất PDF: {str(e)}")
    
    def export_excel(self):
        """Export report as Excel"""
        try:
            import pandas as pd
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Lưu báo cáo Excel"
            )
            
            if not filename:
                return
            
            # Prepare data
            data = []
            for test_name, result in self.results.items():
                data.append({
                    'Tên Test': test_name,
                    'Trạng thái': result.get("Trạng thái", ""),
                    'Kết quả': result.get("Kết quả", ""),
                    'Chi tiết': result.get("Chi tiết", "")
                })
            
            df = pd.DataFrame(data)
            
            # Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Summary sheet
                stats = self.calculate_summary_stats()
                summary_data = {
                    'Thống kê': ['Tổng test', 'Đạt', 'Lỗi', 'Cảnh báo', 'Tỷ lệ thành công'],
                    'Giá trị': [stats["total"], stats["passed"], stats["failed"], 
                               stats["warnings"], f"{stats['success_rate']:.1f}%"]
                }
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Tổng quan', index=False)
                
                # Detailed results sheet
                df.to_excel(writer, sheet_name='Chi tiết', index=False)
            
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo Excel: {filename}")
            
        except ImportError:
            messagebox.showerror("Lỗi", "Cần cài đặt pandas và openpyxl: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất Excel: {str(e)}")
    
    def export_json(self):
        """Export report as JSON"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                title="Lưu báo cáo JSON"
            )
            
            if not filename:
                return
            
            report_data = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "version": "1.0",
                    "generator": "LaptopTester Pro"
                },
                "summary": self.calculate_summary_stats(),
                "results": self.results
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo JSON: {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất JSON: {str(e)}")
    
    def export_text(self):
        """Export report as plain text"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Lưu báo cáo Text"
            )
            
            if not filename:
                return
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("📊 BÁO CÁO KIỂM TRA LAPTOP\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
                
                # Summary
                stats = self.calculate_summary_stats()
                f.write("TỔNG QUAN:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Tổng số test: {stats['total']}\n")
                f.write(f"Test đạt: {stats['passed']}/{stats['total']}\n")
                f.write(f"Tỷ lệ thành công: {stats['success_rate']:.1f}%\n")
                f.write(f"Lỗi nghiêm trọng: {stats['failed']}\n")
                f.write(f"Cảnh báo: {stats['warnings']}\n\n")
                
                # Detailed results
                f.write("CHI TIẾT KẾT QUẢ:\n")
                f.write("-" * 30 + "\n")
                
                for test_name, result in self.results.items():
                    f.write(f"\n{test_name}:\n")
                    f.write(f"  Trạng thái: {result.get('Trạng thái', 'Không rõ')}\n")
                    if result.get("Kết quả"):
                        f.write(f"  Kết quả: {result['Kết quả']}\n")
                    if result.get("Chi tiết"):
                        f.write(f"  Chi tiết: {result['Chi tiết']}\n")
            
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo Text: {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất Text: {str(e)}")

# Export class
__all__ = ['ReportGeneratorFrame']