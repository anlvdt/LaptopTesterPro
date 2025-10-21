#!/usr/bin/env python3
"""
Export utilities for LaptopTester Pro
PDF and Excel report generation
"""

import os
import json
import datetime
from tkinter import filedialog, messagebox

def export_pdf_report(results, success_rate):
    """Generate professional PDF report"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.piecharts import Pie
        
        # File dialog
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
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                   fontSize=24, spaceAfter=30, alignment=1)
        story.append(Paragraph("BÁO CÁO KIỂM TRA LAPTOP", title_style))
        story.append(Paragraph(f"Ngày tạo: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [
            ['Tổng số test', str(len(results))],
            ['Test đạt', str(sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt"))],
            ['Test lỗi', str(sum(1 for r in results.values() if r.get("Trạng thái") == "Lỗi"))],
            ['Tỷ lệ thành công', f"{success_rate:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('GRID',(0,0),(-1,-1),1,colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed results
        story.append(Paragraph("Chi tiết kết quả:", styles['Heading2']))
        
        for step_name, result in results.items():
            status = result.get("Trạng thái", "Không rõ")
            status_color = colors.green if status == "Tốt" else colors.red if status == "Lỗi" else colors.orange
            
            step_style = ParagraphStyle('StepStyle', parent=styles['Normal'], 
                                      textColor=status_color, fontSize=12)
            story.append(Paragraph(f"• {step_name}: {status}", step_style))
            
            if result.get("Kết quả"):
                story.append(Paragraph(f"  → {result['Kết quả']}", styles['Normal']))
        
        doc.build(story)
        messagebox.showinfo("Thành công", f"Đã xuất báo cáo PDF: {filename}")
        
    except ImportError:
        messagebox.showerror("Lỗi", "Cần cài đặt: pip install reportlab")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo PDF: {e}")

def export_excel_report(results, success_rate):
    """Generate Excel report"""
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
        for step_name, result in results.items():
            data.append({
                'Bước kiểm tra': step_name,
                'Trạng thái': result.get("Trạng thái", "Không rõ"),
                'Kết quả': result.get("Kết quả", ""),
                'Chi tiết': result.get("Chi tiết", "")
            })
        
        df = pd.DataFrame(data)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Kết quả test', index=False)
            
            # Summary sheet
            summary_df = pd.DataFrame({
                'Thông số': ['Tổng test', 'Đạt', 'Lỗi', 'Tỷ lệ thành công'],
                'Giá trị': [len(results), 
                           sum(1 for r in results.values() if r.get("Trạng thái") == "Tốt"),
                           sum(1 for r in results.values() if r.get("Trạng thái") == "Lỗi"),
                           f"{success_rate:.1f}%"]
            })
            summary_df.to_excel(writer, sheet_name='Tổng kết', index=False)
        
        messagebox.showinfo("Thành công", f"Đã xuất báo cáo Excel: {filename}")
        
    except ImportError:
        messagebox.showerror("Lỗi", "Cần cài đặt: pip install pandas openpyxl")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo Excel: {e}")

def save_test_history(results, success_rate):
    """Save test history to JSON"""
    try:
        history_dir = os.path.join(os.path.dirname(__file__), "history")
        os.makedirs(history_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = os.path.join(history_dir, f"test_{timestamp}.json")
        
        history_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "success_rate": success_rate,
            "results": results
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
            
        return history_file
    except Exception as e:
        print(f"Cannot save history: {e}")
        return None

def load_test_history():
    """Load test history"""
    try:
        history_dir = os.path.join(os.path.dirname(__file__), "history")
        if not os.path.exists(history_dir):
            return []
        
        history_files = []
        for file in os.listdir(history_dir):
            if file.endswith('.json'):
                file_path = os.path.join(history_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        history_files.append(data)
                except:
                    continue
        
        return sorted(history_files, key=lambda x: x.get('timestamp', ''), reverse=True)
    except:
        return []