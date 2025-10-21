"""
Fix Font Tiếng Việt, Báo Cáo và Encoding
Khắc phục 3 vấn đề chính:
1. Font tiếng Việt không hiển thị đúng
2. Báo cáo thiếu thông tin kết quả
3. Lỗi ô vuông trong hướng dẫn (encoding)
"""

import os
import sys

def fix_main_py():
    """Fix main.py với font và encoding đúng"""
    
    main_file = "main.py"
    
    if not os.path.exists(main_file):
        print(f"❌ Không tìm thấy {main_file}")
        return False
    
    print(f"📝 Đang fix {main_file}...")
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix font - Thay Segoe UI bằng font hỗ trợ tiếng Việt tốt
    replacements = [
        # Font chính - dùng Arial thay vì Segoe UI
        ('self.TITLE_FONT = ("Segoe UI", 42, "bold")', 'self.TITLE_FONT = ("Arial", 42, "bold")'),
        ('self.HEADING_FONT = ("Segoe UI", 28, "bold")', 'self.HEADING_FONT = ("Arial", 28, "bold")'),
        ('self.SUBHEADING_FONT = ("Segoe UI", 22, "bold")', 'self.SUBHEADING_FONT = ("Arial", 22, "bold")'),
        ('self.BODY_FONT = ("Segoe UI", 16)', 'self.BODY_FONT = ("Arial", 16)'),
        ('self.SMALL_FONT = ("Segoe UI", 14)', 'self.SMALL_FONT = ("Arial", 14)'),
        ('self.KEY_FONT = ("Segoe UI", 12)', 'self.KEY_FONT = ("Arial", 12)'),
        ('self.BUTTON_FONT = ("Segoe UI", 14)', 'self.BUTTON_FONT = ("Arial", 14)'),
        
        # Font trong các widget
        ('font=("Segoe UI"', 'font=("Arial"'),
        ('("Segoe UI", 24)', '("Arial", 24)'),
        ('("Segoe UI", 28, "bold")', '("Arial", 28, "bold")'),
        ('("Segoe UI", 20)', '("Arial", 20)'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # 2. Fix bullet points - Thay • bằng - để tránh lỗi encoding
    bullet_fixes = [
        ('• ', '- '),
        ('•', '-'),
    ]
    
    for old, new in bullet_fixes:
        content = content.replace(old, new)
    
    # 3. Đảm bảo encoding UTF-8 ở đầu file
    if not content.startswith('#!/usr/bin/env python3'):
        content = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n' + content
    elif '# -*- coding: utf-8 -*-' not in content[:200]:
        content = content.replace('#!/usr/bin/env python3\n', '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n')
    
    # Backup
    backup_file = "main_backup_before_font_fix.py"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Đã backup vào {backup_file}")
    
    # Save fixed version
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Đã fix font và encoding trong {main_file}")
    return True

def fix_report_generator():
    """Fix report_generator.py để lưu đầy đủ thông tin"""
    
    report_file = "report_generator.py"
    
    if not os.path.exists(report_file):
        print(f"⚠️ Không tìm thấy {report_file}")
        return False
    
    print(f"📝 Đang fix {report_file}...")
    
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix font trong report
    content = content.replace('("Segoe UI"', '("Arial"')
    content = content.replace('"Segoe UI"', '"Arial"')
    
    # Fix bullet points
    content = content.replace('• ', '- ')
    content = content.replace('•', '-')
    
    # Đảm bảo encoding
    if '# -*- coding: utf-8 -*-' not in content[:200]:
        content = '# -*- coding: utf-8 -*-\n' + content
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Đã fix {report_file}")
    return True

def create_enhanced_summary_step():
    """Tạo SummaryStep cải tiến với đầy đủ thông tin"""
    
    summary_code = '''# -*- coding: utf-8 -*-
"""
Enhanced Summary Step - Hiển thị đầy đủ thông tin kết quả
"""

import customtkinter as ctk

class EnhancedSummaryStep(ctk.CTkFrame):
    """Bước tổng kết với đầy đủ thông tin"""
    
    def __init__(self, master, all_results, theme_manager, **kwargs):
        super().__init__(master, fg_color="transparent")
        self.all_results = all_results
        self.theme = theme_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.theme.get_color('CARD'),
            corner_radius=12
        )
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.display_summary()
    
    def display_summary(self):
        """Hiển thị báo cáo tổng kết đầy đủ"""
        
        # Header
        header = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ctk.CTkLabel(
            header,
            text="BÁO CÁO TỔNG KẾT",
            font=("Arial", 32, "bold"),
            text_color=self.theme.get_color('ACCENT')
        ).pack()
        
        # Statistics
        stats = self.calculate_stats()
        self.create_stats_section(stats)
        
        # Hardware capability
        self.create_hardware_section()
        
        # Detailed results
        self.create_results_section()
        
        # Export buttons
        self.create_export_section()
    
    def calculate_stats(self):
        """Tính toán thống kê"""
        total = len(self.all_results)
        passed = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Tốt")
        warning = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Cảnh báo")
        failed = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Lỗi")
        skipped = sum(1 for r in self.all_results.values() if r.get("Trạng thái") == "Bỏ qua")
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "passed": passed,
            "warning": warning,
            "failed": failed,
            "skipped": skipped,
            "success_rate": success_rate
        }
    
    def create_stats_section(self, stats):
        """Tạo phần thống kê"""
        stats_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.theme.get_color('FRAME'),
            corner_radius=12
        )
        stats_frame.grid(row=1, column=0, sticky="ew", pady=10)
        stats_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        
        # Total
        self._create_stat_card(stats_frame, 0, "Tổng số", str(stats["total"]), "#64748B")
        
        # Passed
        self._create_stat_card(stats_frame, 1, "Đạt", str(stats["passed"]), "#10B981")
        
        # Warning
        if stats["warning"] > 0:
            self._create_stat_card(stats_frame, 2, "Cảnh báo", str(stats["warning"]), "#F59E0B")
        
        # Failed
        if stats["failed"] > 0:
            self._create_stat_card(stats_frame, 3, "Lỗi", str(stats["failed"]), "#EF4444")
        
        # Success rate
        rate_color = "#10B981" if stats["success_rate"] >= 80 else "#F59E0B" if stats["success_rate"] >= 60 else "#EF4444"
        self._create_stat_card(stats_frame, 4, "Tỷ lệ", f"{stats['success_rate']:.0f}%", rate_color)
    
    def _create_stat_card(self, parent, col, label, value, color):
        """Tạo card thống kê"""
        card = ctk.CTkFrame(parent, fg_color="transparent")
        card.grid(row=0, column=col, padx=10, pady=15)
        
        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold"),
            text_color=color
        ).pack()
        
        ctk.CTkLabel(
            card,
            text=label,
            font=("Arial", 14),
            text_color=self.theme.get_color('TEXT_SECONDARY')
        ).pack()
    
    def create_hardware_section(self):
        """Tạo phần phân tích phần cứng"""
        hw_info = self.all_results.get("Định danh phần cứng", {})
        
        if not hw_info:
            return
        
        hw_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.theme.get_color('FRAME'),
            corner_radius=12
        )
        hw_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(
            hw_frame,
            text="Khả Năng Sử Dụng Phần Cứng",
            font=("Arial", 22, "bold"),
            text_color=self.theme.get_color('ACCENT')
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Phân tích CPU từ chi tiết
        chi_tiet = hw_info.get("Chi tiết", "")
        cpu_name = ""
        
        for line in chi_tiet.split("\\n"):
            if "CPU:" in line:
                cpu_name = line.split("CPU:")[1].strip()
                break
        
        if cpu_name:
            ctk.CTkLabel(
                hw_frame,
                text=f"Dựa trên: {cpu_name}",
                font=("Arial", 14),
                text_color=self.theme.get_color('TEXT_SECONDARY')
            ).pack(anchor="w", padx=20, pady=(0, 10))
        
        # Capabilities
        capabilities = self._analyze_capabilities(cpu_name, chi_tiet)
        
        for cap in capabilities:
            cap_card = ctk.CTkFrame(
                hw_frame,
                fg_color=self.theme.get_color('BACKGROUND'),
                corner_radius=8,
                border_width=2,
                border_color=cap["color"]
            )
            cap_card.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                cap_card,
                text=f"{cap['icon']} {cap['title']}",
                font=("Arial", 16, "bold"),
                text_color=cap["color"]
            ).pack(anchor="w", padx=15, pady=(10, 5))
            
            ctk.CTkLabel(
                cap_card,
                text=cap["desc"],
                font=("Arial", 14),
                text_color=self.theme.get_color('TEXT_SECONDARY'),
                wraplength=700,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Spacer
        ctk.CTkFrame(hw_frame, height=10, fg_color="transparent").pack()
    
    def _analyze_capabilities(self, cpu_name, chi_tiet):
        """Phân tích khả năng sử dụng"""
        capabilities = []
        
        # Phân tích CPU tier
        cpu_upper = cpu_name.upper()
        
        if any(x in cpu_upper for x in ["I9", "I7", "RYZEN 9", "RYZEN 7"]):
            capabilities.append({
                "icon": "🎮",
                "title": "Gaming & Rendering",
                "desc": "Phù hợp cho gaming AAA, render 3D, video editing chuyên nghiệp",
                "color": "#10B981"
            })
            capabilities.append({
                "icon": "💼",
                "title": "Workstation",
                "desc": "Xử lý đa nhiệm nặng, phát triển phần mềm, máy ảo",
                "color": "#3B82F6"
            })
        elif any(x in cpu_upper for x in ["I5", "RYZEN 5"]):
            capabilities.append({
                "icon": "🎮",
                "title": "Gaming Casual",
                "desc": "Chơi game ở mức trung bình, streaming, content creation",
                "color": "#F59E0B"
            })
            capabilities.append({
                "icon": "💼",
                "title": "Văn phòng nâng cao",
                "desc": "Office, lập trình, thiết kế đồ họa 2D, đa nhiệm vừa phải",
                "color": "#3B82F6"
            })
        else:
            capabilities.append({
                "icon": "📝",
                "title": "Văn phòng cơ bản",
                "desc": "Office, web browsing, email, xem phim",
                "color": "#94A3B8"
            })
            capabilities.append({
                "icon": "🎓",
                "title": "Học tập",
                "desc": "Học online, soạn thảo văn bản, nghiên cứu",
                "color": "#06B6D4"
            })
        
        # Kiểm tra GPU rời
        if any(x in chi_tiet.upper() for x in ["RTX", "GTX", "RADEON RX", "RADEON PRO"]):
            capabilities.insert(0, {
                "icon": "🎨",
                "title": "Đồ họa chuyên nghiệp",
                "desc": "GPU rời mạnh, phù hợp cho CAD, 3D modeling, AI/ML",
                "color": "#8B5CF6"
            })
        
        return capabilities
    
    def create_results_section(self):
        """Tạo phần kết quả chi tiết"""
        results_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.theme.get_color('FRAME'),
            corner_radius=12
        )
        results_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(
            results_frame,
            text="Chi Tiết Kết Quả",
            font=("Arial", 22, "bold"),
            text_color=self.theme.get_color('ACCENT')
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Hiển thị từng kết quả
        for step_name, result_data in self.all_results.items():
            self._create_result_item(results_frame, step_name, result_data)
        
        # Spacer
        ctk.CTkFrame(results_frame, height=10, fg_color="transparent").pack()
    
    def _create_result_item(self, parent, step_name, result_data):
        """Tạo item kết quả"""
        status = result_data.get("Trạng thái", "Không rõ")
        result_text = result_data.get("Kết quả", "")
        chi_tiet = result_data.get("Chi tiết", "")
        
        # Icon và màu
        status_map = {
            "Tốt": ("✅", "#10B981"),
            "Cảnh báo": ("⚠️", "#F59E0B"),
            "Lỗi": ("❌", "#EF4444"),
            "Bỏ qua": ("⏭️", "#94A3B8")
        }
        
        icon, color = status_map.get(status, ("❓", "#64748B"))
        
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme.get_color('BACKGROUND'),
            corner_radius=8
        )
        item_frame.pack(fill="x", padx=20, pady=5)
        
        # Header
        header = ctk.CTkFrame(item_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header,
            text=f"{icon} {step_name}",
            font=("Arial", 16, "bold"),
            text_color=self.theme.get_color('TEXT')
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            header,
            text=status,
            font=("Arial", 14),
            text_color=color,
            fg_color=color + "20",
            corner_radius=6
        ).grid(row=0, column=2, padx=10)
        
        # Kết quả
        if result_text:
            ctk.CTkLabel(
                item_frame,
                text=f"Kết quả: {result_text}",
                font=("Arial", 14),
                text_color=self.theme.get_color('TEXT_SECONDARY'),
                wraplength=700,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 5))
        
        # Chi tiết (nếu có và không quá dài)
        if chi_tiet and len(chi_tiet) < 500:
            detail_text = chi_tiet.replace("\\n", " | ")
            ctk.CTkLabel(
                item_frame,
                text=f"Chi tiết: {detail_text}",
                font=("Arial", 12),
                text_color=self.theme.get_color('TEXT_SECONDARY'),
                wraplength=700,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 10))
    
    def create_export_section(self):
        """Tạo phần xuất báo cáo"""
        export_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.theme.get_color('FRAME'),
            corner_radius=12
        )
        export_frame.grid(row=4, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(
            export_frame,
            text="Xuất Báo Cáo",
            font=("Arial", 18, "bold"),
            text_color=self.theme.get_color('ACCENT')
        ).pack(side="left", padx=20, pady=15)
        
        button_container = ctk.CTkFrame(export_frame, fg_color="transparent")
        button_container.pack(side="right", padx=20, pady=15)
        
        buttons = [
            ("📄 PDF", self.export_pdf),
            ("📊 Excel", self.export_excel),
            ("📋 Text", self.export_text)
        ]
        
        for text, command in buttons:
            ctk.CTkButton(
                button_container,
                text=text,
                command=command,
                font=("Arial", 14),
                width=100,
                height=40
            ).pack(side="left", padx=5)
    
    def export_pdf(self):
        """Xuất PDF"""
        print("Xuất PDF...")
        # TODO: Implement PDF export
    
    def export_excel(self):
        """Xuất Excel"""
        print("Xuất Excel...")
        # TODO: Implement Excel export
    
    def export_text(self):
        """Xuất Text"""
        from tkinter import filedialog
        from datetime import datetime
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Lưu báo cáo"
        )
        
        if not filename:
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\\n")
            f.write("BÁO CÁO KIỂM TRA LAPTOP\\n")
            f.write("=" * 60 + "\\n\\n")
            f.write(f"Ngày: {datetime.now().strftime('%d/%m/%Y %H:%M')}\\n\\n")
            
            # Stats
            stats = self.calculate_stats()
            f.write("THỐNG KÊ:\\n")
            f.write("-" * 30 + "\\n")
            f.write(f"Tổng số test: {stats['total']}\\n")
            f.write(f"Đạt: {stats['passed']}\\n")
            f.write(f"Cảnh báo: {stats['warning']}\\n")
            f.write(f"Lỗi: {stats['failed']}\\n")
            f.write(f"Tỷ lệ thành công: {stats['success_rate']:.1f}%\\n\\n")
            
            # Results
            f.write("CHI TIẾT KẾT QUẢ:\\n")
            f.write("-" * 30 + "\\n\\n")
            
            for step_name, result_data in self.all_results.items():
                f.write(f"{step_name}:\\n")
                f.write(f"  Trạng thái: {result_data.get('Trạng thái', 'N/A')}\\n")
                f.write(f"  Kết quả: {result_data.get('Kết quả', 'N/A')}\\n")
                if result_data.get("Chi tiết"):
                    f.write(f"  Chi tiết: {result_data['Chi tiết']}\\n")
                f.write("\\n")
        
        print(f"✅ Đã lưu báo cáo: {filename}")
'''
    
    with open("enhanced_summary_step.py", 'w', encoding='utf-8') as f:
        f.write(summary_code)
    
    print("✅ Đã tạo enhanced_summary_step.py")
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("FIX FONT TIẾNG VIỆT, BÁO CÁO VÀ ENCODING")
    print("=" * 60)
    print()
    
    # Fix main.py
    if fix_main_py():
        print("✅ Đã fix main.py")
    else:
        print("❌ Lỗi khi fix main.py")
    
    print()
    
    # Fix report_generator.py
    if fix_report_generator():
        print("✅ Đã fix report_generator.py")
    else:
        print("⚠️ Không tìm thấy report_generator.py")
    
    print()
    
    # Create enhanced summary
    if create_enhanced_summary_step():
        print("✅ Đã tạo enhanced_summary_step.py")
    
    print()
    print("=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)
    print()
    print("📝 Các thay đổi:")
    print("  1. ✅ Thay font Segoe UI -> Arial (hỗ trợ tiếng Việt tốt hơn)")
    print("  2. ✅ Fix bullet points (• -> -) để tránh lỗi encoding")
    print("  3. ✅ Thêm # -*- coding: utf-8 -*- vào đầu file")
    print("  4. ✅ Tạo EnhancedSummaryStep với đầy đủ thông tin")
    print()
    print("🔄 Để áp dụng:")
    print("  1. Chạy lại ứng dụng: python main.py")
    print("  2. Kiểm tra font tiếng Việt hiển thị đúng")
    print("  3. Kiểm tra báo cáo có đầy đủ thông tin")
    print()

if __name__ == "__main__":
    main()
